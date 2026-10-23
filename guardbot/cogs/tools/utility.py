"""Reminders and AFK status."""

import logging
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ... import i18n
from ...utils import emb, fmt_duration, parse_duration

log = logging.getLogger(__name__)

MIN_SECONDS = 5
MAX_SECONDS = 365 * 86400
MAX_PER_USER = 10


class Utility(commands.Cog):
    """Small helpers for members."""

    gate = {"on_message": "utility"}

    def __init__(self, bot):
        """Keep the bot reference and the AFK notice cooldowns."""
        self.bot = bot
        self.notified = {}

    async def cog_load(self):
        """Start the reminder loop."""
        self.remind_loop.start()

    async def cog_unload(self):
        """Stop the reminder loop."""
        self.remind_loop.cancel()

    async def deliver(self, guild, item):
        """Send a due reminder to its channel, or by direct message if the channel is gone."""
        channel = guild.get_channel_or_thread(item["channel"])
        text = f"<@{item['user']}> Reminder: {item['text']}"
        if channel is not None:
            try:
                await channel.send(text, allowed_mentions=discord.AllowedMentions(users=[discord.Object(item["user"])]))
                return
            except discord.HTTPException as exc:
                log.info("reminder %s could not be posted in %s: %s", item["id"], channel, exc)
        member = guild.get_member(item["user"])
        if member is None:
            return
        try:
            await member.send(f"Reminder from {guild.name}: {item['text']}")
        except discord.Forbidden:
            log.info("cannot DM %s, direct messages are closed", member)
        except discord.HTTPException as exc:
            log.warning("reminder DM to %s failed: %s", member, exc)

    @tasks.loop(seconds=15)
    async def remind_loop(self):
        """Deliver reminders whose time has come."""
        now = time.time()
        try:
            for guild in self.bot.guilds:
                rm = self.bot.cfg(guild.id)["reminders"]
                due = [i for i in rm["items"] if i["end"] <= now]
                if not due:
                    continue
                rm["items"] = [i for i in rm["items"] if i["end"] > now]
                for item in due:
                    await self.deliver(guild, item)
        except Exception:
            log.exception("reminder loop failed")

    @remind_loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected before the loop starts."""
        await self.bot.wait_until_ready()

    @commands.hybrid_group(name="remind", fallback="set", description="Remind you of something later")
    @app_commands.describe(duration="When, for example 30m, 2h, 1d or 2w", text="What to remind you of")
    async def remind_cmd(self, ctx, duration: str, *, text: str):
        """Remind you of something later."""
        secs = parse_duration(duration)
        if not secs or secs < MIN_SECONDS or secs > MAX_SECONDS:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Invalid time. Use values like 30m, 2h, 1d or 2w, between 5 seconds and one year."), ephemeral=True)
        rm = self.bot.cfg(ctx.guild.id)["reminders"]
        if sum(1 for i in rm["items"] if i["user"] == ctx.author.id) >= MAX_PER_USER:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "You can have {MAX_PER_USER} reminders at once. Use /community remind cancel.", MAX_PER_USER=MAX_PER_USER), ephemeral=True)
        item = {"id": rm["next"], "user": ctx.author.id, "channel": ctx.channel.id, "end": int(time.time()) + secs, "text": text[:500]}
        rm["next"] += 1
        rm["items"].append(item)
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Reminder #{id} set. I will remind you <t:{end}:R>.", id=item['id'], end=item['end']), ephemeral=True)

    @remind_cmd.command(name="list", description="Show your reminders")
    async def remind_list(self, ctx):
        """Show your reminders."""
        mine = [i for i in self.bot.cfg(ctx.guild.id)["reminders"]["items"] if i["user"] == ctx.author.id]
        lines = [f"#{i['id']} <t:{i['end']}:R> {i['text'][:80]}" for i in mine]
        await ctx.send("\n".join(lines) or "You have no reminders.", ephemeral=True)

    @remind_cmd.command(name="cancel", description="Delete one of your reminders")
    @app_commands.describe(id="Reminder number from /community remind list")
    async def remind_cancel(self, ctx, id: int):
        """Delete one of your reminders."""
        rm = self.bot.cfg(ctx.guild.id)["reminders"]
        before = len(rm["items"])
        rm["items"] = [i for i in rm["items"] if not (i["id"] == id and i["user"] == ctx.author.id)]
        await ctx.send("Reminder deleted." if len(rm["items"]) < before else "You have no reminder with that number.", ephemeral=True)

    @commands.hybrid_command(name="afk", description="Show others that you are away")
    @app_commands.describe(reason="Why you are away")
    async def afk_cmd(self, ctx, *, reason: Optional[str] = None):
        """Show others that you are away."""
        rec = self.bot.store.user(ctx.guild.id, ctx.author.id)
        rec["afk"] = {"reason": (reason or "AFK")[:200], "since": int(time.time())}
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "{mention} is AFK now: {reason}", mention=ctx.author.mention, reason=rec['afk']['reason']), allowed_mentions=discord.AllowedMentions.none())

    @commands.Cog.listener()
    async def on_message(self, msg):
        """End the AFK status of the author and tell others who mention someone who is AFK."""
        if msg.author.bot or not msg.guild or not self.bot.module_on(msg.guild.id, "utility"):
            return
        users = self.bot.store.users(msg.guild.id)
        prefix = self.bot.prefix_for(msg.guild.id)
        mine = users.get(str(msg.author.id))
        if mine and mine.get("afk") and not msg.content.lower().startswith(prefix + "afk"):
            data = self.bot.store.user(msg.guild.id, msg.author.id).pop("afk")
            try:
                await msg.channel.send(
                    f"Welcome back {msg.author.mention}, your AFK status is removed. You were away for {fmt_duration(time.time() - data['since'])}.",
                    delete_after=10, allowed_mentions=discord.AllowedMentions(users=[msg.author]))
            except discord.HTTPException as exc:
                log.warning("could not announce the end of AFK in %s: %s", msg.channel, exc)
        now = time.time()
        for member in msg.mentions[:3]:
            rec = users.get(str(member.id))
            if member.bot or member.id == msg.author.id or not rec or not rec.get("afk"):
                continue
            key = (msg.channel.id, member.id)
            if now - self.notified.get(key, 0) < 60:
                continue
            self.notified[key] = now
            afk = rec["afk"]
            try:
                await msg.reply(embed=emb(f"{member.display_name} is AFK", f"{afk['reason']}\nSince <t:{afk['since']}:R>", discord.Color.light_grey()), mention_author=False, delete_after=20)
            except discord.HTTPException as exc:
                log.warning("could not post the AFK notice in %s: %s", msg.channel, exc)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Utility(bot))
