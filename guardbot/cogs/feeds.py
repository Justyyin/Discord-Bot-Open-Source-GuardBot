"""Feeds: new videos of a YouTube channel, streams of a Twitch channel and any RSS or Atom feed."""

import asyncio
import logging
import os
import re
import xml.etree.ElementTree as ET
from typing import Literal, Optional
from urllib.parse import urljoin

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks

from .. import i18n
from ..linkcheck import make_session, url_problem
from ..utils import AdminGroup, emb

log = logging.getLogger(__name__)

MAX_FEEDS = 10
MAX_BYTES = 1_000_000
SEEN_KEEP = 100
MAX_POSTS = 3
YOUTUBE_ID = re.compile(r"UC[\w-]{22}")
TWITCH_LOGIN = re.compile(r"[a-z0-9_]{3,25}")
ATOM = "{http://www.w3.org/2005/Atom}"


def youtube_id(text):
    """Find the channel ID (UC...) in a text or link, or None."""
    m = YOUTUBE_ID.search(text or "")
    return m.group(0) if m else None


def parse_feed(data):
    """Read an RSS or Atom document into entries {id, title, link}, newest first. Documents with entity or doctype declarations are refused."""
    low = data.lower()
    if b"<!doctype" in low or b"<!entity" in low:
        raise ValueError("feeds with a document type declaration are not accepted")
    root = ET.fromstring(data)
    out = []
    for entry in root.iter(f"{ATOM}entry"):
        link = next((link.get("href") for link in entry.findall(f"{ATOM}link") if link.get("rel", "alternate") == "alternate"), None)
        eid = entry.findtext(f"{ATOM}id") or link
        if eid:
            out.append({"id": eid.strip(), "title": (entry.findtext(f"{ATOM}title") or "").strip(), "link": (link or "").strip()})
    for item in root.iter("item"):
        link = (item.findtext("link") or "").strip()
        eid = (item.findtext("guid") or link or "").strip()
        if eid:
            out.append({"id": eid, "title": (item.findtext("title") or "").strip(), "link": link})
    return out


def valid_feed(feed):
    """True if a stored feed has the expected shape. Imported or damaged data must not stop the loop."""
    return (
        isinstance(feed, dict) and feed.get("kind") in ("youtube", "twitch", "rss") and isinstance(feed.get("target"), str) and isinstance(feed.get("channel"), int)
        and isinstance(feed.get("seen"), list) and isinstance(feed.get("seeded"), bool) and (feed.get("ping") is None or isinstance(feed.get("ping"), int))
    )


def new_entries(entries, seen):
    """Entries that were not seen before, oldest first, limited to the number that may be posted at once."""
    fresh = [e for e in entries if e["id"] not in set(seen)]
    return list(reversed(fresh))[-MAX_POSTS:]


def remember(seen, entries):
    """Add entry IDs to the seen list and keep only the newest ones."""
    for e in reversed(entries):
        if e["id"] not in seen:
            seen.append(e["id"])
    del seen[:-SEEN_KEEP]


