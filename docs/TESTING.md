# Testing on a real server

The automated tests (`python -m unittest discover -s tests`) use real discord.py objects built from API data, but they never talk to Discord. Everything that depends on Discord itself has to be checked once on a test server before you use a release on a real community. This list is the minimum.

## Preparation

1. Create an empty test server and a second account (or a friend) to act as a normal member.
2. Invite the bot with the permissions from the setup guide, set `"dashboard": {"enabled": true}` if you want to test the dashboard, and start it with `--sync` once.
3. Run `/server diagnose`. Everything it reports as missing must be fixed first.

## Checklist

| Area | Steps | Expected result |
| --- | --- | --- |
| Start | Start the bot, read the log | "slash commands synced", no traceback |
| Help | `/help`, `/info find text:ban` | Groups and commands are listed, search finds `moderation ban` |
| Overview | `/admin module overview` | Every module with its state, setup status and command count |
| Modules | `/admin module disable name:automod`, post a link as the second account, enable again | No reaction while off, reaction after turning it on |
| Prefix | `/admin prefix` to `?`, then `?ping` | Answers, `!ping` no longer does |
| Language | `/admin language` to German, `/admin module overview` | Reply in German |
| Moderation | `/moderation warn`, `/moderation cases`, `/moderation case undo` | Case is created, listed and taken back |
| Approval | Turn on `/security approval`, ban as moderator 1 | Request appears, second moderator approves, ban happens |
| AutoMod | `/automod toggle rule:caps enabled:True`, send capital letters as member | Message removed, log entry appears |
| Anti-scam | `/security antiscam test` with a sample text | Score and verdict |
| Raid | `/security raid setup`, then `/access lockdown`, `/access unlock` | Channels locked, then restored exactly |
| Verification | `/access verify setup`, join with the second account | Member only sees the verify channel until solved |
| Rules | `/structure rules setup`, `add`, `post`, press the button as member | Role is given, `/structure rules status` counts it |
| Structure | `/structure channel create`, `clone`, `sort`, `/structure category sync` | Channels appear with the expected permissions |
| Temp roles | `/structure temprole give` with a one minute duration | Role is removed after the time |
| Sticky roles | Give a role, let the member leave and rejoin | Role comes back, dangerous roles do not |
| Team | `/team duty roster`, `/team duty away`, open a ticket | Ticket pings an available person, not the away one |
| Applications | `/team apply setup`, `/team apply start` as member | Form arrives in the channel, voting works |
| Backup | `/server backup create`, delete a role, `/server backup restore` | Role is back |
| History | Change a setting, `/admin history list`, rollback | Old value restored |
| Config | `/admin config export`, `/admin config import` without confirm | File is checked, nothing changes |
| Dashboard | Sign in with a viewer, mod and admin role | Viewer reads, mod edits moderation, admin edits all; setup panel and charts show |
| Data | `/server privacy export` and `/server privacy delete` with the ID of the second account | Data is exported, then deleted |
| Metrics | Set `health_port` and `metrics_token`, open the page /metrics of the status server with and without the token | 401 without the token, series with it |
| Restore | Stop the bot, run `python scripts/restore_db.py` with a backup, start again | Data of the backup is back, the old database is kept as before-restore |
| Restart | Stop with Ctrl+C, start again | Runtime state (reminders, timed roles) is still there |

## Reporting problems

Open an issue with the version (`/info about`), what you did, what you expected and the relevant lines from the log. Remove tokens and IDs you do not want to share.
