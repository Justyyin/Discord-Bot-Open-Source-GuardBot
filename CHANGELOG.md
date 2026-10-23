# Changelog

## 1.11.0

- Dashboard details: every plugin page explains what the plugin does, lists all of its functions with their own switch and a short explanation, and keeps the other settings in boxes below. Every setting has a help text. Plugin cards on the Plugins page and on the overview have a real on and off switch and show how many functions and settings they have. All new texts are in 12 languages (machine translated).
- Guard Music: the music can run as a second bot in the same process, with its own token (MUSIC_TOKEN in .env, music_bot in settings.json), the same settings and data, and its own slash commands. It can stay in a voice channel around the clock (/music stay) and play a saved playlist on repeat, also after a restart. Without the token the music stays inside GuardBot as before.
- Music sources: YouTube and SoundCloud play directly. Spotify, Apple Music and Tidal links are read for title and artist and played from the search source (YouTube or SoundCloud); nothing is downloaded from these services. Tidal albums and playlists use the official Tidal API with your own free key. Each source can be switched off per server (/music sources).
- Saved playlists (/music playlist save, add, play, show, remove, delete) that mix all sources and the music folder.
- Dashboard page Music: player with pause, skip, stop, mix, repeat and volume, the queue, adding links, searches and folder music, editing playlists, the 24/7 mode, the sources and the setup guide with the note that use is at your own risk.
- Dashboard appearance (Settings): accent colour, background, boxes and text colour, a wallpaper with darkening and blur, compact view, hidden categories, and own menus and tabs in the side bar (a set of plugins, a shortcut to a page, an https link or a note). Stored per server, checked strictly, and the wallpaper is served only to signed-in users of the server.
- Footer with copyright, Discord and GitHub links. The official logos can be added as guardbot/web/brand/discord.svg and github.svg; without them the dashboard shows its own simple icons.
- Playlists from the dashboard keep only music folder files that really are inside the folder.
- Documentation: Music, Guard Music, sources and appearance in all 12 README and GUIDE files.
- Tests: 393.

## 1.10.0

- Dashboard in 12 languages: a language menu in the top bar and on the sign-in page. The choice is kept in the browser and does not change the server language. All page texts, section titles, explanations, field labels, groups, choices, categories and plugin descriptions are translated (machine translated); anything missing falls back to English.
- The translations live in `guardbot/locales/dashboard/<lang>.json` and are served by the public route `/api/texts/<lang>`; `guardbot/dashtexts.py` collects the English texts, and a test checks that every language is complete and keeps the placeholders.
- The search on the overview also finds settings by their translated names.
- Overview: the charts come first, then the setup status and the module switches.
- Clearer English labels for some fields (for example "OCR language" instead of "ocr_lang").
- Tests: 367.

## 1.9.0

- Dashboard redesign in a dark look: top bar with the user, a left bar with the server picker, the main pages (Overview, Plugins, Commands, Panels, Skills, AI, Bot profile, Settings, Moderation cases, Backup) and every plugin grouped by category with a dot that shows whether it is on; categories can be folded.
- Plugins page: every module as a card with icon, short description and an Active or Activate button, with tabs per category.
- A page per plugin: the switch Active at the top, its settings in boxes that open and close, and its commands with a switch and a pencil that opens the role editor. Plugins with their own page (Panels, Skills, AI) link to it.
- Settings page for prefix, language and the settings that belong to no single plugin.
- `guardbot/plugins.py` holds the catalog of the plugins (category, icon, sections, texts in English and German); a test checks that every module and section is covered.
- The icons are simple line drawings made for this dashboard.

## 1.8.0

- Panels (`/panel`, `guardbot/panels.py`): posts made of banner pictures, text boxes and buttons, for example a welcome post, rules, a role choice, notification buttons or a verification gate. Templates for each of these with texts in the server language. A section has a banner above the box, title, text, colour, a large picture, a small picture and a footer; buttons give or take roles (optionally only one role of the panel at a time), start the verification, or open a link, and keep working after a restart.
- Pictures are uploaded as command options or in the dashboard, checked (PNG, JPEG, GIF, WebP, at most 8 MB), stored once in `data/panels/<server>/` and removed when no panel uses them, because links to Discord attachments stop working after a while.
- `/panel post` posts a panel and replaces an older post of it, `/panel update` changes the posted messages in place after an edit, `/panel preview` shows it only to you.
- Dashboard: new page Panels to create panels from templates, upload pictures, edit sections and buttons, post and update. Pictures are served only to signed-in users of the server.
- Documentation: section Panels in all 12 README files, COMMANDS.md, PRIVACY.md, TESTING.md.
- Tests: 361.

