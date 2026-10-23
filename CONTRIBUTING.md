# Contributing

Bug reports, ideas and pull requests are welcome.

- Open an issue on GitHub or write to Discord: justyyin
- One topic per pull request, small commits with a clear message
- Do not commit tokens, `.env`, `settings.json` or the `data` folder
- Write a docstring for every module, class and function
- Do not ignore errors. Catch the specific exception, log it with `log.warning` or `log.exception`, and tell the user or the staff when the failure matters
- Run `python -m unittest` and `python -m pyflakes guardbot tests scripts main.py` before you open a pull request
- Features that need a live Discord server cannot be covered by the automated tests, so describe how you tried them
- New texts that members see go through `guardbot/i18n.py`: the English text is the key, add the translation to every file in `guardbot/locales/` (a test checks that all files are complete and keep the placeholders)
- New slash commands count against the limit of 100 per bot. Put related commands in a group instead of a new top-level command

## Releases

1. Add the entry at the top of `CHANGELOG.md` under `## <version>`
2. Set `__version__` in `guardbot/__init__.py` to the same version
3. Create and push the tag: `git tag v<version> && git push origin v<version>`

The release workflow checks that tag and version match, runs the tests, takes the notes from the changelog and publishes the release with a zip of the sources.

## Where is what

Source files are in `guardbot/`: `core.py` (bot and start-up), `store.py` (SQLite storage), `tree.py` (slash command tree), `checks.py` (permission checks and team helpers), `layout.py` (command groups), `defaults/` (all settings, one file per area), `cog.py` (base class of the cogs), `workers.py` (lanes for heavy work), `metrics.py` and `logsetup.py` (monitoring), `migrations.py` (changes of the stored data), `dashboard.py`. Every feature is a cog in `guardbot/cogs/`, sorted into the folders security, moderation, server, community and tools:

