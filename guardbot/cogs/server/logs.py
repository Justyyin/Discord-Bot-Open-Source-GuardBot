"""Audit logging of messages, members, roles, channels, voice and server changes."""

import asyncio
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ...defaults import LOG_CATEGORIES
from ...utils import audit_executor, describe, emb, grab_files, trim
from ... import i18n

A = discord.AuditLogAction


def perm_diff(before, after):
    """Describe which permissions were added or removed between two permission sets."""
    add = [n for n, v in after if v and not getattr(before, n)]
    rem = [n for n, v in before if v and not getattr(after, n)]
    out = []
    if add:
        out.append("added: " + ", ".join(add))
    if rem:
        out.append("removed: " + ", ".join(rem))
    return "\n".join(out)


class Logs(commands.Cog):
    """Writes server events to the log channels."""
    grp = app_commands.Group(
        name="log",
        description="Log channels",
        default_permissions=discord.Permissions(manage_guild=True),
        guild_only=True,
    )

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot

    def ok(self, guild):
        """True if logging is turned on for this server."""
        return guild is not None and self.bot.module_on(guild.id, "logging")

    def push(self, guild, cat, title, color, user=None, fields=(), desc=None):
        """Build a log embed and queue it for the channel of the category."""
        e = emb(title, desc, color, user)
        for name, value in fields:
            if value is not None:
                e.add_field(name=name, value=trim(str(value)), inline=len(str(value)) < 40)
        self.bot.log(guild, cat, e)

    @grp.command(name="set", description="Set the channel for a log category")
    @app_commands.describe(category="Log category", channel="Channel (leave empty to remove)")
    async def log_set(self, it: discord.Interaction, category: Literal[LOG_CATEGORIES], channel: Optional[discord.TextChannel] = None):
        """Set the channel for a log category."""
        lc = self.bot.cfg(it.guild_id)["log"]
        if channel:
            p = channel.permissions_for(it.guild.me)
            missing = [n for n, ok in (("Send Messages", p.send_messages), ("Embed Links", p.embed_links), ("Attach Files", p.attach_files)) if not ok]
            if missing:
                return await it.response.send_message(i18n.say(it.client, it.guild, "I am missing in {mention}: {join}", mention=channel.mention, join=', '.join(missing)), ephemeral=True)
        lc[category] = channel.id if channel else None
        await it.response.send_message(f"{category}: {channel.mention if channel else 'removed'}", ephemeral=True)

    @grp.command(name="sent", description="Turn logging of every sent message on or off")
    async def log_sent(self, it: discord.Interaction, enabled: bool):
        """Turn logging of every sent message on or off."""
        self.bot.cfg(it.guild_id)["log_options"]["sent"] = enabled
        await it.response.send_message(i18n.say(it.client, it.guild, "Logging of sent messages: {value}", value='on' if enabled else 'off'), ephemeral=True)

    @grp.command(name="show", description="Show the log channels and ignore lists")
    async def log_show(self, it: discord.Interaction):
        """Show the log channels and ignore lists."""
        g = self.bot.cfg(it.guild_id)
        lines = [f"{k}: {('<#' + str(v) + '>') if v else 'main'}" for k, v in g["log"].items()]
        lo = g["log_options"]
        lines.append("ignored channels: " + (" ".join(f"<#{c}>" for c in lo["ignore_channels"]) or "none"))
        lines.append("ignored users: " + (" ".join(f"<@{u}>" for u in lo["ignore_users"]) or "none"))
        await it.response.send_message("\n".join(lines), ephemeral=True)

    @grp.command(name="ignorechannel", description="Toggle a channel that is not logged (message and voice events)")
    async def log_ignore_channel(self, it: discord.Interaction, channel: discord.abc.GuildChannel):
        """Toggle a channel that is not logged."""
        lst = self.bot.cfg(it.guild_id)["log_options"]["ignore_channels"]
        lst.remove(channel.id) if channel.id in lst else lst.append(channel.id)
        await it.response.send_message(f"{channel.mention} is {'ignored' if channel.id in lst else 'logged again'}.", ephemeral=True)

    @grp.command(name="ignoreuser", description="Toggle a user whose messages and voice activity are not logged")
    async def log_ignore_user(self, it: discord.Interaction, user: discord.User):
        """Toggle a user who is not logged."""
        lst = self.bot.cfg(it.guild_id)["log_options"]["ignore_users"]
        lst.remove(user.id) if user.id in lst else lst.append(user.id)
        await it.response.send_message(f"{user.mention} is {'ignored' if user.id in lst else 'logged again'}.", ephemeral=True)

    def ignored(self, guild, channel_id=None, user_id=None):
        """True if the channel or the user is on the ignore list."""
        lo = self.bot.cfg(guild.id)["log_options"]
        return channel_id in lo["ignore_channels"] or user_id in lo["ignore_users"]

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Runs for every new message."""
        if msg.author.bot or not self.ok(msg.guild):
            return
        if not self.bot.cfg(msg.guild.id)["log_options"]["sent"] or self.bot.is_log_channel(msg.guild, msg.channel.id):
            return
        if self.ignored(msg.guild, msg.channel.id, msg.author.id):
            return
        e = emb("Message sent", color=discord.Color.green(), user=msg.author)
        describe(e, msg)
        e.add_field(name="Link", value=f"[Jump]({msg.jump_url})")
        self.bot.log(msg.guild, "messages", e)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Runs when a message is edited."""
        if after.author.bot or not self.ok(after.guild) or before.content == after.content:
            return
        if self.bot.is_log_channel(after.guild, after.channel.id) or self.ignored(after.guild, after.channel.id, after.author.id):
            return
        e = emb("Message edited", color=discord.Color.blue(), user=after.author)
        e.add_field(name="Before", value=trim(before.content), inline=False)
        e.add_field(name="After", value=trim(after.content), inline=False)
        e.add_field(name="Channel", value=after.channel.mention)
        e.add_field(name="Link", value=f"[Jump]({after.jump_url})")
        self.bot.log(after.guild, "messages", e)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, p):
        """Runs when a message is deleted, also when it was not cached."""
        if not p.guild_id:
            return
        if p.message_id in self.bot.bot_deleted:
            self.bot.bot_deleted.discard(p.message_id)
            return
        guild = self.bot.get_guild(p.guild_id)
        if not self.ok(guild) or self.bot.is_log_channel(guild, p.channel_id) or self.ignored(guild, p.channel_id):
            return
        m = p.cached_message
        if m is None:
            e = emb("Message deleted (not cached)", color=discord.Color.light_grey(), footer=f"Message ID {p.message_id}")
            e.add_field(name="Channel", value=f"<#{p.channel_id}>")
            self.bot.log(guild, "messages", e)
            return
        if m.author.bot or self.ignored(guild, user_id=m.author.id):
            return
        e = emb("Message deleted", color=discord.Color.orange(), user=m.author)
        describe(e, m)
        self.bot.log(guild, "messages", e, await grab_files(m))

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, p):
        """Runs when many messages are deleted at once."""
        guild = self.bot.get_guild(p.guild_id) if p.guild_id else None
        if self.ok(guild):
            self.push(guild, "messages", "Bulk delete", discord.Color.dark_orange(), fields=[("Channel", f"<#{p.channel_id}>"), ("Messages", len(p.message_ids))])

    @commands.Cog.listener()
    async def on_member_join(self, m):
        """Runs when a member joins."""
        if self.ok(m.guild):
            age = (discord.utils.utcnow() - m.created_at).days
            self.push(m.guild, "members", "Member joined", discord.Color.green(), m, [("Account age", f"{age} days"), ("Members", m.guild.member_count)])

    @commands.Cog.listener()
    async def on_member_remove(self, m):
        """Runs when a member leaves or is removed."""
        if self.ok(m.guild):
            roles = ", ".join(r.name for r in m.roles if not r.is_default())
            self.push(m.guild, "members", "Member left", discord.Color.orange(), m, [("Roles", roles or None)])

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Runs when roles, nickname or timeout of a member change."""
        if not self.ok(after.guild):
            return
        if before.roles != after.roles:
            added = [r.mention for r in after.roles if r not in before.roles]
            removed = [r.mention for r in before.roles if r not in after.roles]
            await asyncio.sleep(1.5)
            entry = await audit_executor(after.guild, A.member_role_update, after.id)
            self.push(after.guild, "members", "Roles changed", discord.Color.blue(), after, [
                ("Added", ", ".join(added) or None),
                ("Removed", ", ".join(removed) or None),
                ("By", f"{entry.user.mention} ({entry.user.id})" if entry else None),
            ])
        if before.nick != after.nick:
            self.push(after.guild, "members", "Nickname changed", discord.Color.blue(), after, [("Before", before.nick or "-"), ("After", after.nick or "-")])
        if before.timed_out_until != after.timed_out_until:
            until = f"<t:{int(after.timed_out_until.timestamp())}:R>" if after.timed_out_until else "removed"
            self.push(after.guild, "members", "Timeout changed", discord.Color.orange(), after, [("Until", until)])

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Runs when a member is banned."""
        if self.ok(guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(guild, A.ban, user.id)
            self.push(guild, "moderation", "Member banned", discord.Color.red(), user, [
                ("By", f"{entry.user.mention} ({entry.user.id})" if entry else None),
                ("Reason", entry.reason if entry else None),
            ])

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """Runs when a member is unbanned."""
        if self.ok(guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(guild, A.unban, user.id)
            self.push(guild, "moderation", "Member unbanned", discord.Color.green(), user, [("By", f"{entry.user.mention} ({entry.user.id})" if entry else None)])

    @commands.Cog.listener()
    async def on_voice_state_update(self, m, before, after):
        """Runs when a member joins, leaves or moves between voice channels."""
        if not self.ok(m.guild) or before.channel == after.channel:
            return
        channel = after.channel or before.channel
        if self.ignored(m.guild, channel.id, m.id):
            return
        if before.channel is None:
            title, info = "Voice join", after.channel.mention
        elif after.channel is None:
            title, info = "Voice leave", before.channel.mention
        else:
            title, info = "Voice move", f"{before.channel.mention} to {after.channel.mention}"
        self.push(m.guild, "voice", title, discord.Color.teal(), m, [("Channel", info)])

    @commands.Cog.listener()
    async def on_guild_channel_create(self, ch):
        """Runs when a channel is created."""
        if self.ok(ch.guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(ch.guild, A.channel_create, ch.id)
            self.push(ch.guild, "server", "Channel created", discord.Color.green(), fields=[("Channel", f"{ch.mention} ({ch.id})"), ("Type", ch.type.name), ("By", f"{entry.user.mention}" if entry else None)])

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, ch):
        """Runs when a channel is deleted."""
        if self.ok(ch.guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(ch.guild, A.channel_delete, ch.id)
            self.push(ch.guild, "server", "Channel deleted", discord.Color.red(), fields=[("Channel", f"{ch.name} ({ch.id})"), ("Type", ch.type.name), ("By", f"{entry.user.mention}" if entry else None)])

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        """Runs when a channel changes."""
        if not self.ok(after.guild):
            return
        changes = []
        for attr in ("name", "topic", "nsfw", "slowmode_delay", "category", "bitrate", "user_limit"):
            b, a = getattr(before, attr, None), getattr(after, attr, None)
            if b != a:
                changes.append(f"{attr}: {b} -> {a}")
        if before.overwrites != after.overwrites:
            changes.append("permission overwrites changed")
        if changes:
            await asyncio.sleep(1.5)
            entry = await audit_executor(after.guild, A.channel_update, after.id)
            self.push(after.guild, "server", "Channel updated", discord.Color.blue(), fields=[("Channel", after.mention), ("Changes", "\n".join(changes)), ("By", entry.user.mention if entry else None)])

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Runs when a role is created."""
        if self.ok(role.guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(role.guild, A.role_create, role.id)
            self.push(role.guild, "server", "Role created", discord.Color.green(), fields=[("Role", f"{role.mention} ({role.id})"), ("By", entry.user.mention if entry else None)])

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Runs when a role is deleted."""
        if self.ok(role.guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(role.guild, A.role_delete, role.id)
            self.push(role.guild, "server", "Role deleted", discord.Color.red(), fields=[("Role", f"{role.name} ({role.id})"), ("By", entry.user.mention if entry else None)])

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        """Runs when a role changes."""
        if not self.ok(after.guild):
            return
        changes = []
        for attr in ("name", "color", "hoist", "mentionable"):
            b, a = getattr(before, attr), getattr(after, attr)
            if b != a:
                changes.append(f"{attr}: {b} -> {a}")
        if before.permissions != after.permissions:
            changes.append("permissions " + perm_diff(before.permissions, after.permissions))
        if changes:
            await asyncio.sleep(1.5)
            entry = await audit_executor(after.guild, A.role_update, after.id)
            self.push(after.guild, "server", "Role updated", discord.Color.blue(), fields=[("Role", after.mention), ("Changes", "\n".join(changes)), ("By", entry.user.mention if entry else None)])


    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        """Runs when an invite is created."""
        if invite.guild and self.ok(invite.guild):
            self.push(invite.guild, "server", "Invite created", discord.Color.green(), invite.inviter, [
                ("Code", invite.code), ("Channel", invite.channel.mention if invite.channel else None),
                ("Max uses", invite.max_uses or "unlimited"), ("Expires", f"<t:{int(invite.expires_at.timestamp())}:R>" if invite.expires_at else "never"),
            ])

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        """Runs when an invite is deleted."""
        if invite.guild and self.ok(invite.guild):
            self.push(invite.guild, "server", "Invite deleted", discord.Color.orange(), fields=[("Code", invite.code)])

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        """Runs when emojis are added, removed or renamed."""
        if not self.ok(guild):
            return
        b, a = {e.id: e for e in before}, {e.id: e for e in after}
        added = [str(a[i]) for i in a if i not in b]
        removed = [b[i].name for i in b if i not in a]
        renamed = [f"{b[i].name} -> {a[i].name}" for i in a if i in b and a[i].name != b[i].name]
        if added or removed or renamed:
            self.push(guild, "server", "Emojis changed", discord.Color.blue(), fields=[("Added", " ".join(added) or None), ("Removed", ", ".join(removed) or None), ("Renamed", ", ".join(renamed) or None)])

    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild, before, after):
        """Runs when stickers are added or removed."""
        if not self.ok(guild):
            return
        b, a = {e.id: e for e in before}, {e.id: e for e in after}
        added = [a[i].name for i in a if i not in b]
        removed = [b[i].name for i in b if i not in a]
        if added or removed:
            self.push(guild, "server", "Stickers changed", discord.Color.blue(), fields=[("Added", ", ".join(added) or None), ("Removed", ", ".join(removed) or None)])

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        """Runs when a thread is created."""
        if self.ok(thread.guild):
            self.push(thread.guild, "server", "Thread created", discord.Color.green(), thread.owner, [("Thread", thread.mention), ("Parent", thread.parent.mention if thread.parent else None)])

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        """Runs when a thread is deleted."""
        if self.ok(thread.guild):
            self.push(thread.guild, "server", "Thread deleted", discord.Color.red(), fields=[("Thread", thread.name), ("Parent", thread.parent.mention if thread.parent else None)])

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        """Runs when a thread changes."""
        if not self.ok(after.guild):
            return
        changes = [f"{a}: {getattr(before, a)} -> {getattr(after, a)}" for a in ("name", "archived", "locked", "slowmode_delay") if getattr(before, a) != getattr(after, a)]
        if changes:
            self.push(after.guild, "server", "Thread updated", discord.Color.blue(), fields=[("Thread", after.mention), ("Changes", "\n".join(changes))])

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        """Runs when the webhooks of a channel change."""
        if self.ok(channel.guild):
            await asyncio.sleep(1.5)
            entry = None
            for action in (A.webhook_create, A.webhook_update, A.webhook_delete):
                entry = await audit_executor(channel.guild, action)
                if entry:
                    break
            self.push(channel.guild, "server", "Webhooks changed", discord.Color.blue(), fields=[
                ("Channel", channel.mention), ("Action", entry.action.name if entry else None), ("By", entry.user.mention if entry else None)])

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        """Runs when a user changes name or profile picture."""
        changes = []
        if before.name != after.name:
            changes.append(f"username: {before.name} -> {after.name}")
        if before.global_name != after.global_name:
            changes.append(f"display name: {before.global_name} -> {after.global_name}")
        if (before.avatar.key if before.avatar else None) != (after.avatar.key if after.avatar else None):
            changes.append("profile picture changed")
        if not changes:
            return
        for guild in self.bot.guilds:
            if guild.get_member(after.id) and self.ok(guild):
                e = emb("Profile changed", "\n".join(changes), discord.Color.blue(), after)
                e.set_thumbnail(url=after.display_avatar.url)
                self.bot.log(guild, "members", e)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """Runs when the server settings change."""
        if not self.ok(after):
            return
        changes = [f"{a}: {getattr(before, a)} -> {getattr(after, a)}" for a in ("name", "verification_level", "afk_timeout", "explicit_content_filter", "vanity_url_code") if getattr(before, a, None) != getattr(after, a, None)]
        if (before.icon.key if before.icon else None) != (after.icon.key if after.icon else None):
            changes.append("server icon changed")
        if changes:
            await asyncio.sleep(1.5)
            entry = await audit_executor(after, A.guild_update)
            self.push(after, "server", "Server updated", discord.Color.blue(), fields=[("Changes", "\n".join(changes)), ("By", entry.user.mention if entry else None)])


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Logs(bot))