## 1.7.1

- Gulag notice: the "Account Security Required" message now looks like the template (lock in the title, numbered steps, bold words, footer "Account Safety Check" with the server icon and the time) and is posted with a mention for everyone who comes into the gulag: by command, by AutoMod, by the anti-scam check, when a jailed member rejoins, and when someone gives the gulag role by hand. Taking the role away by hand clears the gulag entry. Changes the bot makes itself are not reported twice.
- Reminder: while someone is in the gulag, an "Account Recovery Reminder" stays at the bottom of the gulag channel and is renewed every 10 minutes (edited when nothing was written since, moved down otherwise, removed when the gulag is empty).
- Release requests: a member in the gulag who writes the prefix and the release word (default `unban`, so `!unban`) in the gulag channel creates a request with Release and Keep buttons that only the staff role or Manage Roles can use. The bot never releases anyone on its own, and the moderation command `unban` does not react to this message.
- `/access jailsetup reminder` switches notice, reminder and requests on or off and sets the interval and the word; the dashboard shows the same settings. `/access jailsetup preview` shows both messages. All texts are translated into the server language (machine translated).
- Tests: 351.

## 1.7.0

- Skills (`guardbot/skills.py`, `/support skill`): commands, games (dice, choice, slots, rock paper scissors, quiz) and automations (member joins or leaves, message contains words, button) built from a fixed set of actions and conditions. Skills are data, never code: every field is checked, unknown fields are refused, and there are limits for actions, messages, role changes, coins and counters. The bot only hands out roles below its own highest role without dangerous permissions. Skills run with `/support skill run`, with the prefix and from persistent buttons (`/support skill panel`).
- AI connection (`guardbot/ai.py`, `/support ai`): Anthropic, OpenAI and Kimi (Moonshot) with the key of the server. The key is entered in a private box or in the dashboard, stored encrypted (secret in `data/ai.secret`), never shown, logged or exported, and the provider can only change together with a new key. Daily limit, wait time per person and answer length can be set. `/support ai make` writes a skill from a description; the answer is checked like an imported skill and saved only after confirmation.
- Anti-scam: a learned filter per server (naive Bayes over hashed words, trained with "Mark as scam" and the new "Not a scam" menu, optional sampling of normal messages), picture fingerprints that find re-saved or resized scam pictures without Tesseract, and an optional AI second opinion for borderline cases that can only lead to the normal anti-scam action.
- Dashboard: new pages Commands (every slash command, prefix command and context menu with module, permission and state; switch on or off, allowed and denied roles, short names, prefix), Skills (list, switch, edit as JSON with the same checks), AI (model, limits, write-only key) and Bot profile (name, picture, banner and about text on the server; everywhere for the owner of the application or `owner_ids`). Bodies of normal requests stay limited to 256 KiB. The moderation cases page loads again (wrong address since 1.5).
- Privacy: counters of skills per member are part of the member export and deletion. PRIVACY.md describes what the AI features send.
- Fix: `scripts/missing_texts.py` scanned no file after the cogs moved into folders in 1.5.2; it now scans all of them and also texts listed in `TEXTS` tuples.
- Documentation: section Skills and AI and the new dashboard pages in all 12 README files, a short section in all guides, COMMANDS.md, TESTING.md. The Korean README had three sections in the wrong place; they are back where the other languages have them.
- Tests: 342.

## 1.6.0

