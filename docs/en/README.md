# GuardBot

[Deutsch](../de/README.md) | **English** | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Self-hosted Discord bot for moderation, security and community. Open source, free, and your data stays on your own machine.

> Beta: GuardBot and its dashboard are in a beta phase. They have not been tested thoroughly, especially not on large servers or against every situation on Discord. Expect bugs, keep backups of the data folder and report problems. Use at your own risk.

<!-- toc -->

- [About](#about)
- [Features](#features)
  - [Security](#security)
  - [Moderation](#moderation)
  - [Logging](#logging)
  - [Community](#community)
  - [Administration](#administration)
- [Project status](#project-status)
- [Requirements](#requirements)
- [Quick start](#quick-start)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Start scripts and autostart](#start-scripts-and-autostart)
  - [Updating](#updating)
- [Bot permissions](#bot-permissions)
- [First steps in Discord](#first-steps-in-discord)
  - [Structure, members and team](#structure-members-and-team)
- [Dashboard](#dashboard)
  - [Set up the dashboard](#set-up-the-dashboard)
  - [Commands, skills, AI and bot profile](#commands-skills-ai-and-bot-profile)
  - [Security](#security-1)
  - [Dashboard on a VPS](#dashboard-on-a-vps)
- [Commands](#commands)
  - [Command groups](#command-groups)
  - [Moderation](#moderation-1)
  - [Gulag (jail)](#gulag-jail)
  - [Auto-moderation](#auto-moderation)
  - [Raid protection and lockdown](#raid-protection-and-lockdown)
  - [Anti-nuke](#anti-nuke)
  - [Verification](#verification)
  - [Logging](#logging-1)
  - [Welcome, goodbye and boosters](#welcome-goodbye-and-boosters)
  - [Tickets](#tickets)
  - [Polls and giveaways](#polls-and-giveaways)
  - [Suggestions and starboard](#suggestions-and-starboard)
  - [XP and levels](#xp-and-levels)
  - [Reaction roles and notifications](#reaction-roles-and-notifications)
  - [Birthdays](#birthdays)
  - [Temporary voice channels](#temporary-voice-channels)
  - [Backup and restore](#backup-and-restore)
  - [Data and privacy](#data-and-privacy)
  - [Moderator tools](#moderator-tools)
  - [Information](#information)
  - [Announcements, tags and reminders](#announcements-tags-and-reminders)
  - [Mod-mail and ban appeals](#mod-mail-and-ban-appeals)
  - [Counting, sticky messages and statistics](#counting-sticky-messages-and-statistics)
  - [More options of existing features](#more-options-of-existing-features)
  - [More AutoMod tools](#more-automod-tools)
  - [Moderator limits and permission audit](#moderator-limits-and-permission-audit)
  - [Reports and invite tracking](#reports-and-invite-tracking)
  - [Diagnostics and debugging](#diagnostics-and-debugging)
  - [Music](#music)
  - [Setup and health](#setup-and-health)
  - [Economy](#economy)
  - [Role menus, scheduled messages and feeds](#role-menus-scheduled-messages-and-feeds)
  - [Activity, bulk actions and case search](#activity-bulk-actions-and-case-search)
  - [Anti-scam and anti-crypto](#anti-scam-and-anti-crypto)
  - [Probation, swarm detection, timeline and learning](#probation-swarm-detection-timeline-and-learning)
  - [Panels](#panels)
  - [Skills and AI](#skills-and-ai)
  - [Message builder and updates](#message-builder-and-updates)
  - [Operations](#operations)
  - [Administration](#administration-1)
- [Message placeholders](#message-placeholders)
- [Configuration](#configuration)
- [Data and storage](#data-and-storage)
- [Repository layout](#repository-layout)
- [Translations](#translations)
- [Roadmap](#roadmap)
- [Privacy and security](#privacy-and-security)
- [Support](#support)
- [Credits](#credits)
- [License](#license)

<!-- tocstop -->

## About

GuardBot bundles the features that many servers pay for with hosted bots: moderation, logging, anti-raid, anti-nuke, tickets, levels and more. You run it yourself, on your own computer or on a small VPS.

Hosted bots store your server data, member IDs and sometimes e-mail addresses with a third party. When you host the bot yourself, that data never leaves your machine. GuardBot is meant to show that anyone can run a full-featured bot without a subscription.

## Features

### Security

- Auto-moderation: word filter, caps filter, mention spam, invite links, phishing domains, personal data, doxxing and threats. Every list can be edited.
- Anti-raid with join-rate detection and a server lockdown for all channels.
- Anti-nuke: limits for mass deletions and bans, an automatic response, and a direct message to the server owner.
- Gulag channel: members who post scam links or images are moved to a single channel with account security instructions. Moderators can also use /moderation jail and /moderation unjail.
- Verification gate with a button or captcha, and automatic removal of members who do not verify in time.
- Anti-nuke also watches permission grants, new webhooks, added bots and server renames.
- Anti-scam: fake giveaways and crypto scams are removed in text and images within milliseconds, including the MrBeast scam in any spelling.

### Moderation

- Warn, mute, kick, ban and jail with a case history that can be filtered by mention, user ID or type.
- Automatic escalation, for example three warnings lead to a timeout.
- Choose which roles or users may use each moderation command.

### Logging

- Sent, edited and deleted messages including images, GIFs and URLs, with separate log channels.
- Role, nickname, ban, voice, channel and server role changes.

### Community

- Welcome and goodbye messages, auto roles and booster rewards.
- Tickets, polls, giveaways and suggestions.
- Reaction roles with any emoji and notification topics that members can switch on or off.
- XP and levels from 1 to 100 for chat and voice, level roles and birthdays.
- Starboard and temporary voice channels.
- Timed jail, polls with multiple choices, rank cards as images and XP boosts per role.
- Economy with a shop, role menus with buttons or a dropdown, scheduled messages, YouTube, Twitch and RSS feeds, activity statistics and a guided /admin setup. Messages to members can be shown in 12 languages.

### Administration

- Every module and every single command can be turned on or off per server.
- Custom prefix, command aliases and renamable commands.
- Backup and restore for roles and channel structure.
- Scheduled automatic backups of roles, channels, emojis and webhooks, with a restore command that only adds what is missing.
- Dashboard: change the settings of every server in the browser after a Discord login, only for members who manage the server and only while the bot is connected.
- Skills: custom commands, games and automations from safe building blocks, optionally written by an AI with your own key (Anthropic, OpenAI, Kimi). The dashboard lists every command and edits skills, AI settings and the bot profile.

## Project status

GuardBot is young and has not been used on large servers yet. The automated tests (`python -m unittest`) cover storage, personal data detection, level calculation, command registration, permission checks and the documentation links. Everything that needs a live Discord server, such as lockdown, backup restore, verification, anti-nuke and the gulag, is not covered by them. Try these features on a test server before you rely on them. The translations of the documentation have not been reviewed by native speakers, corrections are welcome.

## Requirements

- Python 3.11 or newer
- A Discord application with a bot token
- A computer or VPS that stays online
- ffmpeg (only for the music module)
- tesseract-ocr (optional, only to read text in images)

## Quick start

Pick your system. Every variant needs Python 3.11 or newer and the token of your bot. The detailed step by step guide is [GUIDE.md](GUIDE.md).

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

### Start scripts and autostart

The start scripts create the virtual environment, install the packages and start the bot. On the first run they create the file .env and stop, so you can enter the token. Start them again afterwards.

```bash
./start.sh
```

```bat
start.bat
```

To keep the bot running after a restart of the computer, use a service. Linux (systemd) and macOS (launchd):

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

On Windows, create a task in the Task Scheduler that runs start.bat when you log in, or use a service wrapper such as NSSM. With Docker, see [GUIDE.md](GUIDE.md).

### Updating

Stop the bot, run these commands and start it again. Your data in the folder data stays untouched, and the bot makes a database backup before every change of the data format.

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

## Bot permissions

The simplest choice is the Administrator permission. If you prefer minimal rights, grant these, and turn on the Server Members and Message Content intents in the Developer Portal:

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

## First steps in Discord

A sensible starting setup. Run these commands on your server and replace the channels and roles with your own:

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

### Structure, members and team

Version 1.5 adds commands to build and keep a server tidy, to restore members who return, and to run the moderation team. Every part has a module switch (`/admin module`), its own settings and a place in the dashboard.

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

- Channels and categories are created, cloned, renamed, sorted and given the permissions of another channel with `/structure`. Inactive channels are reported or moved to an archive category (`/structure archive`). Roles can be given for a limited time and saved as templates; a template never grants a permission the person who applies it does not have.
- `/structure rules` posts the rules with an accept button and a version number. After `post new_version:True` members who did not accept the new version get one reminder by direct message.
- `/members stickyroles` gives roles back and restores a timeout or a mute when a member returns. `/members nickname` removes hoisting characters, checks banned words in nicknames and user names and renames offenders. The watch list is silent: the team is alerted at the first message of a listed user.
- Four-eyes approval (`/security approval`) lets bans, kicks, timeouts and bulk actions run only after a second moderator agrees. `/moderation case undo` takes a case back, including the actions it caused (for example a mute and the ban that followed). Warnings can expire after a number of days (`/moderation escalation expiry`).
- `/admin history` shows who changed which setting and when and rolls a section back. The name of the person is a guess from the latest commands and dashboard changes on the server. `/admin history copy` copies sections to another server where you may manage the bot; it starts as a dry run. `/admin exceptions` leaves channels and roles out of AutoMod rules and Anti-Scam. `/admin dashaccess` gives roles read only or moderator access to the dashboard.
- `/team` shows the work of every moderator (cases, tickets, reports, response time, inactive members), posts a weekly report (day and hour are UTC), lets moderators sign off with `/team duty away` so tickets and pings go to others, and runs staff applications with a form and a vote of the team.
- Discord cannot hide commands inside a group from single members. The bot still checks every call. Numbers in the team statistics are counted from the day the module was updated; older actions are not included.

## Dashboard

The dashboard is a web page that runs inside the bot. After you sign in with Discord you can change the settings of your servers with switches, menus and fields instead of commands: modules, channels, roles, thresholds, texts, the prefix and the language. It also shows the latest moderation cases and exports and imports settings. It works the same on your own computer and on a VPS, and it is off until you turn it on.

### Set up the dashboard

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

### Commands, skills, AI and bot profile

The dashboard has five more pages: Panels (see the section Panels) and the following four. Commands lists every slash command, prefix command and context menu with its module, the permission it needs and whether it is on; administrators switch them on or off, allow or deny roles, and give prefix commands short names. The prefix is changed on the same page. Skills shows all skills and edits them as JSON with the same checks as the commands. AI sets model and limits and stores a key (write only, it is never sent back to the page). Bot profile changes the name, picture, banner and about text of the bot on this server; the owner of the bot application, or an ID listed in `owner_ids` in settings.json, can also change them everywhere. Discord limits how often the name and picture may change. Every change is written to the audit log.

Every module appears as a plugin: the page Plugins shows them as cards by category, and each plugin has its own page with the switch Active, its settings in boxes that open and close, and its commands with a switch and a role editor. The left bar lists the plugins by category with a dot that shows whether they are on. The dashboard uses a dark design.

The dashboard can be shown in all 12 languages of the bot. Pick the language at the top right or on the sign-in page; the choice is kept in the browser and does not change the language of the server. The dashboard texts are machine translated.

Every plugin page explains what the plugin does, lists all of its functions with their own switch and a short explanation, and keeps the other settings in boxes below. On the Plugins page and the overview every plugin can be switched on or off directly. In Settings, the box Dashboard appearance changes the accent colour, background, boxes and text, sets a wallpaper (darkened and blurred as you like) and adds own menus and tabs to the side bar: a tab can collect chosen plugins, open a page, link to an https address or show a note. The look is stored per server and seen by everyone who opens its dashboard. The footer shows the copyright and links to Discord and GitHub; to show the official logos there, put discord.svg and github.svg from the brand pages of Discord and GitHub into guardbot/web/brand/.

### Security

- Login only with Discord (OAuth2, scope identify). The access token is revoked at once and never stored.
- Only the owner of a server and members with the Administrator or Manage Server permission get access, and only to that server. The permission is checked again on every request.
- Only servers where the bot is connected right now can be opened. If the bot is offline, not on the server or still starting, the dashboard refuses everything. The dashboard runs inside the bot and has no database or service of its own.
- By default it listens only on 127.0.0.1, so nobody else on the network can reach it. A public address is accepted only with HTTPS, otherwise the dashboard does not start.
- Sessions use a random token in an HttpOnly cookie with SameSite and, under HTTPS, the __Host- prefix. They end after 8 hours and live only in memory, so a restart signs everyone out.
- Every change needs a CSRF token and a matching Origin. The Host header is checked against DNS rebinding. The page loads no outside scripts, a strict Content Security Policy blocks inline code, requests are rate limited and bodies are limited to 256 KB.
- Every value is checked against the type of the setting and Discord IDs must exist on the server. Internal state such as counters, tickets and stored items cannot be edited. Each change is written to the security log channel of the server.
- Message content is never shown. Moderation cases are read only.

### Dashboard on a VPS

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

The settings editor shows every setting that is a switch, a number, a text, a channel, a role or a simple list. Things that are created with commands, such as shop items, role menus, feeds, tags and tickets, stay commands. The page is available in English and German and follows the language of your browser. In Docker, publish the port only on 127.0.0.1 (127.0.0.1:8080:8080), set host to 0.0.0.0 and allow_insecure_http to true inside the container.

## Commands

Most commands are slash commands, moderation commands also work with a prefix. The complete list is in the command reference: [COMMANDS.md](../COMMANDS.md).

<!-- groups -->
### Command groups

To save slash command slots (Discord allows 100 top-level commands per bot), related commands are grouped. Type the group first, then the command, for example `/moderation ban`. Text commands with the prefix, for example `!ban`, are not affected. Permissions, aliases and module switches keep using the plain command name.

| Group | Contains |
| --- | --- |
| `/moderation` | `warn`, `unwarn`, `warnings`, `clearwarns`, `note`, `mute`, `unmute`, `kick`, `ban`, `unban`, `tempban`, `jail`, `unjail`, `jailed`, `role`, `case`, `cases`, `bulk`, `escalation`, `purge`, `slowmode` |
| `/security` | `antinuke`, `antiscam`, `raid`, `block`, `unblock`, `blocklist`, `approval` |
| `/access` | `verify`, `probation`, `lockdown`, `lockdownconfig`, `unlock`, `lockchannel`, `unlockchannel`, `jailsetup` |
| `/server` | `log`, `backup`, `privacy`, `invites`, `stats`, `serverinfo`, `roleinfo`, `health`, `diagnose`, `debug` |
| `/admin` | `settings`, `config`, `module`, `command`, `perms`, `alias`, `prefix`, `language`, `setup`, `history`, `exceptions`, `dashaccess` |
| `/info` | `about`, `avatar`, `botinfo`, `ping`, `userinfo`, `mydata`, `leaderboard`, `rank`, `find` |
| `/community` | `welcome`, `booster`, `afk`, `remind`, `activity`, `tempvoice`, `voice` |
| `/engage` | `economy`, `giveaway`, `poll`, `counting`, `starboard` |
| `/support` | `ticket`, `suggest`, `tag`, `autoresponder` |
| `/members` | `stickyroles`, `nickname`, `watch`, `reason` |
| `/structure` | `channel`, `category`, `archive`, `temprole`, `roletemplate`, `rules` |
| `/team` | `teamstats`, `weekly`, `duty`, `apply`, `modwatch`, `permaudit` |
| `/post` | `say`, `embed`, `message`, `sticky`, `schedule`, `feed`, `reactionrole`, `rolemenu` |
| | `/help`, `/play`, `/automod`, `/music`, `/xp`, `/modmail`, `/appeal`, `/report`, `/suggestion`, `/birthday`, `/notify` |

### Moderation

Warnings, mutes, kicks and bans work as slash commands and with the prefix, for example `!warn @User spam`. Every action creates a case with a number.

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

### Gulag (jail)

Members with a hacked account are moved to one channel with security instructions. Their old roles are restored on release.

```
/access jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/access jailsetup apply                                   # apply the channel permissions again
/access jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/access jailsetup preview
/access jailsetup reminder notice:True reminder:True minutes:10 requests:True word:unban

/moderation jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/moderation jail member:@User duration:2h                     # released automatically after 2 hours
/moderation unjail member:@User reason:Account secured
```

Everyone who comes into the gulag, by command, by AutoMod, by the anti-scam check, by rejoining or because someone gave the gulag role by hand, gets the Account Security Required notice with a mention. While someone is in the gulag, an Account Recovery Reminder stays at the bottom of the channel and is renewed every 10 minutes. A member in the gulag who writes the prefix and the release word (for example `!unban`) in the gulag channel creates a release request with Release and Keep buttons for the staff; the bot never releases anyone on its own. `/access jailsetup reminder` switches each part on or off and sets the interval and the word.

### Auto-moderation

Rules delete or punish matching messages. Choose the action per rule: log, delete, warn, timeout or jail.

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

### Raid protection and lockdown

Detects many joins in a short time and can lock the server. Mode channels edits every channel, mode role is instant.

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

### Anti-nuke

Watches the audit log and reacts when someone destroys the server. The server owner gets a direct message.

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

### Verification

New members only see the verification channel until they press the button or solve the captcha.

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

Choose a channel per category, or one main channel for everything.

```
/server log set category:main channel:#logs               # fallback for every category
/server log set category:messages channel:#log-messages
/server log set category:moderation channel:#log-moderation
/server log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/server log sent enabled:False                            # stop logging every sent message
/server log show
```

### Welcome, goodbye and boosters

Messages, auto roles and rewards for server boosters.

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

Members open private channels with a button. Closing a ticket sends a transcript.

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

### Polls and giveaways

Buttons for voting and joining. Durations accept values like 30m, 2h and 1d.

```
/engage poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/engage poll end poll_id:3
/engage poll list

/engage giveaway start prize:Nitro duration:2d winners:2 role:@Member
/engage giveaway end giveaway_id:1
/engage giveaway reroll giveaway_id:1
/engage giveaway list
```

### Suggestions and starboard

Members post suggestions that staff can approve or deny, and popular messages are highlighted.

```
/suggestion setup set channel:#suggestions review_role:@Staff
/support suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/engage starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/engage starboard ignore channel:#spam
```

### XP and levels

XP for chat and voice, level roles, role boosts and rank cards.

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

### Reaction roles and notifications

Give roles for reactions with any emoji and let members choose their own notification topics.

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

### Birthdays

Members store day and month, the bot gives a role and posts a message on the day.

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Temporary voice channels

Joining the hub channel creates a room that disappears when it is empty.

```
/community tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Backup and restore

Backups contain roles, channels, emojis, webhooks and member roles. Restore only adds what is missing.

```
/server backup create name:before-update
/server backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/server backup list
/server backup download name:before-update
/server backup restore name:before-update member_roles:True   # only adds what is missing
/server backup delete name:before-update
```

### Data and privacy

Members can export and delete their own data. Administrators control how long data is kept.

```
/info mydata export                                     # members download their own data
/info mydata delete confirm:True                        # members delete their XP and birthday

/server privacy retention days:90                         # delete data of members who left after 90 days
/server privacy export user_id:123456789012345678
/server privacy delete user_id:123456789012345678 cases:True
```

### Moderator tools

Clean up channels, manage roles and keep private notes. Every action is logged.

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

### Information

Look up users, the server, roles and the bot.

```
/info userinfo user:@User
/server serverinfo
/server roleinfo role:@Moderator
/info avatar user:@User
/help command:ban                                  # explains one command
/info ping
/info botinfo
```

### Announcements, tags and reminders

Post in the name of the bot, create custom commands, auto-answer messages and set reminders.

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

### Mod-mail and ban appeals

Members talk to the staff through a private channel on the server. Nobody has to send the bot a direct message.

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

### Counting, sticky messages and statistics

A counting game, messages that stay at the bottom of a channel and channels that show live numbers.

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

### More options of existing features

Additions to tickets, giveaways, voice rooms, XP, birthdays, backups, logs and the status views.

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

### More AutoMod tools

Follow short links, restrict links for new members, find ghost pings and test rules without punishing anyone.

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

### Moderator limits and permission audit

Get an alarm when a moderator bans or kicks too much, and see which roles hold dangerous permissions.

```
/team modwatch status
/team modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/team modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/team modwatch exclude member:@TrustedMod

/team permaudit run                                                  # roles with dangerous permissions and who holds them
/team permaudit watch enabled:True                                   # alarm when a role or member gets one
/team permaudit trust role:@Admin
```

### Reports and invite tracking

Members report messages to the staff, and the bot records which invite brought each new member.

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

### Diagnostics and debugging

Find missing permissions and broken settings, receive error reports in a channel, and export or import the settings.

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

### Music

Plays links and files from the music folder in a voice channel. Downloads are saved as music/Artist/Album/Track. It needs ffmpeg and the packages from requirements.txt.

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

/music sources spotify:True apple_music:True tidal:True search:youtube
/music playlist save name:Evening
/music playlist play name:Evening shuffle:True
/music stay enabled:True channel:#Lounge playlist:Evening

/music settings dj_role:@DJ volume:50 max_queue:100 per_user:25 max_minutes:60 idle_leave:120
/music settings allow_links:True allow_search:True allow_playlists:True library:True
/music settings allow_download:True download_format:best announce:True
/admin config set path:music.allowed_hosts value:bandcamp.com,archive.org
/music cleardj
/music status
```

Lossless: files you add yourself (FLAC, WAV, ALAC) and sources that offer FLAC are played unchanged. YouTube, SoundCloud and similar sites only offer lossy audio, and nothing can make that lossless afterwards. Discord transmits voice as Opus, the bot uses the bitrate of the voice channel. Responsibility: downloading and playing content can violate the terms of a website or copyright law. Downloads are off by default and the module is off until you enable it. The operator of the bot is responsible for what is played and saved.

Sources: YouTube and SoundCloud links and searches are played directly. Spotify, Apple Music and Tidal links are accepted too, but these services do not hand out their audio: the bot reads title and artist from the public page and plays the same song from the search source (YouTube or SoundCloud, set with /music sources). Albums and playlists of Spotify and Apple Music are read from their public pages; Tidal albums and playlists need a free developer key from developer.tidal.com in .env (TIDAL_CLIENT_ID and TIDAL_CLIENT_SECRET). Files in your music folder are played as they are. Saved playlists can mix all sources, and /music stay keeps the bot in a voice channel around the clock and plays a playlist on repeat, also after a restart.

Guard Music, the second bot: the music can run on its own bot account, so it can stay in a voice channel all the time and moderation is not affected by it.

1. Create a second application in the Discord Developer Portal, name it Guard Music and copy the token of its bot.
2. Write the token into .env as MUSIC_TOKEN and set music_bot.enabled to true in settings.json.
3. Restart GuardBot. Guard Music starts in the same process, uses the same settings and data, and the music commands move to it.
4. Open the page Music in the dashboard and add Guard Music to the server with the button there. Without MUSIC_TOKEN the music stays inside GuardBot.

Use at your own risk: streaming from YouTube and other services can break their terms of use, and copyright applies to what is played. Nothing is downloaded from Spotify, Apple Music or Tidal and no protection is bypassed. The operator of the bot is responsible for what is played. The dashboard page Music shows the player, the queue, the playlists, the 24/7 mode, the sources and this guide.

### Setup and health

A guided assistant sets up the most important things with buttons and menus: log channel, welcome channel, staff roles, the gulag, an AutoMod preset (loose, normal, strict), a server template (community, gaming, support) and the language. /server health shows what is set up and what is still open. The language changes the texts that members see, such as default welcome messages, AutoMod notices, verification, tickets, appeals, mod-mail and role menus. Fixed replies to administrators are translated, replies with names and numbers stay in English.

```
/admin setup                                                         # buttons and menus, nothing is switched off by a template
/server health                                                        # what is set up, what is open, and the self-test
/admin language code:de
```

### Economy

A server currency with a daily reward, work, payments, a leaderboard and a shop whose items can give a role. Switch it on with the economy module. The commands also work with the prefix, for example !economy daily.

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

### Role menus, scheduled messages and feeds

Role menus give roles with buttons or a dropdown. Scheduled messages are posted once or repeated hourly, daily or weekly. Feeds post new YouTube videos, Twitch streams and RSS items. For YouTube use the channel ID (it starts with UC). Twitch needs TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET in .env. Times are written as in 2h, 18:30 or as a date with a time like 2026-12-24 18:00 in the time zone of the server. The first check of a feed only remembers what already exists.

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

### Activity, bulk actions and case search

Activity counts messages per channel and joins and leaves per day, never content or names. Bulk actions ban, kick or time out up to 25 users after a confirmation. Cases can be searched by user, type, name, reason, moderator and age, and linked to each other, for example a note to a ban.

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

### Anti-scam and anti-crypto

Removes fake giveaways, such as the typical MrBeast scam, in text and in images within milliseconds. Names on the instant list are removed on sight in any spelling (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Otherwise words from the lists (names, bait, crypto, links, amounts) add up and the message is removed at the threshold. Images are read with OCR, and images that were judged as scam once are removed without reading them again. Reading images needs tesseract, without it only text is checked. A server about MrBeast can remove the name from the instant list or exempt channels with /automod exemptchannel. Try it with /security antiscam test before you rely on it.

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

### Probation, swarm detection, timeline and learning

Probation puts new members into a role. Until they wrote the set number of normal messages or the minutes passed, links, invites and files are removed with a short notice. Raid protection can also recognise a swarm: several new accounts with the same name pattern, the same profile picture or created within minutes of each other. The timeline of a case search (/moderation case timeline) merges account creation, join and invite, probation, cases and appeals of one user in time order. Messages are never stored, so they are not part of it. /security block, /security unblock and /security blocklist manage the blocklist of AutoMod with short commands. Moderators teach the anti-scam module with the context menu entry Mark as scam on a message, or with a reaction with the emoji set by learn_emoji: the message is deleted and its images and text are removed at once from then on. Switch each part off with its module or its settings.

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

### Panels

Panels are posts such as a welcome post, rules, a role choice, notification buttons or a verification gate, with banner pictures, text boxes and buttons. They are built with `/panel` or in the dashboard on the page Panels. Pictures are uploaded there or as options of the command and stored by the bot in `data/panels`, so they keep working.

```
/panel create name:welcome template:welcome channel:#welcome
/panel section name:welcome banner:image.png
/panel section name:welcome number:1 color:#5865f2 thumbnail:logo.png
/panel create name:origin template:roles
/panel button name:origin kind:role label:KL role:@KL
/panel button name:origin kind:role label:Kreis role:@Kreis
/panel single name:origin value:True
/panel create name:check template:verify
/panel button name:welcome kind:link label:Website url:https://example.com
/panel preview name:welcome
/panel post name:welcome
/panel update name:welcome
/panel list
/panel show name:welcome
/panel removesection name:welcome number:2
/panel removebutton name:origin number:1
/panel delete name:welcome messages:True
```

Templates: empty, welcome, rules, roles, notifications and verify; their texts are in the language of the server and can be changed. `/panel section` opens a form for title, text and footer. Each section becomes one message: the banner above the box, the large picture inside it, the small picture at the top right. Buttons sit under the last section, five per row. A role button gives the role or takes it back; with `single` on, the other roles of the panel are taken away. The verify button starts the verification of the verification module (`/access verify setup` decides between button, captcha and math). Texts can use `{server}` and `{count}`. `/panel update` changes the posted messages after an edit. Limits per server: 25 panels, 5 sections and 20 buttons per panel, 40 pictures of up to 8 MB. The bot only offers roles that are below its own highest role and have no dangerous permission.

### Skills and AI

Skills are commands, games and automations that a server builds itself from safe building blocks. They need no AI and can never run code. An AI is optional: with your own key it writes a skill from a description and gives a second opinion in the anti-scam check.

Skills without AI:

- `/support skill create kind:command name:hello` opens a box with a small example that you change. `/support skill edit`, `show`, `import`, `enable`, `disable`, `delete`, `list` and `stats` manage them. Everyone uses a skill with `/support skill run` or with the prefix, for example `!hello`. `/support skill panel` posts buttons that run skills.
- Kinds: command (a list of actions), game (dice, choice, slots, rock paper scissors, quiz) and automation (starts when a member joins or leaves, when a message contains words, or when a button is pressed).
- Actions: reply, send to a channel, direct message, log, add or remove a role, change a counter, give coins, choose at random. An action can have conditions: has a role, chance, a counter compared with a number.
- Texts can use `{user}`, `{user_name}`, `{server}`, `{channel}`, `{count}`, `{arg1}`, `{arg2}`, `{var:name}`, `{uvar:name}` and `{random:1-6}`.
- Limits: 50 skills per server, 10 actions per skill, 3 role changes and 4 messages per skill. The bot only hands out roles that are below its own highest role and have no dangerous permission. A skill that gives coins needs a cooldown of at least 60 seconds. Names of bot commands, aliases and tags cannot be used.
- Skills are stored as JSON and are part of the settings export. Unknown fields are refused, so a skill from anywhere can do only what the building blocks allow.

Example, a command that gives a role and counts uses (replace the role ID):

```json
{
  "name": "join-team",
  "kind": "command",
  "description": "Join the team once",
  "cooldown": 60,
  "actions": [
    {"do": "add_role", "role": 123456789012345678, "if": [{"not": {"has_role": 123456789012345678}}]},
    {"do": "add_var", "name": "joined", "amount": 1},
    {"do": "reply", "text": "Welcome, {user}! {var:joined} members joined so far."}
  ]
}
```

AI connection (optional):

- `/support ai setup provider:kimi agree:true` opens a private box for your API key. Providers are Anthropic, OpenAI and Kimi (Moonshot). A model is suggested and can be changed in the same command or in the dashboard; model names change at the providers, so check their documentation. You pay your provider.
- `/support ai make wish:...` asks the AI for a skill, checks the answer as strictly as an imported skill and shows a preview. Nothing is saved before you press Save.
- `/support ai status`, `limits` (requests per day, seconds between requests per person) and `remove` finish the set. The key is stored encrypted, with the file `data/ai.secret` as secret. Keep that file with your backups; without it a stored key cannot be read and has to be entered again. The key is never shown, logged or exported. The provider can only change together with a new key, so a key never goes to another provider.
- What is sent: the wish of `/support ai make`, and with the second opinion the text of a suspicious message. Nothing else, and only while the module `ai` is on. See [PRIVACY.md](../PRIVACY.md).

Anti-scam learning:

- The learned filter (`/security antiscam set learned:true`) is a small classifier per server. Moderators train it with the context menu entries "Mark as scam" and "Not a scam". It stores only short hashes of words, never the text, acts only after it has seen 8 scam and 30 normal examples, and then only above 95 percent. With `ham_sampling` it also learns from a tenth of the normal messages.
- Similar images (`similar`, on by default) compare a picture fingerprint with known scam pictures, so a re-saved or resized copy is found. This works without Tesseract.
- AI second opinion (`/support ai limits second_opinion:true`): for cases just under the threshold, or that the learned filter finds suspicious, the AI is asked. A message is only removed when the AI answers scam with at least 80 percent confidence, and its answer cannot do anything else.

### Message builder and updates

The message builder posts messages with several embeds and link buttons from JSON. It reads the JSON that embed generators such as Embed Generator export, so you can design a message there and post it with the bot. Give the JSON as text, as a .json file or as an https link that points straight to the JSON, for example the raw file of a repository (links that redirect are refused). Only link buttons are created, buttons that need an interaction are skipped. Every link must be http or https, mentions in the text never ping, and the limits of Discord apply. /post message copy exports an existing message as JSON, /post message edit changes a message of the bot and /post message preview shows the result only to you. Share links of web editors are not opened, because their format is not public.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

The bot checks the GitHub repository from update.repo (set by scripts/set_repo_url.py) for a newer release every 12 hours. When there is one, the owner of the bot gets a direct message with the release notes, and the release is downloaded and checked: SHA-256 checksum of the release, safe paths inside the archive and a version that matches the tag. It is installed with /server debug update action:install, or by itself when auto_install is on. Before installing, the replaced files are saved in data/update, new packages are installed and the new code is test-imported. If anything fails, the old files are restored. Your .env, settings.json, data and music are never touched. Then the bot restarts itself. In Docker nothing is installed in place, update the image instead. An update runs code from the repository, so only point it at a repository you trust. Turn it off with enabled set to false.

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

### Operations

The bot saves its data every few seconds and keeps database backups in data/dbbackups, one before every change of the data format and one per day. The music queue, sticky messages and moderator counters survive a restart. Large bots can run on several shards. A heartbeat file and an optional status page help monitoring tools. These options are set in settings.json:

```json
{
  "shard_count": null,
  "message_cache": 10000,
  "members_intent": true,
  "chunk_guilds": true,
  "db_backup_hours": 24,
  "db_backup_keep": 7,
  "health_port": 0,
  "health_host": "127.0.0.1",
  "metrics_token": "",
  "log_format": "text",
  "log_max_mb": 2,
  "log_backups": 3,
  "workers": {"ocr": {"threads": 2, "limit": 20}},
  "tesseract": null,
  "music_generic": true
}
```

```
/server debug db action:backup                                         # owner of the bot only, saved in data/dbbackups
/server debug db action:list
```

Logs are written to data/guardbot.log (rotating, see log_max_mb and log_backups). Set log_format to json for one JSON object per line with the server and the command. With health_port set, /metrics serves Prometheus metrics (uptime, latency, memory, database size, errors, command uses and durations, work lanes). Only counts are exported, never names or IDs, and metrics_token makes a bearer token necessary. Heavy work (reading images, drawing cards, music files, backups) runs in lanes with fixed threads and a limit (workers in settings.json). When a lane is full the bot says it is busy instead of piling up work. Every database backup is opened and checked right after it is made. To restore one, stop the bot and run:

```
python scripts/restore_db.py data/dbbackups/guardbot-YYYYMMDD-HHMMSS-auto.db
python scripts/restore_db.py BACKUPFILE --check          # only check a backup
```

The current database is kept as a backup named before-restore.

### Administration

Turn modules and commands on or off, change the prefix, set aliases and restrict commands to roles.

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

## Message placeholders

These placeholders are replaced in the texts you configure:

```
/community welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/community booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/community tempvoice setup     name                            {name}
/access jailsetup notice    text                            {staff}
```

## Configuration

Global options are set in settings.json. Everything else is configured per server with commands such as /admin module, /admin command, /admin perms, /admin alias and /admin config.

To rename a command, add it to command_names and restart the bot:

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

Every single setting can be read and changed with /admin config. These paths are the ones you will use most:

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

## Data and storage

Everything the bot stores lives on your own machine:

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

## Repository layout

```
guardbot/
  main.py                 entry point
  requirements.txt
  settings.example.json   global options
  .env.example            token placeholder
  guardbot/
    core.py               bot class, storage, permission checks
    defaults/             default settings, one file per area (core, security, moderation, community) and base.py for modules and permissions
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature, in the folders security, moderation, server, community, tools
    skills.py             skills engine: checks and runs skills
    ai.py                 AI providers, encrypted keys, limits
    learner.py, imgsim.py learned anti-scam filter, picture fingerprints
    dashboard_manage.py   dashboard pages for commands, skills, AI and profile
  docs/                   documentation in 12 languages, COMMANDS.md, PRIVACY.md
  deploy/                 systemd service, Dockerfile, compose file
  scripts/                maintenance scripts
  tests/                  automated tests (python -m unittest)
  data/                   created at runtime, holds your settings and data
```

## Translations

English is the original language of the project. All translations of the documentation, the dashboard and the bot messages were created with machine translation and have not been checked by native speakers. Expect awkward wording and mistakes, and please report them or send a correction. The files are in docs/ and guardbot/locales/.

## Roadmap

- Charts for activity and moderation in the dashboard.
- Review of all translations by native speakers.
- More fixed reply texts translated.

## Privacy and security

- No telemetry. The bot talks to Discord and, for the update check, to GitHub (no personal data is sent, switch it off with update.enabled). Links that administrators give it, such as feeds, music and JSON links, are only opened on request.
- All data is stored in the data folder on your machine: settings, XP, birthdays (day and month only) and moderation cases.
- The bot ignores direct messages from members.
- The token is read from the .env file. Never share it and never commit it.
- Members can export and delete their own data with /info mydata. Administrators can set how long data of members who left is kept.
- AI features are off until you add your own key. Then only the text of `/support ai make` and, with the second opinion, suspicious messages are sent to the provider you chose.
- [PRIVACY.md](../PRIVACY.md)

## Support

Bugs, ideas and suggestions: write to me on Discord, @justyyin, or open an issue on GitHub.

## Credits

GuardBot is inspired by [Embed Generator](https://github.com/merlinfuchs/embed-generator) by Merlin Fuchs (MIT license, hosted at message.style). The message builder reads the same JSON format, so messages designed there can be posted with this bot. No code of that project is included. Thanks to the authors of discord.py, aiohttp, Pillow, yt-dlp, mutagen and Tesseract.

## License

Released under the MIT License. See [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
