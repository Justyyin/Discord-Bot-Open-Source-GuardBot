# GuardBot

[Deutsch](../de/README.md) | **English** | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Self-hosted Discord bot for moderation, security and community. Open source, free, and your data stays on your own machine.

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
- [Repository layout](#repository-layout)
- [Commands](#commands)
- [Configuration](#configuration)
- [Roadmap](#roadmap)
- [Privacy and security](#privacy-and-security)
- [Support](#support)
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
- Gulag channel: members who post scam links or images are moved to a single channel with account security instructions. Moderators can also use /jail and /unjail.
- Verification gate with a button or captcha, and automatic removal of members who do not verify in time.
- Anti-nuke also watches permission grants, new webhooks, added bots and server renames.

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

### Administration

- Every module and every single command can be turned on or off per server.
- Custom prefix, command aliases and renamable commands.
- Backup and restore for roles and channel structure.
- Scheduled automatic backups of roles, channels, emojis and webhooks, with a restore command that only adds what is missing.

## Project status

GuardBot is young and has not been used on large servers yet. The automated tests (`python -m unittest`) cover storage, personal data detection, level calculation, command registration, permission checks and the documentation links. Everything that needs a live Discord server, such as lockdown, backup restore, verification, anti-nuke and the gulag, is not covered by them. Try these features on a test server before you rely on them. The translations of the documentation have not been reviewed by native speakers, corrections are welcome.

## Requirements

- Python 3.11 or newer
- A Discord application with a bot token
- A computer or VPS that stays online

## Quick start

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

The full step-by-step guide is in [GUIDE.md](GUIDE.md).

## Repository layout

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

## Commands

Most commands are slash commands, moderation commands also work with a prefix. The complete list is in the command reference: [COMMANDS.md](../COMMANDS.md).

## Configuration

Global options are set in settings.json. Everything else is configured per server with commands such as /module, /command, /perms, /alias and /config.

To rename a command, add it to command_names and restart the bot:

```json
{
  "prefix": "!",
  "command_names": {
    "warn": "verwarnen"
  }
}
```

## Roadmap

- Local web dashboard that runs on your own machine, so settings can be changed without any hosted service.
- Translated bot messages.
- Export and import of settings.

## Privacy and security

- No telemetry and no external services. The bot only talks to Discord.
- All data is stored in the data folder on your machine: settings, XP, birthdays (day and month only) and moderation cases.
- The bot ignores direct messages from members.
- The token is read from the .env file. Never share it and never commit it.
- Members can export and delete their own data with /mydata. Administrators can set how long data of members who left is kept.
- [PRIVACY.md](../PRIVACY.md)

## Support

Bugs, ideas and suggestions: write to me on Discord, @justyyin, or open an issue on GitHub.

## License

Released under the MIT License. See [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
