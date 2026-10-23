"""Guard Music: a second bot account that only plays music.

It runs in the same process as GuardBot and uses the same settings, storage and dashboard, but has its own token, name and
voice connection. GuardBot itself then has no music commands. A second account keeps moderation and music apart: the music
bot can sit in a voice channel around the clock, and if a music service ever objects, the moderation bot is not affected.
"""

import asyncio
import hashlib
import json
import logging
import time
from collections import deque
from typing import Any, Optional

import aiohttp
import discord
from discord.ext import commands

from . import i18n
from .checks import Checks
from .workers import Busy

log = logging.getLogger(__name__)

# View channels, send messages, embed links, read history, connect, speak
INVITE_PERMISSIONS = 1024 + 2048 + 16384 + 65536 + 1048576 + 2097152


def settings_of(settings: dict) -> dict:
    """The music_bot part of settings.json with defaults."""
    conf = {"enabled": False, "token_env": "MUSIC_TOKEN", "message_content": True, "status": "/play"}
    conf.update(settings.get("music_bot") or {})
    return conf


def _prefix(bot: Any, message: Any) -> Any:
    """The prefix of the server, the same as GuardBot uses."""
    p = bot.prefix_for(message.guild.id) if message.guild else bot.settings.get("prefix", "!")
    return commands.when_mentioned_or(p)(bot, message)


class MusicBot(Checks, commands.Bot):
    """The second bot. Settings, storage, workers and errors go through the main bot."""

    def __init__(self, main: Any) -> None:
        """Create the bot with only the intents that music needs."""
        conf = settings_of(main.settings)
        intents = discord.Intents.none()
        intents.guilds = True
        intents.voice_states = True
        intents.guild_messages = True
        intents.message_content = bool(conf["message_content"])
        super().__init__(
            command_prefix=_prefix, intents=intents, help_command=None, max_messages=None, chunk_guilds_at_startup=False,
            allowed_mentions=discord.AllowedMentions.none(), activity=discord.Activity(type=discord.ActivityType.listening, name=str(conf["status"])[:100]),
        )
        self.main = main
        self.settings = main.settings
        self.store = main.store
        self.work = main.work
        self.metrics = main.metrics
        self.session: Optional[aiohttp.ClientSession] = None
        self.canonical: dict[str, str] = {}
        self.actors: dict[int, deque] = {}
        self._state_seen: dict[str, str] = {}
        self.closing = False
        self.add_check(self._global_check)

    def cfg(self, gid: Any) -> dict:
        """The settings of a server, shared with GuardBot."""
        return self.main.cfg(gid)

    def module_on(self, gid: Any, name: str) -> bool:
        """True if a module is on for a server."""
        return self.main.module_on(gid, name)

    def prefix_for(self, gid: Any) -> str:
        """The text command prefix of a server."""
        return self.main.prefix_for(gid)

    def report_error(self, guild: Any, where: str, error: BaseException) -> None:
        """Errors are reported by GuardBot in the error channel of the server."""
        self.main.report_error(guild, f"Guard Music: {where}", error)

    def invite_url(self) -> Optional[str]:
        """The link that adds Guard Music to a server, once the bot is logged in."""
        if not self.application_id:
            return None
        return f"https://discord.com/oauth2/authorize?client_id={self.application_id}&scope=bot+applications.commands&permissions={INVITE_PERMISSIONS}"

    async def setup_hook(self) -> None:
        """Load the music commands and sync them when they changed."""
        self.session = aiohttp.ClientSession()
        await self.load_extension("guardbot.cogs.community.music")
        self._jobs = [asyncio.create_task(self._autosave())]
        payload = json.dumps([c.to_dict(self.tree) for c in self.tree.get_commands()], sort_keys=True, default=str)
        digest = hashlib.sha256((payload + str(self.application_id)).encode()).hexdigest()
        if self.settings.get("force_sync") or self.store.get_meta("music_sync_hash") != digest:
            await self.tree.sync()
            self.store.set_meta("music_sync_hash", digest)
            log.info("Guard Music: slash commands synced")

    async def _autosave(self) -> None:
        """Keep the queues saved so the music continues after a restart."""
        while True:
            await asyncio.sleep(10)
            try:
                if not self.closing:
                    self.save_states()
            except Exception:
                log.exception("Guard Music: saving the state failed")

    def save_states(self) -> None:
        """Save the runtime state of the music cog when it changed."""
        for name, cog in self.cogs.items():
            export = getattr(cog, "export_state", None)
            if export is None:
                continue
            state = export()
            digest = json.dumps(state, sort_keys=True, default=str)
            if self._state_seen.get(name) != digest:
                self._state_seen[name] = digest
                self.store.set_state(name, state or None)

    async def on_ready(self) -> None:
        """Log that Guard Music is online."""
        log.info("Guard Music online as %s on %d server(s)", self.user, len(self.guilds))

    async def on_command_error(self, ctx: Any, error: Exception) -> None:
        """Answer failed text and hybrid commands."""
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(getattr(error, "original", None), Busy):
            text = i18n.say(self, ctx.guild, "The bot is busy with this kind of work. Try again in a moment.")
        elif isinstance(error, commands.CheckFailure):
            text = str(error) or i18n.say(self, ctx.guild, "You are not allowed to use this command.")
        elif isinstance(error, (commands.UserInputError, commands.BadUnionArgument)):
            text = f"Invalid input: {error}"
        else:
            log.error("Guard Music: error in command %s", ctx.command, exc_info=error)
            self.report_error(ctx.guild, f"{ctx.prefix}{ctx.command.qualified_name if ctx.command else '?'}", error)
            text = i18n.say(self, ctx.guild, "Something went wrong.")
        try:
            await ctx.send(text, ephemeral=True)
        except discord.HTTPException as exc:
            log.warning("Guard Music: ctx.send failed: %s", exc)

    async def close(self) -> None:
        """Save the queues and close the connection. Storage belongs to GuardBot and stays open."""
        if self.closing:
            return
        self.closing = True
        try:
            self.save_states()
        except Exception:
            log.exception("Guard Music: saving the state failed")
        for job in getattr(self, "_jobs", []):
            job.cancel()
        if self.session:
            await self.session.close()
        await super().close()


async def run(bot: MusicBot, token: str) -> None:
    """Run Guard Music until it is closed. A wrong token is logged and does not stop GuardBot."""
    started = time.time()
    try:
        async with bot:
            await bot.start(token)
    except discord.LoginFailure:
        log.error("Guard Music could not log in: the token in %s is not valid", settings_of(bot.settings)["token_env"])
    except discord.PrivilegedIntentsRequired:
        log.error("Guard Music needs the Message Content Intent in the Developer Portal, or set music_bot.message_content to false in settings.json")
    except (OSError, aiohttp.ClientError) as exc:
        log.error("Guard Music stopped after %d s: %s", int(time.time() - started), exc)
