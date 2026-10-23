"""Bulk actions: ban, kick or time out several users at once, after a confirmation."""

import asyncio
import logging
import re
import secrets
from datetime import timedelta
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from ... import i18n
from ...utils import fmt_duration, parse_duration, trim

log = logging.getLogger(__name__)

MAX_USERS = 25
ID = re.compile(r"\d{15,20}")


def parse_ids(text):
    """Find user IDs or mentions in a text. Duplicates are removed, the order stays."""
    seen, out = set(), []
    for m in ID.finditer(text or ""):
        uid = int(m.group(0))
        if uid not in seen:
            seen.add(uid)
            out.append(uid)
    return out


class Confirm(discord.ui.View):
    """Confirm or cancel a bulk action."""

    def __init__(self, user_id):
        """Remember who may press the buttons."""
        super().__init__(timeout=60)
        self.user_id = user_id
        self.answer = None

    async def interaction_check(self, interaction):
        """Only the moderator who started the action may answer."""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This is not your confirmation."), ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
    async def yes(self, interaction, button):
        """Run the action."""
        self.answer = True
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def no(self, interaction, button):
        """Cancel the action."""
        self.answer = False
        await interaction.response.defer()
        self.stop()


class Bulk(commands.Cog):
    """Moderation for several users at once."""

    bg = app_commands.Group(name="bulk", description="Ban, kick or time out several users at once", default_permissions=discord.Permissions(moderate_members=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot
        self.running = set()

    async def run(self, it, kind, users, reason, seconds=None):
        """Ask for confirmation, then apply the action to each user and report the result."""
        needed = {"ban": "ban_members", "kick": "kick_members", "mute": "moderate_members"}[kind]
        if not getattr(it.user.guild_permissions, needed):
            return await it.response.send_message(i18n.say(it.client, it.guild, "You need the {title} permission for this.", title=needed.replace('_', ' ').title()), ephemeral=True)
        ids = parse_ids(users)
        if not ids:
            return await it.response.send_message(i18n.say(it.client, it.guild, "I found no user IDs or mentions in your list."), ephemeral=True)
        if len(ids) > MAX_USERS:
            return await it.response.send_message(i18n.say(it.client, it.guild, "At most {MAX_USERS} users at once, you gave {count}.", MAX_USERS=MAX_USERS, count=len(ids)), ephemeral=True)
        if it.guild_id in self.running:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Another bulk action is still running on this server."), ephemeral=True)
        mod = self.bot.get_cog("Moderation")
        if mod is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "The moderation module is not loaded."), ephemeral=True)
        view = Confirm(it.user.id)
        names = []
        for uid in ids[:10]:
            m = it.guild.get_member(uid)
            names.append(f"{m} ({uid})" if m else str(uid))
        more = f"\nand {len(ids) - 10} more" if len(ids) > 10 else ""
        how = f" for {fmt_duration(seconds)}" if seconds else ""
        await it.response.send_message(f"{kind} {len(ids)} user(s){how}?\n" + "\n".join(names) + more + f"\nReason: {trim(reason or 'No reason given', 200)}", view=view, ephemeral=True)
        await view.wait()
        if not view.answer:
            return await it.edit_original_response(content="Cancelled." if view.answer is False else "No answer, cancelled.", view=None)
        approval = self.bot.get_cog("Approval")
        if approval is not None and await approval.gate_bulk(it, kind, ids, reason, seconds):
            return await it.edit_original_response(content="This action needs the approval of a second moderator. A request was posted.", view=None)
        await it.edit_original_response(content=f"Working on {len(ids)} user(s).", view=None)
        done, failed = await self.execute(it.guild, it.user, kind, ids, reason, seconds)
        text = f"Done: {len(done)}. Failed: {len(failed)}." + ("\n" + trim("\n".join(failed), 1500) if failed else "")
        await it.edit_original_response(content=text)

    async def execute(self, guild, moderator, kind, ids, reason, seconds=None):
        """Apply the action to each user. Returns (done ids, failure texts). Every case of one run shares a batch number."""
        mod = self.bot.get_cog("Moderation")
        batch = secrets.token_hex(4)
        self.running.add(guild.id)
        done, failed = [], []
        try:
            for uid in ids:
                try:
                    await self.one(guild, moderator, mod, kind, uid, reason, seconds, batch)
                    done.append(uid)
                except (ValueError, discord.HTTPException) as exc:
                    failed.append(f"{uid}: {exc}")
                await asyncio.sleep(0.5)
        finally:
            self.running.discard(guild.id)
        return done, failed

    async def one(self, guild, moderator, mod, kind, uid, reason, seconds, batch):
        """Apply the action to one user. Raises ValueError with the reason when it is not allowed."""
        member = guild.get_member(uid)
        if kind == "ban":
            try:
                user = member or await self.bot.fetch_user(uid)
            except discord.NotFound:
                raise ValueError("unknown user") from None
        elif member is None:
            raise ValueError("not on this server")
        else:
            user = member
        err = mod.target_error(guild, moderator, user)
        if err:
            raise ValueError(err)
        extra = {"bulk": True, "batch": batch}
        if kind == "ban":
            if member:
                await mod.notify(guild, member, f"you were banned. Reason: {reason or 'No reason given'}.{mod.appeal_hint(guild)}")
            await guild.ban(user, reason=reason)
            await mod.add_case(guild, "ban", user, moderator, reason, extra)
        elif kind == "kick":
            await mod.notify(guild, member, f"you were kicked. Reason: {reason or 'No reason given'}")
            await member.kick(reason=reason)
            await mod.add_case(guild, "kick", member, moderator, reason, extra)
        else:
            await member.timeout(timedelta(seconds=seconds), reason=reason)
            case = await mod.add_case(guild, "mute", member, moderator, reason, {**extra, "seconds": seconds})
            await mod.notify(guild, member, f"you were muted for {fmt_duration(seconds)}. Reason: {case['reason']}")

    @bg.command(name="ban", description="Ban several users")
    @app_commands.describe(users="User IDs or mentions, separated by spaces (at most 25)", reason="Reason")
    async def ban(self, it: discord.Interaction, users: app_commands.Range[str, 1, 1000], reason: Optional[str] = None):
        """Ban several users."""
        await self.run(it, "ban", users, reason)

    @bg.command(name="kick", description="Kick several members")
    @app_commands.describe(users="User IDs or mentions, separated by spaces (at most 25)", reason="Reason")
    async def kick(self, it: discord.Interaction, users: app_commands.Range[str, 1, 1000], reason: Optional[str] = None):
        """Kick several members."""
        await self.run(it, "kick", users, reason)

    @bg.command(name="timeout", description="Time out several members")
    @app_commands.describe(users="User IDs or mentions, separated by spaces (at most 25)", duration="For example 30m, 2h, 1d", reason="Reason")
    async def timeout(self, it: discord.Interaction, users: app_commands.Range[str, 1, 1000], duration: str = "1h", reason: Optional[str] = None):
        """Time out several members."""
        seconds = parse_duration(duration)
        if not seconds:
            return await it.response.send_message(i18n.say(it.client, it.guild, "I did not understand the duration. Use 30m, 2h or 1d."), ephemeral=True)
        await self.run(it, "mute", users, reason, min(seconds, 28 * 86400))


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Bulk(bot))
