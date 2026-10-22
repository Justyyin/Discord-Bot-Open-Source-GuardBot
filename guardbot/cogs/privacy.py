"""Data export, deletion and retention."""

import io
import json
import logging
import time

import discord
from discord import app_commands
from discord.ext import commands, tasks

from .. import i18n
from ..utils import CREDIT

log = logging.getLogger(__name__)


class Privacy(commands.Cog):
    """Data export, deletion and retention for members and administrators."""
    md = app_commands.Group(name="mydata", description="Your own stored data", guild_only=True)
    pv = app_commands.Group(name="privacy", description="Data retention and deletion", default_permissions=discord.Permissions(administrator=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot

    async def cog_load(self):
        """Start the background loop of this cog."""
        self.purge_loop.start()

    async def cog_unload(self):
        """Stop the background loop of this cog."""
        self.purge_loop.cancel()

    def anonymize(self, gid, uid):
        """Replace the stored name in the cases of a user. Returns how many cases changed."""
        n = 0
        for c in self.bot.store.cases(gid):
            if c["user"] == uid:
                c["user_name"] = "deleted user"
                n += 1
        return n

    def forget(self, gid, uid):
        """Remove reminders of a user and the name from ban appeals. Returns how many entries changed."""
        cfg = self.bot.cfg(gid)
        before = len(cfg["reminders"]["items"])
        cfg["reminders"]["items"] = [i for i in cfg["reminders"]["items"] if i["user"] != int(uid)]
        n = before - len(cfg["reminders"]["items"])
        for item in cfg["appeals"]["items"].values():
            if item.get("user") == int(uid) and item.get("name") != "deleted user":
                item["name"] = "deleted user"
                n += 1
        return n

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Runs when a member leaves or is removed."""
        rec = self.bot.store.users(member.guild.id).get(str(member.id))
        if rec is not None:
            self.bot.store.user(member.guild.id, member.id)["left_at"] = int(time.time())

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Runs when a member joins."""
        rec = self.bot.store.users(member.guild.id).get(str(member.id))
        if rec and rec.pop("left_at", None):
            self.bot.store.user(member.guild.id, member.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Runs when the bot is removed from a server."""
        if self.bot.settings.get("purge_on_guild_leave"):
            self.bot.store.drop_guild(guild.id)

    @tasks.loop(hours=6)
    async def purge_loop(self):
        """Delete the data of members who left longer ago than the retention time."""
        try:
            now = time.time()
            for guild in self.bot.guilds:
                days = self.bot.cfg(guild.id)["privacy"]["retention_days"]
                if not days or not self.bot.module_on(guild.id, "privacy"):
                    continue
                for uid, rec in list(self.bot.store.users(guild.id).items()):
                    left = rec.get("left_at")
                    if left and now - left > days * 86400 and not guild.get_member(int(uid)):
                        self.bot.store.delete_user(guild.id, uid)
                        self.anonymize(guild.id, int(uid))
        except Exception:
            log.exception("privacy purge loop failed")

    @purge_loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected before the loop starts."""
        await self.bot.wait_until_ready()

    def export(self, gid, uid):
        """Collect everything stored about a user on a server."""
        rec = dict(self.bot.store.users(gid).get(str(uid), {}))
        rec.pop("jail_roles", None)
        cases = [c for c in self.bot.store.cases(gid) if c["user"] == uid]
        cfg = self.bot.cfg(gid)
        reminders = [i for i in cfg["reminders"]["items"] if i["user"] == int(uid)]
        appeals = [i for i in cfg["appeals"]["items"].values() if i.get("user") == int(uid)]
        return {"generator": CREDIT, "server": gid, "user": uid, "stored_profile": rec, "moderation_cases_about_you": cases, "reminders": reminders, "ban_appeals": appeals}

    @md.command(name="export", description="Download the data this bot stores about you on this server")
    async def md_export(self, it: discord.Interaction):
        """Download the data this bot stores about you on this server."""
        raw = json.dumps(self.export(it.guild_id, it.user.id), indent=2, ensure_ascii=False).encode("utf-8")
        await it.response.send_message(i18n.say(it.client, it.guild, "Here is everything stored about you on this server."), file=discord.File(io.BytesIO(raw), filename="mydata.json"), ephemeral=True)

    @md.command(name="delete", description="Delete your XP, birthday and profile data on this server")
    @app_commands.describe(confirm="Set to true to confirm")
    async def md_delete(self, it: discord.Interaction, confirm: bool = False):
        """Delete your XP, birthday and profile data on this server."""
        if not confirm:
            return await it.response.send_message(i18n.say(it.client, it.guild, "This removes your XP, level and birthday. Moderation cases are kept for the safety of the server. Run the command again with confirm set to true."), ephemeral=True)
        rec = self.bot.store.users(it.guild_id).get(str(it.user.id), {})
        if rec.get("jailed"):
            return await it.response.send_message(i18n.say(it.client, it.guild, "You cannot delete your data while you are in the gulag."), ephemeral=True)
        self.bot.store.delete_user(it.guild_id, it.user.id)
        self.forget(it.guild_id, it.user.id)
        await it.response.send_message(i18n.say(it.client, it.guild, "Your data was deleted. Your level roles stay until a moderator removes them."), ephemeral=True)

    @pv.command(name="retention", description="Delete data of members who left after this many days (0 = keep)")
    async def pv_retention(self, it: discord.Interaction, days: app_commands.Range[int, 0, 3650]):
        """Delete data of members who left after this many days (0 = keep)."""
        self.bot.cfg(it.guild_id)["privacy"]["retention_days"] = days
        await it.response.send_message(f"Data of members who left is deleted after {days} days." if days else "Data of members who left is kept.", ephemeral=True)

    @pv.command(name="delete", description="Delete all stored data of a user by ID")
    @app_commands.describe(user_id="User ID", cases="Also remove the name from moderation cases")
    async def pv_delete(self, it: discord.Interaction, user_id: str, cases: bool = True):
        """Delete all stored data of a user by ID."""
        if not user_id.isdigit():
            return await it.response.send_message(i18n.say(it.client, it.guild, "Enter a numeric user ID."), ephemeral=True)
        self.bot.store.delete_user(it.guild_id, user_id)
        self.forget(it.guild_id, user_id)
        n = self.anonymize(it.guild_id, int(user_id)) if cases else 0
        await it.response.send_message(f"Profile data deleted. {n} case names anonymized.", ephemeral=True)

    @pv.command(name="export", description="Export the stored data of a user by ID")
    async def pv_export(self, it: discord.Interaction, user_id: str):
        """Export the stored data of a user by ID."""
        if not user_id.isdigit():
            return await it.response.send_message(i18n.say(it.client, it.guild, "Enter a numeric user ID."), ephemeral=True)
        raw = json.dumps(self.export(it.guild_id, int(user_id)), indent=2, ensure_ascii=False).encode("utf-8")
        await it.response.send_message(file=discord.File(io.BytesIO(raw), filename=f"data-{user_id}.json"), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Privacy(bot))
