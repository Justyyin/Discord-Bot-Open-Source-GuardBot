"""The look of the dashboard for one server: colours, a wallpaper, own menus and tabs.

Everything is checked here before it is stored, the page only shows what passed. Texts are shown as plain text, links must use https.
"""

import copy
import hashlib
import re
from pathlib import Path
from typing import Any, Optional

from .panels import check_image

# The icons the page knows; a test checks that app.js draws every one of them
ICONS = (
    "home", "grid", "terminal", "puzzle", "spark", "image", "face", "cog", "hammer", "list", "save", "lock", "wrench", "info", "clock", "filter",
    "shield", "check", "mail", "scale", "flag", "pin", "tag", "eye", "alert", "users", "key", "hand", "star", "trophy", "smile", "bell", "cake",
    "mic", "chart", "coin", "gift", "hash", "music", "bulb", "ticket", "chat", "megaphone", "edit", "rss", "userplus", "folder", "archive",
    "book", "calendar", "form", "case", "plus", "pencil", "link", "note", "palette",
)
PAGES = ("overview", "plugins", "commands", "panels", "skills", "ai", "music", "profile", "settings", "cases", "backup")
KINDS = ("plugins", "page", "link", "note")
COLORS = ("accent", "background", "surface", "text")
MAX_MENUS = 12
MAX_TABS = 40
MAX_TITLE = 40
MAX_NOTE = 4000
MAX_URL = 300
HEX = re.compile(r"#[0-9a-fA-F]{6}")

DEFAULT: dict[str, Any] = {
    "accent": None, "background": None, "surface": None, "text": None, "wallpaper": None, "dim": 55, "blur": 0,
    "compact": False, "hide_categories": [], "menus": [], "tabs": [],
}


class LookError(ValueError):
    """A value of the look that is not allowed."""


def _title(value: Any, what: str) -> str:
    """A short single-line title."""
    if not isinstance(value, str):
        raise LookError(f"{what} needs a title")
    text = re.sub(r"\s+", " ", value).strip()
    if not 1 <= len(text) <= MAX_TITLE:
        raise LookError(f"{what}: the title must have 1 to {MAX_TITLE} characters")
    return text


def _int(value: Any, low: int, high: int, what: str) -> int:
    """A whole number inside a range."""
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise LookError(f"{what} must be a whole number from {low} to {high}")
    return value


def clean(data: Any, plugins: set, categories: set, current: Optional[dict] = None) -> dict:
    """Check a look sent by the page and return what is stored. The wallpaper is kept from the current look, it changes only by upload."""
    if not isinstance(data, dict):
        raise LookError("the look must be an object")
    out = copy.deepcopy(DEFAULT)
    out["wallpaper"] = (current or {}).get("wallpaper")
    for key in COLORS:
        value = data.get(key)
        if value in (None, ""):
            continue
        if not isinstance(value, str) or not HEX.fullmatch(value):
            raise LookError(f"{key} must be a colour like #1e1f22")
        out[key] = value.lower()
    out["dim"] = _int(data.get("dim", 55), 0, 90, "dim")
    out["blur"] = _int(data.get("blur", 0), 0, 20, "blur")
    out["compact"] = bool(data.get("compact", False))
    hidden = data.get("hide_categories", [])
    if not isinstance(hidden, list) or not all(isinstance(c, str) and c in categories for c in hidden):
        raise LookError("unknown category")
    out["hide_categories"] = sorted(set(hidden))
    menus = data.get("menus", [])
    if not isinstance(menus, list) or len(menus) > MAX_MENUS:
        raise LookError(f"at most {MAX_MENUS} menus")
    seen: set[str] = set()
    for i, m in enumerate(menus):
        if not isinstance(m, dict):
            raise LookError("a menu must be an object")
        raw = m.get("id")
        mid: str = raw if isinstance(raw, str) and re.fullmatch(r"m\d{1,4}", raw) else f"m{i + 1}"
        while mid in seen:
            mid = f"m{int(mid[1:]) + 100}"
        seen.add(mid)
        out["menus"].append({"id": mid, "title": _title(m.get("title"), "menu"), "open": m.get("open", True) is not False})
    menu_ids = {m["id"] for m in out["menus"]}
    tabs = data.get("tabs", [])
    if not isinstance(tabs, list) or len(tabs) > MAX_TABS:
        raise LookError(f"at most {MAX_TABS} tabs")
    seen = set()
    for i, t in enumerate(tabs):
        if not isinstance(t, dict):
            raise LookError("a tab must be an object")
        raw = t.get("id")
        tid: str = raw if isinstance(raw, str) and re.fullmatch(r"t\d{1,4}", raw) else f"t{i + 1}"
        while tid in seen:
            tid = f"t{int(tid[1:]) + 100}"
        seen.add(tid)
        kind = t.get("kind")
        if kind not in KINDS:
            raise LookError("unknown kind of tab")
        icon = t.get("icon") if t.get("icon") in ICONS else "star"
        menu = t.get("menu") or ""
        if menu and menu not in menu_ids:
            raise LookError("a tab points to a menu that does not exist")
        tab = {"id": tid, "title": _title(t.get("title"), "tab"), "icon": icon, "menu": menu, "kind": kind, "plugins": [], "page": "", "url": "", "text": ""}
        if kind == "plugins":
            chosen = t.get("plugins", [])
            if not isinstance(chosen, list) or not chosen or len(chosen) > 40 or not all(isinstance(p, str) and p in plugins for p in chosen):
                raise LookError("choose plugins for the tab")
            tab["plugins"] = list(dict.fromkeys(chosen))
        elif kind == "page":
            if t.get("page") not in PAGES:
                raise LookError("choose a page for the tab")
            tab["page"] = t["page"]
        elif kind == "link":
            url = t.get("url")
            if not isinstance(url, str) or len(url) > MAX_URL or not re.fullmatch(r"https://[^\s<>\"']+", url):
                raise LookError("a link must start with https://")
            tab["url"] = url
        else:
            text = t.get("text")
            if not isinstance(text, str) or not text.strip() or len(text) > MAX_NOTE:
                raise LookError(f"a note needs 1 to {MAX_NOTE} characters")
            tab["text"] = text
        out["tabs"].append(tab)
    return out


def folder(data_dir: Any, gid: int) -> Path:
    """The folder with the wallpaper of a server."""
    return Path(data_dir) / "look" / str(int(gid))


def store_wallpaper(look: dict, data_dir: Any, gid: int, data: bytes) -> str:
    """Save a new wallpaper, delete the old one, and return the file name."""
    kind = check_image(data)
    name = f"{hashlib.sha256(data).hexdigest()[:16]}.{kind}"
    target = folder(data_dir, gid)
    target.mkdir(parents=True, exist_ok=True)
    for old in target.iterdir():
        if old.name != name:
            old.unlink(missing_ok=True)
    (target / name).write_bytes(data)
    look["wallpaper"] = name
    return name


def remove_wallpaper(look: dict, data_dir: Any, gid: int) -> None:
    """Delete the wallpaper."""
    target = folder(data_dir, gid)
    if target.is_dir():
        for old in target.iterdir():
            old.unlink(missing_ok=True)
    look["wallpaper"] = None


def wallpaper_path(look: dict, data_dir: Any, gid: int) -> Optional[Path]:
    """The file of the wallpaper, or None."""
    name = look.get("wallpaper")
    if not isinstance(name, str) or not re.fullmatch(r"[0-9a-f]{16}\.(png|jpg|gif|webp)", name):
        return None
    path = folder(data_dir, gid) / name
    return path if path.is_file() else None
