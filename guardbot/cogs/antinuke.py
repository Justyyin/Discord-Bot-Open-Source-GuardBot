# Copyright (c) Justyn
import asyncio
import time
from collections import deque
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ..defaults import DANGEROUS
from ..utils import audit_executor, emb, trim

A = discord.AuditLogAction
LIMIT_KEYS = ("channel_delete", "role_delete", "channel_create", "ban", "kick")


class AntiNuke(commands.Cog):
    grp = app_commands.Group(
        name="antinuke",
        description="Protection against server destruction",
        default_permissions=discord.Permissions(administrator=True),
        guild_only=True,
    )

    def __init__(self, bot):
        self.bot = bot
        self.hits = {}
        self.warned = {}

    def on(self, guild):
        return guild is not None and self.bot.module_on(guild.id, "antinuke")

    def staff_label(self, guild, member):
        ids = set(self.bot.cfg(guild.id)["antinuke"]["staff_roles"])
        names = [r.name for r in getattr(member, "roles", []) if r.id in ids]
        return ", ".join(names) or None

    async def notify_owner(self, guild, embed):
        if not self.bot.cfg(guild.id)["antinuke"]["notify_owner"]:
            return
        owner = guild.owner or await guild.fetch_member(guild.owner_id)
        try:
            await owner.send(embed=embed)
        except (discord.HTTPException, AttributeError):
            self.bot.log(guild, "security", emb("Could not DM the server owner", color=discord.Color.red()))

    async def record(self, guild, action, key, target_id):
        if not self.on(guild):
            return
        await asyncio.sleep(1.5)
        entry = await audit_executor(guild, action, target_id)
        if not entry or not entry.user:
            return
        ex = entry.user
        an = self.bot.cfg(guild.id)["antinuke"]
        if ex.id in (guild.owner_id, self.bot.user.id) or ex.id in an["whitelist"]:
            return
        count, secs = an["limits"].get(key, [0, 0])
        if not count:
            return
        dq = self.hits.setdefault((guild.id, ex.id, key), deque())
        now = time.time()
        dq.append(now)
        while dq and now - dq[0] > secs:
            dq.popleft()
        if len(dq) >= count:
            dq.clear()
            await self.trigger(guild, ex, key, count, secs)

    async def trigger(self, guild, executor, key, count, secs):
        an = self.bot.cfg(guild.id)["antinuke"]
        member = guild.get_member(executor.id)
        result = "alert only"
        if an["action"] == "strip" and member:
            roles = [r for r in member.roles if r.is_assignable() and any(getattr(r.permissions, p) for p in DANGEROUS)]
            try:
                if roles:
                    await member.remove_roles(*roles, reason="Anti-nuke")
                    self.bot.store.user(guild.id, member.id)["stripped_roles"] = [r.id for r in roles]
                    self.bot.store.mark("users")
                result = "dangerous roles removed: " + (", ".join(r.name for r in roles) or "none found")
            except discord.HTTPException:
                result = "could not remove roles"
        elif an["action"] in ("kick", "ban") and member:
            try:
                if an["action"] == "kick":
                    await member.kick(reason="Anti-nuke")
                else:
                    await guild.ban(member, reason="Anti-nuke")
                result = an["action"]
            except discord.HTTPException:
                result = f"{an['action']} failed"
        e = emb("ANTI-NUKE TRIGGERED", color=discord.Color.dark_red(), user=executor)
        e.add_field(name="Server", value=f"{guild.name} ({guild.id})", inline=False)
        e.add_field(name="Action", value=f"{count} x {key} within {secs}s")
        e.add_field(name="Response", value=result)
        label = self.staff_label(guild, member) if member else None
        e.add_field(name="Staff role", value=label or "none of the configured staff roles")
        self.bot.log(guild, "security", e)
        await self.notify_owner(guild, e)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, ch):
        await self.record(ch.guild, A.channel_delete, "channel_delete", ch.id)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, ch):
        await self.record(ch.guild, A.channel_create, "channel_create", ch.id)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await self.record(role.guild, A.role_delete, "role_delete", role.id)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await self.record(guild, A.ban, "ban", user.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.record(member.guild, A.kick, "kick", member.id)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot or not msg.guild or not self.on(msg.guild) or msg.author.id == msg.guild.owner_id:
            return
        an = self.bot.cfg(msg.guild.id)["antinuke"]
        low = msg.content.lower()
        if not any(w.lower() in low for w in an["watch_words"]):
            return
        names = [msg.guild.name.lower()] + [n.lower() for n in an["server_names"]]
        if not any(n in low for n in names):
            return
        key = (msg.guild.id, msg.author.id)
        if time.time() - self.warned.get(key, 0) < 60:
            return
        self.warned[key] = time.time()
        label = self.staff_label(msg.guild, msg.author)
        e = emb("Nuke talk about this server", color=discord.Color.dark_red(), user=msg.author)
        e.add_field(name="Server", value=f"{msg.guild.name} ({msg.guild.id})", inline=False)
        e.add_field(name="Staff role", value=label or "no staff role")
        e.add_field(name="Channel", value=msg.channel.mention)
        e.add_field(name="Message", value=trim(msg.content), inline=False)
        e.add_field(name="Link", value=f"[Jump]({msg.jump_url})")
        self.bot.log(msg.guild, "security", e)
        if label:
            await self.notify_owner(msg.guild, e)

    @grp.command(name="setup", description="Configure anti-nuke")
    @app_commands.describe(enabled="Turn on or off", action="Response when a limit is reached", notify_owner="Send a DM to the server owner")
    async def an_setup(self, it: discord.Interaction, enabled: Optional[bool] = None, action: Optional[Literal["alert", "strip", "kick", "ban"]] = None, notify_owner: Optional[bool] = None):
        g = self.bot.cfg(it.guild_id)
        if enabled is not None:
            g["modules"]["antinuke"] = enabled
        an = g["antinuke"]
        if action:
            an["action"] = action
        if notify_owner is not None:
            an["notify_owner"] = notify_owner
        self.bot.store.mark("config")
        await it.response.send_message(f"Anti-nuke: {'on' if g['modules']['antinuke'] else 'off'}, action {an['action']}, DM to owner {an['notify_owner']}", ephemeral=True)

    @grp.command(name="limit", description="Set how many actions within how many seconds trigger the protection")
    async def an_limit(self, it: discord.Interaction, kind: Literal[LIMIT_KEYS], count: app_commands.Range[int, 1, 50], seconds: app_commands.Range[int, 1, 600]):
        self.bot.cfg(it.guild_id)["antinuke"]["limits"][kind] = [count, seconds]
        self.bot.store.mark("config")
        await it.response.send_message(f"{kind}: {count} within {seconds}s", ephemeral=True)

    @grp.command(name="whitelist", description="Toggle a user who is never checked")
    async def an_whitelist(self, it: discord.Interaction, user: discord.Member):
        wl = self.bot.cfg(it.guild_id)["antinuke"]["whitelist"]
        wl.remove(user.id) if user.id in wl else wl.append(user.id)
        self.bot.store.mark("config")
        await it.response.send_message(f"{user.mention} is {'whitelisted' if user.id in wl else 'no longer whitelisted'}.", ephemeral=True)

    @grp.command(name="staffrole", description="Toggle a role that counts as staff in alerts (Moderator, Admin, Dev and so on)")
    async def an_staffrole(self, it: discord.Interaction, role: discord.Role):
        lst = self.bot.cfg(it.guild_id)["antinuke"]["staff_roles"]
        lst.remove(role.id) if role.id in lst else lst.append(role.id)
        self.bot.store.mark("config")
        await it.response.send_message(f"{role.mention} is {'a staff role' if role.id in lst else 'no longer a staff role'}.", ephemeral=True)

    @grp.command(name="servername", description="Toggle an extra name that counts as this server in nuke talk")
    async def an_name(self, it: discord.Interaction, name: str):
        lst = self.bot.cfg(it.guild_id)["antinuke"]["server_names"]
        lst.remove(name) if name in lst else lst.append(name)
        self.bot.store.mark("config")
        await it.response.send_message(f"Names: {', '.join(lst) or 'none'}", ephemeral=True)

    @grp.command(name="restore", description="Give back the roles that anti-nuke removed from a member")
    async def an_restore(self, it: discord.Interaction, member: discord.Member):
        rec = self.bot.store.user(it.guild_id, member.id)
        roles = [it.guild.get_role(i) for i in rec.pop("stripped_roles", [])]
        roles = [r for r in roles if r and r.is_assignable()]
        if not roles:
            return await it.response.send_message("Nothing to restore.", ephemeral=True)
        await member.add_roles(*roles, reason=f"Anti-nuke restore by {it.user}")
        self.bot.store.mark("users")
        await it.response.send_message(f"Restored {len(roles)} roles.", ephemeral=True)

    @grp.command(name="status", description="Show the anti-nuke settings")
    async def an_status(self, it: discord.Interaction):
        g = self.bot.cfg(it.guild_id)
        an = g["antinuke"]
        lines = [f"{k}: {v[0]} within {v[1]}s" for k, v in an["limits"].items()]
        text = (
            f"Status: {'on' if g['modules']['antinuke'] else 'off'}\nAction: {an['action']}\nDM owner: {an['notify_owner']}\n"
            f"Staff roles: {' '.join('<@&' + str(i) + '>' for i in an['staff_roles']) or 'none'}\n"
            f"Whitelist: {' '.join('<@' + str(i) + '>' for i in an['whitelist']) or 'none'}\n" + "\n".join(lines)
        )
        await it.response.send_message(text, ephemeral=True)


async def setup(bot):
    await bot.add_cog(AntiNuke(bot))