- Storage: the settings of a server are saved one row per section (`config_sections`), so a change writes only that section instead of the whole server. Schema version 3 converts the old rows once, after an automatic backup. Memory use is about 30 KiB of settings per server and about 400 bytes per user record (`python scripts/bench.py` prints it).
- Heavy work: reading images, drawing rank cards, music files and database maintenance run in lanes (`guardbot/workers.py`) with a fixed number of threads and a limit for running plus waiting jobs. A full lane answers "busy" at once instead of piling up work. Sizes can be set under `workers` in `settings.json`; the anti-scam OCR queue uses the same lanes.
- Structure: `guardbot/cog.py` is the base class of the cogs (settings section, event gate, lanes); 20 cogs use it and lost their own copy of `conf()`. The music cog is split into `musicdl.py` (links, tags, library files) and `musicplayer.py` (voice player), and the personal data checks of AutoMod moved to `detect.py`.
- Types and checks: `python -m mypy` checks the core modules (store, checks, workers, migrations, defaults, health, logging, metrics). `tests/test_schema.py` fails when the code uses a settings key that does not exist in the defaults. The CI also runs mypy and checks that `docs/REFERENCE.md` is current.
- Logging: `log_format` set to `json` writes one JSON object per line; every line made while a command or an event is handled carries the server and the command. `log_max_mb` and `log_backups` set the rotation.
- Metrics: with `health_port` set, `/metrics` serves Prometheus metrics (uptime, latency, memory, database size, cached servers, users and cases, errors, command uses, command durations as a histogram, work lanes). Only counts are exported. `metrics_token` requires a bearer token, `metrics` set to false turns the page off.
- Backups: every database backup is opened and checked (integrity and row counts) right after it is made, and a failed copy is deleted with an error. `python scripts/restore_db.py BACKUP` restores one after checking it, keeps the old database as `before-restore`, refuses while the bot runs, and puts the old database back when the restored one does not start. `--check` only verifies.
- Documentation: Operations section of the README (12 languages) with the new settings and the restore command, new conventions in CONTRIBUTING.md, new rows in `docs/TESTING.md`.
- Tests: 283.

## 1.5.2

- Structure: the cogs are sorted into the folders `security`, `moderation`, `server`, `community` and `tools` under `guardbot/cogs/`, and `defaults.py` became the package `guardbot/defaults/` with one file per area (core, security, moderation, community) and `base.py` for the module list and permissions. Behaviour and settings are unchanged. CONTRIBUTING.md lists every cog with its path.
- Texts: the fixed replies of all cogs go through the translation system (279 replies rewritten, 255 new texts translated in 11 languages, machine translated). Embed titles, field names and a few composed replies are still English.
- Overview: `/admin module overview` and the dashboard show for every module whether it is configured, still open or needs no setup. The dashboard groups its settings into categories with short explanations, has a setup panel, charts for activity and moderation, and a search over all settings.
- Performance: the rules reminder uses a queue, the member scan runs in small batches, the staff roster is cached for ten minutes, and listeners of switched-off modules are skipped before they run. `settings.json` can set `members_intent`, `chunk_guilds` and `message_cache`. `python scripts/bench.py` measures the cost of the loops with many servers and members. The database needs no extra indexes because every query is answered from memory.
- Documentation: the setup guide has a new section for the 1.5 features in all 12 languages, `docs/TESTING.md` is a checklist for a test server, and a test checks that every command named in the guides and in COMMANDS.md exists.
- Tests: 256, among them tests that build real discord.py objects (Guild, Role, Member, TextChannel) from API data to check permissions, the staff roster and the gating of listeners.

## 1.5.1

- Structure: `core.py` is split into `store.py` (SQLite storage), `tree.py` (slash command tree) and `checks.py` (permission checks and team helpers). Behaviour is unchanged. CONTRIBUTING.md now has a table of every cog with its command group.
- Overview: `/help` lists the groups with their commands and fits into one message, `/info find` searches all commands by word, `/admin module overview` shows every module with its state and number of commands, and the dashboard searches all settings from the overview page. `docs/REFERENCE.md` lists every slash command with its options and is generated by `python scripts/build_reference.py`; a test fails when it is out of date.
- Performance: the rules reminder no longer walks all members every ten minutes but plans the next check from the earliest due member, the staff roster is cached for 60 seconds, and the message cache of the bot can be set with `message_cache` in `settings.json` (default 10000, lower it on small machines).
- Translations: all remaining fixed reply texts are translated in 11 languages (machine translated). A test checks that placeholders such as `{reason}` survive in every translation.

## 1.5.0

