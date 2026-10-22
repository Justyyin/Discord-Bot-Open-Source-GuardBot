"""Helpers shared by the cogs: text, message analysis, embeds, durations, audit log lookup and bulk calls."""

import asyncio
import logging
import re
import time
from collections import deque
from urllib.parse import urlparse

import discord
from discord import app_commands

log = logging.getLogger(__name__)

AUTHOR = "Justyn"
CREDIT = "GuardBot \u00a9 " + AUTHOR
VIDEO_EXT = (".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v")
GIF_HOSTS = ("tenor.com", "giphy.com")
URL_RE = re.compile(r"(?:https?://|www\.|discord\.gg/|discord\.com/invite/)\S+", re.I)
LOG_FILE_LIMIT = 8 * 1024 * 1024
UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}


def trim(s, n=1000):
    """Shorten a text to a length and return a dash for empty text."""
    s = s or ""
    if not s.strip():
        return "-"
    return s if len(s) <= n else s[: n - 3] + "..."


def hosts(text):
    """Return the host names of all links in a text."""
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
    """True if an attachment is an image."""
    return (a.content_type or "").startswith("image/")


def is_gif(a):
    """True if an attachment is a GIF."""
    return (a.content_type or "") == "image/gif" or a.filename.lower().endswith(".gif")


def is_video(a):
    """True if an attachment is a video."""
    return (a.content_type or "").startswith("video/") or a.filename.lower().endswith(VIDEO_EXT)


def has_gif_link(text):
    """True if a text links to a known GIF site."""
    return any(h == g or h.endswith("." + g) for h in hosts(text) for g in GIF_HOSTS)


def has_image(msg):
    """True if a message contains an image attachment or image embed."""
    return any(is_image(a) for a in msg.attachments) or any(e.type == "image" for e in msg.embeds)


def has_video(msg):
    """True if a message contains a video attachment or video embed."""
    return any(is_video(a) for a in msg.attachments) or any(e.type == "video" for e in msg.embeds)


def kinds(msg):
    """Name the content types of a message: text, URL, image, GIF, video, file or sticker."""
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
    """List the attachments of a message as markdown links within the embed limit."""
    out, size = [], 0
    for a in msg.attachments:
        line = f"[{a.filename}]({a.url})"
        if size + len(line) > 1000:
            break
        out.append(line)
        size += len(line) + 1
    return "\n".join(out)


async def grab_files(msg):
    """Download up to four attachments again so they can be posted in the log."""
    files, total = [], 0
    for a in msg.attachments[:4]:
        if total + a.size > LOG_FILE_LIMIT:
            continue
        try:
            files.append(await a.to_file())
            total += a.size
        except (discord.HTTPException, discord.ClientException) as exc:
            log.warning("could not re-download attachment %s for the log: %s", a.filename, exc)
    return files


def emb(title=None, desc=None, color=None, user=None, footer=None):
    """Create an embed with timestamp, optional author and the credit in the footer."""
    e = discord.Embed(title=title, description=desc, color=color or discord.Color.blurple(), timestamp=discord.utils.utcnow())
    if user:
        e.set_author(name=f"{user} ({user.id})", icon_url=user.display_avatar.url)
    e.set_footer(text=f"{footer} | {CREDIT}" if footer else CREDIT)
    return e


def describe(e, msg):
    """Fill an embed with the content, channel, type and attachments of a message."""
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
    """Convert 30m, 2h or 1d to seconds, or None if the text is not a duration."""
    m = re.fullmatch(r"(\d+)\s*([smhdw])?", (text or "").strip().lower())
    if not m:
        return None
    return int(m.group(1)) * UNITS[m.group(2) or "m"]


def fmt_duration(sec):
    """Convert seconds to a short text like 2h."""
    sec = int(sec)
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60)):
        if sec >= size:
            return f"{sec // size}{unit}"
    return f"{sec}s"


async def audit_executor(guild, action, target_id=None, within=20):
    """Find the recent audit log entry for an action, or None."""
    if not guild.me or not guild.me.guild_permissions.view_audit_log:
        return None
    try:
        async for entry in guild.audit_logs(limit=8, action=action):
            if (discord.utils.utcnow() - entry.created_at).total_seconds() > within:
                break
            if target_id is None or (entry.target is not None and getattr(entry.target, "id", None) == target_id):
                return entry
    except discord.HTTPException as exc:
        log.warning("guild.audit_logs failed: %s", exc)
    return None


async def bulk(factories, limit=5):
    """Run many Discord calls with limited concurrency and return (succeeded, failed)."""
    sem = asyncio.Semaphore(limit)
    ok = failed = 0

    async def run(make):
        """Run one job inside the concurrency limit and count the result."""
        nonlocal ok, failed
        async with sem:
            try:
                await make()
                ok += 1
            except discord.HTTPException as exc:
                failed += 1
                log.warning("bulk operation failed: %s", exc)

    await asyncio.gather(*(run(f) for f in factories))
    return ok, failed


async def transcript(channel, header):
    """Return the whole history of a channel as UTF-8 text bytes, starting with a header line."""
    lines = [f"{header} | {CREDIT}", ""]
    async for m in channel.history(limit=None, oldest_first=True):
        text = m.content + "".join(f"\n[attachment] {a.url}" for a in m.attachments)
        lines.append(f"[{m.created_at:%Y-%m-%d %H:%M}] {m.author} ({m.author.id}): {text}")
    return "\n".join(lines).encode("utf-8")


class AdminGroup(app_commands.Group):
    """Sub group for settings. Discord cannot hide single sub commands, so every command in it checks Manage Server itself."""

    async def interaction_check(self, interaction):
        """Allow only members with Manage Server and tell everyone else why the command did nothing."""
        if interaction.guild and interaction.user.guild_permissions.manage_guild:
            return True
        await interaction.response.send_message("You need the Manage Server permission for this.", ephemeral=True)
        return False


def export_hits(hits, window_of, now=None):
    """Turn {key tuple: deque of timestamps} into JSON data. Entries older than their window are dropped."""
    now = now or time.time()
    out = {}
    for key, dq in hits.items():
        fresh = [round(t, 1) for t in dq if now - t <= window_of(key)]
        if fresh:
            out["|".join(str(k) for k in key)] = fresh
    return out


def import_hits(raw, window_of, convert, now=None):
    """Rebuild the counters from JSON data and skip entries that are too old or damaged."""
    now = now or time.time()
    hits = {}
    for text, stamps in (raw or {}).items():
        try:
            key = convert(text.split("|"))
            window = window_of(key)
        except (ValueError, KeyError, TypeError):
            continue
        fresh = [t for t in stamps if isinstance(t, (int, float)) and now - t <= window]
        if fresh:
            hits[key] = deque(fresh)
    return hits


async def require(it, perm="manage_guild"):
    """True if the user of an interaction has a permission. Otherwise tell the user and return False. For commands that share a group with commands everyone may use."""
    if it.guild and getattr(it.user.guild_permissions, perm, False):
        return True
    await it.response.send_message(f"You need the {perm.replace('_', ' ').title()} permission for this.", ephemeral=True)
    return False
