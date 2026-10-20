# Privacy notes for server operators

GuardBot runs on your own machine. The bot does not send data to anyone except Discord. This page lists what is stored so you can inform your members.

<!-- toc -->

- [What is stored](#what-is-stored)
- [Rights of members](#rights-of-members)
- [Rights and tools for administrators](#rights-and-tools-for-administrators)
- [Your responsibility](#your-responsibility)

<!-- tocstop -->

## What is stored

| Data | Purpose | Where |
| --- | --- | --- |
| Server settings | Configuration of all modules | `data/guardbot.db` |
| User ID, XP, level | Level system | `data/guardbot.db` |
| Birthday (day and month only) | Birthday role and message | `data/guardbot.db` |
| Moderation cases (user ID, name at the time, moderator, reason, date) | History of warnings, mutes, kicks, bans, jail | `data/guardbot.db` |
| Roles of a jailed member | Restore after release | `data/guardbot.db` |
| Message log entries | Log channel in your server | Discord, not on disk |
| Backups (roles, channels, emojis, webhooks, member roles) | Restore after damage | `data/backups` |

Message content is not written to disk by the bot. It is posted to the log channel you configure, so the access rights of that channel decide who can read it.

## Rights of members

- `/mydata export` sends a member the stored profile and the cases about them.
- `/mydata delete` removes XP, level and birthday. Moderation cases are kept for the safety of the server.
- `/birthday remove` removes only the birthday.

## Rights and tools for administrators

- `/privacy export user_id` and `/privacy delete user_id` handle requests for members who are no longer on the server. Deleting also anonymizes the name in moderation cases.
- `/privacy retention days` deletes the profile data of members who left after the given number of days. The default is 0, which keeps the data.
- Set `purge_on_guild_leave` to `true` in `settings.json` to delete all data of a server when the bot is removed from it.
- Backups with member roles contain user IDs. Turn this off with `/backup schedule include_members:False` if you do not need it.

## Your responsibility

You decide which modules run and how long data is kept. Inform your members in your server rules about logging and moderation records. This page is a technical description and not legal advice.

Copyright (c) Justyn - made in Germany
