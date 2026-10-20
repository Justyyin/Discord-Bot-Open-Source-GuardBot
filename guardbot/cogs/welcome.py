"""Welcome and goodbye messages, auto roles and booster rewards."""

import logging
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

log = logging.getLogger(__name__)


def fmt(text, member, guild):
    """Fill the placeholders {user}, {name}, {server} and {count} in a message."""
    return (
        text.replace("{user}", member.mention)
        .replace("{name}", member.display_name)
        .replace("{server}", guild.name)
        .replace("{count}", str(guild.member_count))
    )


class Welcome(commands.Cog):
    """Welcome, goodbye, auto roles and booster rewards."""
    wg = app_commands.Group(name="welcome", description="Welcome messages and auto roles", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    bg = app_commands.Group(name="booster", description="Booster rewards", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Runs when a member joins."""
        if not self.bot.module_on(member.guild.id, "welcome"):
            return
        w = self.bot.cfg(member.guild.id)["welcome"]
        rec = self.bot.store.users(member.guild.id).get(str(member.id))
        if not (rec and rec.get("jailed")):
            roles = [r for r in (member.guild.get_role(i) for i in (w["bot_roles"] if member.bot else w["roles"])) if r and r.is_assignable()]
            if roles:
                try:
                    await member.add_roles(*roles, reason="Auto role")
                except discord.HTTPException as exc:
                    log.warning("member.add_roles failed: %s", exc)
        ch = member.guild.get_channel(w["channel"]) if w["channel"] else None
        if ch:
            try:
                await ch.send(fmt(w["message"], member, member.guild), allowed_mentions=discord.AllowedMentions(users=[member]))
            except discord.HTTPException as exc:
                log.warning("ch.send failed: %s", exc)
        if w["dm"] and not member.bot:
            try:
                await member.send(fmt(w["dm"], member, member.guild))
            except discord.Forbidden:
                log.info("cannot DM %s, direct messages are closed", member)
            except discord.HTTPException as exc:
                log.warning("member.send failed: %s", exc)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Runs when a member leaves or is removed."""
        if not self.bot.module_on(member.guild.id, "welcome"):
            return
        w = self.bot.cfg(member.guild.id)["welcome"]
        ch = member.guild.get_channel(w["goodbye_channel"]) if w["goodbye_channel"] else None
        if ch:
            try:
                await ch.send(fmt(w["goodbye_message"], member, member.guild))
            except discord.HTTPException as exc:
                log.warning("ch.send failed: %s", exc)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Runs when roles, nickname or timeout of a member change."""
        if before.premium_since == after.premium_since or not self.bot.module_on(after.guild.id, "boosters"):
            return
        b = self.bot.cfg(after.guild.id)["boosters"]
        roles = [r for r in (after.guild.get_role(i) for i in b["roles"]) if r and r.is_assignable()]
        try:
            if after.premium_since and not before.premium_since:
                if roles:
                    await after.add_roles(*roles, reason="Server booster")
                ch = after.guild.get_channel(b["channel"]) if b["channel"] else None
                if ch:
                    await ch.send(fmt(b["message"], after, after.guild), allowed_mentions=discord.AllowedMentions(users=[after]))
            elif before.premium_since and not after.premium_since and b["remove_on_stop"] and roles:
                await after.remove_roles(*roles, reason="Boost ended")
        except discord.HTTPException as exc:
            log.warning("guild.get_channel failed: %s", exc)

    @wg.command(name="set", description="Set welcome and goodbye texts")
    @app_commands.describe(channel="Welcome channel", message="Text with {user}, {name}, {server}, {count}", dm="Private message to new members", goodbye_channel="Goodbye channel", goodbye_message="Goodbye text")
    async def w_set(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None, message: Optional[str] = None, dm: Optional[str] = None, goodbye_channel: Optional[discord.TextChannel] = None, goodbye_message: Optional[str] = None):
        """Set welcome and goodbye texts."""
        g = self.bot.cfg(it.guild_id)
        w = g["welcome"]
        if channel:
            w["channel"] = channel.id
        if goodbye_channel:
            w["goodbye_channel"] = goodbye_channel.id
        for k, v in (("message", message), ("dm", dm), ("goodbye_message", goodbye_message)):
            if v:
                w[k] = v
        g["modules"]["welcome"] = True
        await it.response.send_message("Saved. Use /welcome test to preview.", ephemeral=True)

    @wg.command(name="autorole", description="Toggle a role that new members get")
    async def w_autorole(self, it: discord.Interaction, role: discord.Role):
        """Toggle a role that new members get."""
        lst = self.bot.cfg(it.guild_id)["welcome"]["roles"]
        if role.id not in lst and not role.is_assignable():
            return await it.response.send_message("I cannot assign that role. Move my role above it.", ephemeral=True)
        lst.remove(role.id) if role.id in lst else lst.append(role.id)
        await it.response.send_message(f"{role.mention} is {'an auto role' if role.id in lst else 'no longer an auto role'}.", ephemeral=True)

    @wg.command(name="botrole", description="Toggle a role that new bots get")
    async def w_botrole(self, it: discord.Interaction, role: discord.Role):
        """Toggle a role that new bots get."""
        lst = self.bot.cfg(it.guild_id)["welcome"]["bot_roles"]
        lst.remove(role.id) if role.id in lst else lst.append(role.id)
        await it.response.send_message(f"{role.mention} is {'a bot auto role' if role.id in lst else 'no longer a bot auto role'}.", ephemeral=True)

    @wg.command(name="test", description="Preview the welcome message")
    async def w_test(self, it: discord.Interaction):
        """Preview the welcome message."""
        w = self.bot.cfg(it.guild_id)["welcome"]
        await it.response.send_message(fmt(w["message"], it.user, it.guild), ephemeral=True)

    @bg.command(name="set", description="Set the booster thank-you message")
    async def b_set(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None, message: Optional[str] = None, remove_on_stop: Optional[bool] = None):
        """Set the booster thank-you message."""
        g = self.bot.cfg(it.guild_id)
        b = g["boosters"]
        if channel:
            b["channel"] = channel.id
        if message:
            b["message"] = message
        if remove_on_stop is not None:
            b["remove_on_stop"] = remove_on_stop
        g["modules"]["boosters"] = True
        await it.response.send_message("Saved.", ephemeral=True)

    @bg.command(name="role", description="Toggle a role that boosters get")
    async def b_role(self, it: discord.Interaction, role: discord.Role):
        """Toggle a role that boosters get."""
        lst = self.bot.cfg(it.guild_id)["boosters"]["roles"]
        if role.id not in lst and not role.is_assignable():
            return await it.response.send_message("I cannot assign that role. Move my role above it.", ephemeral=True)
        lst.remove(role.id) if role.id in lst else lst.append(role.id)
        await it.response.send_message(f"{role.mention} is {'a booster role' if role.id in lst else 'no longer a booster role'}.", ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Welcome(bot))
