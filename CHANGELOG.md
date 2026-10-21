# Changelog

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
