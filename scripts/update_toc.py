# Copyright (c) Justyn
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- toc -->", "<!-- tocstop -->"
LANGS = [
    ("de", "Deutsch"), ("en", "English"), ("fr", "Fran\u00e7ais"), ("es", "Espa\u00f1ol"), ("pt", "Portugu\u00eas"),
    ("ru", "\u0420\u0443\u0441\u0441\u043a\u0438\u0439"), ("uk", "\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430"),
    ("sv", "Svenska"), ("da", "Dansk"), ("zh", "\u4e2d\u6587"), ("ja", "\u65e5\u672c\u8a9e"), ("ko", "\ud55c\uad6d\uc5b4"),
]


def slug(text, seen):
    s = re.sub(r"[^\w\- ]", "", text.strip().lower()).replace(" ", "-")
    n = seen.get(s, 0)
    seen[s] = n + 1
    return s if n == 0 else f"{s}-{n}"


def build_toc(text):
    seen, out, fence = {}, [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"^(#{2,3}) (.+?)\s*$", line)
        if m:
            indent = "  " * (len(m.group(1)) - 2)
            out.append(f"{indent}- [{m.group(2)}](#{slug(m.group(2), seen)})")
    return "\n".join(out)


def update(path):
    text = path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        return False
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    toc = build_toc(head + tail)
    path.write_text(f"{head}{START}\n\n{toc}\n\n{END}{tail}", encoding="utf-8")
    return True


def language_bar(prefix):
    return " | ".join(f"[{name}]({prefix}{code}/README.md)" for code, name in LANGS)


def sync_root():
    src = (ROOT / "docs" / "en" / "README.md").read_text(encoding="utf-8")
    src = src.replace("](../../", "](").replace("](../", "](docs/").replace("](GUIDE.md)", "](docs/en/GUIDE.md)")
    (ROOT / "README.md").write_text(src, encoding="utf-8")


def main():
    count = 0
    for p in list((ROOT / "docs").rglob("*.md")):
        if update(p):
            count += 1
    sync_root()
    print(f"updated {count} files and the root README")


if __name__ == "__main__":
    sys.exit(main())
