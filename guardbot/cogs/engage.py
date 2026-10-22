"""Polls, giveaways and suggestions."""

import logging
import random
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from .. import i18n
from ..utils import AdminGroup, emb, parse_duration

log = logging.getLogger(__name__)


def vlist(v):
    """Return a stored vote as a list so old single votes and multiple votes work the same."""
    return v if isinstance(v, list) else [v]


def poll_embed(p, closed=False):
    """Build the embed of a poll with bars and counts."""
    total = len(p["votes"])
    counts = [0] * len(p["opts"])
    for v in p["votes"].values():
        for idx in vlist(v):
            if 0 <= idx < len(counts):
                counts[idx] += 1
    lines = []
    for i, name in enumerate(p["opts"]):
        pct = counts[i] * 100 // total if total else 0
        lines.append(f"{name}\n[{'#' * (pct // 10)}{'-' * (10 - pct // 10)}] {pct}% ({counts[i]})")
    e = emb(("Poll closed: " if closed else "Poll: ") + p["q"], "\n\n".join(lines), discord.Color.dark_grey() if closed else discord.Color.blurple())
    e.add_field(name="Voters", value=str(total))
    if p.get("multi"):
        e.add_field(name="Mode", value="multiple choice")
    if p["end"] and not closed:
        e.add_field(name="Ends", value=f"<t:{p['end']}:R>")
    return e


