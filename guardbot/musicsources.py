"""Music sources: which service a link belongs to, and reading title and artist from Spotify, Apple Music and Tidal links.

These three services do not hand out their audio. The bot only reads the public title and artist of a link and then plays
the same song from the search source (YouTube or SoundCloud). Nothing is downloaded from these services and no protection is bypassed.
The parsers below work on page data and are tested with saved examples; the services can change their pages at any time.
"""

import base64
import html
import json
import logging
import re
import time
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import parse_qs, quote, urlparse

log = logging.getLogger(__name__)

MAX_PAGE = 4 * 1024 * 1024
TIMEOUT = 15
AGENT = "Mozilla/5.0 (X11; Linux x86_64) GuardMusic"

HOSTS = {
    "youtube": ("youtube.com", "youtu.be", "music.youtube.com", "m.youtube.com", "www.youtube.com", "youtube-nocookie.com"),
    "soundcloud": ("soundcloud.com", "on.soundcloud.com", "m.soundcloud.com", "snd.sc"),
    "spotify": ("open.spotify.com", "spotify.link", "play.spotify.com"),
    "apple_music": ("music.apple.com", "embed.music.apple.com", "geo.music.apple.com"),
    "tidal": ("tidal.com", "listen.tidal.com", "www.tidal.com"),
}
NAMES = {"youtube": "YouTube", "soundcloud": "SoundCloud", "spotify": "Spotify", "apple_music": "Apple Music", "tidal": "Tidal"}
MIRRORED = ("spotify", "apple_music", "tidal")
SEARCH = {"youtube": "ytsearch1:", "soundcloud": "scsearch1:"}


@dataclass
class Song:
    """Title, artist and length of a song read from a service."""

    title: str
    artist: str = ""
    length: float = 0.0

    def query(self) -> str:
        """The search text for the search source."""
        return f"{self.artist} - {self.title}" if self.artist else self.title


def service(url: str) -> Optional[str]:
    """The service of a link: youtube, soundcloud, spotify, apple_music, tidal, or None for other sites."""
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return None
    for key, hosts in HOSTS.items():
        if any(host == h or host.endswith("." + h) for h in hosts):
            return key
    return None