- Structure: `/structure channel` and `/structure category` create, clone, rename, move and sort channels and categories and copy permissions. `/structure archive` reports or archives inactive channels. `/structure temprole` gives roles for a limited time, `/structure roletemplate` saves and applies role templates (never more permissions than the person applying has). `/structure rules` posts rules with an accept button, a version number and one reminder for members who did not accept a new version.
- Setup wizard: a new button creates missing roles, categories and channels from the templates community, gaming and support after a confirmation, and fills log, rules, welcome and staff settings only where they are empty.
- Administration: `/admin history` lists changes of the settings with time and a guess who made them, rolls a section back, and copies sections to another server (dry run first, channel and role IDs are mapped by name). `/admin exceptions` leaves channels and roles out of AutoMod rules and Anti-Scam. `/admin dashaccess` gives roles read-only or moderator access to the dashboard.
- Team: `/team teamstats` (cases, tickets, reports, response time, inactive moderators), `/team weekly` (weekly report, UTC), `/team duty` (sign off, tickets and pings go to others) and `/team apply` (staff applications with a form and a vote).
- Moderation: sticky roles and mute-evasion protection (`/members stickyroles`), name moderation with dehoist, banned words and automatic renaming (`/members nickname`), a silent watch list (`/members watch`), reason templates (`/members reason`), four-eyes approval for bans, kicks, timeouts and bulk actions (`/security approval`), `/moderation case undo` including follow-up actions and batches, and expiry of warnings (`/moderation escalation expiry`).
- Command groups: 24 top-level commands. New groups are `/structure`, `/members`, `/team` and `/engage` (economy, giveaway, poll, counting, starboard). `/team modwatch`, `/team permaudit` and `/server debug` moved into groups. Slash commands are registered again on the next start. Commands inside groups cannot be hidden by Discord, the bot still checks every call.
- Dashboard: access levels none, viewer, mod and admin. Settings of the new features appear in the editor automatically.
- Data: new stored data is listed in docs/PRIVACY.md. The watch list is not removed when a member deletes their own data.
- Translations of the new fixed texts in 11 languages (machine translated). Tests: 239.

## 1.4.0

- Command groups: the 99 top-level slash commands are now 20. Related commands are grouped, for example `/moderation ban`, `/security raid`, `/server log`, `/admin config`, `/post embed`. Text commands with the prefix (`!ban`) are unchanged. Permissions, aliases, module switches, the disable list and `command_names` keep working with the plain command names, so no migration is needed. Discord only applies its own "who can see this command" setting to top-level commands, so inside groups visibility is no longer hidden for members; the bot still checks every call. Slash commands are registered again on the next start.
- Anti-scam module: removes fake giveaways and crypto scams, such as the typical MrBeast scam, in text and in images within milliseconds. Names are recognised in any spelling (M R B E A S T, Mr.B3ast, look-alike letters, invisible characters), other words add up to a score, images are read with Tesseract OCR in a worker thread, and images judged as scam once are removed without reading them again. `/security antiscam` sets the lists, the threshold and the action and tests texts and images.
- `/admin setup` guided assistant with buttons and menus (log channel, welcome channel, staff roles, gulag, AutoMod presets loose, normal and strict, templates community, gaming and support, language) and `/server health` for what is set up and what is open.
- Member-facing texts in 12 languages with the server setting `language` and `/admin language`. Default welcome, goodbye, booster, birthday and level-up texts are translated too. Fixed replies to administrators are translated, replies with names and numbers stay in English. The economy and role menu texts are translated as well.
- Economy (`/engage economy`): daily reward, work, payments, leaderboard and a shop whose items can give a role.
- Role menus (`/post rolemenu`) with buttons or a dropdown, scheduled messages (`/post schedule`) and feeds for YouTube, Twitch and RSS (`/post feed`).
- Member statistics (`/community activity`): busiest channels, messages per day, joins and leaves. Only numbers are stored.
- Moderation: `/moderation bulk ban`, `kick` and `timeout` for up to 25 users after a confirmation, a richer `/moderation cases` search (reason, moderator, age) and `/moderation case link` to connect cases and notes.
- Fewer top-level commands: the setup commands of birthdays, suggestions, notifications, mod-mail, appeals, reports and level roles are now sub-commands of their features. Existing aliases, rules and permissions are moved by an automatic migration.
- Operations: sharding (`shard_count`), versioned database migrations with an automatic backup before each one, daily database backups in `data/dbbackups` (`/server debug db action:backup`), a heartbeat file with a Docker health check and an optional status page (`health_port`). The music queue, sticky messages and moderator counters survive restarts.
- Security: feeds and downloads use the checked resolver and check every redirect, feeds with entity definitions are refused, stored scheduled messages and feeds are validated before use, and `music_generic` can switch off the generic yt-dlp extractor. See SECURITY.md for what was reviewed and what remains.
- Probation (`/access probation`): new members get a role and may not post links, invites or files until minutes passed or they wrote normal messages. Raid protection recognises swarms of new accounts (`/security raid swarm`), `/moderation case timeline` merges everything stored about a user, `/security block`, `/security unblock` and `/security blocklist` are own commands, and moderators teach the anti-scam module with the `Mark as scam` menu entry or an emoji.
- Replies to administrators use the server language for fixed texts, with a fallback to English. `scripts/missing_texts.py` lists what is still untranslated, and a test checks the common texts.
- Load tests: 1000 messages through the scan path and a bounded OCR queue.
- Dashboard: a web page inside the bot to change the settings of a server after a Discord login (modules, channels, roles, thresholds, texts, prefix, language, cases, export and import). Off by default, listens on 127.0.0.1, needs HTTPS for public addresses, access only for server managers and only while the bot is connected to the server. Works on Linux, macOS, Windows, Docker and VPS.
- Start scripts `start.sh` and `start.bat`, a launchd file for macOS, a Caddy example for the dashboard, and a README with installation steps for Linux, macOS and Windows in all 12 languages. The README now states that all translations are machine translated and not checked by native speakers.
- Message builder (`/post message send`, `edit`, `preview`, `copy`): posts messages with several embeds and link buttons from JSON, a file or an https link. It reads the JSON format of embed generators such as Embed Generator by Merlin Fuchs (credited in the README).
- Updates from GitHub: the bot checks the release repository, tells the owner by direct message, downloads and verifies the release (SHA-256 file, safe archive paths, version check), and installs it with `/server debug update action:install` or automatically with `update.auto_install`. Replaced files are saved first and restored when the new code does not start. `.env`, `settings.json`, `data` and `music` are never touched.
- The README, the guide and the dashboard state that the bot and the dashboard are in beta.
- Decorative emoji were removed from the code and the dashboard.
- Repository: GitHub Actions for tests and for releases built from a version tag with the changelog as notes, issue templates for bugs, features and translations, a pull request template and release steps in CONTRIBUTING.md.

