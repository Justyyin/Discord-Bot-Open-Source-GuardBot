"""Documentation: tables of contents, links, languages and placeholders."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["de", "en", "fr", "es", "pt", "ru", "uk", "sv", "da", "zh", "ja", "ko"]
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2190-\u21FF\u2300-\u23FF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u20E3]")


def slug(text):
    return re.sub(r"[^\w\- ]", "", text.strip().lower()).replace(" ", "-")


class DocsTest(unittest.TestCase):
    def files(self):
        return list(ROOT.rglob("*.md"))

    def test_every_language_has_both_documents(self):
        for code in LANGS:
            self.assertTrue((ROOT / "docs" / code / "README.md").exists(), code)
            self.assertTrue((ROOT / "docs" / code / "GUIDE.md").exists(), code)

    def test_no_emojis_in_documents(self):
        for p in self.files():
            self.assertIsNone(EMOJI.search(p.read_text(encoding="utf-8")), str(p))

    def test_relative_links_exist(self):
        link = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
        for p in self.files():
            for m in link.finditer(p.read_text(encoding="utf-8")):
                url = m.group(1)
                if not url.startswith(("http://", "https://")):
                    self.assertTrue((p.parent / url).resolve().exists(), f"{p}: {url}")

    def test_table_of_contents_anchors_match_headings(self):
        for p in self.files():
            text = p.read_text(encoding="utf-8")
            seen, anchors = {}, set()
            for h in re.findall(r"^#{1,3} (.+)$", text, re.M):
                s = slug(h)
                n = seen.get(s, 0)
                seen[s] = n + 1
                anchors.add(s if n == 0 else f"{s}-{n}")
            for a in re.findall(r"\]\(#([^)]+)\)", text):
                self.assertIn(a, anchors, f"{p}: #{a}")

    def test_command_reference_is_current(self):
        import asyncio
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        import build_reference
        current = (ROOT / "docs" / "REFERENCE.md").read_text(encoding="utf-8")
        self.assertEqual(current, asyncio.run(build_reference.build()), "run python scripts/build_reference.py")

    def test_documents_have_the_same_structure(self):
        counts = {c: len(re.findall(r"^## ", (ROOT / "docs" / c / "README.md").read_text(encoding="utf-8"), re.M)) for c in LANGS}
        self.assertEqual(len(set(counts.values())), 1, counts)

    def test_commands_named_in_guides_exist(self):
        """Every slash command written in a guide or in COMMANDS.md must exist in the generated reference."""
        ref = (ROOT / "docs" / "REFERENCE.md").read_text(encoding="utf-8")
        known = set(re.findall(r"^\| `/([^`]+)` \|", ref, re.M))
        prefixes = {" ".join(c.split()[:i]) for c in known for i in range(1, len(c.split()) + 1)}
        pattern = re.compile(r"`/([a-z]+(?: [a-z]+){0,3})(?=[ `])")
        files = [ROOT / "docs" / "COMMANDS.md", ROOT / "docs" / "TESTING.md"] + [ROOT / "docs" / code / "GUIDE.md" for code in LANGS]
        missing = []
        for p in files:
            for m in pattern.finditer(p.read_text(encoding="utf-8")):
                path = m.group(1)
                if path not in prefixes and not any(" ".join(path.split()[:i]) in known for i in range(1, len(path.split()) + 1)):
                    missing.append((p.name, path))
        self.assertEqual(missing, [])

if __name__ == "__main__":
    unittest.main()
