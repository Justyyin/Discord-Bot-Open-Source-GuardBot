"""SQLite storage with in-memory caches and change detection. The settings of a server are stored one row per section, so a change writes only that section."""

import asyncio
import copy
import json
import logging
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Optional

from . import migrations
from .defaults import DEFAULTS

log = logging.getLogger(__name__)


def fill(d: dict, default: dict) -> None:
    """Add missing keys of a default dict to a settings dict, including nested ones."""
    for k, v in default.items():
        if k not in d:
            d[k] = copy.deepcopy(v)
        elif isinstance(v, dict) and v:
            fill(d[k], v)


def dumps(obj: Any) -> str:
    """Serialize to compact JSON."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def verify_backup(path: Any) -> dict[str, int]:
    """Open a backup read-only, run the SQLite integrity check and return the number of rows per table. Raises RuntimeError when the file is not a healthy GuardBot database."""
    try:
        db = sqlite3.connect(f"file:{Path(path).as_posix()}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        raise RuntimeError(f"cannot open {path}: {exc}") from exc
    try:
        try:
            result = [r[0] for r in db.execute("PRAGMA integrity_check")]
            if result != ["ok"]:
                raise RuntimeError("integrity check failed: " + "; ".join(result)[:300])
            return Store.counts(db)
        except sqlite3.Error as exc:
            raise RuntimeError(f"not a GuardBot database: {exc}") from exc
    finally:
        db.close()


class Touched:
    """Collects the keys of changed rows over two periods so late edits are not lost."""
    def __init__(self) -> None:
        """Start with empty sets for the current and the previous period."""
        self.now: set = set()
        self.prev: set = set()

    def add(self, key: Any) -> None:
        """Remember that a key changed."""
        self.now.add(key)

    def take(self) -> set:
        """Return the keys changed in this and the previous period and start a new period."""
        out = self.now | self.prev
        self.prev, self.now = self.now, set()
        return out


class Store:
    """SQLite backed storage with in-memory caches and change detection."""
    def __init__(self, directory: Any) -> None:
        """Open the database, load all data and import old JSON files."""
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.dir / "guardbot.db", check_same_thread=False)
        self.lock = threading.Lock()
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=NORMAL")
        self.db.executescript(
            "CREATE TABLE IF NOT EXISTS config(gid TEXT PRIMARY KEY, data TEXT NOT NULL);"
            "CREATE TABLE IF NOT EXISTS config_sections(gid TEXT NOT NULL, section TEXT NOT NULL, data TEXT NOT NULL, PRIMARY KEY(gid, section));"
            "CREATE TABLE IF NOT EXISTS users(gid TEXT NOT NULL, uid TEXT NOT NULL, data TEXT NOT NULL, PRIMARY KEY(gid, uid));"
            "CREATE TABLE IF NOT EXISTS cases(gid TEXT NOT NULL, id INTEGER NOT NULL, data TEXT NOT NULL, PRIMARY KEY(gid, id));"
            "CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);"
        )
        self.config: dict[str, dict] = {}
        self.user_data: dict[str, dict[str, dict]] = {}
        self.case_data: dict[str, list[dict]] = {}
        self.saved: dict[tuple, int] = {}
        self.t_cfg, self.t_users, self.t_cases = Touched(), Touched(), Touched()
        self.filled: set[str] = set()
        self.section_names: dict[str, set[str]] = {}
        try:
            self._load()
            self._migrate()
            migrations.run(self)
        except BaseException:
            self.db.close()
            raise

    def _load(self) -> None:
        """Read all rows from the database into memory."""
        for gid, data in self.db.execute("SELECT gid, data FROM config"):
            self.config[gid] = json.loads(data)
        seen = set()
        for gid, section, data in self.db.execute("SELECT gid, section, data FROM config_sections"):
            if gid not in seen:
                seen.add(gid)
                self.config[gid] = {}
            self.config[gid][section] = json.loads(data)
            self.saved[("c", gid, section)] = hash(data)
            self.section_names.setdefault(gid, set()).add(section)
        for gid, uid, data in self.db.execute("SELECT gid, uid, data FROM users"):
            self.user_data.setdefault(gid, {})[uid] = json.loads(data)
            self.saved[("u", gid, uid)] = hash(data)
        for gid, cid, data in self.db.execute("SELECT gid, id, data FROM cases ORDER BY id"):
            self.case_data.setdefault(gid, []).append(json.loads(data))
            self.saved[("k", gid, cid)] = hash(data)

    def _migrate(self) -> None:
        """Import the old JSON files once and rename them."""
        for name in ("config", "users", "cases"):
            p = self.dir / f"{name}.json"
            if not p.exists():
                continue
            try:
                old = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                log.warning("cannot import %s, it is not valid JSON: %s", p.name, exc)
                continue
            target: Any = {"config": self.config, "users": self.user_data, "cases": self.case_data}[name]
            if target:
                continue
            for gid, value in old.items():
                target[gid] = value
                {"config": self.t_cfg, "users": self.t_users, "cases": self.t_cases}[name].add(gid)
                if name == "users":
                    self.t_users.now.discard(gid)
                    for uid in value:
                        self.t_users.add((gid, uid))
            p.replace(p.with_suffix(".json.migrated"))
        self.flush()

    def mark(self, *names: str) -> None:
        """Kept for old callers. Changes are detected automatically, so this does nothing."""
        return None

    def cfg(self, gid: Any) -> dict:
        """Return the settings dict of a server, filled with defaults."""
        gid = str(gid)
        g = self.config.setdefault(gid, {})
        if gid not in self.filled:
            fill(g, DEFAULTS)
            self.filled.add(gid)
        self.t_cfg.add(gid)
        return g

    def users(self, gid: Any) -> dict[str, dict]:
        """Return all stored user records of a server."""
        return self.user_data.setdefault(str(gid), {})

    def user(self, gid: Any, uid: Any) -> dict:
        """Return the record of one user and create it if needed."""
        gid, uid = str(gid), str(uid)
        rec = self.user_data.setdefault(gid, {}).setdefault(uid, {"xp": 0, "birthday": None, "bday_last": None})
        self.t_users.add((gid, uid))
        return rec

    def cases(self, gid: Any) -> list[dict]:
        """Return the moderation cases of a server."""
        gid = str(gid)
        self.t_cases.add(gid)
        return self.case_data.setdefault(gid, [])

    def delete_case(self, gid: Any, case_id: int) -> bool:
        """Remove one moderation case from memory and the database. Returns False if it does not exist."""
        gid = str(gid)
        cases = self.case_data.get(gid, [])
        before = len(cases)
        self.case_data[gid] = [c for c in cases if c["id"] != case_id]
        self.saved.pop(("k", gid, case_id), None)
        with self.lock, self.db:
            self.db.execute("DELETE FROM cases WHERE gid=? AND id=?", (gid, case_id))
        return len(self.case_data[gid]) < before

    def delete_user(self, gid: Any, uid: Any) -> None:
        """Delete the record of a user from memory and the database."""
        gid, uid = str(gid), str(uid)
        self.user_data.get(gid, {}).pop(uid, None)
        self.saved.pop(("u", gid, uid), None)
        with self.lock, self.db:
            self.db.execute("DELETE FROM users WHERE gid=? AND uid=?", (gid, uid))

    def drop_guild(self, gid: Any) -> None:
        """Delete every stored row of a server."""
        gid = str(gid)
        self.config.pop(gid, None)
        self.user_data.pop(gid, None)
        self.case_data.pop(gid, None)
        self.filled.discard(gid)
        self.section_names.pop(gid, None)
        self.saved = {k: v for k, v in self.saved.items() if k[1] != gid}
        with self.lock, self.db:
            for table in ("config", "config_sections", "users", "cases"):
                self.db.execute(f"DELETE FROM {table} WHERE gid=?", (gid,))

    def get_meta(self, key: str) -> Optional[str]:
        """Read a value from the meta table."""
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

    def set_meta(self, key: str, value: str) -> None:
        """Write a value to the meta table."""
        with self.lock, self.db:
            self.db.execute("INSERT INTO meta(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))

    def snapshot(self) -> dict[str, list[tuple]]:
        """Serialize everything that changed since the last write and skip unchanged rows."""
        rows: dict[str, list[tuple]] = {"c": [], "cd": [], "u": [], "k": []}
        for gid in self.t_cfg.take():
            cfg = self.config.get(gid)
            if cfg is None:
                continue
            known = self.section_names.setdefault(gid, set())
            for section, value in cfg.items():
                text = dumps(value)
                key = ("c", gid, section)
                if self.saved.get(key) != hash(text):
                    self.saved[key] = hash(text)
                    known.add(section)
                    rows["c"].append((gid, section, text))
            for section in known - set(cfg):
                known.discard(section)
                self.saved.pop(("c", gid, section), None)
                rows["cd"].append((gid, section))
        for gid, uid in self.t_users.take():
            rec = self.user_data.get(gid, {}).get(uid)
            if rec is not None:
                text = dumps(rec)
                if self.saved.get(("u", gid, uid)) != hash(text):
                    self.saved[("u", gid, uid)] = hash(text)
                    rows["u"].append((gid, uid, text))
        for gid in self.t_cases.take():
            for case in self.case_data.get(gid, []):
                text = dumps(case)
                key = ("k", gid, case["id"])
                if self.saved.get(key) != hash(text):
                    self.saved[key] = hash(text)
                    rows["k"].append((gid, case["id"], text))
        return rows

    def write(self, rows: dict[str, list[tuple]]) -> None:
        """Write serialized rows to the database in one transaction."""
        if not any(rows.values()):
            return
        with self.lock, self.db:
            self.db.executemany("INSERT INTO config_sections(gid, section, data) VALUES(?, ?, ?) ON CONFLICT(gid, section) DO UPDATE SET data=excluded.data", rows["c"])
            self.db.executemany("DELETE FROM config_sections WHERE gid=? AND section=?", rows["cd"])
            self.db.executemany("INSERT INTO users(gid, uid, data) VALUES(?, ?, ?) ON CONFLICT(gid, uid) DO UPDATE SET data=excluded.data", rows["u"])
            self.db.executemany("INSERT INTO cases(gid, id, data) VALUES(?, ?, ?) ON CONFLICT(gid, id) DO UPDATE SET data=excluded.data", rows["k"])

    def flush(self) -> None:
        """Save all changes now."""
        self.write(self.snapshot())

    async def aflush(self) -> None:
        """Save all changes without blocking the event loop."""
        rows = self.snapshot()
        if any(rows.values()):
            await asyncio.to_thread(self.write, rows)

    def state(self, name: str) -> Any:
        """Read a small piece of runtime state (counters, queues) that should survive a restart. Returns None if there is none."""
        raw = self.get_meta(f"state:{name}")
        try:
            return json.loads(raw) if raw else None
        except ValueError:
            log.warning("state %s is damaged and was ignored", name)
            return None

    def set_state(self, name: str, value: Any) -> None:
        """Save runtime state. None removes it."""
        key = f"state:{name}"
        if value is None:
            with self.lock, self.db:
                self.db.execute("DELETE FROM meta WHERE key=?", (key,))
        else:
            self.set_meta(key, dumps(value))

    def backup(self, label: str = "auto", keep: int = 0, verify: bool = True) -> Path:
        """Copy the database to data/dbbackups with SQLite's online backup and check the copy. With keep > 0 only that many automatic backups stay. A copy that fails the check is deleted and an error is raised."""
        self.flush()
        folder = self.dir / "dbbackups"
        folder.mkdir(exist_ok=True)
        dest = folder / f"guardbot-{time.strftime('%Y%m%d-%H%M%S')}-{label}.db"
        target = sqlite3.connect(dest)
        try:
            with self.lock:
                self.db.backup(target)
                expected = self.counts(self.db)
        finally:
            target.close()
        if verify:
            problem = None
            try:
                found = verify_backup(dest)
                if found != expected:
                    problem = f"the backup has {found}, the database had {expected}"
            except RuntimeError as exc:
                problem = str(exc)
            if problem:
                dest.unlink(missing_ok=True)
                raise RuntimeError(f"the backup failed its check: {problem}")
        if keep > 0:
            old = sorted(folder.glob("guardbot-*-auto.db"))
            for f in old[:-keep]:
                f.unlink()
        return dest

    @staticmethod
    def counts(db: sqlite3.Connection) -> dict[str, int]:
        """Number of rows in the data tables."""
        out = {}
        for table in ("config_sections", "users", "cases"):
            try:
                out[table] = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            except sqlite3.OperationalError:  # a backup made before this table existed
                out[table] = 0
        return out

    def integrity(self) -> list[str]:
        """Run the SQLite integrity check and return its messages."""
        with self.lock:
            return [r[0] for r in self.db.execute("PRAGMA integrity_check")]

    def file_size(self) -> int:
        """Return the size of the database file and its write-ahead log in bytes."""
        total = 0
        for suffix in ("", "-wal"):
            f = self.dir / f"guardbot.db{suffix}"
            total += f.stat().st_size if f.exists() else 0
        return total

    def vacuum(self) -> None:
        """Save pending changes, then rebuild the database file to free unused space."""
        self.flush()
        with self.lock:
            self.db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            self.db.execute("VACUUM")

    def close(self) -> None:
        """Save everything and close the database."""
        for t in (self.t_cfg, self.t_users, self.t_cases):
            t.prev = t.now | t.prev
        self.flush()
        self.flush()
        self.db.close()
