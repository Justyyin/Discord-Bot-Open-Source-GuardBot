"""Safe resolution of shortened links: follows redirects without ever contacting private addresses."""

import asyncio
import ipaddress
import logging
import socket
import time
from urllib.parse import urljoin, urlparse

import aiohttp
from aiohttp.abc import AbstractResolver

log = logging.getLogger(__name__)

REDIRECTS = (301, 302, 303, 307, 308)
ALLOWED_PORTS = (None, 80, 443)
CACHE_SECONDS = 600
CACHE_LIMIT = 500


def is_public(address):
    """True if an IP address is globally routable. Private, loopback, link-local and reserved ranges are not."""
    try:
        return ipaddress.ip_address(address).is_global
    except ValueError:
        return False


def host_of(url):
    """Return the lower case host name of a URL, or None."""
    try:
        return (urlparse(url if "://" in url else "//" + url).hostname or "").lower() or None
    except ValueError:
        return None


class SafeResolver(AbstractResolver):
    """DNS resolver that drops every non-public address, so the connection can only go to the internet."""

    async def resolve(self, host, port=0, family=socket.AF_INET):
        """Resolve a host and keep only public addresses. Raises OSError when none is left."""
        loop = asyncio.get_running_loop()
        infos = await loop.getaddrinfo(host, port, family=family, type=socket.SOCK_STREAM)
        out = [
            {"hostname": host, "host": info[4][0], "port": port, "family": info[0], "proto": 0, "flags": socket.AI_NUMERICHOST}
            for info in infos
            if is_public(info[4][0])
        ]
        if not out:
            raise OSError(f"{host} does not resolve to a public address")
        return out

    async def close(self):
        """Nothing to release."""
        return None


def make_session():
    """Create an HTTP session that can only reach public addresses and ignores proxy environment variables."""
    connector = aiohttp.TCPConnector(resolver=SafeResolver(), use_dns_cache=False, limit=10)
    return aiohttp.ClientSession(connector=connector, trust_env=False, headers={"User-Agent": "Mozilla/5.0 (compatible; GuardBot link check)"})


class Resolver:
    """Follows redirects of a URL step by step and caches the result for a few minutes."""

    def __init__(self, session=None):
        """Use the given session or create one on first use."""
        self.session = session
        self.cache = {}

    async def close(self):
        """Close the session if this object created it."""
        if self.session is not None:
            await self.session.close()
            self.session = None

    def remember(self, url, result):
        """Store a result and drop the oldest entries when the cache is full."""
        if len(self.cache) >= CACHE_LIMIT:
            for key in sorted(self.cache, key=lambda k: self.cache[k][0])[: CACHE_LIMIT // 5]:
                del self.cache[key]
        self.cache[url] = (time.time(), result)

    async def final_url(self, url, hops=4, timeout=4):
        """Return the URL a link leads to after its redirects, or None when it cannot be followed safely."""
        hit = self.cache.get(url)
        if hit and time.time() - hit[0] < CACHE_SECONDS:
            return hit[1]
        result = await self._follow(url if "://" in url else "https://" + url, hops, timeout)
        self.remember(url, result)
        return result

    async def _follow(self, url, hops, timeout):
        """Follow up to a number of redirects. Each step is checked before it is requested."""
        if self.session is None:
            self.session = make_session()
        for _ in range(hops + 1):
            parsed = urlparse(url)
            host = (parsed.hostname or "").lower()
            if parsed.scheme not in ("http", "https") or not host or parsed.port not in ALLOWED_PORTS:
                return None
            try:
                ipaddress.ip_address(host)
            except ValueError:
                pass
            else:
                if not is_public(host):
                    return None
            location = await self._peek(url, timeout)
            if location is None:
                return url
            if location is False:
                return None
            url = urljoin(url, location)
        return url

    async def _peek(self, url, timeout):
        """Request one URL without following redirects. Returns the Location header, None for a final page, False on failure."""
        wait = aiohttp.ClientTimeout(total=timeout)
        for method in ("HEAD", "GET"):
            try:
                async with self.session.request(method, url, allow_redirects=False, timeout=wait) as resp:
                    if resp.status in REDIRECTS and resp.headers.get("Location"):
                        return resp.headers["Location"]
                    if resp.status in (403, 405, 501) and method == "HEAD":
                        continue
                    return None
            except (aiohttp.ClientError, asyncio.TimeoutError, OSError, ValueError) as exc:
                log.info("link check failed for %s: %s", host_of(url), exc)
                return False
        return None


def url_problem(url, allowed=(), blocked=()):
    """Return why a link may not be opened by the bot (scheme, private address, host lists), or None."""
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        port = parsed.port
    except ValueError:
        return "invalid link"
    if parsed.scheme not in ("http", "https") or not host:
        return "only http and https links are supported"
    if port not in ALLOWED_PORTS:
        return "this port is not allowed"
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        if not is_public(host):
            return "private addresses are not allowed"
    if host == "localhost" or host.endswith((".local", ".internal", ".localhost")):
        return "local addresses are not allowed"
    if any(host == b.lower() or host.endswith("." + b.lower()) for b in blocked):
        return "this site is blocked"
    if allowed and not any(host == a.lower() or host.endswith("." + a.lower()) for a in allowed):
        return "this site is not on the allowed list"
    return None


async def public_host(host):
    """True if every address a host name resolves to is public. Hosts that do not resolve count as not public."""
    try:
        ipaddress.ip_address(host)
        return is_public(host)
    except ValueError:
        pass
    try:
        infos = await asyncio.get_running_loop().getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except OSError:
        return False
    return bool(infos) and all(is_public(info[4][0]) for info in infos)
