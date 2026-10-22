"""Versioned migrations of the stored data. They run once at start-up, after an automatic backup."""

import logging

log = logging.getLogger(__name__)

SCHEMA_VERSION = 2

# Commands that moved into another command in 1.4.0: old root name -> new command text
MOVED = {
    "birthdaysetup": "birthday setup",
    "suggestionsetup": "suggestion setup",
    "notifytopic": "notify topic",
    "modmailsetup": "modmail setup",
    "appealsetup": "appeal setup",
    "reportsetup": "report setup",
    "levelrole": "xp levelrole",
}


def v2_moved_commands(store):
    """Commands that were merged into groups: rewrite aliases and drop rules that no longer point to a command."""
    for gid, cfg in store.config.items():
        changed = False
        aliases = cfg.get("aliases")
        if isinstance(aliases, dict):
            for alias, text in list(aliases.items()):
                head, _, rest = str(text).partition(" ")
                if head in MOVED:
                    aliases[alias] = (MOVED[head] + " " + rest).strip()
                    changed = True
        for key in ("disabled_commands",):
            lst = cfg.get(key)
            if isinstance(lst, list):
                keep = [c for c in lst if c not in MOVED]
                if len(keep) != len(lst):
                    log.warning("server %s: disabled command(s) %s were merged into other commands and are enabled again", gid, [c for c in lst if c in MOVED])
                    cfg[key] = keep
                    changed = True
        perms = cfg.get("perms")
        if isinstance(perms, dict):
            for old in [k for k in perms if k in MOVED]:
                log.warning("server %s: the permission rule for /%s was removed because it is now /%s. Set it again with /admin perms if needed", gid, old, MOVED[old])
                del perms[old]
                changed = True
        if changed:
            store.t_cfg.add(gid)


MIGRATIONS = [(2, v2_moved_commands)]


def run(store):
    """Bring the stored data to the current version. Refuses to start on data from a newer version."""
    raw = store.get_meta("schema_version")
    current = int(raw) if raw else (SCHEMA_VERSION if not store.config else 1)
    if current > SCHEMA_VERSION:
        raise RuntimeError(f"the database has schema version {current}, this GuardBot only knows {SCHEMA_VERSION}. Update GuardBot instead of going back to an older version.")
    pending = [(v, fn) for v, fn in MIGRATIONS if v > current]
    if pending:
        path = store.backup("pre-migration")
        log.info("database backup before migration: %s", path.name)
    for version, fn in pending:
        log.info("migrating the data to schema version %d (%s)", version, fn.__name__)
        fn(store)
        store.set_meta("schema_version", str(version))
    if raw is None or str(SCHEMA_VERSION) != raw:
        store.set_meta("schema_version", str(SCHEMA_VERSION))
