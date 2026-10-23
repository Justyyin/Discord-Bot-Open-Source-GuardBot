"""Export and import of the server settings with validation."""

import copy

from . import __version__
from .defaults import DEFAULTS, PROTECTED_COMMANDS

HEADER = "guardbot_config"
MAX_BYTES = 1_000_000

# Runtime state that is not part of the portable settings. Paths use dots.
RUNTIME = (
    "case_counter", "lockdown", "polls", "giveaways", "reminders", "starboard.posts", "tickets.open", "tickets.counter",
    "suggestions.items", "suggestions.next", "modmail.open", "appeals.items", "appeals.last", "appeals.next", "jail.timed",
    "mod.tempbans", "verify.pending", "tempvoice.rooms", "tempvoice.owners", "counting.count", "counting.last_user",
    "counting.record", "automod.hits", "reports.seen", "reports.next", "debug.usage", "debug.errors", "debug.last_hash", "activity.days",
    "approval.items", "approval.next", "watchlist.items", "archive.reported", "archive.last_scan", "temproles.items", "history", "team.stats",
    "team.week", "team.last_report", "team.away", "team.assigned", "applications.items", "applications.next", "applications.last", "rules.message", "rules.changed",
)


def _get(d, path):
    """Return (parent, key) for a dotted path, or (None, None) when it does not exist."""
    parts = path.split(".")
    for part in parts[:-1]:
        d = d.get(part) if isinstance(d, dict) else None
        if d is None:
            return None, None
    return (d, parts[-1]) if isinstance(d, dict) and parts[-1] in d else (None, None)


def export_config(cfg):
    """Return the portable settings of a server as a dict ready for JSON."""
    out = copy.deepcopy(cfg)
    for path in RUNTIME:
        parent, key = _get(out, path)
        if parent is not None:
            del parent[key]
    return {HEADER: 1, "version": __version__, "settings": out}


def _kind(value):
    """Name the JSON type of a value in a way that treats ints and floats alike."""
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    return type(value).__name__


def validate(data, default=None, path=""):
    """Compare imported settings with the defaults and return a list of problems. Empty means valid."""
    default = DEFAULTS if default is None else default
    problems = []
    if not isinstance(data, dict):
        return [f"{path or 'settings'} must be an object"]
    for key, value in data.items():
        here = f"{path}.{key}" if path else key
        if key not in default:
            if default:
                problems.append(f"unknown setting {here}")
            continue
        ref = default[key]
        if ref is None:
            if isinstance(value, (dict, list)):
                problems.append(f"{here} must be a single value")
        elif isinstance(ref, dict):
            if not isinstance(value, dict):
                problems.append(f"{here} must be an object")
            elif ref:
                problems.extend(validate(value, ref, here))
        elif _kind(value) != _kind(ref) and value is not None:
            problems.append(f"{here} must be a {_kind(ref)}")
    if not path:
        bad = [c for c in data.get("disabled_commands", []) if c in PROTECTED_COMMANDS]
        if bad:
            problems.append("protected commands cannot be disabled: " + ", ".join(bad))
    return problems


def _merge(base, over, default):
    """Overlay imported values onto a settings dict. Fixed groups merge key by key, free-form groups are replaced."""
    for key, value in over.items():
        if isinstance(value, dict) and isinstance(default.get(key), dict) and default[key]:
            _merge(base.setdefault(key, {}), value, default[key])
        else:
            base[key] = copy.deepcopy(value)


def apply_import(current, payload):
    """Build the new settings from a payload: defaults, then the imported values, then the runtime state of the server."""
    new = copy.deepcopy(DEFAULTS)
    _merge(new, payload["settings"], DEFAULTS)
    for path in RUNTIME:
        parent, key = _get(current, path)
        if parent is not None:
            target = new
            parts = path.split(".")
            for part in parts[:-1]:
                target = target.setdefault(part, {})
            target[parts[-1]] = copy.deepcopy(parent[key])
    return new


def parse(raw):
    """Decode an uploaded file. Returns (payload, problems)."""
    import json

    if len(raw) > MAX_BYTES:
        return None, ["the file is larger than 1 MB"]
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None, ["the file is not valid JSON"]
    if not isinstance(payload, dict) or payload.get(HEADER) != 1 or not isinstance(payload.get("settings"), dict):
        return None, ["this is not a GuardBot settings file"]
    problems = validate(payload["settings"])
    return payload, problems


