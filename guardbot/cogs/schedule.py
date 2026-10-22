"""Scheduled messages: posts at a set time, once or repeating."""

import logging
import math
import re
import time
from datetime import datetime, timedelta
from typing import Literal, Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import discord
from discord import app_commands
from discord.ext import commands, tasks

from .. import i18n
from ..utils import AdminGroup, emb, parse_duration

log = logging.getLogger(__name__)

MAX_ITEMS = 25
STEP = {"hourly": timedelta(hours=1), "daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


def parse_when(text, tz, now):
    """Read 'in 2h', 'HH:MM' (next time it is that clock time) or 'YYYY-MM-DD HH:MM' in a time zone. Returns a timestamp in the future or None."""
    text = (text or "").strip().lower()
    m = re.fullmatch(r"in\s+(\S+)", text)
    if m:
        seconds = parse_duration(m.group(1))
        return now + seconds if seconds else None
    local = datetime.fromtimestamp(now, tz)
    try:
        if re.fullmatch(r"\d{1,2}:\d{2}", text):
            hh, mm = map(int, text.split(":"))
            at = local.replace(hour=hh, minute=mm, second=0, microsecond=0)
            if at.timestamp() <= now:
                at += timedelta(days=1)
        else:
            at = datetime.strptime(text, "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    except ValueError:
        return None
    ts = at.timestamp()
    return ts if ts > now else None


def valid_item(item):
    """True if a stored scheduled message has the expected shape. Imported or damaged data must not stop the loop."""
    return (
        isinstance(item, dict) and isinstance(item.get("channel"), int) and isinstance(item.get("at"), (int, float)) and not isinstance(item.get("at"), bool)
        and isinstance(item.get("text"), str) and item.get("repeat") in ("none", *STEP)
    )


def advance(at, repeat, tz, now):
    """Move a repeating time forward to the next time after now. Missed runs are skipped, not caught up."""
    if repeat == "hourly":
        return at + math.ceil((now - at) / 3600 + 1e-9) * 3600 if at <= now else at
    step = STEP[repeat]
    for _ in range(500):
        if at > now:
            return at
        at = (datetime.fromtimestamp(at, tz) + step).timestamp()
    return now + step.total_seconds()


class Schedule(commands.Cog):
    """Scheduled messages."""

    sg = AdminGroup(name="schedule", description="Messages that are posted later or on repeat", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    async def cog_load(self):
        """Start the loop."""
        self.loop.start()

    async def cog_unload(self):
        """Stop the loop."""
        self.loop.cancel()

    def conf(self, gid):
        """Return the schedule settings of a server."""
        return self.bot.cfg(gid)["schedule"]

    def zone(self, gid):
        """Return the time zone of a server."""
        try:
            return ZoneInfo(self.conf(gid)["timezone"])
        except (ZoneInfoNotFoundError, ValueError):
            return ZoneInfo("UTC")

    @tasks.loop(seconds=30)
    async def loop(self):
        """Post what is due."""
        now = time.time()
        for guild in list(self.bot.guilds):
            if not self.bot.module_on(guild.id, "schedule"):
                continue
            c = self.conf(guild.id)
            for sid, item in list(c["items"].items()):
                if not valid_item(item):
                    c["items"].pop(sid, None)
                    log.warning("removed a damaged scheduled message on %s", guild.id)
                    continue
                if item["at"] > now:
                    continue
                if item["repeat"] == "none":
                    c["items"].pop(sid, None)
                else:
                    item["at"] = advance(item["at"], item["repeat"], self.zone(guild.id), now)
                try:
                    await self.send(guild, sid, item)
                except Exception:  # one broken message must not stop the others
                    log.exception("scheduled message %s on %s failed", sid, guild.id)

    @loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected."""
        await self.bot.wait_until_ready()

    async def send(self, guild, sid, item):
        """Post one scheduled message. Messages to a channel that is gone or closed are removed and reported."""
        ch = guild.get_channel(item["channel"])
        failed = ch is None
        if not failed:
            try:
                await ch.send(item["text"], allowed_mentions=discord.AllowedMentions(everyone=False, roles=True, users=True))
            except (discord.Forbidden, discord.NotFound):
                failed = True
            except discord.HTTPException as exc:
                log.warning("scheduled message failed: %s", exc)
        if failed:
            self.conf(guild.id)["items"].pop(sid, None)
            self.bot.log(guild, "main", emb("Scheduled message removed", f"Message {sid} could not be posted in <#{item['channel']}> and was removed. Check my permissions there.", color=discord.Color.orange()))

    @sg.command(name="add", description="Schedule a message")
    @app_commands.describe(channel="Channel", when="in 2h, 18:30 (next time) or 2026-12-24 18:00, in the server time zone", text="Message", repeat="How often it is repeated")
    async def add(self, it: discord.Interaction, channel: discord.TextChannel, when: str, text: app_commands.Range[str, 1, 1800], repeat: Literal["none", "hourly", "daily", "weekly"] = "none"):
        """Schedule a message."""
        c = self.conf(it.guild_id)
        if len(c["items"]) >= MAX_ITEMS:
            return await it.response.send_message(f"A server can have {MAX_ITEMS} scheduled messages.", ephemeral=True)
        if not channel.permissions_for(it.guild.me).send_messages:
            return await it.response.send_message(i18n.say(it.client, it.guild, "I cannot post in that channel."), ephemeral=True)
        at = parse_when(when, self.zone(it.guild_id), time.time())
        if at is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "I did not understand the time, or it is in the past. Use in 2h, 18:30 or 2026-12-24 18:00."), ephemeral=True)
        sid = str(c["next"])
        c["next"] += 1
        c["items"][sid] = {"channel": channel.id, "at": at, "text": text, "repeat": repeat, "by": it.user.id}
        await it.response.send_message(f"Scheduled as {sid} for <t:{int(at)}:F> (<t:{int(at)}:R>).", ephemeral=True)

    @sg.command(name="list", description="Show scheduled messages")
    async def list(self, it: discord.Interaction):
        """Show scheduled messages."""
        c = self.conf(it.guild_id)
        lines = [f"{sid}. <#{i['channel']}> <t:{int(i['at'])}:f> {i['repeat']}: {i['text'][:60]}" for sid, i in sorted(c["items"].items(), key=lambda kv: kv[1]["at"])]
        await it.response.send_message("\n".join(lines) or "Nothing is scheduled.", ephemeral=True)

    @sg.command(name="remove", description="Delete a scheduled message")
    @app_commands.describe(number="Number from /post schedule list")
    async def remove(self, it: discord.Interaction, number: int):
        """Delete a scheduled message."""
        gone = self.conf(it.guild_id)["items"].pop(str(number), None)
        await it.response.send_message("Deleted." if gone else "There is no such message.", ephemeral=True)

    @sg.command(name="timezone", description="Set the time zone for times like 18:30")
    @app_commands.describe(name="For example Europe/Berlin or UTC")
    async def timezone(self, it: discord.Interaction, name: Optional[str] = None):
        """Set the time zone, or show it when no name is given."""
        c = self.conf(it.guild_id)
        if name:
            try:
                ZoneInfo(name)
            except (ZoneInfoNotFoundError, ValueError):
                return await it.response.send_message(i18n.say(it.client, it.guild, "Unknown time zone. Use a name like Europe/Berlin."), ephemeral=True)
            c["timezone"] = name
        await it.response.send_message(f"Time zone: {c['timezone']}", ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Schedule(bot))
