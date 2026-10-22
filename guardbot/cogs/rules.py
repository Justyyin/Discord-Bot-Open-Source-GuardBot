"""Rules with an accept button, a version number and reminders for members who did not accept the current version."""

import logging
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from .. import i18n
from ..utils import require, trim

log = logging.getLogger(__name__)

MAX_RULES = 25
REMIND_PER_RUN = 20


def numbered(rules):
    """The rules as numbered lines."""
    return "\n".join(f"**{i}.** {text}" for i, text in enumerate(rules, 1))


def needs_reminder(rec, version, since, hours, now):
    """True if a member has not accepted the current version, was not reminded about it yet and had enough time."""
    rec = rec or {}
    if rec.get("rules", 0) >= version or rec.get("rules_reminded", 0) >= version:
        return False
    return now - since >= hours * 3600


class AcceptButton(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:rules:accept"):
    """The persistent accept button under the rules."""

    def __init__(self, label="I accept the rules"):
        """Create the button."""
        super().__init__(discord.ui.Button(label=label[:80], style=discord.ButtonStyle.success, custom_id="gb:rules:accept"))

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button after a restart."""
        return cls()

    async def callback(self, interaction):
        """Remember that the member accepted the rules."""
        await interaction.client.get_cog("Rules").accept(interaction)


class Rules(commands.Cog):
    """Rules with accept button, version and reminders."""

    rules = app_commands.Group(name="rules", description="Server rules with an accept button", guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and register the persistent button."""
        self.bot = bot
        bot.add_dynamic_items(AcceptButton)

    async def cog_load(self):
        """Start the reminder loop."""
        self.remind_loop.start()

    async def cog_unload(self):
        """Stop the reminder loop."""
        self.remind_loop.cancel()

    def conf(self, gid):
        """Return the rules settings of a server."""
        return self.bot.cfg(gid)["rules"]

    def embed(self, guild):
        """Build the rules message in the language of the server."""
        c = self.conf(guild.id)
        title = i18n.say(self.bot, guild, "Server rules") if c["title"] == "Server rules" else c["title"]
        e = discord.Embed(title=title, description=trim(numbered(c["text"]), 4000), color=discord.Color.blurple())
        e.set_footer(text=i18n.say(self.bot, guild, "Version {version}", version=c["version"]))
        return e

    async def accept(self, interaction):
        """Store the accepted version and give the role."""
        guild = interaction.guild
        if guild is None or not self.bot.module_on(guild.id, "rules"):
            return await interaction.response.send_message(i18n.say(self.bot, guild, "This module is turned off."), ephemeral=True)
        c = self.conf(guild.id)
        rec = self.bot.store.user(guild.id, interaction.user.id)
        rec["rules"] = c["version"]
        role = guild.get_role(c["role"] or 0)
        if role is not None and role not in interaction.user.roles and role.is_assignable():
            try:
                await interaction.user.add_roles(role, reason="Accepted the rules")
            except discord.HTTPException as exc:
                log.warning("rules role for %s failed: %s", interaction.user.id, exc)
        await interaction.response.send_message(i18n.say(self.bot, guild, "Thank you. You accepted the rules."), ephemeral=True)

    @tasks.loop(minutes=10)
    async def remind_loop(self):
        """Remind members who did not accept the current version, once per version."""
        now = time.time()
        for guild in list(self.bot.guilds):
            c = self.conf(guild.id)
            if not self.bot.module_on(guild.id, "rules") or not c["remind"] or not c["text"] or not c["message"]:
                continue
            sent = 0
            users = self.bot.store.users(guild.id)
            for member in guild.members:
                if member.bot or sent >= REMIND_PER_RUN:
                    continue
                since = max(member.joined_at.timestamp() if member.joined_at else 0, c["changed"])
                if not needs_reminder(users.get(str(member.id)), c["version"], since, c["remind_hours"], now):
                    continue
                sent += 1
                self.bot.store.user(guild.id, member.id)["rules_reminded"] = c["version"]
                link = f"https://discord.com/channels/{guild.id}/{c['message'][0]}/{c['message'][1]}"
                try:
                    await member.send(i18n.say(self.bot, guild, "{server}: please read and accept the rules: {link}", server=guild.name, link=link))
                except discord.HTTPException as exc:
                    log.info("rules reminder to %s not delivered: %s", member.id, exc)

    @remind_loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected."""
        await self.bot.wait_until_ready()

    @rules.command(name="setup", description="Choose the channel, the role for members who accepted and the reminders")
    @app_commands.describe(channel="Channel of the rules", role="Role for members who accepted", title="Title of the message", remind="Remind members by direct message", remind_hours="Hours after joining or after a change before the reminder")
    async def setup(
        self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None, role: Optional[discord.Role] = None, title: Optional[app_commands.Range[str, 1, 100]] = None,
        remind: Optional[bool] = None, remind_hours: Optional[app_commands.Range[int, 1, 720]] = None,
    ):
        """Choose the channel, the role for members who accepted and the reminders."""
        if not await require(it):
            return
        c = self.conf(it.guild_id)
        if channel is not None:
            c["channel"] = channel.id
        if role is not None:
            if role.is_default() or role.managed or not role.is_assignable():
                return await it.response.send_message(i18n.say(it.client, it.guild, "I cannot give that role. Move my role above it or choose another one."), ephemeral=True)
            c["role"] = role.id
        for key, value in (("title", title), ("remind", remind), ("remind_hours", remind_hours)):
            if value is not None:
                c[key] = value
        self.bot.cfg(it.guild_id)["modules"]["rules"] = True
        await it.response.send_message("Saved. Add rules with /structure rules add, then publish them with /structure rules post.", ephemeral=True)

    @rules.command(name="add", description="Add a rule")
    async def add(self, it: discord.Interaction, text: app_commands.Range[str, 3, 500], position: Optional[app_commands.Range[int, 1, 25]] = None):
        """Add a rule at the end or at a position."""
        if not await require(it):
            return
        c = self.conf(it.guild_id)
        if len(c["text"]) >= MAX_RULES:
            return await it.response.send_message(f"At most {MAX_RULES} rules.", ephemeral=True)
        c["text"].insert((position - 1) if position else len(c["text"]), text)
        await it.response.send_message(f"Rule added. {len(c['text'])} rules. The published message changes with /structure rules post.", ephemeral=True)

    @rules.command(name="edit", description="Change a rule")
    async def edit(self, it: discord.Interaction, number: app_commands.Range[int, 1, 25], text: app_commands.Range[str, 3, 500]):
        """Change a rule."""
        if not await require(it):
            return
        c = self.conf(it.guild_id)
        if number > len(c["text"]):
            return await it.response.send_message(f"There are only {len(c['text'])} rules.", ephemeral=True)
        c["text"][number - 1] = text
        await it.response.send_message("Changed.", ephemeral=True)

    @rules.command(name="remove", description="Delete a rule")
    async def remove(self, it: discord.Interaction, number: app_commands.Range[int, 1, 25]):
        """Delete a rule."""
        if not await require(it):
            return
        c = self.conf(it.guild_id)
        if number > len(c["text"]):
            return await it.response.send_message(f"There are only {len(c['text'])} rules.", ephemeral=True)
        c["text"].pop(number - 1)
        await it.response.send_message("Deleted.", ephemeral=True)

    @rules.command(name="list", description="Show the rules")
    async def list_cmd(self, it: discord.Interaction):
        """Show the rules."""
        c = self.conf(it.guild_id)
        await it.response.send_message(embed=self.embed(it.guild) if c["text"] else None, content=None if c["text"] else "No rules yet.", ephemeral=True)

    @rules.command(name="post", description="Publish the rules with the accept button, or update the message")
    @app_commands.describe(new_version="Members have to accept again")
    async def post(self, it: discord.Interaction, new_version: bool = False):
        """Publish the rules with the accept button, or update the message. With new_version every member has to accept again and is reminded."""
        if not await require(it):
            return
        c = self.conf(it.guild_id)
        channel = it.guild.get_channel(c["channel"] or 0)
        if channel is None or not c["text"]:
            return await it.response.send_message("Set a channel with /structure rules setup and add rules first.", ephemeral=True)
        await it.response.defer(ephemeral=True)
        if new_version:
            c["version"] += 1
            c["changed"] = int(time.time())
        view = discord.ui.View(timeout=None)
        view.add_item(AcceptButton(i18n.say(self.bot, it.guild, "I accept the rules")))
        old = None
        if c["message"] and c["message"][0] == channel.id:
            try:
                old = await channel.fetch_message(c["message"][1])
            except discord.HTTPException:
                old = None
        try:
            if old is not None:
                await old.edit(embed=self.embed(it.guild), view=view)
                msg = old
            else:
                msg = await channel.send(embed=self.embed(it.guild), view=view)
        except discord.HTTPException as exc:
            return await it.followup.send(f"Discord refused: {exc}")
        c["message"] = [channel.id, msg.id]
        self.bot.cfg(it.guild_id)["modules"]["rules"] = True
        await it.followup.send(f"Published in {channel.mention}, version {c['version']}." + (" Members who did not accept it yet are reminded." if new_version and c["remind"] else ""))

    @rules.command(name="status", description="How many members accepted the current version")
    async def status(self, it: discord.Interaction):
        """How many members accepted the current version."""
        c = self.conf(it.guild_id)
        users = self.bot.store.users(it.guild_id)
        members = [m for m in it.guild.members if not m.bot]
        ok = sum(1 for m in members if users.get(str(m.id), {}).get("rules", 0) >= c["version"])
        await it.response.send_message(f"Version {c['version']}: {ok} of {len(members)} members accepted. Reminders: {'on' if c['remind'] else 'off'} after {c['remind_hours']} hours.", ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Rules(bot))
