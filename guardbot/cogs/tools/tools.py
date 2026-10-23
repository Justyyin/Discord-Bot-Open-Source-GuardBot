"""Moderator tools: purge, slowmode, channel lock, role handling, say and embed."""

import logging
import re
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ... import i18n
from ...utils import URL_RE, emb, has_image

log = logging.getLogger(__name__)

HEX_RE = re.compile(r"#?([0-9a-fA-F]{6})")
LOCK_ATTRS = ("send_messages", "send_messages_in_threads", "create_public_threads", "add_reactions")


def parse_color(text):
    """Turn #ff8800 or ff8800 into a Colour, or return None if the text is not a hex colour."""
    m = HEX_RE.fullmatch((text or "").strip())
    return discord.Colour(int(m.group(1), 16)) if m else None


def purge_check(kind, user):
    """Build the filter function for /moderation purge from a message type and an optional user."""

    def check(message):
        """True if the message should be deleted."""
        if user and message.author.id != user.id:
            return False
        if kind == "links":
            return bool(URL_RE.search(message.content))
        if kind == "images":
            return has_image(message)
        if kind == "bots":
            return message.author.bot
        if kind == "attachments":
            return bool(message.attachments)
        return True

    return check


class Tools(commands.Cog):
    """Everyday moderator tools."""

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    def audit(self, guild, title, user, fields):
        """Write a short entry about a tool use to the moderation log."""
        e = emb(title, color=discord.Color.light_grey(), user=user)
        for name, value in fields:
            e.add_field(name=name, value=str(value)[:1000] or "-", inline=len(str(value)) < 40)
        self.bot.log(guild, "moderation", e)

    @commands.hybrid_command(name="purge", description="Delete many messages at once")
    @app_commands.describe(amount="How many recent messages to check (1 to 500)", user="Only messages of this user", kind="Only one type of message")
    async def purge_cmd(self, ctx, amount: app_commands.Range[int, 1, 500], user: Optional[discord.User] = None, kind: Literal["all", "links", "images", "bots", "attachments"] = "all"):
        """Delete many messages at once."""
        await ctx.defer(ephemeral=True)
        try:
            deleted = await ctx.channel.purge(limit=amount, check=purge_check(kind, user), reason=f"Purge by {ctx.author}")
        except discord.Forbidden:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "I need the Manage Messages and Read Message History permissions in this channel."), ephemeral=True)
        except discord.HTTPException as exc:
            log.warning("purge in %s failed: %s", ctx.channel, exc)
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Discord refused the request: {exc}", exc=exc), ephemeral=True)
        watch = self.bot.get_cog("ModWatch")
        if watch:
            await watch.count(ctx.guild, ctx.author, "purge")
        self.audit(ctx.guild, "Purge", ctx.author, [("Channel", ctx.channel.mention), ("Deleted", len(deleted)), ("Filter", f"{kind}" + (f", user {user}" if user else ""))])
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Deleted {count} messages.", count=len(deleted)), ephemeral=True, delete_after=8)

    @commands.hybrid_command(name="slowmode", description="Set the slowmode of a channel")
    @app_commands.describe(seconds="Seconds between messages, 0 turns it off", channel="Channel (default: this one)")
    async def slowmode_cmd(self, ctx, seconds: app_commands.Range[int, 0, 21600], channel: Optional[discord.TextChannel] = None):
        """Set the slowmode of a channel."""
        channel = channel or ctx.channel
        try:
            await channel.edit(slowmode_delay=seconds, reason=f"Slowmode by {ctx.author}")
        except discord.HTTPException as exc:
            log.warning("slowmode of %s failed: %s", channel, exc)
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "I could not change the slowmode: {exc}", exc=exc), ephemeral=True)
        self.audit(ctx.guild, "Slowmode", ctx.author, [("Channel", channel.mention), ("Seconds", seconds)])
        await ctx.send(f"Slowmode of {channel.mention}: {seconds}s." if seconds else f"Slowmode of {channel.mention} is off.")

    @commands.hybrid_command(name="lockchannel", description="Stop everyone from writing in one channel")
    @app_commands.describe(channel="Channel (default: this one)", reason="Reason")
    async def lockchannel_cmd(self, ctx, channel: Optional[discord.TextChannel] = None, *, reason: Optional[str] = None):
        """Stop everyone from writing in one channel."""
        channel = channel or ctx.channel
        locks = self.bot.cfg(ctx.guild.id)["chanlocks"]
        if str(channel.id) in locks:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "That channel is already locked."), ephemeral=True)
        ow = channel.overwrites_for(ctx.guild.default_role)
        locks[str(channel.id)] = {a: getattr(ow, a) for a in LOCK_ATTRS}
        for a in LOCK_ATTRS:
            setattr(ow, a, False)
        try:
            await channel.set_permissions(ctx.guild.default_role, overwrite=ow, reason=reason or f"Locked by {ctx.author}")
        except discord.HTTPException as exc:
            locks.pop(str(channel.id), None)
            log.warning("locking %s failed: %s", channel, exc)
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "I could not lock the channel: {exc}", exc=exc), ephemeral=True)
        self.audit(ctx.guild, "Channel locked", ctx.author, [("Channel", channel.mention), ("Reason", reason or "-")])
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "{mention} is locked.", mention=channel.mention))

    @commands.hybrid_command(name="unlockchannel", description="Let everyone write in a locked channel again")
    @app_commands.describe(channel="Channel (default: this one)")
    async def unlockchannel_cmd(self, ctx, channel: Optional[discord.TextChannel] = None):
        """Let everyone write in a locked channel again."""
        channel = channel or ctx.channel
        locks = self.bot.cfg(ctx.guild.id)["chanlocks"]
        saved = locks.get(str(channel.id))
        if saved is None:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "That channel is not locked by me."), ephemeral=True)
        ow = channel.overwrites_for(ctx.guild.default_role)
        for a, v in saved.items():
            setattr(ow, a, v)
        try:
            await channel.set_permissions(ctx.guild.default_role, overwrite=None if ow.is_empty() else ow, reason=f"Unlocked by {ctx.author}")
        except discord.HTTPException as exc:
            log.warning("unlocking %s failed: %s", channel, exc)
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "I could not unlock the channel: {exc}", exc=exc), ephemeral=True)
        locks.pop(str(channel.id), None)
        self.audit(ctx.guild, "Channel unlocked", ctx.author, [("Channel", channel.mention)])
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "{mention} is unlocked.", mention=channel.mention))

    @commands.hybrid_group(name="role", description="Give or take a role")
    async def role_group(self, ctx):
        """Parent of /moderation role add and /moderation role remove."""
        if ctx.invoked_subcommand is None:
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Use /moderation role add or /moderation role remove."), ephemeral=True)

    def role_error(self, ctx, role):
        """Return why the moderator may not hand out this role, or None."""
        if not role.is_assignable():
            return "I cannot assign that role. It is above my highest role or managed by an integration."
        if ctx.author.id != ctx.guild.owner_id and role >= ctx.author.top_role:
            return "You cannot hand out a role that is equal to or higher than your own."
        return None

    @role_group.command(name="add", description="Give a role to a member")
    @app_commands.describe(member="Member", role="Role to give")
    async def role_add(self, ctx, member: discord.Member, role: discord.Role):
        """Give a role to a member."""
        err = self.role_error(ctx, role)
        if err:
            return await ctx.send(err, ephemeral=True)
        try:
            await member.add_roles(role, reason=f"Role added by {ctx.author}")
        except discord.HTTPException as exc:
            log.warning("adding %s to %s failed: %s", role, member, exc)
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Discord refused the request: {exc}", exc=exc), ephemeral=True)
        self.audit(ctx.guild, "Role added", ctx.author, [("Member", member.mention), ("Role", role.mention)])
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "{mention} given to {mention2}.", mention=role.mention, mention2=member.mention))

    @role_group.command(name="remove", description="Take a role from a member")
    @app_commands.describe(member="Member", role="Role to take")
    async def role_remove(self, ctx, member: discord.Member, role: discord.Role):
        """Take a role from a member."""
        err = self.role_error(ctx, role)
        if err:
            return await ctx.send(err, ephemeral=True)
        try:
            await member.remove_roles(role, reason=f"Role removed by {ctx.author}")
        except discord.HTTPException as exc:
            log.warning("removing %s from %s failed: %s", role, member, exc)
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Discord refused the request: {exc}", exc=exc), ephemeral=True)
        self.audit(ctx.guild, "Role removed", ctx.author, [("Member", member.mention), ("Role", role.mention)])
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "{mention} taken from {mention2}.", mention=role.mention, mention2=member.mention))

    @commands.hybrid_command(name="say", description="Let the bot send a message in a channel")
    @app_commands.describe(channel="Channel", message="Text, use \\n for a new line")
    async def say_cmd(self, ctx, channel: discord.TextChannel, *, message: str):
        """Let the bot send a message in a channel."""
        try:
            await channel.send(message.replace("\\n", "\n")[:2000], allowed_mentions=discord.AllowedMentions.none())
        except discord.HTTPException as exc:
            log.warning("say in %s failed: %s", channel, exc)
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "I cannot post there: {exc}", exc=exc), ephemeral=True)
        self.audit(ctx.guild, "Say used", ctx.author, [("Channel", channel.mention), ("Text", message[:500])])
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Sent."), ephemeral=True)

    @commands.hybrid_command(name="embed", description="Post an announcement embed in a channel")
    @app_commands.describe(channel="Channel", title="Title", description="Text, use \\n for a new line", color="Hex colour like #5865f2", footer="Small text at the bottom", image_url="Large image (https link)", thumbnail_url="Small image (https link)")
    async def embed_cmd(self, ctx, channel: discord.TextChannel, title: str, description: str, color: Optional[str] = None, footer: Optional[str] = None, image_url: Optional[str] = None, thumbnail_url: Optional[str] = None):
        """Post an announcement embed in a channel."""
        colour = parse_color(color) if color else discord.Colour.blurple()
        if colour is None:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "The colour must be hex like #5865f2."), ephemeral=True)
        for url in (image_url, thumbnail_url):
            if url and not url.startswith("https://"):
                return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Image links must start with https://"), ephemeral=True)
        e = discord.Embed(title=title[:256], description=description.replace("\\n", "\n")[:4000], colour=colour)
        if footer:
            e.set_footer(text=footer[:200])
        if image_url:
            e.set_image(url=image_url)
        if thumbnail_url:
            e.set_thumbnail(url=thumbnail_url)
        try:
            await channel.send(embed=e, allowed_mentions=discord.AllowedMentions.none())
        except discord.HTTPException as exc:
            log.warning("embed in %s failed: %s", channel, exc)
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "I cannot post there: {exc}", exc=exc), ephemeral=True)
        self.audit(ctx.guild, "Embed posted", ctx.author, [("Channel", channel.mention), ("Title", title)])
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Posted."), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Tools(bot))
