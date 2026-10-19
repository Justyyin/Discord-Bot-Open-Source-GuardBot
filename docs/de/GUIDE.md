# GuardBot: Einrichtungsanleitung

Diese Anleitung zeigt, wie du GuardBot auf deinem eigenen Computer oder auf einem VPS betreibst. Du brauchst etwa 15 Minuten.

<!-- toc -->

- [Discord-Bot erstellen](#discord-bot-erstellen)
- [Auf dem eigenen Computer betreiben](#auf-dem-eigenen-computer-betreiben)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux und macOS](#linux-und-macos)
- [Auf einem VPS betreiben](#auf-einem-vps-betreiben)
- [Mit Docker betreiben](#mit-docker-betreiben)
- [Erste Schritte in Discord](#erste-schritte-in-discord)
- [Updates und Backups](#updates-und-backups)
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
git clone https://github.com/YOUR-NAME/guardbot.git
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
git clone https://github.com/YOUR-NAME/guardbot.git
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

Alle Funktionen sind in der Befehlsreferenz beschrieben: [COMMANDS.md](../COMMANDS.md).

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

## Fehlerbehebung

- Slash-Befehle erscheinen nicht: Warte einige Minuten, starte Discord neu und prüfe, ob der Bot mit dem Scope applications.commands eingeladen wurde.
- Der Bot bricht mit einem Fehler zu Privileged Intents ab: Aktiviere im Developer Portal Server Members Intent und Message Content Intent.
- Improper token: Kopiere den Token erneut und achte darauf, dass in .env genau DISCORD_TOKEN=token steht, ohne Leerzeichen oder Anführungszeichen.
- I cannot assign that role: Schiebe die Rolle des Bots über die Rolle, die er verwalten soll.
- Es wird nichts geloggt: Lege mit /log set einen Channel fest und prüfe, ob der Bot dort Nachrichten senden, Links einbetten und Dateien anhängen darf.
- Unknown timezone: Führe pip install tzdata aus und starte den Bot neu.

## Support

Bugs, Ideen und Vorschläge: Discord @justyyin oder ein GitHub-Issue.

Copyright (c) Justyn - made in Germany

<!-- GuardBot (c) Justyn -->
