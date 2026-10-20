"""Insert the real repository URL into the documentation.

Usage: python scripts/set_repo_url.py https://github.com/NAME/guardbot.git
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = "<REPOSITORY_URL>"


def main():
    """Replace the placeholder in every markdown file and report how many files changed."""
    if len(sys.argv) != 2 or not sys.argv[1].startswith(("https://", "git@")):
        sys.exit("Usage: python scripts/set_repo_url.py https://github.com/NAME/guardbot.git")
    url = sys.argv[1]
    changed = 0
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER in text:
            path.write_text(text.replace(PLACEHOLDER, url), encoding="utf-8")
            changed += 1
    print(f"{changed} files updated")


if __name__ == "__main__":
    main()