def iso_seconds(text: Any) -> float:
    """Seconds of an ISO 8601 duration like PT3M25S, 0 when it cannot be read."""
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?", str(text or "").strip())
    if not m or not any(m.groups()):
        return 0.0
    d, h, mi, s = (float(x) if x else 0.0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def _clean(text: Any, limit: int = 200) -> str:
    """Plain single-line text."""
    return re.sub(r"\s+", " ", html.unescape(str(text or ""))).strip()[:limit]


def _scripts(page: str, kind: str) -> list[str]:
    """The contents of all script tags of one type."""
    return re.findall(r'<script[^>]*type=["\']' + re.escape(kind) + r'["\'][^>]*>(.*?)</script>', page, re.S | re.I)


def _meta(page: str, name: str) -> str:
    """The content of a meta tag by property or name."""
    for pattern in (
        r'<meta[^>]+(?:property|name)=["\']' + re.escape(name) + r'["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+(?:property|name)=["\']' + re.escape(name) + r'["\']',
    ):
        m = re.search(pattern, page, re.I)
        if m:
            return _clean(m.group(1))
    return ""


def _walk(node: Any):
    """Every dict inside a JSON value."""
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def spotify_id(url: str) -> Optional[tuple[str, str]]:
    """(kind, id) of a Spotify link: track, album or playlist."""
    m = re.search(r"/(track|album|playlist)/([A-Za-z0-9]{10,40})", urlparse(url).path)
    return (m.group(1), m.group(2)) if m else None


def parse_spotify_embed(page: str) -> list[Song]:
    """Songs from the data of a Spotify embed page."""
    blobs = re.findall(r'<script[^>]*id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>', page, re.S) + _scripts(page, "application/json")
    for blob in blobs:
        try:
            data = json.loads(blob)
        except ValueError:
            continue
        for node in _walk(data):
            items = node.get("trackList")
            if isinstance(items, list) and items:
                songs = [Song(_clean(t.get("title")), _clean(t.get("subtitle")), float(t.get("duration") or 0) / 1000) for t in items if isinstance(t, dict) and t.get("title")]
                if songs:
                    return songs
        for node in _walk(data):
            if node.get("type") == "track" and node.get("name") and isinstance(node.get("artists"), list):
                artists = ", ".join(_clean(a.get("name")) for a in node["artists"] if isinstance(a, dict) and a.get("name"))
                return [Song(_clean(node["name"]), artists, float(node.get("duration") or 0) / 1000)]
    return _from_meta(page)


def _artist_of(node: Any) -> str:
    """Artist names of a JSON-LD byArtist value."""
    if isinstance(node, dict):
        return _clean(node.get("name"))
    if isinstance(node, list):
        return ", ".join(n for n in (_artist_of(x) for x in node) if n)
    return _clean(node)


def parse_apple(page: str, song_id: Optional[str] = None) -> list[Song]:
    """Songs from the JSON-LD data of an Apple Music page. With song_id only that song of an album."""
    for blob in _scripts(page, "application/ld+json"):
        try:
            data = json.loads(blob)
        except ValueError:
            continue
        for node in _walk(data):
            kind = node.get("@type")
            if kind in ("MusicAlbum", "MusicPlaylist"):
                tracks = node.get("tracks") or node.get("track") or []
                if isinstance(tracks, dict):
                    tracks = tracks.get("itemListElement") or [tracks]
                album_artist = _artist_of(node.get("byArtist"))
                songs = []
                for t in tracks if isinstance(tracks, list) else []:
                    t = t.get("item", t) if isinstance(t, dict) else t
                    if not isinstance(t, dict) or not t.get("name"):
                        continue
                    if song_id and song_id not in str(t.get("url") or "") and song_id not in str(t.get("@id") or ""):
                        continue
                    songs.append(Song(_clean(t["name"]), _artist_of(t.get("byArtist")) or album_artist, iso_seconds(t.get("duration"))))
                if songs:
                    return songs
            if kind == "MusicRecording" and node.get("name"):
                return [Song(_clean(node["name"]), _artist_of(node.get("byArtist")), iso_seconds(node.get("duration")))]
    return _from_meta(page)


def _from_meta(page: str) -> list[Song]:
    """One song from the title tags of a page, as a last resort."""
    title = _meta(page, "og:title") or _meta(page, "twitter:title")
    if not title:
        m = re.search(r"<title[^>]*>(.*?)</title>", page, re.S | re.I)
        title = _clean(m.group(1)) if m else ""
    if not title:
        return []
    desc = _meta(page, "og:description")
    for sep in (" by ", " von ", " - ", " – ", " · "):
        if sep in title:
            a, b = title.split(sep, 1)
            if sep in (" by ", " von "):
                return [Song(_clean(a), _clean(b.split(" on ")[0].split(" | ")[0]))]
            return [Song(_clean(a), _clean(b.split(" | ")[0]))]
    artist = desc.split(" · ")[0] if " · " in desc else ""
    return [Song(title, _clean(artist))]


def tidal_id(url: str) -> Optional[tuple[str, str]]:
    """(kind, id) of a Tidal link: track, album or playlist."""
    m = re.search(r"/(track|album|playlist)/([A-Za-z0-9-]{4,60})", urlparse(url).path)
    return (m.group(1), m.group(2)) if m else None


def parse_tidal_api(data: Any) -> list[Song]:
    """Songs from a TIDAL API v2 answer (JSON:API with included artists and tracks)."""
    if not isinstance(data, dict):
        return []
    included = [x for x in data.get("included") or [] if isinstance(x, dict)]
    artists = {x.get("id"): _clean((x.get("attributes") or {}).get("name")) for x in included if x.get("type") == "artists"}

    def names(item: dict) -> str:
        rel = ((item.get("relationships") or {}).get("artists") or {}).get("data") or []
        return ", ".join(artists[r["id"]] for r in rel if isinstance(r, dict) and artists.get(r.get("id")))

    def song(item: dict) -> Optional[Song]:
        attrs = item.get("attributes") or {}
        if not attrs.get("title"):
            return None
        return Song(_clean(attrs["title"]), names(item), iso_seconds(attrs.get("duration")))

    main = data.get("data")
    if isinstance(main, dict) and main.get("type") == "tracks":
        s = song(main)
        if s and not s.artist:
            s.artist = ", ".join(a for a in artists.values() if a)
        return [s] if s else []
    tracks = [x for x in included if x.get("type") == "tracks"]
    order = [r.get("id") for r in main if isinstance(r, dict)] if isinstance(main, list) else [t.get("id") for t in tracks]
    by_id = {t.get("id"): t for t in tracks}
    out = []
    for tid in order:
        t = by_id.get(tid)
        s = song(t) if t else None
        if s:
            out.append(s)
    return out


class Resolver:
    """Reads songs from Spotify, Apple Music and Tidal links with the HTTP session of the bot."""

    def __init__(self, session_getter, settings: dict, env: Optional[dict] = None):
        """session_getter returns the aiohttp session; env holds optional TIDAL_CLIENT_ID and TIDAL_CLIENT_SECRET."""
        self.session = session_getter
        self.settings = settings
        self.env = env or {}
        self.tidal_token: tuple[str, float] = ("", 0.0)

    async def fetch(self, url: str, accept: str = "text/html", headers: Optional[dict] = None, follow: tuple = ()) -> tuple[int, str, str]:
        """GET a page of a known host. Redirects are only followed to hosts in follow. Returns (status, text, final url)."""
        sess = self.session()
        hdrs = {"User-Agent": AGENT, "Accept": accept, "Accept-Language": "en"}
        hdrs.update(headers or {})
        for _ in range(3):
            async with sess.get(url, headers=hdrs, allow_redirects=False, timeout=TIMEOUT) as r:
                if r.status in (301, 302, 303, 307, 308) and r.headers.get("Location"):
                    nxt = r.headers["Location"]
                    host = (urlparse(nxt).hostname or "").lower()
                    if urlparse(nxt).scheme != "https" or not any(host == h or host.endswith("." + h) for h in follow):
                        raise ValueError("the link leads to an unexpected site")
                    url = nxt
                    continue
                body = await r.content.read(MAX_PAGE + 1)
                if len(body) > MAX_PAGE:
                    raise ValueError("the page is too large")
                return r.status, body.decode("utf-8", "replace"), url
        raise ValueError("too many redirects")

    async def songs(self, url: str, limit: int) -> list[Song]:
        """The songs behind a Spotify, Apple Music or Tidal link. Raises ValueError with a reason."""
        kind = service(url)
        if kind == "spotify":
            if (urlparse(url).hostname or "").lower() == "spotify.link":
                _, _, url = await self.fetch(url, follow=("open.spotify.com",))
            ident = spotify_id(url)
            if not ident:
                raise ValueError("this Spotify link is not a track, album or playlist")
            status, page, _ = await self.fetch(f"https://open.spotify.com/embed/{ident[0]}/{ident[1]}")
            if status != 200:
                raise ValueError(f"Spotify answered with {status}")
            found = parse_spotify_embed(page)
        elif kind == "apple_music":
            song_id: Optional[str] = (parse_qs(urlparse(url).query).get("i") or [""])[0] or None
            if not song_id:
                m = re.search(r"/song/(?:[^/]+/)?(\d+)", urlparse(url).path)
                song_id = m.group(1) if m else None
            path = urlparse(url).path
            status, page, _ = await self.fetch(f"https://music.apple.com{path}")
            if status != 200:
                raise ValueError(f"Apple Music answered with {status}")
            found = parse_apple(page, song_id if "/album/" in path else None)
        elif kind == "tidal":
            found = await self.tidal(url, limit)
        else:
            raise ValueError("not a Spotify, Apple Music or Tidal link")
        found = [s for s in found if s.title][:limit]
        if not found:
            raise ValueError("no song could be read from this link")
        return found

    async def tidal(self, url: str, limit: int) -> list[Song]:
        """Songs of a Tidal link: with API keys from the official API, otherwise from the title of the page (single tracks only)."""
        ident = tidal_id(url)
        if not ident:
            raise ValueError("this Tidal link is not a track, album or playlist")
        kind, tid = ident
        cid, secret = self.env.get("TIDAL_CLIENT_ID"), self.env.get("TIDAL_CLIENT_SECRET")
        if not (cid and secret):
            if kind != "track":
                raise ValueError("Tidal albums and playlists need TIDAL_CLIENT_ID and TIDAL_CLIENT_SECRET in .env")
            status, page, _ = await self.fetch(f"https://tidal.com/browse/track/{quote(tid)}")
            if status != 200:
                raise ValueError(f"Tidal answered with {status}")
            return _from_meta(page)
        token = await self.tidal_login(cid, secret)
        country = str(self.settings.get("tidal_country", "US"))[:2].upper()
        base = "https://openapi.tidal.com/v2"
        path = {"track": f"/tracks/{tid}?countryCode={country}&include=artists",
                "album": f"/albums/{tid}/relationships/items?countryCode={country}&include=items,items.artists",
                "playlist": f"/playlists/{tid}/relationships/items?countryCode={country}&include=items,items.artists"}[kind]
        status, text, _ = await self.fetch(base + path, accept="application/vnd.api+json", headers={"Authorization": f"Bearer {token}"})
        if status != 200:
            raise ValueError(f"the Tidal API answered with {status}")
        try:
            return parse_tidal_api(json.loads(text))[:limit]
        except ValueError as exc:
            raise ValueError("the Tidal API sent something unexpected") from exc

    async def tidal_login(self, cid: str, secret: str) -> str:
        """A client credentials token of the Tidal API, cached until shortly before it expires."""
        token, until = self.tidal_token
        if token and time.time() < until:
            return token
        auth = base64.b64encode(f"{cid}:{secret}".encode()).decode()
        sess = self.session()
        async with sess.post("https://auth.tidal.com/v1/oauth2/token", data={"grant_type": "client_credentials", "client_id": cid},
                             headers={"Authorization": f"Basic {auth}", "User-Agent": AGENT}, allow_redirects=False, timeout=TIMEOUT) as r:
            if r.status != 200:
                raise ValueError(f"Tidal login failed with {r.status}, check TIDAL_CLIENT_ID and TIDAL_CLIENT_SECRET")
            data = await r.json(content_type=None)
        token = str(data.get("access_token") or "")
        if not token:
            raise ValueError("Tidal login gave no token")
        self.tidal_token = (token, time.time() + max(60, int(data.get("expires_in") or 3600) - 60))
        return token
