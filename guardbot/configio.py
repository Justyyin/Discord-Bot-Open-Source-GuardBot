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
