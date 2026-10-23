"""Panels: posts made of banner pictures, embeds and buttons, such as a welcome post, rules, role choices, notifications or a verification gate.

A panel is stored as data in the server settings. Pictures are uploaded once (by command or in the dashboard), checked, and kept as
files in the data folder, because links to Discord attachments stop working after a while. This module validates panels, stores
pictures and builds what is sent; the Discord commands are in cogs/tools/panels.py.
"""

import hashlib
import importlib
import io
import re
import time
from pathlib import Path
from typing import Any, Optional

import discord
from PIL import Image

NAME_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,29}")
COLOR_RE = re.compile(r"#[0-9a-fA-F]{6}")
KINDS = ("role", "verify", "link")
STYLES = ("primary", "secondary", "success", "danger")
TEMPLATES = ("empty", "welcome", "rules", "roles", "notifications", "verify")
MAX_PANELS = 25
MAX_SECTIONS = 5
MAX_BUTTONS = 20
MAX_IMAGES = 40
MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_PIXELS = 40_000_000
IMAGE_KINDS = {"PNG": "png", "JPEG": "jpg", "GIF": "gif", "WEBP": "webp"}
SECTION_KEYS = {"title", "text", "color", "footer", "banner", "image", "thumbnail"}
BUTTON_KEYS = {"kind", "label", "emoji", "style", "role", "url"}
PANEL_KEYS = {"name", "channel", "single", "sections", "buttons", "messages"}

# Texts of the templates, translated into the language of the server when a template is used
WELCOME_TITLE = "Welcome to {server}"
WELCOME_TEXT = "Hello and welcome to all our new members! We are happy that you are part of our community.\n\nPlease take a moment to introduce yourself and tell us a little about you.\n\nBefore you start, please read our server rules. We want everyone to have a good time here."
RULES_TITLE = "Rules"
RULES_TEXT = "1. Be friendly and respectful to each other.\n2. Keep your Discord profile appropriate.\n3. No spam.\n4. No advertising.\n5. No personal information.\n6. No hate speech or hurtful language.\n7. Common sense applies to all rules."
ROLES_TEXT = "Press a button to get your role."
NOTIFY_TITLE = "Notifications"
NOTIFY_TEXT = "Choose what you want to be notified about. You can pick one or all options, it is up to you."
VERIFY_TITLE = "Verification"
VERIFY_TEXT = "To enter this server and see all channels, you must first prove that you are human.\nPress the button below to start."
VERIFY_LABEL = "Verify"
TEMPLATE_TEXTS = {
    "welcome": [(WELCOME_TITLE, WELCOME_TEXT)],
    "rules": [(RULES_TITLE, RULES_TEXT)],
    "roles": [("", ROLES_TEXT)],
    "notifications": [(NOTIFY_TITLE, NOTIFY_TEXT)],
    "verify": [(VERIFY_TITLE, VERIFY_TEXT)],
}
TEXTS = (WELCOME_TITLE, WELCOME_TEXT, RULES_TITLE, RULES_TEXT, ROLES_TEXT, NOTIFY_TITLE, NOTIFY_TEXT, VERIFY_TITLE, VERIFY_TEXT, VERIFY_LABEL)


class PanelError(ValueError):
    """A panel or a picture is not valid. The message says what to change."""


# ---- pictures

def image_dir(data_dir: Any, gid: int) -> Path:
    """The folder with the pictures of one server."""
    return Path(data_dir) / "panels" / str(int(gid))


def check_image(data: bytes) -> str:
    """Check a picture and return its file extension. Raises PanelError."""
    if not 100 <= len(data) <= MAX_IMAGE_BYTES:
        raise PanelError("pictures must be smaller than 8 MB")
    try:
        with Image.open(io.BytesIO(data)) as im:
            kind = IMAGE_KINDS.get(im.format or "")
            if kind is None:
                raise PanelError("use a PNG, JPEG, GIF or WebP picture")
            if im.width * im.height > MAX_PIXELS:
                raise PanelError("the picture has too many pixels")
            im.verify()
    except (OSError, Image.DecompressionBombError):
        raise PanelError("the picture cannot be read")
    return kind


