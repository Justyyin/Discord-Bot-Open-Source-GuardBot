# GuardBot: Installationsguide

Den här guiden visar hur du kör GuardBot på din egen dator eller på en VPS. Det tar cirka 15 minuter.

<!-- toc -->

- [Skapa Discord-boten](#skapa-discord-boten)
- [Köra på din egen dator](#köra-på-din-egen-dator)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux och macOS](#linux-och-macos)
- [Köra på en VPS](#köra-på-en-vps)
- [Köra med Docker](#köra-med-docker)
- [Första stegen i Discord](#första-stegen-i-discord)
- [Uppdateringar och säkerhetskopior](#uppdateringar-och-säkerhetskopior)
- [Felsökning](#felsökning)
- [Support](#support)

<!-- tocstop -->

## Skapa Discord-boten

1. Öppna [Discord Developer Portal](https://discord.com/developers/applications) och klicka på New Application.
2. Öppna fliken Bot och klicka på Reset Token. Kopiera token och håll den hemlig.
3. Aktivera Server Members Intent och Message Content Intent på samma flik.
4. Öppna OAuth2, URL Generator. Välj scopes bot och applications.commands.
5. Välj behörigheter: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, View Audit Log, Manage Messages, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Move Members. Administrator fungerar också och är det enklaste valet.
6. Öppna den skapade webbadressen och lägg till boten på din server.
7. Flytta botens roll högst upp i rollistan i serverinställningarna. Boten kan bara hantera roller som ligger under dess egen roll.

Du kan också använda den här inbjudningsadressen. Ersätt YOUR_CLIENT_ID med Application ID från Developer Portal:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## Köra på din egen dator

Installera Python 3.11 eller senare och Git och kör sedan dessa kommandon i en terminal.

### Windows (PowerShell)

```powershell
git clone https://github.com/YOUR-NAME/guardbot.git
cd guardbot
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
python main.py
```

### Linux och macOS

```bash
git clone https://github.com/YOUR-NAME/guardbot.git
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
```

Öppna filen .env och ersätt platshållaren med din bot-token. Boten är online så snart konsolen visar raden som börjar med online as. Låt fönstret vara öppet, boten stoppas när du stänger det.

## Köra på en VPS

Dessa kommandon gäller Ubuntu eller Debian och ställer in boten som en tjänst som startar automatiskt.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
sudo git clone https://github.com/YOUR-NAME/guardbot.git /opt/guardbot
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

Kontrollera status med systemctl status guardbot. Loggen visar raden som börjar med online as när boten är redo.

## Köra med Docker

Docker är valfritt. Skapa först filen .env och kör sedan:

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## Första stegen i Discord

Använd dessa kommandon på din server och byt ut kanalnamnen mot dina egna.

```
/log set category:main channel:#logs
/jailsetup setup
/automod toggle rule:phishing enabled:True action:jail
/automod toggle rule:words enabled:True
/automod add name:words value:example
/raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3
/antinuke setup enabled:True action:strip
/xp config enabled:True
/module list
```

Alla funktioner beskrivs i kommandoreferensen: [COMMANDS.md](../COMMANDS.md).

## Uppdateringar och säkerhetskopior

Uppdatera boten:

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

Säkerhetskopiera dina inställningar genom att kopiera mappen data, till exempel:

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## Felsökning

- Snedstreckskommandon visas inte: vänta några minuter, starta om Discord och kontrollera att boten bjöds in med scope applications.commands.
- Boten stoppar med ett fel om privilegierade intents: aktivera Server Members Intent och Message Content Intent i Developer Portal.
- Improper token: kopiera token igen och kontrollera att .env innehåller exakt DISCORD_TOKEN=token, utan mellanslag eller citattecken.
- I cannot assign that role: flytta botens roll ovanför rollen den ska hantera.
- Inget loggas: ange en kanal med /log set och kontrollera att boten kan skicka meddelanden, bädda in länkar och bifoga filer där.
- Unknown timezone: kör pip install tzdata och starta om boten.

## Support

Buggar, idéer och förslag: Discord @justyyin eller ett GitHub-issue.

Copyright (c) Justyn - made in Germany

<!-- GuardBot (c) Justyn -->
