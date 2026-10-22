"""Team: statistics of the moderators, a weekly report, absence and duty roster."""

import logging
import time
from datetime import datetime, timezone
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from .. import i18n
from ..utils import emb, fmt_duration, parse_duration, require

log = logging.getLogger(__name__)

KINDS = ("cases", "tickets", "reports", "appeals", "modmail")
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
FEATURES = ("tickets", "modmail", "reports")


def cases_by_mod(cases, since, until=None):
    """Count the cases a moderator created in a time range as {user id: {type: count}}. Automatic actions of the bot itself are skipped."""
    out = {}
    for c in cases:
        if c["ts"] < since or (until and c["ts"] > until) or c["extra"].get("auto"):
            continue
        out.setdefault(c["mod"], {})
        out[c["mod"]][c["type"]] = out[c["mod"]].get(c["type"], 0) + 1
    return out


def inactive_members(roster, stats, days, now):
    """Roster members without any counted action for this many days. Returns [(user id, last action or 0)] oldest first."""
    cutoff = now - days * 86400
    out = []
    for uid in roster:
        last = stats.get(str(uid), {}).get("last", 0)
        if last < cutoff:
            out.append((uid, last))
    return sorted(out, key=lambda x: x[1])


def pick_available(candidates, away, assigned, now):
    """The staff member who was given a task the longest time ago among those who are not away. Returns an ID or None."""
    free = [uid for uid in candidates if not (str(uid) in away and (away[str(uid)]["until"] == 0 or away[str(uid)]["until"] > now))]
    if not free:
        return None
    return min(free, key=lambda uid: assigned.get(str(uid), 0))


def due(now_dt, day, hour, last, now):
    """True if the weekly report is due: the right weekday and hour passed and not sent in the last five days."""
    return now_dt.weekday() == day and now_dt.hour >= hour and now - last > 5 * 86400


