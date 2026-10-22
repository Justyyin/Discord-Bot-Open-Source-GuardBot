"""Verification gate with button, captcha or math question."""

import io
import logging
import random
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from .. import i18n
from ..images import HAVE_PIL, captcha, new_code
from ..utils import bulk, emb

log = logging.getLogger(__name__)


class CodeModal(discord.ui.Modal, title="Verification"):
    """Form in which the member types the captcha or math answer."""
    answer = discord.ui.TextInput(label="Your answer", max_length=12)

    def __init__(self, cog):
        """Create the answer form."""
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction):
        """Hand the typed answer to the verification check."""
        await self.cog.check_answer(interaction, str(self.answer.value))


class CodeView(discord.ui.View):
    """Ephemeral view with the button that opens the answer form."""
    def __init__(self, cog):
        """Create the view with the button that opens the answer form."""
        super().__init__(timeout=180)
        self.cog = cog

    @discord.ui.button(label="Enter answer", style=discord.ButtonStyle.primary)
    async def enter(self, interaction, button):
        """Open the answer form."""
        await interaction.response.send_modal(CodeModal(self.cog))


class VerifyButton(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:verify"):
    """Persistent button that starts the verification."""
    def __init__(self):
        """Create the verification button."""
        super().__init__(discord.ui.Button(label="Verify", style=discord.ButtonStyle.success, custom_id="gb:verify"))

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls()

    async def callback(self, interaction):
        """Start the verification for the member who pressed the button."""
        await interaction.client.get_cog("Verify").start(interaction)


class Verify(commands.Cog):
    """Verification gate for new members."""
    grp = app_commands.Group(name="verify", description="Verification gate", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot
        self.codes = {}
        bot.add_dynamic_items(VerifyButton)

    async def cog_load(self):
        """Start the background loop of this cog."""
        self.timeout_loop.start()

    async def cog_unload(self):
        """Stop the background loop of this cog."""
        self.timeout_loop.cancel()

    def conf(self, gid):
        """Return the verification settings of a server."""
        return self.bot.cfg(gid)["verify"]

    def roles(self, guild):
        """Return the verified and unverified role objects, either may be None."""
        v = self.conf(guild.id)
        return (guild.get_role(v["verified_role"]) if v["verified_role"] else None, guild.get_role(v["unverified_role"]) if v["unverified_role"] else None)

    async def finish(self, member):
        """Give the verified role, remove the unverified role and clear the pending entry."""
        v = self.conf(member.guild.id)
        verified, unverified = self.roles(member.guild)
        try:
            if verified:
                await member.add_roles(verified, reason="Verified")
            if unverified and unverified in member.roles:
                await member.remove_roles(unverified, reason="Verified")
        except discord.HTTPException:
            return False
        v["pending"].pop(str(member.id), None)
        return True

    async def start(self, interaction):
        """Check the requirements and then verify at once or ask for a captcha or math answer."""
        guild, member = interaction.guild, interaction.user
        if not self.bot.module_on(guild.id, "verification"):
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Verification is turned off."), ephemeral=True)
        v = self.conf(guild.id)
        verified, _ = self.roles(guild)
        if verified and verified in member.roles:
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "You are already verified."), ephemeral=True)
        age = (discord.utils.utcnow() - member.created_at).days
        if v["min_age_days"] and age < v["min_age_days"]:
            return await interaction.response.send_message(f"Your account must be at least {v['min_age_days']} days old.", ephemeral=True)
        mode = v["mode"]
        if mode == "button":
            ok = await self.finish(member)
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "You are verified. Welcome.") if ok else "I could not change your roles. Please contact a moderator.", ephemeral=True)
        key = (guild.id, member.id)
        if mode == "captcha" and HAVE_PIL:
            code = new_code()
            data = captcha(code)
            self.codes[key] = [code, time.time() + 180, 0]
            return await interaction.response.send_message(
                i18n.say(interaction.client, interaction.guild, "Type the characters from the image."), file=discord.File(io.BytesIO(data), filename="captcha.png"), view=CodeView(self), ephemeral=True)
        a, b = random.randint(2, 12), random.randint(2, 12)
        self.codes[key] = [str(a + b), time.time() + 180, 0]
        await interaction.response.send_message(f"What is {a} + {b}?", view=CodeView(self), ephemeral=True)

    async def check_answer(self, interaction, answer):
        """Compare the answer with the stored code and allow three tries."""
        key = (interaction.guild_id, interaction.user.id)
        item = self.codes.get(key)
        if not item or item[1] < time.time():
            self.codes.pop(key, None)
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "The code expired. Press Verify again."), ephemeral=True)
        if answer.strip().upper() == item[0]:
            self.codes.pop(key, None)
            ok = await self.finish(interaction.user)
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "You are verified. Welcome.") if ok else "I could not change your roles. Please contact a moderator.", ephemeral=True)
        item[2] += 1
        if item[2] >= 3:
            self.codes.pop(key, None)
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Too many wrong answers. Press Verify to get a new code."), ephemeral=True)
        await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Wrong answer. Try again with the button."), ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Runs when a member joins."""
        if member.bot or not self.bot.module_on(member.guild.id, "verification"):
            return
        v = self.conf(member.guild.id)
        _, unverified = self.roles(member.guild)
        if not unverified or not v["channel"]:
            return
        try:
            await member.add_roles(unverified, reason="Verification pending")
            v["pending"][str(member.id)] = int(time.time())
        except discord.HTTPException as exc:
            log.warning("member.add_roles failed: %s", exc)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Runs when a member leaves or is removed."""
        self.conf(member.guild.id)["pending"].pop(str(member.id), None)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, ch):
        """Runs when a channel is created."""
        if self.bot.module_on(ch.guild.id, "verification"):
            await self.apply(ch.guild, only=ch)

    @tasks.loop(seconds=60)
    async def timeout_loop(self):
        """Kick members who did not verify within the configured time."""
        now = int(time.time())
        try:
            for guild in self.bot.guilds:
                v = self.conf(guild.id)
                if not self.bot.module_on(guild.id, "verification") or not v["timeout_minutes"]:
                    continue
                verified, unverified = self.roles(guild)
                for uid, ts in list(v["pending"].items()):
                    if now - ts < v["timeout_minutes"] * 60:
                        continue
                    m = guild.get_member(int(uid))
                    v["pending"].pop(uid, None)
                    if m and (not verified or verified not in m.roles):
                        try:
                            await m.kick(reason="Did not verify in time")
                            self.bot.log(guild, "members", emb("Kicked: did not verify", color=discord.Color.orange(), user=m))
                        except discord.HTTPException as exc:
                            log.warning("m.kick failed: %s", exc)
        except Exception:
            log.exception("verification timeout loop failed")

    @timeout_loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected before the loop starts."""
        await self.bot.wait_until_ready()

    async def apply(self, guild, only=None):
        """Hide all channels except the verification channel from the unverified role. Returns (succeeded, failed)."""
        v = self.conf(guild.id)
        verified, unverified = self.roles(guild)
        gate = guild.get_channel(v["channel"]) if v["channel"] else None
        if not unverified or not gate:
            return 0, 0

        def make(ch):
            """Create the job that sets the permissions of one channel."""
            async def job():
                """Set the verification permissions on one channel."""
                if ch.id == gate.id:
                    await ch.set_permissions(unverified, overwrite=discord.PermissionOverwrite(view_channel=True, send_messages=False, read_message_history=True, add_reactions=False))
                    if verified:
                        await ch.set_permissions(verified, overwrite=discord.PermissionOverwrite(view_channel=False))
                else:
                    await ch.set_permissions(unverified, overwrite=discord.PermissionOverwrite(view_channel=False))
            return job

        return await bulk([make(ch) for ch in ([only] if only else guild.channels)], limit=6)

    @grp.command(name="setup", description="Set up the verification gate and post the panel")
    @app_commands.describe(channel="Channel with the verify button", verified_role="Role for verified members (created if empty)", unverified_role="Role for new members (created if empty)", mode="button, captcha (image) or math", timeout_minutes="Kick members who do not verify in time (0 = never)", min_account_age_days="Refuse accounts younger than this")
    async def v_setup(self, it: discord.Interaction, channel: discord.TextChannel, verified_role: Optional[discord.Role] = None, unverified_role: Optional[discord.Role] = None, mode: Optional[Literal["button", "captcha", "math"]] = None, timeout_minutes: Optional[app_commands.Range[int, 0, 10080]] = None, min_account_age_days: Optional[app_commands.Range[int, 0, 365]] = None):
        """Set up the verification gate and post the panel."""
        await it.response.defer(ephemeral=True)
        guild, g = it.guild, self.bot.cfg(it.guild_id)
        v = g["verify"]
        v["channel"] = channel.id
        for key, role, name in (("verified_role", verified_role, "Verified"), ("unverified_role", unverified_role, "Unverified")):
            if role:
                v[key] = role.id
            elif not (v[key] and guild.get_role(v[key])):
                try:
                    v[key] = (await guild.create_role(name=name, reason="Verification setup")).id
                except discord.HTTPException as exc:
                    return await it.followup.send(f"Could not create the {name} role: {exc}")
        if mode:
            v["mode"] = mode
        if timeout_minutes is not None:
            v["timeout_minutes"] = timeout_minutes
        if min_account_age_days is not None:
            v["min_age_days"] = min_account_age_days
        verified, unverified = self.roles(guild)
        if not unverified.is_assignable() or not verified.is_assignable():
            return await it.followup.send(i18n.say(it.client, it.guild, "I cannot assign the verification roles. Move my bot role above them and run the command again."))
        g["modules"]["verification"] = True
        text = {"button": "Press the button to verify and unlock the server.", "captcha": "Press the button and solve the captcha to unlock the server.", "math": "Press the button and answer a short question to unlock the server."}[v["mode"]]
        view = discord.ui.View(timeout=None)
        view.add_item(VerifyButton())
        try:
            await channel.send(embed=emb("Verification", text), view=view)
        except discord.HTTPException:
            return await it.followup.send(i18n.say(it.client, it.guild, "I cannot post in that channel."))
        n, failed = await self.apply(guild)
        note = f" {failed} channels failed, check my Manage Channels permission." if failed else ""
        await it.followup.send(f"Verification is on. Mode {v['mode']}, roles {verified.mention} and {unverified.mention}. Permissions set on {n} channels.{note} New members get the unverified role and only see {channel.mention}.")

    @grp.command(name="panel", description="Post the verification panel again")
    async def v_panel(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None):
        """Post the verification panel again."""
        v = self.conf(it.guild_id)
        channel = channel or it.guild.get_channel(v["channel"] or 0)
        if not channel:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Run /verify setup first."), ephemeral=True)
        view = discord.ui.View(timeout=None)
        view.add_item(VerifyButton())
        await channel.send(embed=emb("Verification", "Press the button to verify and unlock the server."), view=view)
        await it.response.send_message(i18n.say(it.client, it.guild, "Panel posted."), ephemeral=True)

    @grp.command(name="apply", description="Apply the channel permissions again")
    async def v_apply(self, it: discord.Interaction):
        """Apply the channel permissions again."""
        await it.response.defer(ephemeral=True)
        n, failed = await self.apply(it.guild)
        await it.followup.send(f"Applied to {n} channels." + (f" {failed} failed, check my permissions." if failed else ""))

    @grp.command(name="status", description="Show the verification settings")
    async def v_status(self, it: discord.Interaction):
        """Show the verification settings."""
        v = self.conf(it.guild_id)
        on = self.bot.module_on(it.guild_id, "verification")
        text = (
            f"Status: {'on' if on else 'off'}\nMode: {v['mode']}\n"
            f"Channel: {('<#' + str(v['channel']) + '>') if v['channel'] else 'not set'}\n"
            f"Verified role: {('<@&' + str(v['verified_role']) + '>') if v['verified_role'] else 'not set'}\n"
            f"Unverified role: {('<@&' + str(v['unverified_role']) + '>') if v['unverified_role'] else 'not set'}\n"
            f"Kick after: {v['timeout_minutes'] or 'never'} minutes\nMinimum account age: {v['min_age_days']} days\nWaiting to verify: {len(v['pending'])}"
        )
        await it.response.send_message(text, ephemeral=True)

    @grp.command(name="off", description="Turn the verification gate off")
    async def v_off(self, it: discord.Interaction):
        """Turn the verification gate off."""
        self.bot.cfg(it.guild_id)["modules"]["verification"] = False
        await it.response.send_message(i18n.say(it.client, it.guild, "Verification is off. Existing roles and permissions stay as they are."), ephemeral=True)

    @grp.command(name="member", description="Verify a member manually")
    async def v_member(self, it: discord.Interaction, member: discord.Member):
        """Verify a member manually."""
        ok = await self.finish(member)
        await it.response.send_message(f"{member.mention} verified." if ok else "I could not change the roles.", ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Verify(bot))
