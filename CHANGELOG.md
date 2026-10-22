# Changelog

## 1.4.0

- Anti-scam module: removes fake giveaways and crypto scams, such as the typical MrBeast scam, in text and in images within milliseconds. Names are recognised in any spelling (M R B E A S T, Mr.B3ast, look-alike letters, invisible characters), other words add up to a score, images are read with Tesseract OCR in a worker thread, and images judged as scam once are removed without reading them again. `/antiscam` sets the lists, the threshold and the action and tests texts and images.
- `/setup` guided assistant with buttons and menus (log channel, welcome channel, staff roles, gulag, AutoMod presets loose, normal and strict, templates community, gaming and support, language) and `/health` for what is set up and what is open.
- Member-facing texts in 12 languages with the server setting `language` and `/language`. Default welcome, goodbye, booster, birthday and level-up texts are translated too. Fixed replies to administrators are translated, replies with names and numbers stay in English. The economy and role menu texts are translated as well.
- Economy (`/economy`): daily reward, work, payments, leaderboard and a shop whose items can give a role.
- Role menus (`/rolemenu`) with buttons or a dropdown, scheduled messages (`/schedule`) and feeds for YouTube, Twitch and RSS (`/feed`).
- Member statistics (`/activity`): busiest channels, messages per day, joins and leaves. Only numbers are stored.
- Moderation: `/bulk ban`, `kick` and `timeout` for up to 25 users after a confirmation, a richer `/cases` search (reason, moderator, age) and `/case link` to connect cases and notes.
- Fewer top-level commands: the setup commands of birthdays, suggestions, notifications, mod-mail, appeals, reports and level roles are now sub-commands of their features. Existing aliases, rules and permissions are moved by an automatic migration.
- Operations: sharding (`shard_count`), versioned database migrations with an automatic backup before each one, daily database backups in `data/dbbackups` (`/debug db action:backup`), a heartbeat file with a Docker health check and an optional status page (`health_port`). The music queue, sticky messages and moderator counters survive restarts.
- Security: feeds and downloads use the checked resolver and check every redirect, feeds with entity definitions are refused, stored scheduled messages and feeds are validated before use, and `music_generic` can switch off the generic yt-dlp extractor. See SECURITY.md for what was reviewed and what remains.
- Probation (`/probation`): new members get a role and may not post links, invites or files until minutes passed or they wrote normal messages. Raid protection recognises swarms of new accounts (`/raid swarm`), `/case timeline` merges everything stored about a user, `/block`, `/unblock` and `/blocklist` are own commands, and moderators teach the anti-scam module with the `Mark as scam` menu entry or an emoji.
- Replies to administrators use the server language for fixed texts, with a fallback to English. `scripts/missing_texts.py` lists what is still untranslated, and a test checks the common texts.
- Load tests: 1000 messages through the scan path and a bounded OCR queue.
- Dashboard: a web page inside the bot to change the settings of a server after a Discord login (modules, channels, roles, thresholds, texts, prefix, language, cases, export and import). Off by default, listens on 127.0.0.1, needs HTTPS for public addresses, access only for server managers and only while the bot is connected to the server. Works on Linux, macOS, Windows, Docker and VPS.
- Start scripts `start.sh` and `start.bat`, a launchd file for macOS, a Caddy example for the dashboard, and a README with installation steps for Linux, macOS and Windows in all 12 languages. The README now states that all translations are machine translated and not checked by native speakers.
- Message builder (`/message send`, `edit`, `preview`, `copy`): posts messages with several embeds and link buttons from JSON, a file or an https link. It reads the JSON format of embed generators such as Embed Generator by Merlin Fuchs (credited in the README).
- Updates from GitHub: the bot checks the release repository, tells the owner by direct message, downloads and verifies the release (SHA-256 file, safe archive paths, version check), and installs it with `/debug update action:install` or automatically with `update.auto_install`. Replaced files are saved first and restored when the new code does not start. `.env`, `settings.json`, `data` and `music` are never touched.
- The README, the guide and the dashboard state that the bot and the dashboard are in beta.
- Decorative emoji were removed from the code and the dashboard.
- Repository: GitHub Actions for tests and for releases built from a version tag with the changelog as notes, issue templates for bugs, features and translations, a pull request template and release steps in CONTRIBUTING.md.

