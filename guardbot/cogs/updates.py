"""Checks GitHub for a newer release, tells the owner of the bot, downloads it and installs it on request or automatically."""

import asyncio
import logging
from pathlib import Path

import discord
from discord.ext import commands

from .. import __repository__, __version__, updater

log = logging.getLogger(__name__)

FIRST_CHECK = 120
MIN_HOURS = 1


class Updates(commands.Cog):
    """Update check, notification, download and installation."""

    def __init__(self, bot):
        """Read the update settings from settings.json."""
        self.bot = bot
        c = bot.settings.get("update", {}) or {}
        self.enabled = bool(c.get("enabled", True))
        self.repo = str(c.get("repo") or __repository__ or "")
        self.hours = max(MIN_HOURS, float(c.get("check_hours", 12) or 12))
        self.auto = bool(c.get("auto_install", False))
        self.require_checksum = bool(c.get("require_checksum", False))
        self.data_dir = Path(bot.settings.get("data_dir", "data"))
        self.app_dir = Path(__file__).resolve().parent.parent.parent
        self.latest = None
        self.staged = None
        self.error = None
        self.last_check = 0
        self.lock = asyncio.Lock()
        self.task = None

    async def cog_load(self):
        """Start the background check when updates are on and a repository is known."""
        if not self.enabled:
            return
        if not updater.valid_repo(self.repo):
            log.info("update check is off: no repository set (update.repo in settings.json)")
            return
        self.task = asyncio.create_task(self.loop())

    async def cog_unload(self):
        """Stop the background check."""
        if self.task:
            self.task.cancel()

    async def loop(self):
        """Check now and then. A failed check is logged and tried again later."""
        await asyncio.sleep(FIRST_CHECK)
        while True:
            try:
                await self.cycle()
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # the loop must survive anything
                log.warning("update check failed: %s", exc)
                self.error = str(exc)
            await asyncio.sleep(self.hours * 3600)

    async def check(self):
        """Ask GitHub for the newest release. Returns the release when it is newer than the running version, else None."""
        async with updater.new_session() as session:
            release = await updater.fetch_latest(session, self.repo)
        self.last_check = int(asyncio.get_running_loop().time())
        self.error = None
        self.latest = release if release and updater.is_newer(release["tag"]) else None
        return self.latest

    async def stage(self, release):
        """Download and verify a release. Returns the archive path."""
        async with updater.new_session() as session:
            self.staged = await updater.stage(session, release, self.data_dir, self.require_checksum)
        return self.staged

    async def cycle(self):
        """One round: check, notify once per version, download, and install if automatic installation is on."""
        release = await self.check()
        if not release:
            return
        first = self.bot.store.get_meta("update_notified") != release["tag"]
        try:
            await self.stage(release)
        except (ValueError, OSError) as exc:
            log.warning("update download failed: %s", exc)
            self.error = str(exc)
            if first:
                await self.tell(f"Version {release['tag']} is available but the download failed: {exc}", release)
                self.bot.store.set_meta("update_notified", release["tag"])
            return
        can = not updater.in_docker()
        if first:
            how = "It is installing now." if self.auto and can else "Install it with /debug update action:install." if can else "This installation runs in a container, so update the image or run git pull and restart."
            await self.tell(f"Version {release['tag']} is available (you run {__version__}) and downloaded. {how}", release)
            self.bot.store.set_meta("update_notified", release["tag"])
        if self.auto and can:
            await self.install()

    async def install(self):
        """Install the staged release and restart. Returns (ok, message)."""
        async with self.lock:
            if updater.in_docker():
                return False, "this installation runs in a container, update the image instead"
            if not self.staged or not Path(self.staged).exists():
                if not self.latest:
                    return False, "there is no newer version"
                await self.stage(self.latest)
            ok, message = await updater.run_install(self.staged, self.app_dir, self.data_dir)
            log.info("update: %s", message)
            if not ok:
                self.error = message
                await self.tell("Update problem: " + message, self.latest)
                return False, message
            await self.tell(message + ". The bot restarts now.", self.latest)
            asyncio.create_task(self.restart())
            return True, message

    async def restart(self):
        """Stop the bot so that main.py starts it again with the new files."""
        await asyncio.sleep(2)
        self.bot.restart_requested = True
        await self.bot.close()

    async def owners(self):
        """The people who own the bot application."""
        try:
            info = await self.bot.application_info()
        except discord.HTTPException:
            return []
        if info.team:
            return [m for m in info.team.members if m.id == info.team.owner_id] or list(info.team.members)[:1]
        return [info.owner]

    async def tell(self, text, release):
        """Write to the log and send the text to the owner of the bot by direct message."""
        log.warning("update: %s", text)
        e = discord.Embed(title="GuardBot update", description=text[:1500], colour=discord.Colour.blurple())
        if release:
            if release.get("notes"):
                e.add_field(name="Release notes", value=release["notes"][:900], inline=False)
            if release.get("page"):
                e.add_field(name="Details", value=release["page"], inline=False)
        for owner in await self.owners():
            try:
                await owner.send(embed=e)
            except discord.HTTPException as exc:
                log.info("update notice could not be sent: %s", exc)

    def status(self):
        """Describe the state of the update check for /debug update."""
        lines = [f"Running: {__version__}", f"Repository: {self.repo or 'not set'}", f"Checks: {'every ' + format(self.hours, 'g') + ' h' if self.task else 'off'}", f"Automatic installation: {'on' if self.auto else 'off'}"]
        if updater.in_docker():
            lines.append("Container: updates are shown but not installed here")
        if self.latest:
            lines.append(f"Newer version: {self.latest['tag']}" + (" (downloaded)" if self.staged and Path(self.staged).exists() else ""))
        if self.error:
            lines.append(f"Last problem: {self.error[:200]}")
        return "\n".join(lines)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Updates(bot))