class PollVote(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:poll:(?P<id>\d+):(?P<idx>\d+)"):
    """Persistent button that votes for one poll option."""
    def __init__(self, pid, idx, label="Vote"):
        """Create the button for one poll option."""
        super().__init__(discord.ui.Button(label=label[:80], style=discord.ButtonStyle.secondary, custom_id=f"gb:poll:{pid}:{idx}"))
        self.pid, self.idx = pid, idx

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls(int(match["id"]), int(match["idx"]), item.label)

    async def callback(self, interaction):
        """Toggle the vote of the user for this option and refresh the poll."""
        bot = interaction.client
        p = bot.cfg(interaction.guild_id)["polls"]["items"].get(str(self.pid))
        if not p or p["closed"] or not bot.module_on(interaction.guild_id, "polls"):
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This poll is closed."), ephemeral=True)
        uid = str(interaction.user.id)
        mine = vlist(p["votes"].get(uid, []))
        if p.get("multi"):
            mine = [i for i in mine if i != self.idx] if self.idx in mine else mine + [self.idx]
        else:
            mine = [] if mine == [self.idx] else [self.idx]
        if mine:
            p["votes"][uid] = mine
        else:
            p["votes"].pop(uid, None)
        await interaction.response.edit_message(embed=poll_embed(p))


class GiveawayJoin(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:gw:(?P<id>\d+)"):
    """Persistent button that joins or leaves a giveaway."""
    def __init__(self, gid):
        """Create the join button of a giveaway."""
        super().__init__(discord.ui.Button(label="Join", style=discord.ButtonStyle.success, custom_id=f"gb:gw:{gid}"))
        self.gid = gid

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls(int(match["id"]))

    async def callback(self, interaction):
        """Let the user join or leave the giveaway if they have the required role."""
        bot = interaction.client
        g = bot.cfg(interaction.guild_id)["giveaways"]["items"].get(str(self.gid))
        if not g or g["ended"] or not bot.module_on(interaction.guild_id, "giveaways"):
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This giveaway has ended."), ephemeral=True)
        if g["role"] and g["role"] not in {r.id for r in interaction.user.roles}:
            return await interaction.response.send_message(f"You need the <@&{g['role']}> role to join.", ephemeral=True)
        uid = interaction.user.id
        if uid in g["entries"]:
            g["entries"].remove(uid)
            text = "You left the giveaway."
        else:
            g["entries"].append(uid)
            text = "You joined the giveaway. Good luck."
        await interaction.response.send_message(text, ephemeral=True)


def giveaway_embed(g, ended=False, winners=None):
    """Build the embed of a giveaway, with the result once it has ended."""
    e = emb(f"Giveaway: {g['prize']}", color=discord.Color.dark_grey() if ended else discord.Color.gold())
    e.description = f"Winners: {g['winners']}\nHosted by <@{g['host']}>"
    if g["role"]:
        e.description += f"\nRequired role: <@&{g['role']}>"
    if ended:
        e.add_field(name="Result", value=" ".join(f"<@{w}>" for w in winners) if winners else "No valid entries.")
    else:
        e.add_field(name="Ends", value=f"<t:{g['end']}:R>")
    e.add_field(name="Entries", value=str(len(g["entries"])))
    return e


class Engage(commands.Cog):
    """Polls, giveaways and suggestions."""
    poll = app_commands.Group(name="poll", description="Polls", default_permissions=discord.Permissions(manage_messages=True), guild_only=True)
    gw = app_commands.Group(name="giveaway", description="Giveaways", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    sg = app_commands.Group(name="suggestion", description="Review suggestions", guild_only=True)
    ss = AdminGroup(name="setup", description="Configure suggestions", parent=sg)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot
        bot.add_dynamic_items(PollVote, GiveawayJoin)

    async def cog_load(self):
        """Start the background loop of this cog."""
        self.tick.start()

    async def cog_unload(self):
        """Stop the background loop of this cog."""
        self.tick.cancel()

    @tasks.loop(seconds=20)
    async def tick(self):
        """Close polls and finish giveaways whose time is over."""
        now = int(time.time())
        try:
            for guild in self.bot.guilds:
                g = self.bot.cfg(guild.id)
                for pid, p in list(g["polls"]["items"].items()):
                    if not p["closed"] and p["end"] and p["end"] <= now:
                        await self.close_poll(guild, pid)
                for gid, gw in list(g["giveaways"]["items"].items()):
                    if not gw["ended"] and gw["end"] <= now:
                        await self.finish_giveaway(guild, gid)
        except Exception:
            log.exception("poll and giveaway loop failed")

    @tick.before_loop
    async def _wait(self):
        """Wait until the bot is connected before the loop starts."""
        await self.bot.wait_until_ready()

    async def message_of(self, guild, item):
        """Fetch the message of a poll or giveaway, or None if it is gone."""
        ch = guild.get_channel(item["channel"])
        if not ch:
            return None
        try:
            return await ch.fetch_message(item["msg"])
        except discord.HTTPException:
            return None

    async def close_poll(self, guild, pid):
        """Close a poll and show the final result. Returns False if it was not open."""
        p = self.bot.cfg(guild.id)["polls"]["items"].get(str(pid))
        if not p or p["closed"]:
            return False
        p["closed"] = True
        m = await self.message_of(guild, p)
        if m:
            await m.edit(embed=poll_embed(p, closed=True), view=None)
        return True

    async def finish_giveaway(self, guild, gid, reroll=False):
        """Draw the winners, update the message and announce them. Returns the winner IDs."""
        gw = self.bot.cfg(guild.id)["giveaways"]["items"].get(str(gid))
        if not gw or (gw["ended"] and not reroll):
            return None
        pool = [u for u in gw["entries"] if guild.get_member(u)]
        winners = random.sample(pool, min(gw["winners"], len(pool)))
        gw["ended"], gw["result"] = True, winners
        m = await self.message_of(guild, gw)
        if m:
            await m.edit(embed=giveaway_embed(gw, True, winners), view=None)
            text = ("Congratulations " + " ".join(f"<@{w}>" for w in winners) + f", you won **{gw['prize']}**!") if winners else f"No valid entries for **{gw['prize']}**."
            await m.reply(text, allowed_mentions=discord.AllowedMentions(users=[discord.Object(w) for w in winners]))
        return winners

    @poll.command(name="create", description="Create a poll with up to 10 options")
    @app_commands.describe(question="Question", options="Options separated by ; (2 to 10)", duration="Optional, for example 1h or 2d", multiple="Allow voting for several options")
    async def poll_create(self, it: discord.Interaction, question: str, options: str, duration: Optional[str] = None, multiple: bool = False):
        """Create a poll with up to 10 options."""
        opts = [o.strip() for o in options.split(";") if o.strip()]
        if not 2 <= len(opts) <= 10:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Provide 2 to 10 options separated by ;"), ephemeral=True)
        secs = parse_duration(duration) if duration else None
        if duration and not secs:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Invalid duration. Examples: 30m, 2h, 1d"), ephemeral=True)
        pl = self.bot.cfg(it.guild_id)["polls"]
        pid = pl["next"]
        pl["next"] += 1
        p = {"q": question, "opts": opts, "votes": {}, "end": int(time.time()) + secs if secs else None, "closed": False, "multi": multiple, "channel": it.channel_id, "msg": 0}
        view = discord.ui.View(timeout=None)
        for i, o in enumerate(opts):
            view.add_item(PollVote(pid, i, o))
        await it.response.send_message(embed=poll_embed(p), view=view)
        p["msg"] = (await it.original_response()).id
        pl["items"][str(pid)] = p

    @poll.command(name="end", description="End a poll now")
    async def poll_end(self, it: discord.Interaction, poll_id: int):
        """End a poll now."""
        ok = await self.close_poll(it.guild, poll_id)
        await it.response.send_message("Poll closed." if ok else "No open poll with that ID.", ephemeral=True)

    @poll.command(name="list", description="List open polls")
    async def poll_list(self, it: discord.Interaction):
        """List open polls."""
        lines = [f"#{k}: {p['q']}" for k, p in self.bot.cfg(it.guild_id)["polls"]["items"].items() if not p["closed"]]
        await it.response.send_message("\n".join(lines) or "No open polls.", ephemeral=True)

    @gw.command(name="start", description="Start a giveaway")
    @app_commands.describe(prize="Prize", duration="For example 1h, 2d", winners="Number of winners", role="Role required to join")
    async def gw_start(self, it: discord.Interaction, prize: str, duration: str, winners: app_commands.Range[int, 1, 20] = 1, role: Optional[discord.Role] = None):
        """Start a giveaway."""
        secs = parse_duration(duration)
        if not secs:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Invalid duration. Examples: 30m, 2h, 1d"), ephemeral=True)
        gl = self.bot.cfg(it.guild_id)["giveaways"]
        gid = gl["next"]
        gl["next"] += 1
        gw = {"prize": prize, "winners": winners, "host": it.user.id, "role": role.id if role else None, "end": int(time.time()) + secs, "entries": [], "ended": False, "channel": it.channel_id, "msg": 0}
        view = discord.ui.View(timeout=None)
        view.add_item(GiveawayJoin(gid))
        await it.response.send_message(embed=giveaway_embed(gw), view=view)
        gw["msg"] = (await it.original_response()).id
        gl["items"][str(gid)] = gw

    @gw.command(name="end", description="End a giveaway now")
    async def gw_end(self, it: discord.Interaction, giveaway_id: int):
        """End a giveaway now."""
        await it.response.defer(ephemeral=True)
        w = await self.finish_giveaway(it.guild, giveaway_id)
        await it.followup.send("Giveaway ended." if w is not None else "No running giveaway with that ID.")

    @gw.command(name="reroll", description="Draw new winners")
    async def gw_reroll(self, it: discord.Interaction, giveaway_id: int):
        """Draw new winners."""
        await it.response.defer(ephemeral=True)
        gw = self.bot.cfg(it.guild_id)["giveaways"]["items"].get(str(giveaway_id))
        if not gw or not gw["ended"]:
            return await it.followup.send(i18n.say(it.client, it.guild, "That giveaway has not ended."))
        await self.finish_giveaway(it.guild, giveaway_id, reroll=True)
        await it.followup.send(i18n.say(it.client, it.guild, "New winners drawn."))

    @gw.command(name="cancel", description="Cancel a giveaway without drawing winners")
    async def gw_cancel(self, it: discord.Interaction, giveaway_id: int):
        """Cancel a giveaway without drawing winners."""
        gw = self.bot.cfg(it.guild_id)["giveaways"]["items"].get(str(giveaway_id))
        if not gw or gw["ended"]:
            return await it.response.send_message(i18n.say(it.client, it.guild, "No running giveaway with that ID."), ephemeral=True)
        gw["ended"], gw["result"] = True, []
        msg = await self.message_of(it.guild, gw)
        if msg:
            try:
                await msg.edit(embed=emb(f"Giveaway cancelled: {gw['prize']}", color=discord.Color.dark_grey()), view=None)
            except discord.HTTPException as exc:
                log.warning("could not update the cancelled giveaway %s: %s", giveaway_id, exc)
        await it.response.send_message(i18n.say(it.client, it.guild, "Giveaway cancelled."), ephemeral=True)

    @gw.command(name="edit", description="Change the prize, the number of winners or the end time")
    @app_commands.describe(giveaway_id="Giveaway ID", prize="New prize", winners="New number of winners", extend="Add time, for example 1h or 1d")
    async def gw_edit(self, it: discord.Interaction, giveaway_id: int, prize: Optional[str] = None, winners: Optional[app_commands.Range[int, 1, 20]] = None, extend: Optional[str] = None):
        """Change the prize, the number of winners or the end time."""
        gw = self.bot.cfg(it.guild_id)["giveaways"]["items"].get(str(giveaway_id))
        if not gw or gw["ended"]:
            return await it.response.send_message(i18n.say(it.client, it.guild, "No running giveaway with that ID."), ephemeral=True)
        if extend:
            secs = parse_duration(extend)
            if not secs:
                return await it.response.send_message(i18n.say(it.client, it.guild, "Invalid duration. Examples: 30m, 2h, 1d"), ephemeral=True)
            gw["end"] += secs
        if prize:
            gw["prize"] = prize
        if winners:
            gw["winners"] = winners
        msg = await self.message_of(it.guild, gw)
        if msg:
            try:
                await msg.edit(embed=giveaway_embed(gw))
            except discord.HTTPException as exc:
                log.warning("could not update giveaway %s: %s", giveaway_id, exc)
        await it.response.send_message(i18n.say(it.client, it.guild, "Giveaway updated."), ephemeral=True)

    @gw.command(name="list", description="List running giveaways")
    async def gw_list(self, it: discord.Interaction):
        """List running giveaways."""
        lines = [f"#{k}: {g['prize']} (ends <t:{g['end']}:R>, {len(g['entries'])} entries)" for k, g in self.bot.cfg(it.guild_id)["giveaways"]["items"].items() if not g["ended"]]
        await it.response.send_message("\n".join(lines) or "No running giveaways.", ephemeral=True)

    @commands.hybrid_command(name="suggest", description="Post a suggestion")
    @app_commands.describe(text="Your suggestion")
    async def suggest_cmd(self, ctx, *, text: str):
        """Post a suggestion."""
        s = self.bot.cfg(ctx.guild.id)["suggestions"]
        ch = ctx.guild.get_channel(s["channel"]) if s["channel"] else None
        if not ch:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Suggestions are not set up yet."), ephemeral=True)
        sid = s["next"]
        s["next"] += 1
        e = emb(f"Suggestion #{sid}", text[:3500], discord.Color.blurple(), ctx.author)
        e.add_field(name="Status", value="Open")
        msg = await ch.send(embed=e)
        for emoji in ("\U0001F44D", "\U0001F44E"):
            await msg.add_reaction(emoji)
        s["items"][str(sid)] = {"msg": msg.id, "author": ctx.author.id, "text": text[:3500], "status": "Open"}
        await ctx.send(f"Suggestion #{sid} posted in {ch.mention}.", ephemeral=True)

    @sg.command(name="status", description="Set the status of a suggestion")
    async def sg_status(self, it: discord.Interaction, suggestion_id: int, status: Literal["approved", "denied", "considering", "implemented"], reason: Optional[str] = None):
        """Set the status of a suggestion."""
        s = self.bot.cfg(it.guild_id)["suggestions"]
        allowed = it.user.guild_permissions.manage_guild or (s["review_role"] and s["review_role"] in {r.id for r in it.user.roles})
        if not allowed:
            return await it.response.send_message(i18n.say(it.client, it.guild, "You cannot review suggestions."), ephemeral=True)
        item = s["items"].get(str(suggestion_id))
        ch = it.guild.get_channel(s["channel"]) if s["channel"] else None
        if not item or not ch:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Suggestion not found."), ephemeral=True)
        colors = {"approved": discord.Color.green(), "denied": discord.Color.red(), "considering": discord.Color.orange(), "implemented": discord.Color.teal()}
        author = it.guild.get_member(item["author"])
        e = emb(f"Suggestion #{suggestion_id}", item["text"], colors[status], author)
        e.add_field(name="Status", value=status.capitalize())
        if reason:
            e.add_field(name="Reason", value=reason[:1000], inline=False)
        try:
            msg = await ch.fetch_message(item["msg"])
            await msg.edit(embed=e)
        except discord.HTTPException:
            return await it.response.send_message(i18n.say(it.client, it.guild, "The suggestion message is gone."), ephemeral=True)
        item["status"] = status
        await it.response.send_message(f"Suggestion #{suggestion_id}: {status}.", ephemeral=True)

    @ss.command(name="set", description="Set the suggestion channel and review role")
    async def ss_set(self, it: discord.Interaction, channel: discord.TextChannel, review_role: Optional[discord.Role] = None):
        """Set the suggestion channel and review role."""
        g = self.bot.cfg(it.guild_id)
        g["suggestions"]["channel"] = channel.id
        if review_role:
            g["suggestions"]["review_role"] = review_role.id
        g["modules"]["suggestions"] = True
        await it.response.send_message(i18n.say(it.client, it.guild, "Saved."), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Engage(bot))
