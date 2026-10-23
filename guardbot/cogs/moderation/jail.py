"""The gulag: restricted channel for hacked accounts, with optional release time."""

import logging
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ... import i18n
from ...utils import bulk, emb, fmt_duration, parse_duration

log = logging.getLogger(__name__)

LOCK = "\U0001F510"
KEYCAPS = tuple(f"{n}\ufe0f\u20e3" for n in range(1, 10))
STEPS = (
    ("Reset Your Password", "Change your Discord password immediately."),
    ("Enable 2FA", "Make sure **Two-Factor Authentication** is enabled on your account."),
    ("Check Suspicious Devices", "Go through your logged-in devices and remove anything you do not recognize."),
    (
        "Remove Suspicious Authorized Apps",
        "Go to **User Settings** \u2192 **Authorized Apps** and remove anything suspicious.\n\n"
        "Especially remove apps that say things like **\"join servers for you\"** or anything you do not remember authorizing.",
    ),
    (
        "Clear Browser Data",
        "Sign out of Discord in your browsers, then clear browser cookies, cached files, and saved site data. "
        "This removes old login sessions that may still be compromised.",
    ),
    ("Ping Staff", "After doing all of this, ping a member who has the {staff} role in this channel."),
)
NOTICE_TITLE = "Account Security Required"
NOTICE_TEXT = (
    "To get out of this channel, you need to secure your Discord account first.\n\n"
    "Once you have completed all steps below, ping a member who has the {staff} role so a staff member can remove you from the gulag."
)
NOTICE_FOOTER = "Account Safety Check"
REMINDER_TITLE = "Account Recovery Reminder"
REMINDER_TEXT = "If you've been hacked previously and want to get out of here, please run:"
REMINDER_FOOTER = "This reminder refreshes every {minutes} minutes."
TEXTS = (
    NOTICE_TITLE, NOTICE_TEXT, NOTICE_FOOTER, REMINDER_TITLE, REMINDER_TEXT, REMINDER_FOOTER,
    "Automatic release <t:{until}:R>", "Time", "Release request",
    "{user} says the security steps are done and asks to be released.",
    "You asked already. A staff member will answer soon.",
    "Released by {user}.", "Stays in the gulag, decided by {user}.", "Only staff can decide this.",
)
OWN_EDIT_SECONDS = 15


def plain(text, **values):
    """Fill placeholders without translating, for previews and tests."""
    for key, value in values.items():
        text = text.replace("{" + key + "}", str(value))
    return text


def notice_embed(staff_role, custom=None, until=None, tr=None, guild=None):
    """Build the account security notice that is posted in the gulag channel. `tr` translates a text into the language of the server."""
    tr = tr or plain
    staff = f"<@&{staff_role}>" if staff_role else "@Moderator"
    e = discord.Embed(title=f"{LOCK} {tr(NOTICE_TITLE)}", color=discord.Color.red(), timestamp=discord.utils.utcnow())
    icon = guild.icon.url if guild is not None and getattr(guild, "icon", None) else None
    e.set_footer(text=tr(NOTICE_FOOTER), icon_url=icon)
    if custom:
        e.description = custom.replace("{staff}", staff)
        return e
    e.description = tr(NOTICE_TEXT, staff=staff)
    for (name, text), key in zip(STEPS, KEYCAPS):
        e.add_field(name=f"{key} {tr(name)}", value=tr(text, staff=staff), inline=False)
    if until:
        e.add_field(name=tr("Time"), value=tr("Automatic release <t:{until}:R>", until=until), inline=False)
    return e


def reminder_embed(command, minutes, tr=None):
    """The reminder in the gulag channel that tells members how to ask for their release."""
    tr = tr or plain
    e = discord.Embed(title=f"{LOCK} {tr(REMINDER_TITLE)}", description=f"{tr(REMINDER_TEXT)}\n```\n{command}\n```", color=discord.Color.gold(), timestamp=discord.utils.utcnow())
    e.set_footer(text=tr(REMINDER_FOOTER, minutes=minutes))
    return e


def is_staff(member, j):
    """True for members with the staff role of the gulag or the Manage Roles permission."""
    return member.guild_permissions.manage_roles or any(r.id == j["staff_role"] for r in getattr(member, "roles", []))


