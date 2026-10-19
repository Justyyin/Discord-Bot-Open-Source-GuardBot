# Copyright (c) Justyn
import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal, Optional

from ..defaults import LOG_CATEGORIES
from ..utils import audit_executor, describe, emb, grab_files, trim

A = discord.AuditLogAction


def perm_diff(before, after):
    add = [n for n, v in after if v and not getattr(before, n)]
    rem = [n for n, v in before if v and not getattr(after, n)]
    out = []
    if add:
        out.append("added: " + ", ".join(add))
    if rem:
        out.append("removed: " + ", ".join(rem))
    return "\n".join(out)


class Logs(commands.Cog):
    grp = app_commands.Group(
        name="log",
        description="Log channels",
        default_permissions=discord.Permissions(manage_guild=True),
        guild_only=True,
    )

    def __init__(self, bot):
        self.bot = bot

    def ok(self, guild):
        return guild is not None and self.bot.module_on(guild.id, "logging")

    def push(self, guild, cat, title, color, user=None, fields=(), desc=None):
        e = emb(title, desc, color, user)
        for name, value in fields:
            if value is not None:
                e.add_field(name=name, value=trim(str(value)), inline=len(str(value)) < 40)
        self.bot.log(guild, cat, e)

    @grp.command(name="set", description="Set the channel for a log category")
    @app_commands.describe(category="Log category", channel="Channel (leave empty to remove)")
    async def log_set(self, it: discord.Interaction, category: Literal[LOG_CATEGORIES], channel: Optional[discord.TextChannel] = None):
        lc = self.bot.cfg(it.guild_id)["log"]
        if channel:
            p = channel.permissions_for(it.guild.me)
            missing = [n for n, ok in (("Send Messages", p.send_messages), ("Embed Links", p.embed_links), ("Attach Files", p.attach_files)) if not ok]
            if missing:
                return await it.response.send_message(f"I am missing in {channel.mention}: {', '.join(missing)}", ephemeral=True)
        lc[category] = channel.id if channel else None
        self.bot.store.mark("config")
        await it.response.send_message(f"{category}: {channel.mention if channel else 'removed'}", ephemeral=True)

    @grp.command(name="sent", description="Turn logging of every sent message on or off")
    async def log_sent(self, it: discord.Interaction, enabled: bool):
        self.bot.cfg(it.guild_id)["log_options"]["sent"] = enabled
        self.bot.store.mark("config")
        await it.response.send_message(f"Logging of sent messages: {'on' if enabled else 'off'}", ephemeral=True)

    @grp.command(name="show", description="Show the log channels")
    async def log_show(self, it: discord.Interaction):
        lc = self.bot.cfg(it.guild_id)["log"]
        lines = [f"{k}: {('<#' + str(v) + '>') if v else 'main'}" for k, v in lc.items()]
        await it.response.send_message("\n".join(lines), ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot or not self.ok(msg.guild):
            return
        if not self.bot.cfg(msg.guild.id)["log_options"]["sent"] or self.bot.is_log_channel(msg.guild, msg.channel.id):
            return
        e = emb("Message sent", color=discord.Color.green(), user=msg.author)
        describe(e, msg)
        e.add_field(name="Link", value=f"[Jump]({msg.jump_url})")
        self.bot.log(msg.guild, "messages", e)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot or not self.ok(after.guild) or before.content == after.content:
            return
        if self.bot.is_log_channel(after.guild, after.channel.id):
            return
        e = emb("Message edited", color=discord.Color.blue(), user=after.author)
        e.add_field(name="Before", value=trim(before.content), inline=False)
        e.add_field(name="After", value=trim(after.content), inline=False)
        e.add_field(name="Channel", value=after.channel.mention)
        e.add_field(name="Link", value=f"[Jump]({after.jump_url})")
        self.bot.log(after.guild, "messages", e)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, p):
        if not p.guild_id:
            return
        if p.message_id in self.bot.bot_deleted:
            self.bot.bot_deleted.discard(p.message_id)
            return
        guild = self.bot.get_guild(p.guild_id)
        if not self.ok(guild) or self.bot.is_log_channel(guild, p.channel_id):
            return
        m = p.cached_message
        if m is None:
            e = emb("Message deleted (not cached)", color=discord.Color.light_grey(), footer=f"Message ID {p.message_id}")
            e.add_field(name="Channel", value=f"<#{p.channel_id}>")
            self.bot.log(guild, "messages", e)
            return
        if m.author.bot:
            return
        e = emb("Message deleted", color=discord.Color.orange(), user=m.author)
        describe(e, m)
        self.bot.log(guild, "messages", e, await grab_files(m))

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, p):
        guild = self.bot.get_guild(p.guild_id) if p.guild_id else None
        if self.ok(guild):
            self.push(guild, "messages", "Bulk delete", discord.Color.dark_orange(), fields=[("Channel", f"<#{p.channel_id}>"), ("Messages", len(p.message_ids))])

    @commands.Cog.listener()
    async def on_member_join(self, m):
        if self.ok(m.guild):
            age = (discord.utils.utcnow() - m.created_at).days
            self.push(m.guild, "members", "Member joined", discord.Color.green(), m, [("Account age", f"{age} days"), ("Members", m.guild.member_count)])

    @commands.Cog.listener()
    async def on_member_remove(self, m):
        if self.ok(m.guild):
            roles = ", ".join(r.name for r in m.roles if not r.is_default())
            self.push(m.guild, "members", "Member left", discord.Color.orange(), m, [("Roles", roles or None)])

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
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
        if self.ok(guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(guild, A.ban, user.id)
            self.push(guild, "moderation", "Member banned", discord.Color.red(), user, [
                ("By", f"{entry.user.mention} ({entry.user.id})" if entry else None),
                ("Reason", entry.reason if entry else None),
            ])

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if self.ok(guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(guild, A.unban, user.id)
            self.push(guild, "moderation", "Member unbanned", discord.Color.green(), user, [("By", f"{entry.user.mention} ({entry.user.id})" if entry else None)])

    @commands.Cog.listener()
    async def on_voice_state_update(self, m, before, after):
        if not self.ok(m.guild) or before.channel == after.channel:
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
        if self.ok(ch.guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(ch.guild, A.channel_create, ch.id)
            self.push(ch.guild, "server", "Channel created", discord.Color.green(), fields=[("Channel", f"{ch.mention} ({ch.id})"), ("Type", ch.type.name), ("By", f"{entry.user.mention}" if entry else None)])

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, ch):
        if self.ok(ch.guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(ch.guild, A.channel_delete, ch.id)
            self.push(ch.guild, "server", "Channel deleted", discord.Color.red(), fields=[("Channel", f"{ch.name} ({ch.id})"), ("Type", ch.type.name), ("By", f"{entry.user.mention}" if entry else None)])

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
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
        if self.ok(role.guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(role.guild, A.role_create, role.id)
            self.push(role.guild, "server", "Role created", discord.Color.green(), fields=[("Role", f"{role.mention} ({role.id})"), ("By", entry.user.mention if entry else None)])

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if self.ok(role.guild):
            await asyncio.sleep(1.5)
            entry = await audit_executor(role.guild, A.role_delete, role.id)
            self.push(role.guild, "server", "Role deleted", discord.Color.red(), fields=[("Role", f"{role.name} ({role.id})"), ("By", entry.user.mention if entry else None)])

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
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


async def setup(bot):
    await bot.add_cog(Logs(bot))
