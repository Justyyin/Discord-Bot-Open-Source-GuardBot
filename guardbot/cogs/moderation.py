"""Warnings, mutes, kicks, bans, case history and automatic escalation."""

import logging
import time
from datetime import timedelta
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from .. import i18n
from ..utils import emb, fmt_duration, parse_duration, trim
from .modwatch import CASE_KEYS

log = logging.getLogger(__name__)

KINDS = ("warn", "note", "mute", "unmute", "kick", "ban", "unban", "jail", "unjail")
COLORS = {
    "warn": discord.Color.gold(),
    "note": discord.Color.light_grey(),
    "mute": discord.Color.orange(),
    "unmute": discord.Color.green(),
    "kick": discord.Color.dark_orange(),
    "ban": discord.Color.red(),
    "unban": discord.Color.green(),
    "jail": discord.Color.dark_red(),
    "unjail": discord.Color.green(),
}


def filter_cases(cases, uid=None, kind=None, search=None, text=None, mod=None, days=None, now=None):
    """Select cases by user, type, part of the user name, word in the reason, moderator and age."""
    cutoff = (now if now is not None else time.time()) - days * 86400 if days else 0
    return [
        c for c in cases
        if (not uid or c["user"] == uid) and (not kind or c["type"] == kind) and (not search or search.lower() in c["user_name"].lower())
        and (not text or text.lower() in c["reason"].lower()) and (not mod or c["mod"] == mod) and c["ts"] >= cutoff
    ]


def build_timeline(uid, cases, appeals, rec, joined=None, created=None, probation=None):
    """Merge everything stored about a user into one list of (timestamp, text), oldest first. Message content is never stored, so it is not part of this."""
    events = []
    if created:
        events.append((int(created), "Account created"))
    if joined:
        how = ""
        if rec.get("invited_by") or rec.get("invite"):
            how = f" with invite {rec.get('invite') or 'unknown'}" + (f" from <@{rec['invited_by']}>" if rec.get("invited_by") else "")
        events.append((int(joined), "Joined the server" + how))
    if probation:
        events.append((int(probation["ts"]), f"Probation started, {probation.get('ok', 0)} normal messages so far"))
    if rec.get("left_at"):
        events.append((int(rec["left_at"]), "Left the server"))
    for c in cases:
        if c["user"] == uid:
            events.append((c["ts"], f"Case #{c['id']} {c['type']}" + ("" if c["active"] else " (removed)") + f" by <@{c['mod']}>: {trim(c['reason'], 90)}" + (f" (linked to {', '.join('#' + str(i) for i in c['extra']['links'])})" if c["extra"].get("links") else "")))
    for aid, a in appeals.items():
        if a.get("user") == uid:
            events.append((a["ts"], f"Appeal #{aid} {a['status']}: {trim(a['text'], 90)}"))
    return sorted(events, key=lambda e: e[0])