class ReleaseButton(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:jr:(?P<uid>\d+):(?P<act>release|keep)"):
    """Buttons under a release request. Only staff can use them, and they work after a restart."""

    def __init__(self, uid, act, label=None):
        """Create one of the two buttons."""
        style = discord.ButtonStyle.success if act == "release" else discord.ButtonStyle.secondary
        super().__init__(discord.ui.Button(label=label or ("Release" if act == "release" else "Keep"), style=style, custom_id=f"gb:jr:{uid}:{act}"))
        self.uid, self.act = int(uid), act

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id."""
        return cls(match["uid"], match["act"], item.label)

    async def callback(self, interaction):
        """Release the member or leave them in the gulag."""
        cog = interaction.client.get_cog("Jail")
        guild = interaction.guild
        j = interaction.client.cfg(guild.id)["jail"]
        if cog is None or not is_staff(interaction.user, j):
            return await interaction.response.send_message(i18n.say(interaction.client, guild, "Only staff can decide this."), ephemeral=True)
        member = guild.get_member(self.uid)
        if self.act == "release":
            if member is None:
                text = "That member is not on the server."
            else:
                ok, text = await cog.release(member, interaction.user, "Release request accepted")
                if ok:
                    text = i18n.say(interaction.client, guild, "Released by {user}.", user=interaction.user.mention)
        else:
            text = i18n.say(interaction.client, guild, "Stays in the gulag, decided by {user}.", user=interaction.user.mention)
        await interaction.response.edit_message(content=text, view=None, allowed_mentions=discord.AllowedMentions.none())


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
        self.own = {}
        self.asked = {}
        self.reminded = {}
        bot.add_dynamic_items(ReleaseButton)

    async def cog_load(self):
        """Start the background loops of this cog."""
        self.release_loop.start()
        self.reminder_loop.start()

    async def cog_unload(self):
        """Stop the background loops of this cog."""
        self.release_loop.cancel()
        self.reminder_loop.cancel()

    def tr(self, guild):
        """A function that translates texts into the language of a server."""
        return lambda text, **values: i18n.say(self.bot, guild, text, **values)

    def mark_own(self, member):
        """Remember that the bot itself changes the roles of a member right now, so the role listener ignores it."""
        now = time.time()
        self.own = {k: t for k, t in self.own.items() if now - t < OWN_EDIT_SECONDS}
        self.own[(member.guild.id, member.id)] = now

    def own_edit(self, member):
        """True if the bot changed the roles of this member a moment ago."""
        return time.time() - self.own.get((member.guild.id, member.id), 0) < OWN_EDIT_SECONDS

    async def post_notice(self, member, until=None):
        """Post the account security notice with a mention of the member in the gulag channel."""
        j, role, channel = self.parts(member.guild)
        if channel is None or not j["security_notice"]:
            return
        embed = notice_embed(j["staff_role"], j["notice"], until, tr=self.tr(member.guild), guild=member.guild)
        try:
            await channel.send(member.mention, embed=embed, allowed_mentions=discord.AllowedMentions(users=[member]))
        except discord.HTTPException as exc:
            log.warning("gulag notice could not be posted: %s", exc)

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
        self.mark_own(member)
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
        await self.post_notice(member, until)
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
        self.mark_own(member)
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
                self.mark_own(member)
                try:
                    await member.add_roles(role, reason="Rejoined while in the gulag")
                except discord.HTTPException as exc:
                    log.warning("member.add_roles failed: %s", exc)
                    return
                await self.post_notice(member, self.bot.cfg(member.guild.id)["jail"]["timed"].get(str(member.id)))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """A moderator or another bot gave or took the gulag role by hand: post the notice and keep the gulag list right."""
        if after.bot or not self.bot.module_on(after.guild.id, "jail"):
            return
        j, role, channel = self.parts(after.guild)
        if role is None or self.own_edit(after):
            return
        had, has = role in before.roles, role in after.roles
        if had == has:
            return
        rec = self.bot.store.user(after.guild.id, after.id)
        if has and not rec.get("jailed"):
            rec["jailed"], rec["jail_roles"] = True, []
            await self.post_notice(after)
        elif had and rec.get("jailed"):
            rec["jailed"] = False
            rec.pop("jail_roles", None)
            j["timed"].pop(str(after.id), None)

    def in_jail(self, member):
        """True if a member is in the gulag, by the stored state or by the role."""
        j, role, channel = self.parts(member.guild)
        rec = self.bot.store.users(member.guild.id).get(str(member.id)) or {}
        return bool(rec.get("jailed")) or (role is not None and role in getattr(member, "roles", []))

    def claims(self, message):
        """True if a message is the release request of a member in the gulag. The command handler then ignores it, so the moderation command with the same name does not answer."""
        if message.author.bot or message.guild is None or not message.content:
            return False
        if not self.bot.module_on(message.guild.id, "jail"):
            return False
        j, role, channel = self.parts(message.guild)
        if channel is None or message.channel.id != channel.id or not j["release_requests"]:
            return False
        word = self.bot.prefix_for(message.guild.id) + j["release_word"]
        return message.content.strip().lower() == word.lower() and self.in_jail(message.author)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Turn the release word of a member in the gulag into a request for the staff."""
        if not self.claims(message):
            return
        guild, member = message.guild, message.author
        j = self.bot.cfg(guild.id)["jail"]
        key, now = (guild.id, member.id), time.time()
        if now - self.asked.get(key, 0) < j["reminder_minutes"] * 60:
            try:
                await message.reply(i18n.say(self.bot, guild, "You asked already. A staff member will answer soon."), mention_author=False)
            except discord.HTTPException:
                pass
            return
        self.asked[key] = now
        staff = guild.get_role(j["staff_role"]) if j["staff_role"] else None
        e = discord.Embed(title=i18n.say(self.bot, guild, "Release request"), description=i18n.say(self.bot, guild, "{user} says the security steps are done and asks to be released.", user=member.mention), color=discord.Color.orange(), timestamp=discord.utils.utcnow())
        view = discord.ui.View(timeout=None)
        view.add_item(ReleaseButton(member.id, "release"))
        view.add_item(ReleaseButton(member.id, "keep"))
        try:
            await message.channel.send(staff.mention if staff else None, embed=e, view=view, allowed_mentions=discord.AllowedMentions(roles=[staff] if staff else False))
        except discord.HTTPException as exc:
            log.warning("release request could not be posted: %s", exc)

    @tasks.loop(minutes=1)
    async def reminder_loop(self):
        """Keep one reminder at the bottom of every gulag channel while someone is in the gulag."""
        now = time.time()
        for guild in list(self.bot.guilds):
            try:
                await self.refresh_reminder(guild, now)
            except Exception:
                log.exception("gulag reminder failed in %s", guild.id)

    async def refresh_reminder(self, guild, now):
        """Post, move or remove the reminder of one server."""
        j, role, channel = self.parts(guild)
        if channel is None or role is None:
            return
        anyone = bool(role.members) or any(r.get("jailed") for r in self.bot.store.users(guild.id).values())
        active = self.bot.module_on(guild.id, "jail") and j["reminder"] and anyone
        old = j.get("reminder_message")
        if not active:
            if old:
                j["reminder_message"] = None
                try:
                    await channel.get_partial_message(old).delete()
                except discord.HTTPException:
                    pass
            return
        if now - self.reminded.get(guild.id, 0) < j["reminder_minutes"] * 60 and old:
            return
        self.reminded[guild.id] = now
        embed = reminder_embed(self.bot.prefix_for(guild.id) + j["release_word"], j["reminder_minutes"], tr=self.tr(guild))
        if old and channel.last_message_id == old:
            try:
                await channel.get_partial_message(old).edit(embed=embed)
                return
            except discord.HTTPException:
                pass
        if old:
            try:
                await channel.get_partial_message(old).delete()
            except discord.HTTPException:
                pass
        try:
            msg = await channel.send(embed=embed)
            j["reminder_message"] = msg.id
        except discord.HTTPException as exc:
            log.warning("gulag reminder could not be posted: %s", exc)

    @reminder_loop.before_loop
    async def _wait_reminder(self):
        """Wait until the bot is connected."""
        await self.bot.wait_until_ready()

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

    @grp.command(name="preview", description="Preview the notice and the reminder")
    async def js_preview(self, it: discord.Interaction):
        """Preview the notice and the reminder."""
        j = self.bot.cfg(it.guild_id)["jail"]
        tr = self.tr(it.guild)
        embeds = [notice_embed(j["staff_role"], j["notice"], tr=tr, guild=it.guild), reminder_embed(self.bot.prefix_for(it.guild_id) + j["release_word"], j["reminder_minutes"], tr=tr)]
        await it.response.send_message(it.user.mention, embeds=embeds, ephemeral=True)

    @grp.command(name="reminder", description="Notice, reminder and release requests of the gulag")
    @app_commands.describe(
        notice="Post the account security notice with a mention for everyone who comes into the gulag",
        reminder="Keep a reminder at the bottom of the gulag channel while someone is in it",
        minutes="How often the reminder is renewed",
        requests="Let members in the gulag ask for their release with the release word",
        word="Release word after the prefix, for example unban",
    )
    async def js_reminder(self, it: discord.Interaction, notice: Optional[bool] = None, reminder: Optional[bool] = None, minutes: Optional[app_commands.Range[int, 1, 1440]] = None, requests: Optional[bool] = None, word: Optional[app_commands.Range[str, 1, 30]] = None):
        """Change the notice, the reminder and the release requests."""
        j = self.bot.cfg(it.guild_id)["jail"]
        if word is not None:
            word = word.strip().lower()
            if not word or any(c.isspace() for c in word):
                return await it.response.send_message(i18n.say(it.client, it.guild, "The release word must be one word."), ephemeral=True)
            j["release_word"] = word
        for key, value in (("security_notice", notice), ("reminder", reminder), ("reminder_minutes", minutes), ("release_requests", requests)):
            if value is not None:
                j[key] = value
        self.reminded.pop(it.guild_id, None)
        await it.response.send_message(i18n.say(
            it.client, it.guild, "Notice {notice}, reminder {reminder} every {minutes} minutes, release requests {requests} with {command}.",
            notice="on" if j["security_notice"] else "off", reminder="on" if j["reminder"] else "off", minutes=j["reminder_minutes"],
            requests="on" if j["release_requests"] else "off", command=self.bot.prefix_for(it.guild_id) + j["release_word"]), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Jail(bot))
