# GuardBot: Einrichtungsanleitung

Diese Anleitung zeigt, wie du GuardBot auf deinem eigenen Computer oder auf einem VPS betreibst. Du brauchst etwa 15 Minuten.

> Beta: GuardBot und sein Dashboard befinden sich in einer Beta-Phase. Sie wurden nicht gründlich getestet, vor allem nicht auf großen Servern und nicht in jeder Situation auf Discord. Rechne mit Fehlern, sichere den Ordner data regelmäßig und melde Probleme. Nutzung auf eigene Gefahr.

<!-- toc -->

- [Discord-Bot erstellen](#discord-bot-erstellen)
- [Auf dem eigenen Computer betreiben](#auf-dem-eigenen-computer-betreiben)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux und macOS](#linux-und-macos)
- [Auf einem VPS betreiben](#auf-einem-vps-betreiben)
- [Mit Docker betreiben](#mit-docker-betreiben)
- [Erste Schritte in Discord](#erste-schritte-in-discord)
- [Struktur, Team und Übersicht (1.5)](#struktur-team-und-übersicht-15)
- [Updates und Backups](#updates-und-backups)
- [Musik (optional)](#musik-optional)
- [Optional: Bilder lesen und Sprachen](#optional-bilder-lesen-und-sprachen)
- [Dashboard](#dashboard)
- [Fehlerbehebung](#fehlerbehebung)
- [Support](#support)

<!-- tocstop -->

## Discord-Bot erstellen

1. Öffne das [Discord Developer Portal](https://discord.com/developers/applications) und klicke auf New Application.
2. Öffne den Tab Bot und klicke auf Reset Token. Kopiere den Token und halte ihn geheim.
3. Aktiviere auf demselben Tab Server Members Intent und Message Content Intent.
4. Öffne OAuth2, URL Generator. Wähle die Scopes bot und applications.commands.
5. Wähle die Berechtigungen: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, View Audit Log, Manage Messages, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Move Members. Administrator funktioniert ebenfalls und ist die einfachste Wahl.
6. Öffne die erzeugte URL und füge den Bot deinem Server hinzu.
7. Schiebe in den Servereinstellungen die Rolle des Bots ganz nach oben in der Rollenliste. Der Bot kann nur Rollen verwalten, die unter seiner eigenen Rolle liegen.

Alternativ kannst du diese Einladungs-URL verwenden. Ersetze YOUR_CLIENT_ID durch die Application ID aus dem Developer Portal:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## Auf dem eigenen Computer betreiben

Installiere Python 3.11 oder neuer und Git und führe dann diese Befehle in einem Terminal aus.

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

### Linux und macOS

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

Öffne die Datei .env und ersetze den Platzhalter durch deinen Bot-Token. Der Bot ist online, sobald die Konsole die Zeile mit online as anzeigt. Lass das Fenster geöffnet, der Bot stoppt, wenn du es schließt.

## Auf einem VPS betreiben

Diese Befehle gelten für Ubuntu oder Debian und richten den Bot als Dienst ein, der automatisch startet.

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

Den Status prüfst du mit systemctl status guardbot. Im Log erscheint die Zeile mit online as, sobald der Bot bereit ist.

## Mit Docker betreiben

Docker ist optional. Lege zuerst die Datei .env an und führe dann aus:

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## Erste Schritte in Discord

Nutze diese Befehle auf deinem Server und ersetze die Channel-Namen durch deine eigenen.

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

Alle Funktionen sind in der Befehlsreferenz beschrieben: [COMMANDS.md](../COMMANDS.md).

## Struktur, Team und Übersicht (1.5)

Mit diesen Schritten richtest du die neueren Funktionen ein. Jede lässt sich mit /admin module abschalten, und Präfix und Texte bleiben pro Server änderbar.

1. Sieh, was eingerichtet ist: `/admin module overview` listet jedes Modul mit Zustand und Einrichtungsstatus. Das Dashboard zeigt dasselbe im Einrichtungs-Panel.
2. Befehl finden: `/info find text:ban` durchsucht alle Befehle nach einem Wort, `/help` zeigt die Gruppen.
3. Regeln mit Akzeptieren-Knopf veröffentlichen: `/structure rules setup`, dann `/structure rules add`, dann `/structure rules post`. Wer eine neue Version nicht akzeptiert hat, wird alle paar Stunden erinnert.
4. Dem Bot sagen, wer zum Team gehört: `/team duty roster`. Listen verfügbarer Teammitglieder und die Weiterleitung von Tickets und Warnungen nutzen das.
5. Ungenutzte Kanäle aufräumen: `/structure archive setup`, dann `/structure archive scan`.
6. Zurückkehrenden Mitgliedern ihre Rollen zurückgeben: `/members stickyroles setup`.
7. Namen lesbar halten: `/members nickname setup`, vor `/members nickname scan` mit `/members nickname check` testen.
8. Vor größeren Änderungen die Einstellungen mit `/admin config export` sichern und Rollen und Kanäle mit `/server diagnose` prüfen.

## Updates und Backups

Bot aktualisieren:

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

Deine Einstellungen sicherst du, indem du den Ordner data kopierst, zum Beispiel:

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## Musik (optional)

Das Musikmodul braucht ffmpeg auf dem Rechner, auf dem der Bot läuft. Lege eigene Musik im Ordner music/ als Künstler/Album/01 - Titel.flac ab oder erlaube Downloads. Der Ordner kann groß werden, lege ihn deshalb auf eine Platte mit Platz oder in ein Docker-Volume.

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

## Optional: Bilder lesen und Sprachen

Damit das Anti-Scam-Modul Text in Bildern liest, installiere tesseract auf dem Rechner, auf dem der Bot läuft (das Docker-Image enthält es schon). Prüfe dann mit /security antiscam status, ob es bereit ist. Die Sprache der Nachrichten, die Mitglieder sehen, stellst du mit /admin language ein.

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

Das Dashboard ist eine Webseite, die im Bot läuft. Nach der Anmeldung mit Discord änderst du die Einstellungen deiner Server mit Schaltern, Menüs und Feldern statt mit Befehlen: Module, Channels, Rollen, Schwellenwerte, Texte, das Präfix und die Sprache. Außerdem zeigt es die letzten Moderationsfälle und exportiert und importiert Einstellungen. Es funktioniert auf deinem eigenen Rechner genauso wie auf einem VPS und ist aus, bis du es einschaltest.

1. Öffne deine Anwendung im Developer Portal, gehe zu OAuth2 und kopiere das Client Secret in die Datei .env.
2. Füge auf derselben Seite die Weiterleitungsadresse http://localhost:8080/callback hinzu.
3. Schalte das Dashboard in der settings.json ein.
4. Starte den Bot neu und öffne http://localhost:8080 im Browser. Melde dich mit Discord an.

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

Lass host auf 127.0.0.1 und wähle einen von zwei Wegen. Erstens ein SSH-Tunnel: Nichts wird veröffentlicht, du öffnest http://localhost:8080 auf deinem Rechner, solange der Tunnel läuft.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Zweitens HTTPS über einen Reverse-Proxy wie Caddy, der sich selbst ein Zertifikat holt (siehe deploy/Caddyfile.example). Setze dann public_url auf deine https-Adresse, füge https://deine-adresse/callback als Weiterleitung im Developer Portal hinzu und setze trust_proxy auf true:

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

## Fehlerbehebung

- Slash-Befehle erscheinen nicht: Warte einige Minuten, starte Discord neu und prüfe, ob der Bot mit dem Scope applications.commands eingeladen wurde.
- Der Bot bricht mit einem Fehler zu Privileged Intents ab: Aktiviere im Developer Portal Server Members Intent und Message Content Intent.
- Improper token: Kopiere den Token erneut und achte darauf, dass in .env genau DISCORD_TOKEN=token steht, ohne Leerzeichen oder Anführungszeichen.
- I cannot assign that role: Schiebe die Rolle des Bots über die Rolle, die er verwalten soll.
- Es wird nichts geloggt: Lege mit /server log set einen Channel fest und prüfe, ob der Bot dort Nachrichten senden, Links einbetten und Dateien anhängen darf.
- Unknown timezone: Führe pip install tzdata aus und starte den Bot neu.
- Etwas schlägt ohne erkennbaren Grund fehl: Fehler und Warnungen werden in die Konsole geschrieben. Auf einem VPS liest du sie mit journalctl -u guardbot -f.

## Support

Bugs, Ideen und Vorschläge: Discord @justyyin oder ein GitHub-Issue.

Copyright (c) Justyn - made in Germany
