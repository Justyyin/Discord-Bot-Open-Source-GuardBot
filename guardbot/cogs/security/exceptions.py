"""Exceptions per channel and role for AutoMod rules and for the anti-scam check."""

import logging
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ...utils import require
from ... import i18n

log = logging.getLogger(__name__)

RULES = ("flood", "caps", "mentions", "invites", "phishing", "pii", "doxxing", "threats", "shortlinks", "newlinks", "words", "blocklist", "channelrule")
KEYS = ("automod", "antiscam") + RULES
RULE_OF = {"channel rule": "channelrule"}


def excepted(items, key, channel_ids, role_ids):
    """True if a channel (or its category or thread parent) or a role is excepted for a key, or for all of AutoMod."""
    channel_ids, role_ids = set(channel_ids), set(role_ids)
    names = [key]
    if key in RULES:
        names.append("automod")
    for name in names:
        item = items.get(name)
        if item and (channel_ids & set(item["channels"]) or role_ids & set(item["roles"])):
            return True
    return False


def context_of(message):
    """The IDs of the channel, its category and thread parent, and of the roles of the author."""
    ch = message.channel
    channels = {ch.id, getattr(ch, "category_id", None) or 0, getattr(ch, "parent_id", None) or 0}
    channels.add(getattr(getattr(ch, "parent", None), "category_id", None) or 0)
    return channels - {0}, {r.id for r in getattr(message.author, "roles", [])}


class Exceptions(commands.Cog):
    """Exceptions per channel and role."""

    ex = app_commands.Group(name="exceptions", description="Channels and roles that AutoMod rules or the anti-scam check ignore", guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    def items(self, gid):
        """The exceptions of a server."""
        return self.bot.cfg(gid)["exceptions"]["items"]

    def check(self, message, key):
        """True if a message is excepted for a key. Used by AutoMod and anti-scam."""
        if not message.guild or not self.bot.module_on(message.guild.id, "exceptions"):
            return False
        channels, roles = context_of(message)
        return excepted(self.items(message.guild.id), RULE_OF.get(key, key), channels, roles)

    @ex.command(name="add", description="Ignore a channel, a category or a role for a rule")
    @app_commands.describe(rule="automod = all rules, antiscam, or one rule", channel="Channel or category", role="Role")
    async def add(self, it: discord.Interaction, rule: Literal[KEYS], channel: Optional[discord.abc.GuildChannel] = None, role: Optional[discord.Role] = None):
        """Ignore a channel, a category or a role for a rule."""
        if not await require(it):
            return
        if channel is None and role is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Choose a channel or a role."), ephemeral=True)
        item = self.items(it.guild_id).setdefault(rule, {"channels": [], "roles": []})
        if channel is not None and channel.id not in item["channels"]:
            item["channels"].append(channel.id)
        if role is not None and role.id not in item["roles"]:
            item["roles"].append(role.id)
        await it.response.send_message(i18n.say(it.client, it.guild, "Saved. {rule} now ignores {count} channels and {count2} roles.", rule=rule, count=len(item['channels']), count2=len(item['roles'])), ephemeral=True)

    @ex.command(name="remove", description="End an exception")
    async def remove(self, it: discord.Interaction, rule: Literal[KEYS], channel: Optional[discord.abc.GuildChannel] = None, role: Optional[discord.Role] = None):
        """End an exception."""
        if not await require(it):
            return
        items = self.items(it.guild_id)
        item = items.get(rule)
        if not item:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There are no exceptions for that rule."), ephemeral=True)
        if channel is not None and channel.id in item["channels"]:
            item["channels"].remove(channel.id)
        if role is not None and role.id in item["roles"]:
            item["roles"].remove(role.id)
        if not item["channels"] and not item["roles"]:
            items.pop(rule, None)
        await it.response.send_message(i18n.say(it.client, it.guild, "Saved."), ephemeral=True)

    @ex.command(name="list", description="Show all exceptions")
    async def list_cmd(self, it: discord.Interaction):
        """Show all exceptions."""
        lines = [f"**{k}**: {' '.join('<#' + str(c) + '>' for c in v['channels'])} {' '.join('<@&' + str(r) + '>' for r in v['roles'])}" for k, v in self.items(it.guild_id).items()]
        await it.response.send_message("\n".join(lines) or "No exceptions. AutoMod also has its own list of exempt roles and channels, see /automod status.", ephemeral=True, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Exceptions(bot))
