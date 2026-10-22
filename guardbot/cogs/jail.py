"""The gulag: restricted channel for hacked accounts, with optional release time."""

import logging
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from .. import i18n
from ..utils import bulk, emb, fmt_duration, parse_duration

log = logging.getLogger(__name__)

STEPS = (
    ("1. Reset Your Password", "Change your Discord password immediately."),
    ("2. Enable 2FA", "Make sure Two-Factor Authentication is enabled on your account."),
    ("3. Check Suspicious Devices", "Go through your logged-in devices and remove anything you do not recognize."),
    (
        "4. Remove Suspicious Authorized Apps",
        "Go to User Settings > Authorized Apps and remove anything suspicious.\n\n"
        "Especially remove apps that say things like \"join servers for you\" or anything you do not remember authorizing.",
    ),
    (
        "5. Clear Browser Data",
        "Sign out of Discord in your browsers, then clear browser cookies, cached files, and saved site data. "
        "This removes old login sessions that may still be compromised.",
    ),
    ("6. Ping Staff", "After doing all of this, ping a member who has the {staff} role in this channel."),
)


def notice_embed(staff_role, custom=None, until=None):
    """Build the account security notice that is posted in the gulag channel."""
    staff = f"<@&{staff_role}>" if staff_role else "@Moderator"
    e = discord.Embed(title="Account Security Required", color=discord.Color.red())
    if custom:
        e.description = custom.replace("{staff}", staff)
        return e
    e.description = (
        "To get out of this channel, you need to secure your Discord account first.\n\n"
        f"Once you have completed all steps below, ping a member who has the {staff} role so a staff member can remove you from the gulag."
    )
    for name, text in STEPS:
        e.add_field(name=name, value=text.replace("{staff}", staff), inline=False)
    if until:
        e.add_field(name="Time", value=f"Automatic release <t:{until}:R>", inline=False)
    e.set_footer(text=emb().footer.text)
    return e


