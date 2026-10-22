"""Reports: members flag a message for the staff through a context menu or a command."""

import logging
import re
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from .. import i18n
from ..utils import AdminGroup, emb, trim

log = logging.getLogger(__name__)

LINK_RE = re.compile(r"discord(?:app)?\.com/channels/(\d+)/(\d+)/(\d+)")
KEEP_SECONDS = 7 * 86400


class ReportModal(discord.ui.Modal, title="Report message"):
    """Form that asks why a message is reported."""

    reason = discord.ui.TextInput(label="Reason (optional)", style=discord.TextStyle.paragraph, required=False, max_length=500)

    def __init__(self, message):
        """Remember the message that is reported."""
        super().__init__()
        self.message = message

    async def on_submit(self, interaction):
        """Hand the report to the cog and answer the member privately."""
        cog = interaction.client.get_cog("Reports")
        ok, text = await cog.file_report(interaction.user, self.message, str(self.reason.value or ""))
        await interaction.response.send_message(text, ephemeral=True)


class ReportButton(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:report:(?P<act>resolve|delete):(?P<ch>\d+):(?P<msg>\d+)"):
    """Persistent buttons under a report: resolve it or delete the reported message."""

    def __init__(self, act, channel_id, message_id):
        """Create the button for one action."""
        label, style = ("Resolve", discord.ButtonStyle.success) if act == "resolve" else ("Delete message", discord.ButtonStyle.danger)
        super().__init__(discord.ui.Button(label=label, style=style, custom_id=f"gb:report:{act}:{channel_id}:{message_id}"))
        self.act, self.channel_id, self.message_id = act, int(channel_id), int(message_id)

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls(match["act"], match["ch"], match["msg"])

    async def callback(self, interaction):
        """Resolve the report, or delete the message and resolve."""
        perms = interaction.user.guild_permissions
        if not (perms.manage_messages if self.act == "delete" else perms.moderate_members):
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "You are not allowed to do this."), ephemeral=True)
        note = f"Resolved by {interaction.user.mention}"
        interaction.client.team_count(interaction.guild, interaction.user.id, "reports", time.time() - interaction.message.created_at.timestamp())
        if self.act == "delete":
            channel = interaction.guild.get_channel_or_thread(self.channel_id)
            try:
                if channel is None:
                    raise discord.NotFound(None, "channel")
                await (await channel.fetch_message(self.message_id)).delete()
                note = f"Message deleted by {interaction.user.mention}"
            except discord.HTTPException as exc:
                log.info("reported message could not be deleted: %s", exc)
                note = f"Resolved by {interaction.user.mention} (the message was already gone or could not be deleted)"
        embed = interaction.message.embeds[0]
        embed.color = discord.Color.green()
        embed.add_field(name="Status", value=note, inline=False)
        await interaction.response.edit_message(content=None, embed=embed, view=None)


