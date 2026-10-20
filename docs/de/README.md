# GuardBot

**Deutsch** | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Selbst gehosteter Discord-Bot für Moderation, Sicherheit und Community. Open Source, kostenlos, und deine Daten bleiben auf deinem eigenen Rechner.

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
- [Aufbau des Repositorys](#aufbau-des-repositorys)
- [Befehle](#befehle)
- [Konfiguration](#konfiguration)
- [Roadmap](#roadmap)
- [Datenschutz und Sicherheit](#datenschutz-und-sicherheit)
- [Support](#support)
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
- Gulag-Channel: Wer Scam-Links oder -Bilder postet, landet in einem einzigen Channel mit Anleitung zur Kontosicherung. Moderatoren nutzen außerdem /jail und /unjail.
- Verifizierung per Button oder Captcha, mit automatischem Entfernen von Mitgliedern, die sich nicht rechtzeitig verifizieren.
- Anti-Nuke überwacht zusätzlich Rechtevergabe, neue Webhooks, hinzugefügte Bots und Server-Umbenennungen.

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

### Verwaltung

- Jedes Modul und jeder einzelne Befehl lässt sich pro Server an- oder ausschalten.
- Eigener Prefix, Befehls-Aliase und umbenennbare Befehle.
- Backup und Restore von Rollen und Channel-Struktur.
- Zeitgesteuerte automatische Backups von Rollen, Channels, Emojis und Webhooks, mit einem Restore-Befehl, der nur Fehlendes ergänzt.

## Projektstatus

GuardBot ist noch jung und wurde bisher nicht auf großen Servern eingesetzt. Die automatischen Tests (`python -m unittest`) decken Speicher, Erkennung persönlicher Daten, Levelberechnung, Befehlsregistrierung, Rechteprüfung und die Links der Dokumentation ab. Alles, was einen echten Discord-Server braucht, etwa Lockdown, Backup-Restore, Verifizierung, Anti-Nuke und der Gulag, ist dadurch nicht abgedeckt. Probiere diese Funktionen zuerst auf einem Testserver aus, bevor du dich darauf verlässt. Die Übersetzungen der Dokumentation wurden nicht von Muttersprachlern geprüft, Korrekturen sind willkommen.

## Voraussetzungen

- Python 3.11 oder neuer
- Eine Discord-Anwendung mit Bot-Token
- Ein Computer oder VPS, der durchgehend online ist

## Schnellstart

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Die vollständige Schritt-für-Schritt-Anleitung steht in [GUIDE.md](GUIDE.md).

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

## Befehle

Die meisten Befehle sind Slash-Befehle, Moderationsbefehle funktionieren auch mit Prefix. Die vollständige Liste steht in der Befehlsreferenz: [COMMANDS.md](../COMMANDS.md).

## Konfiguration

Globale Optionen stehen in der settings.json. Alles andere wird pro Server mit Befehlen wie /module, /command, /perms, /alias und /config eingestellt.

Um einen Befehl umzubenennen, trage ihn unter command_names ein und starte den Bot neu:

```json
{
  "prefix": "!",
  "command_names": {
    "warn": "verwarnen"
  }
}
```

## Roadmap

- Lokales Web-Dashboard, das auf deinem eigenen Rechner läuft, damit sich Einstellungen ohne gehosteten Dienst ändern lassen.
- Übersetzte Bot-Nachrichten.
- Export und Import der Einstellungen.

## Datenschutz und Sicherheit

- Keine Telemetrie und keine externen Dienste. Der Bot kommuniziert nur mit Discord.
- Alle Daten liegen im Ordner data auf deinem Rechner: Einstellungen, XP, Geburtstage (nur Tag und Monat) und Moderationsfälle.
- Der Bot ignoriert Direktnachrichten von Mitgliedern.
- Der Token wird aus der Datei .env gelesen. Gib ihn niemals weiter und lade ihn nicht hoch.
- Mitglieder können ihre eigenen Daten mit /mydata exportieren und löschen. Administratoren legen fest, wie lange Daten ausgetretener Mitglieder gespeichert bleiben.
- [PRIVACY.md](../PRIVACY.md)

## Support

Bugs, Ideen und Vorschläge: Schreib mir auf Discord, @justyyin, oder eröffne ein Issue auf GitHub.

## Lizenz

Veröffentlicht unter der MIT-Lizenz. Siehe [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
