"""Watches the staff: raises an alarm when a moderator uses ban, kick, timeout and similar actions too often."""

import asyncio
import logging
import time
from collections import deque
from datetime import timedelta
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from .. import i18n
from ..defaults import DANGEROUS, DEFAULTS
from ..utils import audit_executor, emb, export_hits, fmt_duration, import_hits, parse_duration

log = logging.getLogger(__name__)

A = discord.AuditLogAction
KEYS = tuple(DEFAULTS["modwatch"]["limits"])
ACTIONS = ("alert", "timeout", "strip", "none")
CASE_KEYS = {"warn": "warn", "mute": "timeout", "kick": "kick", "ban": "ban", "unban": "unban", "jail": "jail"}


class ModWatch(commands.Cog):
    """Counts moderation actions per moderator and reacts when a limit is passed."""

    grp = app_commands.Group(name="modwatch", description="Limits for moderators", default_permissions=discord.Permissions(administrator=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the counters."""
        self.bot = bot
        self.hits = {}
        self.seen = deque(maxlen=500)

    def conf(self, gid):
        """Return the settings of a server."""
        return self.bot.cfg(gid)["modwatch"]

    def window(self, key):
        """The time span in seconds that counts for a counter."""
        return self.conf(key[0])["limits"].get(key[2], [0, 0])[1]

    def export_state(self):
        """Counters that should survive a restart."""
        return export_hits(self.hits, self.window)

    async def cog_load(self):
        """Load the counters of the last run."""
        self.hits = import_hits(self.bot.store.state("ModWatch"), self.window, lambda p: (int(p[0]), int(p[1]), p[2]))

    async def count(self, guild, moderator, key):
        """Count one action of a moderator and trigger the response when the limit is reached."""
        if key not in KEYS or not self.bot.module_on(guild.id, "modwatch"):
            return
        me = self.bot.user.id if self.bot.user else None
        if moderator.id in (guild.owner_id, me) or getattr(moderator, "bot", False):
            return
        conf = self.conf(guild.id)
        if moderator.id in conf["whitelist"]:
            return
        limit, secs = conf["limits"].get(key, [0, 0])
        if not limit:
            return
        dq = self.hits.setdefault((guild.id, moderator.id, key), deque())
        now = time.time()
        dq.append(now)
        while dq and now - dq[0] > secs:
            dq.popleft()
        if len(dq) >= limit:
            dq.clear()
            await self.trigger(guild, moderator, key, limit, secs)

    async def trigger(self, guild, moderator, key, limit, secs):
        """Alert, and optionally time out the moderator or remove their dangerous roles."""
        conf = self.conf(guild.id)
        member = guild.get_member(moderator.id)
        result = "alert only"
        if conf["action"] == "timeout" and member:
            try:
                await member.timeout(timedelta(hours=1), reason="Moderator action limit reached")
                result = "timed out for 1 hour"
            except discord.HTTPException as exc:
                log.warning("modwatch could not time out %s: %s", member, exc)
                result = f"timeout failed ({exc})"
        elif conf["action"] == "strip" and member:
            roles = [r for r in member.roles if r.is_assignable() and any(getattr(r.permissions, p) for p in DANGEROUS)]
            try:
                if roles:
                    await member.remove_roles(*roles, reason="Moderator action limit reached")
                    self.bot.store.user(guild.id, member.id)["stripped_roles"] = [r.id for r in roles]
                result = "dangerous roles removed: " + (", ".join(r.name for r in roles) or "none found")
            except discord.HTTPException as exc:
                log.warning("modwatch could not remove roles from %s: %s", member, exc)
                result = f"could not remove roles ({exc})"
        e = emb("MODERATOR LIMIT REACHED", color=discord.Color.dark_red(), user=moderator)
        e.add_field(name="Action", value=f"{limit} x {key} within {fmt_duration(secs)}")
        e.add_field(name="Response", value=result)
        self.bot.log(guild, "security", e)
        if conf["notify_owner"]:
            owner = guild.owner
            if owner:
                try:
                    await owner.send(embed=e)
                except discord.HTTPException as exc:
                    log.warning("modwatch could not DM the owner of %s: %s", guild.id, exc)

    async def from_audit(self, guild, action, key, target_id):
        """Count an action that a moderator did in the Discord interface, found through the audit log."""
        if not self.bot.module_on(guild.id, "modwatch"):
            return
        await asyncio.sleep(1.5)
        entry = await audit_executor(guild, action, target_id)
        if entry and entry.user and entry.id not in self.seen:
            self.seen.append(entry.id)
            await self.count(guild, entry.user, key)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Runs when a member is banned."""
        await self.from_audit(guild, A.ban, "ban", user.id)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """Runs when a user is unbanned."""
        await self.from_audit(guild, A.unban, "unban", user.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Runs when a member leaves or is removed. Only kicks are counted."""
        await self.from_audit(member.guild, A.kick, "kick", member.id)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Runs when a member changes. Only new timeouts are counted."""
        if after.timed_out_until and after.timed_out_until != before.timed_out_until:
            await self.from_audit(after.guild, A.member_update, "timeout", after.id)

    @grp.command(name="status", description="Show the limits and the response")
    async def mw_status(self, it: discord.Interaction):
        """Show the limits and the response."""
        c = self.conf(it.guild_id)
        lines = [f"Module: {'on' if self.bot.module_on(it.guild_id, 'modwatch') else 'off'}", f"Response: {c['action']}, DM the owner: {c['notify_owner']}"]
        for key in KEYS:
            n, secs = c["limits"].get(key, [0, 0])
            lines.append(f"{key}: " + (f"{n} within {fmt_duration(secs)}" if n else "no limit"))
        lines.append("Excluded: " + (" ".join(f"<@{i}>" for i in c["whitelist"]) or "nobody"))
        await it.response.send_message("\n".join(lines), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @grp.command(name="limit", description="Set how many actions of one type a moderator may do in a time span (0 = no limit)")
    @app_commands.describe(kind="Action", count="Maximum number", window="Time span, for example 30m or 1h")
    async def mw_limit(self, it: discord.Interaction, kind: Literal[KEYS], count: app_commands.Range[int, 0, 500], window: Optional[str] = None):
        """Set how many actions of one type a moderator may do in a time span (0 = no limit)."""
        secs = parse_duration(window) if window else self.conf(it.guild_id)["limits"][kind][1]
        if not secs or secs < 10 or secs > 86400 * 7:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Invalid time span. Use values like 10m, 1h or 1d (10 seconds to 7 days)."), ephemeral=True)
        self.conf(it.guild_id)["limits"][kind] = [count, secs]
        await it.response.send_message(f"{kind}: {count} within {fmt_duration(secs)}" if count else f"{kind}: no limit", ephemeral=True)

    @grp.command(name="action", description="Choose what happens when a limit is reached")
    @app_commands.describe(action="alert = log only, timeout = 1 hour, strip = remove roles with dangerous permissions, none = count only")
    async def mw_action(self, it: discord.Interaction, action: Literal[ACTIONS], notify_owner: Optional[bool] = None):
        """Choose what happens when a limit is reached."""
        c = self.conf(it.guild_id)
        c["action"] = action
        if notify_owner is not None:
            c["notify_owner"] = notify_owner
        await it.response.send_message(f"Response: {action}, DM the owner: {c['notify_owner']}", ephemeral=True)

    @grp.command(name="exclude", description="Toggle a member who is not limited")
    async def mw_exclude(self, it: discord.Interaction, member: discord.Member):
        """Toggle a member who is not limited."""
        lst = self.conf(it.guild_id)["whitelist"]
        lst.remove(member.id) if member.id in lst else lst.append(member.id)
        await it.response.send_message(f"{member.mention} is {'excluded' if member.id in lst else 'limited again'}.", ephemeral=True, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(ModWatch(bot))
