# Privacy notes for server operators

GuardBot runs on your own machine. The bot does not send data to anyone except Discord. The other connections are the update check to GitHub, which sends no personal data and can be switched off with `update.enabled` in `settings.json`, and, only if an administrator adds their own AI key, the AI provider they chose (see [AI features](#ai-features)). This page lists what is stored so you can inform your members.

<!-- toc -->

- [What is stored](#what-is-stored)
- [Rights of members](#rights-of-members)
- [Rights and tools for administrators](#rights-and-tools-for-administrators)
- [AI features](#ai-features)
- [Your responsibility](#your-responsibility)

<!-- tocstop -->

## What is stored

| Data | Purpose | Where |
| --- | --- | --- |
| Server settings | Configuration of all modules | `data/guardbot.db` |
| User ID, XP, level | Level system | `data/guardbot.db` |
| Birthday (day and month only) | Birthday role and message | `data/guardbot.db` |
| Moderation cases (user ID, name at the time, moderator, reason, date) | History of warnings, mutes, kicks, bans, jail | `data/guardbot.db` |
| Reminders (user ID, channel, text, time) | `/community remind`, deleted when sent | `data/guardbot.db` |
| AFK status (reason, time) | `/community afk`, removed with your next message | `data/guardbot.db` |
| Ban appeals (user ID, name, text, status) | Decision of the staff | `data/guardbot.db` |
| Mod-mail conversations (user ID, channel) | Link between member and channel while open | `data/guardbot.db` |
| Invite used when joining (invite code, inviter ID) | Invite tracking, only with the module on | `data/guardbot.db` |
| Reports (message excerpt, reporter ID) | Posted to the report channel of your server, the database only keeps message and user IDs for 7 days to block duplicates | Discord and `data/guardbot.db` |
| Command counters (number per command, no user) | `/server debug usage`, can be turned off | `data/guardbot.db` |
| Currency balance, shop items bought, last daily and work time | Economy module | `data/guardbot.db` |
| Messages and joins per channel and day (numbers only, no content, no names) | Activity module, kept 120 days | `data/guardbot.db` |
| Dashboard sessions (Discord user ID and name, no password, no token) | Only if the dashboard is on, kept in memory for 8 hours, never written to disk | Memory only |
| Fingerprints (hash) of images that were judged as scam | Remove the same image again without reading it, no image is stored | `data/guardbot.db` |
| Fingerprints (hash) of texts that a moderator marked as scam | Remove the same text again, the text itself is not stored | `data/guardbot.db` |
| Probation (member ID, start time, count of normal messages) | Probation module, removed when the probation ends | `data/guardbot.db` |
| Scheduled messages, feeds and role menus | Settings of your server | `data/guardbot.db` |
| Roles, timeout and mute of members who left (member ID, role IDs, end time) | Sticky roles and mute-evasion protection, kept for the configured days, removed with `/members stickyroles forget` | `data/guardbot.db` |
| Watch list (user ID, reason, moderator) | `/members watch`, silent observation by the team, not removed when a member deletes their own data | `data/guardbot.db` |
| Rules accepted (version and time) and reminder sent | `/structure rules` | `data/guardbot.db` |
| Staff applications (user ID, answers, votes, status) | `/team apply`, included in the export and removed with the deletion of your data | `data/guardbot.db` |
| Team statistics (numbers per moderator and week) and duty status | `/team`, no content | `data/guardbot.db` |
| Settings history (which setting, old and new value, time, a guess of the person) | `/admin history`, the newest entries up to the configured count | `data/guardbot.db` |
| Timed roles and requests waiting for a second moderator | `/structure temprole`, `/security approval`, removed when done | `data/guardbot.db` |
| Skills (JSON), their use counts and counters per member | Skills module, counters per member are part of the member export and removed with the deletion of their data | `data/guardbot.db` |
| AI key of the server (encrypted), provider, model, number of requests today | AI module, the key is never shown, logged or exported, the secret to read it is the file `data/ai.secret` | `data/guardbot.db` and `data/ai.secret` |
| Learned anti-scam filter (short hashes of words with counts, no text, no user) | Learned filter, trained by moderators and optionally by a sample of normal messages | `data/guardbot.db` |
| Picture fingerprints (64 bit hash) of scam pictures | Find re-saved or resized copies, no picture is stored | `data/guardbot.db` |
| Pictures of panels (banners, pictures, thumbnails you upload) | Panels, deleted when no panel uses them any more and when the bot leaves the server with `purge_on_guild_leave` | `data/panels/<server>/` |
| Copies of the database | Restore after damage, contain everything above | `data/dbbackups` |
| Music library | Files you add or download | `music/` |
| Roles of a jailed member | Restore after release | `data/guardbot.db` |
| Message log entries | Log channel in your server | Discord, not on disk |
| Backups (roles, channels, emojis, webhooks, member roles) | Restore after damage | `data/backups` |

Message content is not written to disk by the bot. Images are read in memory by the anti-scam module and are not saved. It is posted to the log channel you configure, so the access rights of that channel decide who can read it.

## Rights of members

- `/info mydata export` sends a member the stored profile and the cases about them.
- `/info mydata delete` removes XP, level and birthday. Moderation cases are kept for the safety of the server.
- `/birthday remove` removes only the birthday.

## Rights and tools for administrators

- `/server privacy export user_id` and `/server privacy delete user_id` handle requests for members who are no longer on the server. Deleting also anonymizes the name in moderation cases.
- `/server privacy retention days` deletes the profile data of members who left after the given number of days. The default is 0, which keeps the data.
- Set `purge_on_guild_leave` to `true` in `settings.json` to delete all data of a server when the bot is removed from it.
- Backups with member roles contain user IDs. Turn this off with `/server backup schedule include_members:False` if you do not need it.

## AI features

The AI features are off until an administrator stores an API key of Anthropic, OpenAI or Kimi (Moonshot) with `/support ai setup` or in the dashboard. Then these texts are sent to that provider, under the administrator's own account:

- the description typed into `/support ai make`, together with the names and IDs of roles the bot can hand out and of text channels, so the AI can use them in the skill;
- with the second opinion turned on (`/support ai limits second_opinion:true`), the text of messages that the anti-scam check finds suspicious but not clear. Author names and IDs are not sent.

The provider's own terms and privacy rules apply to what it receives. Tell your members in your rules if you turn on the second opinion. `/support ai remove` deletes the key and turns the module off.

## Your responsibility

You decide which modules run and how long data is kept. Inform your members in your server rules about logging and moderation records. This page is a technical description and not legal advice.

Copyright (c) Justyn - made in Germany
