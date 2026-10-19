# Copyright (c) Justyn
import asyncio
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import emb

STEPS = (
    ("1\ufe0f\u20e3 Reset Your Password", "Change your Discord password immediately."),
    ("2\ufe0f\u20e3 Enable 2FA", "Make sure Two-Factor Authentication is enabled on your account."),
    ("3\ufe0f\u20e3 Check Suspicious Devices", "Go through your logged-in devices and remove anything you do not recognize."),
    (
        "4\ufe0f\u20e3 Remove Suspicious Authorized Apps",
        "Go to User Settings \u2192 Authorized Apps and remove anything suspicious.\n\n"
        "Especially remove apps that say things like \"join servers for you\" or anything you do not remember authorizing.",
    ),
    (
        "5\ufe0f\u20e3 Clear Browser Data",
        "Sign out of Discord in your browsers, then clear browser cookies, cached files, and saved site data. "
        "This removes old login sessions that may still be compromised.",
    ),
    ("6\ufe0f\u20e3 Ping Staff", "After doing all of this, ping a member who has the {staff} role in this channel."),
)


def notice_embed(staff_role, custom=None):
    staff = f"<@&{staff_role}>" if staff_role else "@Moderator"
    e = discord.Embed(title="\U0001F510 Account Security Required", color=discord.Color.red())
    if custom:
        e.description = custom.replace("{staff}", staff)
        return e
    e.description = (
        "To get out of this channel, you need to secure your Discord account first.\n\n"
        f"Once you have completed all steps below, ping a member who has the {staff} role so a staff member can remove you from the gulag."
    )
    for name, text in STEPS:
        e.add_field(name=name, value=text.replace("{staff}", staff), inline=False)
    e.set_footer(text=emb().footer.text)
    return e


class Jail(commands.Cog):
    grp = app_commands.Group(
        name="jailsetup",
        description="Gulag (jail) channel setup",
        default_permissions=discord.Permissions(manage_guild=True),
        guild_only=True,
    )

    def __init__(self, bot):
        self.bot = bot

    def parts(self, guild):
        j = self.bot.cfg(guild.id)["jail"]
        role = guild.get_role(j["role"]) if j["role"] else None
        channel = guild.get_channel(j["channel"]) if j["channel"] else None
        return j, role, channel

    async def send_to_jail(self, member, moderator, reason=None, auto=False):
        guild = member.guild
        j, role, channel = self.parts(guild)
        if not role or not channel:
            return False, "The gulag is not set up. Run /jailsetup setup first."
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
        self.bot.store.mark("users")
        if member.voice:
            try:
                await member.move_to(None)
            except discord.HTTPException:
                pass
        await self.bot.get_cog("Moderation").add_case(guild, "jail", member, moderator, reason, {"auto": auto})
        try:
            await channel.send(member.mention, embed=notice_embed(j["staff_role"], j["notice"]), allowed_mentions=discord.AllowedMentions(users=[member]))
        except discord.HTTPException:
            pass
        return True, f"{member.mention} was sent to the gulag."

    async def release(self, member, moderator, reason=None):
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
        self.bot.store.mark("users")
        await self.bot.get_cog("Moderation").add_case(guild, "unjail", member, moderator, reason)
        return True, f"{member.mention} was released."

    async def apply_overwrites(self, guild, only=None):
        j, role, gulag = self.parts(guild)
        if not role or not gulag:
            return 0
        staff = guild.get_role(j["staff_role"]) if j["staff_role"] else None
        n = 0
        for ch in ([only] if only else guild.channels):
            try:
                if ch.id == gulag.id:
                    await ch.set_permissions(guild.default_role, overwrite=discord.PermissionOverwrite(view_channel=False))
                    await ch.set_permissions(role, overwrite=discord.PermissionOverwrite(
                        view_channel=True, send_messages=True, read_message_history=True, attach_files=True,
                        embed_links=True, add_reactions=True, use_external_emojis=True, use_external_stickers=True))
                    if staff:
                        await ch.set_permissions(staff, overwrite=discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True))
                else:
                    await ch.set_permissions(role, overwrite=discord.PermissionOverwrite(view_channel=False))
                n += 1
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.3)
        return n

    @commands.hybrid_command(name="jail", description="Send a member to the gulag channel")
    @app_commands.describe(member="Member to jail", reason="Reason (optional)")
    async def jail_cmd(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
        err = self.bot.get_cog("Moderation").target_error(ctx.guild, ctx.author, member)
        if err:
            return await ctx.send(err, ephemeral=True)
        ok, text = await self.send_to_jail(member, ctx.author, reason)
        await ctx.send(text, ephemeral=not ok)

    @commands.hybrid_command(name="unjail", description="Release a member from the gulag")
    @app_commands.describe(member="Member to release", reason="Reason (optional)")
    async def unjail_cmd(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
        ok, text = await self.release(member, ctx.author, reason)
        await ctx.send(text, ephemeral=not ok)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot or not self.bot.module_on(member.guild.id, "jail"):
            return
        rec = self.bot.store.users(member.guild.id).get(str(member.id))
        if rec and rec.get("jailed"):
            j, role, channel = self.parts(member.guild)
            if role:
                try:
                    await member.add_roles(role, reason="Rejoined while in the gulag")
                except discord.HTTPException:
                    pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, ch):
        if self.bot.module_on(ch.guild.id, "jail") and self.parts(ch.guild)[1]:
            await self.apply_overwrites(ch.guild, only=ch)

    @grp.command(name="setup", description="Create or select the gulag role, channel and staff role")
    @app_commands.describe(role="Gulag role", channel="Gulag channel", staff_role="Role that can see the gulag and release members")
    async def js_setup(self, it: discord.Interaction, role: Optional[discord.Role] = None, channel: Optional[discord.TextChannel] = None, staff_role: Optional[discord.Role] = None):
        await it.response.defer(ephemeral=True)
        guild, j = it.guild, self.bot.cfg(it.guild_id)["jail"]
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
            return await it.followup.send(f"Setup failed: {exc}")
        self.bot.store.mark("config")
        if not guild.get_role(j["role"]).is_assignable():
            return await it.followup.send("I cannot assign the gulag role. Move my bot role above it and run the command again.")
        n = await self.apply_overwrites(guild)
        await it.followup.send(f"Gulag ready: role <@&{j['role']}>, channel <#{j['channel']}>. Permissions applied to {n} channels.")

    @grp.command(name="apply", description="Apply the gulag permissions to all channels again")
    async def js_apply(self, it: discord.Interaction):
        await it.response.defer(ephemeral=True)
        n = await self.apply_overwrites(it.guild)
        await it.followup.send(f"Applied to {n} channels.")

    @grp.command(name="notice", description="Set a custom notice text (empty = default security steps)")
    async def js_notice(self, it: discord.Interaction, text: Optional[str] = None):
        self.bot.cfg(it.guild_id)["jail"]["notice"] = text.replace("\\n", "\n") if text else None
        self.bot.store.mark("config")
        await it.response.send_message("Notice updated.", ephemeral=True)

    @grp.command(name="preview", description="Preview the notice")
    async def js_preview(self, it: discord.Interaction):
        j = self.bot.cfg(it.guild_id)["jail"]
        await it.response.send_message(embed=notice_embed(j["staff_role"], j["notice"]), ephemeral=True)


async def setup(bot):
    await bot.add_cog(Jail(bot))
