"""Translations: every language is complete and keeps the placeholders."""

import json
import re
import unittest
from pathlib import Path

from guardbot import i18n
from guardbot.defaults import DEFAULTS

ROOT = Path(__file__).resolve().parent.parent
HOLES = re.compile(r"\{[a-z_]+\}")


class Locales(unittest.TestCase):
    """The language files."""

    def setUp(self):
        """Load the reference keys."""
        self.keys = list(json.loads((ROOT / "guardbot/locales/de.json").read_text(encoding="utf-8")))

    def test_every_language_has_a_file_with_all_keys(self):
        """No language misses a text and none has extra ones."""
        for lang in i18n.LANGUAGES:
            if lang == "en":
                continue
            data = json.loads((ROOT / f"guardbot/locales/{lang}.json").read_text(encoding="utf-8"))
            self.assertEqual(list(data), self.keys, lang)
            for key, value in data.items():
                self.assertTrue(value.strip(), (lang, key))

    def test_placeholders_are_kept(self):
        """A translation uses exactly the placeholders of the English text."""
        for lang in i18n.LANGUAGES:
            if lang == "en":
                continue
            for key, value in i18n.table(lang).items():
                self.assertEqual(sorted(HOLES.findall(key)), sorted(HOLES.findall(value)), (lang, key))

    def test_default_templates_are_translatable(self):
        """The default welcome, goodbye, booster, birthday and level texts have a translation."""
        defaults = [DEFAULTS["welcome"]["message"], DEFAULTS["welcome"]["goodbye_message"], DEFAULTS["boosters"]["message"], DEFAULTS["birthday"]["message"], DEFAULTS["xp"]["message"]]
        for text in defaults:
            self.assertIn(text, self.keys, text)

    def test_translate_fill_and_fallback(self):
        """tr() fills placeholders, falls back to English and leaves custom texts alone."""
        self.assertEqual(i18n.tr("de", "Happy birthday {user}!").replace("{user}", "X"), "Alles Gute zum Geburtstag, X!")
        self.assertEqual(i18n.tr("de", "Hello {user}", user="A"), "Hello A")
        self.assertEqual(i18n.tr("xx", "Tickets are disabled."), "Tickets are disabled.")
        self.assertEqual(i18n.tr("ja", "Language set to {language}.", language="日本語"), "言語を 日本語 に設定しました。")

    def test_language_of_a_server(self):
        """An unknown or missing code becomes English."""
        class B:
            """Bot with fixed settings."""

            def __init__(self, code):
                """Keep the code."""
                self.code = code

            def cfg(self, gid):
                """Return the settings."""
                return {"language": self.code}

        self.assertEqual(i18n.lang_of(B("de"), 1), "de")
        self.assertEqual(i18n.lang_of(B("klingon"), 1), "en")
        self.assertEqual(i18n.lang_of(B("de"), None), "en")


if __name__ == "__main__":
    unittest.main()
