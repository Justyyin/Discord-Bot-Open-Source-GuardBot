"""Migrations, runtime state, database backups, heartbeat and the status page."""

import asyncio
import json
import sqlite3
import tempfile
import time
import unittest
from collections import deque
from pathlib import Path
from types import SimpleNamespace as NS

from discord.ext import commands

from guardbot import migrations
from guardbot.core import Bot, Store
from guardbot.health import StatusServer, heartbeat_fresh, snapshot, write_heartbeat
from guardbot.utils import export_hits, import_hits


class StoreCase(unittest.TestCase):
    """A store in a temporary folder."""

    def setUp(self):
        """Open a store."""
        self.dir = tempfile.mkdtemp()
        self.store = Store(self.dir)

    def tearDown(self):
        """Close it."""
        self.store.close()


class MigrationTest(unittest.TestCase):
    """Versioned migrations."""

    def old_store(self):
        """A store that looks like one made by version 1.3.0."""
        d = tempfile.mkdtemp()
        db = sqlite3.connect(Path(d) / "guardbot.db")
        db.executescript(
            "CREATE TABLE config(gid TEXT PRIMARY KEY, data TEXT NOT NULL);"
            "CREATE TABLE users(gid TEXT NOT NULL, uid TEXT NOT NULL, data TEXT NOT NULL, PRIMARY KEY(gid, uid));"
            "CREATE TABLE cases(gid TEXT NOT NULL, id INTEGER NOT NULL, data TEXT NOT NULL, PRIMARY KEY(gid, id));"
            "CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);"
        )
        cfg = {"aliases": {"bs": "birthdaysetup set enabled:True", "w": "warn"}, "disabled_commands": ["levelrole", "ban"], "perms": {"modmailsetup": {"roles": [1]}, "ban": {"roles": [2]}}}
        db.execute("INSERT INTO config VALUES('1', ?)", (json.dumps(cfg),))
        db.commit()
        db.close()
        return d

    def test_every_schema_version_has_exactly_one_migration(self):
        """SCHEMA_VERSION equals the highest migration and no number is missing or used twice."""
        from guardbot import migrations
        numbers = [v for v, _ in migrations.MIGRATIONS]
        self.assertEqual(numbers, list(range(2, migrations.SCHEMA_VERSION + 1)))

    def test_old_settings_row_becomes_section_rows(self):
        """Version 3 writes one row per section and removes the old per-server row."""
        d = self.old_store()
        store = Store(d)
        store.close()
        db = sqlite3.connect(Path(d) / "guardbot.db")
        try:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM config").fetchone()[0], 0)
            sections = {r[0] for r in db.execute("SELECT section FROM config_sections WHERE gid='1'")}
            self.assertTrue({"aliases", "perms", "disabled_commands"} <= sections)
        finally:
            db.close()

    def test_old_data_is_migrated_and_backed_up(self):
        """Moved commands are rewritten in aliases and dropped from rules, and a backup is made first."""
        d = self.old_store()
        store = Store(d)
        try:
            cfg = store.config["1"]
            self.assertEqual(cfg["aliases"]["bs"], "birthday setup set enabled:True")
            self.assertEqual(cfg["aliases"]["w"], "warn")
            self.assertEqual(cfg["disabled_commands"], ["ban"])
            self.assertEqual(list(cfg["perms"]), ["ban"])
            self.assertEqual(store.get_meta("schema_version"), str(migrations.SCHEMA_VERSION))
            self.assertTrue(list((Path(d) / "dbbackups").glob("*pre-migration.db")))
        finally:
            store.close()

    def test_fresh_database_gets_the_current_version_without_backup(self):
        """A new database starts at the latest version."""
        d = tempfile.mkdtemp()
        store = Store(d)
        try:
            self.assertEqual(store.get_meta("schema_version"), str(migrations.SCHEMA_VERSION))
            self.assertFalse((Path(d) / "dbbackups").exists())
        finally:
            store.close()

    def test_newer_database_is_refused(self):
        """Data from a newer version is not touched by an older program."""
        d = tempfile.mkdtemp()
        store = Store(d)
        store.set_meta("schema_version", str(migrations.SCHEMA_VERSION + 1))
        store.close()
        with self.assertRaises(RuntimeError):
            Store(d)


