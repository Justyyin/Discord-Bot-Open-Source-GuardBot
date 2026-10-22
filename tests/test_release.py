"""Release notes and version consistency."""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from release_notes import notes  # noqa: E402

from guardbot import __version__  # noqa: E402


class ReleaseTest(unittest.TestCase):
    """The changelog and the version fit together."""

    def test_notes_extraction(self):
        """Only the section of the asked version is returned."""
        text = "# Changelog\n\n## 1.2.0\n\n- b\n\n## 1.1.0\n\n- a\n"
        self.assertEqual(notes(text, "1.2.0"), "- b")
        self.assertEqual(notes(text, "1.1.0"), "- a")
        self.assertIsNone(notes(text, "9.9.9"))

    def test_current_version_is_in_the_changelog(self):
        """The version in the code has a changelog entry with content, and it is the newest one."""
        log = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertTrue(notes(log, __version__), __version__)
        self.assertEqual(re.search(r"^## (\S+)", log, re.M).group(1), __version__)

    def test_workflows_exist(self):
        """CI, release and the templates are in place."""
        for name in (".github/workflows/ci.yml", ".github/workflows/release.yml", ".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE/bug_report.md", ".github/ISSUE_TEMPLATE/translation.md"):
            self.assertTrue((ROOT / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