class Reports(commands.Cog):
    """Message reports for the staff."""

    rp = app_commands.Group(name="report", description="Report messages to the staff", guild_only=True)
    rs = AdminGroup(name="setup", description="Configure message reports", parent=rp)

    def __init__(self, bot):
        """Register the persistent buttons and the context menu."""
        self.bot = bot
        self.last = {}
        bot.add_dynamic_items(ReportButton)
        self.menu = app_commands.ContextMenu(name="Report message", callback=self.menu_report)
        self.menu.guild_only = True

    async def cog_load(self):
        """Add the context menu to the command tree."""
        self.bot.tree.add_command(self.menu)

    async def cog_unload(self):
        """Remove the context menu from the command tree."""
        self.bot.tree.remove_command(self.menu.name, type=self.menu.type)

    def conf(self, gid):
        """Return the settings of a server."""
        return self.bot.cfg(gid)["reports"]

    async def menu_report(self, it: discord.Interaction, message: discord.Message):
        """Context menu entry: ask for a reason, then file the report."""
        await it.response.send_modal(ReportModal(message))

    async def file_report(self, reporter, message, reason):
        """Check the report and post it to the staff channel. Returns (ok, text for the reporter)."""
        guild = message.guild
        conf = self.conf(guild.id)
        channel = guild.get_channel(conf["channel"]) if conf["channel"] else None
        if not self.bot.module_on(guild.id, "reports") or channel is None:
            return False, "Reports are not set up on this server."
        if message.author.id == reporter.id or message.author.bot:
            return False, "You cannot report this message."
        if message.channel.id in conf["ignore_channels"]:
            return False, "Messages in this channel cannot be reported."
        now = time.time()
        key = f"{message.id}:{reporter.id}"
        if key in conf["seen"]:
            return False, "You already reported this message."
        wait = conf["cooldown"] - (now - self.last.get((guild.id, reporter.id), 0))
        if wait > 0:
            return False, f"Please wait {int(wait) + 1} seconds before the next report."
        self.last[(guild.id, reporter.id)] = now
        conf["seen"] = {k: v for k, v in conf["seen"].items() if now - v < KEEP_SECONDS}
        conf["seen"][key] = int(now)
        number = conf["next"]
        conf["next"] += 1
        e = emb(f"Report #{number}", color=discord.Color.orange(), user=message.author)
        e.description = trim(message.content, 1500) or "(no text)"
        e.add_field(name="Message", value=f"[Jump]({message.jump_url}) in {message.channel.mention}")
        e.add_field(name="Reported by", value="anonymous" if conf["anonymous"] else f"{reporter.mention} ({reporter.id})")
        if message.attachments:
            e.add_field(name="Attachments", value=str(len(message.attachments)))
        if reason.strip():
            e.add_field(name="Reason", value=trim(reason, 900), inline=False)
        view = discord.ui.View(timeout=None)
        view.add_item(ReportButton("resolve", message.channel.id, message.id))
        view.add_item(ReportButton("delete", message.channel.id, message.id))
        ping, ping_users, ping_roles = self.bot.staff_ping(guild, "reports", conf["ping_role"])
        try:
            await channel.send(ping or None, embed=e, view=view, allowed_mentions=discord.AllowedMentions(users=[discord.Object(u) for u in ping_users], roles=[discord.Object(r) for r in ping_roles]))
        except discord.HTTPException as exc:
            log.warning("report could not be posted: %s", exc)
            return False, "The report could not be delivered. Please tell a moderator."
        self.bot.team_event(guild, "reports")
        return True, "Thank you, the staff was notified."

    async def report_link(self, member, guild, link, reason):
        """Find the message behind a link on this server and file the report. Returns the text for the reporter."""
        m = LINK_RE.search(link)
        if not m or int(m.group(1)) != guild.id:
            return "Use a link to a message on this server."
        channel = guild.get_channel_or_thread(int(m.group(2)))
        try:
            message = await channel.fetch_message(int(m.group(3))) if channel else None
        except discord.HTTPException:
            message = None
        if message is None:
            return "I could not find that message."
        return (await self.file_report(member, message, reason or ""))[1]

    @rp.command(name="send", description="Report a message to the staff")
    @app_commands.describe(message_link="Link to the message (right click, Copy Message Link)", reason="Why you report it")
    async def report_send(self, it: discord.Interaction, message_link: str, reason: Optional[str] = None):
        """Report a message to the staff."""
        await it.response.send_message(await self.report_link(it.user, it.guild, message_link, reason), ephemeral=True)

    @commands.command(name="report")
    @commands.guild_only()
    async def report_text(self, ctx, message_link: str, *, reason: Optional[str] = None):
        """Report a message with the prefix. The command message is deleted so the report stays private."""
        try:
            await ctx.message.delete()
        except discord.HTTPException as exc:
            log.info("could not delete the report command message: %s", exc)
        await ctx.send(await self.report_link(ctx.author, ctx.guild, message_link, reason), delete_after=10)

    @rs.command(name="set", description="Choose the staff channel and options")
    @app_commands.describe(channel="Channel for reports", ping_role="Role that is pinged", cooldown="Seconds between two reports of one member", anonymous="Hide the name of the reporter from the staff")
    async def rs_set(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None, ping_role: Optional[discord.Role] = None, cooldown: Optional[app_commands.Range[int, 0, 3600]] = None, anonymous: Optional[bool] = None):
        """Choose the staff channel and options."""
        c = self.conf(it.guild_id)
        if channel:
            c["channel"] = channel.id
        if ping_role:
            c["ping_role"] = ping_role.id
        if cooldown is not None:
            c["cooldown"] = cooldown
        if anonymous is not None:
            c["anonymous"] = anonymous
        await it.response.send_message(i18n.say(it.client, it.guild, "Saved. Use /report setup status to see the settings."), ephemeral=True)

    @rs.command(name="clearping", description="Stop pinging a role for new reports")
    async def rs_clearping(self, it: discord.Interaction):
        """Stop pinging a role for new reports."""
        self.conf(it.guild_id)["ping_role"] = None
        await it.response.send_message(i18n.say(it.client, it.guild, "No role is pinged any more."), ephemeral=True)

    @rs.command(name="ignorechannel", description="Toggle a channel whose messages cannot be reported")
    async def rs_ignore(self, it: discord.Interaction, channel: discord.TextChannel):
        """Toggle a channel whose messages cannot be reported."""
        lst = self.conf(it.guild_id)["ignore_channels"]
        lst.remove(channel.id) if channel.id in lst else lst.append(channel.id)
        await it.response.send_message(f"{channel.mention} is {'ignored' if channel.id in lst else 'no longer ignored'}.", ephemeral=True)

    @rs.command(name="status", description="Show the report settings")
    async def rs_status(self, it: discord.Interaction):
        """Show the report settings."""
        c = self.conf(it.guild_id)
        lines = [
            f"Module: {'on' if self.bot.module_on(it.guild_id, 'reports') else 'off'}",
            f"Channel: {'<#' + str(c['channel']) + '>' if c['channel'] else 'not set'}",
            f"Ping role: {'<@&' + str(c['ping_role']) + '>' if c['ping_role'] else 'none'}",
            f"Cooldown: {c['cooldown']} seconds, anonymous: {c['anonymous']}",
            f"Ignored channels: {' '.join('<#' + str(i) + '>' for i in c['ignore_channels']) or 'none'}",
        ]
        await it.response.send_message("\n".join(lines), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Reports(bot))
