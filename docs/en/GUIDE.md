# GuardBot: Setup guide

This guide shows how to run GuardBot on your own computer or on a VPS. It takes about 15 minutes.

> Beta: GuardBot and its dashboard are in a beta phase. They have not been tested thoroughly, especially not on large servers or against every situation on Discord. Expect bugs, keep backups of the data folder and report problems. Use at your own risk.

<!-- toc -->

- [Create the Discord bot](#create-the-discord-bot)
- [Run it on your computer](#run-it-on-your-computer)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux and macOS](#linux-and-macos)
- [Run it on a VPS](#run-it-on-a-vps)
- [Run it with Docker](#run-it-with-docker)
- [First steps in Discord](#first-steps-in-discord)
- [Structure, team and overview (1.5)](#structure-team-and-overview-15)
- [Updates and backups](#updates-and-backups)
- [Music (optional)](#music-optional)
- [Optional: reading images and languages](#optional-reading-images-and-languages)
- [Dashboard](#dashboard)
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
sudo apt install -y python3 python3-venv python3-pip git ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0
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
/server log set category:main channel:#logs
/access jailsetup setup
/automod toggle rule:phishing enabled:True action:jail
/automod toggle rule:words enabled:True
/automod add name:words value:example
/security raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3
/security antinuke setup enabled:True action:strip
/access verify setup channel:#verify mode:captcha timeout_minutes:30
/community welcome set channel:#welcome message:Welcome {user} to {server}!
/server backup schedule enabled:True interval_hours:24 keep:7
/xp config enabled:True
/admin module list
```

Every feature is described in the command reference: [COMMANDS.md](../COMMANDS.md).

## Structure, team and overview (1.5)

These steps set up the newer features. Each one can be turned off with /admin module, and the prefix and texts stay editable per server.

1. See what is configured: `/admin module overview` lists every module with its state and whether it is set up. The dashboard shows the same in its setup panel.
2. Find a command: `/info find text:ban` searches all commands by word, `/help` shows the groups.
3. Publish rules with an accept button: `/structure rules setup`, then `/structure rules add`, then `/structure rules post`. Members who have not accepted a new version are reminded every few hours.
4. Tell the bot who is staff: `/team duty roster`. Lists of available staff and the routing of tickets and alerts use it.
5. Tidy up idle channels: `/structure archive setup`, then `/structure archive scan`.
6. Give returning members their roles back: `/members stickyroles setup`.
7. Keep names readable: `/members nickname setup`, test with `/members nickname check` before `/members nickname scan`.
8. Before big changes export the settings with `/admin config export`, and check roles and channels with `/server diagnose`.

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

## Music (optional)

The music module needs ffmpeg on the computer that runs the bot. Put your own music into the folder music/ as Artist/Album/01 - Title.flac, or allow downloads. The folder can grow large, so keep it on a disk with space or in a Docker volume.

```
# Windows
winget install Gyan.FFmpeg
# macOS
brew install ffmpeg
# Ubuntu or Debian
sudo apt install -y ffmpeg libopus0

# in Discord
/admin module enable name:music
/music settings allow_download:True
```

## Optional: reading images and languages

To let the anti-scam module read text in images, install tesseract on the computer that runs the bot (the Docker image already contains it). Then check with /security antiscam status that it is ready. Choose the language of the messages that members see with /admin language.

```
# Ubuntu or Debian
sudo apt install -y tesseract-ocr
# macOS
brew install tesseract
# Windows
winget install UB-Mannheim.TesseractOCR

# in Discord
/security antiscam status
/admin language code:de
```

## Dashboard

The dashboard is a web page that runs inside the bot. After you sign in with Discord you can change the settings of your servers with switches, menus and fields instead of commands: modules, channels, roles, thresholds, texts, the prefix and the language. It also shows the latest moderation cases and exports and imports settings. It works the same on your own computer and on a VPS, and it is off until you turn it on.

1. Open your application in the Developer Portal, go to OAuth2 and copy the Client Secret into the file .env.
2. On the same page add the redirect address http://localhost:8080/callback.
3. Turn the dashboard on in settings.json.
4. Restart the bot and open http://localhost:8080 in your browser. Sign in with Discord.

```
DISCORD_TOKEN=your-bot-token
DISCORD_CLIENT_SECRET=your-oauth2-client-secret
```

```json
{
  "dashboard": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 8080,
    "public_url": "http://localhost:8080"
  }
}
```

Keep host at 127.0.0.1 and choose one of two ways. First, an SSH tunnel: nothing is exposed, you open http://localhost:8080 on your computer while the tunnel runs.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Second, HTTPS through a reverse proxy such as Caddy, which gets a certificate on its own (see deploy/Caddyfile.example). Then set public_url to your https address, add https://your-address/callback as redirect in the Developer Portal and set trust_proxy to true:

```
dashboard.example.com {
	reverse_proxy 127.0.0.1:8080
}
```

```json
{
  "dashboard": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 8080,
    "public_url": "https://dashboard.example.com",
    "trust_proxy": true
  }
}
```

## Troubleshooting

- Slash commands do not appear: wait a few minutes, restart Discord and check that the bot was invited with the applications.commands scope.
- The bot stops with a privileged intents error: turn on Server Members Intent and Message Content Intent in the Developer Portal.
- Improper token: copy the token again and make sure .env contains DISCORD_TOKEN=token without spaces or quotes.
- I cannot assign that role: move the role of the bot above the role it should manage.
- Nothing is logged: set a channel with /server log set and make sure the bot can send messages, embed links and attach files there.
- Unknown timezone: run pip install tzdata and restart the bot.
- Something fails without a visible reason: errors and warnings are written to the console. On a VPS read them with journalctl -u guardbot -f.

## Support

Bugs, ideas and suggestions: Discord @justyyin or a GitHub issue.

Copyright (c) Justyn - made in Germany
