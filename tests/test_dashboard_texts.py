"""Translations of the dashboard: every language has every text, and the page can load them."""

import re
import unittest

from guardbot import dashtexts, i18n


class DashboardTextsTest(unittest.TestCase):
    def test_page_texts_are_found(self):
        ui = dashtexts.ui_texts()
        self.assertGreater(len(ui), 150)
        self.assertEqual(ui["signin"], "Sign in with Discord")
        self.assertIn("Plugins", dashtexts.english())

    def test_every_language_is_complete(self):
        for lang in i18n.LANGUAGES:
            if lang == "en":
                continue
            self.assertEqual(dashtexts.missing(lang), [], lang)

    def test_placeholders_and_empty_texts(self):
        for lang in i18n.LANGUAGES:
            for en, text in dashtexts.table(lang).items():
                self.assertTrue(text.strip(), (lang, en))
                self.assertEqual(sorted(re.findall(r"\{\w+\}", en)), sorted(re.findall(r"\{\w+\}", text)), (lang, en))

    def test_unknown_and_english(self):
        self.assertEqual(dashtexts.table("en"), {})
        self.assertEqual(dashtexts.table("xx"), {})


if __name__ == "__main__":
    unittest.main()