## 1.3.0

- AutoMod: short links are followed to their target (public addresses only), new members can be barred from posting links, ghost pings are reported, rules can run in dry-run mode, and `/automod test` shows what a text would trigger. AutoMod counts rule hits.
- `/team modwatch`: limits for bans, kicks, timeouts, warnings, gulag and purges per moderator, with alert, timeout or role removal as response.
- `/team permaudit`: lists roles with dangerous permissions and reports new grants.
- Reports through the message menu and `/report`, with buttons for the staff. Invite tracking with `/server invites`.
- `/server diagnose` and a check at start-up for missing permissions, role order, deleted channels and roles. Error reports in a channel, command statistics, database check and vacuum, log level at runtime, rotating log file.
- `/admin config export` and `/admin config import` with validation.
- Music module: `/play`, queue and controls, local library `music/Artist/Album/Track`, downloads with yt-dlp, FLAC and other lossless files played unchanged. Off by default, downloads are a separate switch. Needs ffmpeg.
- Docker image and systemd unit include ffmpeg and the music folder.

## 1.2.0

- Moderator tools: `/moderation purge`, `/moderation slowmode`, `/access lockchannel`, `/access unlockchannel`, `/moderation role add|remove`, `/moderation note`, `/moderation tempban`, `/moderation jailed`, `/moderation case view|edit|delete`.
- Information: `/info userinfo`, `/server serverinfo`, `/server roleinfo`, `/info avatar`, `/info ping`, `/info botinfo`, `/help command:`.
- Announcements and content: `/post say`, `/post embed`, tags, autoresponders, `/community remind`, `/community afk`.
- Mod-mail through private server channels and ban appeals through an appeal server. The bot still reads no direct messages.
- Counting channel, sticky messages and statistics channels.
- Tickets: claim, rename, list. Giveaways: cancel, edit. Temporary voice: owner commands under `/community voice`.
- XP: channel multipliers, reset for everyone, leaderboard pages. Birthdays: list and admin commands. Backups: `/server backup info`.
- Logs: ignore lists for channels and users, `/server log show`.
- Status views: `/automod status`, `/access verify status`, `/security raid status`, `/community welcome show`, `/engage starboard show`.
- `/info mydata` and `/server privacy` also cover reminders and ban appeals.

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
- Data tools: `/info mydata`, `/server privacy`, retention time and `docs/PRIVACY.md`.

## 1.0.0

- First public release.
- Modules: logging, auto-moderation, moderation cases, gulag (jail), anti-raid, lockdown, anti-nuke, XP and levels, reaction roles, notification topics, welcome and auto roles, booster rewards, tickets, polls, giveaways, starboard, temporary voice channels, suggestions, birthdays, backup and restore.
- Per-server configuration: modules, commands, prefix, aliases, permissions.
