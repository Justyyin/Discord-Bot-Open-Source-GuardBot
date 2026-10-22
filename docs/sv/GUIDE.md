# GuardBot: Installationsguide

Den här guiden visar hur du kör GuardBot på din egen dator eller på en VPS. Det tar cirka 15 minuter.

> Beta: GuardBot och dess kontrollpanel är i en betafas. De har inte testats grundligt, särskilt inte på stora servrar eller i alla situationer på Discord. Räkna med buggar, säkerhetskopiera mappen data och rapportera problem. Användning på egen risk.

<!-- toc -->

- [Skapa Discord-boten](#skapa-discord-boten)
- [Köra på din egen dator](#köra-på-din-egen-dator)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux och macOS](#linux-och-macos)
- [Köra på en VPS](#köra-på-en-vps)
- [Köra med Docker](#köra-med-docker)
- [Första stegen i Discord](#första-stegen-i-discord)
- [Uppdateringar och säkerhetskopior](#uppdateringar-och-säkerhetskopior)
- [Musik (valfritt)](#musik-valfritt)
- [Valfritt: läsa bilder och språk](#valfritt-läsa-bilder-och-språk)
- [Kontrollpanel](#kontrollpanel)
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
git clone <REPOSITORY_URL>
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
git clone <REPOSITORY_URL>
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

## Musik (valfritt)

Musikmodulen behöver ffmpeg på datorn som kör boten. Lägg din egen musik i mappen music/ som Artist/Album/01 - Titel.flac, eller tillåt nedladdningar. Mappen kan bli stor, så ha den på en disk med utrymme eller i en Docker-volym.

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

## Valfritt: läsa bilder och språk

För att anti-bedrägerimodulen ska läsa text i bilder, installera tesseract på datorn som kör boten (Docker-avbilden innehåller det redan). Kontrollera sedan med /security antiscam status att det är redo. Välj språk för de meddelanden medlemmarna ser med /admin language.

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

## Kontrollpanel

Kontrollpanelen är en webbsida som körs inuti boten. Efter inloggning med Discord ändrar du inställningarna för dina servrar med reglage, menyer och fält i stället för kommandon: moduler, kanaler, roller, tröskelvärden, texter, prefixet och språket. Den visar också de senaste moderationsärendena samt exporterar och importerar inställningar. Den fungerar likadant på din egen dator och på en VPS och är avstängd tills du slår på den.

1. Öppna din applikation i Developer Portal, gå till OAuth2 och kopiera Client Secret till filen .env.
2. Lägg till omdirigeringsadressen http://localhost:8080/callback på samma sida.
3. Slå på kontrollpanelen i settings.json.
4. Starta om boten och öppna http://localhost:8080 i webbläsaren. Logga in med Discord.

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

Låt host vara 127.0.0.1 och välj en av två vägar. Först en SSH-tunnel: ingenting exponeras och du öppnar http://localhost:8080 på din dator medan tunneln körs.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Sedan HTTPS via en omvänd proxy som Caddy, som skaffar ett certifikat själv (se deploy/Caddyfile.example). Sätt då public_url till din https-adress, lägg till https://din-adress/callback som omdirigering i Developer Portal och sätt trust_proxy till true:

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

## Felsökning

- Snedstreckskommandon visas inte: vänta några minuter, starta om Discord och kontrollera att boten bjöds in med scope applications.commands.
- Boten stoppar med ett fel om privilegierade intents: aktivera Server Members Intent och Message Content Intent i Developer Portal.
- Improper token: kopiera token igen och kontrollera att .env innehåller exakt DISCORD_TOKEN=token, utan mellanslag eller citattecken.
- I cannot assign that role: flytta botens roll ovanför rollen den ska hantera.
- Inget loggas: ange en kanal med /server log set och kontrollera att boten kan skicka meddelanden, bädda in länkar och bifoga filer där.
- Unknown timezone: kör pip install tzdata och starta om boten.
- Något misslyckas utan synlig orsak: fel och varningar skrivs till konsolen. På en VPS läser du dem med journalctl -u guardbot -f.

## Support

Buggar, idéer och förslag: Discord @justyyin eller ett GitHub-issue.

Copyright (c) Justyn - made in Germany
