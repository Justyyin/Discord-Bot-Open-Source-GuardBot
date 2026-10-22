"""Bot class, SQLite storage, command checks and start-up."""

import asyncio
import copy
import copy as _copy
import hashlib
import json
import logging
import re
import sqlite3
import sys
import threading
import time
import traceback
from pathlib import Path

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.hybrid import HybridAppCommand

from . import __version__, i18n, migrations
from .dashboard import Dashboard
from .health import StatusServer, write_heartbeat
from .defaults import COMMAND_MODULES, DEFAULTS, FALLBACK_PERMS
from .utils import CREDIT, emb

log = logging.getLogger(__name__)

EXTENSIONS = (
    "admin",
    "logs",
    "automod",
    "moderation",
    "jail",
    "antinuke",
    "raid",
    "leveling",
    "roles",
    "welcome",
    "tickets",
    "engage",
    "community",
    "birthday",
    "backup",
    "verify",
    "privacy",
    "tools",
    "info",
    "tags",
    "utility",
    "modmail",
    "appeals",
    "channels",
    "modwatch",
    "permaudit",
    "reports",
    "invites",
    "debug",
    "setup",
    "economy",
    "rolemenu",
    "schedule",
    "feeds",
    "activity",
    "bulk",
    "antiscam",
    "probation",
    "shortcuts",
    "builder",
    "updates",
    "music",
)


def banner():
    """Return the start-up line with version, author and origin."""
    return f"GuardBot {__version__} (beta)  |  {CREDIT}  |  made in Germany"


def fill(d, default):
    """Add missing keys of a default dict to a settings dict, including nested ones."""
    for k, v in default.items():
        if k not in d:
            d[k] = copy.deepcopy(v)
        elif isinstance(v, dict) and v:
            fill(d[k], v)


