"""Custom commands (tags) that anyone can call, and autoresponders that answer matching messages."""

import logging
import re
import time
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from .. import i18n
from ..utils import emb
from .welcome import fmt

log = logging.getLogger(__name__)

NAME_RE = re.compile(r"[\w-]{1,30}")
MODES = ("contains", "word", "exact", "startswith")
MAX_TAGS = 100
MAX_RESPONDERS = 50


def match_trigger(text, trigger, mode):
    """True if a message text matches an autoresponder trigger in the given mode."""
    t, g = text.lower().strip(), trigger.lower().strip()
    if not g:
        return False
    if mode == "exact":
        return t == g
    if mode == "startswith":
        return t.startswith(g)
    if mode == "word":
        return re.search(r"(?<!\w)" + re.escape(g) + r"(?!\w)", t) is not None
    return g in t


class Tags(commands.Cog):
    """Tags, custom commands and autoresponders."""

    tag = app_commands.Group(name="tag", description="Custom commands everyone can use", guild_only=True)
    ar = app_commands.Group(name="autoresponder", description="Automatic answers to messages", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and the cooldown table."""
        self.bot = bot
        self.cd = {}

    def conf(self, gid):
        """Return the tag settings of a server."""
        return self.bot.cfg(gid)["tags"]["items"]

    def can_manage(self, member):
        """True if the member may create, change and delete tags."""
        perms = member.guild_permissions
        return perms.manage_messages or perms.manage_guild

    def name_error(self, name):
        """Return why a tag name cannot be used, or None."""
        if not NAME_RE.fullmatch(name):
            return "Use only letters, numbers, - and _ (max 30)."
        if self.bot.get_command(name) or self.bot.tree.get_command(name):
            return "That name is already used by a bot command."
        return None

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Answer custom commands that start with the prefix, and autoresponders for other messages."""
        if msg.author.bot or not msg.guild or not msg.content:
            return
        gid = msg.guild.id
        prefix = self.bot.prefix_for(gid)
        if msg.content.startswith(prefix):
            if not self.bot.module_on(gid, "tags"):
                return
            words = msg.content[len(prefix):].split(None, 1)
            name = words[0].lower() if words else ""
            tag = self.conf(gid).get(name)
            if tag and not self.bot.get_command(name) and name not in self.bot.cfg(gid)["aliases"]:
                await self.send_tag(msg.channel, msg.author, msg.guild, name, tag)
            return
        if self.bot.module_on(gid, "autoresponder"):
            await self.respond(msg)

    async def send_tag(self, channel, user, guild, name, tag):
        """Post a tag, with a short cooldown per user so it cannot be spammed."""
        key = (guild.id, "tag", name, user.id)
        now = time.time()
        if now - self.cd.get(key, 0) < 3:
            return
        self.cd[key] = now
        tag["uses"] = tag.get("uses", 0) + 1
        try:
            await channel.send(fmt(tag["text"], user, guild), allowed_mentions=discord.AllowedMentions(users=[user]))
        except discord.HTTPException as exc:
            log.warning("could not send tag %s in %s: %s", name, channel, exc)

    async def respond(self, msg):
        """Send the response of the first autoresponder that matches and is not on cooldown."""
        ar = self.bot.cfg(msg.guild.id)["autoresponder"]
        now = time.time()
        for item in ar["items"]:
            if not match_trigger(msg.content, item["trigger"], item["mode"]):
                continue
            key = (msg.guild.id, "ar", item["id"], msg.channel.id)
            if now - self.cd.get(key, 0) < item["cooldown"]:
                continue
            self.cd[key] = now
            try:
                await msg.reply(fmt(item["response"], msg.author, msg.guild), mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            except discord.HTTPException as exc:
                log.warning("autoresponder %s could not reply in %s: %s", item["id"], msg.channel, exc)
            return

    @tag.command(name="show", description="Post a tag")
    @app_commands.describe(name="Tag name")
    async def tag_show(self, it: discord.Interaction, name: str):
        """Post a tag."""
        tag = self.conf(it.guild_id).get(name.lower())
        if not tag:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no tag with that name. Use /tag list."), ephemeral=True)
        tag["uses"] = tag.get("uses", 0) + 1
        await it.response.send_message(fmt(tag["text"], it.user, it.guild), allowed_mentions=discord.AllowedMentions(users=[it.user]))

    @tag.command(name="list", description="List all tags")
    async def tag_list(self, it: discord.Interaction):
        """List all tags."""
        names = sorted(self.conf(it.guild_id))
        prefix = self.bot.prefix_for(it.guild_id)
        await it.response.send_message(embed=emb("Tags", " ".join(f"`{n}`" for n in names) or "No tags yet.", footer=f"Use /tag show or {prefix}name"), ephemeral=True)

    @tag.command(name="info", description="Show who made a tag and how often it was used")
    async def tag_info(self, it: discord.Interaction, name: str):
        """Show who made a tag and how often it was used."""
        tag = self.conf(it.guild_id).get(name.lower())
        if not tag:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no tag with that name."), ephemeral=True)
        await it.response.send_message(f"`{name.lower()}` by <@{tag['author']}>, used {tag.get('uses', 0)} times, created <t:{tag['created']}:R>", ephemeral=True)

    @tag.command(name="create", description="Create a tag")
    @app_commands.describe(name="Short name without spaces", text="What the tag says. Supports {user}, {name}, {server}, {count}")
    async def tag_create(self, it: discord.Interaction, name: str, text: app_commands.Range[str, 1, 1900]):
        """Create a tag."""
        if not self.can_manage(it.user):
            return await it.response.send_message(i18n.say(it.client, it.guild, "You need the Manage Messages permission to create tags."), ephemeral=True)
        name = name.lower()
        err = self.name_error(name)
        tags = self.conf(it.guild_id)
        if err or name in tags:
            return await it.response.send_message(err or "That tag exists already. Use /tag edit.", ephemeral=True)
        if len(tags) >= MAX_TAGS:
            return await it.response.send_message(f"A server can have {MAX_TAGS} tags at most.", ephemeral=True)
        tags[name] = {"text": text.replace("\\n", "\n"), "author": it.user.id, "uses": 0, "created": int(time.time())}
        await it.response.send_message(f"Tag `{name}` created. Members can use `/tag show {name}` or `{self.bot.prefix_for(it.guild_id)}{name}`.", ephemeral=True)

    @tag.command(name="edit", description="Change the text of a tag")
    async def tag_edit(self, it: discord.Interaction, name: str, text: app_commands.Range[str, 1, 1900]):
        """Change the text of a tag."""
        if not self.can_manage(it.user):
            return await it.response.send_message(i18n.say(it.client, it.guild, "You need the Manage Messages permission to edit tags."), ephemeral=True)
        tag = self.conf(it.guild_id).get(name.lower())
        if not tag:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no tag with that name."), ephemeral=True)
        tag["text"] = text.replace("\\n", "\n")
        await it.response.send_message(i18n.say(it.client, it.guild, "Tag updated."), ephemeral=True)

    @tag.command(name="delete", description="Delete a tag")
    async def tag_delete(self, it: discord.Interaction, name: str):
        """Delete a tag."""
        if not self.can_manage(it.user):
            return await it.response.send_message(i18n.say(it.client, it.guild, "You need the Manage Messages permission to delete tags."), ephemeral=True)
        if self.conf(it.guild_id).pop(name.lower(), None) is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no tag with that name."), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Tag deleted."), ephemeral=True)

    @ar.command(name="add", description="Answer messages that match a trigger")
    @app_commands.describe(trigger="Text to look for", response="Answer, supports {user}, {name}, {server}, {count}", mode="contains, word (whole word), exact or startswith", cooldown="Seconds before it answers again in the same channel")
    async def ar_add(self, it: discord.Interaction, trigger: app_commands.Range[str, 2, 100], response: app_commands.Range[str, 1, 1900], mode: Literal[MODES] = "contains", cooldown: app_commands.Range[int, 0, 3600] = 10):
        """Answer messages that match a trigger."""
        ar = self.bot.cfg(it.guild_id)["autoresponder"]
        if len(ar["items"]) >= MAX_RESPONDERS:
            return await it.response.send_message(f"A server can have {MAX_RESPONDERS} autoresponders at most.", ephemeral=True)
        item = {"id": ar["next"], "trigger": trigger, "response": response.replace("\\n", "\n"), "mode": mode, "cooldown": cooldown}
        ar["next"] += 1
        ar["items"].append(item)
        await it.response.send_message(f"Autoresponder #{item['id']} created.", ephemeral=True)

    @ar.command(name="remove", description="Delete an autoresponder")
    async def ar_remove(self, it: discord.Interaction, id: int):
        """Delete an autoresponder."""
        ar = self.bot.cfg(it.guild_id)["autoresponder"]
        before = len(ar["items"])
        ar["items"] = [i for i in ar["items"] if i["id"] != id]
        await it.response.send_message("Deleted." if len(ar["items"]) < before else "No autoresponder with that ID.", ephemeral=True)

    @ar.command(name="list", description="List all autoresponders")
    async def ar_list(self, it: discord.Interaction):
        """List all autoresponders."""
        items = self.bot.cfg(it.guild_id)["autoresponder"]["items"]
        lines = [f"#{i['id']} {i['mode']} `{i['trigger']}` -> {i['response'][:60]} (cooldown {i['cooldown']}s)" for i in items]
        await it.response.send_message("\n".join(lines) or "No autoresponders yet.", ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Tags(bot))
