"""The voice player of the music cog: queue, playback and the idle timer of one server."""

import asyncio
import logging
import time

import discord

from . import musiclib as ml
from .utils import emb, trim

log = logging.getLogger(__name__)


class Player:
    """The voice connection, queue and playback state of one server."""

    def __init__(self, cog, guild):
        """Create an idle player."""
        self.cog, self.guild = cog, guild
        self.queue = ml.Queue()
        self.vc = None
        self.text_channel = None
        self.volume = cog.conf(guild.id)["volume"]
        self.gen = 0
        self.since = 0.0
        self.offset = 0.0
        self.paused_at = None
        self.failures = 0
        self.idle_task = None

    @property
    def conf(self):
        """The music settings of this server."""
        return self.cog.conf(self.guild.id)

    @property
    def playing(self):
        """True while a track is playing or paused."""
        return bool(self.vc and self.queue.current and (self.vc.is_playing() or self.vc.is_paused()))

    def position(self):
        """Seconds played of the current track."""
        if not self.queue.current:
            return 0.0
        now = self.paused_at if self.paused_at is not None else time.monotonic()
        return self.offset + now - self.since

    def cancel_idle(self):
        """Stop the timer that leaves the channel."""
        if self.idle_task:
            self.idle_task.cancel()
            self.idle_task = None

    def schedule_idle(self, seconds=None):
        """Leave the voice channel after some time without playback or listeners. Never in 24/7 mode."""
        self.cancel_idle()
        if self.conf.get("stay"):
            return
        seconds = self.conf["idle_leave"] if seconds is None else seconds
        if seconds > 0:
            self.idle_task = asyncio.create_task(self._idle(seconds))

    async def _idle(self, seconds):
        """Wait, then disconnect if nothing is playing or nobody listens."""
        await asyncio.sleep(seconds)
        listeners = [m for m in self.vc.channel.members if not m.bot] if self.vc and self.vc.channel else []
        if not self.playing or not listeners:
            await self.cog.destroy(self.guild.id)

    async def say(self, **kwargs):
        """Post a message in the text channel of the last command, if announcements are on."""
        channel = self.guild.get_channel(self.text_channel) if self.text_channel else None
        if channel and self.conf["announce"]:
            try:
                await channel.send(allowed_mentions=discord.AllowedMentions.none(), **kwargs)
            except discord.HTTPException as exc:
                log.warning("music announcement failed: %s", exc)

    async def next(self, skipped=False):
        """Move to the next track and start it, or go idle when the queue is empty."""
        track = self.queue.advance(skipped)
        if track is None and await self.cog.autoplay(self):
            track = self.queue.advance(False)
        if track is None:
            self.offset = 0.0
            self.schedule_idle()
            return
        self.cancel_idle()
        await self.start(track, 0)

    async def start(self, track, seek):
        """Open the audio of a track and play it from a position."""
        try:
            source = await self.cog.open_source(track, seek, self.guild.id)
        except (RuntimeError, OSError, ValueError, discord.DiscordException) as exc:
            log.warning("could not start %s: %s", track.title, exc)
            self.failures += 1
            await self.say(embed=emb("Could not play a track", f"**{trim(track.title, 100)}**: {trim(str(exc), 300)}", discord.Color.red()))
            if self.failures >= 3:
                self.queue.clear()
                self.queue.current = None
                self.failures = 0
                return self.schedule_idle()
            return await self.next(skipped=True)
        self.failures = 0
        self.gen += 1
        gen = self.gen
        source = discord.PCMVolumeTransformer(source, volume=self.volume / 100)
        kbps = max(16, min(510, (self.vc.channel.bitrate or 128000) // 1000))
        self.vc.play(source, after=lambda err: asyncio.run_coroutine_threadsafe(self.ended(gen, err), self.cog.bot.loop), bitrate=kbps, signal_type="music")
        self.offset, self.since, self.paused_at = float(seek), time.monotonic(), None
        if seek == 0:
            await self.say(embed=self.cog.track_embed(self, "Now playing"))

    async def ended(self, gen, error):
        """Called when the audio of a track ends. Ignored if the track was stopped or skipped on purpose."""
        if gen != self.gen:
            return
        if error:
            log.warning("playback error: %s", error)
        await self.next()

    def halt(self):
        """Stop the current audio without starting the next track."""
        self.gen += 1
        if self.vc and (self.vc.is_playing() or self.vc.is_paused()):
            self.vc.stop()
