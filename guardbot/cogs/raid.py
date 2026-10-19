# Copyright (c) Justyn
import asyncio
import time
from collections import deque
from datetime import timedelta
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import emb, trim

TEXT_ATTRS = ("send_messages", "add_reactions", "create_public_threads", "create_private_threads", "send_messages_in_threads")
VOICE_ATTRS = ("connect",)


class Raid(commands.Cog):
    grp = app_commands.Group(
        name="raid",
        description="Raid protection",
        default_permissions=discord.Permissions(manage_guild=True),
        guild_only=True,
    )
    lgrp = app_commands.Group(
        name="lockdownconfig",
        description="Lockdown settings",
        default_permissions=discord.Permissions(manage_guild=True),
        guild_only=True,
    )

    def __init__(self, bot):
        self.bot = bot
        self.joins = {}
        self.until = {}

    @commands.Cog.listener()
    async def on_member_join(self, member):
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
                except discord.HTTPException:
                    pass
        if notes:
            e = emb("Raid protection triggered", color=discord.Color.dark_red())
            e.add_field(name="Reason", value="\n".join(notes), inline=False)
            e.add_field(name="Action", value=r["action"])
            lines = [f"{m} ({m.id}), account {(discord.utils.utcnow() - m.created_at).days}d old" for m in targets[:15]]
            e.add_field(name="Members", value=trim("\n".join(lines)), inline=False)
            self.bot.log(member.guild, "security", e)

    async def lock(self, guild, reason):
        lk = self.bot.cfg(guild.id)["lockdown"]
        if lk["active"]:
            return 0
        saved, n = {}, 0
        bypass = [guild.get_role(i) for i in lk["bypass_roles"]]
        for ch in guild.channels:
            if isinstance(ch, discord.CategoryChannel) or ch.id in lk["exempt"]:
                continue
            attrs = VOICE_ATTRS if isinstance(ch, (discord.VoiceChannel, discord.StageChannel)) else TEXT_ATTRS
            rec = {}
            try:
                ow = ch.overwrites_for(guild.default_role)
                rec[str(guild.default_role.id)] = {a: getattr(ow, a) for a in attrs}
                for a in attrs:
                    setattr(ow, a, False)
                await ch.set_permissions(guild.default_role, overwrite=ow, reason=reason)
                for role in bypass:
                    if role:
                        bo = ch.overwrites_for(role)
                        rec[str(role.id)] = {a: getattr(bo, a) for a in attrs}
                        setattr(bo, attrs[0], True)
                        await ch.set_permissions(role, overwrite=bo, reason=reason)
                saved[str(ch.id)] = rec
                n += 1
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.3)
        lk["active"], lk["saved"] = True, saved
        self.bot.store.mark("config")
        e = emb("Server locked down", reason, discord.Color.dark_red())
        self.bot.log(guild, "security", e)
        return n

    async def unlock(self, guild, reason):
        lk = self.bot.cfg(guild.id)["lockdown"]
        if not lk["active"]:
            return 0
        n = 0
        for ch_id, rec in lk["saved"].items():
            ch = guild.get_channel(int(ch_id))
            if not ch:
                continue
            for target_id, values in rec.items():
                target = guild.get_role(int(target_id))
                if not target:
                    continue
                try:
                    ow = ch.overwrites_for(target)
                    for a, v in values.items():
                        setattr(ow, a, v)
                    await ch.set_permissions(target, overwrite=None if ow.is_empty() else ow, reason=reason)
                except discord.HTTPException:
                    pass
            n += 1
            await asyncio.sleep(0.3)
        lk["active"], lk["saved"] = False, {}
        self.bot.store.mark("config")
        self.bot.log(guild, "security", emb("Lockdown ended", reason, discord.Color.green()))
        return n

    @commands.hybrid_command(name="lockdown", description="Lock the whole server")
    @app_commands.describe(reason="Reason")
    async def lockdown_cmd(self, ctx, *, reason: Optional[str] = None):
        if self.bot.cfg(ctx.guild.id)["lockdown"]["active"]:
            return await ctx.send("The server is already locked down.", ephemeral=True)
        await ctx.defer()
        n = await self.lock(ctx.guild, reason or f"Lockdown by {ctx.author}")
        await ctx.send(f"Server locked down ({n} channels). Use /unlock to end it.")

    @commands.hybrid_command(name="unlock", description="End the lockdown")
    async def unlock_cmd(self, ctx):
        if not self.bot.cfg(ctx.guild.id)["lockdown"]["active"]:
            return await ctx.send("There is no active lockdown.", ephemeral=True)
        await ctx.defer()
        n = await self.unlock(ctx.guild, f"Unlocked by {ctx.author}")
        await ctx.send(f"Lockdown ended ({n} channels restored).")

    @lgrp.command(name="bypassrole", description="Toggle a role that can still write during a lockdown")
    async def lc_bypass(self, it: discord.Interaction, role: discord.Role):
        lst = self.bot.cfg(it.guild_id)["lockdown"]["bypass_roles"]
        lst.remove(role.id) if role.id in lst else lst.append(role.id)
        self.bot.store.mark("config")
        await it.response.send_message(f"{role.mention} {'can write during a lockdown' if role.id in lst else 'is locked like everyone'}.", ephemeral=True)

    @lgrp.command(name="exempt", description="Toggle a channel that is not touched by a lockdown")
    async def lc_exempt(self, it: discord.Interaction, channel: discord.abc.GuildChannel):
        lst = self.bot.cfg(it.guild_id)["lockdown"]["exempt"]
        lst.remove(channel.id) if channel.id in lst else lst.append(channel.id)
        self.bot.store.mark("config")
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
        r = self.bot.cfg(it.guild_id)["raid"]
        for k, v in (("enabled", enabled), ("joins", joins), ("seconds", seconds), ("action", action), ("min_age", min_age_days), ("lockdown", lockdown)):
            if v is not None:
                r[k] = v
        self.bot.cfg(it.guild_id)["modules"]["raid"] = r["enabled"]
        self.bot.store.mark("config")
        await it.response.send_message(f"Raid protection: {'on' if r['enabled'] else 'off'}, {r['joins']} joins in {r['seconds']}s, action {r['action']}, min account age {r['min_age']}d, auto lockdown {r['lockdown']}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Raid(bot))