def store_image(conf: dict, data_dir: Any, gid: int, data: bytes, name: str = "") -> str:
    """Save a picture for a server and return its ID. The same picture is stored only once."""
    kind = check_image(data)
    pid = hashlib.sha256(data).hexdigest()[:16]
    images = conf.setdefault("images", {})
    if pid not in images:
        if len(images) >= MAX_IMAGES:
            raise PanelError(f"a server can keep {MAX_IMAGES} pictures, delete unused panels first")
        folder = image_dir(data_dir, gid)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{pid}.{kind}").write_bytes(data)
        images[pid] = {"file": f"{pid}.{kind}", "name": re.sub(r"[^\w.\- ]", "", name)[:80], "size": len(data), "added": int(time.time())}
    return pid


def image_path(conf: dict, data_dir: Any, gid: int, pid: Optional[str]) -> Optional[Path]:
    """The file of a picture, or None when it is missing."""
    info = conf.get("images", {}).get(pid or "")
    if not info:
        return None
    path = image_dir(data_dir, gid) / info["file"]
    return path if path.is_file() else None


def used_images(conf: dict) -> set:
    """The IDs of all pictures that a panel uses."""
    used: set[str] = set()
    for panel in conf["items"].values():
        for s in panel["sections"]:
            used.update(x for x in (s.get("banner"), s.get("image"), s.get("thumbnail")) if x)
    return used


KEEP_NEW_SECONDS = 3600


def clean_images(conf: dict, data_dir: Any, gid: int, keep_new: bool = True) -> int:
    """Delete pictures that no panel uses any more. Pictures uploaded in the last hour stay, they may belong to a panel that is still being edited. Returns how many were deleted."""
    used, gone, now = used_images(conf), 0, time.time()
    for pid in list(conf.get("images", {})):
        if keep_new and now - conf["images"][pid].get("added", 0) < KEEP_NEW_SECONDS:
            continue
        if pid not in used:
            info = conf["images"].pop(pid)
            try:
                (image_dir(data_dir, gid) / info["file"]).unlink()
            except OSError:
                pass
            gone += 1
    return gone


# ---- validation

def as_text(value: Any, what: str, limit: int) -> str:
    """A string of limited length, empty allowed."""
    if value is None:
        return ""
    if not isinstance(value, str):
        raise PanelError(f"{what} must be text")
    value = value.replace("\r\n", "\n").strip()
    if len(value) > limit:
        raise PanelError(f"{what} is longer than {limit} characters")
    return value


def as_id(value: Any, what: str) -> int:
    """A Discord ID given as number or digits."""
    if isinstance(value, str) and value.isdigit():
        value = int(value)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise PanelError(f"{what} must be an ID")
    return value


def clean_emoji(value: Any) -> str:
    """A unicode emoji or a custom emoji like <:name:123>, or empty."""
    text = as_text(value, "emoji", 60)
    if not text:
        return ""
    if re.fullmatch(r"<a?:\w{2,32}:\d{5,22}>", text):
        return text
    if len(text) > 8 or re.search(r"[A-Za-z\s]", text) or (re.search(r"[0-9#*]", text) and "\u20e3" not in text):
        raise PanelError("emoji must be one emoji, or a custom emoji like <:name:123>")
    return text


