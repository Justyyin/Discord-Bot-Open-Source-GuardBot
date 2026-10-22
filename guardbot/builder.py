"""Message builder: turns the JSON that embed generators export (content, embeds, link buttons) into safe Discord objects, and back."""

import re
from datetime import datetime
from urllib.parse import urlparse

import discord

MAX_EMBEDS = 10
MAX_TOTAL = 6000
MAX_BUTTONS = 25
MAX_URL = 2000
LIMITS = {"title": 256, "description": 4096}


class BuildError(ValueError):
    """The message cannot be built, the text says why."""


def web_url(value, what):
    """Check that a value is a normal http or https link and return it."""
    if not isinstance(value, str) or len(value) > MAX_URL:
        raise BuildError(f"{what} must be a link")
    p = urlparse(value)
    if p.scheme not in ("http", "https") or not p.netloc:
        raise BuildError(f"{what} must start with http:// or https://")
    return value


def text(value, limit, what):
    """Check a text and its length."""
    if not isinstance(value, str):
        raise BuildError(f"{what} must be text")
    if len(value) > limit:
        raise BuildError(f"{what} is longer than {limit} characters")
    return value


def colour(value):
    """A colour as a number or as #rrggbb."""
    if isinstance(value, bool):
        raise BuildError("color must be a number or #rrggbb")
    if isinstance(value, int) and 0 <= value <= 0xFFFFFF:
        return value
    if isinstance(value, str) and re.fullmatch(r"#?[0-9a-fA-F]{6}", value.strip()):
        return int(value.strip().lstrip("#"), 16)
    raise BuildError("color must be a number or #rrggbb")


def clean_embed(raw):
    """Build the safe dict of one embed from an untrusted one. Unknown keys are dropped."""
    if not isinstance(raw, dict):
        raise BuildError("an embed must be an object")
    out, size = {}, 0
    for key in ("title", "description"):
        if raw.get(key):
            out[key] = text(raw[key], LIMITS[key], key)
            size += len(out[key])
    if raw.get("url"):
        out["url"] = web_url(raw["url"], "url")
    if raw.get("color") is not None:
        out["color"] = colour(raw["color"])
    if raw.get("timestamp"):
        try:
            datetime.fromisoformat(str(raw["timestamp"]).replace("Z", "+00:00"))
        except ValueError:
            raise BuildError("timestamp must look like 2025-01-31T12:00:00Z")
        out["timestamp"] = str(raw["timestamp"])
    footer = raw.get("footer")
    if isinstance(footer, dict) and footer.get("text"):
        out["footer"] = {"text": text(footer["text"], 2048, "footer text")}
        size += len(out["footer"]["text"])
        if footer.get("icon_url"):
            out["footer"]["icon_url"] = web_url(footer["icon_url"], "footer icon")
    for key in ("image", "thumbnail"):
        part = raw.get(key)
        if isinstance(part, dict) and part.get("url"):
            out[key] = {"url": web_url(part["url"], f"{key} url")}
    author = raw.get("author")
    if isinstance(author, dict) and author.get("name"):
        out["author"] = {"name": text(author["name"], 256, "author name")}
        size += len(out["author"]["name"])
        for k in ("url", "icon_url"):
            if author.get(k):
                out["author"][k] = web_url(author[k], f"author {k}")
    fields = raw.get("fields") or []
    if not isinstance(fields, list) or len(fields) > 25:
        raise BuildError("an embed can have at most 25 fields")
    out["fields"] = []
    for f in fields:
        if not isinstance(f, dict) or not f.get("name") or not f.get("value"):
            raise BuildError("every field needs a name and a value")
        item = {"name": text(f["name"], 256, "field name"), "value": text(f["value"], 1024, "field value"), "inline": bool(f.get("inline", False))}
        size += len(item["name"]) + len(item["value"])
        out["fields"].append(item)
    if not any(out.get(k) for k in ("title", "description", "fields", "image", "thumbnail", "author", "footer")):
        raise BuildError("an embed is empty")
    return out, size


def clean_buttons(raw):
    """Collect link buttons from rows or from a flat list. Returns (buttons, warnings). Other kinds of buttons are skipped."""
    flat, warnings = [], []
    for item in raw or []:
        if isinstance(item, dict) and item.get("type") == 1:
            flat.extend(item.get("components") or [])
        else:
            flat.append(item)
    buttons = []
    for b in flat:
        if not isinstance(b, dict) or b.get("type", 2) != 2:
            warnings.append("a component that is not a button was skipped")
            continue
        if b.get("style") != 5 or not b.get("url"):
            warnings.append("a button that is not a link button was skipped")
            continue
        label = b.get("label")
        if not label:
            raise BuildError("every link button needs a label")
        item = {"label": text(label, 80, "button label"), "url": web_url(b["url"], "button link")}
        emoji = b.get("emoji")
        if isinstance(emoji, dict) and emoji.get("name") and not emoji.get("id") and len(str(emoji["name"])) <= 8:
            item["emoji"] = str(emoji["name"])
        buttons.append(item)
    if len(buttons) > MAX_BUTTONS:
        raise BuildError("at most 25 buttons are possible")
    return buttons, warnings


def parse(data):
    """Turn an exported message into (content, embeds, view, warnings). Raises BuildError."""
    if isinstance(data, list):
        data = {"embeds": data}
    if not isinstance(data, dict):
        raise BuildError("the JSON must be an object")
    if "embeds" not in data and "content" not in data and any(k in data for k in ("title", "description", "fields", "image")):
        data = {"embeds": [data]}
    content = data.get("content") or None
    if content is not None:
        content = text(content, 2000, "content")
    raw_embeds = data.get("embeds") or []
    if not isinstance(raw_embeds, list) or len(raw_embeds) > MAX_EMBEDS:
        raise BuildError("at most 10 embeds are possible")
    embeds, total = [], 0
    for raw in raw_embeds:
        clean, size = clean_embed(raw)
        total += size
        embeds.append(discord.Embed.from_dict(clean))
    if total > MAX_TOTAL:
        raise BuildError("all embeds together may have 6000 characters")
    buttons, warnings = clean_buttons(data.get("components"))
    if not content and not embeds:
        raise BuildError("the message needs text or an embed")
    view = None
    if buttons:
        view = discord.ui.View(timeout=None)
        for b in buttons:
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label=b["label"], url=b["url"], emoji=b.get("emoji")))
    return content, embeds, view, warnings


def export(message):
    """Describe a message of Discord as JSON-ready data in the same format that parse reads."""
    out = {}
    if message.content:
        out["content"] = message.content
    embeds = []
    for e in message.embeds:
        d = e.to_dict()
        d.pop("type", None)
        for key in ("video", "provider"):
            d.pop(key, None)
        embeds.append(d)
    if embeds:
        out["embeds"] = embeds
    rows = []
    for row in getattr(message, "components", []) or []:
        buttons = [{"type": 2, "style": 5, "label": c.label or "", "url": c.url} for c in getattr(row, "children", []) if getattr(c, "url", None)]
        if buttons:
            rows.append({"type": 1, "components": buttons})
    if rows:
        out["components"] = rows
    return out
