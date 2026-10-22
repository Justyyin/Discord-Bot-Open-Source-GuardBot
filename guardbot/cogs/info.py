"""Information commands: userinfo, serverinfo, roleinfo, avatar, ping and botinfo."""

import platform
import time
from pathlib import Path
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from .. import __version__
from ..utils import emb, fmt_duration


def stamp(dt):
    """Format a datetime as a Discord timestamp with the relative time."""
    return f"<t:{int(dt.timestamp())}:D> (<t:{int(dt.timestamp())}:R>)" if dt else "-"


class Info(commands.Cog):
    """Read-only information about users, roles, the server and the bot."""

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    @commands.hybrid_command(name="userinfo", description="Show information about a user")
    @app_commands.describe(user="User (default: you)")
    async def userinfo_cmd(self, ctx, user: Optional[discord.User] = None):
        """Show information about a user."""
        user = user or ctx.author
        member = ctx.guild.get_member(user.id)
        e = emb(str(user), color=member.color if member and member.color.value else discord.Color.blurple())
        e.set_thumbnail(url=user.display_avatar.url)
        e.add_field(name="ID", value=str(user.id))
        e.add_field(name="Account created", value=stamp(user.created_at), inline=False)
        if member:
            e.add_field(name="Joined", value=stamp(member.joined_at), inline=False)
            roles = [r.mention for r in reversed(member.roles) if not r.is_default()]
            e.add_field(name=f"Roles ({len(roles)})", value=" ".join(roles[:15]) + (" ..." if len(roles) > 15 else "") if roles else "-", inline=False)
            if member.premium_since:
                e.add_field(name="Boosting since", value=stamp(member.premium_since))
            if member.timed_out_until:
                e.add_field(name="Timeout until", value=stamp(member.timed_out_until))
        if ctx.author.guild_permissions.moderate_members:
            cases = [c for c in self.bot.store.cases(ctx.guild.id) if c["user"] == user.id]
            warns = self.bot.get_cog("Moderation").active_warns(ctx.guild.id, user.id)
            e.add_field(name="Moderation", value=f"{len(cases)} cases, {warns} active warnings", inline=False)
            if self.bot.store.users(ctx.guild.id).get(str(user.id), {}).get("jailed"):
                e.add_field(name="Gulag", value="currently in the gulag", inline=False)
        await ctx.send(embed=e)

    @commands.hybrid_command(name="serverinfo", description="Show information about this server")
    async def serverinfo_cmd(self, ctx):
        """Show information about this server."""
        g = ctx.guild
        humans = sum(1 for m in g.members if not m.bot)
        e = emb(g.name, color=discord.Color.blurple())
        if g.icon:
            e.set_thumbnail(url=g.icon.url)
        e.add_field(name="ID", value=str(g.id))
        e.add_field(name="Owner", value=f"<@{g.owner_id}>")
        e.add_field(name="Created", value=stamp(g.created_at), inline=False)
        e.add_field(name="Members", value=f"{g.member_count} ({humans} humans, {g.member_count - humans} bots)")
        e.add_field(name="Channels", value=f"{len(g.text_channels)} text, {len(g.voice_channels)} voice, {len(g.categories)} categories")
        e.add_field(name="Roles", value=str(len(g.roles) - 1))
        e.add_field(name="Boosts", value=f"{g.premium_subscription_count} (level {g.premium_tier})")
        e.add_field(name="Emojis", value=f"{len(g.emojis)} of {g.emoji_limit}")
        await ctx.send(embed=e)

    @commands.hybrid_command(name="roleinfo", description="Show information about a role")
    @app_commands.describe(role="Role")
    async def roleinfo_cmd(self, ctx, role: discord.Role):
        """Show information about a role."""
        e = emb(role.name, color=role.color if role.color.value else discord.Color.blurple())
        e.add_field(name="ID", value=str(role.id))
        e.add_field(name="Members", value=str(len(role.members)))
        e.add_field(name="Position", value=str(role.position))
        e.add_field(name="Created", value=stamp(role.created_at), inline=False)
        e.add_field(name="Colour", value=str(role.color))
        e.add_field(name="Shown separately", value="yes" if role.hoist else "no")
        e.add_field(name="Mentionable", value="yes" if role.mentionable else "no")
        perms = [name.replace("_", " ") for name, value in role.permissions if value]
        e.add_field(name="Permissions", value=("administrator" if role.permissions.administrator else ", ".join(perms[:20]) + (" ..." if len(perms) > 20 else "")) or "-", inline=False)
        await ctx.send(embed=e)

    @commands.hybrid_command(name="avatar", description="Show the profile picture of a user")
    @app_commands.describe(user="User (default: you)")
    async def avatar_cmd(self, ctx, user: Optional[discord.User] = None):
        """Show the profile picture of a user."""
        user = user or ctx.author
        e = emb(f"Avatar of {user}", color=discord.Color.blurple())
        e.set_image(url=user.display_avatar.replace(size=1024).url)
        await ctx.send(embed=e)

    @commands.hybrid_command(name="ping", description="Show the latency of the bot")
    async def ping_cmd(self, ctx):
        """Show the latency of the bot."""
        await ctx.send(f"Pong. Gateway latency: {round(self.bot.latency * 1000)} ms", ephemeral=True)

    @commands.hybrid_command(name="botinfo", description="Show version, uptime and statistics of the bot")
    async def botinfo_cmd(self, ctx):
        """Show version, uptime and statistics of the bot."""
        db = Path(self.bot.settings.get("data_dir", "data")) / "guardbot.db"
        e = emb("GuardBot", "Open source Discord bot for moderation, security and community.\nBugs, ideas and suggestions: Discord @justyyin", discord.Color.blurple())
        e.add_field(name="Version", value=__version__)
        e.add_field(name="Uptime", value=fmt_duration(time.time() - self.bot.started))
        e.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)} ms")
        e.add_field(name="Servers", value=str(len(self.bot.guilds)))
        e.add_field(name="Python", value=platform.python_version())
        e.add_field(name="discord.py", value=discord.__version__)
        e.add_field(name="Database", value=f"{db.stat().st_size // 1024} KB" if db.exists() else "-")
        await ctx.send(embed=e, ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Info(bot))
