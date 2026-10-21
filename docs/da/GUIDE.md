# GuardBot: Installationsvejledning

Denne vejledning viser, hvordan du kører GuardBot på din egen computer eller på en VPS. Det tager cirka 15 minutter.

<!-- toc -->

- [Opret Discord-botten](#opret-discord-botten)
- [Kør den på din egen computer](#kør-den-på-din-egen-computer)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux og macOS](#linux-og-macos)
- [Kør den på en VPS](#kør-den-på-en-vps)
- [Kør den med Docker](#kør-den-med-docker)
- [Første skridt i Discord](#første-skridt-i-discord)
- [Opdateringer og backup](#opdateringer-og-backup)
- [Fejlfinding](#fejlfinding)
- [Support](#support)

<!-- tocstop -->

## Opret Discord-botten

1. Åbn [Discord Developer Portal](https://discord.com/developers/applications) og klik på New Application.
2. Åbn fanen Bot og klik på Reset Token. Kopiér tokenet og hold det hemmeligt.
3. Slå Server Members Intent og Message Content Intent til på samme fane.
4. Åbn OAuth2, URL Generator. Vælg scopes bot og applications.commands.
5. Vælg tilladelser: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, View Audit Log, Manage Messages, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Move Members. Administrator virker også og er det nemmeste valg.
6. Åbn den genererede webadresse og tilføj botten til din server.
7. Flyt botens rolle øverst på rollelisten i serverindstillingerne. Botten kan kun administrere roller, der ligger under dens egen rolle.

Du kan også bruge denne invitationsadresse. Erstat YOUR_CLIENT_ID med Application ID fra Developer Portal:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## Kør den på din egen computer

Installér Python 3.11 eller nyere og Git, og kør derefter disse kommandoer i en terminal.

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

### Linux og macOS

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

Åbn filen .env og erstat pladsholderen med dit bot-token. Botten er online, så snart konsollen viser linjen, der starter med online as. Lad vinduet være åbent, botten stopper, når du lukker det.

## Kør den på en VPS

Disse kommandoer gælder for Ubuntu eller Debian og opsætter botten som en tjeneste, der starter automatisk.

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

Tjek status med systemctl status guardbot. Loggen viser linjen, der starter med online as, når botten er klar.

## Kør den med Docker

Docker er valgfrit. Opret først filen .env og kør derefter:

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## Første skridt i Discord

Brug disse kommandoer på din server og erstat kanalnavnene med dine egne.

```
/log set category:main channel:#logs
/jailsetup setup
/automod toggle rule:phishing enabled:True action:jail
/automod toggle rule:words enabled:True
/automod add name:words value:example
/raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3
/antinuke setup enabled:True action:strip
/verify setup channel:#verify mode:captcha timeout_minutes:30
/welcome set channel:#welcome message:Welcome {user} to {server}!
/backup schedule enabled:True interval_hours:24 keep:7
/xp config enabled:True
/module list
```

Alle funktioner er beskrevet i kommandoreferencen: [COMMANDS.md](../COMMANDS.md).

## Opdateringer og backup

Opdatér botten:

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

Tag backup af dine indstillinger ved at kopiere mappen data, for eksempel:

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## Fejlfinding

- Skråstregskommandoer vises ikke: vent nogle minutter, genstart Discord og tjek, at botten blev inviteret med scope applications.commands.
- Botten stopper med en fejl om privilegerede intents: slå Server Members Intent og Message Content Intent til i Developer Portal.
- Improper token: kopiér tokenet igen og tjek, at .env indeholder præcis DISCORD_TOKEN=token, uden mellemrum eller citationstegn.
- I cannot assign that role: flyt botens rolle over den rolle, den skal administrere.
- Intet bliver logget: angiv en kanal med /log set og tjek, at botten kan sende beskeder, indlejre links og vedhæfte filer der.
- Unknown timezone: kør pip install tzdata og genstart botten.
- Noget fejler uden synlig årsag: fejl og advarsler skrives til konsollen. På en VPS læser du dem med journalctl -u guardbot -f.

## Support

Fejl, idéer og forslag: Discord @justyyin eller et GitHub-issue.

Copyright (c) Justyn - made in Germany
