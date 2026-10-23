"""Permission audit: lists roles with dangerous permissions and warns when new ones appear."""

import asyncio
import logging

import discord
from discord import app_commands
from discord.ext import commands

from ...cog import BaseCog
from ...defaults import DANGEROUS
from ...utils import audit_executor, emb, trim
from ... import i18n

log = logging.getLogger(__name__)

A = discord.AuditLogAction
NAMES = {p: p.replace("_", " ") for p in DANGEROUS}


def dangerous(perms):
    """Return the dangerous permissions in a Permissions object. Administrator counts for everything."""
    return [p for p in DANGEROUS if getattr(perms, p)]


class PermAudit(BaseCog):
    """Shows who holds dangerous permissions and reports new grants."""
    section = "permaudit"

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    def active(self, guild):
        """True if the module and the watch are on for a server."""
        return self.bot.module_on(guild.id, "permaudit") and self.conf(guild.id)["watch"]

    @commands.hybrid_group(name="permaudit", fallback="run", description="List roles with dangerous permissions and who holds them")
    async def audit(self, ctx):
        """List roles with dangerous permissions and who holds them."""
        guild = ctx.guild
        trusted = set(self.conf(guild.id)["trusted"])
        rows, risky_everyone = [], dangerous(guild.default_role.permissions)
        for role in sorted(guild.roles, key=lambda r: -r.position):
            perms = dangerous(role.permissions)
            if role.is_default() or not perms:
                continue
            people = [m for m in role.members if not m.bot]
            tag = "managed by an integration" if role.managed else ("trusted" if role.id in trusted else "check")
            names = ", ".join(m.display_name for m in people[:6]) + (f" and {len(people) - 6} more" if len(people) > 6 else "")
            rows.append((role, perms, len(role.members), tag, names or "nobody"))
        e = emb("Permission audit", color=discord.Color.orange() if rows or risky_everyone else discord.Color.green())
        if risky_everyone:
            e.add_field(name="@everyone has dangerous permissions", value=", ".join(NAMES[p] for p in risky_everyone), inline=False)
        for role, perms, n, tag, names in rows[:20]:
            e.add_field(name=f"{role.name} ({n}, {tag})", value=trim(f"{', '.join(NAMES[p] for p in perms)}\n{names}", 1000), inline=False)
        if len(rows) > 20:
            e.add_field(name="More", value=f"{len(rows) - 20} further roles are not shown.", inline=False)
        if not rows and not risky_everyone:
            e.description = "No role has dangerous permissions."
        e.set_footer(text=f"Checked: {', '.join(NAMES.values())}")
        await ctx.send(embed=e, ephemeral=True)

    @audit.command(name="watch", description="Report when a role or member gets dangerous permissions")
    @app_commands.describe(enabled="On or off")
    async def watch(self, ctx, enabled: bool):
        """Report when a role or member gets dangerous permissions."""
        self.conf(ctx.guild.id)["watch"] = enabled
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Watching for new dangerous permissions: {value}.", value='on' if enabled else 'off'), ephemeral=True)

    @audit.command(name="trust", description="Toggle a role whose permissions are expected, so it raises no alarm")
    async def trust(self, ctx, role: discord.Role):
        """Toggle a role whose permissions are expected, so it raises no alarm."""
        lst = self.conf(ctx.guild.id)["trusted"]
        lst.remove(role.id) if role.id in lst else lst.append(role.id)
        await ctx.send(f"{role.name} is {'trusted' if role.id in lst else 'no longer trusted'}.", ephemeral=True)

    async def alert(self, guild, title, lines, action, target_id):
        """Post an alert with the person who made the change, if the audit log shows them."""
        await asyncio.sleep(1.5)
        entry = await audit_executor(guild, action, target_id)
        who = entry.user if entry and entry.user else None
        if who and who.id == self.bot.user.id:
            return
        e = emb(title, color=discord.Color.orange(), user=who)
        for name, value in lines:
            e.add_field(name=name, value=value, inline=False)
        e.add_field(name="Changed by", value=f"{who.mention} ({who.id})" if who else "unknown (no audit log access)", inline=False)
        self.bot.log(guild, "security", e)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        """Runs when a role changes."""
        if not self.active(after.guild) or after.id in self.conf(after.guild.id)["trusted"]:
            return
        new = set(dangerous(after.permissions)) - set(dangerous(before.permissions))
        if new:
            await self.alert(after.guild, "Role gained dangerous permissions", [("Role", f"{after.mention} ({len(after.members)} members)"), ("New", ", ".join(NAMES[p] for p in DANGEROUS if p in new))], A.role_update, after.id)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Runs when a role is created."""
        if not self.active(role.guild) or role.managed:
            return
        perms = dangerous(role.permissions)
        if perms:
            await self.alert(role.guild, "New role with dangerous permissions", [("Role", role.mention), ("Permissions", ", ".join(NAMES[p] for p in perms))], A.role_create, role.id)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Runs when a member changes. Reports new roles that carry dangerous permissions."""
        if after.bot or not self.active(after.guild):
            return
        trusted = set(self.conf(after.guild.id)["trusted"])
        added = [r for r in after.roles if r not in before.roles and r.id not in trusted and dangerous(r.permissions)]
        if added:
            lines = [("Member", f"{after.mention} ({after.id})"), ("Role", ", ".join(f"{r.name}: {', '.join(NAMES[p] for p in dangerous(r.permissions))}" for r in added))]
            await self.alert(after.guild, "Member received a role with dangerous permissions", lines, A.member_role_update, after.id)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(PermAudit(bot))
