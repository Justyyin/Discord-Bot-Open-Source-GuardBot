"""Entry point: loads the token and settings and starts the bot."""

import json
import logging
import logging.handlers
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from guardbot.core import Bot, banner


def setup_logging(settings):
    """Log to the console and to a rotating file (data/guardbot.log, 2 MB, 3 old files)."""
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    handlers = [logging.StreamHandler()]
    if settings.get("log_file", True):
        directory = Path(settings.get("data_dir", "data"))
        directory.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.handlers.RotatingFileHandler(directory / "guardbot.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8"))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    for handler in handlers:
        handler.setFormatter(fmt)
        root.addHandler(handler)
    level = str(settings.get("log_level", "INFO")).upper()
    logging.getLogger("guardbot").setLevel(getattr(logging, level, logging.INFO))


def main():
    """Read the token and settings, then start the bot."""
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        sys.exit("DISCORD_TOKEN is missing. Copy .env.example to .env and enter your bot token.")
    settings = {}
    path = Path("settings.json")
    if path.exists():
        settings = json.loads(path.read_text(encoding="utf-8"))
    print(banner())
    setup_logging(settings)
    bot = Bot(settings)
    bot.run(token, log_handler=None)
    if bot.restart_requested:
        logging.shutdown()
        if os.name == "nt":
            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit(0)
        os.execv(sys.executable, [sys.executable] + sys.argv)


if __name__ == "__main__":
    main()
