"""Staff applications: a form for members and a vote of the team."""

import logging
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from .. import i18n
from ..utils import require, trim

log = logging.getLogger(__name__)

MAX_QUESTIONS = 5


def tally(votes):
    """Count yes and no votes. votes maps user id to 'yes' or 'no'."""
    values = list(votes.values())
    return values.count("yes"), values.count("no")


def outcome(votes, needed):
    """'accepted' or 'denied' once one side has enough votes, else None."""
    yes, no = tally(votes)
    if yes >= needed:
        return "accepted"
    if no >= needed:
        return "denied"
    return None


class VoteButton(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:app:(?P<vote>yes|no):(?P<id>\d+)"):
    """Persistent vote buttons under an application."""

    def __init__(self, vote, aid):
        """Create the button for one vote on one application."""
        style = discord.ButtonStyle.success if vote == "yes" else discord.ButtonStyle.danger
        super().__init__(discord.ui.Button(label="Yes" if vote == "yes" else "No", style=style, custom_id=f"gb:app:{vote}:{aid}"))
        self.vote, self.aid = vote, aid

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button after a restart."""
        return cls(match["vote"], int(match["id"]))

    async def callback(self, interaction):
        """Register the vote."""
        await interaction.client.get_cog("Applications").cast(interaction, self.vote, self.aid)


class Form(discord.ui.Modal):
    """The application form with the questions of the server."""

    def __init__(self, cog, questions):
        """Add one text field per question."""
        super().__init__(title="Application", timeout=900)
        self.cog = cog
        self.questions = questions
        self.fields = []
        for q in questions[:MAX_QUESTIONS]:
            field = discord.ui.TextInput(label=q[:45], style=discord.TextStyle.paragraph, max_length=900, required=True)
            self.fields.append(field)
            self.add_item(field)

    async def on_submit(self, interaction):
        """Send the application to the team."""
        await self.cog.submit(interaction, [(q, f.value) for q, f in zip(self.questions, self.fields)])


class Applications(commands.Cog):
    """Applications for the team with a vote."""

    ap = app_commands.Group(name="apply", description="Apply for the team", guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and register the persistent buttons."""
        self.bot = bot
        bot.add_dynamic_items(VoteButton)

    def conf(self, gid):
        """Return the application settings of a server."""
        return self.bot.cfg(gid)["applications"]

    def embed(self, item, number):
        """Build the message of an application with the current votes."""
        yes, no = tally(item["votes"])
        color = {"open": discord.Color.blurple(), "accepted": discord.Color.green(), "denied": discord.Color.red()}[item["status"]]
        e = discord.Embed(title=f"Application #{number} ({item['status']})", description=f"<@{item['user']}> ({item['name']})", color=color)
        for q, a in item["answers"]:
            e.add_field(name=trim(q, 250), value=trim(a, 1000), inline=False)
        e.add_field(name="Votes", value=f"Yes {yes}, no {no}. {self.conf_votes(item)} votes decide.", inline=False)
        return e

    def conf_votes(self, item):
        """Votes needed, as stored with the application."""
        return item.get("needed", 2)

    @ap.command(name="start", description="Fill in the application form")
    async def start(self, it: discord.Interaction):
        """Fill in the application form."""
        c = self.conf(it.guild_id)
        if not self.bot.module_on(it.guild_id, "applications") or not c["open"]:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Applications are closed right now."), ephemeral=True)
        if not it.guild.get_channel(c["channel"] or 0):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Applications are not set up yet."), ephemeral=True)
        wait = c["last"].get(str(it.user.id), 0) + c["cooldown_days"] * 86400
        if wait > time.time():
            return await it.response.send_message(f"You applied before. You can apply again <t:{int(wait)}:R>.", ephemeral=True)
        await it.response.send_modal(Form(self, c["questions"]))

    async def submit(self, interaction, answers):
        """Store an application and post it for the vote."""
        guild, c = interaction.guild, self.conf(interaction.guild_id)
        channel = guild.get_channel(c["channel"] or 0)
        if channel is None:
            return await interaction.response.send_message(i18n.say(self.bot, guild, "Applications are not set up yet."), ephemeral=True)
        number = c["next"]
        c["next"] += 1
        now = int(time.time())
        item = {"user": interaction.user.id, "name": str(interaction.user), "answers": answers, "status": "open", "votes": {}, "ts": now, "needed": c["votes"], "message": None}
        c["items"][str(number)] = item
        c["last"][str(interaction.user.id)] = now
        view = discord.ui.View(timeout=None)
        view.add_item(VoteButton("yes", number))
        view.add_item(VoteButton("no", number))
        role = c["staff_role"]
        try:
            msg = await channel.send(f"<@&{role}>" if role else None, embed=self.embed(item, number), view=view, allowed_mentions=discord.AllowedMentions(roles=[discord.Object(role)] if role else []))
        except discord.HTTPException as exc:
            log.warning("application could not be posted: %s", exc)
            c["items"].pop(str(number), None)
            c["last"].pop(str(interaction.user.id), None)
            return await interaction.response.send_message(i18n.say(self.bot, guild, "I could not deliver your application. Try again later."), ephemeral=True)
        item["message"] = [channel.id, msg.id]
        await interaction.response.send_message(i18n.say(self.bot, guild, "Your application was sent. The team will vote on it."), ephemeral=True)

    async def finish(self, guild, number, item, status, by):
        """Close an application: tell the applicant, give the role and update the message."""
        item["status"] = status
        user = guild.get_member(item["user"])
        c = self.conf(guild.id)
        if status == "accepted":
            role = guild.get_role(c["accept_role"] or 0)
            if user is not None and role is not None and role.is_assignable():
                try:
                    await user.add_roles(role, reason=f"Application #{number} accepted")
                except discord.HTTPException as exc:
                    log.warning("application role failed: %s", exc)
        if user is not None:
            try:
                await user.send(i18n.say(self.bot, guild, "{server}: your application was accepted." if status == "accepted" else "{server}: your application was not accepted.", server=guild.name))
            except discord.HTTPException as exc:
                log.info("application answer not delivered: %s", exc)
        channel = guild.get_channel(item["message"][0]) if item.get("message") else None
        if channel is not None:
            try:
                msg = await channel.fetch_message(item["message"][1])
                e = self.embed(item, number)
                e.add_field(name="Decision", value=f"{status} ({by})", inline=False)
                await msg.edit(embed=e, view=None)
            except discord.HTTPException as exc:
                log.info("application message not updated: %s", exc)

    async def cast(self, interaction, vote, number):
        """Register the vote of a team member."""
        guild = interaction.guild
        c = self.conf(guild.id)
        item = c["items"].get(str(number))
        if not self.bot.module_on(guild.id, "applications") or not item or item["status"] != "open":
            return await interaction.response.send_message(i18n.say(self.bot, guild, "This application was already decided."), ephemeral=True)
        member = interaction.user
        staff = guild.get_role(c["staff_role"] or 0)
        if member.id == item["user"] or not (member.guild_permissions.manage_guild or (staff is not None and staff in member.roles)):
            return await interaction.response.send_message(i18n.say(self.bot, guild, "You cannot vote on this application."), ephemeral=True)
        item["votes"][str(member.id)] = vote
        result = outcome(item["votes"], item.get("needed", c["votes"]))
        if result:
            await interaction.response.defer()
            return await self.finish(guild, number, item, result, "by vote")
        await interaction.response.edit_message(embed=self.embed(item, number))

    @ap.command(name="setup", description="Channel, team role, reward role and number of votes")
    @app_commands.describe(channel="Channel where applications arrive", staff_role="Role that votes", accept_role="Role for accepted applicants", votes="Votes that decide", cooldown_days="Days before a new application", open="Accept new applications")
    async def setup(
        self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None, staff_role: Optional[discord.Role] = None, accept_role: Optional[discord.Role] = None,
        votes: Optional[app_commands.Range[int, 1, 20]] = None, cooldown_days: Optional[app_commands.Range[int, 0, 365]] = None, open: Optional[bool] = None,
    ):
        """Channel, team role, reward role and number of votes."""
        if not await require(it):
            return
        c = self.conf(it.guild_id)
        if channel is not None:
            c["channel"] = channel.id
        if staff_role is not None:
            c["staff_role"] = staff_role.id
        if accept_role is not None:
            if accept_role.is_default() or accept_role.managed or not accept_role.is_assignable():
                return await it.response.send_message(i18n.say(it.client, it.guild, "I cannot give that role. Move my role above it or choose another one."), ephemeral=True)
            c["accept_role"] = accept_role.id
        for key, value in (("votes", votes), ("cooldown_days", cooldown_days), ("open", open)):
            if value is not None:
                c[key] = value
        self.bot.cfg(it.guild_id)["modules"]["applications"] = True
        await it.response.send_message(f"Applications are on. Channel {'<#' + str(c['channel']) + '>' if c['channel'] else 'not set'}, {c['votes']} votes decide, {'open' if c['open'] else 'closed'}.", ephemeral=True)

    @ap.command(name="question", description="Add, change or remove a question of the form")
    @app_commands.describe(action="What to do", text="Question text (at most 45 characters are shown)", number="Number of the question for change and remove")
    async def question(self, it: discord.Interaction, action: Literal["add", "change", "remove", "list"], text: Optional[app_commands.Range[str, 3, 200]] = None, number: Optional[app_commands.Range[int, 1, 5]] = None):
        """Add, change or remove a question of the form."""
        if not await require(it):
            return
        qs = self.conf(it.guild_id)["questions"]
        if action == "add":
            if not text or len(qs) >= MAX_QUESTIONS:
                return await it.response.send_message(f"Give a text. At most {MAX_QUESTIONS} questions fit in a form.", ephemeral=True)
            qs.append(text)
        elif action in ("change", "remove"):
            if not number or number > len(qs) or (action == "change" and not text):
                return await it.response.send_message("Give the number of an existing question" + (" and the new text." if action == "change" else "."), ephemeral=True)
            if action == "change":
                qs[number - 1] = text
            else:
                qs.pop(number - 1)
        await it.response.send_message("\n".join(f"{i}. {q}" for i, q in enumerate(qs, 1)) or "No questions.", ephemeral=True)

    @ap.command(name="list", description="Show open applications")
    async def list_cmd(self, it: discord.Interaction):
        """Show open applications."""
        if not await require(it):
            return
        items = self.conf(it.guild_id)["items"]
        lines = [f"#{n} <@{i['user']}> <t:{i['ts']}:R> yes {tally(i['votes'])[0]}, no {tally(i['votes'])[1]}" for n, i in items.items() if i["status"] == "open"]
        await it.response.send_message("\n".join(lines[:25]) or "No open applications.", ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @ap.command(name="decide", description="Decide an application without waiting for the votes")
    async def decide(self, it: discord.Interaction, number: int, decision: Literal["accept", "deny"]):
        """Decide an application without waiting for the votes."""
        if not await require(it):
            return
        item = self.conf(it.guild_id)["items"].get(str(number))
        if not item or item["status"] != "open":
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no open application with that number."), ephemeral=True)
        await it.response.defer(ephemeral=True)
        await self.finish(it.guild, number, item, "accepted" if decision == "accept" else "denied", str(it.user))
        await it.followup.send("Done.")


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Applications(bot))
