# Copyright (c) Justyn
import random
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ..utils import emb, fmt_duration, parse_duration


def poll_embed(p, closed=False):
    total = len(p["votes"])
    counts = [0] * len(p["opts"])
    for idx in p["votes"].values():
        counts[idx] += 1
    lines = []
    for i, name in enumerate(p["opts"]):
        pct = counts[i] * 100 // total if total else 0
        lines.append(f"{name}\n[{'#' * (pct // 10)}{'-' * (10 - pct // 10)}] {pct}% ({counts[i]})")
    e = emb(("Poll closed: " if closed else "Poll: ") + p["q"], "\n\n".join(lines), discord.Color.dark_grey() if closed else discord.Color.blurple())
    e.add_field(name="Votes", value=str(total))
    if p["end"] and not closed:
        e.add_field(name="Ends", value=f"<t:{p['end']}:R>")
    return e


class PollVote(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:poll:(?P<id>\d+):(?P<idx>\d+)"):
    def __init__(self, pid, idx, label="Vote"):
        super().__init__(discord.ui.Button(label=label[:80], style=discord.ButtonStyle.secondary, custom_id=f"gb:poll:{pid}:{idx}"))
        self.pid, self.idx = pid, idx

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        return cls(int(match["id"]), int(match["idx"]), item.label)

    async def callback(self, interaction):
        bot = interaction.client
        p = bot.cfg(interaction.guild_id)["polls"]["items"].get(str(self.pid))
        if not p or p["closed"] or not bot.module_on(interaction.guild_id, "polls"):
            return await interaction.response.send_message("This poll is closed.", ephemeral=True)
        uid = str(interaction.user.id)
        if p["votes"].get(uid) == self.idx:
            del p["votes"][uid]
        else:
            p["votes"][uid] = self.idx
        bot.store.mark("config")
        await interaction.response.edit_message(embed=poll_embed(p))


class GiveawayJoin(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:gw:(?P<id>\d+)"):
    def __init__(self, gid):
        super().__init__(discord.ui.Button(label="Join", style=discord.ButtonStyle.success, custom_id=f"gb:gw:{gid}"))
        self.gid = gid

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        return cls(int(match["id"]))

    async def callback(self, interaction):
        bot = interaction.client
        g = bot.cfg(interaction.guild_id)["giveaways"]["items"].get(str(self.gid))
        if not g or g["ended"] or not bot.module_on(interaction.guild_id, "giveaways"):
            return await interaction.response.send_message("This giveaway has ended.", ephemeral=True)
        if g["role"] and g["role"] not in {r.id for r in interaction.user.roles}:
            return await interaction.response.send_message(f"You need the <@&{g['role']}> role to join.", ephemeral=True)
        uid = interaction.user.id
        if uid in g["entries"]:
            g["entries"].remove(uid)
            text = "You left the giveaway."
        else:
            g["entries"].append(uid)
            text = "You joined the giveaway. Good luck."
        bot.store.mark("config")
        await interaction.response.send_message(text, ephemeral=True)


def giveaway_embed(g, ended=False, winners=None):
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
    poll = app_commands.Group(name="poll", description="Polls", default_permissions=discord.Permissions(manage_messages=True), guild_only=True)
    gw = app_commands.Group(name="giveaway", description="Giveaways", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    sg = app_commands.Group(name="suggestion", description="Review suggestions", guild_only=True)
    ss = app_commands.Group(name="suggestionsetup", description="Configure suggestions", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        self.bot = bot
        bot.add_dynamic_items(PollVote, GiveawayJoin)

    async def cog_load(self):
        self.tick.start()

    async def cog_unload(self):
        self.tick.cancel()

    @tasks.loop(seconds=20)
    async def tick(self):
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
        except Exception as exc:
            print("engage loop error:", exc)

    @tick.before_loop
    async def _wait(self):
        await self.bot.wait_until_ready()

    async def message_of(self, guild, item):
        ch = guild.get_channel(item["channel"])
        if not ch:
            return None
        try:
            return await ch.fetch_message(item["msg"])
        except discord.HTTPException:
            return None

    async def close_poll(self, guild, pid):
        p = self.bot.cfg(guild.id)["polls"]["items"].get(str(pid))
        if not p or p["closed"]:
            return False
        p["closed"] = True
        self.bot.store.mark("config")
        m = await self.message_of(guild, p)
        if m:
            await m.edit(embed=poll_embed(p, closed=True), view=None)
        return True

    async def finish_giveaway(self, guild, gid, reroll=False):
        gw = self.bot.cfg(guild.id)["giveaways"]["items"].get(str(gid))
        if not gw or (gw["ended"] and not reroll):
            return None
        pool = [u for u in gw["entries"] if guild.get_member(u)]
        winners = random.sample(pool, min(gw["winners"], len(pool)))
        gw["ended"], gw["result"] = True, winners
        self.bot.store.mark("config")
        m = await self.message_of(guild, gw)
        if m:
            await m.edit(embed=giveaway_embed(gw, True, winners), view=None)
            text = ("Congratulations " + " ".join(f"<@{w}>" for w in winners) + f", you won **{gw['prize']}**!") if winners else f"No valid entries for **{gw['prize']}**."
            await m.reply(text, allowed_mentions=discord.AllowedMentions(users=[discord.Object(w) for w in winners]))
        return winners

    @poll.command(name="create", description="Create a poll with up to 10 options")
    @app_commands.describe(question="Question", options="Options separated by ; (2 to 10)", duration="Optional, for example 1h or 2d")
    async def poll_create(self, it: discord.Interaction, question: str, options: str, duration: Optional[str] = None):
        opts = [o.strip() for o in options.split(";") if o.strip()]
        if not 2 <= len(opts) <= 10:
            return await it.response.send_message("Provide 2 to 10 options separated by ;", ephemeral=True)
        secs = parse_duration(duration) if duration else None
        if duration and not secs:
            return await it.response.send_message("Invalid duration. Examples: 30m, 2h, 1d", ephemeral=True)
        pl = self.bot.cfg(it.guild_id)["polls"]
        pid = pl["next"]
        pl["next"] += 1
        p = {"q": question, "opts": opts, "votes": {}, "end": int(time.time()) + secs if secs else None, "closed": False, "channel": it.channel_id, "msg": 0}
        view = discord.ui.View(timeout=None)
        for i, o in enumerate(opts):
            view.add_item(PollVote(pid, i, o))
        await it.response.send_message(embed=poll_embed(p), view=view)
        p["msg"] = (await it.original_response()).id
        pl["items"][str(pid)] = p
        self.bot.store.mark("config")

    @poll.command(name="end", description="End a poll now")
    async def poll_end(self, it: discord.Interaction, poll_id: int):
        ok = await self.close_poll(it.guild, poll_id)
        await it.response.send_message("Poll closed." if ok else "No open poll with that ID.", ephemeral=True)

    @poll.command(name="list", description="List open polls")
    async def poll_list(self, it: discord.Interaction):
        lines = [f"#{k}: {p['q']}" for k, p in self.bot.cfg(it.guild_id)["polls"]["items"].items() if not p["closed"]]
        await it.response.send_message("\n".join(lines) or "No open polls.", ephemeral=True)

    @gw.command(name="start", description="Start a giveaway")
    @app_commands.describe(prize="Prize", duration="For example 1h, 2d", winners="Number of winners", role="Role required to join")
    async def gw_start(self, it: discord.Interaction, prize: str, duration: str, winners: app_commands.Range[int, 1, 20] = 1, role: Optional[discord.Role] = None):
        secs = parse_duration(duration)
        if not secs:
            return await it.response.send_message("Invalid duration. Examples: 30m, 2h, 1d", ephemeral=True)
        gl = self.bot.cfg(it.guild_id)["giveaways"]
        gid = gl["next"]
        gl["next"] += 1
        gw = {"prize": prize, "winners": winners, "host": it.user.id, "role": role.id if role else None, "end": int(time.time()) + secs, "entries": [], "ended": False, "channel": it.channel_id, "msg": 0}
        view = discord.ui.View(timeout=None)
        view.add_item(GiveawayJoin(gid))
        await it.response.send_message(embed=giveaway_embed(gw), view=view)
        gw["msg"] = (await it.original_response()).id
        gl["items"][str(gid)] = gw
        self.bot.store.mark("config")

    @gw.command(name="end", description="End a giveaway now")
    async def gw_end(self, it: discord.Interaction, giveaway_id: int):
        await it.response.defer(ephemeral=True)
        w = await self.finish_giveaway(it.guild, giveaway_id)
        await it.followup.send("Giveaway ended." if w is not None else "No running giveaway with that ID.")

    @gw.command(name="reroll", description="Draw new winners")
    async def gw_reroll(self, it: discord.Interaction, giveaway_id: int):
        await it.response.defer(ephemeral=True)
        gw = self.bot.cfg(it.guild_id)["giveaways"]["items"].get(str(giveaway_id))
        if not gw or not gw["ended"]:
            return await it.followup.send("That giveaway has not ended.")
        await self.finish_giveaway(it.guild, giveaway_id, reroll=True)
        await it.followup.send("New winners drawn.")

    @gw.command(name="list", description="List running giveaways")
    async def gw_list(self, it: discord.Interaction):
        lines = [f"#{k}: {g['prize']} (ends <t:{g['end']}:R>, {len(g['entries'])} entries)" for k, g in self.bot.cfg(it.guild_id)["giveaways"]["items"].items() if not g["ended"]]
        await it.response.send_message("\n".join(lines) or "No running giveaways.", ephemeral=True)

    @commands.hybrid_command(name="suggest", description="Post a suggestion")
    @app_commands.describe(text="Your suggestion")
    async def suggest_cmd(self, ctx, *, text: str):
        s = self.bot.cfg(ctx.guild.id)["suggestions"]
        ch = ctx.guild.get_channel(s["channel"]) if s["channel"] else None
        if not ch:
            return await ctx.send("Suggestions are not set up yet.", ephemeral=True)
        sid = s["next"]
        s["next"] += 1
        e = emb(f"Suggestion #{sid}", text[:3500], discord.Color.blurple(), ctx.author)
        e.add_field(name="Status", value="Open")
        msg = await ch.send(embed=e)
        for emoji in ("\U0001F44D", "\U0001F44E"):
            await msg.add_reaction(emoji)
        s["items"][str(sid)] = {"msg": msg.id, "author": ctx.author.id, "text": text[:3500], "status": "Open"}
        self.bot.store.mark("config")
        await ctx.send(f"Suggestion #{sid} posted in {ch.mention}.", ephemeral=True)

    @sg.command(name="status", description="Set the status of a suggestion")
    async def sg_status(self, it: discord.Interaction, suggestion_id: int, status: Literal["approved", "denied", "considering", "implemented"], reason: Optional[str] = None):
        s = self.bot.cfg(it.guild_id)["suggestions"]
        allowed = it.user.guild_permissions.manage_guild or (s["review_role"] and s["review_role"] in {r.id for r in it.user.roles})
        if not allowed:
            return await it.response.send_message("You cannot review suggestions.", ephemeral=True)
        item = s["items"].get(str(suggestion_id))
        ch = it.guild.get_channel(s["channel"]) if s["channel"] else None
        if not item or not ch:
            return await it.response.send_message("Suggestion not found.", ephemeral=True)
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
            return await it.response.send_message("The suggestion message is gone.", ephemeral=True)
        item["status"] = status
        self.bot.store.mark("config")
        await it.response.send_message(f"Suggestion #{suggestion_id}: {status}.", ephemeral=True)

    @ss.command(name="set", description="Set the suggestion channel and review role")
    async def ss_set(self, it: discord.Interaction, channel: discord.TextChannel, review_role: Optional[discord.Role] = None):
        g = self.bot.cfg(it.guild_id)
        g["suggestions"]["channel"] = channel.id
        if review_role:
            g["suggestions"]["review_role"] = review_role.id
        g["modules"]["suggestions"] = True
        self.bot.store.mark("config")
        await it.response.send_message("Saved.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Engage(bot))
