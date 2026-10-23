"""Music: plays links, searches, saved playlists and files of the local library in voice channels and downloads into a structured library.

Spotify, Apple Music and Tidal links are read as title and artist and played from the search source (YouTube or SoundCloud).
With 24/7 mode the bot stays in a home channel and plays a saved playlist on repeat.
"""

import asyncio
import logging
import os
import random
import re
import shlex
import shutil
import time
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Literal, Optional
from urllib.parse import urlparse

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from ...cog import BaseCog
from ... import i18n, musiclib as ml, musicsources as ms
from ...linkcheck import public_host, url_problem
from ...utils import emb, trim

from ...musicdl import FORMATS, GENERIC, INDEX_TTL, LOSSLESS_CODECS, NET_INPUT, PAGE, RESUME_WITHIN, clean_artist, download_job, extract, file_into_library, yt_dlp
from ...musicplayer import Player

log = logging.getLogger(__name__)

MAX_LISTS = 50
MAX_LIST_ITEMS = 500
REJOIN_SECONDS = 15


def list_name(name):
    """A playlist name: one line, at most 40 characters."""
    return re.sub(r"\s+", " ", str(name or "")).strip()[:40]


def saved_track(t):
    """The part of a track that a playlist keeps."""
    return {"title": t.title[:200], "artist": t.artist[:200], "kind": t.kind, "ref": t.ref[:500], "length": float(t.length or 0)}


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
        self.rejoin = {}
        self.resolver = ms.Resolver(lambda: self.bot.session, bot.settings, os.environ)
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
        for guild in list(self.bot.guilds):
            try:
                await self.ensure_home(guild)
            except (discord.DiscordException, asyncio.TimeoutError) as exc:
                log.warning("could not join the 24/7 channel of %s: %s", guild.id, exc)

    async def restore(self, gid, data):
        """Rebuild the player of one server from saved state."""
        guild = self.bot.get_guild(gid)
        channel = guild.get_channel(data["channel"]) if guild else None
        if channel is None or time.time() - data["saved"] > RESUME_WITHIN or not self.bot.module_on(gid, "music") or self.not_ready():
            return
        if not [m for m in channel.members if not m.bot] and not self.conf(gid)["stay"]:
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
        for task in self.rejoin.values():
            task.cancel()
        for gid in list(self.players):
            await self.destroy(gid)

    async def connect_to(self, guild, channel):
        """Connect or move the player of a server to a voice channel. Returns (player, problem)."""
        problem = self.not_ready()
        if problem:
            return None, problem
        perms = channel.permissions_for(guild.me)
        if not (perms.connect and perms.speak):
            return None, i18n.say(self.bot, guild, "I need the Connect and Speak permissions in your voice channel.")
        player = self.players.get(guild.id)
        if player and player.vc and player.vc.is_connected():
            if player.vc.channel != channel:
                await player.vc.move_to(channel)
            return player, None
        if player is None:
            player = self.players[guild.id] = Player(self, guild)
        try:
            player.vc = await channel.connect(self_deaf=True)
        except (discord.DiscordException, asyncio.TimeoutError) as exc:
            self.players.pop(guild.id, None)
            log.warning("voice connect failed: %s", exc)
            return None, i18n.say(self.bot, guild, "I could not join the voice channel: {exc}", exc=exc)
        return player, None

    async def ensure_home(self, guild):
        """In 24/7 mode, join the home channel and start the 24/7 playlist when the bot is not in a voice channel yet."""
        conf = self.conf(guild.id)
        if not self.bot.module_on(guild.id, "music") or not conf["stay"] or not conf["home_channel"]:
            return
        player = self.players.get(guild.id)
        if player and player.vc and player.vc.is_connected():
            return
        channel = guild.get_channel(conf["home_channel"])
        if not isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
            return
        player, problem = await self.connect_to(guild, channel)
        if problem:
            log.info("24/7 channel of %s not joined: %s", guild.id, problem)
            return
        if not player.playing:
            await player.next()

    def schedule_rejoin(self, guild):
        """Join the 24/7 channel again a few seconds after the bot was disconnected."""
        old = self.rejoin.pop(guild.id, None)
        if old:
            old.cancel()

        async def later():
            await asyncio.sleep(REJOIN_SECONDS)
            self.rejoin.pop(guild.id, None)
            try:
                await self.ensure_home(guild)
            except (discord.DiscordException, asyncio.TimeoutError) as exc:
                log.warning("could not rejoin the 24/7 channel of %s: %s", guild.id, exc)

        self.rejoin[guild.id] = asyncio.create_task(later())

    async def autoplay(self, player):
        """In 24/7 mode with a 24/7 playlist, fill the empty queue with that playlist. Returns True when tracks were added."""
        conf = player.conf
        if not conf["stay"] or not conf["autoplay"]:
            return False
        _, data = self.find_list(player.guild.id, conf["autoplay"])
        if not data:
            return False
        for t in self.list_tracks(data, self.bot.user.id if self.bot.user else 0)[: conf["max_queue"]]:
            player.queue.add(t)
        return len(player.queue) > 0

    def playlists(self, gid):
        """The saved playlists of a server as {name: {"tracks": [...], "by": user id, "updated": time}}."""
        return self.conf(gid).setdefault("playlists", {})

    def find_list(self, gid, name):
        """(stored name, playlist) for a name in any letter case, or (None, None)."""
        want = list_name(name).casefold()
        for key, data in self.playlists(gid).items():
            if key.casefold() == want:
                return key, data
        return None, None

    @staticmethod
    def list_tracks(data, uid):
        """The tracks of a saved playlist as queue entries."""
        out = []
        for t in data.get("tracks", []):
            try:
                out.append(ml.Track(title=str(t["title"]), artist=str(t.get("artist", "")), kind=t["kind"], ref=str(t["ref"]), length=float(t.get("length") or 0), requester=uid))
            except (KeyError, TypeError, ValueError):
                continue
        return [t for t in out if t.kind in ("local", "web", "search")]

    def store_list(self, gid, name, tracks, uid, append):
        """Save tracks under a playlist name, new or appended. Returns (name, number of tracks, problem)."""
        name = list_name(name)
        if not name:
            return None, 0, "Give the playlist a name."
        lists = self.playlists(gid)
        key, data = self.find_list(gid, name)
        if data is None:
            if len(lists) >= MAX_LISTS:
                return None, 0, f"A server can keep at most {MAX_LISTS} playlists."
            key, data = name, {"tracks": [], "by": uid, "updated": 0}
            lists[key] = data
        items = (data["tracks"] if append else []) + [saved_track(t) for t in tracks]
        data["tracks"], data["by"], data["updated"] = items[:MAX_LIST_ITEMS], uid, int(time.time())
        return key, len(data["tracks"]), None

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
        if track.kind == "search":
            if not track.ref.startswith(tuple(ms.SEARCH.values())):
                raise RuntimeError("unknown search")
            found = await self.bot.work.run("music", extract, track.ref, self.ffmpeg, False, 1, True)
            entries = [e for e in (found or {}).get("entries") or [] if e]
            if not entries:
                raise RuntimeError("no matching song was found")
            info = entries[0]
            page = info.get("webpage_url") or info.get("original_url") or ""
            problem = url_problem(page, conf["allowed_hosts"], conf["blocked_hosts"]) if page else None
            if problem:
                raise RuntimeError(problem)
        else:
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

    @staticmethod
    def search_prefix(conf):
        """The yt-dlp search of the search source, falling back to the other one, or None when both are switched off."""
        for src in (conf.get("search_source", "youtube"), "youtube", "soundcloud"):
            if src in ms.SEARCH and conf.get(src, True):
                return ms.SEARCH[src]
        return None

    async def find_tracks(self, gid, uid, query, local_only=False):
        """Turn a link or a search text into tracks. Returns (tracks, error)."""
        conf = self.conf(gid)
        query = query.strip()
        if query.startswith(("http://", "https://")) and not local_only:
            if not conf["allow_links"]:
                return [], i18n.say(self.bot, gid, "Playing links is turned off on this server.")
            problem = url_problem(query, conf["allowed_hosts"], conf["blocked_hosts"])
            if problem or not await public_host(urlparse(query).hostname or ""):
                return [], i18n.say(self.bot, gid, "I cannot open this link: {value}.", value=problem or "it does not resolve to a public address")
            src = ms.service(query)
            if src and not conf.get(src, True):
                return [], i18n.say(self.bot, gid, "{service} links are turned off on this server.", service=ms.NAMES[src])
            if yt_dlp is None:
                return [], i18n.say(self.bot, gid, "Link playback needs yt-dlp. Install it with: pip install yt-dlp")
            if src in ms.MIRRORED:
                return await self.from_service(gid, uid, query, conf)
            return await self.from_web(gid, uid, query, conf, playlist=conf["allow_playlists"])
        if conf["library"]:
            hits = ml.search(await self.index(), query, 1)
            if hits:
                return [self.track_from_entry(hits[0], uid)], None
        prefix = self.search_prefix(conf)
        if local_only or yt_dlp is None:
            return [], i18n.say(self.bot, gid, "Nothing found in the library.")
        if not conf["allow_search"] or prefix is None:
            return [], i18n.say(self.bot, gid, "Searching the web is turned off on this server.")
        return await self.from_web(gid, uid, f"{prefix}{query}", conf, playlist=False)

    async def from_service(self, gid, uid, url, conf):
        """Read the songs of a Spotify, Apple Music or Tidal link and queue them as searches on the search source."""
        prefix = self.search_prefix(conf)
        if prefix is None:
            return [], i18n.say(self.bot, gid, "Songs from this service are played through YouTube or SoundCloud. Switch one of them on.")
        try:
            songs = await self.resolver.songs(url, conf["playlist_limit"] if conf["allow_playlists"] else 1)
        except (ValueError, aiohttp.ClientError, asyncio.TimeoutError) as exc:
            log.info("could not read %s: %s", urlparse(url).hostname, exc)
            return [], i18n.say(self.bot, gid, "I could not read this link: {reason}", reason=trim(str(exc) or type(exc).__name__, 200))
        tracks = [ml.Track(title=s.title, artist=s.artist, kind="search", ref=prefix + s.query(), length=s.length, requester=uid) for s in songs if not (s.length and s.length > conf["max_minutes"] * 60)]
        if not tracks:
            return [], i18n.say(self.bot, gid, "No playable result (tracks longer than {minutes} minutes are skipped).", minutes=conf["max_minutes"])
        return tracks, None

    async def from_web(self, gid, uid, target, conf, playlist):
        """Read a link or search result with yt-dlp and build the tracks."""
        try:
            info = await self.bot.work.run("music", extract, target, self.ffmpeg, playlist, conf["playlist_limit"], target.startswith(tuple(ms.SEARCH.values())))
        except yt_dlp.utils.DownloadError as exc:
            log.info("yt-dlp could not read %s: %s", urlparse(target).hostname, exc)
            return [], f"I could not read that: {trim(str(exc).replace('ERROR: ', ''), 300)}"
        if info is None:
            return [], "Nothing found."
        entries = info.get("entries")
        items = [e for e in entries if e] if entries is not None else [info]
        tracks = []
        for e in items[: conf["playlist_limit"]]:
            t = self.track_from_info(e, uid)
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
        player = self.players.get(ctx.guild.id)
        if player and player.vc and player.vc.is_connected() and player.vc.channel != channel:
            others = [m for m in player.vc.channel.members if not m.bot]
            if others and not self.is_dj(ctx.author):
                await ctx.send(i18n.say(ctx.bot, ctx.guild, "I am already playing in {mention}.", mention=player.vc.channel.mention), ephemeral=True)
                return None
        player, problem = await self.connect_to(ctx.guild, channel)
        if problem:
            await ctx.send(problem, ephemeral=True)
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
        added = await self.add_tracks(player, tracks, ctx.author.id)
        if not added:
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "The queue is full for you or for the server."), ephemeral=True)
        return added

    async def add_tracks(self, player, tracks, uid):
        """Add tracks within the limits of the queue and start playing if idle. Returns how many were added."""
        conf = player.conf
        room = min(conf["max_queue"] - len(player.queue), conf["per_user"] - player.queue.count_by(uid))
        tracks = tracks[: max(room, 0)]
        for t in tracks:
            player.queue.add(t)
        if tracks and not player.playing:
            await player.next()
        return len(tracks)

    @commands.hybrid_command(name="play", description="Play a link, or search the library and the web")
    @app_commands.describe(query="Link, or words from the artist or title")
    @commands.guild_only()
    async def play(self, ctx, *, query: str):
        """Play a link, or search the library and the web."""
        await ctx.defer()
        tracks, error = await self.find_tracks(ctx.guild.id, ctx.author.id, query)
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
        tracks, error = await self.find_tracks(ctx.guild.id, ctx.author.id, query, local_only=True)
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

    @library.command(name="playall", description="Queue all tracks of an artist, album or folder (* for everything)")
    @app_commands.describe(query="Artist, album or folder name, or * for the whole library", shuffle="Mix the order")
    async def lib_playall(self, ctx, query: str, shuffle: bool = False):
        """Queue all tracks of an artist, album or folder."""
        if not self.conf(ctx.guild.id)["library"]:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "The music folder is turned off on this server."), ephemeral=True)
        await ctx.defer()
        tracks = self.folder_tracks(await self.index(), query, ctx.author.id, shuffle)
        if not tracks:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Nothing found in the library."), ephemeral=True)
        added = await self.enqueue(ctx, tracks)
        if added:
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Added {count} tracks from the library.", count=added))

    def folder_tracks(self, entries, query, uid, shuffle=False):
        """Library tracks whose artist, album or folder contains the words, or all for *."""
        q = (query or "").strip().casefold()
        hits = entries if q == "*" else [e for e in entries if q and (q in e["artist"].casefold() or q in (e["album"] or "").casefold() or q in e["path"].casefold())]
        tracks = [self.track_from_entry(e, uid) for e in hits]
        if shuffle:
            random.shuffle(tracks)
        return tracks

    @music.group(name="playlist", description="Saved playlists of this server")
    async def playlist(self, ctx):
        """Commands for saved playlists."""
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Use save, add, play, list, show, remove or delete."), ephemeral=True)

    async def list_complete(self, it: discord.Interaction, current: str):
        """Suggest saved playlists while typing."""
        if not it.guild_id:
            return []
        return [app_commands.Choice(name=k[:100], value=k[:100]) for k in self.playlists(it.guild_id) if current.casefold() in k.casefold()][:25]

    def may_edit_lists(self, member):
        """DJs, or everyone when no DJ role is set, may change playlists."""
        return self.is_dj(member)

    @playlist.command(name="save", description="Save the current track and the queue as a playlist")
    @app_commands.describe(name="Name of the playlist")
    async def pl_save(self, ctx, *, name: str):
        """Save the current track and the queue as a playlist."""
        if not self.may_edit_lists(ctx.author):
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Only members with the DJ role can do this."), ephemeral=True)
        player = self.players.get(ctx.guild.id)
        tracks = ([player.queue.current] if player and player.queue.current else []) + (list(player.queue.items) if player else [])
        if not tracks:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "The queue is empty."), ephemeral=True)
        key, count, problem = self.store_list(ctx.guild.id, name, tracks, ctx.author.id, append=False)
        if problem:
            return await ctx.send(problem, ephemeral=True)
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Saved {count} tracks as playlist {name}.", count=count, name=key), ephemeral=True)

    @playlist.command(name="add", description="Add a link or search result to a playlist")
    @app_commands.describe(name="Name of the playlist", query="Link, or words from the artist or title")
    @app_commands.autocomplete(name=list_complete)
    async def pl_add(self, ctx, name: str, *, query: str):
        """Add a link or search result to a playlist."""
        if not self.may_edit_lists(ctx.author):
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Only members with the DJ role can do this."), ephemeral=True)
        await ctx.defer(ephemeral=True)
        tracks, error = await self.find_tracks(ctx.guild.id, ctx.author.id, query)
        if error:
            return await ctx.send(error, ephemeral=True)
        key, count, problem = self.store_list(ctx.guild.id, name, tracks, ctx.author.id, append=True)
        if problem:
            return await ctx.send(problem, ephemeral=True)
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Added {added} tracks, playlist {name} has {count} now.", added=len(tracks), name=key, count=count), ephemeral=True)

    @playlist.command(name="play", description="Play a saved playlist")
    @app_commands.describe(name="Name of the playlist", shuffle="Mix the order")
    @app_commands.autocomplete(name=list_complete)
    async def pl_play(self, ctx, name: str, shuffle: bool = False):
        """Play a saved playlist."""
        key, data = self.find_list(ctx.guild.id, name)
        if data is None:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "No playlist with this name."), ephemeral=True)
        tracks = self.list_tracks(data, ctx.author.id)
        if shuffle:
            random.shuffle(tracks)
        added = await self.enqueue(ctx, tracks)
        if added:
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "Added {count} tracks from playlist {name}.", count=added, name=key))

    @playlist.command(name="list", description="List the saved playlists")
    async def pl_list(self, ctx):
        """List the saved playlists."""
        lists = self.playlists(ctx.guild.id)
        lines = [f"**{trim(k, 40)}** ({len(v.get('tracks', []))})" for k, v in sorted(lists.items(), key=lambda kv: kv[0].casefold())]
        await ctx.send(embed=emb("Playlists", "\n".join(lines) or i18n.say(ctx.bot, ctx.guild, "No playlists yet.")), ephemeral=True)

    @playlist.command(name="show", description="Show the tracks of a playlist")
    @app_commands.describe(name="Name of the playlist", page="Page")
    @app_commands.autocomplete(name=list_complete)
    async def pl_show(self, ctx, name: str, page: int = 1):
        """Show the tracks of a playlist."""
        key, data = self.find_list(ctx.guild.id, name)
        if data is None:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "No playlist with this name."), ephemeral=True)
        items = data.get("tracks", [])
        pages = max(1, -(-len(items) // PAGE))
        page = min(max(page, 1), pages)
        lines = [f"{i}. {trim(t.get('artist') + ' - ' if t.get('artist') else '', 50)}{trim(t.get('title', ''), 70)}" for i, t in enumerate(items[(page - 1) * PAGE : page * PAGE], (page - 1) * PAGE + 1)]
        e = emb(key, "\n".join(lines) or i18n.say(ctx.bot, ctx.guild, "The playlist is empty."))
        e.set_footer(text=f"{page}/{pages} | {len(items)}")
        await ctx.send(embed=e, ephemeral=True)

    @playlist.command(name="remove", description="Remove a track from a playlist by its number")
    @app_commands.describe(name="Name of the playlist", number="Number of the track")
    @app_commands.autocomplete(name=list_complete)
    async def pl_remove(self, ctx, name: str, number: int):
        """Remove a track from a playlist by its number."""
        if not self.may_edit_lists(ctx.author):
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Only members with the DJ role can do this."), ephemeral=True)
        key, data = self.find_list(ctx.guild.id, name)
        if data is None or not 1 <= number <= len(data.get("tracks", [])):
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "No track with this number."), ephemeral=True)
        gone = data["tracks"].pop(number - 1)
        data["updated"] = int(time.time())
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Removed {title}.", title=trim(gone.get("title", ""), 100)), ephemeral=True)

    @playlist.command(name="delete", description="Delete a playlist")
    @app_commands.describe(name="Name of the playlist")
    @app_commands.autocomplete(name=list_complete)
    async def pl_delete(self, ctx, *, name: str):
        """Delete a playlist."""
        if not self.may_edit_lists(ctx.author):
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Only members with the DJ role can do this."), ephemeral=True)
        key, data = self.find_list(ctx.guild.id, name)
        if data is None:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "No playlist with this name."), ephemeral=True)
        del self.playlists(ctx.guild.id)[key]
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Playlist {name} deleted.", name=key), ephemeral=True)

    @music.command(name="sources", description="Switch music sources on or off (Manage Server)")
    @app_commands.describe(youtube="YouTube and YouTube Music", soundcloud="SoundCloud", spotify="Spotify links", apple_music="Apple Music links", tidal="Tidal links", search="Where searches and songs from Spotify, Apple Music and Tidal are looked up")
    async def sources(self, ctx, youtube: Optional[bool] = None, soundcloud: Optional[bool] = None, spotify: Optional[bool] = None, apple_music: Optional[bool] = None, tidal: Optional[bool] = None, search: Optional[Literal["youtube", "soundcloud"]] = None):
        """Switch music sources on or off."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "You need the Manage Server permission."), ephemeral=True)
        c = self.conf(ctx.guild.id)
        for key, value in (("youtube", youtube), ("soundcloud", soundcloud), ("spotify", spotify), ("apple_music", apple_music), ("tidal", tidal), ("search_source", search)):
            if value is not None:
                c[key] = value
        state = ", ".join(f"{ms.NAMES[k]} {'on' if c[k] else 'off'}" for k in ms.NAMES)
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Sources: {state}. Search: {search}.", state=state, search=ms.NAMES[c["search_source"]]), ephemeral=True)

    @music.command(name="stay", description="24/7: stay in a voice channel and play a playlist on repeat (Manage Server)")
    @app_commands.describe(enabled="Stay in the channel even when nobody listens", channel="Voice channel to join by itself", playlist="Saved playlist that plays when the queue is empty")
    @app_commands.autocomplete(playlist=list_complete)
    async def stay(self, ctx, enabled: bool, channel: Optional[discord.VoiceChannel] = None, playlist: Optional[str] = None):
        """Switch 24/7 mode on or off."""
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "You need the Manage Server permission."), ephemeral=True)
        c = self.conf(ctx.guild.id)
        if playlist is not None:
            key, data = self.find_list(ctx.guild.id, playlist)
            if playlist and data is None:
                return await ctx.send(i18n.say(ctx.bot, ctx.guild, "No playlist with this name."), ephemeral=True)
            c["autoplay"] = key or ""
        if channel is not None:
            c["home_channel"] = channel.id
        c["stay"] = enabled
        player = self.players.get(ctx.guild.id)
        if not enabled:
            if player:
                player.schedule_idle()
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "24/7 mode is off."), ephemeral=True)
        await ctx.defer(ephemeral=True)
        if player:
            player.cancel_idle()
        await self.ensure_home(ctx.guild)
        player = self.players.get(ctx.guild.id)
        if player and not player.playing:
            await player.next()
        home = f"<#{c['home_channel']}>" if c["home_channel"] else "-"
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "24/7 mode is on. Channel: {channel}, playlist: {playlist}.", channel=home, playlist=c["autoplay"] or "-"), ephemeral=True)

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

    def snapshot(self, guild):
        """State of the music on a server for the dashboard."""
        player = self.players.get(guild.id)
        conf = self.conf(guild.id)

        def track(t):
            return {"title": t.title, "artist": t.artist, "length": t.length, "kind": t.kind, "ref": t.ref, "detail": t.detail, "requester": str(t.requester)} if t else None

        lists = [{"name": k, "count": len(v.get("tracks", [])), "updated": v.get("updated", 0)} for k, v in sorted(self.playlists(guild.id).items(), key=lambda kv: kv[0].casefold())]
        vc = player.vc if player else None
        return {
            "ready": self.not_ready(), "ytdlp": yt_dlp is not None, "library": len(self.entries), "library_dir": str(self.root),
            "channel": str(vc.channel.id) if vc and vc.channel else None, "channel_name": vc.channel.name if vc and vc.channel else None,
            "current": track(player.queue.current) if player else None, "position": int(player.position()) if player and player.queue.current else 0,
            "paused": bool(vc and vc.is_paused()), "volume": player.volume if player else conf["volume"], "loop": player.queue.loop if player else "off",
            "queue": [track(t) for t in list(player.queue.items)[:100]] if player else [], "waiting": len(player.queue) if player else 0,
            "playlists": lists, "stay": conf["stay"], "home_channel": str(conf["home_channel"]) if conf["home_channel"] else None, "autoplay": conf["autoplay"],
        }

    async def remote(self, guild, uid, action, value=None):
        """Carry out a control action from the dashboard. Returns (ok, message)."""
        player = self.players.get(guild.id)

        def say(text, **values):
            return i18n.say(self.bot, guild, text, **values)

        if action == "join":
            channel = guild.get_channel(int(value)) if str(value or "").isdigit() else None
            if not isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
                return False, say("Choose a voice channel.")
            player, problem = await self.connect_to(guild, channel)
            if problem:
                return False, problem
            if not player.playing:
                await player.next()
            return True, say("Joined {mention}.", mention=channel.name)
        if action in ("add", "playlist", "folder"):
            if action == "add":
                tracks, error = await self.find_tracks(guild.id, uid, str(value or "")[:500])
                if error:
                    return False, error
            elif action == "playlist":
                _, data = self.find_list(guild.id, str(value or ""))
                if data is None:
                    return False, say("No playlist with this name.")
                tracks = self.list_tracks(data, uid)
            else:
                if not self.conf(guild.id)["library"]:
                    return False, say("The music folder is turned off on this server.")
                tracks = self.folder_tracks(await self.index(), str(value or ""), uid)
            if not tracks:
                return False, say("Nothing found.")
            if player is None or not player.vc or not player.vc.is_connected():
                return False, say("The bot is not in a voice channel. Let it join first.")
            added = await self.add_tracks(player, tracks, uid)
            return (True, say("Added {count} tracks.", count=added)) if added else (False, say("The queue is full for you or for the server."))
        if player is None or not player.vc:
            return False, say("Nothing is playing.")
        if action == "pause" and player.vc.is_playing():
            player.vc.pause()
            player.paused_at = time.monotonic()
        elif action == "resume" and player.vc.is_paused():
            player.vc.resume()
            player.since += time.monotonic() - player.paused_at
            player.paused_at = None
        elif action == "skip":
            player.halt()
            await player.next(skipped=True)
        elif action == "stop":
            player.queue.clear()
            player.queue.current = None
            player.halt()
            player.schedule_idle()
        elif action == "leave":
            await self.destroy(guild.id)
        elif action == "shuffle":
            player.queue.shuffle()
        elif action == "clear":
            player.queue.clear()
        elif action == "loop" and value in ("off", "track", "queue"):
            player.queue.loop = value
        elif action == "volume" and isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 150:
            player.volume = value
            if player.vc.source:
                player.vc.source.volume = value / 100
        elif action == "remove" and isinstance(value, int) and not isinstance(value, bool):
            if player.queue.remove(value) is None:
                return False, say("No track with this number.")
        elif action not in ("pause", "resume"):
            return False, say("Unknown action.")
        return True, say("Done.")

    def save_playlist(self, guild, uid, name, tracks):
        """Replace or create a playlist from the dashboard with tracks given as dicts. Returns (name, problem)."""
        clean = []
        for t in tracks if isinstance(tracks, list) else []:
            if isinstance(t, dict) and t.get("kind") in ("local", "web", "search") and isinstance(t.get("ref"), str) and isinstance(t.get("title"), str):
                if t["kind"] == "web" and url_problem(t["ref"]):
                    continue
                if t["kind"] == "local" and ml.resolve(self.root, t["ref"]) is None:
                    continue
                if t["kind"] == "search" and not t["ref"].startswith(tuple(ms.SEARCH.values())):
                    continue
                length = t.get("length")
                clean.append(ml.Track(title=t["title"][:200], artist=str(t.get("artist") or "")[:200], kind=t["kind"], ref=t["ref"][:500], length=float(length) if isinstance(length, (int, float)) and not isinstance(length, bool) else 0.0, requester=uid))
        key, _, problem = self.store_list(guild.id, name, clean, uid, append=False)
        return key, problem

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Leave when the bot is disconnected, and when nobody listens any more."""
        player = self.players.get(member.guild.id)
        if player is None or player.vc is None:
            return
        if member.id == self.bot.user.id and after.channel is None:
            await self.destroy(member.guild.id)
            if self.conf(member.guild.id)["stay"] and not self.bot.is_closed():
                self.schedule_rejoin(member.guild)
            return
        channel = player.vc.channel
        if channel is None or player.conf["stay"]:
            return
        listeners = [m for m in channel.members if not m.bot]
        if not listeners:
            player.schedule_idle(max(player.conf["idle_leave"], 30) if player.conf["idle_leave"] else 60)
        elif player.playing:
            player.cancel_idle()


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Music(bot))