class StateTest(StoreCase):
    """Runtime state and backups."""

    def test_state_roundtrip(self):
        """State is saved, read back and removed."""
        self.store.set_state("x", {"a": [1, 2]})
        self.assertEqual(self.store.state("x"), {"a": [1, 2]})
        self.store.set_state("x", None)
        self.assertIsNone(self.store.state("x"))

    def test_damaged_state_is_ignored(self):
        """Broken JSON does not stop the bot."""
        self.store.set_meta("state:x", "{broken")
        self.assertIsNone(self.store.state("x"))

    def test_backup_is_a_valid_database_and_old_ones_are_pruned(self):
        """The backup opens as SQLite with the data in it, and only the newest automatic ones stay."""
        self.store.cfg(1)["prefix"] = "?"
        path = self.store.backup("manual")
        db = sqlite3.connect(path)
        self.assertEqual(json.loads(db.execute("SELECT data FROM config_sections WHERE gid='1' AND section='prefix'").fetchone()[0]), "?")
        db.close()
        folder = self.store.dir / "dbbackups"
        for n in range(4):
            (folder / f"guardbot-20200101-00000{n}-auto.db").write_bytes(b"x")
        self.store.backup("auto", keep=2)
        self.assertEqual(len(list(folder.glob("*-auto.db"))), 2)
        self.assertTrue(path.exists(), "manual backups are never pruned")


class HitsTest(unittest.TestCase):
    """Counters that survive a restart."""

    def test_export_import_drops_old_entries(self):
        """Only timestamps inside the window are kept."""
        now = time.time()
        hits = {(1, 2, "ban"): deque([now - 10, now - 5000]), (1, 3, "kick"): deque([now - 9999])}
        raw = export_hits(hits, lambda key: 100, now)
        self.assertEqual(list(raw), ["1|2|ban"])
        back = import_hits(raw, lambda key: 100, lambda p: (int(p[0]), int(p[1]), p[2]), now)
        self.assertEqual(len(back[(1, 2, "ban")]), 1)

    def test_damaged_input_is_skipped(self):
        """Wrong keys and values do not raise."""
        back = import_hits({"x": [1], "1|2|ban": ["no"], "a|b|c": [time.time()]}, lambda k: 100, lambda p: (int(p[0]), int(p[1]), p[2]))
        self.assertEqual(back, {})


class HealthTest(unittest.IsolatedAsyncioTestCase):
    """Heartbeat and status page."""

    def test_heartbeat(self):
        """A fresh file is healthy, an old or missing one is not."""
        path = Path(tempfile.mkdtemp()) / "heartbeat"
        self.assertFalse(heartbeat_fresh(path))
        write_heartbeat(path)
        self.assertTrue(heartbeat_fresh(path))
        self.assertFalse(heartbeat_fresh(path, now=time.time() + 500))

    async def test_status_server_answers_and_shows_only_counts(self):
        """The page returns JSON without names and 503 when not ready."""
        bot = NS(latency=0.05, is_ready=lambda: True, started=time.time() - 5, guilds=[1, 2], shard_count=2, settings={"health_port": 18765})
        server = StatusServer(bot)
        await server.start()
        try:
            import aiohttp

            async with aiohttp.ClientSession() as s:
                async with s.get("http://127.0.0.1:18765/health") as r:
                    data = await r.json()
                    self.assertEqual((r.status, data["status"], data["servers"], data["shards"]), (200, "ok", 2, 2))
                    self.assertEqual(set(data), {"status", "version", "ready", "uptime_seconds", "latency_ms", "servers", "shards"})
            bot.is_ready = lambda: False
            async with aiohttp.ClientSession() as s:
                async with s.get("http://127.0.0.1:18765/health") as r:
                    self.assertEqual(r.status, 503)
        finally:
            await server.stop()

    def test_snapshot_handles_missing_latency(self):
        """A disconnected bot has no latency and is degraded."""
        bot = NS(latency=float("inf"), is_ready=lambda: True, started=time.time(), guilds=[], shard_count=None)
        data = snapshot(bot)
        self.assertEqual((data["status"], data["latency_ms"]), ("degraded", None))

    def test_off_by_default(self):
        """Without health_port nothing is started."""
        server = StatusServer(NS(settings={}))
        asyncio.run(server.start())
        self.assertIsNone(server.runner)


class BotShape(unittest.TestCase):
    """The bot class."""

    def test_bot_uses_shards(self):
        """The bot can run on several shards."""
        self.assertTrue(issubclass(Bot, commands.AutoShardedBot))


if __name__ == "__main__":
    unittest.main()
