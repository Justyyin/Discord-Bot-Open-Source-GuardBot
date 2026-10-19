# Copyright (c) Justyn
import re
from urllib.parse import urlparse

import discord

AUTHOR = "Justyn"
CREDIT = "GuardBot \u00a9 " + AUTHOR
VIDEO_EXT = (".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v")
GIF_HOSTS = ("tenor.com", "giphy.com")
URL_RE = re.compile(r"(?:https?://|www\.|discord\.gg/|discord\.com/invite/)\S+", re.I)
LOG_FILE_LIMIT = 8 * 1024 * 1024
UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}


def trim(s, n=1000):
    s = s or ""
    if not s.strip():
        return "-"
    return s if len(s) <= n else s[: n - 3] + "..."


def hosts(text):
    out = []
    for u in URL_RE.findall(text or ""):
        try:
            h = urlparse(u if "://" in u else "//" + u).hostname
        except ValueError:
            h = None
        if h:
            out.append(h.lower().rstrip("."))
    return out


def is_image(a):
    return (a.content_type or "").startswith("image/")


def is_gif(a):
    return (a.content_type or "") == "image/gif" or a.filename.lower().endswith(".gif")


def is_video(a):
    return (a.content_type or "").startswith("video/") or a.filename.lower().endswith(VIDEO_EXT)


def has_gif_link(text):
    return any(h == g or h.endswith("." + g) for h in hosts(text) for g in GIF_HOSTS)


def has_image(msg):
    return any(is_image(a) for a in msg.attachments) or any(e.type == "image" for e in msg.embeds)


def has_video(msg):
    return any(is_video(a) for a in msg.attachments) or any(e.type == "video" for e in msg.embeds)


def kinds(msg):
    out = []
    if URL_RE.sub("", msg.content).strip():
        out.append("Text")
    if URL_RE.search(msg.content):
        out.append("URL")
    atts = msg.attachments
    if any(is_image(a) and not is_gif(a) for a in atts):
        out.append("Image")
    if any(is_gif(a) for a in atts) or has_gif_link(msg.content):
        out.append("GIF")
    if any(is_video(a) for a in atts):
        out.append("Video")
    if any(not (is_image(a) or is_video(a)) for a in atts):
        out.append("File")
    if msg.stickers:
        out.append("Sticker")
    return out or ["Other"]


def att_lines(msg):
    out, size = [], 0
    for a in msg.attachments:
        line = f"[{a.filename}]({a.url})"
        if size + len(line) > 1000:
            break
        out.append(line)
        size += len(line) + 1
    return "\n".join(out)


async def grab_files(msg):
    files, total = [], 0
    for a in msg.attachments[:4]:
        if total + a.size > LOG_FILE_LIMIT:
            continue
        try:
            files.append(await a.to_file())
            total += a.size
        except Exception:
            pass
    return files


def emb(title=None, desc=None, color=None, user=None, footer=None):
    e = discord.Embed(title=title, description=desc, color=color or discord.Color.blurple(), timestamp=discord.utils.utcnow())
    if user:
        e.set_author(name=f"{user} ({user.id})", icon_url=user.display_avatar.url)
    e.set_footer(text=f"{footer} | {CREDIT}" if footer else CREDIT)
    return e


def describe(e, msg):
    e.description = trim(msg.content, 3500)
    e.add_field(name="Channel", value=msg.channel.mention)
    e.add_field(name="Type", value=", ".join(kinds(msg)))
    lines = att_lines(msg)
    if lines:
        e.add_field(name="Attachments", value=lines, inline=False)
    for a in msg.attachments:
        if is_image(a):
            e.set_thumbnail(url=a.url)
            break
    e.set_footer(text=f"Message ID {msg.id} | {CREDIT}")


def parse_duration(text):
    m = re.fullmatch(r"(\d+)\s*([smhdw])?", (text or "").strip().lower())
    if not m:
        return None
    return int(m.group(1)) * UNITS[m.group(2) or "m"]


def fmt_duration(sec):
    sec = int(sec)
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60)):
        if sec >= size:
            return f"{sec // size}{unit}"
    return f"{sec}s"


async def audit_executor(guild, action, target_id=None, within=20):
    if not guild.me or not guild.me.guild_permissions.view_audit_log:
        return None
    try:
        async for entry in guild.audit_logs(limit=8, action=action):
            if (discord.utils.utcnow() - entry.created_at).total_seconds() > within:
                break
            if target_id is None or (entry.target is not None and getattr(entry.target, "id", None) == target_id):
                return entry
    except discord.HTTPException:
        pass
    return None
