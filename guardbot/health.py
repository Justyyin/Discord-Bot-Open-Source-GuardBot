"""Heartbeat file and an optional local status page for monitoring."""

import logging
import math
import os
import time
from pathlib import Path
from typing import Any, Optional, Union

from aiohttp import web

from . import __version__, metrics

log = logging.getLogger(__name__)

STALE_SECONDS = 120


def snapshot(bot: Any) -> dict[str, Any]:
    """Collect the status of the bot. Contains only counts, never names or IDs."""
    latency = bot.latency
    ready = bot.is_ready()
    ok = ready and not math.isnan(latency) and not math.isinf(latency) and latency < 5
    return {
        "status": "ok" if ok else "degraded",
        "version": __version__,
        "ready": ready,
        "uptime_seconds": int(time.time() - bot.started),
        "latency_ms": round(latency * 1000) if not (math.isnan(latency) or math.isinf(latency)) else None,
        "servers": len(bot.guilds),
        "shards": bot.shard_count or 1,
    }


def write_heartbeat(path: Union[str, Path]) -> None:
    """Write the current time to a file, atomically. Docker and monitoring can check that it is recent."""
    path = Path(path)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(str(int(time.time())), encoding="utf-8")
    os.replace(tmp, path)


def heartbeat_fresh(path: Union[str, Path], now: Optional[float] = None) -> bool:
    """True if the heartbeat file was written in the last two minutes."""
    try:
        return (now or time.time()) - int(Path(path).read_text(encoding="utf-8")) < STALE_SECONDS
    except (OSError, ValueError):
        return False


class StatusServer:
    """Serves /health as JSON and /metrics in the Prometheus format. Off unless health_port is set in settings.json, and only on localhost unless health_host says otherwise."""

    def __init__(self, bot: Any) -> None:
        """Remember the bot."""
        self.bot = bot
        self.runner: Any = None

    async def handle(self, request: Any) -> Any:
        """Answer with the status. HTTP 503 when the bot is not healthy, so monitoring tools can react."""
        data = snapshot(self.bot)
        return web.json_response(data, status=200 if data["status"] == "ok" else 503)

    async def metrics_page(self, request: Any) -> Any:
        """Metrics in the Prometheus format. When metrics_token is set in settings.json, the request needs it as a bearer token."""
        token = str(self.bot.settings.get("metrics_token", "") or "")
        if token and request.headers.get("Authorization", "") != f"Bearer {token}":
            return web.Response(status=401, text="unauthorized\n")
        return web.Response(text=metrics.render(self.bot), content_type="text/plain", charset="utf-8")

    async def start(self) -> None:
        """Start listening if a port is configured."""
        port = int(self.bot.settings.get("health_port", 0) or 0)
        if not port:
            return
        host = self.bot.settings.get("health_host", "127.0.0.1")
        app = web.Application()
        app.router.add_get("/health", self.handle)
        if self.bot.settings.get("metrics", True):
            app.router.add_get("/metrics", self.metrics_page)
        self.runner = web.AppRunner(app, access_log=None)
        await self.runner.setup()
        await web.TCPSite(self.runner, host, port).start()
        log.info("status page on http://%s:%d/health", host, port)

    async def stop(self) -> None:
        """Stop listening."""
        if self.runner:
            await self.runner.cleanup()
            self.runner = None
