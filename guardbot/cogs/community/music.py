"""Music: plays links and files of the local library in voice channels and downloads into a structured library."""

import asyncio
import logging
import shlex
import shutil
import time
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Literal, Optional
from urllib.parse import urlparse

import discord
from discord import app_commands
from discord.ext import commands

from ...cog import BaseCog
from ... import i18n, musiclib as ml
from ...linkcheck import public_host, url_problem
from ...utils import emb, trim

from ...musicdl import FORMATS, GENERIC, INDEX_TTL, LOSSLESS_CODECS, NET_INPUT, PAGE, RESUME_WITHIN, clean_artist, download_job, extract, file_into_library, yt_dlp
from ...musicplayer import Player

log = logging.getLogger(__name__)


class Music(BaseCog):
    """Voice playback from links and from the local library."""
    section = "music"

    def __init__(self, bot):
        """Prepare the player registry and the library index."""
        self.bot = bot
        self.players = {}
        self.entries = []
        self.cache = {}
        self.indexed = 0.0
        self.index_lock = asyncio.Lock()
        self.restored = False
        GENERIC["on"] = bool(bot.settings.get("music_generic", True))

    def export_state(self):
        """Queues of all servers, so playback can continue after a restart."""
        out = {}
        for gid, p in self.players.items():
            if p.vc and p.vc.channel and (p.queue.current or p.queue.items):
                out[str(gid)] = {
                    "channel": p.vc.channel.id, "text": p.text_channel, "volume": p.volume, "loop": p.queue.loop,
                    "position": int(p.position()), "saved": int(time.time()),
                    "current": asdict(p.queue.current) if p.queue.current else None, "items": [asdict(t) for t in p.queue.items],
                }
        return out

    @commands.Cog.listener()
    async def on_ready(self):
        """After a restart, rejoin and continue where the music stopped, if listeners are still in the channel."""
        if self.restored:
            return
        self.restored = True
        for gid, data in (self.bot.store.state("Music") or {}).items():
            try:
                await self.restore(int(gid), data)
            except (discord.DiscordException, asyncio.TimeoutError, KeyError, TypeError, ValueError) as exc:
                log.warning("could not resume the music of %s: %s", gid, exc)

    async def restore(self, gid, data):
        """Rebuild the player of one server from saved state."""
        guild = self.bot.get_guild(gid)
        channel = guild.get_channel(data["channel"]) if guild else None
        if channel is None or time.time() - data["saved"] > RESUME_WITHIN or not self.bot.module_on(gid, "music") or self.not_ready():
            return
        if not [m for m in channel.members if not m.bot]:
            return
        player = Player(self, guild)
        player.text_channel, player.volume = data.get("text"), int(data["volume"])
        player.queue.loop = data["loop"] if data["loop"] in ("off", "track", "queue") else "off"
        for t in data["items"]:
            player.queue.add(ml.Track(**t))
        player.vc = await channel.connect(self_deaf=True)
        self.players[gid] = player
        if data["current"]:
            player.queue.current = ml.Track(**data["current"])
            await player.start(player.queue.current, data["position"])
        else:
            await player.next()
        log.info("music resumed on %s", gid)

    async def cog_unload(self):
        """Disconnect everywhere."""
        for gid in list(self.players):
            await self.destroy(gid)

    @property
    def root(self):
        """The folder of the music library."""
        return Path(self.bot.settings.get("music_dir", "music"))

    @property
    def ffmpeg(self):
        """The ffmpeg program, from settings.json or the system path."""
        return self.bot.settings.get("ffmpeg", "ffmpeg")

    async def index(self, force=False):
        """Return the library entries, scanning the folder again when the data is older than two minutes."""
        async with self.index_lock:
            if force or time.monotonic() - self.indexed > INDEX_TTL:
                self.root.mkdir(parents=True, exist_ok=True)
                self.entries = await self.bot.work.run("music", ml.scan, self.root, self.cache)
                self.indexed = time.monotonic()
            return self.entries

    async def destroy(self, gid):
        """Stop playback, leave the channel and forget the player of a server."""
        player = self.players.pop(gid, None)
        if player is None:
            return
        player.cancel_idle()
        player.queue.clear()
        player.queue.current = None
        player.halt()
        if player.vc:
            try:
                await player.vc.disconnect(force=True)
            except discord.DiscordException as exc:
                log.warning("disconnect failed: %s", exc)

    def is_dj(self, member):
        """True if the member may control playback: no DJ role set, the role, or Manage Server."""
        role = self.conf(member.guild.id)["dj_role"]
        return not role or member.guild_permissions.manage_guild or any(r.id == role for r in member.roles)

    def track_embed(self, player, title):
        """Embed for the current track."""
        t = player.queue.current
        e = emb(title, f"**{trim(t.title, 200)}**" + (f"\n{trim(t.artist, 100)}" if t.artist else ""), discord.Color.blurple())
        e.add_field(name="Length", value=ml.fmt_time(t.length) if t.length else "stream")
        e.add_field(name="Quality", value=t.detail or ("lossless" if t.lossless else "stream"))
        e.add_field(name="Requested by", value=f"<@{t.requester}>")
        if player.queue.loop != "off":
            e.add_field(name="Loop", value=player.queue.loop)
        return e

    async def open_source(self, track, seek, gid):
        """Create the ffmpeg audio source for a track."""
        before = f"-ss {int(seek)} " if seek else ""
        if track.kind == "local":
            path = ml.resolve(self.root, track.ref)
            if path is None:
                raise RuntimeError("the file is no longer in the library")
            return discord.FFmpegPCMAudio(str(path), executable=self.ffmpeg, before_options=before + "-protocol_whitelist file", options="-vn")
        if yt_dlp is None:
            raise RuntimeError("yt-dlp is not installed")
        conf = self.conf(gid)
        problem = url_problem(track.ref, conf["allowed_hosts"], conf["blocked_hosts"])
        if problem:
            raise RuntimeError(problem)
        info = await self.bot.work.run("music", extract, track.ref, self.ffmpeg)
        stream = info.get("url") or next((f["url"] for f in reversed(info.get("formats") or []) if f.get("url") and f.get("vcodec") in (None, "none")), None)
        if not stream:
            raise RuntimeError("no audio stream found")
        host = urlparse(stream).hostname or ""
        problem = url_problem(stream)
        if problem or not await public_host(host):
            raise RuntimeError("the audio stream is on a private address")
        track.detail = self.web_quality(info)
        agent = (info.get("http_headers") or {}).get("User-Agent")
        extra = f"-user_agent {shlex.quote(agent)} " if agent else ""
        return discord.FFmpegPCMAudio(stream, executable=self.ffmpeg, before_options=f"{NET_INPUT} {extra}{before}".strip(), options="-vn")

    @staticmethod
    def web_quality(info):
        """Describe the codec and bitrate of a stream."""
        codec = (info.get("acodec") or "").split(".")[0] or info.get("ext") or "audio"
        kbps = f" {int(info['abr'])} kbps" if info.get("abr") else ""
        return f"{codec.upper()}{kbps} ({'lossless' if codec in LOSSLESS_CODECS else 'lossy stream'})"

    def track_from_info(self, info, user_id):
        """Build a queue entry from yt-dlp metadata. Returns None if the entry is unusable."""
        ref = info.get("webpage_url") or info.get("original_url") or info.get("url")
        if not ref or not ref.startswith(("http://", "https://")):
            return None
        codec = (info.get("acodec") or "").split(".")[0]
        return ml.Track(
            title=info.get("track") or info.get("title") or "Unknown title",
            artist=clean_artist(info.get("artist") or info.get("uploader") or info.get("channel") or ""),
            kind="web", ref=ref, length=float(info.get("duration") or 0), requester=user_id, lossless=codec in LOSSLESS_CODECS,
        )

    def track_from_entry(self, entry, user_id):
        """Build a queue entry from a library entry."""
        return ml.Track(title=entry["title"], artist=entry["artist"], kind="local", ref=entry["path"], length=entry["length"], requester=user_id, lossless=entry["lossless"], detail=ml.quality(entry))

    async def find_tracks(self, ctx, query, local_only=False):
        """Turn a link or a search text into tracks. Returns (tracks, error)."""
        conf = self.conf(ctx.guild.id)
        query = query.strip()
        if query.startswith(("http://", "https://")) and not local_only:
            if not conf["allow_links"]:
                return [], "Playing links is turned off on this server."
            if yt_dlp is None:
                return [], "Link playback needs yt-dlp. Install it with: pip install yt-dlp"
            problem = url_problem(query, conf["allowed_hosts"], conf["blocked_hosts"])
            if problem or not await public_host(urlparse(query).hostname or ""):
                return [], f"I cannot open this link: {problem or 'it does not resolve to a public address'}."
            return await self.from_web(ctx, query, conf, playlist=conf["allow_playlists"])
        if conf["library"]:
            hits = ml.search(await self.index(), query, 1)
            if hits:
                return [self.track_from_entry(hits[0], ctx.author.id)], None
        if local_only or not conf["allow_search"] or yt_dlp is None:
            return [], "Nothing found in the library." if local_only or yt_dlp is None else "Searching the web is turned off on this server."
        return await self.from_web(ctx, f"ytsearch1:{query}", conf, playlist=False)

    async def from_web(self, ctx, target, conf, playlist):
        """Read a link or search result with yt-dlp and build the tracks."""
        try:
            info = await self.bot.work.run("music", extract, target, self.ffmpeg, playlist, conf["playlist_limit"], target.startswith("ytsearch"))
        except yt_dlp.utils.DownloadError as exc:
            log.info("yt-dlp could not read %s: %s", urlparse(target).hostname, exc)
            return [], f"I could not read that: {trim(str(exc).replace('ERROR: ', ''), 300)}"
        if info is None:
            return [], "Nothing found."
        entries = info.get("entries")
        items = [e for e in entries if e] if entries is not None else [info]
        tracks = []
        for e in items[: conf["playlist_limit"]]:
            t = self.track_from_info(e, ctx.author.id)
            if t is None or url_problem(t.ref, conf["allowed_hosts"], conf["blocked_hosts"]):
                continue
            if t.length and t.length > conf["max_minutes"] * 60:
                continue
            tracks.append(t)
        if not tracks:
            return [], f"No playable result (tracks longer than {conf['max_minutes']} minutes are skipped)."
        return tracks, None

    def not_ready(self):
        """Return why voice playback cannot work on this machine, or None."""
        if not discord.voice_client.has_nacl:
            return "Voice needs PyNaCl. Install it with: pip install PyNaCl"
        if not discord.opus.is_loaded():
            return "The Opus library is missing. On Linux install libopus0, on Windows and macOS it comes with discord.py."
        if shutil.which(self.ffmpeg) is None:
            return "ffmpeg was not found. Install it or set the path in settings.json (ffmpeg)."
        return None

    async def join(self, ctx):
        """Return a connected player in the voice channel of the author, or None after answering."""
        problem = self.not_ready()
        if problem:
            await ctx.send(problem, ephemeral=True)
            return None
        voice = ctx.author.voice
        if not voice or not voice.channel:
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Join a voice channel first."), ephemeral=True)
            return None
        channel = voice.channel
        perms = channel.permissions_for(ctx.guild.me)
        if not (perms.connect and perms.speak):
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "I need the Connect and Speak permissions in your voice channel."), ephemeral=True)
            return None
        player = self.players.get(ctx.guild.id)
        if player and player.vc and player.vc.is_connected() and player.vc.channel != channel:
            others = [m for m in player.vc.channel.members if not m.bot]
            if others and not self.is_dj(ctx.author):
                await ctx.send(i18n.say(ctx.bot, ctx.guild, "I am already playing in {mention}.", mention=player.vc.channel.mention), ephemeral=True)
                return None
            await player.vc.move_to(channel)
        if player is None:
            player = self.players[ctx.guild.id] = Player(self, ctx.guild)
        if not player.vc or not player.vc.is_connected():
            try:
                player.vc = await channel.connect(self_deaf=True)
            except (discord.DiscordException, asyncio.TimeoutError) as exc:
                self.players.pop(ctx.guild.id, None)
                log.warning("voice connect failed: %s", exc)
                await ctx.send(i18n.say(ctx.bot, ctx.guild, "I could not join the voice channel: {exc}", exc=exc), ephemeral=True)
                return None
        player.text_channel = ctx.channel.id
        return player

    async def control(self, ctx):
        """Return the player for a control command if the author is allowed and listening, else answer and return None."""
        player = self.players.get(ctx.guild.id)
        if player is None or not player.vc:
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Nothing is playing."), ephemeral=True)
            return None
        if not ctx.author.voice or ctx.author.voice.channel != player.vc.channel:
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Join my voice channel to control the music."), ephemeral=True)
            return None
        if not self.is_dj(ctx.author):
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Only members with the DJ role can do this."), ephemeral=True)
            return None
        return player

    async def enqueue(self, ctx, tracks):
        """Add tracks to the queue within the limits and start playing if idle. Returns how many were added."""
        player = await self.join(ctx)
        if player is None:
            return 0
        conf = player.conf
        room = min(conf["max_queue"] - len(player.queue), conf["per_user"] - player.queue.count_by(ctx.author.id))
        tracks = tracks[: max(room, 0)]
        if not tracks:
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "The queue is full for you or for the server."), ephemeral=True)
            return 0
        for t in tracks:
            player.queue.add(t)
        if not player.playing:
            await player.next()
        return len(tracks)

    @commands.hybrid_command(name="play", description="Play a link, or search the library and the web")
    @app_commands.describe(query="Link, or words from the artist or title")
    @commands.guild_only()
    async def play(self, ctx, *, query: str):
        """Play a link, or search the library and the web."""
        await ctx.defer()
        tracks, error = await self.find_tracks(ctx, query)
        if error:
            return await ctx.send(error, ephemeral=True)
        waiting = len(self.players[ctx.guild.id].queue) if ctx.guild.id in self.players else 0
        added = await self.enqueue(ctx, tracks)
        if added:
            first = tracks[0]
            text = f"Added **{trim(first.title, 100)}**" + (f" and {added - 1} more" if added > 1 else "")
            await ctx.send(text + (f" at position {waiting + 1}." if waiting else "."))

    @play.autocomplete("query")
    async def play_complete(self, it: discord.Interaction, current: str):
        """Suggest tracks from the library while typing."""
        if not current or current.startswith("http") or not it.guild_id or not self.conf(it.guild_id)["library"]:
            return []
        return [app_commands.Choice(name=f"{e['artist']} - {e['title']}"[:100], value=f"{e['artist']} {e['title']}"[:100]) for e in ml.search(self.entries or await self.index(), current, 25)]

    @commands.hybrid_group(name="music", fallback="queue", description="Show the queue")
    @app_commands.describe(page="Page")
    @commands.guild_only()
    async def music(self, ctx, page: int = 1):
        """Show the queue."""
        player = self.players.get(ctx.guild.id)
        if not player or not player.queue.current:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "The queue is empty."), ephemeral=True)
        q = player.queue
        pages = max(1, -(-len(q) // PAGE))
        page = min(max(page, 1), pages)
        lines = [f"{i}. {trim(t.title, 70)} ({ml.fmt_time(t.length) if t.length else 'stream'})" for i, t in enumerate(list(q.items)[(page - 1) * PAGE : page * PAGE], (page - 1) * PAGE + 1)]
        e = emb("Queue", f"Now: **{trim(q.current.title, 100)}**\n\n" + ("\n".join(lines) or "No more tracks."))
        e.set_footer(text=f"Page {page}/{pages} | {len(q)} waiting, {ml.fmt_time(q.total_length())} | loop {q.loop}")
        await ctx.send(embed=e, ephemeral=True)

    @music.command(name="nowplaying", description="Show the current track")
    async def nowplaying(self, ctx):
        """Show the current track."""
        player = self.players.get(ctx.guild.id)
        if not player or not player.queue.current:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Nothing is playing."), ephemeral=True)
        t = player.queue.current
        e = self.track_embed(player, "Now playing")
        e.add_field(name="Position", value=f"{ml.fmt_time(player.position())} {ml.bar(player.position(), t.length)} {ml.fmt_time(t.length) if t.length else ''}", inline=False)
        await ctx.send(embed=e, ephemeral=True)

    @music.command(name="join", description="Make the bot join your voice channel")
    async def join_cmd(self, ctx):
        """Make the bot join your voice channel."""
        player = await self.join(ctx)
        if player:
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Joined {mention}.", mention=player.vc.channel.mention), ephemeral=True)

    @music.command(name="leave", description="Stop the music and leave the voice channel")
    async def leave(self, ctx):
        """Stop the music and leave the voice channel."""
        if await self.control(ctx):
            await self.destroy(ctx.guild.id)
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Left the voice channel."), ephemeral=True)

    @music.command(name="skip", description="Skip the current track")
    async def skip(self, ctx):
        """Skip the current track."""
        player = await self.control(ctx)
        if player:
            player.halt()
            await player.next(skipped=True)
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Skipped."), ephemeral=True)

    @music.command(name="stop", description="Stop playing and clear the queue")
    async def stop(self, ctx):
        """Stop playing and clear the queue."""
        player = await self.control(ctx)
        if player:
            player.queue.clear()
            player.queue.current = None
            player.halt()
            player.schedule_idle()
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Stopped."), ephemeral=True)

    @music.command(name="pause", description="Pause the music")
    async def pause(self, ctx):
        """Pause the music."""
        player = await self.control(ctx)
        if player and player.vc.is_playing():
            player.vc.pause()
            player.paused_at = time.monotonic()
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Paused."), ephemeral=True)

    @music.command(name="resume", description="Continue the music")
    async def resume(self, ctx):
        """Continue the music."""
        player = await self.control(ctx)
        if player and player.vc.is_paused():
            player.vc.resume()
            player.since += time.monotonic() - player.paused_at
            player.paused_at = None
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Continued."), ephemeral=True)

    @music.command(name="volume", description="Set the volume (1 to 150 percent)")
    async def volume(self, ctx, percent: app_commands.Range[int, 1, 150]):
        """Set the volume (1 to 150 percent)."""
        player = await self.control(ctx)
        if player:
            player.volume = percent
            if player.vc.source:
                player.vc.source.volume = percent / 100
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Volume: {percent}%", percent=percent), ephemeral=True)

    @music.command(name="loop", description="Repeat the track or the queue")
    async def loop(self, ctx, mode: Literal["off", "track", "queue"]):
        """Repeat the track or the queue."""
        player = await self.control(ctx)
        if player:
            player.queue.loop = mode
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Loop: {mode}", mode=mode), ephemeral=True)

    @music.command(name="shuffle", description="Mix the waiting tracks")
    async def shuffle(self, ctx):
        """Mix the waiting tracks."""
        player = await self.control(ctx)
        if player:
            player.queue.shuffle()
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Mixed."), ephemeral=True)

    @music.command(name="remove", description="Remove a waiting track by its number")
    async def remove(self, ctx, number: int):
        """Remove a waiting track by its number."""
        player = await self.control(ctx)
        if player:
            t = player.queue.remove(number)
            await ctx.send(f"Removed **{trim(t.title, 100)}**." if t else "No track with this number.", ephemeral=True)

    @music.command(name="clear", description="Remove all waiting tracks")
    async def clear(self, ctx):
        """Remove all waiting tracks."""
        player = await self.control(ctx)
        if player:
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Removed {clear} tracks.", clear=player.queue.clear()), ephemeral=True)

    @music.command(name="seek", description="Jump to a position, for example 1:30")
    async def seek(self, ctx, position: str):
        """Jump to a position, for example 1:30."""
        player = await self.control(ctx)
        if not player:
            return
        secs = ml.parse_time(position)
        t = player.queue.current
        if secs is None or not t or (t.length and secs >= t.length):
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Use a time inside the track, like 90 or 1:30."), ephemeral=True)
        player.halt()
        await player.start(t, secs)
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Jumped to {fmt_time}.", fmt_time=ml.fmt_time(secs)), ephemeral=True)

    @music.group(name="library", description="The music folder on the bot's computer")
    async def library(self, ctx):
        """Commands for the music library."""
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Use search, list, play, scan, info or download."), ephemeral=True)

    @library.command(name="search", description="Search the library")
    async def lib_search(self, ctx, *, query: str):
        """Search the library."""
        hits = ml.search(await self.index(), query, 15)
        lines = [f"{trim(e['artist'], 40)} - {trim(e['title'], 60)} | {ml.quality(e)}" for e in hits]
        await ctx.send(embed=emb("Library", "\n".join(lines) or "Nothing found."), ephemeral=True)

    @library.command(name="list", description="List artists, or the albums and tracks of one artist")
    async def lib_list(self, ctx, *, artist: Optional[str] = None):
        """List artists, or the albums and tracks of one artist."""
        entries = await self.index()
        if not artist:
            counts = {}
            for e in entries:
                counts[e["artist"] or "Unknown"] = counts.get(e["artist"] or "Unknown", 0) + 1
            lines = [f"{a} ({n})" for a, n in sorted(counts.items(), key=lambda kv: kv[0].lower())]
            return await ctx.send(embed=emb(f"{len(lines)} artists", trim("\n".join(lines) or "The library is empty.", 3800)), ephemeral=True)
        mine = [e for e in entries if e["artist"].lower() == artist.lower()]
        if not mine:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "No artist with this name."), ephemeral=True)
        lines, last = [], None
        for e in mine:
            if e["album"] != last:
                lines.append(f"**{e['album'] or 'Singles'}**")
                last = e["album"]
            lines.append(f"{e['track']:02d} {e['title']}" if e["track"] else f"- {e['title']}")
        await ctx.send(embed=emb(mine[0]["artist"], trim("\n".join(lines), 3800)), ephemeral=True)

    @library.command(name="play", description="Play something from the library")
    async def lib_play(self, ctx, *, query: str):
        """Play something from the library."""
        await ctx.defer()
        tracks, error = await self.find_tracks(ctx, query, local_only=True)
        if error:
            return await ctx.send(error, ephemeral=True)
        if await self.enqueue(ctx, tracks):
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Added **{trim}**.", trim=trim(tracks[0].title, 100)))

    @library.command(name="scan", description="Read the music folder again")
    async def lib_scan(self, ctx):
        """Read the music folder again."""
        await ctx.defer(ephemeral=True)
        entries = await self.index(force=True)
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "{count} tracks found in `{root}`.", count=len(entries), root=self.root), ephemeral=True)

    @library.command(name="info", description="Show how big the library is")
    async def lib_info(self, ctx):
        """Show how big the library is."""
        entries = await self.index()
        size = await self.bot.work.run("music", ml.total_bytes, self.root)
        lossless = sum(1 for e in entries if e["lossless"])
        artists = len({e["artist"] for e in entries})
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "{count} tracks, {artists} artists, {lossless} lossless, {value} GB in `{root}`.", count=len(entries), artists=artists, lossless=lossless, value=format(size / 1024 ** 3, ".2f"), root=self.root), ephemeral=True)

    @library.command(name="download", description="Save the audio of a link in the library (Artist/Album/Track)")
    @app_commands.describe(url="Link to a track or playlist", format="best keeps the original quality, the others convert")
    async def lib_download(self, ctx, url: str, format: Optional[Literal[FORMATS]] = None):
        """Save the audio of a link in the library (Artist/Album/Track)."""
        conf = self.conf(ctx.guild.id)
        if not conf["allow_download"]:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Downloads are turned off on this server. An admin can allow them with /music settings."), ephemeral=True)
        if not self.is_dj(ctx.author) or (not conf["dj_role"] and not ctx.author.guild_permissions.manage_guild):
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Only members with the DJ role or the Manage Server permission can download."), ephemeral=True)
        if yt_dlp is None:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Downloads need yt-dlp. Install it with: pip install yt-dlp"), ephemeral=True)
        problem = url_problem(url, conf["allowed_hosts"], conf["blocked_hosts"])
        if problem or not await public_host(urlparse(url).hostname or ""):
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "I cannot open this link: {value}.", value=problem or 'it does not resolve to a public address'), ephemeral=True)
        limit_gb = float(self.bot.settings.get("music_max_gb", 20))
        if await self.bot.work.run("music", ml.total_bytes, self.root) > limit_gb * 1024 ** 3:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "The library reached its size limit of {limit_gb} GB (music_max_gb in settings.json).", limit_gb=format(limit_gb, "g")), ephemeral=True)
        await ctx.defer()
        fmt = format or conf["download_format"]
        folder = self.root / ml.TEMP_DIR / uuid.uuid4().hex
        folder.mkdir(parents=True, exist_ok=True)
        try:
            files = await self.bot.work.run("music", download_job, url, folder, self.ffmpeg, fmt, conf["allow_playlists"], conf["playlist_limit"], conf["max_minutes"] * 60, int(self.bot.settings.get("music_max_mb", 300)))
            saved = []
            for source, info in files:
                entry, codec = await self.bot.work.run("music", file_into_library, self.root, source, info)
                saved.append((entry, codec))
        except yt_dlp.utils.DownloadError as exc:
            log.info("download failed: %s", exc)
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "The download failed: {trim}", trim=trim(str(exc).replace('ERROR: ', ''), 300)))
        except (OSError, ValueError) as exc:
            log.warning("download could not be saved: %s", exc)
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "The file could not be saved: {exc}", exc=exc))
        finally:
            shutil.rmtree(folder, ignore_errors=True)
        if not saved:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Nothing was saved. The track may be too long, too large or a live stream."))
        await self.index(force=True)
        lines = [f"`{e['path']}` | source {codec.split('.')[0]}, saved as {e['ext'][1:].upper()}" for e, codec in saved[:12]]
        lossy_source = any(codec.split(".")[0] not in LOSSLESS_CODECS for _, codec in saved)
        note = "\nThe source was lossy. Converting to FLAC does not add quality." if lossy_source and fmt == "flac" else ""
        await ctx.send(embed=emb(f"Saved {len(saved)} file(s)", trim("\n".join(lines), 3500) + note))

    @music.command(name="settings", description="Change the music settings (Manage Server)")
    @app_commands.describe(dj_role="Role that controls playback (leave empty for everyone)", volume="Default volume", max_queue="Tracks in the queue", per_user="Tracks per member", max_minutes="Longest track in minutes", idle_leave="Seconds until the bot leaves when idle (0 = never)", allow_links="Play links", allow_search="Search the web for text", allow_playlists="Allow playlists", library="Play from the local library", allow_download="Allow saving links in the library", download_format="Format of downloads", announce="Post the new track in the channel")
    async def settings(self, ctx, dj_role: Optional[discord.Role] = None, volume: Optional[app_commands.Range[int, 1, 150]] = None, max_queue: Optional[app_commands.Range[int, 1, 500]] = None, per_user: Optional[app_commands.Range[int, 1, 500]] = None, max_minutes: Optional[app_commands.Range[int, 1, 600]] = None, idle_leave: Optional[app_commands.Range[int, 0, 3600]] = None, allow_links: Optional[bool] = None, allow_search: Optional[bool] = None, allow_playlists: Optional[bool] = None, library: Optional[bool] = None, allow_download: Optional[bool] = None, download_format: Optional[Literal[FORMATS]] = None, announce: Optional[bool] = None):
        """Change the music settings (Manage Server)."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "You need the Manage Server permission."), ephemeral=True)
        c = self.conf(ctx.guild.id)
        if dj_role:
            c["dj_role"] = dj_role.id
        for key, value in (("volume", volume), ("max_queue", max_queue), ("per_user", per_user), ("max_minutes", max_minutes), ("idle_leave", idle_leave), ("allow_links", allow_links), ("allow_search", allow_search), ("allow_playlists", allow_playlists), ("library", library), ("allow_download", allow_download), ("download_format", download_format), ("announce", announce)):
            if value is not None:
                c[key] = value
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Saved. /music status shows the settings."), ephemeral=True)

    @music.command(name="cleardj", description="Let everyone control the music again (Manage Server)")
    async def cleardj(self, ctx):
        """Let everyone control the music again (Manage Server)."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "You need the Manage Server permission."), ephemeral=True)
        self.conf(ctx.guild.id)["dj_role"] = None
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Everyone can control the music."), ephemeral=True)

    @music.command(name="status", description="Show the music settings and whether this machine is ready")
    async def status(self, ctx):
        """Show the music settings and whether this machine is ready."""
        c = self.conf(ctx.guild.id)
        lines = [
            f"Module: {'on' if self.bot.module_on(ctx.guild.id, 'music') else 'off'}",
            f"Ready: {self.not_ready() or 'yes'}",
            f"yt-dlp: {'installed' if yt_dlp else 'missing'}",
            f"Library folder: `{self.root}`, {len(self.entries)} tracks known",
            f"DJ role: {'<@&' + str(c['dj_role']) + '>' if c['dj_role'] else 'none, everyone controls'}",
            f"Links {c['allow_links']}, web search {c['allow_search']}, playlists {c['allow_playlists']} (max {c['playlist_limit']}), library {c['library']}",
            f"Downloads {c['allow_download']} ({c['download_format']}), longest track {c['max_minutes']} min",
            f"Queue: {c['max_queue']} total, {c['per_user']} per member, idle leave {c['idle_leave']} s, volume {c['volume']}%",
        ]
        await ctx.send("\n".join(lines), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Leave when the bot is disconnected, and when nobody listens any more."""
        player = self.players.get(member.guild.id)
        if player is None or player.vc is None:
            return
        if member.id == self.bot.user.id and after.channel is None:
            return await self.destroy(member.guild.id)
        channel = player.vc.channel
        if channel is None:
            return
        listeners = [m for m in channel.members if not m.bot]
        if not listeners:
            player.schedule_idle(max(player.conf["idle_leave"], 30) if player.conf["idle_leave"] else 60)
        elif player.playing:
            player.cancel_idle()


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Music(bot))
