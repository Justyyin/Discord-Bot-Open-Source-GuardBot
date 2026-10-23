"""Pure helper functions of the tools, tags and channels cogs."""

import unittest
from types import SimpleNamespace as NS

from guardbot.cogs.server.channels import parse_count, render_template
from guardbot.cogs.community.tags import match_trigger
from guardbot.cogs.tools.tools import parse_color, purge_check


class HelperTest(unittest.TestCase):
    """Tests for functions that need no Discord connection."""

    def test_parse_count(self):
        """Only a leading number counts."""
        self.assertEqual(parse_count("42"), 42)
        self.assertEqual(parse_count("42 nice"), 42)
        self.assertIsNone(parse_count("nice 42"))
        self.assertIsNone(parse_count(""))
        self.assertIsNone(parse_count(None))

    def test_render_template(self):
        """Known placeholders are replaced, unknown ones stay."""
        self.assertEqual(render_template("Members: {members} {x}", {"members": 5}), "Members: 5 {x}")

    def test_match_trigger_modes(self):
        """The four autoresponder modes."""
        self.assertTrue(match_trigger("Hello there", "hello", "contains"))
        self.assertTrue(match_trigger("say hello please", "hello", "word"))
        self.assertFalse(match_trigger("helloworld", "hello", "word"))
        self.assertTrue(match_trigger("Hello", "hello", "exact"))
        self.assertFalse(match_trigger("hello you", "hello", "exact"))
        self.assertTrue(match_trigger("hello you", "hello", "startswith"))
        self.assertFalse(match_trigger("anything", "", "contains"))

    def test_parse_color(self):
        """Hex colours with or without the hash."""
        self.assertEqual(parse_color("#ff8800").value, 0xFF8800)
        self.assertEqual(parse_color("ff8800").value, 0xFF8800)
        self.assertIsNone(parse_color("orange"))
        self.assertIsNone(parse_color(None))

    def test_purge_check(self):
        """Filters by user and by message type."""
        msg = NS(content="see https://example.com", author=NS(id=1, bot=False), attachments=[])
        self.assertTrue(purge_check("all", None)(msg))
        self.assertTrue(purge_check("links", None)(msg))
        self.assertFalse(purge_check("bots", None)(msg))
        self.assertFalse(purge_check("attachments", None)(msg))
        self.assertTrue(purge_check("all", NS(id=1))(msg))
        self.assertFalse(purge_check("all", NS(id=2))(msg))


if __name__ == "__main__":
    unittest.main()
