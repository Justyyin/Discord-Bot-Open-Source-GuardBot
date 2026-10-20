"""Entry point: loads the token and settings and starts the bot."""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from guardbot.core import Bot, banner


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
    Bot(settings).run(token)


if __name__ == "__main__":
    main()
