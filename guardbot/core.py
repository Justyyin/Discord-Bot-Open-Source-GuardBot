"""Bot class, SQLite storage, command checks and start-up."""

import asyncio
import copy
import copy as _copy
import hashlib
import json
import logging
import re
import sys
import time
import traceback
from pathlib import Path

import aiohttp
import discord
from discord.ext import commands

from . import __version__, i18n
from . import layout
from .dashboard import Dashboard
from .health import StatusServer, write_heartbeat
from .ai import AI
from .checks import Checks
from .logsetup import CONTEXT
from .metrics import Metrics
from .store import Store, dumps
from .tree import Tree
from .utils import CREDIT, emb
from .workers import Busy, Workers

log = logging.getLogger(__name__)

EXTENSIONS = (
    "server.admin",
    "server.logs",
    "security.automod",
    "moderation.moderation",
    "moderation.jail",
    "security.antinuke",
    "security.raid",
    "community.leveling",
    "community.roles",
    "community.welcome",
    "moderation.tickets",
    "community.engage",
    "community.community",
    "community.birthday",
    "server.backup",
    "security.verify",
    "server.privacy",
    "tools.tools",
    "tools.info",
    "community.tags",
    "tools.skills",
    "tools.aicog",
    "tools.panels",
    "tools.utility",
    "moderation.modmail",
    "moderation.appeals",
    "server.channels",
    "security.modwatch",
    "security.permaudit",
    "moderation.reports",
    "server.invites",
    "server.debug",
    "server.setup",
    "community.economy",
    "community.rolemenu",
    "community.schedule",
    "community.feeds",
    "community.activity",
    "moderation.bulk",
    "security.antiscam",
    "security.probation",
    "moderation.approval",
    "moderation.members",
    "server.structure",
    "server.rules",
    "moderation.history",
    "server.team",
    "server.applications",
    "security.exceptions",
    "tools.shortcuts",
    "tools.builder",
    "server.updates",
    "community.music",
)


def banner():
    """Return the start-up line with version, author and origin."""
    return f"GuardBot {__version__} (beta)  |  {CREDIT}  |  made in Germany"


def _prefix(bot, message):
    """Return the command prefix of the server, or the mention for direct use."""
    p = bot.prefix_for(message.guild.id) if message.guild else bot.settings.get("prefix", "!")
    return commands.when_mentioned_or(p)(bot, message)


