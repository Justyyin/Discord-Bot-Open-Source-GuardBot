"""Ticket system with buttons and transcripts."""

import asyncio
import io
import logging
import re
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from ... import i18n
from ...utils import emb, transcript

log = logging.getLogger(__name__)

PERMS = dict(view_channel=True, send_messages=True, attach_files=True, read_message_history=True, embed_links=True)


async def open_ticket(interaction, type_key):
    """Create a private ticket channel for the user and post the first message."""
    bot, guild, user = interaction.client, interaction.guild, interaction.user
    if not bot.module_on(guild.id, "tickets"):
        return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Tickets are disabled."), ephemeral=True)
    t = bot.cfg(guild.id)["tickets"]
    if type_key not in t["types"]:
        return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This ticket type no longer exists."), ephemeral=True)
    mine = [cid for cid, d in t["open"].items() if d["user"] == user.id]
    if len(mine) >= t["max_open"]:
        return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "You already have an open ticket: <#{mine}>", mine=mine[0]), ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    category = guild.get_channel(t["category"]) if t["category"] else None
    support = guild.get_role(t["support_role"]) if t["support_role"] else None
    t["counter"] += 1
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(**PERMS),
        guild.me: discord.PermissionOverwrite(**PERMS, manage_channels=True),
    }
    if support:
        overwrites[support] = discord.PermissionOverwrite(**PERMS, manage_messages=True)
    try:
        ch = await guild.create_text_channel(
            f"{type_key}-{t['counter']:04d}",
            category=category if isinstance(category, discord.CategoryChannel) else None,
            overwrites=overwrites,
            topic=f"Ticket of {user} ({user.id}) | {type_key}",
            reason="Ticket opened",
        )
    except discord.HTTPException as exc:
        return await interaction.followup.send(i18n.say(interaction.client, interaction.guild, "Could not create the ticket: {exc}", exc=exc), ephemeral=True)
    t["open"][str(ch.id)] = {"user": user.id, "type": type_key, "ts": int(time.time())}
    bot.team_event(guild, "tickets_opened")
    view = discord.ui.View(timeout=None)
    view.add_item(TicketClose())
    info = t["types"][type_key]
    staff_text, staff_users, staff_roles = bot.staff_ping(guild, "tickets", t["support_role"])
    mentions = user.mention + (f" {staff_text}" if staff_text else "")
    await ch.send(
        mentions,
        embed=emb(f"{info['label']} ticket", f"{user.mention}, describe your request. A staff member will answer here.\nPress the button below to close the ticket."),
        view=view,
        allowed_mentions=discord.AllowedMentions(users=[user, *(discord.Object(u) for u in staff_users)], roles=[discord.Object(r) for r in staff_roles]),
    )
    await interaction.followup.send(i18n.say(interaction.client, interaction.guild, "Your ticket: {mention}", mention=ch.mention), ephemeral=True)


async def close_ticket(interaction):
    """Send the transcript to the log channel and the owner, then delete the ticket channel."""
    bot, guild, ch = interaction.client, interaction.guild, interaction.channel
    t = bot.cfg(guild.id)["tickets"]
    data = t["open"].get(str(ch.id))
    if not data:
        return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This is not a ticket."), ephemeral=True)
    member = interaction.user
    support = guild.get_role(t["support_role"]) if t["support_role"] else None
    if not (member.id == data["user"] or member.guild_permissions.manage_channels or (support and support in member.roles)):
        return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Only the ticket owner or staff can close it."), ephemeral=True)
    await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Closing the ticket in 5 seconds."))
    raw = await transcript(ch, f"Transcript of #{ch.name} | closed by {member}")
    dest = guild.get_channel(t["log_channel"]) if t["log_channel"] else None
    e = emb("Ticket closed", color=discord.Color.orange())
    e.add_field(name="Ticket", value=ch.name)
    e.add_field(name="Owner", value=f"<@{data['user']}> ({data['user']})")
    e.add_field(name="Closed by", value=member.mention)
    if dest:
        await dest.send(embed=e, file=discord.File(io.BytesIO(raw), filename=f"{ch.name}.txt"))
    else:
        bot.log(guild, "main", e)
    owner = guild.get_member(data["user"])
    if owner:
        try:
            await owner.send(f"Your ticket in {guild.name} was closed. Transcript attached.", file=discord.File(io.BytesIO(raw), filename=f"{ch.name}.txt"))
        except discord.Forbidden:
            log.info("cannot DM %s, direct messages are closed", owner)
        except discord.HTTPException as exc:
            log.warning("owner.send failed: %s", exc)
    t["open"].pop(str(ch.id), None)
    bot.team_event(guild, "tickets_closed")
    if member.id != data["user"]:
        bot.team_count(guild, member.id, "tickets", time.time() - data["ts"] if data.get("ts") else None)
    await asyncio.sleep(5)
    try:
        await ch.delete(reason="Ticket closed")
    except discord.HTTPException as exc:
        log.warning("ch.delete failed: %s", exc)


