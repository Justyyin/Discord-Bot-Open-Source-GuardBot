"""Probation: new members get a role and may not post links or files until a few minutes passed or they wrote a normal message."""

import logging
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ...cog import BaseCog
from ... import i18n, scamscan
from ...utils import AdminGroup

log = logging.getLogger(__name__)

INVITE = ("discord.gg/", "discord.com/invite/", "discordapp.com/invite/")


def has_link(text):
    """True if a text contains a link or an invite."""
    low = (text or "").casefold()
    return bool(scamscan.URL.search(low)) or any(x in low for x in INVITE)


def is_harmless(text):
    """True if a message counts as a normal first message: some text, no link, no scam words."""
    t = (text or "").strip()
    return len(t) >= 3 and not has_link(t) and scamscan.scan(t).points == 0


def due(entry, minutes, now):
    """True if the time of probation of a member is over. Zero minutes switches the time route off."""
    return minutes > 0 and now - entry["ts"] >= minutes * 60


class Probation(BaseCog):
    """Probation for new members."""
    section = "probation"

    pg = AdminGroup(name="probation", description="New members may not post links or files at first", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    async def cog_load(self):
        """Start the loop that ends probation after the set time."""
        self.loop.start()

    async def cog_unload(self):
        """Stop the loop."""
        self.loop.cancel()

    def active(self, gid):
        """True if the module is on and a role is set."""
        return self.bot.module_on(gid, "probation") and bool(self.conf(gid)["role"])

    async def start(self, member):
        """Give a member the probation role and remember when it began."""
        c = self.conf(member.guild.id)
        role = member.guild.get_role(c["role"] or 0)
        if role is None or not role.is_assignable():
            self.bot.log(member.guild, "security", discord.Embed(title="Probation role cannot be given", description="Move my role above the probation role or choose another one with /access probation setup.", color=discord.Color.orange()))
            return False
        try:
            await member.add_roles(role, reason="Probation")
        except discord.HTTPException as exc:
            log.warning("probation role for %s failed: %s", member.id, exc)
            return False
        c["members"][str(member.id)] = {"ts": int(time.time()), "ok": 0}
        return True

    async def release(self, guild, uid, member=None):
        """End probation of a member and take the role away."""
        c = self.conf(guild.id)
        c["members"].pop(str(uid), None)
        member = member or guild.get_member(uid)
        role = guild.get_role(c["role"] or 0)
        if member is not None and role is not None and role in member.roles:
            try:
                await member.remove_roles(role, reason="Probation over")
            except discord.HTTPException as exc:
                log.warning("probation role could not be removed from %s: %s", uid, exc)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Start probation for a new member."""
        if not member.bot and self.active(member.guild.id):
            await self.start(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Forget a member who left."""
        if member.guild and str(member.id) in self.conf(member.guild.id)["members"]:
            self.conf(member.guild.id)["members"].pop(str(member.id), None)

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Block links and files of members on probation and count their normal messages."""
        if msg.author.bot or msg.guild is None or not self.active(msg.guild.id):
            return
        c = self.conf(msg.guild.id)
        entry = c["members"].get(str(msg.author.id))
        if entry is None:
            return
        banned = (c["block_links"] and has_link(msg.content)) or (c["block_files"] and (msg.attachments or msg.stickers))
        if banned:
            self.bot.bot_deleted.add(msg.id)
            try:
                await msg.delete()
            except discord.HTTPException as exc:
                self.bot.bot_deleted.discard(msg.id)
                log.warning("probation delete failed: %s", exc)
                return
            if c["notice"]:
                try:
                    await msg.channel.send(i18n.say(self.bot, msg.guild, "{user} Links and files are not allowed yet. Write a normal message first or wait a few minutes.", user=msg.author.mention), delete_after=8, allowed_mentions=discord.AllowedMentions(users=[msg.author]))
                except discord.HTTPException as exc:
                    log.warning("probation notice failed: %s", exc)
            return
        if c["messages"] and is_harmless(msg.content):
            entry["ok"] += 1
            if entry["ok"] >= c["messages"]:
                await self.release(msg.guild, msg.author.id, msg.author if isinstance(msg.author, discord.Member) else None)

    @tasks.loop(seconds=30)
    async def loop(self):
        """End probation of everyone whose time is over."""
        now = time.time()
        for guild in list(self.bot.guilds):
            if not self.bot.module_on(guild.id, "probation"):
                continue
            c = self.conf(guild.id)
            for uid, entry in list(c["members"].items()):
                try:
                    if due(entry, c["minutes"], now):
                        await self.release(guild, int(uid))
                except Exception:  # one broken entry must not stop the others
                    log.exception("probation release of %s failed", uid)
                    c["members"].pop(uid, None)

    @loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected."""
        await self.bot.wait_until_ready()

    @pg.command(name="setup", description="Choose the role and the rules of the probation")
    @app_commands.describe(role="Probation role, empty = create one named Probation", minutes="Release after this many minutes, 0 = only by messages", messages="Release after this many normal messages, 0 = only by time", block_links="Delete links and invites", block_files="Delete images, files and stickers", notice="Tell the member why the message was deleted")
    async def setup(
        self, it: discord.Interaction, role: Optional[discord.Role] = None, minutes: Optional[app_commands.Range[int, 0, 10080]] = None, messages: Optional[app_commands.Range[int, 0, 50]] = None,
        block_links: Optional[bool] = None, block_files: Optional[bool] = None, notice: Optional[bool] = None,
    ):
        """Choose the role and the rules of the probation."""
        c = self.conf(it.guild_id)
        await it.response.defer(ephemeral=True)
        if role is not None:
            if role.is_default() or role.managed or not role.is_assignable():
                return await it.followup.send(i18n.say(it.client, it.guild, "I cannot give that role. Move my role above it or choose another one."))
            c["role"] = role.id
        elif not it.guild.get_role(c["role"] or 0):
            try:
                c["role"] = (await it.guild.create_role(name="Probation", permissions=discord.Permissions.none(), reason="Probation setup")).id
            except discord.HTTPException as exc:
                return await it.followup.send(i18n.say(it.client, it.guild, "I could not create the role: {exc}", exc=exc))
        for key, value in (("minutes", minutes), ("messages", messages), ("block_links", block_links), ("block_files", block_files), ("notice", notice)):
            if value is not None:
                c[key] = value
        if c["minutes"] == 0 and c["messages"] == 0:
            c["minutes"] = 10
        self.bot.cfg(it.guild_id)["modules"]["probation"] = True
        await it.followup.send(i18n.say(it.client, it.guild, "Probation is on with <@&{role}>: release after {minutes} minutes or {messages} normal messages. Links {value}, files {value2}.", role=c['role'], minutes=c['minutes'], messages=c['messages'], value='blocked' if c['block_links'] else 'allowed', value2='blocked' if c['block_files'] else 'allowed'))

    @pg.command(name="status", description="Show the settings and who is on probation")
    async def status(self, it: discord.Interaction):
        """Show the settings and who is on probation."""
        c = self.conf(it.guild_id)
        lines = [
            f"Module: {'on' if self.bot.module_on(it.guild_id, 'probation') else 'off'}, role: {'<@&' + str(c['role']) + '>' if c['role'] else 'not set'}",
            f"Release after {c['minutes']} minutes or {c['messages']} normal messages. Links blocked: {c['block_links']}, files blocked: {c['block_files']}",
            f"On probation now: {len(c['members'])}",
        ] + [f"<@{uid}> since <t:{e['ts']}:R>, {e['ok']} normal messages" for uid, e in list(c["members"].items())[:15]]
        await it.response.send_message("\n".join(lines), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @pg.command(name="release", description="End the probation of a member now")
    async def release_cmd(self, it: discord.Interaction, member: discord.Member):
        """End the probation of a member now."""
        if str(member.id) not in self.conf(it.guild_id)["members"]:
            return await it.response.send_message(i18n.say(it.client, it.guild, "That member is not on probation."), ephemeral=True)
        await it.response.defer(ephemeral=True)
        await self.release(it.guild, member.id, member)
        await it.followup.send(i18n.say(it.client, it.guild, "{mention} is released.", mention=member.mention), allowed_mentions=discord.AllowedMentions.none())

    @pg.command(name="add", description="Put a member on probation")
    async def add(self, it: discord.Interaction, member: discord.Member):
        """Put a member on probation."""
        if not self.conf(it.guild_id)["role"]:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Run /access probation setup first."), ephemeral=True)
        await it.response.defer(ephemeral=True)
        ok = await self.start(member)
        await it.followup.send(f"{member.mention} is on probation." if ok else "I could not give the role.", allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Probation(bot))
