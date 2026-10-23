"""Translations for the texts that members see.

The English text itself is the key. A language file maps English texts to the
translation; a missing entry falls back to English. Placeholders such as
{user} are written the same way in every language and filled in by tr().
"""

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

LANGUAGES = {
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "pt": "Português",
    "ru": "Русский",
    "uk": "Українська",
    "sv": "Svenska",
    "da": "Dansk",
    "zh": "中文",
    "ja": "日本語",
    "ko": "한국어",
}

_DIR = Path(__file__).parent / "locales"
_tables: dict = {}


def table(lang):
    """Return the translations of a language (empty for English or an unknown code)."""
    if lang in _tables:
        return _tables[lang]
    data = {}
    if lang in LANGUAGES and lang != "en":
        try:
            data = json.loads((_DIR / f"{lang}.json").read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            log.warning("language file %s could not be read: %s", lang, exc)
    _tables[lang] = data
    return data


def tr(lang, text, **values):
    """Translate an English text and fill in the placeholders that were passed."""
    out = table(lang).get(text, text)
    for key, value in values.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def lang_of(bot, guild):
    """Return the language code of a server, English when none is set."""
    gid = getattr(guild, "id", guild)
    if gid is None:
        return "en"
    code = bot.cfg(gid).get("language", "en")
    return code if code in LANGUAGES else "en"


def say(bot, guild, text, **values):
    """Translate a text into the language of a server."""
    return tr(lang_of(bot, guild), text, **values)
