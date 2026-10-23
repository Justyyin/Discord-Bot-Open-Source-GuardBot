"""Metrics in the Prometheus text format: latency, errors, memory, commands and the work lanes. Only counts, never names, IDs or message content."""

import math
import os
import time
from typing import Any

from . import __version__

BUCKETS = (0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)


def resident_bytes() -> int:
    """Memory of the process in bytes, 0 where it cannot be read."""
    try:
        with open("/proc/self/statm", encoding="ascii") as f:
            return int(f.read().split()[1]) * os.sysconf("SC_PAGE_SIZE")
    except (OSError, ValueError, IndexError, AttributeError):
        try:
            import resource
            return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        except (ImportError, OSError):
            return 0


class Metrics:
    """Counters that are filled while the bot runs: command durations and errors."""

    def __init__(self) -> None:
        """Start with empty counters."""
        self.durations: dict[str, list[float]] = {}  # command -> [bucket counts..., sum, count]
        self.errors = 0
        self.events = 0

    def observe(self, command: str, seconds: float) -> None:
        """Record how long a command took."""
        row = self.durations.setdefault(command, [0.0] * (len(BUCKETS) + 2))
        for i, bound in enumerate(BUCKETS):
            if seconds <= bound:
                row[i] += 1
        row[-2] += seconds
        row[-1] += 1

    def error(self) -> None:
        """Count one unexpected error."""
        self.errors += 1


def label(value: Any) -> str:
    """Escape a label value."""
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def usage_totals(bot: Any) -> dict[str, int]:
    """How often every command was used, summed over all servers. Servers are not listed."""
    out: dict[str, int] = {}
    for cfg in bot.store.config.values():
        for name, n in (cfg.get("debug", {}).get("usage", {}) or {}).items():
            out[name] = out.get(name, 0) + int(n)
    return out


def render(bot: Any) -> str:
    """The metrics as text."""
    latency = bot.latency
    lines: list[str] = []

    def metric(name: str, kind: str, help_text: str, samples: list[tuple[str, Any]]) -> None:
        lines.append(f"# HELP {name} {help_text}")
        lines.append(f"# TYPE {name} {kind}")
        for labels, value in samples:
            lines.append(f"{name}{labels} {value}")

    metric("guardbot_info", "gauge", "Version of GuardBot", [(f'{{version="{label(__version__)}"}}', 1)])
    metric("guardbot_up", "gauge", "1 when the bot is connected and ready", [("", 1 if bot.is_ready() else 0)])
    metric("guardbot_uptime_seconds", "gauge", "Seconds since the start", [("", int(time.time() - bot.started))])
    metric("guardbot_gateway_latency_seconds", "gauge", "Latency of the Discord gateway", [("", round(latency, 4) if not (math.isnan(latency) or math.isinf(latency)) else 0)])
    metric("guardbot_guilds", "gauge", "Servers the bot is on", [("", len(bot.guilds))])
    metric("guardbot_shards", "gauge", "Number of shards", [("", bot.shard_count or 1)])
    metric("guardbot_process_resident_memory_bytes", "gauge", "Memory of the process", [("", resident_bytes())])
    metric("guardbot_database_size_bytes", "gauge", "Size of the database file and its log", [("", bot.store.file_size())])
    metric("guardbot_cached_servers", "gauge", "Servers with settings in memory", [("", len(bot.store.config))])
    metric("guardbot_cached_users", "gauge", "User records in memory", [("", sum(len(v) for v in bot.store.user_data.values()))])
    metric("guardbot_cached_cases", "gauge", "Moderation cases in memory", [("", sum(len(v) for v in bot.store.case_data.values()))])
    metric("guardbot_errors_total", "counter", "Unexpected errors since the start", [("", bot.metrics.errors)])
    usage = usage_totals(bot)
    metric("guardbot_command_uses_total", "counter", "Uses of every command, all servers together", [(f'{{command="{label(k)}"}}', v) for k, v in sorted(usage.items())])
    samples: list[tuple[str, Any]] = []
    for command, row in sorted(bot.metrics.durations.items()):
        for i, bound in enumerate(BUCKETS):
            samples.append((f'_bucket{{command="{label(command)}",le="{bound}"}}', int(row[i])))
        samples.append((f'_bucket{{command="{label(command)}",le="+Inf"}}', int(row[-1])))
        samples.append((f'_sum{{command="{label(command)}"}}', round(row[-2], 4)))
        samples.append((f'_count{{command="{label(command)}"}}', int(row[-1])))
    lines.append("# HELP guardbot_command_duration_seconds Time commands took until they finished")
    lines.append("# TYPE guardbot_command_duration_seconds histogram")
    for suffix, value in samples:
        lines.append(f"guardbot_command_duration_seconds{suffix} {value}")
    for field, kind, text in (("running", "gauge", "Jobs running in the lane"), ("waiting", "gauge", "Jobs waiting in the lane"), ("done", "counter", "Jobs finished"),
                              ("failed", "counter", "Jobs that raised an error"), ("rejected", "counter", "Jobs refused because the lane was full"), ("seconds", "counter", "Seconds spent working")):
        suffix = "_total" if kind == "counter" else ""
        metric(f"guardbot_lane_{field}{suffix}", kind, text, [(f'{{lane="{lane}"}}', st[field]) for lane, st in bot.work.stats().items()])
    return "\n".join(lines) + "\n"
