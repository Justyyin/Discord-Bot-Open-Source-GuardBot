# GuardBot: Setup guide

This guide shows how to run GuardBot on your own computer or on a VPS. It takes about 15 minutes.

<!-- toc -->

- [Create the Discord bot](#create-the-discord-bot)
- [Run it on your computer](#run-it-on-your-computer)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux and macOS](#linux-and-macos)
- [Run it on a VPS](#run-it-on-a-vps)
- [Run it with Docker](#run-it-with-docker)
- [First steps in Discord](#first-steps-in-discord)
- [Updates and backups](#updates-and-backups)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

<!-- tocstop -->

## Create the Discord bot

1. Open the [Discord Developer Portal](https://discord.com/developers/applications) and click New Application.
2. Open the Bot tab and click Reset Token. Copy the token and keep it secret.
3. On the same tab, turn on Server Members Intent and Message Content Intent.
4. Open OAuth2, URL Generator. Select the scopes bot and applications.commands.
5. Select the permissions: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, View Audit Log, Manage Messages, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Move Members. Administrator also works and is the simplest choice.
6. Open the generated URL and add the bot to your server.
7. In the server settings, move the role of the bot to the top of the role list. The bot can only manage roles below its own role.

Alternatively, use this invite URL. Replace YOUR_CLIENT_ID with the Application ID from the Developer Portal:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## Run it on your computer

Install Python 3.11 or newer and Git, then run these commands in a terminal.

### Windows (PowerShell)

```powershell
git clone <REPOSITORY_URL>
cd guardbot
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
python main.py
```

### Linux and macOS

```bash
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
```

Open .env and replace the placeholder with your bot token. The bot is online as soon as the console shows the line starting with online as. Keep the window open, the bot stops when you close it.

## Run it on a VPS

These commands are for Ubuntu or Debian and set up the bot as a service that starts automatically.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
sudo git clone <REPOSITORY_URL> /opt/guardbot
sudo useradd --system --no-create-home --shell /usr/sbin/nologin guardbot
cd /opt/guardbot
sudo python3 -m venv .venv
sudo .venv/bin/pip install -r requirements.txt
sudo cp .env.example .env
sudo nano .env
sudo mkdir -p data
sudo chown -R guardbot:guardbot /opt/guardbot
sudo chmod 600 .env
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now guardbot
sudo journalctl -u guardbot -f
```

Check the status with systemctl status guardbot. The log shows the line starting with online as when the bot is ready.

## Run it with Docker

Docker is optional. Create the .env file first, then run:

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## First steps in Discord

Use these commands in your server and replace the channel names with your own.

```
/log set category:main channel:#logs
/jailsetup setup
/automod toggle rule:phishing enabled:True action:jail
/automod toggle rule:words enabled:True
/automod add name:words value:example
/raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3
/antinuke setup enabled:True action:strip
/verify setup channel:#verify mode:captcha timeout_minutes:30
/backup schedule enabled:True interval_hours:24 keep:7
/xp config enabled:True
/module list
```

Every feature is described in the command reference: [COMMANDS.md](../COMMANDS.md).

## Updates and backups

Update the bot:

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

Back up your settings by copying the data folder, for example:

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## Troubleshooting

- Slash commands do not appear: wait a few minutes, restart Discord and check that the bot was invited with the applications.commands scope.
- The bot stops with a privileged intents error: turn on Server Members Intent and Message Content Intent in the Developer Portal.
- Improper token: copy the token again and make sure .env contains DISCORD_TOKEN=token without spaces or quotes.
- I cannot assign that role: move the role of the bot above the role it should manage.
- Nothing is logged: set a channel with /log set and make sure the bot can send messages, embed links and attach files there.
- Unknown timezone: run pip install tzdata and restart the bot.
- Something fails without a visible reason: errors and warnings are written to the console. On a VPS read them with journalctl -u guardbot -f.

## Support

Bugs, ideas and suggestions: Discord @justyyin or a GitHub issue.

Copyright (c) Justyn - made in Germany
