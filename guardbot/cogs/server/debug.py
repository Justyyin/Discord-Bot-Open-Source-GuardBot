"""Diagnostics: configuration self-test, error reports, usage statistics and database maintenance."""

import asyncio
import hashlib
import logging
from typing import Literal, Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from ...cog import BaseCog
from ... import __version__, i18n, layout, updater
from ...defaults import LOG_CATEGORIES
from ...utils import emb, trim

log = logging.getLogger(__name__)

NEEDS = {
    "moderation": ("ban_members", "kick_members", "moderate_members"),
    "automod": ("manage_messages", "moderate_members"),
    "logging": ("view_audit_log",),
    "jail": ("manage_roles", "manage_channels"),
    "antinuke": ("view_audit_log", "manage_roles", "ban_members"),
    "modwatch": ("view_audit_log",),
    "permaudit": ("view_audit_log",),
    "invites": ("manage_guild",),
    "tickets": ("manage_channels", "manage_roles"),
    "tempvoice": ("manage_channels", "move_members"),
    "backup": ("manage_roles", "manage_channels", "manage_guild"),
    "reactionroles": ("manage_roles",),
}
# (module, label, path in the settings, kind)
TARGETS = (
    [("logging", f"log channel {c}", ("log", c), "logsend") for c in LOG_CATEGORIES]
    + [
        ("welcome", "welcome channel", ("welcome", "channel"), "send"),
        ("welcome", "goodbye channel", ("welcome", "goodbye_channel"), "send"),
        ("welcome", "welcome roles", ("welcome", "roles"), "roles"),
        ("welcome", "bot roles", ("welcome", "bot_roles"), "roles"),
        ("boosters", "booster channel", ("boosters", "channel"), "send"),
        ("boosters", "booster roles", ("boosters", "roles"), "roles"),
        ("starboard", "starboard channel", ("starboard", "channel"), "send"),
        ("suggestions", "suggestion channel", ("suggestions", "channel"), "send"),
        ("suggestions", "suggestion review role", ("suggestions", "review_role"), "exists"),
        ("birthday", "birthday channel", ("birthday", "channel"), "send"),
        ("birthday", "birthday role", ("birthday", "role"), "role"),
        ("jail", "gulag role", ("jail", "role"), "role"),
        ("jail", "gulag channel", ("jail", "channel"), "send"),
        ("jail", "gulag staff role", ("jail", "staff_role"), "exists"),
        ("verification", "verification channel", ("verify", "channel"), "send"),
        ("verification", "verified role", ("verify", "verified_role"), "role"),
        ("verification", "unverified role", ("verify", "unverified_role"), "role"),
        ("tickets", "ticket category", ("tickets", "category"), "category"),
        ("tickets", "ticket support role", ("tickets", "support_role"), "exists"),
        ("tickets", "ticket log channel", ("tickets", "log_channel"), "send"),
        ("modmail", "mod-mail category", ("modmail", "category"), "category"),
        ("modmail", "mod-mail staff role", ("modmail", "staff_role"), "exists"),
        ("modmail", "mod-mail log channel", ("modmail", "log_channel"), "send"),
        ("reports", "report channel", ("reports", "channel"), "send"),
        ("counting", "counting channel", ("counting", "channel"), "send"),
        ("leveling", "level-up channel", ("xp", "announce_channel"), "send"),
        ("tempvoice", "voice hub", ("tempvoice", "hub"), "voice"),
        ("tempvoice", "voice category", ("tempvoice", "category"), "category"),
        ("appeals", "appeal staff channel", ("appeals", "staff_channel"), "send"),
        ("debug", "error channel", ("debug", "error_channel"), "send"),
    ]
)


def pretty(name):
    """Turn a permission name into words."""
    return name.replace("_", " ")


