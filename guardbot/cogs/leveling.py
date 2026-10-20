"""XP and levels for chat and voice, level roles, boosts and rank cards."""

import asyncio
import bisect
import io
import logging
import random
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ..images import HAVE_PIL, rank_card
from ..utils import emb

log = logging.getLogger(__name__)

TOTALS = [0]
for _n in range(101):
    TOTALS.append(TOTALS[-1] + 5 * _n * _n + 50 * _n + 100)


def level_of(xp, cap=100):
    """Return the level for an XP total, limited by the highest allowed level."""
    return min(bisect.bisect_right(TOTALS, xp) - 1, cap, 100)


def summary(x):
    """Describe the XP settings as text."""
    ann = x["announce"]
    if ann == "channel" and x["announce_channel"]:
        ann = f"<#{x['announce_channel']}>"
    return (
        f"Status: {'on' if x['enabled'] else 'off'}\nChat XP: {x['min']}-{x['max']} every {x['cooldown']}s\n"
        f"Voice XP: {x['voice_xp']} per minute\nMultiplier: {x['multiplier']}\nMax level: {x['max_level']}\n"
        f"Keep older level roles: {x['stack']}\nLevel-up message: {ann}\nText: {x['message']}"
    )


class Leveling(commands.Cog):
    """XP, levels, level roles, boosts and rank cards."""
    xp = app_commands.Group(name="xp", description="XP and level system", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    lr = app_commands.Group(name="levelrole", description="Roles given at levels", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot
        self.cd = {}

    async def cog_load(self):
        """Start the background loop of this cog."""
        self.voice_loop.start()

    async def cog_unload(self):
        """Stop the background loop of this cog."""
        self.voice_loop.cancel()

    def conf(self, gid):
        """Return the XP settings of a server."""
        return self.bot.cfg(gid)["xp"]

    def on(self, guild):
        """True if the module and the XP system are both turned on."""
        return guild is not None and self.bot.module_on(guild.id, "leveling") and self.conf(guild.id)["enabled"]

    async def sync_roles(self, member, level):
        """Give the level roles a member earned and remove the ones they should not have."""
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
        except discord.HTTPException as exc:
            log.warning("member.add_roles failed: %s", exc)

    async def level_up(self, member, level, channel):
        """Update the level roles and announce the new level."""
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
            except discord.HTTPException as exc:
                log.warning("target.send failed: %s", exc)

    async def add_xp(self, member, amount, channel=None):
        """Add XP with the global multiplier and the best role boost, and handle level-ups."""
        x = self.conf(member.guild.id)
        boost = max([x["boosts"].get(str(r.id), 1.0) for r in member.roles] or [1.0])
        amount = int(round(amount * x["multiplier"] * boost))
        if amount <= 0:
            return
        rec = self.bot.store.user(member.guild.id, member.id)
        old = level_of(rec["xp"], x["max_level"])
        rec["xp"] += amount
        new = level_of(rec["xp"], x["max_level"])
        if new > old:
            await self.level_up(member, new, channel)

    async def set_xp(self, member, value):
        """Set the XP of a member to an exact value and update their level roles."""
        rec = self.bot.store.user(member.guild.id, member.id)
        rec["xp"] = max(0, int(value))
        await self.sync_roles(member, level_of(rec["xp"], self.conf(member.guild.id)["max_level"]))

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Runs for every new message."""
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
        """Runs when a member joins."""
        if member.bot or not self.on(member.guild):
            return
        rec = self.bot.store.users(member.guild.id).get(str(member.id))
        if rec and rec["xp"] > 0:
            await self.sync_roles(member, level_of(rec["xp"], self.conf(member.guild.id)["max_level"]))

    @tasks.loop(seconds=60)
    async def voice_loop(self):
        """Give voice XP to members who talk with at least one other person."""
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
        except Exception:
            log.exception("voice xp loop failed")

    @voice_loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected before the loop starts."""
        await self.bot.wait_until_ready()

    @commands.hybrid_command(name="rank", description="Show level and XP")
    @app_commands.describe(user="Member (default: you)")
    async def rank_cmd(self, ctx, user: Optional[discord.Member] = None):
        """Show level and XP."""
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
        if x["card"] and HAVE_PIL:
            try:
                avatar = await m.display_avatar.replace(size=256, format="png").read()
                cur, span = (0, 1) if lvl >= x["max_level"] else (xp - TOTALS[lvl], TOTALS[lvl + 1] - TOTALS[lvl])
                data = await asyncio.to_thread(rank_card, m.display_name, avatar, lvl, pos, cur, span, xp, lvl >= x["max_level"])
                return await ctx.send(file=discord.File(io.BytesIO(data), filename="rank.png"))
            except Exception as exc:
                log.warning("rank card failed, falling back to an embed: %s", exc)
        e = emb(m.display_name)
        e.set_thumbnail(url=m.display_avatar.url)
        e.add_field(name="Level", value=str(lvl))
        e.add_field(name="Total XP", value=str(xp))
        e.add_field(name="Rank", value=f"#{pos}")
        e.add_field(name="Progress", value=f"{bar} {prog}", inline=False)
        await ctx.send(embed=e)

    @commands.hybrid_command(name="leaderboard", description="Top 10 members by XP")
    async def leaderboard_cmd(self, ctx):
        """Top 10 members by XP."""
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
        card: Optional[bool] = None,
    ):
        """Change XP system settings."""
        g = self.bot.cfg(it.guild_id)
        x = g["xp"]
        for k, v in (("card", card), ("enabled", enabled), ("min", min_xp), ("max", max_xp), ("cooldown", cooldown), ("voice_xp", voice_xp), ("multiplier", multiplier), ("max_level", max_level), ("stack", stack_roles), ("announce", announce), ("message", message)):
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
        await it.response.send_message(summary(x), ephemeral=True)

    @xp.command(name="show", description="Show XP settings and level roles")
    async def xp_show(self, it: discord.Interaction):
        """Show XP settings and level roles."""
        x = self.conf(it.guild_id)
        e = emb("XP settings", summary(x))
        e.add_field(name="Level roles", value="\n".join(f"Level {k}: <@&{v}>" for k, v in sorted(x["level_roles"].items(), key=lambda i: int(i[0]))) or "none", inline=False)
        e.add_field(name="Ignored channels", value=" ".join(f"<#{c}>" for c in x["ignore_channels"]) or "none", inline=False)
        e.add_field(name="Role boosts", value="\n".join(f"<@&{k}>: x{v}" for k, v in x["boosts"].items()) or "none", inline=False)
        await it.response.send_message(embed=e, ephemeral=True)

    @xp.command(name="boost", description="XP multiplier for a role (1.0 removes the boost)")
    async def xp_boost(self, it: discord.Interaction, role: discord.Role, multiplier: app_commands.Range[float, 0.1, 10.0]):
        """XP multiplier for a role (1.0 removes the boost)."""
        boosts = self.conf(it.guild_id)["boosts"]
        if multiplier == 1.0:
            boosts.pop(str(role.id), None)
        else:
            boosts[str(role.id)] = multiplier
        await it.response.send_message(f"{role.mention}: x{multiplier}", ephemeral=True)

    @xp.command(name="give", description="Give XP to a member")
    async def xp_give(self, it: discord.Interaction, user: discord.Member, amount: app_commands.Range[int, 1, 100000000]):
        """Give XP to a member."""
        await it.response.defer(ephemeral=True)
        rec = self.bot.store.user(it.guild_id, user.id)
        await self.set_xp(user, rec["xp"] + amount)
        await it.followup.send(f"{user.display_name} now has {rec['xp']} XP.")

    @xp.command(name="take", description="Remove XP from a member")
    async def xp_take(self, it: discord.Interaction, user: discord.Member, amount: app_commands.Range[int, 1, 100000000]):
        """Remove XP from a member."""
        await it.response.defer(ephemeral=True)
        rec = self.bot.store.user(it.guild_id, user.id)
        await self.set_xp(user, rec["xp"] - amount)
        await it.followup.send(f"{user.display_name} now has {rec['xp']} XP.")

    @xp.command(name="setlevel", description="Set a member to an exact level")
    async def xp_setlevel(self, it: discord.Interaction, user: discord.Member, level: app_commands.Range[int, 0, 100]):
        """Set a member to an exact level."""
        await it.response.defer(ephemeral=True)
        await self.set_xp(user, TOTALS[level])
        await it.followup.send(f"{user.display_name} is now level {level}.")

    @xp.command(name="reset", description="Reset a member's XP")
    async def xp_reset(self, it: discord.Interaction, user: discord.Member):
        """Reset a member's XP."""
        await it.response.defer(ephemeral=True)
        await self.set_xp(user, 0)
        await it.followup.send(f"XP of {user.display_name} reset.")

    @xp.command(name="ignore", description="Toggle a channel that gives no XP")
    async def xp_ignore(self, it: discord.Interaction, channel: discord.abc.GuildChannel):
        """Toggle a channel that gives no XP."""
        lst = self.conf(it.guild_id)["ignore_channels"]
        lst.remove(channel.id) if channel.id in lst else lst.append(channel.id)
        await it.response.send_message(f"{channel.mention} {'gives no XP' if channel.id in lst else 'gives XP again'}.", ephemeral=True)

    @lr.command(name="add", description="Give a role when members reach a level")
    async def lr_add(self, it: discord.Interaction, level: app_commands.Range[int, 1, 100], role: discord.Role):
        """Give a role when members reach a level."""
        if not role.is_assignable():
            return await it.response.send_message("I cannot assign that role. Move my role above it.", ephemeral=True)
        self.conf(it.guild_id)["level_roles"][str(level)] = role.id
        await it.response.send_message(f"Level {level} gives {role.mention}.", ephemeral=True)

    @lr.command(name="remove", description="Remove the role of a level")
    async def lr_remove(self, it: discord.Interaction, level: app_commands.Range[int, 1, 100]):
        """Remove the role of a level."""
        if self.conf(it.guild_id)["level_roles"].pop(str(level), None) is None:
            return await it.response.send_message("No role set for that level.", ephemeral=True)
        await it.response.send_message("Removed.", ephemeral=True)

    @lr.command(name="list", description="List level roles")
    async def lr_list(self, it: discord.Interaction):
        """List level roles."""
        lr = self.conf(it.guild_id)["level_roles"]
        text = "\n".join(f"Level {k}: <@&{v}>" for k, v in sorted(lr.items(), key=lambda i: int(i[0]))) or "No level roles set."
        await it.response.send_message(text, ephemeral=True)

    @lr.command(name="sync", description="Apply level roles to all members")
    async def lr_sync(self, it: discord.Interaction):
        """Apply level roles to all members."""
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
    """Register the cog with the bot."""
    await bot.add_cog(Leveling(bot))