def clean_section(section: Any, images: dict) -> dict:
    """One block of a panel: a banner above, an embed with title, text, colour, picture, thumbnail and footer."""
    if not isinstance(section, dict):
        raise PanelError("a section must be an object")
    extra = set(section) - SECTION_KEYS
    if extra:
        raise PanelError("unknown field(s) in a section: " + ", ".join(sorted(extra)[:5]))
    out: dict[str, Any] = {"title": as_text(section.get("title"), "title", 256), "text": as_text(section.get("text"), "text", 4000), "footer": as_text(section.get("footer"), "footer", 200)}
    color = section.get("color") or None
    if color is not None and (not isinstance(color, str) or not COLOR_RE.fullmatch(color)):
        raise PanelError("color must look like #5865f2")
    out["color"] = color.lower() if color else None
    for key in ("banner", "image", "thumbnail"):
        pid = section.get(key) or None
        if pid is not None and pid not in images:
            raise PanelError(f"the picture for {key} does not exist, upload it again")
        out[key] = pid
    if not (out["title"] or out["text"] or out["banner"] or out["image"]):
        raise PanelError("a section needs a title, a text or a picture")
    return out


def clean_button(button: Any) -> dict:
    """One button: a role to take or give back, the verification, or a link."""
    if not isinstance(button, dict):
        raise PanelError("a button must be an object")
    extra = set(button) - BUTTON_KEYS
    if extra:
        raise PanelError("unknown field(s) in a button: " + ", ".join(sorted(extra)[:5]))
    kind = button.get("kind")
    if kind not in KINDS:
        raise PanelError("kind must be role, verify or link")
    style = button.get("style") or ("success" if kind == "verify" else "primary")
    if style not in STYLES:
        raise PanelError("style must be primary, secondary, success or danger")
    out: dict[str, Any] = {"kind": kind, "label": as_text(button.get("label"), "label", 80), "emoji": clean_emoji(button.get("emoji")), "style": style}
    if not out["label"] and not out["emoji"]:
        raise PanelError("a button needs a label or an emoji")
    if kind == "role":
        out["role"] = as_id(button.get("role"), "role")
    if kind == "link":
        url = as_text(button.get("url"), "url", 512)
        if not re.fullmatch(r"https://[^\s<>\"']{3,500}", url):
            raise PanelError("a link must start with https://")
        out["url"] = url
    return out


def clean(panel: Any, images: dict) -> dict:
    """Validate a panel and return it in its normal form. Raises PanelError."""
    if not isinstance(panel, dict):
        raise PanelError("a panel must be an object")
    extra = set(panel) - PANEL_KEYS
    if extra:
        raise PanelError("unknown field(s): " + ", ".join(sorted(extra)[:5]))
    name = as_text(panel.get("name"), "name", 30).lower()
    if not NAME_RE.fullmatch(name):
        raise PanelError("name uses lowercase letters, digits, - and _ (1 to 30 characters)")
    sections = panel.get("sections") or []
    buttons = panel.get("buttons") or []
    if not isinstance(sections, list) or not 1 <= len(sections) <= MAX_SECTIONS:
        raise PanelError(f"a panel needs 1 to {MAX_SECTIONS} sections")
    if not isinstance(buttons, list) or len(buttons) > MAX_BUTTONS:
        raise PanelError(f"a panel can have {MAX_BUTTONS} buttons at most")
    out: dict[str, Any] = {
        "name": name, "channel": as_id(panel["channel"], "channel") if panel.get("channel") else None, "single": bool(panel.get("single", False)),
        "sections": [clean_section(s, images) for s in sections], "buttons": [clean_button(b) for b in buttons],
        "messages": [as_id(m, "message") for m in panel.get("messages") or []][:MAX_SECTIONS],
    }
    if sum(1 for b in out["buttons"] if b["kind"] == "verify") > 1:
        raise PanelError("a panel can have one verify button")
    return out


def template(kind: str, name: str, tr: Any = None) -> dict:
    """A new panel from a template, with texts in the language of the server."""
    tr = tr or (lambda text: text)
    panel: dict[str, Any] = {"name": name, "channel": None, "single": kind == "roles", "sections": [], "buttons": [], "messages": []}
    for title, text in TEMPLATE_TEXTS.get(kind, [("", "")]):
        panel["sections"].append({"title": tr(title) if title else "", "text": tr(text) if text else "", "footer": "", "color": None, "banner": None, "image": None, "thumbnail": None})
    if kind == "verify":
        panel["buttons"].append({"kind": "verify", "label": tr(VERIFY_LABEL), "emoji": "", "style": "success"})
    if kind == "empty":
        panel["sections"][0]["text"] = name
    return panel