# Sections that are not copied between servers or tracked in the history
LOCAL_ONLY = ("history", "team", "debug", "dashboard_access", "appeals", "case_counter", "applications")
MIN_ID = 10 ** 15


def sections(cfg):
    """The portable sections of a server as {name: value}, without runtime state."""
    return {k: v for k, v in export_config(cfg)["settings"].items() if k not in LOCAL_ONLY}


def restore(current, section, before):
    """Put a section back to an earlier value. The runtime state inside the section (open tickets, counters) stays as it is now."""
    new = copy.deepcopy(before)
    for path in RUNTIME:
        parts = path.split(".")
        if parts[0] != section or len(parts) < 2:
            continue
        parent, key = _get(current, path)
        if parent is None:
            continue
        target = new
        for part in parts[1:-1]:
            target = target.setdefault(part, {})
        target[parts[-1]] = copy.deepcopy(parent[key])
    fill_missing(new, DEFAULTS.get(section))
    current[section] = new
    return new


def fill_missing(value, default):
    """Add settings that an older copy does not have, with their defaults."""
    if not isinstance(value, dict) or not isinstance(default, dict):
        return
    for key, ref in default.items():
        if key not in value:
            value[key] = copy.deepcopy(ref)
        else:
            fill_missing(value[key], ref)


def remap(value, mapping):
    """Replace channel and role IDs in a settings value with the IDs of another server. IDs without a counterpart are dropped (None, removed from lists and dicts). Returns (new value, mapped count, dropped count)."""
    counts = [0, 0]

    def big(x):
        """True for something that looks like a Discord ID."""
        return isinstance(x, int) and not isinstance(x, bool) and x >= MIN_ID

    def walk(v):
        """Rebuild a value with new IDs."""
        if big(v):
            if v in mapping:
                counts[0] += 1
                return mapping[v]
            counts[1] += 1
            return None
        if isinstance(v, list):
            out = []
            for x in v:
                new = walk(x)
                if new is not None or not big(x):
                    out.append(new)
            return out
        if isinstance(v, dict):
            out = {}
            for k, x in v.items():
                if isinstance(k, str) and k.isdigit() and int(k) >= MIN_ID:
                    if int(k) not in mapping:
                        counts[1] += 1
                        continue
                    counts[0] += 1
                    k = str(mapping[int(k)])
                out[k] = walk(x)
            return out
        return v

    return walk(value), counts[0], counts[1]


def id_map(source, target):
    """Match channels, categories and roles of two servers by name and type. @everyone maps to @everyone."""
    mapping = {source.default_role.id: target.default_role.id}
    roles = {}
    for r in target.roles:
        roles.setdefault(r.name.casefold(), r.id)
    for r in source.roles:
        if r.name.casefold() in roles and not r.is_default():
            mapping[r.id] = roles[r.name.casefold()]
    channels = {}
    for c in target.channels:
        channels.setdefault((c.name.casefold(), str(c.type)), c.id)
    for c in source.channels:
        key = (c.name.casefold(), str(c.type))
        if key in channels:
            mapping[c.id] = channels[key]
    return mapping


# Which settings section holds the setup of a module. Modules that are not listed use the section with their own name.
# None means the module needs no setup.
MODULE_SECTIONS = {
    "logging": ("log", "log_options"), "moderation": ("mod",), "leveling": ("xp",), "reactionroles": ("reaction_roles",),
    "verification": ("verify",), "rolemenu": ("rolemenus",), "duty": ("team",), "structure": ("roletemplates",),
    "info": None, "announce": None, "utility": None, "builder": None, "privacy": None, "exceptions": ("exceptions",),
}


def module_status(cfg):
    """For every module: whether it is on and whether its settings differ from the defaults.

    The result is {module: (on, setup)} where setup is "done" (settings were changed), "open" (still the defaults) or "none" (nothing to set up).
    """
    from .store import fill

    fresh = {}
    fill(fresh, DEFAULTS)
    mine, base = export_config(cfg)["settings"], export_config(fresh)["settings"]
    out = {}
    for name, on in cfg["modules"].items():
        sections = MODULE_SECTIONS.get(name, (name,))
        if sections is None:
            out[name] = (on, "none")
        else:
            changed = any(mine.get(s) != base.get(s) for s in sections if s in base)
            out[name] = (on, "done" if changed else "open")
    return out
