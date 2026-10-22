# GuardBot

**Deutsch** | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Selbst gehosteter Discord-Bot für Moderation, Sicherheit und Community. Open Source, kostenlos, und deine Daten bleiben auf deinem eigenen Rechner.

> Beta: GuardBot und sein Dashboard befinden sich in einer Beta-Phase. Sie wurden nicht gründlich getestet, vor allem nicht auf großen Servern und nicht in jeder Situation auf Discord. Rechne mit Fehlern, sichere den Ordner data regelmäßig und melde Probleme. Nutzung auf eigene Gefahr.

<!-- toc -->

- [Über das Projekt](#über-das-projekt)
- [Funktionen](#funktionen)
  - [Sicherheit](#sicherheit)
  - [Moderation](#moderation)
  - [Logging](#logging)
  - [Community](#community)
  - [Verwaltung](#verwaltung)
- [Projektstatus](#projektstatus)
- [Voraussetzungen](#voraussetzungen)
- [Schnellstart](#schnellstart)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Startskripte und Autostart](#startskripte-und-autostart)
  - [Aktualisieren](#aktualisieren)
- [Bot-Berechtigungen](#bot-berechtigungen)
- [Erste Schritte in Discord](#erste-schritte-in-discord)
  - [Struktur, Mitglieder und Team](#struktur-mitglieder-und-team)
- [Dashboard](#dashboard)
  - [Dashboard einrichten](#dashboard-einrichten)
  - [Sicherheit](#sicherheit-1)
  - [Dashboard auf einem VPS](#dashboard-auf-einem-vps)
- [Befehle](#befehle)
  - [Befehlsgruppen](#befehlsgruppen)
  - [Moderation](#moderation-1)
  - [Gulag (Jail)](#gulag-jail)
  - [Auto-Moderation](#auto-moderation)
  - [Raid-Schutz und Lockdown](#raid-schutz-und-lockdown)
  - [Anti-Nuke](#anti-nuke)
  - [Verifizierung](#verifizierung)
  - [Logging](#logging-1)
  - [Willkommen, Abschied und Booster](#willkommen-abschied-und-booster)
  - [Tickets](#tickets)
  - [Umfragen und Giveaways](#umfragen-und-giveaways)
  - [Vorschläge und Starboard](#vorschläge-und-starboard)
  - [XP und Level](#xp-und-level)
  - [Reaction Roles und Benachrichtigungen](#reaction-roles-und-benachrichtigungen)
  - [Geburtstage](#geburtstage)
  - [Temporäre Voice-Channels](#temporäre-voice-channels)
  - [Backup und Restore](#backup-und-restore)
  - [Daten und Datenschutz](#daten-und-datenschutz)
  - [Moderator-Werkzeuge](#moderator-werkzeuge)
  - [Informationen](#informationen)
  - [Ankündigungen, Tags und Erinnerungen](#ankündigungen-tags-und-erinnerungen)
  - [Mod-Mail und Ban-Einsprüche](#mod-mail-und-ban-einsprüche)
  - [Zähl-Channel, Sticky-Nachrichten und Statistiken](#zähl-channel-sticky-nachrichten-und-statistiken)
  - [Weitere Optionen bestehender Funktionen](#weitere-optionen-bestehender-funktionen)
  - [Weitere AutoMod-Werkzeuge](#weitere-automod-werkzeuge)
  - [Moderator-Limits und Rechte-Audit](#moderator-limits-und-rechte-audit)
  - [Meldungen und Invite-Tracking](#meldungen-und-invite-tracking)
  - [Diagnose und Fehlersuche](#diagnose-und-fehlersuche)
  - [Musik](#musik)
  - [Einrichtung und Gesundheitscheck](#einrichtung-und-gesundheitscheck)
  - [Wirtschaft](#wirtschaft)
  - [Rollenmenüs, geplante Nachrichten und Feeds](#rollenmenüs-geplante-nachrichten-und-feeds)
  - [Aktivität, Sammelaktionen und Fallsuche](#aktivität-sammelaktionen-und-fallsuche)
  - [Anti-Scam und Anti-Krypto](#anti-scam-und-anti-krypto)
  - [Prüfung, Schwarm-Erkennung, Zeitleiste und Lernen](#prüfung-schwarm-erkennung-zeitleiste-und-lernen)
  - [Nachrichten-Builder und Updates](#nachrichten-builder-und-updates)
  - [Betrieb](#betrieb)
  - [Verwaltung](#verwaltung-1)
- [Platzhalter in Nachrichten](#platzhalter-in-nachrichten)
- [Konfiguration](#konfiguration)
- [Daten und Speicherort](#daten-und-speicherort)
- [Aufbau des Repositorys](#aufbau-des-repositorys)
- [Übersetzungen](#übersetzungen)
- [Roadmap](#roadmap)
- [Datenschutz und Sicherheit](#datenschutz-und-sicherheit)
- [Support](#support)
- [Credits](#credits)
- [Lizenz](#lizenz)

<!-- tocstop -->

## Über das Projekt

GuardBot bündelt Funktionen, für die viele Server bei gehosteten Bots bezahlen: Moderation, Logging, Anti-Raid, Anti-Nuke, Tickets, Level und mehr. Du betreibst den Bot selbst, auf deinem eigenen Computer oder auf einem kleinen VPS.

Gehostete Bots speichern Serverdaten, Mitglieds-IDs und teils E-Mail-Adressen bei einem Drittanbieter. Wenn du den Bot selbst hostest, verlassen diese Daten deinen Rechner nicht. GuardBot soll zeigen, dass jeder einen vollwertigen Bot ohne Abo betreiben kann.

## Funktionen

### Sicherheit

- Auto-Moderation: Wortfilter, Caps-Filter, Mention-Spam, Einladungslinks, Phishing-Domains, persönliche Daten, Doxing und Drohungen. Alle Listen sind editierbar.
- Anti-Raid mit Erkennung von Beitrittswellen und ein Server-Lockdown für alle Channels.
- Anti-Nuke: Limits für Massenlöschungen und Bans, automatische Reaktion und eine Direktnachricht an den Server-Gründer.
- Gulag-Channel: Wer Scam-Links oder -Bilder postet, landet in einem einzigen Channel mit Anleitung zur Kontosicherung. Moderatoren nutzen außerdem /moderation jail und /moderation unjail.
- Verifizierung per Button oder Captcha, mit automatischem Entfernen von Mitgliedern, die sich nicht rechtzeitig verifizieren.
- Anti-Nuke überwacht zusätzlich Rechtevergabe, neue Webhooks, hinzugefügte Bots und Server-Umbenennungen.
- Anti-Scam: falsche Gewinnspiele und Krypto-Betrug werden in Text und Bildern innerhalb von Millisekunden entfernt, auch der MrBeast-Scam in jeder Schreibweise.

### Moderation

- Warn, Mute, Kick, Ban und Jail mit Verlauf, filterbar nach Erwähnung, User-ID oder Typ.
- Automatische Eskalation, zum Beispiel führen drei Verwarnungen zu einem Timeout.
- Festlegen, welche Rollen oder Nutzer die einzelnen Moderationsbefehle verwenden dürfen.

### Logging

- Gesendete, bearbeitete und gelöschte Nachrichten inklusive Bildern, GIFs und URLs, mit eigenen Log-Channels.
- Änderungen an Rollen, Nicknames, Bans, Voice, Channels und Server-Rollen.

### Community

- Willkommens- und Abschiedsnachrichten, Auto-Rollen und Booster-Belohnungen.
- Tickets, Umfragen, Giveaways und Vorschläge.
- Reaction Roles mit beliebigen Emojis und Benachrichtigungs-Themen, die Mitglieder selbst an- oder ausschalten.
- XP und Level von 1 bis 100 für Chat und Voice, Level-Rollen und Geburtstage.
- Starboard und temporäre Voice-Channels.
- Jail mit Zeitdauer, Umfragen mit Mehrfachauswahl, Rank-Karten als Bild und XP-Boosts pro Rolle.
- Wirtschaft mit Shop, Rollenmenüs mit Buttons oder Dropdown, geplante Nachrichten, YouTube-, Twitch- und RSS-Feeds, Aktivitätsstatistik und ein geführtes /admin setup. Nachrichten an Mitglieder gibt es in 12 Sprachen.

### Verwaltung

- Jedes Modul und jeder einzelne Befehl lässt sich pro Server an- oder ausschalten.
- Eigener Prefix, Befehls-Aliase und umbenennbare Befehle.
- Backup und Restore von Rollen und Channel-Struktur.
- Zeitgesteuerte automatische Backups von Rollen, Channels, Emojis und Webhooks, mit einem Restore-Befehl, der nur Fehlendes ergänzt.
- Dashboard: Einstellungen jedes Servers im Browser ändern, nach einer Discord-Anmeldung, nur für Mitglieder, die den Server verwalten, und nur solange der Bot verbunden ist.

## Projektstatus

GuardBot ist noch jung und wurde bisher nicht auf großen Servern eingesetzt. Die automatischen Tests (`python -m unittest`) decken Speicher, Erkennung persönlicher Daten, Levelberechnung, Befehlsregistrierung, Rechteprüfung und die Links der Dokumentation ab. Alles, was einen echten Discord-Server braucht, etwa Lockdown, Backup-Restore, Verifizierung, Anti-Nuke und der Gulag, ist dadurch nicht abgedeckt. Probiere diese Funktionen zuerst auf einem Testserver aus, bevor du dich darauf verlässt. Die Übersetzungen der Dokumentation wurden nicht von Muttersprachlern geprüft, Korrekturen sind willkommen.

## Voraussetzungen

- Python 3.11 oder neuer
- Eine Discord-Anwendung mit Bot-Token
- Ein Computer oder VPS, der durchgehend online ist
- ffmpeg (nur für das Musikmodul)
- tesseract-ocr (optional, nur zum Lesen von Text in Bildern)

## Schnellstart

Wähle dein System. Jede Variante braucht Python 3.11 oder neuer und den Token deines Bots. Die ausführliche Schritt-für-Schritt-Anleitung steht in [GUIDE.md](GUIDE.md).

### Linux

```bash
sudo apt install -y python3 python3-venv python3-pip git ffmpeg tesseract-ocr
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
```

### macOS

```bash
brew install python@3.12 git ffmpeg tesseract
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
open -e .env
python main.py
```

### Windows

```powershell
winget install Python.Python.3.12 Git.Git Gyan.FFmpeg UB-Mannheim.TesseractOCR
git clone <REPOSITORY_URL>
cd guardbot
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
python main.py
```

### Startskripte und Autostart

Die Startskripte legen die virtuelle Umgebung an, installieren die Pakete und starten den Bot. Beim ersten Start erstellen sie die Datei .env und halten an, damit du den Token eintragen kannst. Starte sie danach noch einmal.

```bash
./start.sh
```

```bat
start.bat
```

Damit der Bot nach einem Neustart des Rechners weiterläuft, nutze einen Dienst. Linux (systemd) und macOS (launchd):

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

Unter Windows legst du in der Aufgabenplanung eine Aufgabe an, die start.bat bei der Anmeldung startet, oder nutzt einen Dienst-Wrapper wie NSSM. Für Docker siehe [GUIDE.md](GUIDE.md).

### Aktualisieren

Stoppe den Bot, führe diese Befehle aus und starte ihn wieder. Deine Daten im Ordner data bleiben unberührt, und der Bot macht vor jeder Änderung des Datenformats eine Datenbank-Sicherung.

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

## Bot-Berechtigungen

Am einfachsten ist die Berechtigung Administrator. Wenn du mit minimalen Rechten arbeiten willst, vergib diese und aktiviere im Developer Portal die Intents Server Members und Message Content:

```
Basics
  View Channels, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions
Moderation
  Moderate Members (timeouts), Kick Members, Ban Members, Manage Messages
Roles and channels
  Manage Roles, Manage Channels (gulag, lockdown, verification, tickets, backup)
Optional
  View Audit Log (who did what in logs and anti-nuke), Move Members, Manage Webhooks, Create Expressions
```

## Erste Schritte in Discord

Ein sinnvoller Start. Führe diese Befehle auf deinem Server aus und ersetze Channels und Rollen durch deine eigenen:

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

### Struktur, Mitglieder und Team

Version 1.5 bringt Befehle, um einen Server aufzubauen und aufgeräumt zu halten, zurückkehrende Mitglieder wiederherzustellen und das Moderationsteam zu führen. Jeder Teil hat einen Modulschalter (`/admin module`), eigene Einstellungen und einen Platz im Dashboard.

```
/structure channel create name:news kind:text category:Info private:False
/structure channel clone channel:#news name:news-2
/structure channel rename channel:#news name:announcements
/structure channel move channel:#news category:Info position:1
/structure channel sort category:Info
/structure channel copyperms source:#news target:#rules whole_category:False
/structure category create name:Events private:False
/structure category clone category:Events name:Events 2
/structure category sort
/structure category sync category:Events
/structure archive setup action:report days:60 report_channel:#staff interval_hours:24
/structure archive ignore channel:#news
/structure archive scan action:report
/structure temprole give member:@User role:@Event duration:7d reason:Contest
/structure temprole list
/structure roletemplate save name:mod role:@Moderator
/structure roletemplate apply name:mod role_name:Trial Mod
/structure rules setup channel:#rules role:@Member remind:True remind_hours:24
/structure rules add text:Be kind to each other.
/structure rules post new_version:True
/structure rules status

/members stickyroles setup roles:True days:30 punishments:True dangerous:False
/members stickyroles status
/members stickyroles forget user:@User
/members nickname setup dehoist:True usernames:True rename_to:Renamed notify:True
/members nickname word word:badword
/members nickname check name:!!hoisted
/members nickname scan
/members watch setup channel:#staff ping_role:@Moderator repeat:False
/members watch add user:@User reason:Suspicious
/members watch list
/members reason add name:spam action:mute text:Spam duration:1h
/members reason use name:spam user:@User

/security approval setup channel:#staff role:@Moderator ban:True bulk:True minutes:30 owner_bypass:True
/security approval list
/security approval cancel request_id:3
/moderation case undo case_id:12 reason:Mistake follow:True batch:False
/moderation escalation expiry days:90

/admin history list
/admin history show number:5
/admin history rollback number:5 section:welcome
/admin history keep count:200
/admin history copy source:123456789012345678 sections:welcome,tickets dry_run:True
/admin exceptions add rule:invites channel:#media role:@Artist
/admin exceptions list
/admin dashaccess add role:@Helper level:viewer
/admin dashaccess list

/team teamstats overview days:30
/team teamstats member user:@User
/team teamstats inactive days:14
/team weekly setup channel:#staff day:Monday hour:9
/team weekly now days:7
/team duty away duration:3d reason:Holiday
/team duty back
/team duty route feature:tickets enabled:True
/team duty roster role:@Moderator
/team apply setup channel:#applications staff_role:@Moderator accept_role:@Trial votes:3 open:True cooldown_days:30
/team apply question action:add text:Why do you want to join?
/team apply start
/team apply list
/team apply decide number:4 decision:accept
```

- Mit `/structure` werden Kanäle und Kategorien erstellt, geklont, umbenannt, sortiert und mit den Rechten eines anderen Kanals versehen. Inaktive Kanäle werden gemeldet oder in eine Archiv-Kategorie verschoben (`/structure archive`). Rollen können zeitlich begrenzt vergeben und als Vorlage gespeichert werden; eine Vorlage vergibt nie ein Recht, das die anwendende Person selbst nicht hat.
- `/structure rules` veröffentlicht die Regeln mit Annehmen-Knopf und Versionsnummer. Nach `post new_version:True` erhalten Mitglieder, die die neue Version nicht angenommen haben, eine einmalige Erinnerung per Direktnachricht.
- `/members stickyroles` gibt Rollen zurück und stellt Timeout oder Mute wieder her, wenn ein Mitglied zurückkehrt. `/members nickname` entfernt Sonderzeichen am Namensanfang, prüft verbotene Wörter in Spitznamen und Benutzernamen und benennt Verstöße um. Die Beobachtungsliste ist still: Das Team wird bei der ersten Nachricht eines gelisteten Nutzers gewarnt.
- Die Vier-Augen-Freigabe (`/security approval`) lässt Bans, Kicks, Timeouts und Sammelaktionen erst laufen, wenn ein zweiter Moderator zustimmt. `/moderation case undo` nimmt einen Fall zurück, auch die Folgeaktionen (zum Beispiel einen Mute und den darauf folgenden Ban). Verwarnungen können nach einer Anzahl Tage ablaufen (`/moderation escalation expiry`).
- `/admin history` zeigt, wer wann welche Einstellung geändert hat, und setzt einen Bereich zurück. Der Name der Person ist eine Vermutung aus den letzten Befehlen und Dashboard-Änderungen auf dem Server. `/admin history copy` kopiert Bereiche auf einen anderen Server, den du mit dem Bot verwalten darfst; es startet als Probelauf. `/admin exceptions` nimmt Kanäle und Rollen von AutoMod-Regeln und Anti-Scam aus. `/admin dashaccess` gibt Rollen Nur-Lese- oder Moderator-Zugriff auf das Dashboard.
- `/team` zeigt die Arbeit jedes Moderators (Fälle, Tickets, Meldungen, Reaktionszeit, inaktive Mitglieder), sendet einen Wochenbericht (Tag und Stunde in UTC), lässt Moderatoren sich mit `/team duty away` abmelden, damit Tickets und Pings an andere gehen, und führt Team-Bewerbungen mit Formular und Abstimmung.
- Discord kann Befehle in Gruppen nicht für einzelne Mitglieder ausblenden. Der Bot prüft trotzdem jeden Aufruf. Die Zahlen der Team-Statistik werden ab dem Tag der Aktualisierung gezählt; ältere Aktionen fehlen.

## Dashboard

Das Dashboard ist eine Webseite, die im Bot läuft. Nach der Anmeldung mit Discord änderst du die Einstellungen deiner Server mit Schaltern, Menüs und Feldern statt mit Befehlen: Module, Channels, Rollen, Schwellenwerte, Texte, das Präfix und die Sprache. Außerdem zeigt es die letzten Moderationsfälle und exportiert und importiert Einstellungen. Es funktioniert auf deinem eigenen Rechner genauso wie auf einem VPS und ist aus, bis du es einschaltest.

### Dashboard einrichten

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

### Sicherheit

- Anmeldung nur mit Discord (OAuth2, Bereich identify). Das Zugriffstoken wird sofort widerrufen und nie gespeichert.
- Zugriff haben nur der Besitzer eines Servers und Mitglieder mit der Berechtigung Administrator oder Server verwalten, und nur auf diesen Server. Die Berechtigung wird bei jeder Anfrage neu geprüft.
- Es lassen sich nur Server öffnen, auf denen der Bot gerade verbunden ist. Ist der Bot offline, nicht auf dem Server oder noch am Starten, verweigert das Dashboard alles. Das Dashboard läuft im Bot und hat keine eigene Datenbank und keinen eigenen Dienst.
- Standardmäßig hört es nur auf 127.0.0.1, sodass niemand sonst im Netzwerk darauf zugreifen kann. Eine öffentliche Adresse wird nur mit HTTPS akzeptiert, sonst startet das Dashboard nicht.
- Sitzungen nutzen ein zufälliges Token in einem HttpOnly-Cookie mit SameSite und unter HTTPS dem Präfix __Host-. Sie enden nach 8 Stunden und liegen nur im Arbeitsspeicher, ein Neustart meldet alle ab.
- Jede Änderung braucht ein CSRF-Token und einen passenden Origin. Der Host-Header wird gegen DNS-Rebinding geprüft. Die Seite lädt keine fremden Skripte, eine strikte Content Security Policy blockiert Inline-Code, Anfragen sind ratenbegrenzt und der Inhalt ist auf 256 KB begrenzt.
- Jeder Wert wird gegen den Typ der Einstellung geprüft, und Discord-IDs müssen auf dem Server existieren. Interner Zustand wie Zähler, Tickets und gespeicherte Einträge lässt sich nicht bearbeiten. Jede Änderung wird in den Sicherheits-Log-Channel des Servers geschrieben.
- Nachrichteninhalte werden nie angezeigt. Moderationsfälle sind nur lesbar.

### Dashboard auf einem VPS

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

Der Einstellungs-Editor zeigt jede Einstellung, die ein Schalter, eine Zahl, ein Text, ein Channel, eine Rolle oder eine einfache Liste ist. Was mit Befehlen angelegt wird, etwa Shop-Artikel, Rollenmenüs, Feeds, Tags und Tickets, bleibt Befehlssache. Die Seite gibt es auf Englisch und Deutsch und folgt der Sprache deines Browsers. In Docker veröffentlichst du den Port nur auf 127.0.0.1 (127.0.0.1:8080:8080) und setzt im Container host auf 0.0.0.0 und allow_insecure_http auf true.

## Befehle

Die meisten Befehle sind Slash-Befehle, Moderationsbefehle funktionieren auch mit Prefix. Die vollständige Liste steht in der Befehlsreferenz: [COMMANDS.md](../COMMANDS.md).

<!-- groups -->
### Befehlsgruppen

Um Slash-Plätze zu sparen (Discord erlaubt 100 Befehle pro Bot auf oberster Ebene), sind zusammengehörige Befehle gruppiert. Zuerst die Gruppe, dann der Befehl, zum Beispiel `/moderation ban`. Textbefehle mit Präfix, zum Beispiel `!ban`, bleiben unverändert. Rechte, Aliase und Modulschalter verwenden weiter den einfachen Befehlsnamen.

| Gruppe | Enthält |
| --- | --- |
| `/moderation` | `warn`, `unwarn`, `warnings`, `clearwarns`, `note`, `mute`, `unmute`, `kick`, `ban`, `unban`, `tempban`, `jail`, `unjail`, `jailed`, `role`, `case`, `cases`, `bulk`, `escalation`, `purge`, `slowmode` |
| `/security` | `antinuke`, `antiscam`, `raid`, `block`, `unblock`, `blocklist`, `approval` |
| `/access` | `verify`, `probation`, `lockdown`, `lockdownconfig`, `unlock`, `lockchannel`, `unlockchannel`, `jailsetup` |
| `/server` | `log`, `backup`, `privacy`, `invites`, `stats`, `serverinfo`, `roleinfo`, `health`, `diagnose`, `debug` |
| `/admin` | `settings`, `config`, `module`, `command`, `perms`, `alias`, `prefix`, `language`, `setup`, `history`, `exceptions`, `dashaccess` |
| `/info` | `about`, `avatar`, `botinfo`, `ping`, `userinfo`, `mydata`, `leaderboard`, `rank` |
| `/community` | `welcome`, `booster`, `afk`, `remind`, `activity`, `tempvoice`, `voice` |
| `/engage` | `economy`, `giveaway`, `poll`, `counting`, `starboard` |
| `/support` | `ticket`, `suggest`, `tag`, `autoresponder` |
| `/members` | `stickyroles`, `nickname`, `watch`, `reason` |
| `/structure` | `channel`, `category`, `archive`, `temprole`, `roletemplate`, `rules` |
| `/team` | `teamstats`, `weekly`, `duty`, `apply`, `modwatch`, `permaudit` |
| `/post` | `say`, `embed`, `message`, `sticky`, `schedule`, `feed`, `reactionrole`, `rolemenu` |
| | `/help`, `/play`, `/automod`, `/music`, `/xp`, `/modmail`, `/appeal`, `/report`, `/suggestion`, `/birthday`, `/notify` |

### Moderation

Verwarnungen, Mutes, Kicks und Bans funktionieren als Slash-Befehle und mit Prefix, zum Beispiel `!warn @User spam`. Jede Aktion erzeugt einen Fall mit Nummer.

```
/moderation warn member:@User reason:Spam                    # also: !warn @User Spam
/moderation unwarn case_id:12                                 # remove one warning
/moderation clearwarns user:@User                             # remove all active warnings
/moderation mute member:@User duration:30m reason:Spam        # also: !mute @User 30m Spam
/moderation unmute member:@User
/moderation kick member:@User reason:Advertising
/moderation ban user:@User reason:Raid                        # user can also be an ID
/moderation unban user:123456789012345678

/moderation cases user:@User                                  # history, filter by mention or ID
/moderation cases kind:ban page:2                             # filter by type
/moderation cases search:john                                 # filter by part of a name
/moderation warnings user:@User
/moderation case view case_id:12

/moderation escalation list
/moderation escalation set warns:3 action:timeout minutes:60  # 3 warnings = 1 hour timeout
/moderation escalation set warns:5 action:kick
/moderation escalation set warns:7 action:ban                 # actions: timeout, kick, ban, jail
/moderation escalation remove warns:5
```

### Gulag (Jail)

Mitglieder mit gehacktem Account kommen in einen einzigen Channel mit Sicherheitsanleitung. Beim Freilassen bekommen sie ihre alten Rollen zurück.

```
/access jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/access jailsetup apply                                   # apply the channel permissions again
/access jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/access jailsetup preview

/moderation jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/moderation jail member:@User duration:2h                     # released automatically after 2 hours
/moderation unjail member:@User reason:Account secured
```

### Auto-Moderation

Regeln löschen oder bestrafen passende Nachrichten. Die Aktion wählst du pro Regel: log, delete, warn, timeout oder jail.

```
/automod toggle rule:words enabled:True action:delete
/automod toggle rule:phishing enabled:True action:jail
/automod toggle rule:pii enabled:True action:delete
# rules: words, caps, mentions, invites, phishing, pii, doxxing, threats
# actions: log, delete, warn, timeout, jail

/automod add name:words value:badword              # lists: words, phishing, phishing_allow,
/automod remove name:words value:badword           #        invites_allow, doxxing, threats
/automod show name:phishing
/automod import name:phishing file:<upload a .txt, one entry per line>

/automod set rule:caps option:percent value:80
/automod set rule:caps option:min_len value:15
/automod set rule:mentions option:max value:5
/automod set rule:phishing option:lookalike value:True

/automod channel channel:#media images:True videos:True links:False
/automod channel links:True                        # no channel = all channels without own rule
/automod unchannel channel:#media

/automod block kind:link value:evil.example
/automod block kind:message value:free nitro
/automod block kind:image image:<upload a picture>
/automod blocklist
/automod unblock kind:link number:1

/automod flood enabled:True count:5 seconds:5 timeout:10
/automod exemptrole role:@Moderator
/automod exemptchannel channel:#bot-commands
```

### Raid-Schutz und Lockdown

Erkennt viele Beitritte in kurzer Zeit und kann den Server sperren. Modus channels ändert jeden Channel, Modus role wirkt sofort.

```
/security raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3 lockdown:True
# 5 joins within 10 seconds count as a raid, accounts younger than 3 days are punished,
# actions: alert, timeout, kick

/access lockdown mode:role reason:Raid                    # instant, edits only the @everyone role
/access lockdown mode:channels reason:Raid                # thorough, edits every channel
/access unlock

/access lockdownconfig mode mode:role                     # default mode
/access lockdownconfig lockrole role:@Member              # extra role locked in role mode
/access lockdownconfig bypassrole role:@Moderator         # can still write in channels mode
/access lockdownconfig exempt channel:#announcements
```

### Anti-Nuke

Überwacht das Audit-Log und reagiert, wenn jemand den Server zerstört. Der Server-Gründer bekommt eine Direktnachricht.

```
/security antinuke setup enabled:True action:strip notify_owner:True   # actions: alert, strip, kick, ban
/security antinuke limit kind:channel_delete count:3 seconds:10
# kinds: channel_delete, role_delete, channel_create, ban, kick,
#        role_perm, role_grant, webhook_create, bot_add, guild_update
/security antinuke whitelist user:@TrustedAdmin             # toggle, never checked
/security antinuke staffrole role:@Moderator                # toggle, shown in alerts
/security antinuke servername name:MyServer                 # extra name for the nuke talk detection
/security antinuke newbots kick:True                        # kick bots added by untrusted users
/security antinuke restore member:@User                     # give back roles that were removed
/security antinuke status
```

### Verifizierung

Neue Mitglieder sehen nur den Verifizierungs-Channel, bis sie den Button drücken oder das Captcha lösen.

```
/access verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/access verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/access verify panel channel:#verify                      # post the button again
/access verify apply                                      # apply the channel permissions again
/access verify member member:@User                        # verify someone manually
/access verify off
```

### Logging

Wähle einen Channel pro Kategorie oder einen Haupt-Channel für alles.

```
/server log set category:main channel:#logs               # fallback for every category
/server log set category:messages channel:#log-messages
/server log set category:moderation channel:#log-moderation
/server log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/server log sent enabled:False                            # stop logging every sent message
/server log show
```

### Willkommen, Abschied und Booster

Nachrichten, Auto-Rollen und Belohnungen für Server-Booster.

```
/community welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/community welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/community welcome autorole role:@Member                     # toggle, given to every new member
/community welcome botrole role:@Bots                        # toggle, given to every new bot
/community welcome test

/community booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/community booster role role:@Booster                        # toggle
```

### Tickets

Mitglieder öffnen per Button private Channels. Beim Schließen wird ein Transkript verschickt.

```
/support ticket setup category:Tickets support_role:@Support log_channel:#ticket-logs max_open:1
/support ticket addtype key:report label:Report description:Report a member
/support ticket removetype key:report
/support ticket panel channel:#support title:Support description:Press a button to open a ticket

# inside a ticket
/support ticket add member:@User
/support ticket remove member:@User
/support ticket close
```

### Umfragen und Giveaways

Buttons zum Abstimmen und Teilnehmen. Dauern akzeptieren Werte wie 30m, 2h und 1d.

```
/engage poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/engage poll end poll_id:3
/engage poll list

/engage giveaway start prize:Nitro duration:2d winners:2 role:@Member
/engage giveaway end giveaway_id:1
/engage giveaway reroll giveaway_id:1
/engage giveaway list
```

### Vorschläge und Starboard

Mitglieder posten Vorschläge, die das Team annehmen oder ablehnen kann, und beliebte Nachrichten werden hervorgehoben.

```
/suggestion setup set channel:#suggestions review_role:@Staff
/support suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/engage starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/engage starboard ignore channel:#spam
```

### XP und Level

XP für Chat und Voice, Level-Rollen, Rollen-Boosts und Rank-Karten.

```
/xp config enabled:True min_xp:15 max_xp:25 cooldown:60 voice_xp:10 multiplier:1.5
/xp config max_level:100 stack_roles:True card:True
/xp config announce:channel announce_channel:#levels message:{user} reached level {level}!
/xp show
/xp boost role:@Booster multiplier:1.5             # 1.0 removes the boost
/xp ignore channel:#spam                           # toggle

/xp levelrole add level:10 role:@Active
/xp levelrole add level:50 role:@Veteran
/xp levelrole remove level:10
/xp levelrole list
/xp levelrole sync                                    # apply to everyone who already has XP

/xp give user:@User amount:500
/xp take user:@User amount:100
/xp setlevel user:@User level:20
/xp reset user:@User

/info rank                                              # also: !rank, shows a rank card image
/info rank user:@User
/info leaderboard
```

### Reaction Roles und Benachrichtigungen

Rollen per Reaktion mit beliebigen Emojis vergeben und Mitglieder ihre Benachrichtigungs-Themen selbst wählen lassen.

```
/post reactionrole panel channel:#roles title:Pick your roles description:React below
/post reactionrole add message:<message link> emoji:<any emoji> role:@Gamer
/post reactionrole add message:<message link> emoji:<any emoji> role:@Artist mode:unique
# mode unique: only one role of that message at a time
/post reactionrole remove message:<message link> emoji:<any emoji>
/post reactionrole list

/notify topic add key:events role:@Events description:Server events
/notify topic panel channel:#roles title:Notifications   # one button per topic
/notify topic remove key:events
/notify subscribe topic:events                     # members choose for themselves
/notify unsubscribe topic:events
/notify list
```

### Geburtstage

Mitglieder hinterlegen Tag und Monat, der Bot vergibt am Tag eine Rolle und schreibt eine Nachricht.

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Temporäre Voice-Channels

Wer den Hub-Channel betritt, bekommt einen Raum, der verschwindet, wenn er leer ist.

```
/community tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Backup und Restore

Backups enthalten Rollen, Channels, Emojis, Webhooks und Mitglieder-Rollen. Restore ergänzt nur, was fehlt.

```
/server backup create name:before-update
/server backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/server backup list
/server backup download name:before-update
/server backup restore name:before-update member_roles:True   # only adds what is missing
/server backup delete name:before-update
```

### Daten und Datenschutz

Mitglieder können ihre eigenen Daten exportieren und löschen. Administratoren legen fest, wie lange Daten gespeichert bleiben.

```
/info mydata export                                     # members download their own data
/info mydata delete confirm:True                        # members delete their XP and birthday

/server privacy retention days:90                         # delete data of members who left after 90 days
/server privacy export user_id:123456789012345678
/server privacy delete user_id:123456789012345678 cases:True
```

### Moderator-Werkzeuge

Channels aufräumen, Rollen verwalten und private Notizen führen. Jede Aktion wird protokolliert.

```
/moderation purge amount:50 user:@User kind:links           # kind: all, links, images, bots, attachments
/moderation slowmode seconds:10 channel:#general              # 0 turns it off
/access lockchannel channel:#general reason:Spam wave
/access unlockchannel channel:#general

/moderation role add member:@User role:@Member
/moderation role remove member:@User role:@Member

/moderation note user:@User text:Watch this member            # private, shown in /moderation cases
/moderation tempban user:@User duration:7d reason:Spam        # unbanned automatically
/moderation jailed                                            # who is in the gulag right now

/moderation case view case_id:12
/moderation case edit case_id:12 reason:Corrected reason
/moderation case delete case_id:12
```

### Informationen

Nutzer, Server, Rollen und den Bot nachschlagen.

```
/info userinfo user:@User
/server serverinfo
/server roleinfo role:@Moderator
/info avatar user:@User
/help command:ban                                  # explains one command
/info ping
/info botinfo
```

### Ankündigungen, Tags und Erinnerungen

Im Namen des Bots schreiben, eigene Befehle anlegen, Nachrichten automatisch beantworten und Erinnerungen setzen.

```
/post say channel:#news message:Maintenance tonight
/post embed channel:#news title:Update description:New rules color:#5865F2

/support tag create name:rules text:Be kind to each other
/support tag show name:rules
/support tag list
/support tag info name:rules
/support tag edit name:rules text:Be kind and read the pinned message
/support tag delete name:rules

/support autoresponder add trigger:server ip response:The IP is in #info mode:contains cooldown:30
/support autoresponder list
/support autoresponder remove id:1                         # mode: contains, word, exact, startswith

/community remind set duration:2h text:Stream starts
/community remind list
/community remind cancel id:1
/community afk reason:Lunch                                  # the bot tells others who mention you
```

### Mod-Mail und Ban-Einsprüche

Mitglieder schreiben dem Team über einen privaten Channel auf dem Server. Niemand muss dem Bot eine Direktnachricht schicken.

```
/modmail setup set category:Mod-mail staff_role:@Moderator log_channel:#modmail-log anonymous:False
/modmail setup panel channel:#help text:Press the button to write to the staff
/modmail setup block member:@User                   # toggles
/modmail setup status

/modmail send text:I need help with my account     # inside a mod-mail channel
/modmail close reason:Solved

/appeal setup set main_server_id:123456789012345678 staff_channel:#appeals cooldown_days:7
/appeal setup set invite:https://discord.gg/example rejoin_invite:https://discord.gg/example
/appeal setup status
/appeal send text:I understand the rule now and ask for a second chance
```

### Zähl-Channel, Sticky-Nachrichten und Statistiken

Ein Zählspiel, Nachrichten, die unten im Channel bleiben, und Channels mit Live-Zahlen.

```
/engage counting setup channel:#counting reset_on_fail:True delete_wrong:True
/engage counting status
/engage counting set number:100
/engage counting off

/post sticky set channel:#rules text:Read the rules before you write
/post sticky list
/post sticky remove channel:#rules

/server stats create template:Members: {members} category:Statistics
/server stats add channel:#info template:Boosts: {boosts}
/server stats list
/server stats refresh
/server stats remove channel:#info
```

### Weitere Optionen bestehender Funktionen

Ergänzungen zu Tickets, Giveaways, Voice-Räumen, XP, Geburtstagen, Backups, Logs und den Status-Anzeigen.

```
/support ticket claim
/support ticket rename name:billing-help
/support ticket list

/engage giveaway cancel giveaway_id:3
/engage giveaway edit giveaway_id:3 prize:Nitro winners:2 extend:1h

/community voice rename name:Study room                      # only the owner of the room
/community voice limit limit:4
/community voice lock
/community voice unlock
/community voice kick member:@User
/community voice transfer member:@User
/community voice claim                                       # if the owner left

/xp channelboost channel:#chat multiplier:1.5
/xp resetall confirm:True
/info leaderboard page:2

/birthday list
/birthday setup user member:@User day:14 month:3
/birthday setup clear member:@User

/server backup info name:weekly
/server log show
/server log ignorechannel channel:#bots
/server log ignoreuser user:@Bot
/server log sent enabled:True

/automod status
/access verify status
/security raid status
/community welcome show
/engage starboard show
```

### Weitere AutoMod-Werkzeuge

Kurzlinks verfolgen, Links für neue Mitglieder einschränken, Ghost-Pings finden und Regeln testen, ohne jemanden zu bestrafen.

```
/automod toggle rule:shortlinks enabled:True action:delete    # follow short links and judge the target
/automod set rule:shortlinks option:resolve value:true         # false = block short links outright
/automod set rule:shortlinks option:block_unresolved value:false
/automod add name:shortlink_domains value:example.link

/automod toggle rule:newlinks enabled:True action:delete       # new members may not post links
/automod set rule:newlinks option:hours value:48
/automod add name:newlinks_allow value:tenor.com

/automod ghostping enabled:True notify:True max_age:120
/automod dryrun rule:words enabled:True                        # report only, rule: all, words, caps, phishing, flood ...
/automod test text:free nitro at bit.ly/example member:@User
```

### Moderator-Limits und Rechte-Audit

Alarm, wenn ein Moderator zu viel bannt oder kickt, und eine Übersicht, welche Rollen gefährliche Rechte haben.

```
/team modwatch status
/team modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/team modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/team modwatch exclude member:@TrustedMod

/team permaudit run                                                  # roles with dangerous permissions and who holds them
/team permaudit watch enabled:True                                   # alarm when a role or member gets one
/team permaudit trust role:@Admin
```

### Meldungen und Invite-Tracking

Mitglieder melden Nachrichten an das Team, und der Bot merkt sich, welche Einladung ein neues Mitglied gebracht hat.

```
/report setup set channel:#reports ping_role:@Moderator cooldown:60 anonymous:False
/report setup ignorechannel channel:#staff
/report setup status

/report send message_link:https://discord.com/channels/1/2/3 reason:Spam
# or right click a message, Apps, Report message

/server invites who member:@User
/server invites stats user:@User
/server invites top
/server invites setup log:True alert_joins:5 alert_minutes:60
```

### Diagnose und Fehlersuche

Fehlende Rechte und kaputte Einstellungen finden, Fehlerberichte in einem Channel erhalten und Einstellungen exportieren oder importieren.

```
/server diagnose                                                       # permissions, role order, deleted channels and roles
/server debug status
/server debug errorchannel channel:#bot-errors
/server debug errortest
/server debug selftest enabled:True                                    # check at start-up
/server debug usagestats enabled:True
/server debug usage reset:False
/server debug level level:DEBUG                                        # owner of the bot only
/server debug db action:check                                          # owner of the bot only: check, vacuum, size

/admin config export
/admin config import file:guardbot-settings.json confirm:False        # first without confirm
```

### Musik

Spielt Links und Dateien aus dem Ordner music in einem Voice-Channel ab. Downloads werden als music/Künstler/Album/Titel gespeichert. Nötig sind ffmpeg und die Pakete aus requirements.txt.

```
/play query:daft punk one more time                            # library first, then the web
/play query:https://example.com/track                           # a link that yt-dlp supports

/music queue page:1
/music nowplaying
/music skip
/music pause
/music resume
/music stop
/music volume percent:70
/music loop mode:queue
/music shuffle
/music remove number:3
/music clear
/music seek position:1:30
/music join
/music leave

/music library search query:discovery
/music library list artist:Daft Punk
/music library play query:one more time
/music library scan                                             # after you copied files into music/
/music library info
/music library download url:https://example.com/track format:best

/music settings dj_role:@DJ volume:50 max_queue:100 per_user:25 max_minutes:60 idle_leave:120
/music settings allow_links:True allow_search:True allow_playlists:True library:True
/music settings allow_download:True download_format:best announce:True
/admin config set path:music.allowed_hosts value:bandcamp.com,archive.org
/music cleardj
/music status
```

Verlustfrei: eigene Dateien (FLAC, WAV, ALAC) und Quellen, die FLAC anbieten, werden unverändert abgespielt. YouTube, SoundCloud und ähnliche Seiten liefern nur verlustbehaftetes Audio, das sich nachträglich nicht verlustfrei machen lässt. Discord überträgt Voice als Opus, der Bot nutzt die Bitrate des Voice-Channels. Verantwortung: Herunterladen und Abspielen kann gegen die Nutzungsbedingungen einer Seite oder das Urheberrecht verstoßen. Downloads sind standardmäßig aus und das Modul ist aus, bis du es aktivierst. Wer den Bot betreibt, ist für abgespielte und gespeicherte Inhalte verantwortlich.

### Einrichtung und Gesundheitscheck

Ein geführter Assistent richtet das Wichtigste mit Buttons und Menüs ein: Log-Channel, Willkommens-Channel, Team-Rollen, das Gulag, ein AutoMod-Preset (locker, normal, streng), eine Server-Vorlage (Community, Gaming, Support) und die Sprache. /server health zeigt, was eingerichtet ist und was noch offen ist. Die Sprache ändert die Texte, die Mitglieder sehen, etwa Standard-Willkommensnachrichten, AutoMod-Hinweise, Verifizierung, Tickets, Einsprüche, Mod-Mail und Rollenmenüs. Feste Antworten an Administratoren sind übersetzt, Antworten mit Namen und Zahlen bleiben Englisch.

```
/admin setup                                                         # buttons and menus, nothing is switched off by a template
/server health                                                        # what is set up, what is open, and the self-test
/admin language code:de
```

### Wirtschaft

Eine Server-Währung mit täglicher Belohnung, Arbeit, Zahlungen, Rangliste und einem Shop, dessen Artikel eine Rolle geben können. Aktiviere sie mit dem Modul economy. Die Befehle funktionieren auch mit dem Präfix, zum Beispiel !economy daily.

```
/admin module enable name:economy
/engage economy balance member:@User                                  # same as !economy
/engage economy daily
/engage economy work
/engage economy pay member:@User amount:50
/engage economy leaderboard
/engage economy shop
/engage economy buy item:1
/engage economy inventory

/engage economy give member:@User amount:500                          # staff, a negative amount takes away
/engage economy shopadd name:VIP price:1000 role:@VIP stock:10
/engage economy shopremove item:1
/engage economy config name:gold daily:200 daily_hours:24 work_min:20 work_max:80 work_minutes:30
```

### Rollenmenüs, geplante Nachrichten und Feeds

Rollenmenüs vergeben Rollen mit Buttons oder einem Dropdown. Geplante Nachrichten werden einmal gepostet oder stündlich, täglich oder wöchentlich wiederholt. Feeds posten neue YouTube-Videos, Twitch-Streams und RSS-Einträge. Für YouTube brauchst du die Kanal-ID (sie beginnt mit UC). Twitch braucht TWITCH_CLIENT_ID und TWITCH_CLIENT_SECRET in der .env. Zeiten schreibst du als in 2h, 18:30 oder als Datum mit Uhrzeit wie 2026-12-24 18:00 in der Zeitzone des Servers. Die erste Prüfung eines Feeds merkt sich nur, was schon existiert.

```
/post rolemenu create title:Pick your roles kind:buttons single:False channel:#roles
/post rolemenu add menu:1 role:@Red label:Red
/post rolemenu remove menu:1 role:@Red
/post rolemenu delete menu:1
/post rolemenu list

/post schedule add channel:#news when:18:30 text:Daily reminder repeat:daily
/post schedule add channel:#news when:in 2h text:Restart soon repeat:none
/post schedule list
/post schedule remove number:1
/post schedule timezone name:Europe/Berlin

/post feed add kind:youtube target:UCxxxxxxxxxxxxxxxxxxxxxx channel:#videos ping:@Subscribers
/post feed add kind:twitch target:somestreamer channel:#live
/post feed add kind:rss target:https://example.com/feed.xml channel:#news
/post feed list
/post feed check
/post feed remove number:1
```

### Aktivität, Sammelaktionen und Fallsuche

Aktivität zählt Nachrichten pro Channel sowie Beitritte und Austritte pro Tag, niemals Inhalte oder Namen. Sammelaktionen bannen, kicken oder muten bis zu 25 Nutzer nach einer Bestätigung. Fälle lassen sich nach Nutzer, Art, Name, Grund, Moderator und Alter durchsuchen und miteinander verknüpfen, zum Beispiel eine Notiz mit einem Bann.

```
/admin module enable name:activity
/community activity overview days:7
/community activity channels days:30
/community activity growth days:14
/community activity reset

/moderation bulk ban users:123456789012345678 223456789012345678 reason:Raid
/moderation bulk kick users:123456789012345678 223456789012345678 reason:Spam
/moderation bulk timeout users:123456789012345678 223456789012345678 duration:2h reason:Spam

/moderation cases user:@User kind:ban text:scam moderator:@Mod days:30
/moderation case link case_id:12 other:15
/moderation case unlink case_id:12 other:15
```

### Anti-Scam und Anti-Krypto

Entfernt falsche Gewinnspiele, etwa den typischen MrBeast-Scam, in Text und Bildern innerhalb von Millisekunden. Namen auf der Sofort-Liste werden in jeder Schreibweise sofort entfernt (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Sonst addieren sich Wörter aus den Listen (Namen, Köder, Krypto, Links, Beträge), und die Nachricht wird ab dem Schwellenwert entfernt. Bilder werden per OCR gelesen, und Bilder, die einmal als Scam erkannt wurden, werden ohne erneutes Lesen entfernt. Für Bilder wird tesseract gebraucht, ohne tesseract wird nur Text geprüft. Ein Server über MrBeast kann den Namen aus der Sofort-Liste nehmen oder Channels mit /automod exemptchannel ausnehmen. Probiere es mit /security antiscam test aus, bevor du dich darauf verlässt.

```
/security antiscam status
/security antiscam set action:delete threshold:3 text:True images:True ocr_lang:eng max_images:3
/security antiscam words action:add kind:instant word:mrbeast
/security antiscam words action:remove kind:crypto word:token
/security antiscam test text:MrBeast is giving away 1000 BTC, claim now
/security antiscam testimage image:scam.png
/security antiscam forget
/automod dryrun rule:antiscam enabled:True                     # only report, do not remove
```

### Prüfung, Schwarm-Erkennung, Zeitleiste und Lernen

Die Prüfung steckt neue Mitglieder in eine Rolle. Bis sie die eingestellte Zahl normaler Nachrichten geschrieben haben oder die Minuten vergangen sind, werden Links, Einladungen und Dateien mit einem kurzen Hinweis entfernt. Der Raid-Schutz erkennt außerdem einen Schwarm: mehrere neue Konten mit gleichem Namensmuster, gleichem Profilbild oder Erstellung innerhalb weniger Minuten. Die Zeitleiste (/moderation case timeline) führt Kontoerstellung, Beitritt und Einladung, Prüfung, Fälle und Einsprüche eines Nutzers in zeitlicher Reihenfolge zusammen. Nachrichten werden nie gespeichert und sind deshalb nicht enthalten. /security block, /security unblock und /security blocklist verwalten die Blockliste des AutoMod mit kurzen Befehlen. Moderatoren bringen dem Anti-Scam-Modul etwas bei, mit dem Kontextmenü-Eintrag Mark as scam an einer Nachricht oder mit einer Reaktion mit dem Emoji aus learn_emoji: Die Nachricht wird gelöscht, und ihre Bilder und ihr Text werden von da an sofort entfernt. Jeden Teil schaltest du über sein Modul oder seine Einstellungen aus.

```
/admin module enable name:probation
/access probation setup minutes:10 messages:1 block_links:True block_files:True
/access probation status
/access probation release member:@User
/access probation add member:@User

/security raid swarm enabled:True minimum:4 minutes:10
/moderation case timeline user:@User

/security block kind:link value:evil.example
/security blocklist
/security unblock kind:link number:1
/security antiscam set learn_emoji:X
```

### Nachrichten-Builder und Updates

Der Nachrichten-Builder postet Nachrichten mit mehreren Embeds und Link-Buttons aus JSON. Er liest das JSON, das Embed-Generatoren wie Embed Generator exportieren, sodass du dort eine Nachricht gestaltest und sie mit dem Bot postest. Gib das JSON als Text, als .json-Datei oder als https-Link an, der direkt auf das JSON zeigt, zum Beispiel die Rohdatei eines Repositories (Links mit Weiterleitung werden abgelehnt). Es werden nur Link-Buttons erstellt, Buttons, die eine Interaktion brauchen, werden übersprungen. Jeder Link muss http oder https sein, Erwähnungen im Text pingen nie, und die Grenzen von Discord gelten. /post message copy exportiert eine vorhandene Nachricht als JSON, /post message edit ändert eine Nachricht des Bots und /post message preview zeigt das Ergebnis nur dir. Teilen-Links von Web-Editoren werden nicht geöffnet, weil ihr Format nicht öffentlich ist.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Der Bot prüft alle 12 Stunden das GitHub-Repository aus update.repo (gesetzt mit scripts/set_repo_url.py) auf ein neueres Release. Gibt es eines, bekommt der Besitzer des Bots eine Direktnachricht mit den Release-Notizen, und das Release wird heruntergeladen und geprüft: SHA-256-Prüfsumme des Releases, sichere Pfade im Archiv und eine Version, die zum Tag passt. Installiert wird mit /server debug update action:install oder von selbst, wenn auto_install an ist. Vor der Installation werden die ersetzten Dateien in data/update gesichert, neue Pakete installiert und der neue Code probeweise importiert. Schlägt etwas fehl, werden die alten Dateien wiederhergestellt. Deine .env, settings.json, data und music werden nie angefasst. Danach startet sich der Bot selbst neu. In Docker wird nichts an Ort und Stelle installiert, aktualisiere stattdessen das Image. Ein Update führt Code aus dem Repository aus, zeige es also nur auf ein Repository, dem du vertraust. Mit enabled auf false schaltest du es aus.

```json
{
  "update": {
    "enabled": true,
    "repo": "NAME/guardbot",
    "check_hours": 12,
    "auto_install": false,
    "require_checksum": false
  }
}
```

```
/post message send channel:#news url:https://example.com/message.json
/post message send channel:#news file:message.json
/post message preview url:https://example.com/message.json
/post message edit message:https://discord.com/channels/1/2/3 url:https://example.com/message.json
/post message copy message:https://discord.com/channels/1/2/3
/admin module disable name:builder
/server debug update action:status
/server debug update action:check
/server debug update action:install
```

### Betrieb

Der Bot speichert seine Daten alle paar Sekunden und legt Datenbank-Sicherungen in data/dbbackups ab, eine vor jeder Änderung des Datenformats und eine pro Tag. Musik-Warteschlange, Sticky-Nachrichten und Moderator-Zähler überstehen einen Neustart. Große Bots können auf mehreren Shards laufen. Eine Heartbeat-Datei und eine optionale Statusseite helfen Überwachungswerkzeugen. Diese Optionen stehen in der settings.json:

```json
{
  "shard_count": null,
  "db_backup_hours": 24,
  "db_backup_keep": 7,
  "health_port": 0,
  "health_host": "127.0.0.1",
  "tesseract": null,
  "music_generic": true
}
```

```
/server debug db action:backup                                         # owner of the bot only, saved in data/dbbackups
/server debug db action:list
```

### Verwaltung

Module und Befehle an- oder ausschalten, Prefix ändern, Aliase setzen und Befehle auf Rollen beschränken.

```
/admin module list
/admin module disable name:starboard
/admin module enable name:tickets
/admin command disable name:ban                          # single commands
/admin command enable name:ban
/admin command list

/admin prefix new_prefix:?                               # text commands now start with ?
/admin alias add alias:w command:warn                    # ?w @User Spam
/admin alias remove alias:w
/admin alias list

/admin perms allow command:ban target:@HeadModerator     # only this role may use /moderation ban
/admin perms deny command:warn target:@Trainee
/admin perms reset command:ban
/admin perms show

/admin settings
/help
/info about
```

## Platzhalter in Nachrichten

Diese Platzhalter werden in den Texten, die du einstellst, ersetzt:

```
/community welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/community booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/community tempvoice setup     name                            {name}
/access jailsetup notice    text                            {staff}
```

## Konfiguration

Globale Optionen stehen in der settings.json. Alles andere wird pro Server mit Befehlen wie /admin module, /admin command, /admin perms, /admin alias und /admin config eingestellt.

Um einen Befehl umzubenennen, trage ihn unter command_names ein und starte den Bot neu:

```json
{
  "prefix": "!",
  "data_dir": "data",
  "force_sync": false,
  "purge_on_guild_leave": false,
  "command_names": {
    "warn": "verwarnen",
    "ban": "sperren"
  }
}
```

Jede einzelne Einstellung lässt sich mit /admin config lesen und ändern. Diese Pfade brauchst du am häufigsten:

```
/admin config get path:automod.caps.percent
/admin config set path:automod.caps.percent value:80
/admin config set path:mod.dm_user value:false             # no direct message on punishments
/admin config set path:mod.warn_expiry_days value:30       # warnings expire after 30 days
/admin config set path:mod.default_mute_minutes value:120
/admin config set path:automod.mentions.max value:5
/admin config set path:automod.phishing.lookalike value:true
/admin config set path:raid.joins value:8
/admin config set path:xp.cooldown value:45
/admin config set path:tickets.max_open value:2
/admin config set path:privacy.retention_days value:90
/admin config reset section:welcome                        # back to the defaults of one section
```

## Daten und Speicherort

Alles, was der Bot speichert, liegt auf deinem eigenen Rechner:

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

## Aufbau des Repositorys

```
guardbot/
  main.py                 entry point
  requirements.txt
  settings.example.json   global options
  .env.example            token placeholder
  guardbot/
    core.py               bot class, storage, permission checks
    defaults.py           default settings of every module
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature group
  docs/                   documentation in 12 languages, COMMANDS.md, PRIVACY.md
  deploy/                 systemd service, Dockerfile, compose file
  scripts/                maintenance scripts
  tests/                  automated tests (python -m unittest)
  data/                   created at runtime, holds your settings and data
```

## Übersetzungen

Englisch ist die Originalsprache des Projekts. Alle Übersetzungen der Dokumentation, des Dashboards und der Bot-Nachrichten wurden maschinell erstellt und nicht von Muttersprachlern geprüft. Rechne mit holpriger Wortwahl und Fehlern und melde sie bitte oder schicke eine Korrektur. Die Dateien liegen in docs/ und guardbot/locales/.

## Roadmap

- Diagramme für Aktivität und Moderation im Dashboard.
- Prüfung aller Übersetzungen durch Muttersprachler.
- Mehr feste Antworttexte übersetzt.

## Datenschutz und Sicherheit

- Keine Telemetrie. Der Bot kommuniziert mit Discord und, für die Update-Prüfung, mit GitHub (es werden keine personenbezogenen Daten gesendet, mit update.enabled schaltest du es aus). Links, die Administratoren ihm geben, etwa Feeds, Musik und JSON-Links, werden nur auf Anfrage geöffnet.
- Alle Daten liegen im Ordner data auf deinem Rechner: Einstellungen, XP, Geburtstage (nur Tag und Monat) und Moderationsfälle.
- Der Bot ignoriert Direktnachrichten von Mitgliedern.
- Der Token wird aus der Datei .env gelesen. Gib ihn niemals weiter und lade ihn nicht hoch.
- Mitglieder können ihre eigenen Daten mit /info mydata exportieren und löschen. Administratoren legen fest, wie lange Daten ausgetretener Mitglieder gespeichert bleiben.
- [PRIVACY.md](../PRIVACY.md)

## Support

Bugs, Ideen und Vorschläge: Schreib mir auf Discord, @justyyin, oder eröffne ein Issue auf GitHub.

## Credits

GuardBot ist inspiriert von [Embed Generator](https://github.com/merlinfuchs/embed-generator) von Merlin Fuchs (MIT-Lizenz, gehostet auf message.style). Der Nachrichten-Builder liest dasselbe JSON-Format, daher lassen sich dort gestaltete Nachrichten mit diesem Bot posten. Code dieses Projekts ist nicht enthalten. Danke an die Autoren von discord.py, aiohttp, Pillow, yt-dlp, mutagen und Tesseract.

## Lizenz

Veröffentlicht unter der MIT-Lizenz. Siehe [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
