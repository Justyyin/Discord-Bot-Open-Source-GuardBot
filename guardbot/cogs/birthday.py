"""Birthdays with a role and a message on the day."""

import calendar
import logging
from datetime import date, datetime, timezone
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ..utils import emb

log = logging.getLogger(__name__)


def get_tz(name):
    """Return the timezone for a name and fall back to UTC with a warning."""
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError, OSError):
        log.warning("unknown timezone %r, falling back to UTC", name)
        return timezone.utc


def next_date(month, day, today):
    """Return the next date of a day and month, using 28 February when 29 February does not exist."""
    for year in (today.year, today.year + 1):
        try:
            d = date(year, month, day)
        except ValueError:
            d = date(year, 2, 28)
        if d >= today:
            return d


class Birthday(commands.Cog):
    """Stores birthdays and congratulates on the day."""
    bd = app_commands.Group(name="birthday", description="Birthdays", guild_only=True)
    setup_grp = app_commands.Group(name="birthdaysetup", description="Configure the birthday system", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot

    async def cog_load(self):
        """Start the background loop of this cog."""
        self.loop.start()

    async def cog_unload(self):
        """Stop the background loop of this cog."""
        self.loop.cancel()

    @tasks.loop(minutes=5)
    async def loop(self):
        """Give and remove the birthday role and post the congratulations once per day."""
        try:
            for guild in self.bot.guilds:
                b = self.bot.cfg(guild.id)["birthday"]
                if not self.bot.module_on(guild.id, "birthday") or not b["enabled"] or not b["role"]:
                    continue
                role = guild.get_role(b["role"])
                if not role:
                    continue
                now = datetime.now(get_tz(b["timezone"]))
                keys = {now.strftime("%m-%d")}
                if keys == {"02-28"} and not calendar.isleap(now.year):
                    keys.add("02-29")
                iso = now.strftime("%Y-%m-%d")
                gusers = self.bot.store.users(guild.id)
                celebrants = {int(u) for u, r in gusers.items() if r.get("birthday") in keys}
                for uid in celebrants:
                    m = guild.get_member(uid)
                    if not m:
                        continue
                    try:
                        if role not in m.roles:
                            await m.add_roles(role, reason="Birthday")
                        rec = self.bot.store.user(guild.id, uid)
                        if rec.get("bday_last") != iso:
                            rec["bday_last"] = iso
                            ch = guild.get_channel(b["channel"]) if b["channel"] else guild.system_channel
                            if ch:
                                text = b["message"].replace("{user}", m.mention).replace("{name}", m.display_name)
                                await ch.send(text, allowed_mentions=discord.AllowedMentions(users=[m]))
                    except discord.HTTPException as exc:
                        log.warning("m.add_roles failed: %s", exc)
                for m in list(role.members):
                    if m.id not in celebrants:
                        try:
                            await m.remove_roles(role, reason="Birthday over")
                        except discord.HTTPException as exc:
                            log.warning("m.remove_roles failed: %s", exc)
        except Exception:
            log.exception("birthday loop failed")

    @loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected before the loop starts."""
        await self.bot.wait_until_ready()

    @bd.command(name="set", description="Set your birthday (day and month only)")
    async def bd_set(self, it: discord.Interaction, day: app_commands.Range[int, 1, 31], month: app_commands.Range[int, 1, 12]):
        """Set your birthday (day and month only)."""
        try:
            date(2000, month, day)
        except ValueError:
            return await it.response.send_message("That date does not exist.", ephemeral=True)
        rec = self.bot.store.user(it.guild_id, it.user.id)
        rec["birthday"], rec["bday_last"] = f"{month:02d}-{day:02d}", None
        await it.response.send_message(f"Birthday saved: {day:02d}.{month:02d}.", ephemeral=True)

    @bd.command(name="remove", description="Delete your birthday")
    async def bd_remove(self, it: discord.Interaction):
        """Delete your birthday."""
        self.bot.store.user(it.guild_id, it.user.id)["birthday"] = None
        await it.response.send_message("Birthday deleted.", ephemeral=True)

    @bd.command(name="show", description="Show a member's birthday")
    async def bd_show(self, it: discord.Interaction, user: Optional[discord.Member] = None):
        """Show a member's birthday."""
        m = user or it.user
        v = self.bot.store.user(it.guild_id, m.id)["birthday"]
        if not v:
            return await it.response.send_message(f"{m.display_name} has not set a birthday.", ephemeral=True)
        month, day = v.split("-")
        await it.response.send_message(f"{m.display_name}: {day}.{month}.", ephemeral=True)

    @bd.command(name="upcoming", description="Next birthdays on this server")
    async def bd_upcoming(self, it: discord.Interaction):
        """Next birthdays on this server."""
        b = self.bot.cfg(it.guild_id)["birthday"]
        today = datetime.now(get_tz(b["timezone"])).date()
        items = []
        for uid, rec in self.bot.store.users(it.guild_id).items():
            if rec.get("birthday") and it.guild.get_member(int(uid)):
                month, day = map(int, rec["birthday"].split("-"))
                items.append((next_date(month, day, today), uid))
        items.sort()
        lines = [f"{d.strftime('%d.%m.')} - <@{u}> ({'today' if d == today else 'in ' + str((d - today).days) + ' days'})" for d, u in items[:10]]
        await it.response.send_message(embed=emb("Upcoming birthdays", "\n".join(lines) or "No birthdays saved."))

    @setup_grp.command(name="set", description="Configure the birthday system")
    @app_commands.describe(role="Role for the birthday person (created if none exists)", channel="Channel for messages", message="Text with {user} and {name}", timezone="IANA timezone, for example Europe/Berlin")
    async def bd_setup(self, it: discord.Interaction, enabled: Optional[bool] = None, role: Optional[discord.Role] = None, channel: Optional[discord.TextChannel] = None, message: Optional[str] = None, timezone: Optional[str] = None):
        """Configure the birthday system."""
        await it.response.defer(ephemeral=True)
        g = self.bot.cfg(it.guild_id)
        b = g["birthday"]
        if timezone:
            try:
                ZoneInfo(timezone)
            except (ZoneInfoNotFoundError, ValueError, OSError):
                if timezone.upper() != "UTC":
                    return await it.followup.send("Unknown timezone. Use a name like Europe/Berlin. On Windows run: pip install tzdata")
            b["timezone"] = timezone
        if role:
            if not role.is_assignable():
                return await it.followup.send("I cannot assign that role. Move my role above it.")
            b["role"] = role.id
        if channel:
            b["channel"] = channel.id
        if message:
            b["message"] = message
        if enabled is not None:
            b["enabled"] = enabled
            g["modules"]["birthday"] = enabled
        if b["enabled"] and not (b["role"] and it.guild.get_role(b["role"])):
            try:
                new = await it.guild.create_role(name="Birthday", colour=discord.Colour.gold(), reason="Birthday system")
                b["role"] = new.id
            except discord.HTTPException:
                return await it.followup.send("I could not create the Birthday role. Give me Manage Roles or pick a role.")
        await it.followup.send(f"Birthday system: {'on' if b['enabled'] else 'off'}, role {('<@&' + str(b['role']) + '>') if b['role'] else 'none'}, timezone {b['timezone']}")


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Birthday(bot))
