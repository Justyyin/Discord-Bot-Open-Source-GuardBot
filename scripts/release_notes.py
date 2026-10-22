"""Print the changelog entry of one version, used for the text of a GitHub release.

Usage: python scripts/release_notes.py 1.4.0
"""

import re
import sys
from pathlib import Path


def notes(changelog, version):
    """Return the lines under '## <version>' up to the next version heading, or None if the version is not in the changelog."""
    match = re.search(rf"^## {re.escape(version)}\s*$(.*?)(?=^## |\Z)", changelog, re.S | re.M)
    return match.group(1).strip() if match else None


def main():
    """Read CHANGELOG.md and print the entry for the version given on the command line."""
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/release_notes.py VERSION")
    text = notes((Path(__file__).resolve().parent.parent / "CHANGELOG.md").read_text(encoding="utf-8"), sys.argv[1])
    if text is None:
        sys.exit(f"Version {sys.argv[1]} is not in CHANGELOG.md")
    print(text)


if __name__ == "__main__":
    main()