class Bot(Checks, commands.AutoShardedBot):
    """The Discord bot with storage, checks and the log queue. Uses shards automatically when Discord asks for them."""
    def __init__(self, settings):
        """Create the bot with the needed intents, storage and command checks."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = bool(settings.get("members_intent", True))
        intents.dm_messages = False
        intents.dm_reactions = False
        intents.dm_typing = False
        intents.guild_typing = False
        shards = settings.get("shard_count")
        super().__init__(
            shard_count=int(shards) if shards else None,
            command_prefix=_prefix,
            intents=intents,
            tree_cls=Tree,
            help_command=None,
            max_messages=int(settings.get("message_cache", 10000)) or None,
            chunk_guilds_at_startup=bool(settings.get("chunk_guilds", True)),
            allowed_mentions=discord.AllowedMentions.none(),
        )
        self.settings = settings
        self.store = Store(settings.get("data_dir", "data"))
        self.work = Workers(settings)
        self.ai = AI(self)
        self.metrics = Metrics()
        self.session = None
        self.queue = None
        self.bot_deleted = set()
        self.canonical = {}
        self.started = time.time()
        self._error_sent = {}
        self._state_seen = {}
        self.closing = False
        self.restart_requested = False
        self.music_bot = None
        self.layout = {}
        self.actors = {}
        self.status_server = StatusServer(self)
        self.dashboard = Dashboard(self)
        self.add_check(self._global_check)

    def _schedule_event(self, coro, event_name, *args, **kwargs):
        """Skip listeners of cogs whose module is off on the server of the event. A cog opts in with a gate dict such as {"on_message": "automod"}."""
        gate = getattr(getattr(coro, "__self__", None), "gate", None)
        guild = getattr(args[0], "guild", None) if args else None
        if gate and guild is not None and event_name in gate and not self.module_on(guild.id, gate[event_name]):
            return None
        token = CONTEXT.set({"guild": guild.id, "command": event_name}) if guild is not None else None
        try:
            return super()._schedule_event(coro, event_name, *args, **kwargs)
        finally:
            if token is not None:
                CONTEXT.reset(token)

    def cfg(self, gid):
        """Return the settings of a server."""
        return self.store.cfg(gid)

    def module_on(self, gid, name):
        """True if a module is turned on for a server."""
        return self.cfg(gid)["modules"].get(name, True)

    def prefix_for(self, gid):
        """Return the text command prefix of a server."""
        return self.cfg(gid)["prefix"] or self.settings.get("prefix", "!")

    def report_error(self, guild, where, error):
        """Count an unexpected error and post a short report to the error channel of the server, at most one every five seconds."""
        if guild is None:
            return
        self.metrics.error()
        d = self.cfg(guild.id)["debug"]
        d["errors"] += 1
        channel = d["error_channel"]
        now = time.monotonic()
        if not channel or not self.module_on(guild.id, "debug") or self.queue is None or now - self._error_sent.get(guild.id, 0) < 5:
            return
        self._error_sent[guild.id] = now
        original = getattr(error, "original", error)
        frames = [f for f in traceback.extract_tb(original.__traceback__) if "guardbot" in f.filename][-5:]
        e = emb("Unexpected error", color=discord.Color.red())
        e.add_field(name="Where", value=where, inline=False)
        e.add_field(name="Error", value=f"{type(original).__name__}: {str(original)[:300]}", inline=False)
        if frames:
            e.add_field(name="Trace", value="\n".join(f"{Path(f.filename).name}:{f.lineno} {f.name}" for f in frames), inline=False)
        self.queue.put_nowait((channel, e, []))

    async def on_error(self, event_method, *args, **kwargs):
        """Log errors of event listeners and report them to the error channel."""
        error = sys.exc_info()[1]
        log.error("unhandled error in %s", event_method, exc_info=error)
        guild = next((g for g in (getattr(a, "guild", None) for a in args) if g), None)
        self.report_error(guild, event_method, error)

    async def get_context(self, message, *, cls=commands.Context):
        """Resolve per-server aliases before the command is looked up."""
        jail = self.get_cog("Jail")
        if jail is not None and message.guild and jail.claims(message):
            message = _copy.copy(message)
            message.content = ""
            return await super().get_context(message, cls=cls)
        if message.guild and message.content:
            g = self.cfg(message.guild.id)
            p = self.prefix_for(message.guild.id)
            if g["aliases"] and message.content.startswith(p):
                parts = message.content[len(p):].split(None, 1)
                if parts and parts[0].lower() in g["aliases"]:
                    message = _copy.copy(message)
                    rest = " " + parts[1] if len(parts) > 1 else ""
                    message.content = p + g["aliases"][parts[0].lower()] + rest
        return await super().get_context(message, cls=cls)

    async def on_command_error(self, ctx, error):
        """Answer failed text and hybrid commands and log unexpected errors."""
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(getattr(error, "original", None), Busy):
            text = i18n.say(self, ctx.guild, "The bot is busy with this kind of work. Try again in a moment.")
        elif isinstance(error, commands.CommandInvokeError):
            log.error("unhandled error in command %s", ctx.command, exc_info=error)
            self.report_error(ctx.guild, f"{ctx.prefix}{ctx.command.qualified_name if ctx.command else '?'}", error)
            text = i18n.say(self, ctx.guild, "Something went wrong.")
        elif isinstance(error, commands.CheckFailure):
            text = str(error) or i18n.say(self, ctx.guild, "You are not allowed to use this command.")
        elif isinstance(error, (commands.UserInputError, commands.BadUnionArgument)):
            text = f"Invalid input: {error}"
        else:
            text = i18n.say(self, ctx.guild, "Something went wrong.")
        try:
            await ctx.send(text, ephemeral=True)
        except discord.HTTPException as exc:
            log.warning("ctx.send failed: %s", exc)

    def log(self, guild, category, embed, files=None):
        """Queue an embed for the log channel of a category."""
        lc = self.cfg(guild.id)["log"]
        ch = lc.get(category) or lc.get("main")
        if ch and self.queue is not None and self.queue.qsize() < 2000:
            self.queue.put_nowait((ch, embed, files or []))

    def is_log_channel(self, guild, channel_id):
        """True if the channel is one of the configured log channels."""
        return channel_id in {v for v in self.cfg(guild.id)["log"].values() if v}

    async def _log_worker(self):
        """Send queued log embeds one by one to stay inside the rate limits."""
        while True:
            ch_id, embed, files = await self.queue.get()
            ch = self.get_channel(ch_id)
            if ch:
                try:
                    await ch.send(embed=embed, files=files)
                except discord.HTTPException as exc:
                    log.warning("ch.send failed: %s", exc)
            await asyncio.sleep(0.5)

    async def _autosave(self):
        """Save changed data and the runtime state of the cogs every ten seconds."""
        while True:
            await asyncio.sleep(10)
            try:
                await self.store.aflush()
                if not self.closing:
                    self.save_states()
            except Exception:
                log.exception("autosave failed")

    def save_states(self):
        """Ask every cog that has export_state() for its runtime state and save it when it changed."""
        for name, cog in self.cogs.items():
            export = getattr(cog, "export_state", None)
            if export is None:
                continue
            state = export()
            digest = dumps(state)
            if self._state_seen.get(name) != digest:
                self._state_seen[name] = digest
                self.store.set_state(name, state or None)

    async def _housekeeping(self):
        """Write the heartbeat every 30 seconds and make the automatic database backup when it is due."""
        directory = Path(self.settings.get("data_dir", "data"))
        while True:
            try:
                write_heartbeat(directory / "heartbeat")
                hours = float(self.settings.get("db_backup_hours", 24))
                last = float(self.store.get_meta("last_db_backup") or 0)
                if hours > 0 and time.time() - last >= hours * 3600:
                    path = await self.work.run("maintenance", self.store.backup, "auto", int(self.settings.get("db_backup_keep", 7)))
                    self.store.set_meta("last_db_backup", str(int(time.time())))
                    log.info("database backup written: %s", path.name)
            except Exception:
                log.exception("housekeeping failed")
            await asyncio.sleep(30)

    def arrange_commands(self):
        """Apply the renames from settings.json, then gather the commands into their groups."""
        self.apply_command_names()
        layout.apply(self)
        self.tree.loading = False

    def apply_command_names(self):
        """Rename commands as configured in settings.json."""
        for old, new in self.settings.get("command_names", {}).items():
            new = str(new).lower()
            if not re.fullmatch(r"[\w-]{1,32}", new):
                log.warning("command_names: %r is not a valid name, skipped", new)
                continue
            cmd = self.get_command(old)
            if cmd:
                self.remove_command(old)
                cmd.name = new
                self.add_command(cmd)
                app = getattr(cmd, "app_command", None)
                if app:
                    self.tree.remove_command(old)
                    app.name = new
                    self.tree.add_command(app)
            else:
                app = self.tree.get_command(old)
                if not app:
                    log.warning("command_names: unknown command %r, skipped", old)
                    continue
                self.tree.remove_command(old)
                app.name = new
                self.tree.add_command(app)
            self.canonical[new] = old

    async def setup_hook(self):
        """Open the HTTP session, load all cogs and sync slash commands when they changed."""
        self.session = aiohttp.ClientSession()
        self.queue = asyncio.Queue()
        self._jobs = [asyncio.create_task(self._log_worker()), asyncio.create_task(self._autosave()), asyncio.create_task(self._housekeeping())]
        for ext in EXTENSIONS:
            if ext == "community.music" and self.music_bot is not None:
                continue
            await self.load_extension(f"guardbot.cogs.{ext}")
        self.arrange_commands()
        await self.status_server.start()
        await self.dashboard.start()
        payload = json.dumps([c.to_dict(self.tree) for c in self.tree.get_commands()], sort_keys=True, default=str)
        digest = hashlib.sha256((payload + str(self.application_id)).encode()).hexdigest()
        if self.settings.get("force_sync") or "--sync" in sys.argv or self.store.get_meta("sync_hash") != digest:
            await self.tree.sync()
            self.store.set_meta("sync_hash", digest)
            log.info("slash commands synced")
        else:
            log.info("slash commands unchanged, sync skipped")

    async def close(self):
        """Save the data and close the connections."""
        self.save_states()
        self.closing = True
        if self.music_bot is not None and not self.music_bot.is_closed():
            await self.music_bot.close()
        await self.status_server.stop()
        await self.dashboard.stop()
        self.store.close()
        self.work.close()
        if self.session:
            await self.session.close()
        await super().close()

    async def on_app_command_completion(self, interaction, command):
        """Record how long a finished slash command took."""
        start = interaction.extras.get("gb_start")
        if start is not None:
            self.metrics.observe("/" + command.qualified_name, time.perf_counter() - start)

    async def on_command_completion(self, ctx):
        """Record how long a finished text command took."""
        start = getattr(ctx, "gb_start", None)
        if start is not None:
            self.metrics.observe(self.prefix_for(ctx.guild.id) + ctx.command.qualified_name, time.perf_counter() - start)

    def music_cog(self):
        """The music cog, on Guard Music when the second bot runs, otherwise on this bot."""
        if self.music_bot is not None:
            return self.music_bot.get_cog("Music")
        return self.get_cog("Music")

    async def on_ready(self):
        """Log that the bot is online."""
        log.info("online as %s on %d server(s)", self.user, len(self.guilds))