def dumps(obj):
    """Serialize to compact JSON."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


class Touched:
    """Collects the keys of changed rows over two periods so late edits are not lost."""
    def __init__(self):
        """Start with empty sets for the current and the previous period."""
        self.now, self.prev = set(), set()

    def add(self, key):
        """Remember that a key changed."""
        self.now.add(key)

    def take(self):
        """Return the keys changed in this and the previous period and start a new period."""
        out = self.now | self.prev
        self.prev, self.now = self.now, set()
        return out


class Store:
    """SQLite backed storage with in-memory caches and change detection."""
    def __init__(self, directory):
        """Open the database, load all data and import old JSON files."""
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.dir / "guardbot.db", check_same_thread=False)
        self.lock = threading.Lock()
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=NORMAL")
        self.db.executescript(
            "CREATE TABLE IF NOT EXISTS config(gid TEXT PRIMARY KEY, data TEXT NOT NULL);"
            "CREATE TABLE IF NOT EXISTS users(gid TEXT NOT NULL, uid TEXT NOT NULL, data TEXT NOT NULL, PRIMARY KEY(gid, uid));"
            "CREATE TABLE IF NOT EXISTS cases(gid TEXT NOT NULL, id INTEGER NOT NULL, data TEXT NOT NULL, PRIMARY KEY(gid, id));"
            "CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);"
        )
        self.config, self.user_data, self.case_data = {}, {}, {}
        self.saved = {}
        self.t_cfg, self.t_users, self.t_cases = Touched(), Touched(), Touched()
        self.filled = set()
        self._load()
        self._migrate()
        migrations.run(self)

    def _load(self):
        """Read all rows from the database into memory."""
        for gid, data in self.db.execute("SELECT gid, data FROM config"):
            self.config[gid] = json.loads(data)
            self.saved[("c", gid)] = hash(data)
        for gid, uid, data in self.db.execute("SELECT gid, uid, data FROM users"):
            self.user_data.setdefault(gid, {})[uid] = json.loads(data)
            self.saved[("u", gid, uid)] = hash(data)
        for gid, cid, data in self.db.execute("SELECT gid, id, data FROM cases ORDER BY id"):
            self.case_data.setdefault(gid, []).append(json.loads(data))
            self.saved[("k", gid, cid)] = hash(data)

    def _migrate(self):
        """Import the old JSON files once and rename them."""
        for name in ("config", "users", "cases"):
            p = self.dir / f"{name}.json"
            if not p.exists():
                continue
            try:
                old = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                log.warning("cannot import %s, it is not valid JSON: %s", p.name, exc)
                continue
            target = {"config": self.config, "users": self.user_data, "cases": self.case_data}[name]
            if target:
                continue
            for gid, value in old.items():
                target[gid] = value
                {"config": self.t_cfg, "users": self.t_users, "cases": self.t_cases}[name].add(gid)
                if name == "users":
                    self.t_users.now.discard(gid)
                    for uid in value:
                        self.t_users.add((gid, uid))
            p.replace(p.with_suffix(".json.migrated"))
        self.flush()

    def mark(self, *names):
        """Kept for old callers. Changes are detected automatically, so this does nothing."""
        return None

    def cfg(self, gid):
        """Return the settings dict of a server, filled with defaults."""
        gid = str(gid)
        g = self.config.setdefault(gid, {})
        if gid not in self.filled:
            fill(g, DEFAULTS)
            self.filled.add(gid)
        self.t_cfg.add(gid)
        return g

    def users(self, gid):
        """Return all stored user records of a server."""
        return self.user_data.setdefault(str(gid), {})

    def user(self, gid, uid):
        """Return the record of one user and create it if needed."""
        gid, uid = str(gid), str(uid)
        rec = self.user_data.setdefault(gid, {}).setdefault(uid, {"xp": 0, "birthday": None, "bday_last": None})
        self.t_users.add((gid, uid))
        return rec

    def cases(self, gid):
        """Return the moderation cases of a server."""
        gid = str(gid)
        self.t_cases.add(gid)
        return self.case_data.setdefault(gid, [])

    def delete_case(self, gid, case_id):
        """Remove one moderation case from memory and the database. Returns False if it does not exist."""
        gid = str(gid)
        cases = self.case_data.get(gid, [])
        before = len(cases)
        self.case_data[gid] = [c for c in cases if c["id"] != case_id]
        self.saved.pop(("k", gid, case_id), None)
        with self.lock, self.db:
            self.db.execute("DELETE FROM cases WHERE gid=? AND id=?", (gid, case_id))
        return len(self.case_data[gid]) < before

    def delete_user(self, gid, uid):
        """Delete the record of a user from memory and the database."""
        gid, uid = str(gid), str(uid)
        self.user_data.get(gid, {}).pop(uid, None)
        self.saved.pop(("u", gid, uid), None)
        with self.lock, self.db:
            self.db.execute("DELETE FROM users WHERE gid=? AND uid=?", (gid, uid))

    def drop_guild(self, gid):
        """Delete every stored row of a server."""
        gid = str(gid)
        self.config.pop(gid, None)
        self.user_data.pop(gid, None)
        self.case_data.pop(gid, None)
        self.filled.discard(gid)
        self.saved = {k: v for k, v in self.saved.items() if k[1] != gid}
        with self.lock, self.db:
            for table in ("config", "users", "cases"):
                self.db.execute(f"DELETE FROM {table} WHERE gid=?", (gid,))

    def get_meta(self, key):
        """Read a value from the meta table."""
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

    def set_meta(self, key, value):
        """Write a value to the meta table."""
        with self.lock, self.db:
            self.db.execute("INSERT INTO meta(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))

    def snapshot(self):
        """Serialize everything that changed since the last write and skip unchanged rows."""
        rows = {"c": [], "u": [], "k": []}
        for gid in self.t_cfg.take():
            if gid in self.config:
                text = dumps(self.config[gid])
                if self.saved.get(("c", gid)) != hash(text):
                    self.saved[("c", gid)] = hash(text)
                    rows["c"].append((gid, text))
        for gid, uid in self.t_users.take():
            rec = self.user_data.get(gid, {}).get(uid)
            if rec is not None:
                text = dumps(rec)
                if self.saved.get(("u", gid, uid)) != hash(text):
                    self.saved[("u", gid, uid)] = hash(text)
                    rows["u"].append((gid, uid, text))
        for gid in self.t_cases.take():
            for case in self.case_data.get(gid, []):
                text = dumps(case)
                key = ("k", gid, case["id"])
                if self.saved.get(key) != hash(text):
                    self.saved[key] = hash(text)
                    rows["k"].append((gid, case["id"], text))
        return rows

    def write(self, rows):
        """Write serialized rows to the database in one transaction."""
        if not any(rows.values()):
            return
        with self.lock, self.db:
            self.db.executemany("INSERT INTO config(gid, data) VALUES(?, ?) ON CONFLICT(gid) DO UPDATE SET data=excluded.data", rows["c"])
            self.db.executemany("INSERT INTO users(gid, uid, data) VALUES(?, ?, ?) ON CONFLICT(gid, uid) DO UPDATE SET data=excluded.data", rows["u"])
            self.db.executemany("INSERT INTO cases(gid, id, data) VALUES(?, ?, ?) ON CONFLICT(gid, id) DO UPDATE SET data=excluded.data", rows["k"])

    def flush(self):
        """Save all changes now."""
        self.write(self.snapshot())

    async def aflush(self):
        """Save all changes without blocking the event loop."""
        rows = self.snapshot()
        if any(rows.values()):
            await asyncio.to_thread(self.write, rows)

    def state(self, name):
        """Read a small piece of runtime state (counters, queues) that should survive a restart. Returns None if there is none."""
        raw = self.get_meta(f"state:{name}")
        try:
            return json.loads(raw) if raw else None
        except ValueError:
            log.warning("state %s is damaged and was ignored", name)
            return None

    def set_state(self, name, value):
        """Save runtime state. None removes it."""
        key = f"state:{name}"
        if value is None:
            with self.lock, self.db:
                self.db.execute("DELETE FROM meta WHERE key=?", (key,))
        else:
            self.set_meta(key, dumps(value))

    def backup(self, label="auto", keep=0):
        """Copy the database to data/dbbackups with SQLite's online backup. With keep > 0 only that many automatic backups stay."""
        self.flush()
        folder = self.dir / "dbbackups"
        folder.mkdir(exist_ok=True)
        dest = folder / f"guardbot-{time.strftime('%Y%m%d-%H%M%S')}-{label}.db"
        target = sqlite3.connect(dest)
        try:
            with self.lock:
                self.db.backup(target)
        finally:
            target.close()
        if keep > 0:
            old = sorted(folder.glob("guardbot-*-auto.db"))
            for f in old[:-keep]:
                f.unlink()
        return dest

    def integrity(self):
        """Run the SQLite integrity check and return its messages."""
        with self.lock:
            return [r[0] for r in self.db.execute("PRAGMA integrity_check")]

    def file_size(self):
        """Return the size of the database file and its write-ahead log in bytes."""
        total = 0
        for suffix in ("", "-wal"):
            f = self.dir / f"guardbot.db{suffix}"
            total += f.stat().st_size if f.exists() else 0
        return total

    def vacuum(self):
        """Save pending changes, then rebuild the database file to free unused space."""
        self.flush()
        with self.lock:
            self.db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            self.db.execute("VACUUM")

    def close(self):
        """Save everything and close the database."""
        for t in (self.t_cfg, self.t_users, self.t_cases):
            t.prev = t.now | t.prev
        self.flush()
        self.flush()
        self.db.close()