async def fetch(session, url, hops=3):
    """Download a small document. Every redirect target is checked again, the size is capped and only public hosts are reached."""
    for _ in range(hops + 1):
        problem = url_problem(url)
        if problem:
            raise ValueError(problem)
        async with session.get(url, allow_redirects=False, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status in (301, 302, 303, 307, 308) and resp.headers.get("Location"):
                url = urljoin(url, resp.headers["Location"])
                continue
            if resp.status != 200:
                raise ValueError(f"the server answered {resp.status}")
            data = bytearray()
            async for chunk in resp.content.iter_chunked(65536):
                data += chunk
                if len(data) > MAX_BYTES:
                    raise ValueError("the feed is too large")
            return bytes(data)
    raise ValueError("too many redirects")


class Feeds(commands.Cog):
    """Feeds for YouTube, Twitch and RSS."""

    fg = AdminGroup(name="feed", description="Post new videos, streams and articles", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot
        self.session = None
        self.twitch_token = None

    async def cog_load(self):
        """Start the loop."""
        self.session = make_session()
        self.poll.start()

    async def cog_unload(self):
        """Stop the loop and close the connection."""
        self.poll.cancel()
        if self.session:
            await self.session.close()

    def conf(self, gid):
        """Return the feed settings of a server."""
        return self.bot.cfg(gid)["feeds"]

    async def twitch_stream(self, login):
        """Return the running stream of a channel as an entry, or None when it is offline."""
        cid, secret = os.environ.get("TWITCH_CLIENT_ID"), os.environ.get("TWITCH_CLIENT_SECRET")
        if not cid or not secret:
            raise ValueError("TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET are not set in .env")
        for attempt in range(2):
            if not self.twitch_token:
                async with self.session.post("https://id.twitch.tv/oauth2/token", data={"client_id": cid, "client_secret": secret, "grant_type": "client_credentials"}, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        raise ValueError("Twitch refused the login, check the client ID and secret")
                    self.twitch_token = (await resp.json())["access_token"]
            async with self.session.get("https://api.twitch.tv/helix/streams", params={"user_login": login}, headers={"Client-Id": cid, "Authorization": f"Bearer {self.twitch_token}"}, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 401 and attempt == 0:
                    self.twitch_token = None
                    continue
                if resp.status != 200:
                    raise ValueError(f"Twitch answered {resp.status}")
                data = (await resp.json()).get("data", [])
            if not data:
                return None
            s = data[0]
            return {"id": str(s["id"]), "title": f"{s['user_name']} is live: {s.get('title', '')}".strip(), "link": f"https://twitch.tv/{login}"}
        return None

    async def entries_of(self, feed):
        """Fetch the current entries of a feed."""
        if feed["kind"] == "twitch":
            live = await self.twitch_stream(feed["target"])
            return [live] if live else []
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={feed['target']}" if feed["kind"] == "youtube" else feed["target"]
        return parse_feed(await fetch(self.session, url))

    async def run_feed(self, guild, fid, feed):
        """Check one feed and post what is new. The first check only remembers what exists."""
        try:
            entries = await self.entries_of(feed)
        except (ValueError, ET.ParseError, aiohttp.ClientError, asyncio.TimeoutError, OSError, KeyError) as exc:
            feed["errors"] = feed.get("errors", 0) + 1
            if feed["errors"] == 12:
                self.bot.log(guild, "main", emb("Feed does not work", f"Feed {fid} ({feed['kind']}) failed 12 times in a row: {exc}", color=discord.Color.orange()))
            return 0
        feed["errors"] = 0
        if not feed["seeded"]:
            feed["seeded"] = True
            remember(feed["seen"], entries)
            return 0
        fresh = new_entries(entries, feed["seen"])
        remember(feed["seen"], entries)
        ch = guild.get_channel(feed["channel"])
        if ch is None:
            return 0
        ping = f"<@&{feed['ping']}> " if feed["ping"] else ""
        sent = 0
        for e in fresh:
            try:
                await ch.send(f"{ping}{e['title']}\n{e['link']}".strip()[:1900], allowed_mentions=discord.AllowedMentions(roles=True, users=False, everyone=False))
                sent += 1
            except discord.HTTPException as exc:
                log.warning("feed post failed: %s", exc)
                break
            await asyncio.sleep(1)
        return sent

    @tasks.loop(minutes=10)
    async def poll(self):
        """Check all feeds of all servers."""
        for guild in list(self.bot.guilds):
            if not self.bot.module_on(guild.id, "feeds"):
                continue
            for fid, feed in list(self.conf(guild.id)["items"].items()):
                if not valid_feed(feed):
                    self.conf(guild.id)["items"].pop(fid, None)
                    log.warning("removed a damaged feed on %s", guild.id)
                    continue
                try:
                    await self.run_feed(guild, fid, feed)
                except Exception:  # one broken feed must not stop the others
                    log.exception("feed %s on %s failed", fid, guild.id)

    @poll.before_loop
    async def _wait(self):
        """Wait until the bot is connected."""
        await self.bot.wait_until_ready()

    @fg.command(name="add", description="Follow a YouTube channel, a Twitch channel or an RSS feed")
    @app_commands.describe(kind="Type of feed", target="YouTube channel ID or link, Twitch name, or the feed link", channel="Where to post", ping="Role to ping for new items")
    async def add(self, it: discord.Interaction, kind: Literal["youtube", "twitch", "rss"], target: str, channel: discord.TextChannel, ping: Optional[discord.Role] = None):
        """Follow a YouTube channel, a Twitch channel or an RSS feed."""
        c = self.conf(it.guild_id)
        if len(c["items"]) >= MAX_FEEDS:
            return await it.response.send_message(f"A server can have {MAX_FEEDS} feeds.", ephemeral=True)
        target = target.strip()
        if kind == "youtube":
            target = youtube_id(target)
            if not target:
                return await it.response.send_message(i18n.say(it.client, it.guild, "I need the channel ID (starts with UC) or a channel link that contains it. Names starting with @ cannot be resolved."), ephemeral=True)
        elif kind == "twitch":
            target = target.lower().rsplit("/", 1)[-1]
            if not TWITCH_LOGIN.fullmatch(target):
                return await it.response.send_message(i18n.say(it.client, it.guild, "That is not a Twitch channel name."), ephemeral=True)
            if not os.environ.get("TWITCH_CLIENT_ID") or not os.environ.get("TWITCH_CLIENT_SECRET"):
                return await it.response.send_message(i18n.say(it.client, it.guild, "Twitch needs TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET in the .env file of the bot."), ephemeral=True)
        else:
            problem = url_problem(target)
            if problem:
                return await it.response.send_message(f"That link cannot be used: {problem}.", ephemeral=True)
        if not channel.permissions_for(it.guild.me).send_messages:
            return await it.response.send_message(i18n.say(it.client, it.guild, "I cannot post in that channel."), ephemeral=True)
        fid = str(c["next"])
        feed = {"kind": kind, "target": target, "channel": channel.id, "ping": ping.id if ping else None, "seen": [], "seeded": False, "errors": 0}
        await it.response.defer(ephemeral=True)
        try:
            await self.entries_of(feed)
        except (ValueError, ET.ParseError, aiohttp.ClientError, asyncio.TimeoutError, OSError, KeyError) as exc:
            return await it.followup.send(f"I could not read that feed: {exc}")
        c["next"] += 1
        c["items"][fid] = feed
        await self.run_feed(it.guild, fid, feed)
        await it.followup.send(f"Feed {fid} added. Only items that appear from now on are posted in {channel.mention}.")

    @fg.command(name="list", description="Show the feeds")
    async def list(self, it: discord.Interaction):
        """Show the feeds."""
        items = self.conf(it.guild_id)["items"]
        lines = [f"{fid}. {f['kind']} {f['target']} to <#{f['channel']}>" + (f", {f['errors']} errors in a row" if f.get("errors") else "") for fid, f in items.items()]
        await it.response.send_message("\n".join(lines) or "No feeds yet.", ephemeral=True)

    @fg.command(name="remove", description="Stop a feed")
    @app_commands.describe(number="Number from /post feed list")
    async def remove(self, it: discord.Interaction, number: int):
        """Stop a feed."""
        gone = self.conf(it.guild_id)["items"].pop(str(number), None)
        await it.response.send_message("Removed." if gone else "There is no such feed.", ephemeral=True)

    @fg.command(name="check", description="Check all feeds now")
    async def check(self, it: discord.Interaction):
        """Check all feeds now."""
        await it.response.defer(ephemeral=True)
        total = 0
        for fid, feed in list(self.conf(it.guild_id)["items"].items()):
            if valid_feed(feed):
                total += await self.run_feed(it.guild, fid, feed)
        await it.followup.send(f"{total} new item(s) posted.")


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Feeds(bot))
