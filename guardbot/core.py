# Copyright (c) Justyn
import asyncio
import copy
import copy as _copy
import json
import re
import traceback
from pathlib import Path

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from . import __version__
from .defaults import COMMAND_MODULES, DEFAULTS, FALLBACK_PERMS
from .utils import CREDIT

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
)


def banner():
    return f"GuardBot {__version__}  |  {CREDIT}  |  made in Germany"


def fill(d, default):
    for k, v in default.items():
        if k not in d:
            d[k] = copy.deepcopy(v)
        elif isinstance(v, dict) and v:
            fill(d[k], v)


class Store:
    NAMES = ("config", "users", "cases")

    def __init__(self, directory):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.data = {n: self._read(n) for n in self.NAMES}
        self.dirty = set()
        self._filled = set()

    def _read(self, name):
        p = self.dir / f"{name}.json"
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                p.replace(self.dir / f"{name}.broken.json")
        return {}

    def mark(self, *names):
        self.dirty.update(names or ("config",))

    def flush(self):
        for name in list(self.dirty):
            tmp = self.dir / f"{name}.json.tmp"
            tmp.write_text(json.dumps(self.data[name], ensure_ascii=False, indent=1), encoding="utf-8")
            tmp.replace(self.dir / f"{name}.json")
        self.dirty.clear()

    def cfg(self, gid):
        g = self.data["config"].setdefault(str(gid), {})
        if gid not in self._filled:
            fill(g, DEFAULTS)
            self._filled.add(gid)
        return g

    def users(self, gid):
        return self.data["users"].setdefault(str(gid), {})

    def user(self, gid, uid):
        return self.users(gid).setdefault(str(uid), {"xp": 0, "birthday": None, "bday_last": None})

    def cases(self, gid):
        return self.data["cases"].setdefault(str(gid), [])


def _prefix(bot, message):
    p = bot.prefix_for(message.guild.id) if message.guild else bot.settings.get("prefix", "!")
    return commands.when_mentioned_or(p)(bot, message)


class Tree(app_commands.CommandTree):
    async def interaction_check(self, interaction):
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
        if isinstance(error, app_commands.CheckFailure):
            return
        traceback.print_exception(type(error), error, error.__traceback__)
        text = "Something went wrong."
        try:
            if interaction.response.is_done():
                await interaction.followup.send(text, ephemeral=True)
            else:
                await interaction.response.send_message(text, ephemeral=True)
        except discord.HTTPException:
            pass


class Bot(commands.Bot):
    def __init__(self, settings):
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
        return self.store.cfg(gid)

    def module_on(self, gid, name):
        return self.cfg(gid)["modules"].get(name, True)

    def prefix_for(self, gid):
        return self.cfg(gid)["prefix"] or self.settings.get("prefix", "!")

    def can_use(self, member, root):
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
        if ctx.guild is None:
            return False
        root = (ctx.command.root_parent or ctx.command).name
        problem = self.check_command(ctx.author, ctx.guild, root)
        if problem:
            raise commands.CheckFailure(problem)
        return True

    async def get_context(self, message, *, cls=commands.Context):
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
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CommandInvokeError):
            traceback.print_exception(type(error), error, error.__traceback__)
            text = "Something went wrong."
        elif isinstance(error, commands.CheckFailure):
            text = str(error) or "You are not allowed to use this command."
        elif isinstance(error, (commands.UserInputError, commands.BadUnionArgument)):
            text = f"Invalid input: {error}"
        else:
            text = "Something went wrong."
        try:
            await ctx.send(text, ephemeral=True)
        except discord.HTTPException:
            pass

    def log(self, guild, category, embed, files=None):
        lc = self.cfg(guild.id)["log"]
        ch = lc.get(category) or lc.get("main")
        if ch and self.queue is not None and self.queue.qsize() < 2000:
            self.queue.put_nowait((ch, embed, files or []))

    def is_log_channel(self, guild, channel_id):
        return channel_id in {v for v in self.cfg(guild.id)["log"].values() if v}

    async def _log_worker(self):
        while True:
            ch_id, embed, files = await self.queue.get()
            ch = self.get_channel(ch_id)
            if ch:
                try:
                    await ch.send(embed=embed, files=files)
                except discord.HTTPException:
                    pass
            await asyncio.sleep(0.5)

    async def _autosave(self):
        while True:
            await asyncio.sleep(10)
            self.store.flush()

    def apply_command_names(self):
        for old, new in self.settings.get("command_names", {}).items():
            new = str(new).lower()
            if not re.fullmatch(r"[\w-]{1,32}", new):
                print(f"command_names: '{new}' is not a valid name, skipped")
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
                    print(f"command_names: unknown command '{old}', skipped")
                    continue
                self.tree.remove_command(old)
                app.name = new
                self.tree.add_command(app)
            self.canonical[new] = old

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        self.queue = asyncio.Queue()
        self._jobs = [asyncio.create_task(self._log_worker()), asyncio.create_task(self._autosave())]
        for ext in EXTENSIONS:
            await self.load_extension(f"guardbot.cogs.{ext}")
        self.apply_command_names()
        await self.tree.sync()

    async def close(self):
        self.store.mark("config", "users", "cases")
        self.store.flush()
        if self.session:
            await self.session.close()
        await super().close()

    async def on_ready(self):
        print(f"online as {self.user} on {len(self.guilds)} server(s)")
