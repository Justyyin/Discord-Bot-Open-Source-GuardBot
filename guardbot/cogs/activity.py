"""Member statistics: busiest channels, messages per day and member growth. Only counts are stored, never content or names."""

import logging
from datetime import datetime, timedelta, timezone
from discord import app_commands
from discord.ext import commands

from .. import i18n
from ..utils import emb

log = logging.getLogger(__name__)

KEEP_DAYS = 120


def day_key(ts=None):
    """The date (UTC) of a timestamp as text."""
    return datetime.fromtimestamp(ts if ts is not None else datetime.now(timezone.utc).timestamp(), timezone.utc).strftime("%Y-%m-%d")


def prune(days, today=None):
    """Remove days older than the retention time."""
    limit = day_key((datetime.strptime(today or day_key(), "%Y-%m-%d").replace(tzinfo=timezone.utc) - timedelta(days=KEEP_DAYS)).timestamp())
    for key in [k for k in days if k < limit]:
        del days[key]


def last_days(days, count, today=None):
    """The day keys of the last N days up to and including today, oldest first."""
    end = datetime.strptime(today or day_key(), "%Y-%m-%d")
    return [(end - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(count - 1, -1, -1)]


def top_channels(days, keys, limit=10):
    """Sum the messages per channel over the given days and return the busiest as (channel id, count)."""
    total = {}
    for k in keys:
        for cid, n in days.get(k, {}).get("channels", {}).items():
            total[cid] = total.get(cid, 0) + n
    return sorted(total.items(), key=lambda kv: kv[1], reverse=True)[:limit]


def bar(value, top, width=20):
    """A text bar for a value relative to the largest value."""
    return "#" * (round(value / top * width) if top else 0)


class Activity(commands.Cog):
    """Counts messages per channel and joins and leaves per day."""

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    def days(self, gid):
        """Return the per-day numbers of a server."""
        return self.bot.cfg(gid)["activity"]["days"]

    def today(self, gid):
        """Return the record of today and remove old days when a new day starts."""
        days = self.days(gid)
        key = day_key()
        if key not in days:
            days[key] = {"msgs": 0, "channels": {}, "joins": 0, "leaves": 0}
            prune(days)
        return days[key]

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Count a message."""
        if msg.guild is None or msg.author.bot or not self.bot.module_on(msg.guild.id, "activity"):
            return
        d = self.today(msg.guild.id)
        d["msgs"] += 1
        parent = getattr(msg.channel, "parent_id", None) or msg.channel.id
        k = str(parent)
        d["channels"][k] = d["channels"].get(k, 0) + 1

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Count a join."""
        if self.bot.module_on(member.guild.id, "activity"):
            self.today(member.guild.id)["joins"] += 1

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Count a leave."""
        if self.bot.module_on(member.guild.id, "activity"):
            self.today(member.guild.id)["leaves"] += 1

    @commands.hybrid_group(name="activity", fallback="overview", description="Messages, busiest channels and member growth")
    @commands.guild_only()
    @app_commands.describe(days="How many days to look at (1 to 90)")
    async def activity(self, ctx, days: commands.Range[int, 1, 90] = 7):
        """Summary of the last days."""
        keys = last_days(self.days(ctx.guild.id), days)
        data = self.days(ctx.guild.id)
        msgs = sum(data.get(k, {}).get("msgs", 0) for k in keys)
        joins = sum(data.get(k, {}).get("joins", 0) for k in keys)
        leaves = sum(data.get(k, {}).get("leaves", 0) for k in keys)
        e = emb(f"Activity of the last {days} days")
        e.add_field(name="Messages", value=f"{msgs} ({msgs // days} per day)")
        e.add_field(name="Joined", value=str(joins))
        e.add_field(name="Left", value=str(leaves))
        e.add_field(name="Members", value=f"{ctx.guild.member_count} (change {joins - leaves:+d})")
        if not self.bot.module_on(ctx.guild.id, "activity"):
            e.set_footer(text="The activity module is off, so nothing is counted. Switch it on with /admin module.")
        await ctx.send(embed=e, ephemeral=True)

    @activity.command(name="channels", description="The busiest channels")
    @app_commands.describe(days="How many days to look at (1 to 90)")
    async def channels(self, ctx, days: commands.Range[int, 1, 90] = 7):
        """The busiest channels."""
        top = top_channels(self.days(ctx.guild.id), last_days(self.days(ctx.guild.id), days))
        biggest = top[0][1] if top else 0
        lines = [f"<#{cid}> {n}\n`{bar(n, biggest)}`" for cid, n in top]
        await ctx.send(embed=emb(f"Busiest channels, last {days} days", "\n".join(lines) or "Nothing counted yet."), ephemeral=True)

    @activity.command(name="growth", description="Joins and leaves per day")
    @app_commands.describe(days="How many days to look at (1 to 30)")
    async def growth(self, ctx, days: commands.Range[int, 1, 30] = 14):
        """Joins and leaves per day."""
        data = self.days(ctx.guild.id)
        rows = []
        for k in last_days(data, days):
            d = data.get(k, {})
            rows.append(f"{k[5:]}  +{d.get('joins', 0):<3} -{d.get('leaves', 0):<3} msgs {d.get('msgs', 0)}")
        await ctx.send(embed=emb(f"Growth, last {days} days", "```\n" + "\n".join(rows) + "\n```"), ephemeral=True)

    @activity.command(name="reset", description="Staff: delete all collected numbers")
    @commands.has_guild_permissions(manage_guild=True)
    async def reset(self, ctx):
        """Delete all collected numbers."""
        self.days(ctx.guild.id).clear()
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "All numbers were deleted."), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Activity(bot))
