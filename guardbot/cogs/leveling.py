# Copyright (c) Justyn
import asyncio
import bisect
import random
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ..utils import emb

TOTALS = [0]
for _n in range(101):
    TOTALS.append(TOTALS[-1] + 5 * _n * _n + 50 * _n + 100)


def level_of(xp, cap=100):
    return min(bisect.bisect_right(TOTALS, xp) - 1, cap, 100)


def summary(x):
    ann = x["announce"]
    if ann == "channel" and x["announce_channel"]:
        ann = f"<#{x['announce_channel']}>"
    return (
        f"Status: {'on' if x['enabled'] else 'off'}\nChat XP: {x['min']}-{x['max']} every {x['cooldown']}s\n"
        f"Voice XP: {x['voice_xp']} per minute\nMultiplier: {x['multiplier']}\nMax level: {x['max_level']}\n"
        f"Keep older level roles: {x['stack']}\nLevel-up message: {ann}\nText: {x['message']}"
    )


class Leveling(commands.Cog):
    xp = app_commands.Group(name="xp", description="XP and level system", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    lr = app_commands.Group(name="levelrole", description="Roles given at levels", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        self.bot = bot
        self.cd = {}

    async def cog_load(self):
        self.voice_loop.start()

    async def cog_unload(self):
        self.voice_loop.cancel()

    def conf(self, gid):
        return self.bot.cfg(gid)["xp"]

    def on(self, guild):
        return guild is not None and self.bot.module_on(guild.id, "leveling") and self.conf(guild.id)["enabled"]

    async def sync_roles(self, member, level):
        x = self.conf(member.guild.id)
        lr = {int(k): v for k, v in x["level_roles"].items()}
        if not lr:
            return
        eligible = {l: r for l, r in lr.items() if l <= level}
        want = set(eligible.values()) if x["stack"] else ({eligible[max(eligible)]} if eligible else set())
        current = {r.id for r in member.roles}
        add = [r for r in (member.guild.get_role(i) for i in want - current) if r]
        rem = [r for r in (member.guild.get_role(i) for i in (set(lr.values()) - want) & current) if r]
        try:
            if add:
                await member.add_roles(*add, reason="Level reward")
            if rem:
                await member.remove_roles(*rem, reason="Level reward")
        except discord.HTTPException:
            pass

    async def level_up(self, member, level, channel):
        x = self.conf(member.guild.id)
        await self.sync_roles(member, level)
        target = None
        if x["announce"] == "channel" and x["announce_channel"]:
            target = member.guild.get_channel(x["announce_channel"])
        elif x["announce"] in ("same", "channel"):
            target = channel
        if target:
            text = x["message"].replace("{user}", member.mention).replace("{level}", str(level)).replace("{name}", member.display_name)
            try:
                await target.send(text, allowed_mentions=discord.AllowedMentions(users=[member]))
            except discord.HTTPException:
                pass

    async def add_xp(self, member, amount, channel=None):
        x = self.conf(member.guild.id)
        amount = int(round(amount * x["multiplier"]))
        if amount <= 0:
            return
        rec = self.bot.store.user(member.guild.id, member.id)
        old = level_of(rec["xp"], x["max_level"])
        rec["xp"] += amount
        self.bot.store.mark("users")
        new = level_of(rec["xp"], x["max_level"])
        if new > old:
            await self.level_up(member, new, channel)

    async def set_xp(self, member, value):
        rec = self.bot.store.user(member.guild.id, member.id)
        rec["xp"] = max(0, int(value))
        self.bot.store.mark("users")
        await self.sync_roles(member, level_of(rec["xp"], self.conf(member.guild.id)["max_level"]))

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot or not self.on(msg.guild):
            return
        x = self.conf(msg.guild.id)
        if msg.channel.id in x["ignore_channels"] or getattr(msg.channel, "parent_id", None) in x["ignore_channels"]:
            return
        if len(msg.content) < 3 and not msg.attachments:
            return
        key, now = (msg.guild.id, msg.author.id), time.time()
        if now - self.cd.get(key, 0) < x["cooldown"]:
            return
        try:
            await asyncio.sleep(0.5)
            await msg.channel.fetch_message(msg.id)
        except discord.NotFound:
            return
        self.cd[key] = now
        await self.add_xp(msg.author, random.randint(x["min"], max(x["min"], x["max"])), msg.channel)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot or not self.on(member.guild):
            return
        rec = self.bot.store.users(member.guild.id).get(str(member.id))
        if rec and rec["xp"] > 0:
            await self.sync_roles(member, level_of(rec["xp"], self.conf(member.guild.id)["max_level"]))

    @tasks.loop(seconds=60)
    async def voice_loop(self):
        try:
            for guild in self.bot.guilds:
                if not self.on(guild):
                    continue
                x = self.conf(guild.id)
                if x["voice_xp"] <= 0:
                    continue
                for vc in list(guild.voice_channels) + list(guild.stage_channels):
                    if vc == guild.afk_channel or vc.id in x["ignore_channels"]:
                        continue
                    humans = [m for m in vc.members if not m.bot]
                    if len(humans) < 2:
                        continue
                    for m in humans:
                        if m.voice and not (m.voice.self_deaf or m.voice.deaf):
                            await self.add_xp(m, x["voice_xp"])
        except Exception as exc:
            print("voice xp error:", exc)

    @voice_loop.before_loop
    async def _wait(self):
        await self.bot.wait_until_ready()

    @commands.hybrid_command(name="rank", description="Show level and XP")
    @app_commands.describe(user="Member (default: you)")
    async def rank_cmd(self, ctx, user: Optional[discord.Member] = None):
        x = self.conf(ctx.guild.id)
        if not x["enabled"]:
            return await ctx.send("The XP system is off.", ephemeral=True)
        m = user or ctx.author
        xp = self.bot.store.user(ctx.guild.id, m.id)["xp"]
        lvl = level_of(xp, x["max_level"])
        ranking = sorted((r["xp"] for r in self.bot.store.users(ctx.guild.id).values() if r["xp"] > 0), reverse=True)
        pos = ranking.index(xp) + 1 if xp in ranking else len(ranking) + 1
        if lvl >= x["max_level"]:
            bar, prog = "[##########]", "MAX"
        else:
            cur, span = xp - TOTALS[lvl], TOTALS[lvl + 1] - TOTALS[lvl]
            filled = int(10 * cur / span)
            bar, prog = "[" + "#" * filled + "-" * (10 - filled) + "]", f"{cur}/{span} XP"
        e = emb(m.display_name)
        e.set_thumbnail(url=m.display_avatar.url)
        e.add_field(name="Level", value=str(lvl))
        e.add_field(name="Total XP", value=str(xp))
        e.add_field(name="Rank", value=f"#{pos}")
        e.add_field(name="Progress", value=f"{bar} {prog}", inline=False)
        await ctx.send(embed=e)

    @commands.hybrid_command(name="leaderboard", description="Top 10 members by XP")
    async def leaderboard_cmd(self, ctx):
        x = self.conf(ctx.guild.id)
        if not x["enabled"]:
            return await ctx.send("The XP system is off.", ephemeral=True)
        rows = sorted(self.bot.store.users(ctx.guild.id).items(), key=lambda i: i[1]["xp"], reverse=True)
        lines = []
        for uid, rec in rows:
            if rec["xp"] <= 0:
                break
            if ctx.guild.get_member(int(uid)):
                lines.append(f"{len(lines) + 1}. <@{uid}> - level {level_of(rec['xp'], x['max_level'])} ({rec['xp']} XP)")
            if len(lines) == 10:
                break
        await ctx.send(embed=emb("Leaderboard", "\n".join(lines) or "Nobody has XP yet."))

    @xp.command(name="config", description="Change XP system settings")
    @app_commands.describe(multiplier="Global XP multiplier (2.0 = double speed)", voice_xp="XP per minute in voice (0 = off)", message="Level-up text, supports {user}, {name}, {level}")
    async def xp_config(
        self, it: discord.Interaction,
        enabled: Optional[bool] = None,
        min_xp: Optional[app_commands.Range[int, 1, 1000]] = None,
        max_xp: Optional[app_commands.Range[int, 1, 1000]] = None,
        cooldown: Optional[app_commands.Range[int, 0, 3600]] = None,
        voice_xp: Optional[app_commands.Range[int, 0, 1000]] = None,
        multiplier: Optional[app_commands.Range[float, 0.1, 10.0]] = None,
        max_level: Optional[app_commands.Range[int, 1, 100]] = None,
        stack_roles: Optional[bool] = None,
        announce: Optional[Literal["same", "channel", "off"]] = None,
        announce_channel: Optional[discord.TextChannel] = None,
        message: Optional[str] = None,
    ):
        g = self.bot.cfg(it.guild_id)
        x = g["xp"]
        for k, v in (("enabled", enabled), ("min", min_xp), ("max", max_xp), ("cooldown", cooldown), ("voice_xp", voice_xp), ("multiplier", multiplier), ("max_level", max_level), ("stack", stack_roles), ("announce", announce), ("message", message)):
            if v is not None:
                x[k] = v
        if announce_channel:
            x["announce_channel"] = announce_channel.id
            if announce is None:
                x["announce"] = "channel"
        if x["max"] < x["min"]:
            x["max"] = x["min"]
        if enabled is not None:
            g["modules"]["leveling"] = enabled
        self.bot.store.mark("config")
        await it.response.send_message(summary(x), ephemeral=True)

    @xp.command(name="show", description="Show XP settings and level roles")
    async def xp_show(self, it: discord.Interaction):
        x = self.conf(it.guild_id)
        e = emb("XP settings", summary(x))
        e.add_field(name="Level roles", value="\n".join(f"Level {k}: <@&{v}>" for k, v in sorted(x["level_roles"].items(), key=lambda i: int(i[0]))) or "none", inline=False)
        e.add_field(name="Ignored channels", value=" ".join(f"<#{c}>" for c in x["ignore_channels"]) or "none", inline=False)
        await it.response.send_message(embed=e, ephemeral=True)

    @xp.command(name="give", description="Give XP to a member")
    async def xp_give(self, it: discord.Interaction, user: discord.Member, amount: app_commands.Range[int, 1, 100000000]):
        await it.response.defer(ephemeral=True)
        rec = self.bot.store.user(it.guild_id, user.id)
        await self.set_xp(user, rec["xp"] + amount)
        await it.followup.send(f"{user.display_name} now has {rec['xp']} XP.")

    @xp.command(name="take", description="Remove XP from a member")
    async def xp_take(self, it: discord.Interaction, user: discord.Member, amount: app_commands.Range[int, 1, 100000000]):
        await it.response.defer(ephemeral=True)
        rec = self.bot.store.user(it.guild_id, user.id)
        await self.set_xp(user, rec["xp"] - amount)
        await it.followup.send(f"{user.display_name} now has {rec['xp']} XP.")

    @xp.command(name="setlevel", description="Set a member to an exact level")
    async def xp_setlevel(self, it: discord.Interaction, user: discord.Member, level: app_commands.Range[int, 0, 100]):
        await it.response.defer(ephemeral=True)
        await self.set_xp(user, TOTALS[level])
        await it.followup.send(f"{user.display_name} is now level {level}.")

    @xp.command(name="reset", description="Reset a member's XP")
    async def xp_reset(self, it: discord.Interaction, user: discord.Member):
        await it.response.defer(ephemeral=True)
        await self.set_xp(user, 0)
        await it.followup.send(f"XP of {user.display_name} reset.")

    @xp.command(name="ignore", description="Toggle a channel that gives no XP")
    async def xp_ignore(self, it: discord.Interaction, channel: discord.abc.GuildChannel):
        lst = self.conf(it.guild_id)["ignore_channels"]
        lst.remove(channel.id) if channel.id in lst else lst.append(channel.id)
        self.bot.store.mark("config")
        await it.response.send_message(f"{channel.mention} {'gives no XP' if channel.id in lst else 'gives XP again'}.", ephemeral=True)

    @lr.command(name="add", description="Give a role when members reach a level")
    async def lr_add(self, it: discord.Interaction, level: app_commands.Range[int, 1, 100], role: discord.Role):
        if not role.is_assignable():
            return await it.response.send_message("I cannot assign that role. Move my role above it.", ephemeral=True)
        self.conf(it.guild_id)["level_roles"][str(level)] = role.id
        self.bot.store.mark("config")
        await it.response.send_message(f"Level {level} gives {role.mention}.", ephemeral=True)

    @lr.command(name="remove", description="Remove the role of a level")
    async def lr_remove(self, it: discord.Interaction, level: app_commands.Range[int, 1, 100]):
        if self.conf(it.guild_id)["level_roles"].pop(str(level), None) is None:
            return await it.response.send_message("No role set for that level.", ephemeral=True)
        self.bot.store.mark("config")
        await it.response.send_message("Removed.", ephemeral=True)

    @lr.command(name="list", description="List level roles")
    async def lr_list(self, it: discord.Interaction):
        lr = self.conf(it.guild_id)["level_roles"]
        text = "\n".join(f"Level {k}: <@&{v}>" for k, v in sorted(lr.items(), key=lambda i: int(i[0]))) or "No level roles set."
        await it.response.send_message(text, ephemeral=True)

    @lr.command(name="sync", description="Apply level roles to all members")
    async def lr_sync(self, it: discord.Interaction):
        await it.response.defer(ephemeral=True)
        x, n = self.conf(it.guild_id), 0
        for uid, rec in list(self.bot.store.users(it.guild_id).items()):
            m = it.guild.get_member(int(uid))
            if m and rec["xp"] > 0:
                await self.sync_roles(m, level_of(rec["xp"], x["max_level"]))
                n += 1
                await asyncio.sleep(0.3)
        await it.followup.send(f"Synced {n} members.")


async def setup(bot):
    await bot.add_cog(Leveling(bot))