class Debug(BaseCog):
    """Self-test, error reporting, statistics and database tools."""
    section = "debug"

    dg = app_commands.Group(name="debug", description="Diagnostics and statistics", default_permissions=discord.Permissions(administrator=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    def lookup(self, cfg, path):
        """Read a value from the settings by its path."""
        for key in path:
            cfg = cfg.get(key) if isinstance(cfg, dict) else None
        return cfg

    def check_target(self, guild, label, value, kind):
        """Check one configured channel or role and return a problem text or None."""
        me = guild.me
        if kind == "roles":
            problems = [self.check_target(guild, label, v, "role") for v in value or []]
            return "; ".join(p for p in problems if p) or None
        if kind in ("exists", "role"):
            role = guild.get_role(value)
            if role is None:
                return f"{label}: the role no longer exists"
            if kind == "role" and role.managed:
                return f"{label}: {role.name} is managed by an integration and cannot be given"
            if kind == "role" and role >= me.top_role:
                return f"{label}: {role.name} is above my highest role, so I cannot give or take it"
            return None
        channel = guild.get_channel(value)
        if channel is None:
            return f"{label}: the channel no longer exists"
        perms = channel.permissions_for(me)
        if kind == "category":
            if not isinstance(channel, discord.CategoryChannel):
                return f"{label}: {channel.name} is not a category"
            need = ("view_channel", "manage_channels")
        elif kind == "voice":
            need = ("view_channel", "manage_channels", "move_members")
        else:
            need = ("view_channel", "send_messages", "embed_links") + (("attach_files",) if kind == "logsend" else ())
        missing = [pretty(p) for p in need if not getattr(perms, p)]
        return f"{label}: I am missing {', '.join(missing)} in #{channel.name}" if missing else None

    def selftest(self, guild):
        """Check the permissions of the bot and every configured channel and role. Returns (problems, number of checks)."""
        cfg = self.bot.cfg(guild.id)
        problems, checks = [], 0
        gp = guild.me.guild_permissions
        for module, perms in NEEDS.items():
            if cfg["modules"].get(module):
                checks += 1
                missing = [pretty(p) for p in perms if not getattr(gp, p) and not gp.administrator]
                if missing:
                    problems.append(f"module {module}: I am missing the server permissions {', '.join(missing)}")
        for module, label, path, kind in TARGETS:
            if not cfg["modules"].get(module):
                continue
            value = self.lookup(cfg, path)
            if value in (None, [], 0):
                continue
            checks += 1
            problem = self.check_target(guild, label, value, kind)
            if problem:
                problems.append(problem)
        for level, role_id in cfg["xp"]["level_roles"].items() if cfg["modules"].get("leveling") else ():
            checks += 1
            problem = self.check_target(guild, f"level {level} role", role_id, "role")
            if problem:
                problems.append(problem)
        return problems, checks

    def report_embed(self, problems, checks, title):
        """Build the embed that lists the problems of a self-test."""
        e = emb(title, color=discord.Color.orange() if problems else discord.Color.green())
        if problems:
            shown = problems[:15]
            e.description = trim("\n".join(f"- {p}" for p in shown) + (f"\n... and {len(problems) - 15} more" if len(problems) > 15 else ""), 3800)
            e.add_field(name="Result", value=f"{len(problems)} problem(s) in {checks} checks")
        else:
            e.description = f"All {checks} checks passed."
        return e

    @commands.hybrid_command(name="diagnose", description="Check my permissions, role order and the configured channels and roles")
    @commands.guild_only()
    async def diagnose(self, ctx):
        """Check my permissions, role order and the configured channels and roles."""
        problems, checks = self.selftest(ctx.guild)
        await ctx.send(embed=self.report_embed(problems, checks, "Diagnosis"), ephemeral=True)

    async def startup_check(self, guild):
        """Run the self-test for a server and post it when the problems changed since the last report."""
        d = self.conf(guild.id)
        if not d["selftest"] or not self.bot.module_on(guild.id, "debug"):
            return
        problems, checks = self.selftest(guild)
        digest = hashlib.sha256("\n".join(problems).encode()).hexdigest() if problems else None
        if digest == d["last_hash"]:
            return
        d["last_hash"] = digest
        if not problems:
            return
        e = self.report_embed(problems, checks, "Configuration check at start-up")
        if d["error_channel"] and self.bot.queue is not None:
            self.bot.queue.put_nowait((d["error_channel"], e, []))
        else:
            self.bot.log(guild, "security", e)

    @commands.Cog.listener()
    async def on_ready(self):
        """Check every server once the bot is connected."""
        for guild in self.bot.guilds:
            try:
                await self.startup_check(guild)
            except (discord.HTTPException, AttributeError, KeyError) as exc:
                log.warning("start-up check of %s failed: %s", guild.id, exc)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Check a server the bot was just added to."""
        await asyncio.sleep(3)
        await self.startup_check(guild)

    @dg.command(name="status", description="Show the debug settings")
    async def status(self, it: discord.Interaction):
        """Show the debug settings."""
        d = self.conf(it.guild_id)
        size = self.bot.store.file_size() / 1024
        lines = [
            f"Module: {'on' if self.bot.module_on(it.guild_id, 'debug') else 'off'}",
            f"Error channel: {'<#' + str(d['error_channel']) + '>' if d['error_channel'] else 'not set'}",
            f"Start-up check: {d['selftest']}, usage statistics: {d['usage_stats']}",
            f"Errors counted: {d['errors']}",
            f"Log level of the bot: {logging.getLevelName(logging.getLogger('guardbot').getEffectiveLevel())}",
            f"Database: {size:.0f} KB",
        ]
        await it.response.send_message("\n".join(lines), ephemeral=True)

    @dg.command(name="errorchannel", description="Choose the channel for error reports (no channel = turn off)")
    async def errorchannel(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None):
        """Choose the channel for error reports (no channel = turn off)."""
        self.conf(it.guild_id)["error_channel"] = channel.id if channel else None
        await it.response.send_message(f"Error reports go to {channel.mention}." if channel else "Error reports are off.", ephemeral=True)

    @dg.command(name="errortest", description="Send a test message to the error channel")
    async def errortest(self, it: discord.Interaction):
        """Send a test message to the error channel."""
        ch = self.conf(it.guild_id)["error_channel"]
        if not ch:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Set an error channel first with /server debug errorchannel."), ephemeral=True)
        self.bot.queue.put_nowait((ch, emb("Error report test", "This is how an error report looks. Nothing is wrong.", discord.Color.green()), []))
        await it.response.send_message(i18n.say(it.client, it.guild, "Test sent."), ephemeral=True)

    @dg.command(name="selftest", description="Turn the configuration check at start-up on or off")
    async def selftest_cmd(self, it: discord.Interaction, enabled: bool):
        """Turn the configuration check at start-up on or off."""
        self.conf(it.guild_id)["selftest"] = enabled
        await it.response.send_message(i18n.say(it.client, it.guild, "Start-up check: {value}.", value='on' if enabled else 'off'), ephemeral=True)

    @dg.command(name="usagestats", description="Turn the counting of command uses on or off")
    async def usagestats(self, it: discord.Interaction, enabled: bool):
        """Turn the counting of command uses on or off."""
        self.conf(it.guild_id)["usage_stats"] = enabled
        await it.response.send_message(i18n.say(it.client, it.guild, "Usage statistics: {value}. Only the number per command is counted, never who used it.", value='on' if enabled else 'off'), ephemeral=True)

    @dg.command(name="usage", description="Show which commands are used and which AutoMod rules trigger most")
    @app_commands.describe(reset="Set all counters back to zero")
    async def usage(self, it: discord.Interaction, reset: bool = False):
        """Show which commands are used and which AutoMod rules trigger most."""
        g = self.bot.cfg(it.guild_id)
        d, hits = g["debug"], g["automod"]["hits"]
        top = sorted(d["usage"].items(), key=lambda kv: -kv[1])[:15]
        rules = sorted(hits.items(), key=lambda kv: -kv[1])
        e = emb("Usage")
        e.add_field(name="Commands", value="\n".join(f"/{layout.slash_path(self.bot, k)}: {v}" for k, v in top) or "nothing counted yet", inline=False)
        e.add_field(name="AutoMod rules", value="\n".join(f"{k}: {v}" for k, v in rules) or "no hits yet", inline=False)
        e.add_field(name="Errors", value=str(d["errors"]))
        if reset:
            d["usage"].clear()
            hits.clear()
            d["errors"] = 0
            e.set_footer(text="Counters were reset after this report.")
        await it.response.send_message(embed=e, ephemeral=True)

    async def owner_only(self, it):
        """Answer and return False when the user is not the owner of the bot."""
        if await self.bot.is_owner(it.user):
            return True
        await it.response.send_message(i18n.say(it.client, it.guild, "Only the owner of the bot can do this, because it affects every server."), ephemeral=True)
        return False

    @dg.command(name="level", description="Change how much the bot writes to its log file (owner of the bot only)")
    @app_commands.describe(level="DEBUG is very detailed, WARNING shows only problems")
    async def level(self, it: discord.Interaction, level: Literal["DEBUG", "INFO", "WARNING"]):
        """Change how much the bot writes to its log file (owner of the bot only)."""
        if not await self.owner_only(it):
            return
        logging.getLogger("guardbot").setLevel(getattr(logging, level))
        log.warning("log level set to %s by %s", level, it.user.id)
        await it.response.send_message(i18n.say(it.client, it.guild, "Log level: {level}. It applies to the bot's own messages until the next restart. Discord's gateway log is not changed because it can contain message content.", level=level), ephemeral=True)

    @dg.command(name="update", description="Check for a new version on GitHub and install it (owner of the bot only)")
    @app_commands.describe(action="status = show the state, check = ask GitHub now, install = download and install the newer version and restart")
    async def update(self, it: discord.Interaction, action: Literal["status", "check", "install"]):
        """Check for a new version on GitHub and install it (owner of the bot only)."""
        if not await self.owner_only(it):
            return
        cog = self.bot.get_cog("Updates")
        if cog is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "The update module is not loaded."), ephemeral=True)
        await it.response.defer(ephemeral=True)
        if action == "status":
            return await it.followup.send(cog.status())
        if not updater.valid_repo(cog.repo):
            return await it.followup.send(i18n.say(it.client, it.guild, "No repository is set. Put \"update\": {\"repo\": \"owner/name\"} into settings.json."))
        try:
            release = await cog.check()
        except (ValueError, aiohttp.ClientError, asyncio.TimeoutError) as exc:
            return await it.followup.send(i18n.say(it.client, it.guild, "The check failed: {exc}", exc=exc))
        if release is None:
            return await it.followup.send(i18n.say(it.client, it.guild, "You run the newest version ({version}).", version=__version__))
        if action == "check":
            return await it.followup.send(i18n.say(it.client, it.guild, "Version {tag} is available. Run /server debug update action:install to install it.", tag=release['tag']))
        ok, message = await cog.install()
        await it.followup.send(("Done: " if ok else "Not installed: ") + message)

    @dg.command(name="db", description="Check or shrink the database (owner of the bot only)")
    @app_commands.describe(action="check = integrity test, vacuum = free unused space, size = show the size, backup = save a copy now, list = show the backups")
    async def db(self, it: discord.Interaction, action: Literal["check", "vacuum", "size", "backup", "list"]):
        """Check or shrink the database (owner of the bot only)."""
        if not await self.owner_only(it):
            return
        await it.response.defer(ephemeral=True)
        store = self.bot.store
        before = store.file_size()
        if action == "size":
            return await it.followup.send(i18n.say(it.client, it.guild, "Database: {value} KB", value=format(before / 1024, ".0f")))
        if action == "backup":
            path = await self.bot.work.run("maintenance", store.backup, "manual")
            return await it.followup.send(i18n.say(it.client, it.guild, "Backup saved as data/dbbackups/{name} ({value} KB). It contains all stored data, keep it private.", name=path.name, value=format(path.stat().st_size / 1024, ".0f")))
        if action == "list":
            files = sorted((store.dir / "dbbackups").glob("guardbot-*.db"), reverse=True)[:15]
            return await it.followup.send("\n".join(f"{f.name} ({f.stat().st_size / 1024:.0f} KB)" for f in files) or "No backups yet.")
        if action == "check":
            result = await self.bot.work.run("maintenance", store.integrity)
            return await it.followup.send("Integrity check: " + ("ok" if result == ["ok"] else trim("; ".join(result), 1500)))
        await self.bot.work.run("maintenance", store.vacuum)
        await it.followup.send(i18n.say(it.client, it.guild, "Done. {value} KB before, {value2} KB after.", value=format(before / 1024, ".0f"), value2=format(store.file_size() / 1024, ".0f")))


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Debug(bot))
