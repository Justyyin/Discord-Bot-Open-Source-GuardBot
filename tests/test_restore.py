"""Backups are checked when they are made, and restoring them brings the data back."""

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import restore_db  # noqa: E402
from guardbot.health import write_heartbeat  # noqa: E402
from guardbot.store import Store, verify_backup  # noqa: E402


def fill(store):
    """Some settings, users and cases."""
    store.cfg(1)["prefix"] = "?"
    store.cfg(1)["xp"]["enabled"] = False
    store.cfg(2)["language"] = "de"
    store.user(1, 5)["xp"] = 123
    store.cases(1).append({"id": 1, "type": "warn", "user": 5, "user_name": "x", "active": True})
    store.set_state("thing", {"a": 1})


class RestoreTest(unittest.TestCase):
    def test_backup_restore_round_trip(self):
        d = Path(tempfile.mkdtemp())
        store = Store(d)
        fill(store)
        backup = store.backup("manual")
        store.cfg(1)["prefix"] = "changed after the backup"
        store.user(1, 5)["xp"] = 999
        store.close()
        message = restore_db.restore(backup, d)
        self.assertIn("healthy", message)
        self.assertTrue(list((d / "dbbackups").glob("*-before-restore.db")))
        again = Store(d)
        self.assertEqual(again.cfg(1)["prefix"], "?")
        self.assertFalse(again.cfg(1)["xp"]["enabled"])
        self.assertEqual(again.cfg(2)["language"], "de")
        self.assertEqual(again.user(1, 5)["xp"], 123)
        self.assertEqual(again.cases(1)[0]["type"], "warn")
        self.assertEqual(again.state("thing"), {"a": 1})
        again.close()

    def test_every_backup_is_checked_and_counted(self):
        d = Path(tempfile.mkdtemp())
        store = Store(d)
        fill(store)
        path = store.backup("manual")
        counts = verify_backup(path)
        self.assertEqual(counts["users"], 1)
        self.assertEqual(counts["cases"], 1)
        self.assertGreater(counts["config_sections"], 10)
        store.close()

    def test_a_damaged_file_is_refused(self):
        d = Path(tempfile.mkdtemp())
        bad = d / "bad.db"
        bad.write_bytes(b"this is not a database" * 100)
        with self.assertRaises(RuntimeError):
            verify_backup(bad)
        with self.assertRaises(RuntimeError):
            restore_db.restore(bad, d)

    def test_a_truncated_backup_is_refused(self):
        d = Path(tempfile.mkdtemp())
        store = Store(d)
        fill(store)
        path = store.backup("manual")
        store.close()
        data = path.read_bytes()
        path.write_bytes(data[: len(data) // 2])
        with self.assertRaises(RuntimeError):
            verify_backup(path)

    def test_restore_refuses_while_the_bot_runs(self):
        d = Path(tempfile.mkdtemp())
        store = Store(d)
        fill(store)
        path = store.backup("manual")
        store.close()
        write_heartbeat(d / "heartbeat")
        with self.assertRaises(RuntimeError) as ctx:
            restore_db.restore(path, d)
        self.assertIn("running", str(ctx.exception))
        self.assertIn("healthy", restore_db.restore(path, d, check_only=True))

    def test_backup_from_before_section_rows_can_be_restored(self):
        """A backup made by 1.5.1 has one settings row per server. It is checked, restored and migrated when opened."""
        d = Path(tempfile.mkdtemp())
        old = d / "old.db"
        db = sqlite3.connect(old)
        db.executescript(
            "CREATE TABLE config(gid TEXT PRIMARY KEY, data TEXT NOT NULL);"
            "CREATE TABLE users(gid TEXT NOT NULL, uid TEXT NOT NULL, data TEXT NOT NULL, PRIMARY KEY(gid, uid));"
            "CREATE TABLE cases(gid TEXT NOT NULL, id INTEGER NOT NULL, data TEXT NOT NULL, PRIMARY KEY(gid, id));"
            "CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);"
            "INSERT INTO config VALUES('1', '{\"prefix\": \"%\"}');"
            "INSERT INTO meta VALUES('schema_version', '2');"
        )
        db.commit()
        db.close()
        target = d / "data"
        target.mkdir()
        restore_db.restore(old, target)
        store = Store(target)
        self.assertEqual(store.cfg(1)["prefix"], "%")
        store.close()

    def test_failed_start_puts_the_previous_database_back(self):
        d = Path(tempfile.mkdtemp())
        store = Store(d)
        fill(store)
        good = store.backup("manual")
        store.close()
        broken = d / "future.db"
        broken.write_bytes(good.read_bytes())
        db = sqlite3.connect(broken)
        db.execute("INSERT INTO meta VALUES('schema_version', '999') ON CONFLICT(key) DO UPDATE SET value='999'")
        db.commit()
        db.close()
        with self.assertRaises(RuntimeError) as ctx:
            restore_db.restore(broken, d)
        self.assertIn("put back", str(ctx.exception))
        again = Store(d)
        self.assertEqual(again.cfg(1)["prefix"], "?")
        again.close()


if __name__ == "__main__":
    unittest.main()
