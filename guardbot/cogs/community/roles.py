"""Reaction roles and notification topics."""

import logging
import re
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ... import i18n
from ...utils import AdminGroup, emb, trim

log = logging.getLogger(__name__)


def ekey(e):
    """Return a stable key for an emoji: the ID of custom emojis, the character of normal ones."""
    return str(e.id) if e.id else e.name.replace("\ufe0f", "")


def parse_msg(it, text, channel):
    """Read a message link or ID and return (channel ID, message ID) or None."""
    m = re.search(r"channels/\d+/(\d+)/(\d+)", text)
    if m:
        return int(m.group(1)), int(m.group(2))
    if text.strip().isdigit():
        return (channel or it.channel).id, int(text.strip())
    return None


async def toggle_topic(interaction, topic):
    """Add or remove the role of a notification topic for the user of the interaction."""
    bot = interaction.client
    if not bot.module_on(interaction.guild_id, "notify"):
        return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Notifications are disabled."), ephemeral=True)
    t = bot.cfg(interaction.guild_id)["notify"]["topics"].get(topic)
    role = interaction.guild.get_role(t["role"]) if t else None
    if not role:
        return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This topic no longer exists."), ephemeral=True)
    try:
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role, reason="Notification topic")
            text = f"You no longer get notifications for {topic}."
        else:
            await interaction.user.add_roles(role, reason="Notification topic")
            text = f"You now get notifications for {topic}."
    except discord.HTTPException:
        text = "I could not change your roles."
    await interaction.response.send_message(text, ephemeral=True)