def _prefix(bot, message):
    """Return the command prefix of the server, or the mention for direct use."""
    p = bot.prefix_for(message.guild.id) if message.guild else bot.settings.get("prefix", "!")
    return commands.when_mentioned_or(p)(bot, message)


class Tree(app_commands.CommandTree):
    """Command tree that applies module, disable and permission checks to slash commands."""
    async def interaction_check(self, interaction):
        """Block slash commands that are disabled or not allowed for the user."""
        cmd = interaction.command
        if cmd is None or interaction.guild is None:
            return True
        root = cmd.root_parent.name if getattr(cmd, "root_parent", None) else cmd.name
        problem = interaction.client.check_command(interaction.user, interaction.guild, root)
        if problem:
            await interaction.response.send_message(problem, ephemeral=True)
            return False
        if not isinstance(cmd, HybridAppCommand):
            interaction.client.count_use(interaction.guild.id, root)
        return True

    async def on_error(self, interaction, error):
        """Log unexpected errors of slash commands and tell the user."""
        if isinstance(error, app_commands.CheckFailure):
            return
        log.error("unhandled error in a slash command", exc_info=error)
        where = f"/{interaction.command.qualified_name}" if interaction.command else "interaction"
        interaction.client.report_error(interaction.guild, where, error)
        text = i18n.say(interaction.client, interaction.guild, "Something went wrong.")
        try:
            if interaction.response.is_done():
                await interaction.followup.send(text, ephemeral=True)
            else:
                await interaction.response.send_message(text, ephemeral=True)
        except discord.HTTPException as exc:
            log.warning("response.is_done failed: %s", exc)


