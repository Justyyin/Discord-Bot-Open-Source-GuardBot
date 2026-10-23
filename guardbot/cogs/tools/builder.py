"""Message builder: post, edit, preview and copy messages with embeds and link buttons from JSON, a file or a link."""

import io
import json
import logging
import re
from typing import Literal, Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from ... import builder, i18n
from ...linkcheck import make_session, url_problem
from ...utils import emb

log = logging.getLogger(__name__)

MAX_SOURCE = 100_000
MESSAGE_LINK = re.compile(r"https?://(?:\w+\.)?discord(?:app)?\.com/channels/(\d+)/(\d+)/(\d+)")


class Builder(commands.Cog):
    """Post and edit messages with embeds and link buttons."""
    mg = app_commands.Group(name="message", description="Post messages with embeds and link buttons from JSON", default_permissions=discord.Permissions(manage_messages=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and an HTTP session for JSON links."""
        self.bot = bot
        self.http = None

    async def cog_unload(self):
        """Close the HTTP session."""
        if self.http is not None:
            await self.http.close()

    async def read_source(self, text, file, url):
        """Get the JSON from exactly one of text, file or link. Returns the decoded data. Raises BuildError."""
        given = [x for x in (text, file, url) if x]
        if len(given) != 1:
            raise builder.BuildError("give exactly one of json, file or url")
        if text:
            raw = text
        elif file:
            if file.size > MAX_SOURCE:
                raise builder.BuildError("the file is larger than 100 KB")
            raw = (await file.read()).decode("utf-8", "replace")
        else:
            problem = url_problem(url)
            if problem or not url.startswith("https://"):
                raise builder.BuildError(problem or "only https links are supported")
            if self.http is None:
                self.http = make_session()
            try:
                async with self.http.get(url, allow_redirects=False, timeout=aiohttp.ClientTimeout(total=8)) as r:
                    if r.status != 200:
                        raise builder.BuildError(f"the link answered with status {r.status}, it must point straight to the JSON (no redirect)")
                    raw = (await r.content.read(MAX_SOURCE + 1)).decode("utf-8", "replace")
            except (aiohttp.ClientError, OSError, TimeoutError) as exc:
                raise builder.BuildError(f"the link could not be read: {exc}")
            if len(raw) > MAX_SOURCE:
                raise builder.BuildError("the JSON is larger than 100 KB")
        try:
            return json.loads(raw)
        except ValueError as exc:
            raise builder.BuildError(f"this is not valid JSON: {exc}")

    async def fail(self, it, exc):
        """Tell the user why a message could not be built."""
        text = i18n.say(self.bot, it.guild, "The message cannot be built: {reason}", reason=str(exc))
        if it.response.is_done():
            return await it.followup.send(text, ephemeral=True)
        await it.response.send_message(text, ephemeral=True)

    def locate(self, it, link):
        """Find the channel and the message id from a message link of this server. Returns (channel, message id) or None."""
        m = MESSAGE_LINK.search(link or "")
        if not m or int(m.group(1)) != it.guild_id:
            return None
        channel = it.guild.get_channel_or_thread(int(m.group(2)))
        if channel is None or not hasattr(channel, "fetch_message"):
            return None
        perms = channel.permissions_for(it.user)
        if not perms.view_channel or not perms.read_message_history:
            return None
        return channel, int(m.group(3))

    @mg.command(name="send", description="Post a message with embeds and link buttons")
    @app_commands.describe(channel="Where to post", json="The JSON of the message", file="A .json file", url="A https link straight to the JSON")
    async def send(self, it: discord.Interaction, channel: discord.TextChannel, json: Optional[str] = None, file: Optional[discord.Attachment] = None, url: Optional[str] = None):
        """Post a message with embeds and link buttons."""
        await it.response.defer(ephemeral=True)
        try:
            content, embeds, view, warnings = builder.parse(await self.read_source(json, file, url))
        except builder.BuildError as exc:
            return await self.fail(it, exc)
        perms = channel.permissions_for(it.user)
        if not perms.send_messages or (embeds and not perms.embed_links):
            return await it.followup.send(i18n.say(self.bot, it.guild, "You cannot post in that channel."), ephemeral=True)
        try:
            sent = await channel.send(content=content, embeds=embeds, view=view, allowed_mentions=discord.AllowedMentions.none())
        except discord.HTTPException as exc:
            log.warning("message send in %s failed: %s", channel, exc)
            return await it.followup.send(i18n.say(it.client, it.guild, "I cannot post there: {exc}", exc=exc), ephemeral=True)
        self.audit(it, "Message posted", [("Channel", channel.mention), ("Message", sent.jump_url)])
        await it.followup.send(i18n.say(self.bot, it.guild, "Posted.") + " " + sent.jump_url + ("\n" + "\n".join(warnings[:3]) if warnings else ""), ephemeral=True)

    @mg.command(name="edit", description="Change a message that the bot posted")
    @app_commands.describe(message="Link of the message", json="The new JSON of the message", file="A .json file", url="A https link straight to the JSON")
    async def edit(self, it: discord.Interaction, message: str, json: Optional[str] = None, file: Optional[discord.Attachment] = None, url: Optional[str] = None):
        """Change a message that the bot posted."""
        await it.response.defer(ephemeral=True)
        found = self.locate(it, message)
        if found is None:
            return await it.followup.send(i18n.say(self.bot, it.guild, "Message not found."), ephemeral=True)
        try:
            content, embeds, view, warnings = builder.parse(await self.read_source(json, file, url))
            target = await found[0].fetch_message(found[1])
        except builder.BuildError as exc:
            return await self.fail(it, exc)
        except discord.HTTPException:
            return await it.followup.send(i18n.say(self.bot, it.guild, "Message not found."), ephemeral=True)
        if target.author.id != self.bot.user.id:
            return await it.followup.send(i18n.say(self.bot, it.guild, "I can only change my own messages."), ephemeral=True)
        try:
            await target.edit(content=content, embeds=embeds, view=view, allowed_mentions=discord.AllowedMentions.none())
        except discord.HTTPException as exc:
            return await it.followup.send(i18n.say(it.client, it.guild, "I cannot change it: {exc}", exc=exc), ephemeral=True)
        self.audit(it, "Message changed", [("Message", target.jump_url)])
        await it.followup.send(i18n.say(self.bot, it.guild, "Saved.") + ("\n" + "\n".join(warnings[:3]) if warnings else ""), ephemeral=True)

    @mg.command(name="preview", description="Show how a message would look, only to you")
    @app_commands.describe(json="The JSON of the message", file="A .json file", url="A https link straight to the JSON")
    async def preview(self, it: discord.Interaction, json: Optional[str] = None, file: Optional[discord.Attachment] = None, url: Optional[str] = None):
        """Show how a message would look, only to you."""
        await it.response.defer(ephemeral=True)
        try:
            content, embeds, view, warnings = builder.parse(await self.read_source(json, file, url))
        except builder.BuildError as exc:
            return await self.fail(it, exc)
        await it.followup.send(content=content or ("\n".join(warnings[:3]) or None), embeds=embeds, view=view, ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @mg.command(name="copy", description="Export a message of this server as JSON")
    @app_commands.describe(message="Link of the message", kind="What to export")
    async def copy(self, it: discord.Interaction, message: str, kind: Literal["json"] = "json"):
        """Export a message of this server as JSON, for editing here or in an embed generator."""
        await it.response.defer(ephemeral=True)
        found = self.locate(it, message)
        if found is None:
            return await it.followup.send(i18n.say(self.bot, it.guild, "Message not found."), ephemeral=True)
        try:
            target = await found[0].fetch_message(found[1])
        except discord.HTTPException:
            return await it.followup.send(i18n.say(self.bot, it.guild, "Message not found."), ephemeral=True)
        data = builder.export(target)
        if not data:
            return await it.followup.send(i18n.say(self.bot, it.guild, "That message has nothing to export."), ephemeral=True)
        raw = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        await it.followup.send(file=discord.File(io.BytesIO(raw), filename=f"message-{target.id}.json"), ephemeral=True)

    def audit(self, it, title, fields):
        """Write the use of the builder to the moderation log."""
        e = emb(title, color=discord.Color.light_grey(), user=it.user)
        for name, value in fields:
            e.add_field(name=name, value=str(value)[:1000] or "-", inline=False)
        self.bot.log(it.guild, "moderation", e)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Builder(bot))
