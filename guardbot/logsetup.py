"""Logging: console and rotating file, in plain text or as one JSON object per line, with the server and command in every line."""

import contextvars
import json
import logging
import logging.handlers
import time
from pathlib import Path
from typing import Any, Optional

# set while a command or an event is handled, so every log line of it carries the server and the command
CONTEXT: contextvars.ContextVar[dict] = contextvars.ContextVar("guardbot_log_context", default={})

TEXT_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


class ContextFilter(logging.Filter):
    """Copies the server and command of the current context onto every record."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Add the fields, never drop a record."""
        ctx = CONTEXT.get()
        record.guild = ctx.get("guild")
        record.command = ctx.get("command")
        return True


class TextFormatter(logging.Formatter):
    """The classic line, with the server and command appended when there are any."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a record."""
        line = super().format(record)
        extra = [f"{k}={v}" for k, v in (("guild", getattr(record, "guild", None)), ("command", getattr(record, "command", None))) if v]
        if extra and "\n" not in line:
            line += " [" + " ".join(extra) + "]"
        return line


class JsonFormatter(logging.Formatter):
    """One JSON object per line: time, level, logger, message, guild, command and the error text."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a record."""
        data: dict[str, Any] = {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(record.created)) + time.strftime("%z", time.localtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key in ("guild", "command"):
            if getattr(record, key, None):
                data[key] = getattr(record, key)
        if record.exc_info:
            data["error"] = self.formatException(record.exc_info)
        return json.dumps(data, ensure_ascii=False)


def build_handlers(settings: dict) -> list[logging.Handler]:
    """The console handler and, unless log_file is false, the rotating file handler (log_max_mb and log_backups in settings.json)."""
    json_lines = str(settings.get("log_format", "text")).lower() == "json"
    formatter: logging.Formatter = JsonFormatter() if json_lines else TextFormatter(TEXT_FORMAT, "%Y-%m-%d %H:%M:%S")
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if settings.get("log_file", True):
        directory = Path(settings.get("data_dir", "data"))
        directory.mkdir(parents=True, exist_ok=True)
        size = int(float(settings.get("log_max_mb", 2)) * 1_000_000)
        handlers.append(logging.handlers.RotatingFileHandler(directory / "guardbot.log", maxBytes=size, backupCount=int(settings.get("log_backups", 3)), encoding="utf-8"))
    for handler in handlers:
        handler.setFormatter(formatter)
        handler.addFilter(ContextFilter())
    return handlers


def setup_logging(settings: dict, root: Optional[logging.Logger] = None) -> list[logging.Handler]:
    """Install the handlers on the root logger and set the level of the bot's own messages."""
    root = root or logging.getLogger()
    root.setLevel(logging.INFO)
    handlers = build_handlers(settings)
    for handler in handlers:
        root.addHandler(handler)
    level = str(settings.get("log_level", "INFO")).upper()
    logging.getLogger("guardbot").setLevel(getattr(logging, level, logging.INFO))
    return handlers
