"""Entry point: loads the token and settings and starts the bot."""

import json
import logging
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from guardbot.core import Bot, banner
from guardbot.logsetup import setup_logging


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
