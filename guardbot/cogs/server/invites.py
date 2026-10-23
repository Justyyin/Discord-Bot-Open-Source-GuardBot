"""Invite tracking: shows which invite and which member brought a new member, and warns about invite abuse."""

import asyncio
import logging
import time
from collections import deque
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from ... import i18n
from ...utils import emb, export_hits, import_hits

log = logging.getLogger(__name__)


class Invites(commands.Cog):
    """Compares the use counters of the invites before and after a join."""

    def __init__(self, bot):
        """Keep the bot reference and prepare the caches."""
        self.bot = bot
        self.cache = {}
        self.locks = {}
        self.joins = {}
        self.warned = set()

    def window(self, key):
        """The time span in seconds that counts for a counter."""
        return self.bot.cfg(key[0])["invites"]["alert_minutes"] * 60

    def export_state(self):
        """Counters that should survive a restart."""
        return export_hits(self.joins, self.window)

    async def cog_load(self):
        """Load the counters of the last run."""
        self.joins = import_hits(self.bot.store.state("Invites"), self.window, lambda p: (int(p[0]), int(p[1])))

    def on(self, guild):
        """True if the module is on for a server."""
        return guild is not None and self.bot.module_on(guild.id, "invites")

    async def fetch(self, guild):
        """Return {code: (uses, inviter id, max uses)} for all invites, or None when the bot may not read them."""
        if not guild.me.guild_permissions.manage_guild:
            if guild.id not in self.warned:
                self.warned.add(guild.id)
                log.warning("invite tracking on %s needs the Manage Server permission", guild.id)
            return None
        try:
            return {i.code: (i.uses or 0, i.inviter.id if i.inviter else None, i.max_uses) for i in await guild.invites()}
        except discord.HTTPException as exc:
            log.warning("could not read the invites of %s: %s", guild.id, exc)
            return None

    @commands.Cog.listener()
    async def on_ready(self):
        """Fill the caches when the bot is connected."""
        for guild in self.bot.guilds:
            if self.on(guild):
                data = await self.fetch(guild)
                if data is not None:
                    self.cache[guild.id] = data

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Fill the cache for a new server."""
        if self.on(guild):
            data = await self.fetch(guild)
            if data is not None:
                self.cache[guild.id] = data

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        """Add a new invite to the cache."""
        if invite.guild and invite.guild.id in self.cache:
            self.cache[invite.guild.id][invite.code] = (invite.uses or 0, invite.inviter.id if invite.inviter else None, invite.max_uses)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        """Keep deleted invites in the cache until the next join, because a used-up invite disappears right after the join."""
        return None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Find the invite that was used."""
        guild = member.guild
        if member.bot or not self.on(guild):
            return
        async with self.locks.setdefault(guild.id, asyncio.Lock()):
            old = self.cache.get(guild.id)
            new = await self.fetch(guild)
            if new is None:
                return
            self.cache[guild.id] = new
            if old is None:
                return
            used = next((c for c, (n, _, _) in new.items() if n > old.get(c, (0, None, None))[0]), None)
            if used is None:
                gone = [c for c in old if c not in new]
                used = gone[0] if len(gone) == 1 else None
            inviter = (new.get(used) or old.get(used) or (0, None, None))[1] if used else None
        rec = self.bot.store.user(guild.id, member.id)
        rec["invite"], rec["invited_by"] = used, inviter
        conf = self.bot.cfg(guild.id)["invites"]
        if conf["log"]:
            e = emb("Member joined via invite", color=discord.Color.green(), user=member)
            e.add_field(name="Invite", value=f"`{used}`" if used else "unknown (vanity link or expired invite)")
            e.add_field(name="Invited by", value=f"<@{inviter}> ({inviter})" if inviter else "unknown")
            self.bot.log(guild, "members", e)
        if inviter and conf["alert_joins"]:
            await self.watch(guild, inviter, conf)

    async def watch(self, guild, inviter, conf):
        """Warn when one inviter brings many members in a short time."""
        dq = self.joins.setdefault((guild.id, inviter), deque())
        now = time.time()
        dq.append(now)
        while dq and now - dq[0] > conf["alert_minutes"] * 60:
            dq.popleft()
        if len(dq) >= conf["alert_joins"]:
            dq.clear()
            e = emb("Many joins through one inviter", color=discord.Color.orange())
            e.add_field(name="Inviter", value=f"<@{inviter}> ({inviter})")
            e.add_field(name="Joins", value=f"{conf['alert_joins']} within {conf['alert_minutes']} minutes")
            e.description = "This can be a raid or a group of alternate accounts."
            self.bot.log(guild, "security", e)

    def invited(self, guild, uid):
        """Return the ids of the current members that a user invited."""
        return [int(k) for k, rec in self.bot.store.users(guild.id).items() if rec.get("invited_by") == uid and guild.get_member(int(k))]

    @commands.hybrid_group(name="invites", fallback="who", description="Show who invited a member")
    @app_commands.describe(member="Member")
    @commands.guild_only()
    async def invites(self, ctx, member: discord.Member):
        """Show who invited a member."""
        rec = self.bot.store.users(ctx.guild.id).get(str(member.id), {})
        who = rec.get("invited_by")
        text = f"{member.mention} joined with invite `{rec.get('invite') or 'unknown'}`, invited by " + (f"<@{who}>." if who else "an unknown source.")
        await ctx.send(text, ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @invites.command(name="stats", description="Show how many members a user invited")
    async def stats(self, ctx, user: Optional[discord.Member] = None):
        """Show how many members a user invited."""
        user = user or ctx.author
        total = sum(1 for rec in self.bot.store.users(ctx.guild.id).values() if rec.get("invited_by") == user.id)
        here = len(self.invited(ctx.guild, user.id))
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "{mention} invited {total} members, {here} of them are still on the server.", mention=user.mention, total=total, here=here), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @invites.command(name="top", description="The members who invited the most people")
    async def top(self, ctx):
        """The members who invited the most people."""
        counts = {}
        for rec in self.bot.store.users(ctx.guild.id).values():
            if rec.get("invited_by"):
                counts[rec["invited_by"]] = counts.get(rec["invited_by"], 0) + 1
        best = sorted(counts.items(), key=lambda kv: -kv[1])[:10]
        lines = [f"{n}. <@{uid}>: {c} joined, {len(self.invited(ctx.guild, uid))} still here" for n, (uid, c) in enumerate(best, 1)]
        await ctx.send(embed=emb("Top inviters", "\n".join(lines) or "Nothing recorded yet."), ephemeral=True)

    @invites.command(name="setup", description="Choose what is logged and when a warning is raised")
    @app_commands.describe(log="Post every join with its invite to the member log", alert_joins="Warn after this many joins of one inviter (0 = never)", alert_minutes="Within this many minutes")
    async def setup_cmd(self, ctx, log: Optional[bool] = None, alert_joins: Optional[app_commands.Range[int, 0, 100]] = None, alert_minutes: Optional[app_commands.Range[int, 1, 1440]] = None):
        """Choose what is logged and when a warning is raised."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "You need the Manage Server permission."), ephemeral=True)
        c = self.bot.cfg(ctx.guild.id)["invites"]
        for k, v in (("log", log), ("alert_joins", alert_joins), ("alert_minutes", alert_minutes)):
            if v is not None:
                c[k] = v
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Log joins: {log}. Warning: {alert_joins} joins within {alert_minutes} minutes.", log=c['log'], alert_joins=c['alert_joins'], alert_minutes=c['alert_minutes']), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Invites(bot))
