"""Ban appeals through an appeal server. The bot never reads direct messages: banned users use /appeal on a second server."""

import logging
import time

import discord
from discord import app_commands

from ...cog import BaseCog
from ... import i18n
from ...utils import AdminGroup, emb

log = logging.getLogger(__name__)


class AppealButton(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:appeal:(?P<action>accept|deny):(?P<id>\d+)"):
    """Persistent accept and deny buttons under an appeal."""

    def __init__(self, action, aid):
        """Create the button for one action of one appeal."""
        style = discord.ButtonStyle.success if action == "accept" else discord.ButtonStyle.danger
        super().__init__(discord.ui.Button(label="Accept" if action == "accept" else "Deny", style=style, custom_id=f"gb:appeal:{action}:{aid}"))
        self.action, self.aid = action, aid

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls(match["action"], int(match["id"]))

    async def callback(self, interaction):
        """Decide the appeal."""
        await interaction.client.get_cog("Appeals").decide(interaction, self.action, self.aid)


class Appeals(BaseCog):
    """Ban appeals reviewed by the staff of the main server."""
    section = "appeals"

    ap = app_commands.Group(name="appeal", description="Ban appeals", guild_only=True)
    aps = AdminGroup(name="setup", description="Configure ban appeals", parent=ap)

    def __init__(self, bot):
        """Keep the bot reference and register the persistent buttons."""
        self.bot = bot
        bot.add_dynamic_items(AppealButton)

    async def dm(self, user, text):
        """Send a direct message and note it in the log when that is not possible."""
        try:
            await user.send(text)
        except discord.Forbidden:
            log.info("cannot DM %s, direct messages are closed", user)
        except discord.HTTPException as exc:
            log.warning("DM to %s failed: %s", user, exc)

    @ap.command(name="send", description="Ask the staff of the main server to lift your ban")
    @app_commands.describe(text="Why should the ban be lifted?")
    @app_commands.guild_only()
    async def appeal_cmd(self, it: discord.Interaction, text: app_commands.Range[str, 10, 1500]):
        """Ask the staff of the main server to lift your ban."""
        here = self.conf(it.guild_id)
        main = self.bot.get_guild(here["main_guild"] or 0)
        if main is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Appeals are not set up on this server."), ephemeral=True)
        try:
            ban = await main.fetch_ban(discord.Object(it.user.id))
        except discord.NotFound:
            return await it.response.send_message(i18n.say(it.client, it.guild, "You are not banned on the main server."), ephemeral=True)
        except discord.HTTPException as exc:
            log.warning("could not check the ban of %s on %s: %s", it.user, main.id, exc)
            return await it.response.send_message(i18n.say(it.client, it.guild, "I could not check your ban. Try again later."), ephemeral=True)
        ma = self.conf(main.id)
        now = int(time.time())
        wait = ma["last"].get(str(it.user.id), 0) + ma["cooldown_days"] * 86400
        if wait > now:
            return await it.response.send_message(i18n.say(it.client, it.guild, "You already sent an appeal. You can send the next one <t:{wait}:R>.", wait=wait), ephemeral=True)
        channel = main.get_channel(ma["staff_channel"] or 0)
        if channel is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "The staff of the main server did not set up appeals yet."), ephemeral=True)
        aid = ma["next"]
        ma["next"] += 1
        ma["items"][str(aid)] = {"user": it.user.id, "name": str(it.user), "text": text, "status": "open", "ts": now}
        ma["last"][str(it.user.id)] = now
        e = emb(f"Ban appeal #{aid}", text, discord.Color.orange(), it.user)
        e.add_field(name="Ban reason", value=(ban.reason or "none")[:500], inline=False)
        e.add_field(name="Account created", value=f"<t:{int(it.user.created_at.timestamp())}:R>")
        view = discord.ui.View(timeout=None)
        view.add_item(AppealButton("accept", aid))
        view.add_item(AppealButton("deny", aid))
        try:
            await channel.send(embed=e, view=view)
        except discord.HTTPException as exc:
            log.warning("could not post appeal %s: %s", aid, exc)
            ma["items"].pop(str(aid), None)
            ma["last"].pop(str(it.user.id), None)
            return await it.response.send_message(i18n.say(it.client, it.guild, "I could not deliver your appeal to the staff. Try again later."), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Your appeal was sent. You get a direct message with the answer, so keep your direct messages open."), ephemeral=True)

    async def decide(self, interaction, action, aid):
        """Accept or deny an appeal, tell the user and update the staff message."""
        guild = interaction.guild
        if not self.bot.module_on(guild.id, "appeals"):
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Appeals are turned off."), ephemeral=True)
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "You need the Ban Members permission to decide appeals."), ephemeral=True)
        ma = self.conf(guild.id)
        item = ma["items"].get(str(aid))
        if not item or item["status"] != "open":
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This appeal was already decided."), ephemeral=True)
        user = await self.bot.fetch_user(item["user"])
        if action == "accept":
            try:
                await guild.unban(user, reason=f"Appeal #{aid} accepted by {interaction.user}")
            except discord.NotFound:
                log.info("user %s was already unbanned", user)
            except discord.HTTPException as exc:
                log.warning("could not unban %s: %s", user, exc)
                return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "I could not lift the ban: {exc}", exc=exc), ephemeral=True)
            await self.bot.get_cog("Moderation").add_case(guild, "unban", user, interaction.user, f"Appeal #{aid} accepted")
            rejoin = f" You can join again here: {ma['rejoin_invite']}" if ma["rejoin_invite"] else ""
            await self.dm(user, f"Your ban appeal for {guild.name} was accepted.{rejoin}")
        else:
            await self.dm(user, f"Your ban appeal for {guild.name} was denied.")
        item["status"] = "accepted" if action == "accept" else "denied"
        self.bot.team_count(guild, interaction.user.id, "appeals", time.time() - item["ts"])
        self.bot.team_event(guild, "appeals")
        e = interaction.message.embeds[0]
        e.color = discord.Color.green() if action == "accept" else discord.Color.red()
        e.add_field(name="Decision", value=f"{item['status']} by {interaction.user.mention}", inline=False)
        await interaction.response.edit_message(embed=e, view=None)

    @aps.command(name="set", description="Configure ban appeals")
    @app_commands.describe(main_server_id="On the appeal server: the ID of the main server", staff_channel="On the main server: where appeals arrive", invite="On the main server: invite of the appeal server, sent to banned users", rejoin_invite="On the main server: invite to the main server for accepted users", cooldown_days="Days before a user may appeal again")
    async def ap_set(self, it: discord.Interaction, main_server_id: str = None, staff_channel: discord.TextChannel = None, invite: str = None, rejoin_invite: str = None, cooldown_days: app_commands.Range[int, 0, 365] = None):
        """Configure ban appeals."""
        g = self.bot.cfg(it.guild_id)
        a = g["appeals"]
        if main_server_id:
            if not main_server_id.isdigit() or self.bot.get_guild(int(main_server_id)) is None:
                return await it.response.send_message(i18n.say(it.client, it.guild, "The bot is not on a server with that ID. Invite the bot to the main server first."), ephemeral=True)
            a["main_guild"] = int(main_server_id)
        if staff_channel:
            a["staff_channel"] = staff_channel.id
        for key, value in (("invite", invite), ("rejoin_invite", rejoin_invite)):
            if value:
                if not value.startswith("https://"):
                    return await it.response.send_message(i18n.say(it.client, it.guild, "Invites must start with https://"), ephemeral=True)
                a[key] = value
        if cooldown_days is not None:
            a["cooldown_days"] = cooldown_days
        g["modules"]["appeals"] = True
        await it.response.send_message(i18n.say(it.client, it.guild, "Saved. Run /appeal setup status to check the setup."), ephemeral=True)

    @aps.command(name="status", description="Show the appeal settings")
    async def ap_status(self, it: discord.Interaction):
        """Show the appeal settings."""
        a = self.conf(it.guild_id)
        on = self.bot.module_on(it.guild_id, "appeals")
        open_items = sum(1 for i in a["items"].values() if i["status"] == "open")
        text = (
            f"Status: {'on' if on else 'off'}\nMain server: {a['main_guild'] or 'this is the main server'}\n"
            f"Staff channel: {('<#' + str(a['staff_channel']) + '>') if a['staff_channel'] else 'not set'}\n"
            f"Appeal server invite: {a['invite'] or 'not set'}\nRejoin invite: {a['rejoin_invite'] or 'not set'}\n"
            f"Cooldown: {a['cooldown_days']} days\nOpen appeals: {open_items}"
        )
        await it.response.send_message(text, ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Appeals(bot))
