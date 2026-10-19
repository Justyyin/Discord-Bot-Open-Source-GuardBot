# Copyright (c) Justyn
import calendar
from datetime import date, datetime, timezone
from typing import Optional
from zoneinfo import ZoneInfo

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ..utils import emb


def get_tz(name):
    try:
        return ZoneInfo(name)
    except Exception:
        return timezone.utc


def next_date(month, day, today):
    for year in (today.year, today.year + 1):
        try:
            d = date(year, month, day)
        except ValueError:
            d = date(year, 2, 28)
        if d >= today:
            return d


class Birthday(commands.Cog):
    bd = app_commands.Group(name="birthday", description="Birthdays", guild_only=True)
    setup_grp = app_commands.Group(name="birthdaysetup", description="Configure the birthday system", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.loop.start()

    async def cog_unload(self):
        self.loop.cancel()

    @tasks.loop(minutes=5)
    async def loop(self):
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
                        rec = gusers[str(uid)]
                        if rec.get("bday_last") != iso:
                            rec["bday_last"] = iso
                            self.bot.store.mark("users")
                            ch = guild.get_channel(b["channel"]) if b["channel"] else guild.system_channel
                            if ch:
                                text = b["message"].replace("{user}", m.mention).replace("{name}", m.display_name)
                                await ch.send(text, allowed_mentions=discord.AllowedMentions(users=[m]))
                    except discord.HTTPException:
                        pass
                for m in list(role.members):
                    if m.id not in celebrants:
                        try:
                            await m.remove_roles(role, reason="Birthday over")
                        except discord.HTTPException:
                            pass
        except Exception as exc:
            print("birthday loop error:", exc)

    @loop.before_loop
    async def _wait(self):
        await self.bot.wait_until_ready()

    @bd.command(name="set", description="Set your birthday (day and month only)")
    async def bd_set(self, it: discord.Interaction, day: app_commands.Range[int, 1, 31], month: app_commands.Range[int, 1, 12]):
        try:
            date(2000, month, day)
        except ValueError:
            return await it.response.send_message("That date does not exist.", ephemeral=True)
        rec = self.bot.store.user(it.guild_id, it.user.id)
        rec["birthday"], rec["bday_last"] = f"{month:02d}-{day:02d}", None
        self.bot.store.mark("users")
        await it.response.send_message(f"Birthday saved: {day:02d}.{month:02d}.", ephemeral=True)

    @bd.command(name="remove", description="Delete your birthday")
    async def bd_remove(self, it: discord.Interaction):
        self.bot.store.user(it.guild_id, it.user.id)["birthday"] = None
        self.bot.store.mark("users")
        await it.response.send_message("Birthday deleted.", ephemeral=True)

    @bd.command(name="show", description="Show a member's birthday")
    async def bd_show(self, it: discord.Interaction, user: Optional[discord.Member] = None):
        m = user or it.user
        v = self.bot.store.user(it.guild_id, m.id)["birthday"]
        if not v:
            return await it.response.send_message(f"{m.display_name} has not set a birthday.", ephemeral=True)
        month, day = v.split("-")
        await it.response.send_message(f"{m.display_name}: {day}.{month}.", ephemeral=True)

    @bd.command(name="upcoming", description="Next birthdays on this server")
    async def bd_upcoming(self, it: discord.Interaction):
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
        await it.response.defer(ephemeral=True)
        g = self.bot.cfg(it.guild_id)
        b = g["birthday"]
        if timezone:
            try:
                ZoneInfo(timezone)
            except Exception:
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
        self.bot.store.mark("config")
        await it.followup.send(f"Birthday system: {'on' if b['enabled'] else 'off'}, role {('<@&' + str(b['role']) + '>') if b['role'] else 'none'}, timezone {b['timezone']}")


async def setup(bot):
    await bot.add_cog(Birthday(bot))