class TicketOpen(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:ticket:open:(?P<type>[\w-]+)"):
    """Persistent button that opens a ticket."""
    def __init__(self, type_key, label="Open ticket"):
        """Create the button that opens a ticket of one type."""
        super().__init__(discord.ui.Button(label=label, style=discord.ButtonStyle.primary, custom_id=f"gb:ticket:open:{type_key}"))
        self.type_key = type_key

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls(match["type"], item.label)

    async def callback(self, interaction):
        """Open a ticket of this button's type."""
        await open_ticket(interaction, self.type_key)


class TicketClose(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:ticket:close"):
    """Persistent button that closes a ticket."""
    def __init__(self):
        """Create the button that closes a ticket."""
        super().__init__(discord.ui.Button(label="Close ticket", style=discord.ButtonStyle.danger, custom_id="gb:ticket:close"))

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls()

    async def callback(self, interaction):
        """Close the ticket this button belongs to."""
        await close_ticket(interaction)


class Tickets(commands.Cog):
    """Ticket setup and panel commands."""
    grp = app_commands.Group(name="ticket", description="Ticket system", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot
        bot.add_dynamic_items(TicketOpen, TicketClose)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, ch):
        """Runs when a channel is deleted."""
        t = self.bot.cfg(ch.guild.id)["tickets"]
        t["open"].pop(str(ch.id), None)

    @grp.command(name="setup", description="Configure the ticket system")
    @app_commands.describe(category="Category for ticket channels", support_role="Role that can see and answer tickets", log_channel="Channel for transcripts", max_open="Open tickets per member")
    async def t_setup(self, it: discord.Interaction, category: Optional[discord.CategoryChannel] = None, support_role: Optional[discord.Role] = None, log_channel: Optional[discord.TextChannel] = None, max_open: Optional[app_commands.Range[int, 1, 10]] = None):
        """Configure the ticket system."""
        t = self.bot.cfg(it.guild_id)["tickets"]
        if category:
            t["category"] = category.id
        if support_role:
            t["support_role"] = support_role.id
        if log_channel:
            t["log_channel"] = log_channel.id
        if max_open:
            t["max_open"] = max_open
        await it.response.send_message(i18n.say(it.client, it.guild, "Saved. Post a panel with /support ticket panel."), ephemeral=True)

    @grp.command(name="panel", description="Post the ticket panel with one button per type")
    async def t_panel(self, it: discord.Interaction, channel: discord.TextChannel, title: str = "Support", description: str = "Press a button to open a ticket."):
        """Post the ticket panel with one button per type."""
        types = self.bot.cfg(it.guild_id)["tickets"]["types"]
        if not types:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Add a ticket type first."), ephemeral=True)
        view = discord.ui.View(timeout=None)
        for key, info in list(types.items())[:25]:
            view.add_item(TicketOpen(key, info["label"]))
        lines = "\n".join(f"{i['label']}: {i['desc']}" for i in types.values())
        await channel.send(embed=emb(title, description.replace("\\n", "\n") + "\n\n" + lines), view=view)
        await it.response.send_message(i18n.say(it.client, it.guild, "Panel posted."), ephemeral=True)

    @grp.command(name="addtype", description="Add or change a ticket type")
    async def t_addtype(self, it: discord.Interaction, key: str, label: str, description: str = ""):
        """Add or change a ticket type."""
        if not re.fullmatch(r"[\w-]{1,20}", key):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Use only letters, numbers, - and _ (max 20)."), ephemeral=True)
        self.bot.cfg(it.guild_id)["tickets"]["types"][key.lower()] = {"label": label[:80], "desc": description}
        await it.response.send_message(i18n.say(it.client, it.guild, "Type '{lower}' saved. Post the panel again to show it.", lower=key.lower()), ephemeral=True)

    @grp.command(name="removetype", description="Remove a ticket type")
    async def t_removetype(self, it: discord.Interaction, key: str):
        """Remove a ticket type."""
        if self.bot.cfg(it.guild_id)["tickets"]["types"].pop(key.lower(), None) is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "No such type."), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Removed."), ephemeral=True)

    @grp.command(name="add", description="Add a member to this ticket")
    async def t_add(self, it: discord.Interaction, member: discord.Member):
        """Add a member to this ticket."""
        if str(it.channel_id) not in self.bot.cfg(it.guild_id)["tickets"]["open"]:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Use this inside a ticket."), ephemeral=True)
        await it.channel.set_permissions(member, overwrite=discord.PermissionOverwrite(**PERMS))
        await it.response.send_message(i18n.say(it.client, it.guild, "{mention} added.", mention=member.mention))

    @grp.command(name="remove", description="Remove a member from this ticket")
    async def t_remove(self, it: discord.Interaction, member: discord.Member):
        """Remove a member from this ticket."""
        if str(it.channel_id) not in self.bot.cfg(it.guild_id)["tickets"]["open"]:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Use this inside a ticket."), ephemeral=True)
        await it.channel.set_permissions(member, overwrite=None)
        await it.response.send_message(i18n.say(it.client, it.guild, "{mention} removed.", mention=member.mention))

    def ticket_here(self, it):
        """Return the stored ticket data of the channel of an interaction, or None."""
        return self.bot.cfg(it.guild_id)["tickets"]["open"].get(str(it.channel_id))

    def is_staff(self, it):
        """True if the user may handle tickets (support role or Manage Channels)."""
        t = self.bot.cfg(it.guild_id)["tickets"]
        support = it.guild.get_role(t["support_role"]) if t["support_role"] else None
        return it.user.guild_permissions.manage_channels or (support is not None and support in it.user.roles)

    @grp.command(name="claim", description="Take over this ticket")
    async def t_claim(self, it: discord.Interaction):
        """Take over this ticket."""
        data = self.ticket_here(it)
        if not data:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Use this inside a ticket."), ephemeral=True)
        if not self.is_staff(it):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Only the support team can claim tickets."), ephemeral=True)
        if data.get("claimed") and data["claimed"] != it.user.id:
            return await it.response.send_message(i18n.say(it.client, it.guild, "This ticket is already claimed by <@{claimed}>.", claimed=data['claimed']), ephemeral=True)
        data["claimed"] = it.user.id
        await it.response.send_message(embed=emb("Ticket claimed", f"{it.user.mention} takes care of this ticket."))

    @grp.command(name="rename", description="Rename this ticket channel")
    @app_commands.describe(name="New name")
    async def t_rename(self, it: discord.Interaction, name: str):
        """Rename this ticket channel."""
        if not self.ticket_here(it):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Use this inside a ticket."), ephemeral=True)
        if not self.is_staff(it):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Only the support team can rename tickets."), ephemeral=True)
        clean = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")[:90]
        if not clean:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Use letters and numbers in the name."), ephemeral=True)
        try:
            await it.channel.edit(name=clean, reason=f"Renamed by {it.user}")
        except discord.HTTPException as exc:
            log.warning("renaming ticket %s failed: %s", it.channel_id, exc)
            return await it.response.send_message(i18n.say(it.client, it.guild, "I could not rename the channel: {exc}", exc=exc), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Renamed to {clean}.", clean=clean))

    @grp.command(name="list", description="List all open tickets")
    async def t_list(self, it: discord.Interaction):
        """List all open tickets."""
        lines = []
        for cid, d in self.bot.cfg(it.guild_id)["tickets"]["open"].items():
            lines.append(f"<#{cid}> {d['type']} by <@{d['user']}>" + (f", claimed by <@{d['claimed']}>" if d.get("claimed") else ""))
        await it.response.send_message("\n".join(lines[:40]) or "No open tickets.", ephemeral=True)

    @grp.command(name="close", description="Close this ticket")
    async def t_close(self, it: discord.Interaction):
        """Close this ticket."""
        await close_ticket(it)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Tickets(bot))
