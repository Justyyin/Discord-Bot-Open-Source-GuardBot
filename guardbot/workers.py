"""Lanes for heavy work that must not block the bot: reading images, drawing cards, music files, backups.

Every lane has a fixed number of threads and a limit for running plus waiting jobs. A job that does not fit is
refused at once with Busy, so a flood of work can slow down one lane but never fills the memory or the thread pool.
"""

import asyncio
import functools
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Optional

# lane: (threads, jobs allowed at once including the waiting ones)
DEFAULT_LANES: dict[str, tuple[int, int]] = {
    "ocr": (2, 20),
    "image": (2, 20),
    "music": (2, 8),
    "maintenance": (1, 4),
}


class Busy(Exception):
    """Raised when a lane is full."""

    def __init__(self, lane: str) -> None:
        """Remember which lane was full."""
        super().__init__(f"the {lane} lane is busy")
        self.lane = lane


class Lane:
    """One kind of heavy work with its own threads and its own limit."""

    def __init__(self, name: str, threads: Any, limit: Any) -> None:
        """Create the thread pool and the counters."""
        self.name, self.threads, self.limit = name, max(1, int(threads)), max(1, int(limit))
        self.executor = ThreadPoolExecutor(max_workers=self.threads, thread_name_prefix=f"gb-{name}")
        self.sem = asyncio.Semaphore(self.threads)
        self.waiting = self.running = self.done = self.rejected = self.failed = 0
        self.seconds = 0.0

    @property
    def load(self) -> int:
        """Jobs that are running or waiting."""
        return self.waiting + self.running

    def stats(self) -> dict[str, Any]:
        """Counters of the lane."""
        return {"threads": self.threads, "limit": self.limit, "running": self.running, "waiting": self.waiting,
                "done": self.done, "failed": self.failed, "rejected": self.rejected, "seconds": round(self.seconds, 3)}


class Workers:
    """All lanes of the bot. Sizes can be changed in settings.json under "workers", for example {"ocr": {"threads": 1, "limit": 10}}."""

    def __init__(self, settings: Optional[dict] = None) -> None:
        """Build the lanes from the defaults and the settings."""
        custom = (settings or {}).get("workers", {}) or {}
        self.lanes: dict[str, Lane] = {}
        for name, (threads, limit) in DEFAULT_LANES.items():
            c = custom.get(name, {}) if isinstance(custom.get(name, {}), dict) else {}
            self.lanes[name] = Lane(name, c.get("threads", threads), c.get("limit", limit))

    async def run(self, lane: str, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Run fn(*args) in a thread of the lane. Raises Busy when the lane is full."""
        ln = self.lanes[lane]
        if ln.load >= ln.limit:
            ln.rejected += 1
            raise Busy(lane)
        ln.waiting += 1
        queued = True
        try:
            async with ln.sem:
                ln.waiting -= 1
                queued = False
                ln.running += 1
                start = time.perf_counter()
                try:
                    return await asyncio.get_running_loop().run_in_executor(ln.executor, functools.partial(fn, *args, **kwargs))
                except BaseException:
                    ln.failed += 1
                    raise
                finally:
                    ln.running -= 1
                    ln.seconds += time.perf_counter() - start
                    ln.done += 1
        finally:
            if queued:
                ln.waiting -= 1

    def stats(self) -> dict[str, dict[str, Any]]:
        """Counters of every lane."""
        return {name: lane.stats() for name, lane in self.lanes.items()}

    def close(self) -> None:
        """Stop the threads once their jobs are done."""
        for lane in self.lanes.values():
            lane.executor.shutdown(wait=False, cancel_futures=True)
