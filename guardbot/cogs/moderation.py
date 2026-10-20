"""Warnings, mutes, kicks, bans, case history and automatic escalation."""

import logging
import time
from datetime import timedelta
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import emb, fmt_duration, parse_duration, trim

log = logging.getLogger(__name__)

KINDS = ("warn", "mute", "unmute", "kick", "ban", "unban", "jail", "unjail")
COLORS = {
    "warn": discord.Color.gold(),
    "mute": discord.Color.orange(),
    "unmute": discord.Color.green(),
    "kick": discord.Color.dark_orange(),
    "ban": discord.Color.red(),
    "unban": discord.Color.green(),
    "jail": discord.Color.dark_red(),
    "unjail": discord.Color.green(),
}


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

    async def warn_member(self, guild, member, mod, reason):
        """Create a warning, tell the member and run the escalation steps."""
        case = await self.add_case(guild, "warn", member, mod, reason)
        count = self.active_warns(guild.id, member.id)
        await self.notify(guild, member, f"you received a warning ({count} active). Reason: {case['reason']}")
        await self.escalate(guild, member, count)
        return case, count

    async def escalate(self, guild, member, count):
        """Apply the punishment that is configured for the current number of warnings."""
        for rule in self.bot.cfg(guild.id)["mod"]["escalation"]:
            if rule["warns"] != count:
                continue
            act, why = rule["action"], f"Automatic: {count} warnings"
            try:
                if act == "timeout":
                    mins = min(int(rule.get("minutes", 60)), 40320)
                    await member.timeout(timedelta(minutes=mins), reason=why)
                    await self.add_case(guild, "mute", member, guild.me, why, {"auto": True, "minutes": mins})
                elif act == "kick":
                    await member.kick(reason=why)
                    await self.add_case(guild, "kick", member, guild.me, why, {"auto": True})
                elif act == "ban":
                    await guild.ban(member, reason=why)
                    await self.add_case(guild, "ban", member, guild.me, why, {"auto": True})
                elif act == "jail":
                    await self.bot.get_cog("Jail").send_to_jail(member, guild.me, why, auto=True)
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
        await ctx.send("No warning with that case number.", ephemeral=True)

    @commands.hybrid_command(name="clearwarns", description="Remove all active warnings of a user")
    async def clearwarns_cmd(self, ctx, user: discord.User):
        """Remove all active warnings of a user."""
        n = 0
        for c in self.bot.store.cases(ctx.guild.id):
            if c["type"] == "warn" and c["user"] == user.id and c["active"]:
                c["active"] = False
                n += 1
        await ctx.send(f"Removed {n} warnings of {user}.")

    @commands.hybrid_command(name="mute", description="Timeout a member")
    @app_commands.describe(member="Member", duration="For example 30m, 2h, 1d", reason="Reason")
    async def mute_cmd(self, ctx, member: discord.Member, duration: Optional[str] = None, *, reason: Optional[str] = None):
        """Timeout a member."""
        err = self.target_error(ctx.guild, ctx.author, member)
        if err:
            return await ctx.send(err, ephemeral=True)
        secs = parse_duration(duration) if duration else None
        if duration and secs is None:
            reason, duration = f"{duration} {reason or ''}".strip(), None
        secs = min(secs or self.bot.cfg(ctx.guild.id)["mod"]["default_mute_minutes"] * 60, 28 * 86400)
        await member.timeout(timedelta(seconds=secs), reason=reason)
        case = await self.add_case(ctx.guild, "mute", member, ctx.author, reason, {"seconds": secs})
        await self.notify(ctx.guild, member, f"you were muted for {fmt_duration(secs)}. Reason: {case['reason']}")
        await ctx.send(f"{member.mention} muted for {fmt_duration(secs)} (case #{case['id']}).")

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
        await self.notify(ctx.guild, member, f"you were kicked. Reason: {reason or 'No reason given'}")
        await member.kick(reason=reason)
        case = await self.add_case(ctx.guild, "kick", member, ctx.author, reason)
        await ctx.send(f"{member} was kicked (case #{case['id']}).")

    @commands.hybrid_command(name="ban", description="Ban a user, also by ID")
    async def ban_cmd(self, ctx, user: discord.User, *, reason: Optional[str] = None):
        """Ban a user, also by ID."""
        member = ctx.guild.get_member(user.id)
        err = self.target_error(ctx.guild, ctx.author, member or user)
        if err:
            return await ctx.send(err, ephemeral=True)
        if member:
            await self.notify(ctx.guild, member, f"you were banned. Reason: {reason or 'No reason given'}")
        await ctx.guild.ban(user, reason=reason)
        case = await self.add_case(ctx.guild, "ban", user, ctx.author, reason)
        await ctx.send(f"{user} was banned (case #{case['id']}).")

    @commands.hybrid_command(name="unban", description="Unban a user by ID")
    async def unban_cmd(self, ctx, user: discord.User, *, reason: Optional[str] = None):
        """Unban a user by ID."""
        try:
            await ctx.guild.unban(user, reason=reason)
        except discord.NotFound:
            return await ctx.send("That user is not banned.", ephemeral=True)
        case = await self.add_case(ctx.guild, "unban", user, ctx.author, reason)
        await ctx.send(f"{user} was unbanned (case #{case['id']}).")

    def case_line(self, c):
        """Format a case as one line for lists."""
        return f"#{c['id']} {c['type']} | <@{c['user']}> ({c['user']}) | {trim(c['reason'], 70)} | <t:{c['ts']}:R>" + ("" if c["active"] else " (removed)")

    @commands.hybrid_command(name="cases", description="Moderation history, filter by user, type or name")
    @app_commands.describe(user="Member or user ID", kind="Case type", search="Part of a user name", page="Page")
    async def cases_cmd(self, ctx, user: Optional[discord.User] = None, kind: Optional[Literal[KINDS]] = None, search: Optional[str] = None, page: int = 1):
        """Moderation history, filter by user, type or name."""
        items = [
            c for c in self.bot.store.cases(ctx.guild.id)
            if (not user or c["user"] == user.id) and (not kind or c["type"] == kind) and (not search or search.lower() in c["user_name"].lower())
        ][::-1]
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

    @commands.hybrid_command(name="case", description="Show one case")
    async def case_cmd(self, ctx, case_id: int):
        """Show one case."""
        for c in self.bot.store.cases(ctx.guild.id):
            if c["id"] == case_id:
                e = emb(f"Case #{c['id']} | {c['type']}", color=COLORS.get(c["type"]))
                e.add_field(name="User", value=f"<@{c['user']}> ({c['user']})\n{c['user_name']}")
                e.add_field(name="Moderator", value=f"<@{c['mod']}> ({c['mod']})")
                e.add_field(name="Date", value=f"<t:{c['ts']}:F>")
                e.add_field(name="Reason", value=trim(c["reason"]), inline=False)
                return await ctx.send(embed=e, ephemeral=True)
        await ctx.send("Case not found.", ephemeral=True)

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
