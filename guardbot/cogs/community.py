"""Starboard and temporary voice channels."""

import logging
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import emb, is_image

log = logging.getLogger(__name__)


class Community(commands.Cog):
    """Starboard and temporary voice channels."""
    sb = app_commands.Group(name="starboard", description="Starboard", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    tv = app_commands.Group(name="tempvoice", description="Temporary voice channels", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot

    async def refresh_star(self, p):
        """Count the stars of a message and create or update its starboard post."""
        if not p.guild_id or not self.bot.module_on(p.guild_id, "starboard"):
            return
        sb = self.bot.cfg(p.guild_id)["starboard"]
        if not sb["channel"] or p.channel_id == sb["channel"] or p.channel_id in sb["ignore_channels"]:
            return
        if str(p.emoji) != sb["emoji"]:
            return
        guild = self.bot.get_guild(p.guild_id)
        src, target = guild.get_channel_or_thread(p.channel_id), guild.get_channel(sb["channel"])
        if not src or not target:
            return
        try:
            msg = await src.fetch_message(p.message_id)
        except discord.HTTPException:
            return
        reaction = discord.utils.get(msg.reactions, emoji=sb["emoji"])
        users = [u async for u in reaction.users()] if reaction else []
        count = len([u for u in users if not u.bot and (sb["self_star"] or u.id != msg.author.id)])
        head = f"{sb['emoji']} **{count}** | {src.mention}"
        post_id = sb["posts"].get(str(msg.id))
        if post_id:
            try:
                post = await target.fetch_message(post_id)
                await post.edit(content=head)
            except discord.HTTPException:
                sb["posts"].pop(str(msg.id), None)
            return
        if count < sb["threshold"]:
            return
        e = emb(color=discord.Color.gold(), user=msg.author)
        e.description = (msg.content or "")[:3500] + f"\n\n[Jump to message]({msg.jump_url})"
        for a in msg.attachments:
            if is_image(a):
                e.set_image(url=a.url)
                break
        post = await target.send(head, embed=e)
        sb["posts"][str(msg.id)] = post.id

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, p):
        """Runs when a reaction is added."""
        await self.refresh_star(p)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, p):
        """Runs when a reaction is removed."""
        await self.refresh_star(p)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Runs when a member joins, leaves or moves between voice channels."""
        if not self.bot.module_on(member.guild.id, "tempvoice"):
            return
        t = self.bot.cfg(member.guild.id)["tempvoice"]
        if after.channel and t["hub"] and after.channel.id == t["hub"]:
            category = member.guild.get_channel(t["category"]) if t["category"] else after.channel.category
            try:
                room = await member.guild.create_voice_channel(
                    t["name"].replace("{name}", member.display_name)[:100],
                    category=category if isinstance(category, discord.CategoryChannel) else None,
                    user_limit=t["limit"],
                    overwrites={member: discord.PermissionOverwrite(manage_channels=True, move_members=True, connect=True)},
                    reason="Temporary voice channel",
                )
                t["rooms"].append(room.id)
                await member.move_to(room)
            except discord.HTTPException as exc:
                log.warning("guild.create_voice_channel failed: %s", exc)
        if before.channel and before.channel.id in t["rooms"] and not before.channel.members:
            try:
                await before.channel.delete(reason="Temporary voice channel empty")
            except discord.HTTPException as exc:
                log.warning("channel.delete failed: %s", exc)
            t["rooms"].remove(before.channel.id)

    @commands.Cog.listener()
    async def on_ready(self):
        """Runs once the bot is connected and the server cache is ready."""
        for guild in self.bot.guilds:
            t = self.bot.cfg(guild.id)["tempvoice"]
            for rid in list(t["rooms"]):
                ch = guild.get_channel(rid)
                if ch is None:
                    t["rooms"].remove(rid)
                elif not ch.members:
                    try:
                        await ch.delete(reason="Temporary voice channel empty")
                    except discord.HTTPException as exc:
                        log.warning("ch.delete failed: %s", exc)
                    t["rooms"].remove(rid)

    @sb.command(name="setup", description="Configure the starboard")
    @app_commands.describe(channel="Highlight channel", emoji="Emoji that counts", threshold="Reactions needed", self_star="Count the author's own reaction")
    async def sb_setup(self, it: discord.Interaction, channel: discord.TextChannel, emoji: Optional[str] = None, threshold: Optional[app_commands.Range[int, 1, 50]] = None, self_star: Optional[bool] = None):
        """Configure the starboard."""
        g = self.bot.cfg(it.guild_id)
        s = g["starboard"]
        s["channel"] = channel.id
        if emoji:
            s["emoji"] = emoji.strip()
        if threshold:
            s["threshold"] = threshold
        if self_star is not None:
            s["self_star"] = self_star
        g["modules"]["starboard"] = True
        await it.response.send_message(f"Starboard: {channel.mention}, {s['emoji']} x {s['threshold']}", ephemeral=True)

    @sb.command(name="ignore", description="Toggle a channel the starboard ignores")
    async def sb_ignore(self, it: discord.Interaction, channel: discord.TextChannel):
        """Toggle a channel the starboard ignores."""
        lst = self.bot.cfg(it.guild_id)["starboard"]["ignore_channels"]
        lst.remove(channel.id) if channel.id in lst else lst.append(channel.id)
        await it.response.send_message(f"{channel.mention} is {'ignored' if channel.id in lst else 'no longer ignored'}.", ephemeral=True)

    @tv.command(name="setup", description="Set the join-to-create channel")
    @app_commands.describe(hub="Voice channel members join to get their own room", category="Category for the rooms", name="Room name, {name} is the member", limit="User limit (0 = none)")
    async def tv_setup(self, it: discord.Interaction, hub: discord.VoiceChannel, category: Optional[discord.CategoryChannel] = None, name: Optional[str] = None, limit: Optional[app_commands.Range[int, 0, 99]] = None):
        """Set the join-to-create channel."""
        g = self.bot.cfg(it.guild_id)
        t = g["tempvoice"]
        t["hub"] = hub.id
        if category:
            t["category"] = category.id
        if name:
            t["name"] = name
        if limit is not None:
            t["limit"] = limit
        g["modules"]["tempvoice"] = True
        await it.response.send_message(f"Join {hub.mention} to create a room.", ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Community(bot))