## 1.3.0

- AutoMod: short links are followed to their target (public addresses only), new members can be barred from posting links, ghost pings are reported, rules can run in dry-run mode, and `/automod test` shows what a text would trigger. AutoMod counts rule hits.
- `/modwatch`: limits for bans, kicks, timeouts, warnings, gulag and purges per moderator, with alert, timeout or role removal as response.
- `/permaudit`: lists roles with dangerous permissions and reports new grants.
- Reports through the message menu and `/report`, with buttons for the staff. Invite tracking with `/invites`.
- `/diagnose` and a check at start-up for missing permissions, role order, deleted channels and roles. Error reports in a channel, command statistics, database check and vacuum, log level at runtime, rotating log file.
- `/config export` and `/config import` with validation.
- Music module: `/play`, queue and controls, local library `music/Artist/Album/Track`, downloads with yt-dlp, FLAC and other lossless files played unchanged. Off by default, downloads are a separate switch. Needs ffmpeg.
- Docker image and systemd unit include ffmpeg and the music folder.

## 1.2.0

- Moderator tools: `/purge`, `/slowmode`, `/lockchannel`, `/unlockchannel`, `/role add|remove`, `/note`, `/tempban`, `/jailed`, `/case view|edit|delete`.
- Information: `/userinfo`, `/serverinfo`, `/roleinfo`, `/avatar`, `/ping`, `/botinfo`, `/help command:`.
- Announcements and content: `/say`, `/embed`, tags, autoresponders, `/remind`, `/afk`.
- Mod-mail through private server channels and ban appeals through an appeal server. The bot still reads no direct messages.
- Counting channel, sticky messages and statistics channels.
- Tickets: claim, rename, list. Giveaways: cancel, edit. Temporary voice: owner commands under `/voice`.
- XP: channel multipliers, reset for everyone, leaderboard pages. Birthdays: list and admin commands. Backups: `/backup info`.
- Logs: ignore lists for channels and users, `/log show`.
- Status views: `/automod status`, `/verify status`, `/raid status`, `/welcome show`, `/starboard show`.
- `/mydata` and `/privacy` also cover reminders and ban appeals.

## 1.1.2

- Much more detailed README in all 12 languages: bot permissions, first steps, a command section with example code blocks for every module, message placeholders, configuration paths and data locations.
- A test checks that every command example in the README uses a real command and real parameter names.

## 1.1.1

- Removed the copyright comment from the top of every source file. The license and the credit in the bot output stay.
- Added a docstring to every module, class and function.
- Errors are no longer swallowed. Exceptions are caught by type, written to the log, and failures of lockdown, gulag and verification setup are reported to the user. Unexpected errors are not hidden any more.
- Added automated tests (`python -m unittest`) for storage, detection, levels, command registration, permission checks and the documentation.
- Documentation: project status section, notes about the translations, `<REPOSITORY_URL>` placeholder and `scripts/set_repo_url.py` instead of a fake URL.

## 1.1.0

- Storage moved from JSON files to SQLite. Existing JSON files are imported on first start and renamed to `.migrated`.
- Slash commands are only synced to Discord when they changed. Use `--sync` or `force_sync` in `settings.json` to force it.
- Lockdown and gulag permissions run concurrently. New lockdown mode `role` changes only the @everyone role and is instant.
- Anti-nuke also detects permission grants, new webhooks, added bots and server renames, and can revert them.
- New log events: invites, emojis, stickers, threads, webhooks, profile changes and server updates.
- Timed jail with automatic release.
- Polls with multiple choices.
- Rank card as image and XP boosts per role.
- Backups include role order, member overwrites, emojis, webhooks and member roles, and can run on a schedule.
- Verification gate with button, captcha or math question.
- Data tools: `/mydata`, `/privacy`, retention time and `docs/PRIVACY.md`.

## 1.0.0

- First public release.
- Modules: logging, auto-moderation, moderation cases, gulag (jail), anti-raid, lockdown, anti-nuke, XP and levels, reaction roles, notification topics, welcome and auto roles, booster rewards, tickets, polls, giveaways, starboard, temporary voice channels, suggestions, birthdays, backup and restore.
- Per-server configuration: modules, commands, prefix, aliases, permissions.