class NotifyToggle(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:notify:(?P<topic>[\w-]+)"):
    """Persistent button that switches a notification topic on or off."""
    def __init__(self, topic, label=None):
        """Create the button for one notification topic."""
        super().__init__(discord.ui.Button(label=label or topic, style=discord.ButtonStyle.secondary, custom_id=f"gb:notify:{topic}"))
        self.topic = topic

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls(match["topic"], item.label)

    async def callback(self, interaction):
        """Switch the notification topic of this button on or off for the user."""
        await toggle_topic(interaction, self.topic)


class Roles(commands.Cog):
    """Reaction roles and notification topics."""
    rr = app_commands.Group(name="reactionrole", description="Reaction roles", default_permissions=discord.Permissions(manage_roles=True), guild_only=True)
    nf = app_commands.Group(name="notify", description="Choose what you get notified about", guild_only=True)
    nt = AdminGroup(name="topic", description="Manage notification topics", parent=nf)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot
        bot.add_dynamic_items(NotifyToggle)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, p):
        """Runs when a message is deleted, also when it was not cached."""
        if p.guild_id:
            self.bot.cfg(p.guild_id)["reaction_roles"].pop(str(p.message_id), None)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, p):
        """Runs when a reaction is added."""
        if not p.guild_id or p.user_id == self.bot.user.id or not self.bot.module_on(p.guild_id, "reactionroles"):
            return
        entry = self.bot.cfg(p.guild_id)["reaction_roles"].get(str(p.message_id))
        item = entry["map"].get(ekey(p.emoji)) if entry else None
        if not item:
            return
        guild = self.bot.get_guild(p.guild_id)
        member = p.member or guild.get_member(p.user_id)
        role = guild.get_role(item["role"])
        if not member or member.bot or not role:
            return
        try:
            if entry["mode"] == "unique":
                others = [guild.get_role(v["role"]) for k, v in entry["map"].items() if k != ekey(p.emoji)]
                others = [r for r in others if r and r in member.roles]
                if others:
                    await member.remove_roles(*others, reason="Reaction role (unique)")
                ch = self.bot.get_channel(p.channel_id)
                if ch:
                    msg = await ch.fetch_message(p.message_id)
                    for reaction in msg.reactions:
                        if ekey(reaction.emoji) != ekey(p.emoji):
                            try:
                                await reaction.remove(member)
                            except discord.HTTPException as exc:
                                log.warning("reaction.remove failed: %s", exc)
            await member.add_roles(role, reason="Reaction role")
        except discord.HTTPException as exc:
            log.warning("bot.get_channel failed: %s", exc)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, p):
        """Runs when a reaction is removed."""
        if not p.guild_id or p.user_id == self.bot.user.id or not self.bot.module_on(p.guild_id, "reactionroles"):
            return
        entry = self.bot.cfg(p.guild_id)["reaction_roles"].get(str(p.message_id))
        item = entry["map"].get(ekey(p.emoji)) if entry else None
        if not item:
            return
        guild = self.bot.get_guild(p.guild_id)
        member, role = guild.get_member(p.user_id), guild.get_role(item["role"])
        if member and not member.bot and role and role in member.roles:
            try:
                await member.remove_roles(role, reason="Reaction role removed")
            except discord.HTTPException as exc:
                log.warning("member.remove_roles failed: %s", exc)

    @rr.command(name="add", description="Give a role when members react with an emoji")
    @app_commands.describe(message="Message link or ID", emoji="Any emoji, including custom server emojis", role="Role to give", mode="normal: any number of roles, unique: only one role from this message", channel="Channel of the message (only for plain IDs outside the current channel)")
    async def rr_add(self, it: discord.Interaction, message: str, emoji: str, role: discord.Role, mode: Optional[Literal["normal", "unique"]] = None, channel: Optional[discord.TextChannel] = None):
        """Give a role when members react with an emoji."""
        await it.response.defer(ephemeral=True)
        parsed = parse_msg(it, message, channel)
        if not parsed:
            return await it.followup.send(i18n.say(it.client, it.guild, "Provide a message link or a message ID."))
        cid, mid = parsed
        ch = it.guild.get_channel_or_thread(cid)
        if not ch:
            return await it.followup.send(i18n.say(it.client, it.guild, "Channel not found."))
        if not role.is_assignable():
            return await it.followup.send(i18n.say(it.client, it.guild, "I cannot assign that role. Move my role above it."))
        try:
            msg = await ch.fetch_message(mid)
        except discord.HTTPException:
            return await it.followup.send(i18n.say(it.client, it.guild, "Message not found."))
        pe = discord.PartialEmoji.from_str(emoji.strip())
        try:
            await msg.add_reaction(pe)
        except discord.HTTPException:
            return await it.followup.send(i18n.say(it.client, it.guild, "I cannot use that emoji."))
        entry = self.bot.cfg(it.guild_id)["reaction_roles"].setdefault(str(mid), {"channel": cid, "mode": "normal", "map": {}})
        if mode:
            entry["mode"] = mode
        entry["map"][ekey(pe)] = {"role": role.id, "emoji": str(pe)}
        await it.followup.send(i18n.say(it.client, it.guild, "{pe} on that message now gives {mention} (mode: {mode}).", pe=pe, mention=role.mention, mode=entry['mode']))

    @rr.command(name="remove", description="Remove an emoji from a reaction role message")
    async def rr_remove(self, it: discord.Interaction, message: str, emoji: str, channel: Optional[discord.TextChannel] = None):
        """Remove an emoji from a reaction role message."""
        await it.response.defer(ephemeral=True)
        parsed = parse_msg(it, message, channel)
        if not parsed:
            return await it.followup.send(i18n.say(it.client, it.guild, "Provide a message link or a message ID."))
        cid, mid = parsed
        g = self.bot.cfg(it.guild_id)
        entry = g["reaction_roles"].get(str(mid))
        pe = discord.PartialEmoji.from_str(emoji.strip())
        if not entry or entry["map"].pop(ekey(pe), None) is None:
            return await it.followup.send(i18n.say(it.client, it.guild, "No such reaction role."))
        if not entry["map"]:
            del g["reaction_roles"][str(mid)]
        ch = it.guild.get_channel_or_thread(cid)
        if ch:
            try:
                msg = await ch.fetch_message(mid)
                await msg.clear_reaction(pe)
            except discord.HTTPException as exc:
                log.warning("could not clear the reaction %s on message %s: %s", pe, mid, exc)
        await it.followup.send(i18n.say(it.client, it.guild, "Removed."))

    @rr.command(name="list", description="List all reaction roles")
    async def rr_list(self, it: discord.Interaction):
        """List all reaction roles."""
        lines = []
        for mid, entry in self.bot.cfg(it.guild_id)["reaction_roles"].items():
            link = f"https://discord.com/channels/{it.guild_id}/{entry['channel']}/{mid}"
            pairs = ", ".join(f"{v['emoji']} <@&{v['role']}>" for v in entry["map"].values())
            lines.append(f"[{mid}]({link}) ({entry['mode']}): {pairs}")
        await it.response.send_message(embed=emb("Reaction roles", trim("\n".join(lines) or "No reaction roles set.", 4000)), ephemeral=True)

    @rr.command(name="panel", description="Post a panel message you can attach reaction roles to")
    async def rr_panel(self, it: discord.Interaction, channel: discord.TextChannel, title: str, description: str):
        """Post a panel message you can attach reaction roles to."""
        try:
            msg = await channel.send(embed=discord.Embed(title=title, description=description.replace("\\n", "\n")))
        except discord.HTTPException:
            return await it.response.send_message(i18n.say(it.client, it.guild, "I cannot post in that channel."), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Panel posted: {jump_url}\nNow use /post reactionrole add with this link.", jump_url=msg.jump_url), ephemeral=True)

    @nt.command(name="add", description="Create a notification topic with a role")
    @app_commands.describe(key="Short name without spaces", role="Role that is pinged for this topic", description="What the topic is about")
    async def nt_add(self, it: discord.Interaction, key: str, role: discord.Role, description: str = ""):
        """Create a notification topic with a role."""
        if not re.fullmatch(r"[\w-]{1,30}", key):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Use only letters, numbers, - and _ (max 30)."), ephemeral=True)
        if not role.is_assignable():
            return await it.response.send_message(i18n.say(it.client, it.guild, "I cannot assign that role. Move my role above it."), ephemeral=True)
        self.bot.cfg(it.guild_id)["notify"]["topics"][key.lower()] = {"role": role.id, "desc": description}
        await it.response.send_message(i18n.say(it.client, it.guild, "Topic '{lower}' created.", lower=key.lower()), ephemeral=True)

    @nt.command(name="remove", description="Delete a notification topic")
    async def nt_remove(self, it: discord.Interaction, key: str):
        """Delete a notification topic."""
        if self.bot.cfg(it.guild_id)["notify"]["topics"].pop(key.lower(), None) is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "No such topic."), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Removed."), ephemeral=True)

    @nt.command(name="panel", description="Post a panel with a button for every topic")
    async def nt_panel(self, it: discord.Interaction, channel: discord.TextChannel, title: str = "Notifications"):
        """Post a panel with a button for every topic."""
        topics = self.bot.cfg(it.guild_id)["notify"]["topics"]
        if not topics:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Create a topic first."), ephemeral=True)
        view = discord.ui.View(timeout=None)
        lines = []
        for key, t in list(topics.items())[:25]:
            view.add_item(NotifyToggle(key, key))
            lines.append(f"{key}: {t['desc'] or '-'}")
        await channel.send(embed=emb(title, "Press a button to turn notifications for a topic on or off.\n\n" + "\n".join(lines)), view=view)
        await it.response.send_message(i18n.say(it.client, it.guild, "Panel posted."), ephemeral=True)

    @nf.command(name="subscribe", description="Get notifications for a topic")
    async def nf_sub(self, it: discord.Interaction, topic: str):
        """Get notifications for a topic."""
        t = self.bot.cfg(it.guild_id)["notify"]["topics"].get(topic.lower())
        role = it.guild.get_role(t["role"]) if t else None
        if not role:
            return await it.response.send_message(i18n.say(it.client, it.guild, "No such topic. Use /notify list."), ephemeral=True)
        await it.user.add_roles(role, reason="Notification topic")
        await it.response.send_message(i18n.say(it.client, it.guild, "Subscribed to {lower}.", lower=topic.lower()), ephemeral=True)

    @nf.command(name="unsubscribe", description="Stop notifications for a topic")
    async def nf_unsub(self, it: discord.Interaction, topic: str):
        """Stop notifications for a topic."""
        t = self.bot.cfg(it.guild_id)["notify"]["topics"].get(topic.lower())
        role = it.guild.get_role(t["role"]) if t else None
        if not role:
            return await it.response.send_message(i18n.say(it.client, it.guild, "No such topic. Use /notify list."), ephemeral=True)
        await it.user.remove_roles(role, reason="Notification topic")
        await it.response.send_message(i18n.say(it.client, it.guild, "Unsubscribed from {lower}.", lower=topic.lower()), ephemeral=True)

    @nf.command(name="list", description="Show all topics")
    async def nf_list(self, it: discord.Interaction):
        """Show all topics."""
        topics = self.bot.cfg(it.guild_id)["notify"]["topics"]
        mine = {r.id for r in it.user.roles}
        lines = [f"{k} ({'subscribed' if t['role'] in mine else 'not subscribed'}): {t['desc'] or '-'}" for k, t in topics.items()]
        await it.response.send_message("\n".join(lines) or "No topics yet.", ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Roles(bot))