class Bot(commands.AutoShardedBot):
    """The Discord bot with storage, checks and the log queue. Uses shards automatically when Discord asks for them."""
    def __init__(self, settings):
        """Create the bot with the needed intents, storage and command checks."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
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
            max_messages=10000,
            allowed_mentions=discord.AllowedMentions.none(),
        )
        self.settings = settings
        self.store = Store(settings.get("data_dir", "data"))
        self.session = None
        self.queue = None
        self.bot_deleted = set()
        self.canonical = {}
        self.started = time.time()
        self._error_sent = {}
        self._state_seen = {}
        self.closing = False
        self.restart_requested = False
        self.status_server = StatusServer(self)
        self.dashboard = Dashboard(self)
        self.add_check(self._global_check)

    def cfg(self, gid):
        """Return the settings of a server."""
        return self.store.cfg(gid)

    def module_on(self, gid, name):
        """True if a module is turned on for a server."""
        return self.cfg(gid)["modules"].get(name, True)

    def prefix_for(self, gid):
        """Return the text command prefix of a server."""
        return self.cfg(gid)["prefix"] or self.settings.get("prefix", "!")

    def can_use(self, member, root):
        """Check the permission rules of a command for a member, falling back to the Discord permission."""
        if member.id == member.guild.owner_id:
            return True
        rule = self.cfg(member.guild.id)["perms"].get(root, {})
        roles = {r.id for r in member.roles}
        if member.id in rule.get("deny_users", []) or roles & set(rule.get("deny_roles", [])):
            return False
        if rule.get("roles") or rule.get("users"):
            return member.id in rule.get("users", []) or bool(roles & set(rule.get("roles", [])))
        perm = FALLBACK_PERMS.get(root)
        return getattr(member.guild_permissions, perm) if perm else True

    def check_command(self, member, guild, root):
        """Return why a command may not be used (disabled, module off, no permission) or None."""
        root = self.canonical.get(root, root)
        g = self.cfg(guild.id)
        if root in g["disabled_commands"]:
            return i18n.say(self, guild, "This command is disabled on this server.")
        mod = COMMAND_MODULES.get(root)
        if mod and not self.module_on(guild.id, mod):
            return i18n.say(self, guild, "The module '{module}' is disabled on this server.", module=mod)
        if not self.can_use(member, root):
            return i18n.say(self, guild, "You are not allowed to use this command.")
        return None

    async def _global_check(self, ctx):
        """Apply the command checks to text commands."""
        if ctx.guild is None:
            return False
        root = (ctx.command.root_parent or ctx.command).name
        problem = self.check_command(ctx.author, ctx.guild, root)
        if problem:
            raise commands.CheckFailure(problem)
        self.count_use(ctx.guild.id, root)
        return True

    def count_use(self, gid, root):
        """Count one use of a command, if usage statistics are on for the server."""
        d = self.cfg(gid)["debug"]
        if d["usage_stats"]:
            root = self.canonical.get(root, root)
            d["usage"][root] = d["usage"].get(root, 0) + 1

    def report_error(self, guild, where, error):
        """Count an unexpected error and post a short report to the error channel of the server, at most one every five seconds."""
        if guild is None:
            return
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
        if isinstance(error, commands.CommandInvokeError):
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
                    path = await asyncio.to_thread(self.store.backup, "auto", int(self.settings.get("db_backup_keep", 7)))
                    self.store.set_meta("last_db_backup", str(int(time.time())))
                    log.info("database backup written: %s", path.name)
            except Exception:
                log.exception("housekeeping failed")
            await asyncio.sleep(30)

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
            await self.load_extension(f"guardbot.cogs.{ext}")
        self.apply_command_names()
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
        await self.status_server.stop()
        await self.dashboard.stop()
        self.store.close()
        if self.session:
            await self.session.close()
        await super().close()

    async def on_ready(self):
        """Log that the bot is online."""
        log.info("online as %s on %d server(s)", self.user, len(self.guilds))
