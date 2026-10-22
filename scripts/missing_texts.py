"""List the fixed reply texts of the commands that have no translation yet.

Usage: python scripts/missing_texts.py [language]

Texts that are built with f-strings are not listed because they contain names and numbers; they stay English.
"""

import ast
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAMES = ("send_message", "send", "edit_message", "edit_original_response")


def wrapped_texts(root=ROOT):
    """Return {English text: number of uses} for every text passed to i18n.say in the command modules."""
    found = Counter()
    for path in sorted((root / "guardbot" / "cogs").glob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ("say", "tr") and isinstance(node.func.value, ast.Name) and node.func.value.id == "i18n":
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and len(arg.value) >= 5:
                        found[arg.value] += 1
                        break
    return found


def missing(lang, root=ROOT):
    """Texts that the language file does not contain."""
    have = json.loads((root / "guardbot" / "locales" / f"{lang}.json").read_text(encoding="utf-8"))
    return {text: n for text, n in wrapped_texts(root).items() if text not in have}


def main():
    """Print the missing texts of one language, most used first."""
    lang = sys.argv[1] if len(sys.argv) > 1 else "de"
    items = missing(lang)
    for text, n in sorted(items.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{n:3d}  {text}")
    print(f"{len(items)} texts without translation in {lang}", file=sys.stderr)


if __name__ == "__main__":
    main()
