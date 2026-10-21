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
- [Bot-Berechtigungen](#bot-berechtigungen)
- [Erste Schritte in Discord](#erste-schritte-in-discord)
- [Befehle](#befehle)
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
  - [Verwaltung](#verwaltung-1)
- [Platzhalter in Nachrichten](#platzhalter-in-nachrichten)
- [Konfiguration](#konfiguration)
- [Daten und Speicherort](#daten-und-speicherort)
- [Aufbau des Repositorys](#aufbau-des-repositorys)
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

## Befehle

Die meisten Befehle sind Slash-Befehle, Moderationsbefehle funktionieren auch mit Prefix. Die vollständige Liste steht in der Befehlsreferenz: [COMMANDS.md](../COMMANDS.md).

### Moderation

Verwarnungen, Mutes, Kicks und Bans funktionieren als Slash-Befehle und mit Prefix, zum Beispiel `!warn @User spam`. Jede Aktion erzeugt einen Fall mit Nummer.

```
/warn member:@User reason:Spam                    # also: !warn @User Spam
/unwarn case_id:12                                 # remove one warning
/clearwarns user:@User                             # remove all active warnings
/mute member:@User duration:30m reason:Spam        # also: !mute @User 30m Spam
/unmute member:@User
/kick member:@User reason:Advertising
/ban user:@User reason:Raid                        # user can also be an ID
/unban user:123456789012345678

/cases user:@User                                  # history, filter by mention or ID
/cases kind:ban page:2                             # filter by type
/cases search:john                                 # filter by part of a name
/warnings user:@User
/case case_id:12

/escalation list
/escalation set warns:3 action:timeout minutes:60  # 3 warnings = 1 hour timeout
/escalation set warns:5 action:kick
/escalation set warns:7 action:ban                 # actions: timeout, kick, ban, jail
/escalation remove warns:5
```

### Gulag (Jail)

Mitglieder mit gehacktem Account kommen in einen einzigen Channel mit Sicherheitsanleitung. Beim Freilassen bekommen sie ihre alten Rollen zurück.

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
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
/raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3 lockdown:True
# 5 joins within 10 seconds count as a raid, accounts younger than 3 days are punished,
# actions: alert, timeout, kick

/lockdown mode:role reason:Raid                    # instant, edits only the @everyone role
/lockdown mode:channels reason:Raid                # thorough, edits every channel
/unlock

/lockdownconfig mode mode:role                     # default mode
/lockdownconfig lockrole role:@Member              # extra role locked in role mode
/lockdownconfig bypassrole role:@Moderator         # can still write in channels mode
/lockdownconfig exempt channel:#announcements
```

### Anti-Nuke

Überwacht das Audit-Log und reagiert, wenn jemand den Server zerstört. Der Server-Gründer bekommt eine Direktnachricht.

```
/antinuke setup enabled:True action:strip notify_owner:True   # actions: alert, strip, kick, ban
/antinuke limit kind:channel_delete count:3 seconds:10
# kinds: channel_delete, role_delete, channel_create, ban, kick,
#        role_perm, role_grant, webhook_create, bot_add, guild_update
/antinuke whitelist user:@TrustedAdmin             # toggle, never checked
/antinuke staffrole role:@Moderator                # toggle, shown in alerts
/antinuke servername name:MyServer                 # extra name for the nuke talk detection
/antinuke newbots kick:True                        # kick bots added by untrusted users
/antinuke restore member:@User                     # give back roles that were removed
/antinuke status
```

### Verifizierung

Neue Mitglieder sehen nur den Verifizierungs-Channel, bis sie den Button drücken oder das Captcha lösen.

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### Logging

Wähle einen Channel pro Kategorie oder einen Haupt-Channel für alles.

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### Willkommen, Abschied und Booster

Nachrichten, Auto-Rollen und Belohnungen für Server-Booster.

```
/welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/welcome autorole role:@Member                     # toggle, given to every new member
/welcome botrole role:@Bots                        # toggle, given to every new bot
/welcome test

/booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/booster role role:@Booster                        # toggle
```

### Tickets

Mitglieder öffnen per Button private Channels. Beim Schließen wird ein Transkript verschickt.

```
/ticket setup category:Tickets support_role:@Support log_channel:#ticket-logs max_open:1
/ticket addtype key:report label:Report description:Report a member
/ticket removetype key:report
/ticket panel channel:#support title:Support description:Press a button to open a ticket

# inside a ticket
/ticket add member:@User
/ticket remove member:@User
/ticket close
```

### Umfragen und Giveaways

Buttons zum Abstimmen und Teilnehmen. Dauern akzeptieren Werte wie 30m, 2h und 1d.

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### Vorschläge und Starboard

Mitglieder posten Vorschläge, die das Team annehmen oder ablehnen kann, und beliebte Nachrichten werden hervorgehoben.

```
/suggestionsetup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
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

/levelrole add level:10 role:@Active
/levelrole add level:50 role:@Veteran
/levelrole remove level:10
/levelrole list
/levelrole sync                                    # apply to everyone who already has XP

/xp give user:@User amount:500
/xp take user:@User amount:100
/xp setlevel user:@User level:20
/xp reset user:@User

/rank                                              # also: !rank, shows a rank card image
/rank user:@User
/leaderboard
```

### Reaction Roles und Benachrichtigungen

Rollen per Reaktion mit beliebigen Emojis vergeben und Mitglieder ihre Benachrichtigungs-Themen selbst wählen lassen.

```
/reactionrole panel channel:#roles title:Pick your roles description:React below
/reactionrole add message:<message link> emoji:<any emoji> role:@Gamer
/reactionrole add message:<message link> emoji:<any emoji> role:@Artist mode:unique
# mode unique: only one role of that message at a time
/reactionrole remove message:<message link> emoji:<any emoji>
/reactionrole list

/notifytopic add key:events role:@Events description:Server events
/notifytopic panel channel:#roles title:Notifications   # one button per topic
/notifytopic remove key:events
/notify subscribe topic:events                     # members choose for themselves
/notify unsubscribe topic:events
/notify list
```

### Geburtstage

Mitglieder hinterlegen Tag und Monat, der Bot vergibt am Tag eine Rolle und schreibt eine Nachricht.

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Temporäre Voice-Channels

Wer den Hub-Channel betritt, bekommt einen Raum, der verschwindet, wenn er leer ist.

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Backup und Restore

Backups enthalten Rollen, Channels, Emojis, Webhooks und Mitglieder-Rollen. Restore ergänzt nur, was fehlt.

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### Daten und Datenschutz

Mitglieder können ihre eigenen Daten exportieren und löschen. Administratoren legen fest, wie lange Daten gespeichert bleiben.

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### Verwaltung

Module und Befehle an- oder ausschalten, Prefix ändern, Aliase setzen und Befehle auf Rollen beschränken.

```
/module list
/module disable name:starboard
/module enable name:tickets
/command disable name:ban                          # single commands
/command enable name:ban
/command list

/prefix new_prefix:?                               # text commands now start with ?
/alias add alias:w command:warn                    # ?w @User Spam
/alias remove alias:w
/alias list

/perms allow command:ban target:@HeadModerator     # only this role may use /ban
/perms deny command:warn target:@Trainee
/perms reset command:ban
/perms show

/settings
/help
/about
```

## Platzhalter in Nachrichten

Diese Platzhalter werden in den Texten, die du einstellst, ersetzt:

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthdaysetup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## Konfiguration

Globale Optionen stehen in der settings.json. Alles andere wird pro Server mit Befehlen wie /module, /command, /perms, /alias und /config eingestellt.

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

Jede einzelne Einstellung lässt sich mit /config lesen und ändern. Diese Pfade brauchst du am häufigsten:

```
/config get path:automod.caps.percent
/config set path:automod.caps.percent value:80
/config set path:mod.dm_user value:false             # no direct message on punishments
/config set path:mod.warn_expiry_days value:30       # warnings expire after 30 days
/config set path:mod.default_mute_minutes value:120
/config set path:automod.mentions.max value:5
/config set path:automod.phishing.lookalike value:true
/config set path:raid.joins value:8
/config set path:xp.cooldown value:45
/config set path:tickets.max_open value:2
/config set path:privacy.retention_days value:90
/config reset section:welcome                        # back to the defaults of one section
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