class Jail(commands.Cog):
    """Sends members to the gulag channel and releases them again."""
    grp = app_commands.Group(
        name="jailsetup",
        description="Gulag (jail) channel setup",
        default_permissions=discord.Permissions(manage_guild=True),
        guild_only=True,
    )

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot

    async def cog_load(self):
        """Start the background loop of this cog."""
        self.release_loop.start()

    async def cog_unload(self):
        """Stop the background loop of this cog."""
        self.release_loop.cancel()

    @tasks.loop(seconds=60)
    async def release_loop(self):
        """Release members whose jail time is over."""
        now = int(time.time())
        try:
            for guild in self.bot.guilds:
                timed = self.bot.cfg(guild.id)["jail"]["timed"]
                for uid, until in list(timed.items()):
                    if until > now:
                        continue
                    member = guild.get_member(int(uid))
                    if member:
                        await self.release(member, guild.me, "Jail time is over")
                    elif not self.bot.store.users(guild.id).get(uid, {}).get("jailed"):
                        timed.pop(uid, None)
        except Exception:
            log.exception("jail release loop failed")

    @release_loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected before the loop starts."""
        await self.bot.wait_until_ready()

    def parts(self, guild):
        """Return the jail settings with the jail role and channel objects."""
        j = self.bot.cfg(guild.id)["jail"]
        role = guild.get_role(j["role"]) if j["role"] else None
        channel = guild.get_channel(j["channel"]) if j["channel"] else None
        return j, role, channel

    async def send_to_jail(self, member, moderator, reason=None, auto=False, seconds=None, from_case=None):
        """Replace the roles of a member with the gulag role and post the notice. Returns (success, message)."""
        guild = member.guild
        j, role, channel = self.parts(guild)
        if not role or not channel:
            return False, "The gulag is not set up. Run /access jailsetup setup first."
        rec = self.bot.store.user(guild.id, member.id)
        if rec.get("jailed"):
            return False, "That member is already in the gulag."
        if member.id == guild.owner_id or member.top_role >= guild.me.top_role or role >= guild.me.top_role:
            return False, "My role is not high enough for that member."
        keep = [r for r in member.roles if not r.is_default() and not r.is_assignable()]
        saved = [r.id for r in member.roles if not r.is_default() and r.is_assignable()]
        try:
            await member.edit(roles=keep + [role], reason=f"Gulag: {reason or 'no reason'}")
        except discord.HTTPException as exc:
            return False, f"Discord refused: {exc}"
        rec["jailed"], rec["jail_roles"] = True, saved
        until = int(time.time()) + seconds if seconds else None
        if until:
            j["timed"][str(member.id)] = until
        if member.voice:
            try:
                await member.move_to(None)
            except discord.HTTPException as exc:
                log.warning("member.move_to failed: %s", exc)
        await self.bot.get_cog("Moderation").add_case(guild, "jail", member, moderator, reason, {"auto": auto, "seconds": seconds, "from_case": from_case})
        try:
            await channel.send(member.mention, embed=notice_embed(j["staff_role"], j["notice"], until), allowed_mentions=discord.AllowedMentions(users=[member]))
        except discord.HTTPException as exc:
            log.warning("channel.send failed: %s", exc)
        return True, f"{member.mention} was sent to the gulag" + (f" for {fmt_duration(seconds)}." if seconds else ".")

    async def release(self, member, moderator, reason=None):
        """Give a jailed member their old roles back. Returns (success, message)."""
        guild = member.guild
        j, role, channel = self.parts(guild)
        rec = self.bot.store.user(guild.id, member.id)
        if not rec.get("jailed"):
            return False, "That member is not in the gulag."
        restore = [guild.get_role(i) for i in rec.get("jail_roles", [])]
        roles = {r.id: r for r in member.roles if not r.is_default() and r != role}
        roles.update({r.id: r for r in restore if r and r.is_assignable()})
        try:
            await member.edit(roles=list(roles.values()), reason=f"Released: {reason or 'no reason'}")
        except discord.HTTPException as exc:
            return False, f"Discord refused: {exc}"
        rec["jailed"] = False
        rec.pop("jail_roles", None)
        j["timed"].pop(str(member.id), None)
        await self.bot.get_cog("Moderation").add_case(guild, "unjail", member, moderator, reason)
        return True, f"{member.mention} was released."

    async def apply_overwrites(self, guild, only=None):
        """Hide every channel from the gulag role except the gulag channel. Returns (succeeded, failed)."""
        j, role, gulag = self.parts(guild)
        if not role or not gulag:
            return 0, 0
        staff = guild.get_role(j["staff_role"]) if j["staff_role"] else None

        def make(ch):
            """Create the job that sets the permissions of one channel."""
            async def job():
                """Set the gulag permissions on one channel."""
                if ch.id == gulag.id:
                    await ch.set_permissions(guild.default_role, overwrite=discord.PermissionOverwrite(view_channel=False))
                    await ch.set_permissions(role, overwrite=discord.PermissionOverwrite(
                        view_channel=True, send_messages=True, read_message_history=True, attach_files=True,
                        embed_links=True, add_reactions=True, use_external_emojis=True, use_external_stickers=True))
                    if staff:
                        await ch.set_permissions(staff, overwrite=discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True))
                else:
                    await ch.set_permissions(role, overwrite=discord.PermissionOverwrite(view_channel=False))
            return job

        return await bulk([make(ch) for ch in ([only] if only else guild.channels)], limit=6)

    @commands.hybrid_command(name="jail", description="Send a member to the gulag channel")
    @app_commands.describe(member="Member to jail", duration="Optional, for example 30m, 2h, 1d", reason="Reason (optional)")
    async def jail_cmd(self, ctx, member: discord.Member, duration: Optional[str] = None, *, reason: Optional[str] = None):
        """Send a member to the gulag channel."""
        err = self.bot.get_cog("Moderation").target_error(ctx.guild, ctx.author, member)
        if err:
            return await ctx.send(err, ephemeral=True)
        secs = parse_duration(duration) if duration else None
        if duration and secs is None:
            reason = f"{duration} {reason or ''}".strip()
        ok, text = await self.send_to_jail(member, ctx.author, reason, seconds=secs)
        await ctx.send(text, ephemeral=not ok)

    @commands.hybrid_command(name="unjail", description="Release a member from the gulag")
    @app_commands.describe(member="Member to release", reason="Reason (optional)")
    async def unjail_cmd(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
        """Release a member from the gulag."""
        ok, text = await self.release(member, ctx.author, reason)
        await ctx.send(text, ephemeral=not ok)

    @commands.hybrid_command(name="jailed", description="List members who are in the gulag right now")
    async def jailed_cmd(self, ctx):
        """List members who are in the gulag right now."""
        timed = self.bot.cfg(ctx.guild.id)["jail"]["timed"]
        lines = []
        for uid, rec in self.bot.store.users(ctx.guild.id).items():
            if rec.get("jailed"):
                until = timed.get(uid)
                lines.append(f"<@{uid}> ({uid})" + (f", released <t:{until}:R>" if until else ", no time limit"))
        await ctx.send(embed=emb("In the gulag", "\n".join(lines[:40]) or "Nobody is in the gulag.", discord.Color.dark_red()), ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Runs when a member joins."""
        if member.bot or not self.bot.module_on(member.guild.id, "jail"):
            return
        rec = self.bot.store.users(member.guild.id).get(str(member.id))
        if rec and rec.get("jailed"):
            j, role, channel = self.parts(member.guild)
            if role:
                try:
                    await member.add_roles(role, reason="Rejoined while in the gulag")
                except discord.HTTPException as exc:
                    log.warning("member.add_roles failed: %s", exc)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, ch):
        """Runs when a channel is created."""
        if self.bot.module_on(ch.guild.id, "jail") and self.parts(ch.guild)[1]:
            await self.apply_overwrites(ch.guild, only=ch)

    @grp.command(name="setup", description="Create or select the gulag role, channel and staff role")
    @app_commands.describe(role="Gulag role", channel="Gulag channel", staff_role="Role that can see the gulag and release members")
    async def js_setup(self, it: discord.Interaction, role: Optional[discord.Role] = None, channel: Optional[discord.TextChannel] = None, staff_role: Optional[discord.Role] = None):
        """Create or select the gulag role, channel and staff role."""
        await it.response.defer(ephemeral=True)
        await it.followup.send(await self.build(it.guild, role, channel, staff_role))

    async def build(self, guild, role=None, channel=None, staff_role=None):
        """Create what is missing of the gulag, apply the permissions and return a status text."""
        j = self.bot.cfg(guild.id)["jail"]
        if role:
            j["role"] = role.id
        if channel:
            j["channel"] = channel.id
        if staff_role:
            j["staff_role"] = staff_role.id
        try:
            if not guild.get_role(j["role"] or 0):
                new = await guild.create_role(name="Gulag", colour=discord.Colour.dark_grey(), permissions=discord.Permissions.none(), reason="Gulag setup")
                j["role"] = new.id
            if not guild.get_channel(j["channel"] or 0):
                ch = await guild.create_text_channel("gulag", reason="Gulag setup")
                j["channel"] = ch.id
        except discord.HTTPException as exc:
            return f"Setup failed: {exc}"
        if not guild.get_role(j["role"]).is_assignable():
            return "I cannot assign the gulag role. Move my bot role above it and run the command again."
        n, failed = await self.apply_overwrites(guild)
        note = f" {failed} channels failed, check my Manage Channels permission." if failed else ""
        return f"Gulag ready: role <@&{j['role']}>, channel <#{j['channel']}>. Permissions applied to {n} channels.{note}"

    @grp.command(name="apply", description="Apply the gulag permissions to all channels again")
    async def js_apply(self, it: discord.Interaction):
        """Apply the gulag permissions to all channels again."""
        await it.response.defer(ephemeral=True)
        n, failed = await self.apply_overwrites(it.guild)
        await it.followup.send(f"Applied to {n} channels." + (f" {failed} failed, check my permissions." if failed else ""))

    @grp.command(name="notice", description="Set a custom notice text (empty = default security steps)")
    async def js_notice(self, it: discord.Interaction, text: Optional[str] = None):
        """Set a custom notice text (empty = default security steps)."""
        self.bot.cfg(it.guild_id)["jail"]["notice"] = text.replace("\\n", "\n") if text else None
        await it.response.send_message(i18n.say(it.client, it.guild, "Notice updated."), ephemeral=True)

    @grp.command(name="preview", description="Preview the notice")
    async def js_preview(self, it: discord.Interaction):
        """Preview the notice."""
        j = self.bot.cfg(it.guild_id)["jail"]
        await it.response.send_message(embed=notice_embed(j["staff_role"], j["notice"]), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Jail(bot))
