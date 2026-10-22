"""Mod-mail: members contact the staff privately through the server. The bot never reads direct messages."""

import asyncio
import io
import logging
import re
import time

import discord
from discord import app_commands
from discord.ext import commands

from .. import i18n
from ..utils import AdminGroup, emb, transcript

log = logging.getLogger(__name__)

STAFF_PERMS = dict(view_channel=True, send_messages=True, attach_files=True, read_message_history=True, embed_links=True, manage_messages=True)


class ModmailModal(discord.ui.Modal, title="Contact the staff"):
    """Form with a subject and a message."""

    subject = discord.ui.TextInput(label="Subject", max_length=80)
    text = discord.ui.TextInput(label="Your message", style=discord.TextStyle.paragraph, max_length=1500)

    async def on_submit(self, interaction):
        """Hand the form to the mod-mail cog."""
        await interaction.client.get_cog("Modmail").submit(interaction, str(self.subject.value), str(self.text.value))


class ModmailOpen(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:modmail"):
    """Persistent button that opens the contact form."""

    def __init__(self):
        """Create the button."""
        super().__init__(discord.ui.Button(label="Contact the staff", style=discord.ButtonStyle.primary, custom_id="gb:modmail"))

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls()

    async def callback(self, interaction):
        """Show the contact form."""
        await interaction.response.send_modal(ModmailModal())


class Modmail(commands.Cog):
    """Private conversations between members and the staff."""

    mm = app_commands.Group(name="modmail", description="Talk to the staff privately", guild_only=True)
    ms = AdminGroup(name="setup", description="Configure mod-mail", parent=mm)

    def __init__(self, bot):
        """Keep the bot reference and register the persistent button."""
        self.bot = bot
        self.last = {}
        bot.add_dynamic_items(ModmailOpen)

    def conf(self, gid):
        """Return the mod-mail settings of a server."""
        return self.bot.cfg(gid)["modmail"]

    def open_channel_of(self, guild, user_id):
        """Return the open mod-mail channel of a member, or None."""
        for cid, data in self.conf(guild.id)["open"].items():
            if data["user"] == user_id:
                return guild.get_channel(int(cid))
        return None

    async def submit(self, interaction, subject, text):
        """Create a mod-mail channel for the member or add the message to the open one."""
        guild, member, c = interaction.guild, interaction.user, self.conf(interaction.guild_id)
        if not self.bot.module_on(guild.id, "modmail"):
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Mod-mail is turned off."), ephemeral=True)
        if member.id in c["blocked"]:
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "You cannot use mod-mail on this server."), ephemeral=True)
        if time.time() - self.last.get(member.id, 0) < 5:
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Please wait a few seconds."), ephemeral=True)
        self.last[member.id] = time.time()
        category = guild.get_channel(c["category"]) if c["category"] else None
        staff = guild.get_role(c["staff_role"]) if c["staff_role"] else None
        if not isinstance(category, discord.CategoryChannel) or staff is None:
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Mod-mail is not set up yet. Ask an administrator."), ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        channel = self.open_channel_of(guild, member.id)
        if channel is None:
            name = re.sub(r"[^a-z0-9-]", "", member.name.lower())[:40] or "member"
            overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False), staff: discord.PermissionOverwrite(**STAFF_PERMS), guild.me: discord.PermissionOverwrite(**STAFF_PERMS, manage_channels=True)}
            try:
                channel = await guild.create_text_channel(f"mail-{name}", category=category, overwrites=overwrites, topic=f"Mod-mail of {member} ({member.id})", reason="Mod-mail opened")
            except discord.HTTPException as exc:
                log.warning("could not create a mod-mail channel: %s", exc)
                return await interaction.followup.send(f"I could not open a conversation: {exc}", ephemeral=True)
            c["open"][str(channel.id)] = {"user": member.id, "subject": subject, "ts": int(time.time())}
            head = emb("New mod-mail", f"{member.mention} ({member.id})\nAccount created <t:{int(member.created_at.timestamp())}:R>", discord.Color.blurple(), member)
            head.add_field(name="Subject", value=subject, inline=False)
            ping, ping_users, ping_roles = self.bot.staff_ping(guild, "modmail", c["staff_role"])
            await channel.send(ping or staff.mention, embed=head, allowed_mentions=discord.AllowedMentions(users=[discord.Object(u) for u in ping_users], roles=[discord.Object(r) for r in (ping_roles or [staff.id])]))
            await channel.send(embed=emb("How it works", "Write here to answer. The member receives your message by direct message. Start a message with // to write a note only the staff sees. Close the conversation with /modmail close.", discord.Color.light_grey()))
        msg = discord.Embed(description=text, colour=discord.Colour.green())
        msg.set_author(name=f"{member} writes", icon_url=member.display_avatar.url)
        if subject != "Message":
            msg.title = subject
        await channel.send(embed=msg)
        await interaction.followup.send(i18n.say(interaction.client, interaction.guild, "Your message was sent to the staff. Their answer arrives by direct message, so keep your direct messages open."), ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Send what the staff writes in a mod-mail channel to the member by direct message."""
        if msg.author.bot or not msg.guild or not msg.content and not msg.attachments:
            return
        c = self.conf(msg.guild.id)
        data = c["open"].get(str(msg.channel.id))
        if not data or msg.content.startswith("//") or not self.bot.module_on(msg.guild.id, "modmail"):
            return
        member = msg.guild.get_member(data["user"])
        if member is None:
            return await msg.channel.send("The member left the server, so I cannot deliver this.", delete_after=15)
        text = msg.content + "".join(f"\n{a.url}" for a in msg.attachments)
        e = discord.Embed(title=f"Message from the staff of {msg.guild.name}", description=text[:4000], colour=discord.Colour.blurple())
        if not c["anonymous"]:
            e.set_footer(text=f"from {msg.author.display_name}")
        e.add_field(name="Reply", value=f"Use /modmail send on {msg.guild.name} to answer.", inline=False)
        try:
            await member.send(embed=e)
            await msg.add_reaction("\u2705")
        except discord.Forbidden:
            log.info("cannot DM %s, direct messages are closed", member)
            await msg.channel.send("This member has closed their direct messages. I cannot deliver the message. Ask them in the server instead.", delete_after=30)
        except discord.HTTPException as exc:
            log.warning("mod-mail DM to %s failed: %s", member, exc)
            await msg.channel.send(f"Delivery failed: {exc}", delete_after=30)

    @mm.command(name="send", description="Write to the staff privately")
    @app_commands.describe(text="Your message")
    async def mm_send(self, it: discord.Interaction, text: app_commands.Range[str, 1, 1500]):
        """Write to the staff privately."""
        await self.submit(it, "Message", text)

    @mm.command(name="close", description="Close this mod-mail conversation")
    @app_commands.describe(reason="Reason, shown to the member")
    async def mm_close(self, it: discord.Interaction, reason: str = "No reason given"):
        """Close this mod-mail conversation."""
        c = self.conf(it.guild_id)
        data = c["open"].get(str(it.channel_id))
        if not data:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Use this inside a mod-mail channel."), ephemeral=True)
        staff = it.guild.get_role(c["staff_role"]) if c["staff_role"] else None
        if not (it.user.guild_permissions.manage_messages or (staff and staff in it.user.roles)):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Only the staff can close conversations."), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Closing the conversation in 5 seconds."))
        self.bot.team_count(it.guild, it.user.id, "modmail", time.time() - data["ts"] if data.get("ts") else None)
        raw = await transcript(it.channel, f"Mod-mail of {data['user']} | closed by {it.user} | {reason}")
        dest = it.guild.get_channel(c["log_channel"]) if c["log_channel"] else None
        e = emb("Mod-mail closed", color=discord.Color.orange())
        e.add_field(name="Member", value=f"<@{data['user']}> ({data['user']})")
        e.add_field(name="Closed by", value=it.user.mention)
        e.add_field(name="Reason", value=reason[:500], inline=False)
        try:
            if dest:
                await dest.send(embed=e, file=discord.File(io.BytesIO(raw), filename=f"{it.channel.name}.txt"))
            else:
                self.bot.log(it.guild, "moderation", e)
        except discord.HTTPException as exc:
            log.warning("could not store the mod-mail transcript: %s", exc)
        member = it.guild.get_member(data["user"])
        if member:
            try:
                await member.send(f"Your conversation with the staff of {it.guild.name} was closed. Reason: {reason}")
            except discord.Forbidden:
                log.info("cannot DM %s, direct messages are closed", member)
            except discord.HTTPException as exc:
                log.warning("closing notice to %s failed: %s", member, exc)
        c["open"].pop(str(it.channel_id), None)
        await asyncio.sleep(5)
        try:
            await it.channel.delete(reason="Mod-mail closed")
        except discord.HTTPException as exc:
            log.warning("could not delete the mod-mail channel: %s", exc)

    @ms.command(name="set", description="Configure mod-mail")
    @app_commands.describe(category="Category for the conversations", staff_role="Role that sees and answers them", log_channel="Channel for transcripts", anonymous="Hide the name of the staff member in answers")
    async def ms_set(self, it: discord.Interaction, category: discord.CategoryChannel, staff_role: discord.Role, log_channel: discord.TextChannel = None, anonymous: bool = False):
        """Configure mod-mail."""
        g = self.bot.cfg(it.guild_id)
        c = g["modmail"]
        c["category"], c["staff_role"], c["anonymous"] = category.id, staff_role.id, anonymous
        c["log_channel"] = log_channel.id if log_channel else c["log_channel"]
        g["modules"]["modmail"] = True
        await it.response.send_message(i18n.say(it.client, it.guild, "Mod-mail is on. Post the button with /modmail setup panel, or members use /modmail send."), ephemeral=True)

    @ms.command(name="panel", description="Post the button that opens a conversation")
    async def ms_panel(self, it: discord.Interaction, channel: discord.TextChannel, text: str = "Press the button to write to the staff privately."):
        """Post the button that opens a conversation."""
        view = discord.ui.View(timeout=None)
        view.add_item(ModmailOpen())
        try:
            await channel.send(embed=emb("Contact the staff", text.replace("\\n", "\n")), view=view)
        except discord.HTTPException as exc:
            log.warning("could not post the mod-mail panel: %s", exc)
            return await it.response.send_message(f"I cannot post there: {exc}", ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Panel posted."), ephemeral=True)

    @ms.command(name="block", description="Toggle a member who may not use mod-mail")
    async def ms_block(self, it: discord.Interaction, member: discord.Member):
        """Toggle a member who may not use mod-mail."""
        lst = self.conf(it.guild_id)["blocked"]
        lst.remove(member.id) if member.id in lst else lst.append(member.id)
        await it.response.send_message(f"{member.mention} is {'blocked' if member.id in lst else 'allowed again'}.", ephemeral=True)

    @ms.command(name="status", description="Show the mod-mail settings")
    async def ms_status(self, it: discord.Interaction):
        """Show the mod-mail settings."""
        c = self.conf(it.guild_id)
        on = self.bot.module_on(it.guild_id, "modmail")
        text = (
            f"Status: {'on' if on else 'off'}\nCategory: {('<#' + str(c['category']) + '>') if c['category'] else 'not set'}\n"
            f"Staff role: {('<@&' + str(c['staff_role']) + '>') if c['staff_role'] else 'not set'}\nTranscripts: {('<#' + str(c['log_channel']) + '>') if c['log_channel'] else 'moderation log'}\n"
            f"Anonymous answers: {c['anonymous']}\nOpen conversations: {len(c['open'])}\nBlocked members: {len(c['blocked'])}"
        )
        await it.response.send_message(text, ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Modmail(bot))