class Moderation(commands.Cog):
    """Cases, warnings and punishments with escalation."""
    esc = app_commands.Group(
        name="escalation",
        description="Automatic punishments for warnings",
        default_permissions=discord.Permissions(manage_guild=True),
        guild_only=True,
    )

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot

    async def add_case(self, guild, kind, user, mod, reason=None, extra=None):
        """Store a moderation case, log it and return it."""
        g = self.bot.cfg(guild.id)
        g["case_counter"] += 1
        case = {
            "id": g["case_counter"],
            "type": kind,
            "user": user.id,
            "user_name": str(user),
            "mod": mod.id,
            "mod_name": str(mod),
            "reason": reason or "No reason given",
            "ts": int(time.time()),
            "extra": extra or {},
            "active": True,
        }
        self.bot.store.cases(guild.id).append(case)
        e = emb(f"Case #{case['id']} | {kind}", color=COLORS.get(kind), user=user)
        e.add_field(name="User", value=f"{user.mention} ({user.id})")
        e.add_field(name="Moderator", value=f"{mod.mention} ({mod.id})")
        e.add_field(name="Reason", value=trim(case["reason"]), inline=False)
        self.bot.log(guild, "moderation", e)
        if not (extra or {}).get("auto") and mod.id != guild.me.id:
            self.bot.team_count(guild, mod.id, "cases")
        watch = self.bot.get_cog("ModWatch")
        if watch and kind in CASE_KEYS:
            await watch.count(guild, mod, CASE_KEYS[kind])
        return case

    def target_error(self, guild, mod, target):
        """Return why the moderator may not act on the target, or None if it is allowed."""
        if target.id == guild.owner_id:
            return "You cannot do this to the server owner."
        if target.id == self.bot.user.id:
            return "I will not do that to myself."
        if target.id == mod.id:
            return "You cannot do this to yourself."
        if isinstance(target, discord.Member):
            if mod.id != guild.owner_id and target.top_role >= mod.top_role:
                return "That member has an equal or higher role than you."
            if target.top_role >= guild.me.top_role:
                return "My role is not high enough for that member."
        return None

    async def notify(self, guild, user, text):
        """Send the user a direct message about a punishment if that is enabled."""
        if self.bot.cfg(guild.id)["mod"]["dm_user"]:
            try:
                await user.send(f"{guild.name}: {text}")
            except discord.Forbidden:
                log.info("cannot DM %s, direct messages are closed", user)
            except discord.HTTPException as exc:
                log.warning("DM to %s failed: %s", user, exc)

    def active_warns(self, gid, uid):
        """Count the warnings of a user that are not removed or expired."""
        days = self.bot.cfg(gid)["mod"]["warn_expiry_days"]
        cutoff = time.time() - days * 86400 if days else 0
        return sum(1 for c in self.bot.store.cases(gid) if c["type"] == "warn" and c["user"] == uid and c["active"] and c["ts"] >= cutoff)

    async def warn_member(self, guild, member, mod, reason, extra=None):
        """Create a warning, tell the member and run the escalation steps."""
        case = await self.add_case(guild, "warn", member, mod, reason, extra)
        count = self.active_warns(guild.id, member.id)
        await self.notify(guild, member, f"you received a warning ({count} active). Reason: {case['reason']}")
        await self.escalate(guild, member, count, case["id"])
        return case, count

    async def escalate(self, guild, member, count, from_case=None):
        """Apply the punishment that is configured for the current number of warnings."""
        for rule in self.bot.cfg(guild.id)["mod"]["escalation"]:
            if rule["warns"] != count:
                continue
            act, why = rule["action"], f"Automatic: {count} warnings"
            try:
                if act == "timeout":
                    mins = min(int(rule.get("minutes", 60)), 40320)
                    await member.timeout(timedelta(minutes=mins), reason=why)
                    await self.add_case(guild, "mute", member, guild.me, why, {"auto": True, "minutes": mins, "from_case": from_case})
                elif act == "kick":
                    await member.kick(reason=why)
                    await self.add_case(guild, "kick", member, guild.me, why, {"auto": True, "from_case": from_case})
                elif act == "ban":
                    await guild.ban(member, reason=why)
                    await self.add_case(guild, "ban", member, guild.me, why, {"auto": True, "from_case": from_case})
                elif act == "jail":
                    await self.bot.get_cog("Jail").send_to_jail(member, guild.me, why, auto=True, from_case=from_case)
            except discord.HTTPException as exc:
                log.warning("escalation %s for %s failed: %s", act, member, exc)
                self.bot.log(guild, "moderation", emb("Automatic punishment failed", f"{act} for {member.mention}: {exc}", discord.Color.red()))

    @commands.hybrid_command(name="warn", description="Warn a member")
    @app_commands.describe(member="Member to warn", reason="Reason")
    async def warn_cmd(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
        """Warn a member."""
        err = self.target_error(ctx.guild, ctx.author, member)
        if err:
            return await ctx.send(err, ephemeral=True)
        case, count = await self.warn_member(ctx.guild, member, ctx.author, reason)
        await ctx.send(f"{member.mention} was warned (case #{case['id']}, {count} active warnings).")

    @commands.hybrid_command(name="unwarn", description="Remove a warning by case number")
    @app_commands.describe(case_id="Case number")
    async def unwarn_cmd(self, ctx, case_id: int):
        """Remove a warning by case number."""
        for c in self.bot.store.cases(ctx.guild.id):
            if c["id"] == case_id and c["type"] == "warn":
                c["active"] = False
                return await ctx.send(f"Warning #{case_id} removed.")
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "No warning with that case number."), ephemeral=True)

    @commands.hybrid_command(name="clearwarns", description="Remove all active warnings of a user")
    async def clearwarns_cmd(self, ctx, user: discord.User):
        """Remove all active warnings of a user."""
        n = 0
        for c in self.bot.store.cases(ctx.guild.id):
            if c["type"] == "warn" and c["user"] == user.id and c["active"]:
                c["active"] = False
                n += 1
        await ctx.send(f"Removed {n} warnings of {user}.")

    async def punish(self, guild, mod, target, kind, reason=None, seconds=None, extra=None):
        """Carry out one punishment and write the case. Returns (ok, text, case). Checks who may be punished, but not the rights of the moderator."""
        member = target if isinstance(target, discord.Member) else guild.get_member(target.id)
        err = self.target_error(guild, mod, member or target)
        if err:
            return False, err, None
        extra = dict(extra or {})
        why = reason or "No reason given"
        try:
            if kind == "mute":
                if member is None:
                    return False, "That user is not on this server.", None
                secs = min(seconds or self.bot.cfg(guild.id)["mod"]["default_mute_minutes"] * 60, 28 * 86400)
                await member.timeout(timedelta(seconds=secs), reason=reason)
                case = await self.add_case(guild, "mute", member, mod, reason, {**extra, "seconds": secs})
                await self.notify(guild, member, f"you were muted for {fmt_duration(secs)}. Reason: {case['reason']}")
                return True, f"{member.mention} muted for {fmt_duration(secs)} (case #{case['id']}).", case
            if kind == "kick":
                if member is None:
                    return False, "That user is not on this server.", None
                await self.notify(guild, member, f"you were kicked. Reason: {why}")
                await member.kick(reason=reason)
                case = await self.add_case(guild, "kick", member, mod, reason, extra)
                return True, f"{member} was kicked (case #{case['id']}).", case
            if kind == "ban":
                if member:
                    await self.notify(guild, member, f"you were banned. Reason: {why}.{self.appeal_hint(guild)}")
                await guild.ban(target, reason=reason)
                case = await self.add_case(guild, "ban", target, mod, reason, extra)
                return True, f"{target} was banned (case #{case['id']}).", case
            if kind == "tempban":
                if not seconds:
                    return False, "A temporary ban needs a duration.", None
                if member:
                    await self.notify(guild, member, f"you were banned for {fmt_duration(seconds)}. Reason: {why}.{self.appeal_hint(guild)}")
                await guild.ban(target, reason=f"Tempban {fmt_duration(seconds)}: {reason or 'no reason'}")
                until = int(time.time()) + seconds
                self.bot.cfg(guild.id)["mod"]["tempbans"][str(target.id)] = until
                case = await self.add_case(guild, "ban", target, mod, reason, {**extra, "seconds": seconds, "until": until})
                return True, f"{target} was banned for {fmt_duration(seconds)} (case #{case['id']}).", case
            if kind == "warn":
                if member is None:
                    return False, "That user is not on this server.", None
                case, count = await self.warn_member(guild, member, mod, reason, extra)
                return True, f"{member.mention} was warned (case #{case['id']}, {count} active warnings).", case
            if kind == "jail":
                if member is None:
                    return False, "That user is not on this server.", None
                ok, text = await self.bot.get_cog("Jail").send_to_jail(member, mod, reason, seconds=seconds)
                return ok, text, None
        except discord.HTTPException as exc:
            log.warning("%s of %s failed: %s", kind, target, exc)
            return False, f"Discord refused: {exc}", None
        return False, f"Unknown action {kind}.", None

    async def gated(self, ctx, kind, target, reason, seconds=None):
        """True if the action was sent to a second moderator for approval instead of being carried out."""
        approval = self.bot.get_cog("Approval")
        return bool(approval) and await approval.gate(ctx, kind, target, reason, seconds)

    @commands.hybrid_command(name="mute", description="Timeout a member")
    @app_commands.describe(member="Member", duration="For example 30m, 2h, 1d", reason="Reason")
    async def mute_cmd(self, ctx, member: discord.Member, duration: Optional[str] = None, *, reason: Optional[str] = None):
        """Timeout a member."""
        secs = parse_duration(duration) if duration else None
        if duration and secs is None:
            reason, duration = f"{duration} {reason or ''}".strip(), None
        ok, text, _ = await self.punish(ctx.guild, ctx.author, member, "mute", reason, secs)
        await ctx.send(text, ephemeral=not ok)

    @commands.hybrid_command(name="unmute", description="Remove a timeout")
    async def unmute_cmd(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
        """Remove a timeout."""
        await member.timeout(None, reason=reason)
        case = await self.add_case(ctx.guild, "unmute", member, ctx.author, reason)
        await ctx.send(f"{member.mention} was unmuted (case #{case['id']}).")

    @commands.hybrid_command(name="kick", description="Kick a member")
    async def kick_cmd(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
        """Kick a member."""
        err = self.target_error(ctx.guild, ctx.author, member)
        if err:
            return await ctx.send(err, ephemeral=True)
        if await self.gated(ctx, "kick", member, reason):
            return
        ok, text, _ = await self.punish(ctx.guild, ctx.author, member, "kick", reason)
        await ctx.send(text, ephemeral=not ok)

    @commands.hybrid_command(name="ban", description="Ban a user, also by ID")
    async def ban_cmd(self, ctx, user: discord.User, *, reason: Optional[str] = None):
        """Ban a user, also by ID."""
        err = self.target_error(ctx.guild, ctx.author, ctx.guild.get_member(user.id) or user)
        if err:
            return await ctx.send(err, ephemeral=True)
        if await self.gated(ctx, "ban", user, reason):
            return
        ok, text, _ = await self.punish(ctx.guild, ctx.author, user, "ban", reason)
        await ctx.send(text, ephemeral=not ok)

    @commands.hybrid_command(name="unban", description="Unban a user by ID")
    async def unban_cmd(self, ctx, user: discord.User, *, reason: Optional[str] = None):
        """Unban a user by ID."""
        try:
            await ctx.guild.unban(user, reason=reason)
        except discord.NotFound:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "That user is not banned."), ephemeral=True)
        case = await self.add_case(ctx.guild, "unban", user, ctx.author, reason)
        await ctx.send(f"{user} was unbanned (case #{case['id']}).")

    def case_line(self, c):
        """Format a case as one line for lists."""
        return f"#{c['id']} {c['type']} | <@{c['user']}> ({c['user']}) | {trim(c['reason'], 70)} | <t:{c['ts']}:R>" + ("" if c["active"] else " (removed)")

    @commands.hybrid_command(name="cases", description="Search the moderation history")
    @app_commands.describe(user="Member or user ID", kind="Case type", search="Part of a user name", text="Word in the reason", moderator="Moderator who handled the case", days="Only the last N days", page="Page")
    async def cases_cmd(
        self, ctx, user: Optional[discord.User] = None, kind: Optional[Literal[KINDS]] = None, search: Optional[str] = None, text: Optional[str] = None,
        moderator: Optional[discord.User] = None, days: Optional[commands.Range[int, 1, 3650]] = None, page: int = 1,
    ):
        """Search the moderation history by user, type, name, reason, moderator and age."""
        items = filter_cases(self.bot.store.cases(ctx.guild.id), user.id if user else None, kind, search, text, moderator.id if moderator else None, days)[::-1]
        pages = max(1, -(-len(items) // 10))
        page = min(max(page, 1), pages)
        chunk = items[(page - 1) * 10: page * 10]
        e = emb("Moderation history", "\n".join(self.case_line(c) for c in chunk) or "No cases found.", footer=f"Page {page}/{pages}, {len(items)} cases")
        await ctx.send(embed=e, ephemeral=True)

    @commands.hybrid_command(name="warnings", description="Show warnings of a user")
    async def warnings_cmd(self, ctx, user: discord.User):
        """Show warnings of a user."""
        items = [c for c in self.bot.store.cases(ctx.guild.id) if c["type"] == "warn" and c["user"] == user.id][::-1]
        text = "\n".join(self.case_line(c) for c in items[:15]) or "No warnings."
        await ctx.send(embed=emb(f"Warnings of {user}", text, footer=f"{self.active_warns(ctx.guild.id, user.id)} active"), ephemeral=True)

    def find_case(self, gid, case_id):
        """Return the stored case with this number, or None."""
        return next((c for c in self.bot.store.cases(gid) if c["id"] == case_id), None)

    @commands.hybrid_group(name="case", fallback="view", description="Show one case")
    @app_commands.describe(case_id="Case number")
    async def case_cmd(self, ctx, case_id: int):
        """Show one case."""
        c = self.find_case(ctx.guild.id, case_id)
        if not c:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Case not found."), ephemeral=True)
        e = emb(f"Case #{c['id']} | {c['type']}", color=COLORS.get(c["type"]))
        e.add_field(name="User", value=f"<@{c['user']}> ({c['user']})\n{c['user_name']}")
        e.add_field(name="Moderator", value=f"<@{c['mod']}> ({c['mod']})")
        e.add_field(name="Date", value=f"<t:{c['ts']}:F>")
        e.add_field(name="Reason", value=trim(c["reason"]), inline=False)
        links = [self.find_case(ctx.guild.id, i) for i in c["extra"].get("links", [])]
        if any(links):
            e.add_field(name="Linked cases", value=trim("\n".join(self.case_line(x) for x in links if x), 1000), inline=False)
        notes = [x for x in self.bot.store.cases(ctx.guild.id) if x["type"] == "note" and x["user"] == c["user"] and x["id"] != c["id"] and x["id"] not in c["extra"].get("links", [])][-3:]
        if notes:
            e.add_field(name="Latest notes on this user", value=trim("\n".join(self.case_line(x) for x in notes), 1000), inline=False)
        await ctx.send(embed=e, ephemeral=True)

    @case_cmd.command(name="timeline", description="Everything stored about a user in time order")
    @app_commands.describe(user="Member or user ID", page="Page")
    async def case_timeline(self, ctx, user: discord.User, page: int = 1):
        """Everything stored about a user in time order: account, join and invite, probation, cases, appeals."""
        gid = ctx.guild.id
        member = ctx.guild.get_member(user.id)
        rec = self.bot.store.user_data.get(str(gid), {}).get(str(user.id), {})
        main = self.bot.cfg(gid)["appeals"]
        appeals = main["items"]
        events = build_timeline(user.id, self.bot.store.cases(gid), appeals, rec, member.joined_at.timestamp() if member and member.joined_at else None, discord.utils.snowflake_time(user.id).timestamp(), self.bot.cfg(gid)["probation"]["members"].get(str(user.id)))
        pages = max(1, -(-len(events) // 12))
        page = min(max(page, 1), pages)
        chunk = events[(page - 1) * 12: page * 12]
        e = emb(f"Timeline of {user}", "\n".join(f"<t:{ts}:f> {text}" for ts, text in chunk), footer=f"Page {page}/{pages}. The bot does not store messages, so they are not listed.")
        await ctx.send(embed=e, ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @case_cmd.command(name="link", description="Link two cases, for example a note to a ban")
    @app_commands.describe(case_id="Case number", other="Case to link to it")
    async def case_link(self, ctx, case_id: int, other: int):
        """Link two cases to each other so both show the connection."""
        a, b = self.find_case(ctx.guild.id, case_id), self.find_case(ctx.guild.id, other)
        if not a or not b or a is b:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Both case numbers must exist and differ."), ephemeral=True)
        self.bot.store.cases(ctx.guild.id)
        for x, y in ((a, b), (b, a)):
            links = x["extra"].setdefault("links", [])
            if y["id"] not in links:
                links.append(y["id"])
        await ctx.send(f"Cases #{case_id} and #{other} are linked.", ephemeral=True)

    @case_cmd.command(name="unlink", description="Remove the link between two cases")
    @app_commands.describe(case_id="Case number", other="Linked case")
    async def case_unlink(self, ctx, case_id: int, other: int):
        """Remove the link between two cases."""
        a, b = self.find_case(ctx.guild.id, case_id), self.find_case(ctx.guild.id, other)
        if not a or not b:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Case not found."), ephemeral=True)
        self.bot.store.cases(ctx.guild.id)
        for x, y in ((a, b), (b, a)):
            if y["id"] in x["extra"].get("links", []):
                x["extra"]["links"].remove(y["id"])
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Link removed."), ephemeral=True)

    async def undo_one(self, guild, mod, case, reason):
        """Take back the effect of one case. Returns a short result text."""
        kind, uid = case["type"], case["user"]
        user = discord.Object(uid)
        text = "marked as removed"
        try:
            if kind == "ban":
                await guild.unban(user, reason=reason)
                self.bot.cfg(guild.id)["mod"]["tempbans"].pop(str(uid), None)
                text = "unbanned"
            elif kind == "mute":
                member = guild.get_member(uid)
                if member is not None and member.timed_out_until:
                    await member.timeout(None, reason=reason)
                    text = "timeout removed"
            elif kind == "jail":
                member = guild.get_member(uid)
                if member is not None and self.bot.store.users(guild.id).get(str(uid), {}).get("jailed"):
                    ok, msg = await self.bot.get_cog("Jail").release(member, mod, reason)
                    text = "released" if ok else msg
            elif kind == "kick":
                text = "a kick cannot be taken back, marked as removed"
        except discord.NotFound:
            text = "was already gone"
        except discord.HTTPException as exc:
            return f"#{case['id']} {kind}: Discord refused ({exc})"
        case["active"] = False
        case["extra"]["undone_by"] = mod.id
        case["extra"]["undone_at"] = int(time.time())
        self.bot.store.cases(guild.id)
        return f"#{case['id']} {kind}: {text}"

    def undo_set(self, gid, case, follow=True, batch=False):
        """The cases that belong to an undo: the case itself, automatic punishments that its warning caused, and for a bulk action every case of the same run."""
        cases = self.bot.store.cases(gid)
        chosen = {case["id"]: case}
        if follow:
            for c in cases:
                if c["extra"].get("from_case") == case["id"] and c["active"]:
                    chosen[c["id"]] = c
        batch_id = case["extra"].get("batch")
        if batch and batch_id:
            for c in cases:
                if c["extra"].get("batch") == batch_id and c["active"]:
                    chosen[c["id"]] = c
        return [c for c in chosen.values() if c["active"] and c["type"] not in ("note", "unban", "unmute", "unjail")] or ([case] if case["active"] else [])

    @case_cmd.command(name="undo", description="Take back a case and what it caused")
    @app_commands.describe(case_id="Case number", reason="Why it is taken back", follow="Also take back automatic punishments caused by this warning", batch="For a bulk action: take back every case of the same run")
    async def case_undo(self, ctx, case_id: int, reason: Optional[str] = None, follow: bool = True, batch: bool = False):
        """Take back a case: unban, remove the timeout, release from the gulag or remove the warning, together with the follow-up punishments."""
        c = self.find_case(ctx.guild.id, case_id)
        if not c:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Case not found."), ephemeral=True)
        if not c["active"] and not (c["extra"].get("batch") and batch):
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "That case is already taken back."), ephemeral=True)
        why = f"Case #{case_id} taken back: {reason or 'no reason'}"
        chosen = self.undo_set(ctx.guild.id, c, follow, batch)
        if len(chosen) > 25:
            return await ctx.send(f"That would take back {len(chosen)} cases. At most 25 at once.", ephemeral=True)
        await ctx.defer(ephemeral=True)
        lines = []
        for item in chosen:
            if item["type"] == "warn":
                item["active"] = False
                item["extra"]["undone_by"] = ctx.author.id
                item["extra"]["undone_at"] = int(time.time())
                self.bot.store.cases(ctx.guild.id)
                lines.append(f"#{item['id']} warn: removed")
            else:
                lines.append(await self.undo_one(ctx.guild, ctx.author, item, why))
        e = emb(f"Case #{case_id} taken back", color=discord.Color.green(), user=ctx.author)
        e.add_field(name="Reason", value=trim(reason or "none"), inline=False)
        e.add_field(name="Result", value=trim("\n".join(lines), 1000), inline=False)
        self.bot.log(ctx.guild, "moderation", e)
        await ctx.send(trim("\n".join(lines), 1800), ephemeral=True)

    @case_cmd.command(name="edit", description="Change the reason of a case")
    @app_commands.describe(case_id="Case number", reason="New reason")
    async def case_edit(self, ctx, case_id: int, *, reason: str):
        """Change the reason of a case."""
        c = self.find_case(ctx.guild.id, case_id)
        if not c:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Case not found."), ephemeral=True)
        old, c["reason"] = c["reason"], reason[:1000]
        self.bot.store.cases(ctx.guild.id)
        e = emb(f"Case #{case_id} edited", color=discord.Color.light_grey(), user=ctx.author)
        e.add_field(name="Before", value=trim(old), inline=False)
        e.add_field(name="After", value=trim(c["reason"]), inline=False)
        self.bot.log(ctx.guild, "moderation", e)
        await ctx.send(f"Case #{case_id} updated.", ephemeral=True)

    @case_cmd.command(name="delete", description="Delete a case completely")
    @app_commands.describe(case_id="Case number")
    async def case_delete(self, ctx, case_id: int):
        """Delete a case completely."""
        c = self.find_case(ctx.guild.id, case_id)
        if not c:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Case not found."), ephemeral=True)
        self.bot.store.delete_case(ctx.guild.id, case_id)
        e = emb(f"Case #{case_id} deleted", color=discord.Color.light_grey(), user=ctx.author)
        e.add_field(name="Was", value=f"{c['type']} of <@{c['user']}>: {trim(c['reason'], 300)}", inline=False)
        self.bot.log(ctx.guild, "moderation", e)
        await ctx.send(f"Case #{case_id} deleted.", ephemeral=True)

    @commands.hybrid_command(name="note", description="Add a private moderator note about a user")
    @app_commands.describe(user="User", text="Note")
    async def note_cmd(self, ctx, user: discord.User, *, text: str):
        """Add a private moderator note about a user."""
        case = await self.add_case(ctx.guild, "note", user, ctx.author, text[:1000])
        await ctx.send(f"Note saved as case #{case['id']}. The user is not told.", ephemeral=True)

    def appeal_hint(self, guild):
        """Return a sentence with the appeal server invite if one is configured."""
        invite = self.bot.cfg(guild.id)["appeals"]["invite"]
        return f" You can appeal here: {invite}" if invite else ""

    @commands.hybrid_command(name="tempban", description="Ban a user for a limited time")
    @app_commands.describe(user="User", duration="For example 7d, 12h, 2w", reason="Reason")
    async def tempban_cmd(self, ctx, user: discord.User, duration: str, *, reason: Optional[str] = None):
        """Ban a user for a limited time."""
        secs = parse_duration(duration)
        if not secs:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Invalid duration. Examples: 12h, 7d, 2w"), ephemeral=True)
        err = self.target_error(ctx.guild, ctx.author, ctx.guild.get_member(user.id) or user)
        if err:
            return await ctx.send(err, ephemeral=True)
        if await self.gated(ctx, "tempban", user, reason, secs):
            return
        ok, text, _ = await self.punish(ctx.guild, ctx.author, user, "tempban", reason, secs)
        await ctx.send(text, ephemeral=not ok)

    @tasks.loop(seconds=60)
    async def tempban_loop(self):
        """Unban users whose temporary ban is over."""
        now = int(time.time())
        try:
            for guild in self.bot.guilds:
                bans = self.bot.cfg(guild.id)["mod"]["tempbans"]
                for uid, until in list(bans.items()):
                    if until > now:
                        continue
                    try:
                        await guild.unban(discord.Object(int(uid)), reason="Temporary ban is over")
                    except discord.NotFound:
                        log.info("user %s was already unbanned in %s", uid, guild.id)
                    except discord.HTTPException as exc:
                        log.warning("could not unban %s in %s: %s", uid, guild.id, exc)
                        continue
                    bans.pop(uid, None)
                    try:
                        user = await self.bot.fetch_user(int(uid))
                    except discord.NotFound:
                        log.info("user %s no longer exists, no unban case written", uid)
                        continue
                    await self.add_case(guild, "unban", user, guild.me, "Temporary ban is over")
        except Exception:
            log.exception("tempban loop failed")

    @tempban_loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected before the loop starts."""
        await self.bot.wait_until_ready()

    async def cog_load(self):
        """Start the tempban loop."""
        self.tempban_loop.start()

    async def cog_unload(self):
        """Stop the tempban loop."""
        self.tempban_loop.cancel()

    @esc.command(name="list", description="Show the escalation steps")
    async def esc_list(self, it: discord.Interaction):
        """Show the escalation steps."""
        rules = sorted(self.bot.cfg(it.guild_id)["mod"]["escalation"], key=lambda r: r["warns"])
        text = "\n".join(f"{r['warns']} warnings: {r['action']}" + (f" {r['minutes']} min" if r["action"] == "timeout" else "") for r in rules)
        await it.response.send_message(text or "No steps set.", ephemeral=True)

    @esc.command(name="set", description="Set the punishment for a number of warnings")
    async def esc_set(self, it: discord.Interaction, warns: app_commands.Range[int, 1, 50], action: Literal["timeout", "kick", "ban", "jail"], minutes: app_commands.Range[int, 1, 40320] = 60):
        """Set the punishment for a number of warnings."""
        rules = [r for r in self.bot.cfg(it.guild_id)["mod"]["escalation"] if r["warns"] != warns]
        rules.append({"warns": warns, "action": action, "minutes": minutes})
        self.bot.cfg(it.guild_id)["mod"]["escalation"] = rules
        await it.response.send_message(f"{warns} warnings: {action}", ephemeral=True)

    @esc.command(name="expiry", description="Warnings stop counting after this many days (0 = never)")
    @app_commands.describe(days="Days until a warning no longer counts for the escalation")
    async def esc_expiry(self, it: discord.Interaction, days: app_commands.Range[int, 0, 3650]):
        """Warnings stop counting after this many days (0 = never)."""
        self.bot.cfg(it.guild_id)["mod"]["warn_expiry_days"] = days
        await it.response.send_message(f"Warnings stop counting after {days} days." if days else "Warnings count forever.", ephemeral=True)

    @esc.command(name="remove", description="Remove an escalation step")
    async def esc_remove(self, it: discord.Interaction, warns: int):
        """Remove an escalation step."""
        m = self.bot.cfg(it.guild_id)["mod"]
        before = len(m["escalation"])
        m["escalation"] = [r for r in m["escalation"] if r["warns"] != warns]
        await it.response.send_message("Removed." if len(m["escalation"]) < before else "No such step.", ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Moderation(bot))