class Team(commands.Cog):
    """Team statistics, weekly report and duty roster."""

    ts = app_commands.Group(name="teamstats", description="What your moderators did", guild_only=True)
    wk = app_commands.Group(name="weekly", description="Weekly summary for the team", guild_only=True)
    du = app_commands.Group(name="duty", description="Absence and duty roster of the team", guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    async def cog_load(self):
        """Start the loops."""
        self.loop.start()

    async def cog_unload(self):
        """Stop the loops."""
        self.loop.cancel()

    def conf(self, gid):
        """Return the team settings of a server."""
        return self.bot.cfg(gid)["team"]

    # counting ---------------------------------------------------------------

    def count(self, guild, uid, kind, seconds=None):
        """Count one handled item for a staff member."""
        if not self.bot.module_on(guild.id, "team"):
            return
        s = self.conf(guild.id)["stats"].setdefault(str(uid), {})
        s[kind] = s.get(kind, 0) + 1
        s["last"] = int(time.time())
        if seconds is not None and seconds >= 0:
            s["secs"] = s.get("secs", 0) + int(seconds)
            s["handled"] = s.get("handled", 0) + 1

    def event(self, guild, name, amount=1):
        """Count an event for the weekly report."""
        if self.bot.module_on(guild.id, "team"):
            week = self.conf(guild.id)["week"]
            week[name] = week.get(name, 0) + amount

    # roster and routing -------------------------------------------------------

    def roster(self, guild):
        """The staff members: everyone with one of the roster roles, or with the staff roles of the gulag, tickets or mod-mail."""
        c = self.bot.cfg(guild.id)
        ids = set(c["team"]["roster_roles"]) or {r for r in (c["jail"]["staff_role"], c["tickets"]["support_role"], c["modmail"]["staff_role"]) if r}
        return [m for m in guild.members if not m.bot and any(r.id in ids for r in m.roles)]

    def is_away(self, guild, uid, now=None):
        """True if a member reported absence that has not ended."""
        entry = self.conf(guild.id)["away"].get(str(uid))
        now = now or time.time()
        return bool(entry) and (entry["until"] == 0 or entry["until"] > now)

    def ping(self, guild, feature, role_id):
        """The mention for a new ticket, report or mod-mail as (text, user ids, role ids). With routing on, one available member of the role is pinged, otherwise the whole role."""
        c = self.conf(guild.id)
        role = guild.get_role(role_id or 0)
        if role is None:
            return "", [], []
        if feature in c["route"] and self.bot.module_on(guild.id, "duty"):
            uid = pick_available([m.id for m in role.members if not m.bot], c["away"], c["assigned"], time.time())
            if uid is not None:
                c["assigned"][str(uid)] = int(time.time())
                return f"<@{uid}>", [uid], []
        return role.mention, [], [role.id]

    @tasks.loop(minutes=1)
    async def loop(self):
        """End absences that are over and send the weekly report."""
        now = time.time()
        now_dt = datetime.now(timezone.utc)
        for guild in list(self.bot.guilds):
            c = self.conf(guild.id)
            for uid, entry in list(c["away"].items()):
                if entry["until"] and entry["until"] <= now:
                    c["away"].pop(uid, None)
            if not self.bot.module_on(guild.id, "team") or not c["report_channel"]:
                continue
            if due(now_dt, c["report_day"], c["report_hour"], c["last_report"], now):
                c["last_report"] = int(now)
                try:
                    await self.send_report(guild)
                except Exception:  # one server must not stop the others
                    log.exception("weekly report of %s failed", guild.id)

    @loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected."""
        await self.bot.wait_until_ready()

    # report -----------------------------------------------------------------

    def report_embed(self, guild, days=7):
        """Build the summary of the last days."""
        gid, now = guild.id, time.time()
        since = now - days * 86400
        cases = [c for c in self.bot.store.cases(gid) if c["ts"] >= since]
        by_type = {}
        for c in cases:
            by_type[c["type"]] = by_type.get(c["type"], 0) + 1
        mods = cases_by_mod(self.bot.store.cases(gid), since)
        week = self.conf(gid)["week"]
        t = self.bot.cfg(gid)["tickets"]
        act = self.bot.cfg(gid)["activity"]["days"]
        keys = sorted(act)[-days:]
        e = emb(f"Report of the last {days} days", color=discord.Color.blurple())
        e.add_field(name="Members", value=f"Joined {sum(act[k].get('joins', 0) for k in keys)}, left {sum(act[k].get('leaves', 0) for k in keys)}, now {guild.member_count}" if keys else f"Now {guild.member_count}. Switch on the activity module for joins and leaves.", inline=False)
        e.add_field(name="Moderation", value=", ".join(f"{n} {k}" for k, n in sorted(by_type.items(), key=lambda kv: -kv[1])) or "No cases", inline=False)
        top = sorted(mods.items(), key=lambda kv: -sum(kv[1].values()))[:3]
        e.add_field(name="Most active moderators", value="\n".join(f"<@{u}>: {sum(v.values())} cases" for u, v in top) or "nobody", inline=False)
        e.add_field(name="Support", value=f"Tickets opened {week.get('tickets_opened', 0)}, closed {week.get('tickets_closed', 0)}, open now {len(t['open'])}. Reports {week.get('reports', 0)}, appeals {week.get('appeals', 0)}.", inline=False)
        e.add_field(name="Security", value=f"Raid alerts {week.get('raids', 0)}, anti-scam removals so far {self.bot.cfg(gid)['antiscam']['hits']}, watched members {len(self.bot.cfg(gid)['watchlist']['items'])}", inline=False)
        away = [m for m in self.roster(guild) if self.is_away(guild, m.id)]
        if away:
            e.add_field(name="Away", value=" ".join(m.mention for m in away)[:500], inline=False)
        return e

    async def send_report(self, guild, channel=None):
        """Send the report and start a new week."""
        channel = channel or guild.get_channel(self.conf(guild.id)["report_channel"] or 0)
        if channel is None:
            return False
        await channel.send(embed=self.report_embed(guild), allowed_mentions=discord.AllowedMentions.none())
        self.conf(guild.id)["week"] = {}
        return True

    @wk.command(name="setup", description="Where and when the weekly report is sent")
    @app_commands.describe(channel="Channel for the report", day="Weekday", hour="Hour (UTC)")
    async def wk_setup(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None, day: Optional[Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]] = None, hour: Optional[app_commands.Range[int, 0, 23]] = None):
        """Where and when the weekly report is sent."""
        if not await require(it):
            return
        c = self.conf(it.guild_id)
        if channel is not None:
            c["report_channel"] = channel.id
        if day is not None:
            c["report_day"] = DAYS.index(day)
        if hour is not None:
            c["report_hour"] = hour
        self.bot.cfg(it.guild_id)["modules"]["team"] = True
        ch = f"<#{c['report_channel']}>" if c["report_channel"] else "not set"
        await it.response.send_message(f"Weekly report: {DAYS[c['report_day']]} at {c['report_hour']}:00 UTC in {ch}.", ephemeral=True)

    @wk.command(name="now", description="Send the report now")
    async def wk_now(self, it: discord.Interaction, days: app_commands.Range[int, 1, 90] = 7):
        """Show the report for the last days to you only."""
        await it.response.send_message(embed=self.report_embed(it.guild, days), ephemeral=True)

    # statistics ---------------------------------------------------------------

    @ts.command(name="overview", description="Cases per moderator in the last days")
    async def ts_overview(self, it: discord.Interaction, days: app_commands.Range[int, 1, 365] = 30):
        """Cases per moderator in the last days."""
        mods = cases_by_mod(self.bot.store.cases(it.guild_id), time.time() - days * 86400)
        stats = self.conf(it.guild_id)["stats"]
        lines = []
        for uid, kinds in sorted(mods.items(), key=lambda kv: -sum(kv[1].values()))[:20]:
            s = stats.get(str(uid), {})
            avg = f", average {fmt_duration(s['secs'] // s['handled'])} per ticket, report or appeal" if s.get("handled") else ""
            lines.append(f"<@{uid}>: {sum(kinds.values())} cases ({', '.join(f'{n} {k}' for k, n in kinds.items())}), tickets {s.get('tickets', 0)}, reports {s.get('reports', 0)}, appeals {s.get('appeals', 0)}{avg}")
        await it.response.send_message(embed=emb(f"Moderators, last {days} days", "\n".join(lines) or "No cases in this time.", discord.Color.blurple()), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @ts.command(name="member", description="Everything counted for one moderator")
    async def ts_member(self, it: discord.Interaction, user: discord.User):
        """Everything counted for one moderator."""
        s = self.conf(it.guild_id)["stats"].get(str(user.id))
        if not s:
            return await it.response.send_message("Nothing was counted for this person yet.", ephemeral=True)
        avg = f"\nAverage time for tickets, reports and appeals: {fmt_duration(s['secs'] // s['handled'])}" if s.get("handled") else ""
        text = "\n".join(f"{k}: {s.get(k, 0)}" for k in KINDS) + f"\nLast action <t:{s.get('last', 0)}:R>" + avg
        await it.response.send_message(embed=emb(f"Statistics of {user}", text, discord.Color.blurple()), ephemeral=True)

    @ts.command(name="inactive", description="Moderators without any action for a while")
    async def ts_inactive(self, it: discord.Interaction, days: Optional[app_commands.Range[int, 1, 365]] = None):
        """Moderators without any action for a while."""
        c = self.conf(it.guild_id)
        days = days or c["inactive_days"]
        roster = self.roster(it.guild)
        if not roster:
            return await it.response.send_message("No staff members found. Set the staff roles with /admin setup or /team duty roster.", ephemeral=True)
        out = inactive_members([m.id for m in roster], c["stats"], days, time.time())
        lines = [f"<@{uid}>: " + (f"last action <t:{last}:R>" if last else "nothing counted yet") + (", away" if self.is_away(it.guild, uid) else "") for uid, last in out[:25]]
        await it.response.send_message(embed=emb(f"Inactive for {days} days", "\n".join(lines) or "Everybody was active.", discord.Color.orange()), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    # duty ------------------------------------------------------------------------

    @du.command(name="away", description="Report that you are away")
    @app_commands.describe(duration="For example 3d or 12h, empty = until you come back", reason="Reason for the team")
    async def du_away(self, it: discord.Interaction, duration: Optional[str] = None, reason: Optional[app_commands.Range[str, 1, 200]] = None):
        """Report that you are away. You get no new tickets, reports or mod-mail while routing is on."""
        if not await require(it, "moderate_members"):
            return
        secs = parse_duration(duration) if duration else None
        if duration and not secs:
            return await it.response.send_message(i18n.say(it.client, it.guild, "I did not understand the duration. Use 30m, 2h or 1d."), ephemeral=True)
        until = int(time.time()) + secs if secs else 0
        self.conf(it.guild_id)["away"][str(it.user.id)] = {"until": until, "reason": reason or "", "ts": int(time.time())}
        self.bot.cfg(it.guild_id)["modules"]["duty"] = True
        await it.response.send_message("You are away" + (f" until <t:{until}:f>." if until else " until you use /team duty back."), ephemeral=True)

    @du.command(name="back", description="Report that you are back")
    async def du_back(self, it: discord.Interaction):
        """Report that you are back."""
        if self.conf(it.guild_id)["away"].pop(str(it.user.id), None) is None:
            return await it.response.send_message("You were not away.", ephemeral=True)
        await it.response.send_message("Welcome back.", ephemeral=True)

    @du.command(name="list", description="Who is available and who is away")
    async def du_list(self, it: discord.Interaction):
        """Who is available and who is away."""
        c = self.conf(it.guild_id)
        free, gone = [], []
        for m in self.roster(it.guild):
            if self.is_away(it.guild, m.id):
                a = c["away"][str(m.id)]
                gone.append(f"{m.mention}" + (f" until <t:{a['until']}:R>" if a["until"] else "") + (f": {a['reason']}" if a["reason"] else ""))
            else:
                free.append(m.mention)
        text = f"Available ({len(free)}): {' '.join(free[:40]) or 'nobody'}\nAway ({len(gone)}):\n" + ("\n".join(gone[:25]) or "nobody")
        await it.response.send_message(text[:1900], ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @du.command(name="route", description="Ping one available person instead of the whole role")
    @app_commands.describe(feature="tickets, mod-mail or reports", enabled="On or off")
    async def du_route(self, it: discord.Interaction, feature: Literal["tickets", "modmail", "reports"], enabled: bool):
        """Ping one available person instead of the whole role. Members who are away are skipped, the tasks go round."""
        if not await require(it):
            return
        route = self.conf(it.guild_id)["route"]
        if enabled and feature not in route:
            route.append(feature)
        elif not enabled and feature in route:
            route.remove(feature)
        self.bot.cfg(it.guild_id)["modules"]["duty"] = True
        await it.response.send_message(f"Routing for {feature} is {'on' if enabled else 'off'}. Routed: {', '.join(route) or 'nothing'}.", ephemeral=True)

    @du.command(name="roster", description="Roles that count as staff for the lists and the routing")
    async def du_roster(self, it: discord.Interaction, role: discord.Role, remove: bool = False):
        """Roles that count as staff for the lists and the routing."""
        if not await require(it):
            return
        lst = self.conf(it.guild_id)["roster_roles"]
        if remove and role.id in lst:
            lst.remove(role.id)
        elif not remove and role.id not in lst:
            lst.append(role.id)
        await it.response.send_message("Staff roles: " + (" ".join(f"<@&{i}>" for i in lst) or "the roles of gulag, tickets and mod-mail"), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Team(bot))
