"""Texts of the dashboard in all languages.

English is the original. Every other language has one file in guardbot/locales/dashboard/ that maps the English text to the translation.
The page loads the file of the chosen language and falls back to English for anything that is missing.
"""

import importlib
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from . import i18n

DIR = Path(__file__).parent / "locales" / "dashboard"
WEB = Path(__file__).parent / "web" / "app.js"
PAIR = re.compile(r'(\w+): "((?:[^"\\]|\\.)*)"')


def ui_texts() -> dict[str, str]:
    """The English texts of the page itself, from the TEXT.en blocks of app.js, as {key: text}."""
    out: dict[str, str] = {}
    for line in WEB.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("en: {") or s.startswith("Object.assign(TEXT.en,") or s.startswith("TEXT.en.cat"):
            for key, value in PAIR.findall(s):
                out[key] = json.loads(f'"{value}"')
            for value in re.findall(r'"((?:[^"\\]|\\.)*)": "(?:[^"\\]|\\.)*"', s):
                out["cat:" + value] = json.loads(f'"{value}"')
    return out


def setting_texts() -> list[str]:
    """Section titles, explanations, field labels, groups and choices of the settings, and the plugin catalog."""
    from . import dashhelp, plugins
    from .defaults import DEFAULTS
    dashboard: Any = importlib.import_module(__package__ + ".dashboard")
    texts: list[str] = []
    for s in dashboard.describe(json.loads(json.dumps(DEFAULTS)), []):
        texts.append(s["title"])
        if s.get("info"):
            texts.append(s["info"])
        for f in [] if s["key"] == "modules" else s["fields"]:
            texts.append(f["label"])
            if f.get("help"):
                texts.append(f["help"])
            texts.extend(p for p in (f.get("group") or "").split(" / ") if p)
            if f["type"] == "choice" and f["path"] != "language":
                texts.extend(str(c[1]) for c in f.get("choices", []))
    for _key, title, _de in plugins.CATEGORIES:
        texts.append(title)
    for key, entry in plugins.PLUGINS.items():
        texts.extend((entry[4], entry[6], dashhelp.ABOUT.get(key, entry[6])))
    return texts


def english() -> list[str]:
    """Every English text of the dashboard, each once, in a fixed order."""
    seen: dict[str, None] = {}
    for text in list(ui_texts().values()) + setting_texts():
        if text and text not in seen:
            seen[text] = None
    return list(seen)


@lru_cache(maxsize=16)
def table(lang: str) -> dict[str, str]:
    """The translations of one language, empty for English or unknown languages."""
    if lang not in i18n.LANGUAGES or lang == "en":
        return {}
    path = DIR / f"{lang}.json"
    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {k: v for k, v in data.items() if isinstance(k, str) and isinstance(v, str)}


def missing(lang: str) -> list[str]:
    """English texts without a translation in a language."""
    have = table(lang)
    return [t for t in english() if t not in have]
