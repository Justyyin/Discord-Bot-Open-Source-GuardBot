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
from pathlib import Path

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from . import __version__
from .defaults import COMMAND_MODULES, DEFAULTS, FALLBACK_PERMS
from .utils import CREDIT

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
)


def banner():
    """Return the start-up line with version, author and origin."""
    return f"GuardBot {__version__}  |  {CREDIT}  |  made in Germany"


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
        return True

    async def on_error(self, interaction, error):
        """Log unexpected errors of slash commands and tell the user."""
        if isinstance(error, app_commands.CheckFailure):
            return
        log.error("unhandled error in a slash command", exc_info=error)
        text = "Something went wrong."
        try:
            if interaction.response.is_done():
                await interaction.followup.send(text, ephemeral=True)
            else:
                await interaction.response.send_message(text, ephemeral=True)
        except discord.HTTPException as exc:
            log.warning("response.is_done failed: %s", exc)


class Bot(commands.Bot):
    """The Discord bot with storage, checks and the log queue."""
    def __init__(self, settings):
        """Create the bot with the needed intents, storage and command checks."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.dm_messages = False
        intents.dm_reactions = False
        intents.dm_typing = False
        intents.guild_typing = False
        super().__init__(
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
            return "This command is disabled on this server."
        mod = COMMAND_MODULES.get(root)
        if mod and not self.module_on(guild.id, mod):
            return f"The module '{mod}' is disabled on this server."
        if not self.can_use(member, root):
            return "You are not allowed to use this command."
        return None

    async def _global_check(self, ctx):
        """Apply the command checks to text commands."""
        if ctx.guild is None:
            return False
        root = (ctx.command.root_parent or ctx.command).name
        problem = self.check_command(ctx.author, ctx.guild, root)
        if problem:
            raise commands.CheckFailure(problem)
        return True

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
            text = "Something went wrong."
        elif isinstance(error, commands.CheckFailure):
            text = str(error) or "You are not allowed to use this command."
        elif isinstance(error, (commands.UserInputError, commands.BadUnionArgument)):
            text = f"Invalid input: {error}"
        else:
            text = "Something went wrong."
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
        """Save changed data every ten seconds."""
        while True:
            await asyncio.sleep(10)
            try:
                await self.store.aflush()
            except Exception:
                log.exception("autosave failed")

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
        self._jobs = [asyncio.create_task(self._log_worker()), asyncio.create_task(self._autosave())]
        for ext in EXTENSIONS:
            await self.load_extension(f"guardbot.cogs.{ext}")
        self.apply_command_names()
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
        self.store.close()
        if self.session:
            await self.session.close()
        await super().close()

    async def on_ready(self):
        """Log that the bot is online."""
        log.info("online as %s on %d server(s)", self.user, len(self.guilds))
