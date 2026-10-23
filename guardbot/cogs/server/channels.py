"""Special channels: counting game, sticky messages and statistics channels."""

import asyncio
import logging
import re
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ... import i18n
from ...utils import emb

log = logging.getLogger(__name__)

COUNT_RE = re.compile(r"\s*(\d{1,15})\b")
STAT_KEYS = ("members", "humans", "bots", "boosts", "channels", "roles", "emojis")


def parse_count(text):
    """Return the number a message starts with, or None."""
    m = COUNT_RE.match(text or "")
    return int(m.group(1)) if m else None


def render_template(template, values):
    """Replace {members}, {bots} and the other placeholders. Unknown placeholders stay as they are."""
    return re.sub(r"\{(\w+)\}", lambda m: str(values.get(m.group(1), m.group(0))), template)


def stat_values(guild):
    """Collect the numbers that statistics channels can show."""
    bots = sum(1 for m in guild.members if m.bot)
    return {
        "members": guild.member_count, "humans": guild.member_count - bots, "bots": bots,
        "boosts": guild.premium_subscription_count, "channels": len(guild.channels), "roles": len(guild.roles) - 1, "emojis": len(guild.emojis),
    }


class Channels(commands.Cog):
    """Counting game, sticky messages and statistics channels."""

    cg = app_commands.Group(name="counting", description="Counting game", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    sg = app_commands.Group(name="sticky", description="Messages that stay at the bottom of a channel", default_permissions=discord.Permissions(manage_messages=True), guild_only=True)
    st = app_commands.Group(name="stats", description="Channels that show server statistics", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and the pending sticky tasks."""
        self.bot = bot
        self.pending = {}

    async def cog_load(self):
        """Start the statistics loop."""
        self.stats_loop.start()

    async def cog_unload(self):
        """Stop the statistics loop and the pending sticky tasks."""
        self.stats_loop.cancel()
        for task in self.pending.values():
            task.cancel()

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Run the counting game and refresh sticky messages."""
        if not msg.guild:
            return
        if not msg.author.bot and self.bot.module_on(msg.guild.id, "counting"):
            await self.count(msg)
        if self.bot.module_on(msg.guild.id, "sticky") and msg.author.id != self.bot.user.id:
            self.schedule_sticky(msg.channel)

    async def count(self, msg):
        """Check a message in the counting channel and continue or reset the chain."""
        c = self.bot.cfg(msg.guild.id)["counting"]
        if msg.channel.id != c["channel"]:
            return
        n = parse_count(msg.content)
        if n is None:
            if c["delete_wrong"]:
                await self.try_delete(msg)
            return
        if n == c["count"] + 1 and msg.author.id != c["last_user"]:
            c["count"], c["last_user"] = n, msg.author.id
            c["record"] = max(c["record"], n)
            await self.react(msg, "\u2705")
            return
        reason = "counted twice in a row" if n == c["count"] + 1 else f"the next number was {c['count'] + 1}"
        await self.react(msg, "\u274c")
        broke = c["count"]
        if c["reset_on_fail"]:
            c["count"], c["last_user"] = 0, None
        text = f"{msg.author.mention} broke the chain at {broke}: {reason}." + (" Start again with 1." if c["reset_on_fail"] else "")
        try:
            await msg.channel.send(text, allowed_mentions=discord.AllowedMentions(users=[msg.author]))
        except discord.HTTPException as exc:
            log.warning("could not post the counting result in %s: %s", msg.channel, exc)
        if c["delete_wrong"]:
            await self.try_delete(msg)

    async def react(self, msg, emoji):
        """Add a reaction and log if that is not possible."""
        try:
            await msg.add_reaction(emoji)
        except discord.HTTPException as exc:
            log.warning("could not react in %s: %s", msg.channel, exc)

    async def try_delete(self, msg):
        """Delete a message and log if that is not possible."""
        try:
            await msg.delete()
        except discord.NotFound:
            return
        except discord.HTTPException as exc:
            log.warning("could not delete a message in %s: %s", msg.channel, exc)

    @commands.Cog.listener()
    async def on_ready(self):
        """Bring sticky messages back to the bottom if messages were sent while the bot was offline."""
        for guild in self.bot.guilds:
            if not self.bot.module_on(guild.id, "sticky"):
                continue
            for cid, item in self.bot.cfg(guild.id)["sticky"]["items"].items():
                channel = guild.get_channel(int(cid))
                if channel is not None and channel.last_message_id != item.get("msg"):
                    self.schedule_sticky(channel)

    def schedule_sticky(self, channel):
        """Plan a refresh of the sticky message of a channel after a short quiet period."""
        gid = channel.guild.id
        if str(channel.id) not in self.bot.cfg(gid)["sticky"]["items"]:
            return
        old = self.pending.get(channel.id)
        if old:
            old.cancel()
        self.pending[channel.id] = asyncio.create_task(self.refresh_sticky(channel))

    async def refresh_sticky(self, channel):
        """Delete the old sticky message and post it again at the bottom."""
        try:
            await asyncio.sleep(4)
        except asyncio.CancelledError:
            return
        item = self.bot.cfg(channel.guild.id)["sticky"]["items"].get(str(channel.id))
        if not item:
            return
        if item.get("msg"):
            try:
                await channel.get_partial_message(item["msg"]).delete()
            except discord.NotFound:
                log.debug("the old sticky message in %s was already gone", channel)
            except discord.HTTPException as exc:
                log.warning("could not delete the old sticky message in %s: %s", channel, exc)
        try:
            sent = await channel.send(embed=emb("Pinned message", item["text"], discord.Color.light_grey()), allowed_mentions=discord.AllowedMentions.none())
            item["msg"] = sent.id
        except discord.HTTPException as exc:
            log.warning("could not post the sticky message in %s: %s", channel, exc)

    @tasks.loop(minutes=10)
    async def stats_loop(self):
        """Rename statistics channels when their numbers changed."""
        try:
            for guild in self.bot.guilds:
                if self.bot.module_on(guild.id, "stats"):
                    await self.update_stats(guild)
        except Exception:
            log.exception("statistics loop failed")

    @stats_loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected before the loop starts."""
        await self.bot.wait_until_ready()

    async def update_stats(self, guild):
        """Rename all statistics channels of a server. Returns how many were changed."""
        values = stat_values(guild)
        changed = 0
        for cid, template in list(self.bot.cfg(guild.id)["stats"]["channels"].items()):
            channel = guild.get_channel(int(cid))
            if channel is None:
                self.bot.cfg(guild.id)["stats"]["channels"].pop(cid, None)
                continue
            name = render_template(template, values)[:100]
            if channel.name == name:
                continue
            try:
                await channel.edit(name=name, reason="Statistics channel")
                changed += 1
            except discord.HTTPException as exc:
                log.warning("could not rename statistics channel %s: %s", channel, exc)
        return changed

    @cg.command(name="setup", description="Set the counting channel")
    @app_commands.describe(channel="Channel for counting", reset_on_fail="Start again at 1 when someone makes a mistake", delete_wrong="Delete wrong messages")
    async def cg_setup(self, it: discord.Interaction, channel: discord.TextChannel, reset_on_fail: Optional[bool] = None, delete_wrong: Optional[bool] = None):
        """Set the counting channel."""
        g = self.bot.cfg(it.guild_id)
        c = g["counting"]
        c["channel"] = channel.id
        if reset_on_fail is not None:
            c["reset_on_fail"] = reset_on_fail
        if delete_wrong is not None:
            c["delete_wrong"] = delete_wrong
        g["modules"]["counting"] = True
        await it.response.send_message(i18n.say(it.client, it.guild, "Counting in {mention}. The next number is {value}.", mention=channel.mention, value=c['count'] + 1), ephemeral=True)

    @cg.command(name="status", description="Show the counting game")
    async def cg_status(self, it: discord.Interaction):
        """Show the counting game."""
        c = self.bot.cfg(it.guild_id)["counting"]
        on = self.bot.module_on(it.guild_id, "counting")
        await it.response.send_message(
            i18n.say(it.client, it.guild, "Status: {value}\nChannel: {value2}\nCurrent number: {count}\nRecord: {record}\nReset on mistake: {reset_on_fail}\nDelete wrong messages: {delete_wrong}", value='on' if on else 'off', value2='<#' + str(c['channel']) + '>' if c['channel'] else 'not set', count=c['count'], record=c['record'], reset_on_fail=c['reset_on_fail'], delete_wrong=c['delete_wrong']), ephemeral=True)

    @cg.command(name="set", description="Set the current number")
    async def cg_set(self, it: discord.Interaction, number: app_commands.Range[int, 0, 1000000000]):
        """Set the current number."""
        c = self.bot.cfg(it.guild_id)["counting"]
        c["count"], c["last_user"] = number, None
        await it.response.send_message(i18n.say(it.client, it.guild, "The next number is {value}.", value=number + 1), ephemeral=True)

    @cg.command(name="off", description="Turn the counting game off")
    async def cg_off(self, it: discord.Interaction):
        """Turn the counting game off."""
        self.bot.cfg(it.guild_id)["modules"]["counting"] = False
        await it.response.send_message(i18n.say(it.client, it.guild, "Counting is off. The current number is kept."), ephemeral=True)

    @sg.command(name="set", description="Keep a message at the bottom of a channel")
    @app_commands.describe(channel="Channel", text="Message, use \\n for a new line")
    async def sg_set(self, it: discord.Interaction, channel: discord.TextChannel, text: app_commands.Range[str, 1, 1900]):
        """Keep a message at the bottom of a channel."""
        items = self.bot.cfg(it.guild_id)["sticky"]["items"]
        old = items.get(str(channel.id), {})
        items[str(channel.id)] = {"text": text.replace("\\n", "\n"), "msg": old.get("msg")}
        self.schedule_sticky(channel)
        await it.response.send_message(i18n.say(it.client, it.guild, "Sticky message set in {mention}. It appears after a few seconds.", mention=channel.mention), ephemeral=True)

    @sg.command(name="remove", description="Remove the sticky message of a channel")
    async def sg_remove(self, it: discord.Interaction, channel: discord.TextChannel):
        """Remove the sticky message of a channel."""
        item = self.bot.cfg(it.guild_id)["sticky"]["items"].pop(str(channel.id), None)
        if item is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "That channel has no sticky message."), ephemeral=True)
        if item.get("msg"):
            try:
                await channel.get_partial_message(item["msg"]).delete()
            except discord.HTTPException as exc:
                log.info("could not delete the sticky message in %s: %s", channel, exc)
        await it.response.send_message(i18n.say(it.client, it.guild, "Sticky message removed."), ephemeral=True)

    @sg.command(name="list", description="List the sticky messages")
    async def sg_list(self, it: discord.Interaction):
        """List the sticky messages."""
        items = self.bot.cfg(it.guild_id)["sticky"]["items"]
        await it.response.send_message("\n".join(f"<#{c}>: {i['text'][:80]}" for c, i in items.items()) or "No sticky messages.", ephemeral=True)

    @st.command(name="create", description="Create a statistics channel")
    @app_commands.describe(template="Name with placeholders: {members} {humans} {bots} {boosts} {channels} {roles} {emojis}", category="Category for the new channel")
    async def st_create(self, it: discord.Interaction, template: app_commands.Range[str, 1, 90], category: Optional[discord.CategoryChannel] = None):
        """Create a statistics channel."""
        await it.response.defer(ephemeral=True)
        overwrites = {it.guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)}
        try:
            channel = await it.guild.create_voice_channel(render_template(template, stat_values(it.guild))[:100], category=category, overwrites=overwrites, reason="Statistics channel")
        except discord.HTTPException as exc:
            log.warning("could not create a statistics channel: %s", exc)
            return await it.followup.send(i18n.say(it.client, it.guild, "I could not create the channel: {exc}", exc=exc))
        g = self.bot.cfg(it.guild_id)
        g["stats"]["channels"][str(channel.id)] = template
        g["modules"]["stats"] = True
        await it.followup.send(i18n.say(it.client, it.guild, "Created {mention}. It updates every 10 minutes.", mention=channel.mention))

    @st.command(name="add", description="Show statistics in the name of an existing channel")
    async def st_add(self, it: discord.Interaction, channel: discord.abc.GuildChannel, template: app_commands.Range[str, 1, 90]):
        """Show statistics in the name of an existing channel."""
        g = self.bot.cfg(it.guild_id)
        g["stats"]["channels"][str(channel.id)] = template
        g["modules"]["stats"] = True
        await it.response.send_message(i18n.say(it.client, it.guild, "{mention} will be renamed every 10 minutes. Use /server stats refresh to do it now.", mention=channel.mention), ephemeral=True)

    @st.command(name="remove", description="Stop updating a channel")
    async def st_remove(self, it: discord.Interaction, channel: discord.abc.GuildChannel):
        """Stop updating a channel."""
        removed = self.bot.cfg(it.guild_id)["stats"]["channels"].pop(str(channel.id), None)
        await it.response.send_message("Removed." if removed else "That channel is not a statistics channel.", ephemeral=True)

    @st.command(name="list", description="List the statistics channels")
    async def st_list(self, it: discord.Interaction):
        """List the statistics channels."""
        items = self.bot.cfg(it.guild_id)["stats"]["channels"]
        await it.response.send_message("\n".join(f"<#{c}>: `{t}`" for c, t in items.items()) or "No statistics channels.", ephemeral=True)

    @st.command(name="refresh", description="Update all statistics channels now")
    async def st_refresh(self, it: discord.Interaction):
        """Update all statistics channels now."""
        await it.response.defer(ephemeral=True)
        n = await self.update_stats(it.guild)
        await it.followup.send(i18n.say(it.client, it.guild, "Updated {n} channels. Discord allows two renames per channel every 10 minutes, so some may follow later.", n=n))


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Channels(bot))