| File | Purpose | Command group |
| --- | --- | --- |
| `community/activity.py` | Member statistics: busiest channels, messages per day and member growth. Only counts are stored, never content or names | `/community` |
| `server/admin.py` | Server administration: modules, command switches, prefix, aliases, permissions and raw settings | `/admin`, `/help`, `/info` |
| `security/antinuke.py` | Protection against mass deletions, permission grants, webhooks, new bots and renames | `/security` |
| `security/antiscam.py` | Anti-scam and anti-crypto detection for text and images. Removes fake giveaways such as the typical MrBeast scam at once | `/security` |
| `moderation/appeals.py` | Ban appeals through an appeal server. The bot never reads direct messages: banned users use /appeal on a second server | `/admin`, `/appeal` |
| `server/applications.py` | Staff applications: a form for members and a vote of the team | `/team` |
| `moderation/approval.py` | Two-person rule: serious actions (ban, kick, temporary ban, bulk actions) wait until a second moderator approves them | `/security` |
| `security/automod.py` | Automatic moderation rules, blocklist, flood protection and personal data detection | `/automod` |
| `server/backup.py` | Backup and restore of roles, channels, emojis, webhooks and member roles | `/server` |
| `community/birthday.py` | Birthdays with a role and a message on the day | `/admin`, `/birthday` |
| `tools/builder.py` | Message builder: post, edit, preview and copy messages with embeds and link buttons from JSON, a file or a link | `/post` |
| `moderation/bulk.py` | Bulk actions: ban, kick or time out several users at once, after a confirmation | `/moderation` |
| `server/channels.py` | Special channels: counting game, sticky messages and statistics channels | `/engage`, `/post`, `/server` |
| `community/community.py` | Starboard and temporary voice channels | `/community`, `/engage` |
| `server/debug.py` | Diagnostics: configuration self-test, error reports, usage statistics and database maintenance | `/server` |
| `community/economy.py` | Server currency: daily reward, work, payments, a shop with roles and a leaderboard | `/engage` |
| `community/engage.py` | Polls, giveaways and suggestions | `/admin`, `/engage`, `/suggestion`, `/support` |
| `security/exceptions.py` | Exceptions per channel and role for AutoMod rules and for the anti-scam check | `/admin` |
| `community/feeds.py` | Feeds: new videos of a YouTube channel, streams of a Twitch channel and any RSS or Atom feed | `/post` |
| `moderation/history.py` | History of settings changes with rollback, and copying settings from one server to another | `/admin` |
| `tools/info.py` | Information commands: userinfo, serverinfo, roleinfo, avatar, ping and botinfo | `/info`, `/server` |
| `server/invites.py` | Invite tracking: shows which invite and which member brought a new member, and warns about invite abuse | `/server` |
| `moderation/jail.py` | The gulag: restricted channel for hacked accounts, with optional release time | `/access`, `/moderation` |
| `community/leveling.py` | XP and levels for chat and voice, level roles, boosts and rank cards | `/info`, `/levelrole`, `/xp` |
| `server/logs.py` | Audit logging of messages, members, roles, channels, voice and server changes | `/server` |
| `moderation/members.py` | Member management: sticky roles, name moderation, watch list and reason templates | `/members` |
| `moderation/moderation.py` | Warnings, mutes, kicks, bans, case history and automatic escalation | `/moderation` |
| `moderation/modmail.py` | Mod-mail: members contact the staff privately through the server. The bot never reads direct messages | `/admin`, `/modmail` |
| `security/modwatch.py` | Watches the staff: raises an alarm when a moderator uses ban, kick, timeout and similar actions too often | `/team` |
| `community/music.py` | Music: plays links and files of the local library in voice channels and downloads into a structured library | `/music`, `/play` |
| `security/permaudit.py` | Permission audit: lists roles with dangerous permissions and warns when new ones appear | `/team` |
| `server/privacy.py` | Data export, deletion and retention | `/info`, `/server` |
| `security/probation.py` | Probation: new members get a role and may not post links or files until a few minutes passed or they wrote a normal message | `/access` |
| `security/raid.py` | Raid detection and server lockdown | `/access`, `/security` |
| `moderation/reports.py` | Reports: members flag a message for the staff through a context menu or a command | `/admin`, `/report` |
| `community/rolemenu.py` | Role menus: posts with buttons or a dropdown that give and remove roles | `/post` |
| `community/roles.py` | Reaction roles and notification topics | `/notify`, `/post`, `/topic` |
| `server/rules.py` | Rules with an accept button, a version number and reminders for members who did not accept the current version | `/structure` |
| `community/schedule.py` | Scheduled messages: posts at a set time, once or repeating | `/post` |
| `server/setup.py` | Guided setup with buttons, AutoMod presets, server templates and the health overview | `/admin`, `/server` |
| `tools/shortcuts.py` | Short top-level commands /security block, /security unblock and /security blocklist for the AutoMod blocklist | `/security` |
| `server/structure.py` | Server structure: channels and categories by command, archiving of idle channels, timed roles and role templates | `/structure` |
| `community/tags.py` | Custom commands (tags) that anyone can call, and autoresponders that answer matching messages | `/support` |
| `server/team.py` | Team: statistics of the moderators, a weekly report, absence and duty roster | `/team` |
| `moderation/tickets.py` | Ticket system with buttons and transcripts | `/support` |
| `tools/tools.py` | Moderator tools: purge, slowmode, channel lock, role handling, say and embed | `/access`, `/moderation`, `/post` |
| `server/updates.py` | Checks GitHub for a newer release, tells the owner of the bot, downloads it and installs it on request or automatically | - |
| `tools/utility.py` | Reminders and AFK status | `/community` |
| `security/verify.py` | Verification gate with button, captcha or math question | `/access` |
| `community/welcome.py` | Welcome and goodbye messages, auto roles and booster rewards | `/community` |

The list of all commands with options is generated into [docs/REFERENCE.md](docs/REFERENCE.md) by `python scripts/build_reference.py`.

Before a release, run through the checklist in [docs/TESTING.md](docs/TESTING.md) on a test server. The automated tests cannot reach Discord.

## Conventions

- A cog that owns a section of the server settings extends `BaseCog` and sets `section = "name"`; `self.conf(gid)` then returns that section. A cog that should not receive events while its module is off sets `gate = {"on_message": "module"}`.
- Heavy or blocking work goes through `await self.work("lane", function, args)` (lanes ocr, image, music, maintenance). Catch `workers.Busy` where a refusal can be answered in a friendly way.
- A new setting goes into the file of its area in `guardbot/defaults/`. `tests/test_schema.py` checks that every settings key written as a literal in the code exists there.
- A change to the shape of stored data needs a numbered function in `guardbot/migrations.py`, added to `MIGRATIONS`, and `SCHEMA_VERSION` raised by one. Migrations run once after an automatic backup; write a test with an old database.
- Type hints are required in the modules listed in `mypy.ini` (run `python -m mypy`). Other modules may follow.
- Text shown to people goes through `i18n.say`; run `python scripts/missing_texts.py` and translate what it lists.