# ---- building what is sent

def fill(text: str, guild: Any) -> str:
    """Replace {server} and {count} in a text."""
    return text.replace("{server}", str(getattr(guild, "name", ""))).replace("{count}", str(getattr(guild, "member_count", "")))


def build_section(section: dict, conf: dict, data_dir: Any, guild: Any, index: int) -> tuple[Optional[discord.Embed], list]:
    """The embed and the files of one section. The banner is a file above the embed, picture and thumbnail live inside the embed."""
    files: list = []

    def attach(pid: Optional[str], stem: str) -> Optional[str]:
        path = image_path(conf, data_dir, guild.id, pid)
        if path is None:
            return None
        filename = f"{stem}{index}{path.suffix}"
        files.append(discord.File(io.BytesIO(path.read_bytes()), filename=filename))
        return f"attachment://{filename}"

    attach(section.get("banner"), "banner")
    embed = None
    if section["title"] or section["text"] or section.get("image") or section.get("thumbnail") or section["footer"]:
        color = int(section["color"][1:], 16) if section.get("color") else None
        embed = discord.Embed(title=fill(section["title"], guild) or None, description=fill(section["text"], guild) or None, color=color)
        image = attach(section.get("image"), "image")
        if image:
            embed.set_image(url=image)
        thumb = attach(section.get("thumbnail"), "thumb")
        if thumb:
            embed.set_thumbnail(url=thumb)
        if section["footer"]:
            embed.set_footer(text=fill(section["footer"], guild))
    return embed, files


class PanelButton(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:pn:(?P<pid>\d+):(?P<idx>\d+)"):
    """A role button of a panel. It keeps working after a restart because the panel and the position are in its ID."""

    def __init__(self, pid: int, index: int, label: Optional[str] = None, emoji: Optional[str] = None, style: str = "primary"):
        """Create the button."""
        super().__init__(discord.ui.Button(label=label, emoji=emoji, style=getattr(discord.ButtonStyle, style, discord.ButtonStyle.primary), custom_id=f"gb:pn:{pid}:{index}"))
        self.pid, self.index = int(pid), int(index)

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its ID."""
        return cls(int(match["pid"]), int(match["idx"]), item.label)

    async def callback(self, interaction: discord.Interaction) -> None:
        """Give or take the role."""
        cog = getattr(interaction.client, "get_cog")("Panels")
        if cog is not None:
            await cog.press(interaction, self.pid, self.index)


def button_item(pid: int, index: int, button: dict) -> discord.ui.Item:
    """The Discord button of a panel button. The verify button reuses the gate of the verification module."""
    emoji = button["emoji"] or None
    label = button["label"] or None
    if button["kind"] == "link":
        return discord.ui.Button(label=label, emoji=emoji, url=button["url"], style=discord.ButtonStyle.link)
    if button["kind"] == "verify":
        item = importlib.import_module("guardbot.cogs.security.verify").VerifyButton()
        item.item.label, item.item.emoji = label, emoji
        item.item.style = getattr(discord.ButtonStyle, button["style"], discord.ButtonStyle.success)
        return item
    return PanelButton(pid, index, label, emoji, button["style"])


def build_view(pid: int, panel: dict) -> Optional[discord.ui.View]:
    """The buttons of a panel, five per row."""
    if not panel["buttons"]:
        return None
    view = discord.ui.View(timeout=None)
    for i, button in enumerate(panel["buttons"]):
        item = button_item(pid, i, button)
        item.row = i // 5
        view.add_item(item)
    return view
