"""Message builder: JSON of embed generators, link buttons and the limits."""

import unittest
from types import SimpleNamespace

from guardbot import builder
from guardbot.builder import BuildError, parse


class ParseTest(unittest.TestCase):
    """Reading messages."""

    def test_full_message(self):
        """Text, an embed with fields and link buttons are built."""
        data = {
            "content": "Hello",
            "embeds": [{"title": "T", "description": "D", "color": "#5865f2", "url": "https://example.com", "footer": {"text": "f"}, "image": {"url": "https://example.com/a.png"}, "fields": [{"name": "a", "value": "b", "inline": True}], "timestamp": "2025-01-31T12:00:00Z"}],
            "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open", "url": "https://example.com"}]}],
        }
        content, embeds, view, warnings = parse(data)
        self.assertEqual(content, "Hello")
        self.assertEqual(embeds[0].title, "T")
        self.assertEqual(embeds[0].colour.value, 0x5865F2)
        self.assertEqual(len(view.children), 1)
        self.assertEqual(view.children[0].url, "https://example.com")
        self.assertEqual(warnings, [])

    def test_shapes(self):
        """A single embed, a list of embeds and a flat list of buttons are understood."""
        self.assertEqual(parse({"title": "Only an embed"})[1][0].title, "Only an embed")
        self.assertEqual(len(parse([{"title": "a"}, {"title": "b"}])[1]), 2)
        view = parse({"content": "x", "components": [{"type": 2, "style": 5, "label": "A", "url": "https://a.example"}]})[2]
        self.assertEqual(len(view.children), 1)

    def test_other_buttons_are_skipped(self):
        """Buttons that need an interaction are skipped with a warning, never created."""
        data = {"content": "x", "components": [{"type": 1, "components": [{"type": 2, "style": 1, "label": "Click", "custom_id": "abc"}, {"type": 2, "style": 5, "label": "L", "url": "https://a.example"}]}]}
        _, _, view, warnings = parse(data)
        self.assertEqual(len(view.children), 1)
        self.assertEqual(len(warnings), 1)

    def test_bad_links_are_refused(self):
        """Only http and https links are allowed anywhere."""
        for bad in ("javascript:alert(1)", "data:text/html,x", "file:///etc/passwd", "attachment://a.png", "ftp://x.example", "//x.example"):
            with self.assertRaises(BuildError, msg=bad):
                parse({"embeds": [{"title": "t", "image": {"url": bad}}]})
            with self.assertRaises(BuildError, msg=bad):
                parse({"content": "x", "components": [{"type": 2, "style": 5, "label": "A", "url": bad}]})

    def test_limits(self):
        """Lengths and counts follow the limits of Discord."""
        for data in (
            {"content": "x" * 2001}, {"content": ""}, {"embeds": [{"title": "t"}] * 11}, {"embeds": [{"title": "x" * 257}]}, {"embeds": [{"description": "x" * 4097}]},
            {"embeds": [{"title": "t", "fields": [{"name": "a", "value": "b"}] * 26}]}, {"embeds": [{"description": "x" * 4000}, {"description": "y" * 4000}]},
            {"embeds": [{"title": "t", "color": "red"}]}, {"embeds": [{"title": "t", "timestamp": "yesterday"}]}, {"embeds": [{}]}, {"content": "x", "components": [{"type": 2, "style": 5, "label": "", "url": "https://a.example"}]},
            {"content": "x", "components": [{"type": 2, "style": 5, "label": "a", "url": "https://a.example"}] * 26}, "text", 5, None,
        ):
            with self.assertRaises(BuildError, msg=str(data)[:60]):
                parse(data)

    def test_unknown_keys_are_dropped(self):
        """Fields that a bot cannot send, such as video, do not reach Discord."""
        _, embeds, _, _ = parse({"embeds": [{"title": "t", "video": {"url": "https://evil.example/v.mp4"}, "provider": {"name": "x"}, "type": "video"}]})
        self.assertIsNone(embeds[0].video.url)

    def test_export_round_trip(self):
        """An exported message can be read again."""
        button = SimpleNamespace(url="https://a.example", label="Go")
        message = SimpleNamespace(content="hi", embeds=[__import__("discord").Embed(title="T", description="D")], components=[SimpleNamespace(children=[button])])
        data = builder.export(message)
        self.assertEqual(data["content"], "hi")
        content, embeds, view, _ = parse(data)
        self.assertEqual((content, embeds[0].title, view.children[0].label), ("hi", "T", "Go"))


if __name__ == "__main__":
    unittest.main()
