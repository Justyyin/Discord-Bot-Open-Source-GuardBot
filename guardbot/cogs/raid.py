"""Raid detection and server lockdown."""

import logging
import time
from collections import deque
from datetime import timedelta
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import bulk, emb, trim

log = logging.getLogger(__name__)

TEXT_ATTRS = ("send_messages", "add_reactions", "create_public_threads", "create_private_threads", "send_messages_in_threads")
VOICE_ATTRS = ("connect",)
ROLE_ATTRS = dict(send_messages=False, send_messages_in_threads=False, add_reactions=False, create_public_threads=False, create_private_threads=False, connect=False)


class Raid(commands.Cog):
    """Detects raids and locks the server."""
    grp = app_commands.Group(name="raid", description="Raid protection", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    lgrp = app_commands.Group(name="lockdownconfig", description="Lockdown settings", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot
        self.joins = {}
        self.until = {}

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Runs when a member joins."""
        if member.bot or not self.bot.module_on(member.guild.id, "raid"):
            return
        r = self.bot.cfg(member.guild.id)["raid"]
        if not r["enabled"]:
            return
        gid, now = member.guild.id, time.time()
        dq = self.joins.setdefault(gid, deque())
        dq.append((now, member))
        while dq and now - dq[0][0] > r["seconds"]:
            dq.popleft()
        active = now < self.until.get(gid, 0)
        triggered = len(dq) >= r["joins"]
        targets, notes = [], []
        if triggered:
            self.until[gid] = now + 60
            if active:
                targets = [member]
            else:
                targets = [m for _, m in dq]
                notes.append(f"{len(dq)} joins within {r['seconds']} seconds")
                if r["lockdown"]:
                    await self.lock(member.guild, "Raid protection")
                    notes.append("server locked down")
        elif active:
            targets = [member]
        age = (discord.utils.utcnow() - member.created_at).days
        if r["min_age"] and age < r["min_age"]:
            if member not in targets:
                targets.append(member)
            notes.append(f"account of {member} is {age} days old (minimum {r['min_age']})")
        if not targets:
            return
        if r["action"] != "alert":
            for m in targets:
                try:
                    if r["action"] == "kick":
                        await m.kick(reason="Raid protection")
                    else:
                        await m.timeout(timedelta(hours=1), reason="Raid protection")
                except discord.HTTPException as exc:
                    log.warning("m.kick failed: %s", exc)
        if notes:
            e = emb("Raid protection triggered", color=discord.Color.dark_red())
            e.add_field(name="Reason", value="\n".join(notes), inline=False)
            e.add_field(name="Action", value=r["action"])
            lines = [f"{m} ({m.id}), account {(discord.utils.utcnow() - m.created_at).days}d old" for m in targets[:15]]
            e.add_field(name="Members", value=trim("\n".join(lines)), inline=False)
            self.bot.log(member.guild, "security", e)

    async def lock(self, guild, reason, mode=None):
        """Lock the server in channel mode or role mode. Returns (changed, failed)."""
        lk = self.bot.cfg(guild.id)["lockdown"]
        if lk["active"]:
            return 0, 0
        mode = mode or lk["mode"]
        if mode == "role":
            saved, n, failed = {}, 0, 0
            roles = [guild.default_role] + [r for r in (guild.get_role(i) for i in lk["lock_roles"]) if r]
            for role in roles:
                saved[str(role.id)] = role.permissions.value
                perms = role.permissions
                perms.update(**ROLE_ATTRS)
                try:
                    await role.edit(permissions=perms, reason=reason)
                    n += 1
                except discord.HTTPException as exc:
                    failed += 1
                    log.warning("lockdown could not edit role %s: %s", role.name, exc)
            lk["active"], lk["active_mode"], lk["role_saved"] = True, "role", saved
            self.bot.log(guild, "security", emb("Server locked down (role mode)", reason, discord.Color.dark_red()))
            return n, failed
        saved = {}
        bypass = [r for r in (guild.get_role(i) for i in lk["bypass_roles"]) if r]

        def make(ch):
            """Create the job that locks one channel."""
            async def job():
                """Remove the write permissions of everyone in one channel and keep the old values."""
                attrs = VOICE_ATTRS if isinstance(ch, (discord.VoiceChannel, discord.StageChannel)) else TEXT_ATTRS
                rec = {}
                ow = ch.overwrites_for(guild.default_role)
                rec[str(guild.default_role.id)] = {a: getattr(ow, a) for a in attrs}
                for a in attrs:
                    setattr(ow, a, False)
                await ch.set_permissions(guild.default_role, overwrite=ow, reason=reason)
                for role in bypass:
                    bo = ch.overwrites_for(role)
                    rec[str(role.id)] = {a: getattr(bo, a) for a in attrs}
                    setattr(bo, attrs[0], True)
                    await ch.set_permissions(role, overwrite=bo, reason=reason)
                saved[str(ch.id)] = rec
            return job

        jobs = [make(ch) for ch in guild.channels if not isinstance(ch, discord.CategoryChannel) and ch.id not in lk["exempt"]]
        n, failed = await bulk(jobs, limit=6)
        lk["active"], lk["active_mode"], lk["saved"] = True, "channels", saved
        self.bot.log(guild, "security", emb("Server locked down", reason + (f" ({failed} channels failed)" if failed else ""), discord.Color.dark_red()))
        return n, failed

    async def unlock(self, guild, reason):
        """Restore the permissions saved by the lockdown. Returns (restored, failed)."""
        lk = self.bot.cfg(guild.id)["lockdown"]
        if not lk["active"]:
            return 0, 0
        n = failed = 0
        if lk["active_mode"] == "role":
            for rid, value in lk["role_saved"].items():
                role = guild.get_role(int(rid))
                if role:
                    try:
                        await role.edit(permissions=discord.Permissions(value), reason=reason)
                        n += 1
                    except discord.HTTPException as exc:
                        failed += 1
                        log.warning("unlock could not restore role %s: %s", role.name, exc)
            lk["role_saved"] = {}
        else:
            def make(ch, rec):
                """Create the job that restores one channel."""

                async def job():
                    """Put the saved permission values of one channel back."""
                    for target_id, values in rec.items():
                        target = guild.get_role(int(target_id))
                        if not target:
                            continue
                        ow = ch.overwrites_for(target)
                        for a, v in values.items():
                            setattr(ow, a, v)
                        await ch.set_permissions(target, overwrite=None if ow.is_empty() else ow, reason=reason)
                return job

            jobs = [make(guild.get_channel(int(cid)), rec) for cid, rec in lk["saved"].items() if guild.get_channel(int(cid))]
            n, failed = await bulk(jobs, limit=6)
            lk["saved"] = {}
        lk["active"], lk["active_mode"] = False, None
        self.bot.log(guild, "security", emb("Lockdown ended", reason, discord.Color.green()))
        return n, failed

    @commands.hybrid_command(name="lockdown", description="Lock the whole server")
    @app_commands.describe(mode="channels: edit every channel, role: instant, edits the @everyone role only", reason="Reason")
    async def lockdown_cmd(self, ctx, mode: Optional[Literal["channels", "role"]] = None, *, reason: Optional[str] = None):
        """Lock the whole server."""
        if self.bot.cfg(ctx.guild.id)["lockdown"]["active"]:
            return await ctx.send("The server is already locked down.", ephemeral=True)
        await ctx.defer()
        n, failed = await self.lock(ctx.guild, reason or f"Lockdown by {ctx.author}", mode)
        note = f" {failed} failed, check my permissions." if failed else ""
        await ctx.send(f"Server locked down ({n} items changed).{note} Use /unlock to end it.")

    @commands.hybrid_command(name="unlock", description="End the lockdown")
    async def unlock_cmd(self, ctx):
        """End the lockdown."""
        if not self.bot.cfg(ctx.guild.id)["lockdown"]["active"]:
            return await ctx.send("There is no active lockdown.", ephemeral=True)
        await ctx.defer()
        n, failed = await self.unlock(ctx.guild, f"Unlocked by {ctx.author}")
        note = f" {failed} failed, check my permissions." if failed else ""
        await ctx.send(f"Lockdown ended ({n} items restored).{note}")

    @lgrp.command(name="mode", description="Default lockdown mode")
    @app_commands.describe(mode="channels: thorough, edits every channel. role: instant, edits the @everyone role (channels with their own allow rules stay open)")
    async def lc_mode(self, it: discord.Interaction, mode: Literal["channels", "role"]):
        """Default lockdown mode."""
        self.bot.cfg(it.guild_id)["lockdown"]["mode"] = mode
        await it.response.send_message(f"Default lockdown mode: {mode}", ephemeral=True)

    @lgrp.command(name="lockrole", description="Toggle an extra role whose write permissions are removed in role mode")
    async def lc_lockrole(self, it: discord.Interaction, role: discord.Role):
        """Toggle an extra role whose write permissions are removed in role mode."""
        lst = self.bot.cfg(it.guild_id)["lockdown"]["lock_roles"]
        lst.remove(role.id) if role.id in lst else lst.append(role.id)
        await it.response.send_message(f"{role.mention} {'is locked in role mode' if role.id in lst else 'is no longer locked in role mode'}.", ephemeral=True)

    @lgrp.command(name="bypassrole", description="Toggle a role that can still write during a lockdown")
    async def lc_bypass(self, it: discord.Interaction, role: discord.Role):
        """Toggle a role that can still write during a lockdown."""
        lst = self.bot.cfg(it.guild_id)["lockdown"]["bypass_roles"]
        lst.remove(role.id) if role.id in lst else lst.append(role.id)
        await it.response.send_message(f"{role.mention} {'can write during a lockdown' if role.id in lst else 'is locked like everyone'}.", ephemeral=True)

    @lgrp.command(name="exempt", description="Toggle a channel that is not touched by a lockdown")
    async def lc_exempt(self, it: discord.Interaction, channel: discord.abc.GuildChannel):
        """Toggle a channel that is not touched by a lockdown."""
        lst = self.bot.cfg(it.guild_id)["lockdown"]["exempt"]
        lst.remove(channel.id) if channel.id in lst else lst.append(channel.id)
        await it.response.send_message(f"{channel.mention} {'is exempt' if channel.id in lst else 'is no longer exempt'}.", ephemeral=True)

    @grp.command(name="setup", description="Configure raid protection")
    @app_commands.describe(joins="Joins that count as a raid", seconds="Within this many seconds", action="Response", min_age_days="Minimum account age (0 = off)", lockdown="Lock the server automatically on a raid")
    async def raid_setup(
        self,
        it: discord.Interaction,
        enabled: Optional[bool] = None,
        joins: Optional[app_commands.Range[int, 2, 100]] = None,
        seconds: Optional[app_commands.Range[int, 1, 300]] = None,
        action: Optional[Literal["alert", "timeout", "kick"]] = None,
        min_age_days: Optional[app_commands.Range[int, 0, 365]] = None,
        lockdown: Optional[bool] = None,
    ):
        """Configure raid protection."""
        r = self.bot.cfg(it.guild_id)["raid"]
        for k, v in (("enabled", enabled), ("joins", joins), ("seconds", seconds), ("action", action), ("min_age", min_age_days), ("lockdown", lockdown)):
            if v is not None:
                r[k] = v
        self.bot.cfg(it.guild_id)["modules"]["raid"] = r["enabled"]
        await it.response.send_message(f"Raid protection: {'on' if r['enabled'] else 'off'}, {r['joins']} joins in {r['seconds']}s, action {r['action']}, min account age {r['min_age']}d, auto lockdown {r['lockdown']}", ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Raid(bot))
