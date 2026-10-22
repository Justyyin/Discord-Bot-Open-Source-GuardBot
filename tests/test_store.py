"""Storage: persistence, change detection, migration and deletion."""

import json
import tempfile
import unittest
from pathlib import Path

from guardbot.core import Store


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def test_roundtrip(self):
        s = Store(self.dir)
        s.cfg(1)["prefix"] = "?"
        s.user(1, 5)["xp"] = 42
        s.cases(1).append({"id": 1, "type": "warn", "user": 5, "user_name": "x", "active": True})
        s.close()
        s = Store(self.dir)
        self.assertEqual(s.cfg(1)["prefix"], "?")
        self.assertEqual(s.user(1, 5)["xp"], 42)
        self.assertEqual(len(s.cases(1)), 1)
        s.close()

    def test_defaults_are_filled_for_old_data(self):
        s = Store(self.dir)
        s.config["7"] = {"prefix": "!"}
        self.assertIn("verification", s.cfg(7)["modules"])
        self.assertEqual(s.cfg(7)["lockdown"]["mode"], "channels")
        s.close()

    def test_unchanged_rows_are_not_written_again(self):
        s = Store(self.dir)
        s.cfg(1)["prefix"] = "!"
        s.flush()
        s.cfg(1)
        rows = s.snapshot()
        self.assertEqual(sum(len(v) for v in rows.values()), 0)
        s.close()

    def test_modified_case_is_saved(self):
        s = Store(self.dir)
        s.cases(1).append({"id": 1, "type": "warn", "user": 5, "user_name": "x", "active": True})
        s.flush()
        s.cases(1)[0]["active"] = False
        s.close()
        s = Store(self.dir)
        self.assertFalse(s.cases(1)[0]["active"])
        s.close()

    def test_json_migration(self):
        Path(self.dir, "config.json").write_text(json.dumps({"1": {"prefix": "%"}}))
        Path(self.dir, "users.json").write_text(json.dumps({"1": {"9": {"xp": 3, "birthday": None, "bday_last": None}}}))
        s = Store(self.dir)
        self.assertEqual(s.cfg(1)["prefix"], "%")
        self.assertEqual(s.user(1, 9)["xp"], 3)
        self.assertTrue(Path(self.dir, "config.json.migrated").exists())
        s.close()

    def test_delete_user_and_guild(self):
        s = Store(self.dir)
        s.user(1, 5)["xp"] = 1
        s.delete_user(1, 5)
        self.assertNotIn("5", s.users(1))
        s.cfg(1)
        s.drop_guild(1)
        self.assertEqual(s.config, {})
        s.close()

    def test_meta(self):
        s = Store(self.dir)
        s.set_meta("a", "b")
        self.assertEqual(s.get_meta("a"), "b")
        self.assertIsNone(s.get_meta("missing"))
        s.close()


if __name__ == "__main__":
    unittest.main()
