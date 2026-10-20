# Command reference

Commands marked with a slash work as slash commands. Moderation commands also work with the prefix (default `!`), for example `!warn @user spam`.

Every command name can be changed in `settings.json` under `command_names`, and every module or single command can be turned off per server with `/module` and `/command`.

<!-- toc -->

- [Moderation](#moderation)
- [Gulag (jail)](#gulag-jail)
- [Auto-moderation](#auto-moderation)
- [Security](#security)
- [Logging](#logging)
- [Community](#community)
- [Privacy](#privacy)
- [Administration](#administration)

<!-- tocstop -->

## Moderation

| Command | Description | Default permission |
| --- | --- | --- |
| `/warn member reason` | Warn a member, reason is optional | Timeout members |
| `/unwarn case_id` | Remove one warning | Timeout members |
| `/clearwarns user` | Remove all active warnings of a user | Timeout members |
| `/mute member duration reason` | Timeout, for example `30m`, `2h`, `1d` | Timeout members |
| `/unmute member` | Remove a timeout | Timeout members |
| `/kick member reason` | Kick a member | Kick members |
| `/ban user reason` | Ban a user, also by ID | Ban members |
| `/unban user` | Unban a user by ID | Ban members |
| `/cases user kind search page` | History, filter by mention, user ID, type or part of a name | Timeout members |
| `/warnings user` | Warnings of one user | Timeout members |
| `/case case_id` | Details of one case | Timeout members |
| `/escalation list`, `set`, `remove` | Automatic punishments, for example 3 warnings = timeout | Manage server |

Who may use these commands can be changed with `/perms allow`, `/perms deny`, `/perms reset` and `/perms show`.

## Gulag (jail)

| Command | Description |
| --- | --- |
| `/jail member duration reason` | Send a member to the gulag channel, duration (`30m`, `2h`, `1d`) and reason are optional |
| `/unjail member reason` | Release a member and give the old roles back |
| `/jailsetup setup` | Create or select role, channel and staff role |
| `/jailsetup apply` | Apply the channel permissions again |
| `/jailsetup notice` | Set a custom notice, empty restores the default security steps |
| `/jailsetup preview` | Show the notice |

## Auto-moderation

| Command | Description |
| --- | --- |
| `/automod toggle rule enabled action` | Rules: words, caps, mentions, invites, phishing, pii, doxxing, threats |
| `/automod add`, `remove`, `show`, `import` | Edit the lists: words, phishing, phishing_allow, invites_allow, doxxing, threats |
| `/automod set rule option value` | Numbers and options such as `caps percent 80` |
| `/automod channel` | Remove links, images or videos in a channel |
| `/automod block`, `unblock`, `blocklist` | Blocklist for links, texts and images |
| `/automod flood` | Flood protection |
| `/automod exemptrole`, `exemptchannel` | Ignore roles or channels |

Actions: `log`, `delete`, `warn`, `timeout`, `jail`.

## Security

| Command | Description |
| --- | --- |
| `/lockdown mode reason` and `/unlock` | Lock or unlock the server. Mode `channels` edits every channel, mode `role` edits only the @everyone role and is instant |
| `/lockdownconfig mode`, `lockrole`, `bypassrole`, `exempt` | Default mode, extra roles locked in role mode, roles that can still write, channels that stay open |
| `/verify setup`, `panel`, `apply`, `member`, `off` | Verification gate with button, captcha or math question, optional kick after a timeout |
| `/raid setup` | Join-rate detection, minimum account age, automatic lockdown |
| `/antinuke setup`, `limit`, `newbots`, `whitelist`, `staffrole`, `servername`, `restore`, `status` | Mass deletions, bans, kicks, permission grants, new webhooks, added bots, server renames and nuke talk |
| `/backup create`, `schedule`, `list`, `download`, `delete`, `restore` | Roles with order, channels with member overwrites, emojis, webhooks and member roles. Backups can run automatically |

## Logging

| Command | Description |
| --- | --- |
| `/log set category channel` | Categories: main, messages, members, voice, server, moderation, security |
| `/log sent enabled` | Log every sent message on or off |
| `/log show` | Show the log channels |

## Community

| Command | Description |
| --- | --- |
| `/welcome set`, `autorole`, `botrole`, `test` | Welcome and goodbye messages, auto roles |
| `/booster set`, `role` | Booster rewards |
| `/reactionrole add`, `remove`, `list`, `panel` | Reaction roles with any emoji |
| `/notifytopic add`, `remove`, `panel` and `/notify subscribe`, `unsubscribe`, `list` | Notification topics |
| `/ticket setup`, `panel`, `addtype`, `removetype`, `add`, `remove`, `close` | Tickets |
| `/poll create`, `end`, `list` | Polls, optionally with multiple choices |
| `/giveaway start`, `end`, `reroll`, `list` | Giveaways |
| `/starboard setup`, `ignore` | Starboard |
| `/tempvoice setup` | Temporary voice channels |
| `/suggest text`, `/suggestion status`, `/suggestionsetup set` | Suggestions |
| `/xp config`, `show`, `boost`, `give`, `take`, `setlevel`, `reset`, `ignore` | XP system, rank card on or off, XP boost per role |
| `/levelrole add`, `remove`, `list`, `sync` | Roles for levels |
| `/rank`, `/leaderboard` | Level as an image card and top list |
| `/birthday set`, `remove`, `show`, `upcoming` and `/birthdaysetup set` | Birthdays |

## Privacy

| Command | Description |
| --- | --- |
| `/mydata export` and `/mydata delete` | Members export or delete their own stored data |
| `/privacy retention`, `delete`, `export` | Retention time for members who left, deletion and export by user ID |

Details are in [PRIVACY.md](PRIVACY.md).

## Administration

| Command | Description |
| --- | --- |
| `/module list`, `enable`, `disable` | Turn features on or off |
| `/command list`, `enable`, `disable` | Turn single commands on or off |
| `/prefix` | Change the prefix of text commands |
| `/alias add`, `remove`, `list` | Short names for text commands |
| `/perms allow`, `deny`, `reset`, `show` | Who may use which command |
| `/config get`, `set`, `reset` | Read and change any setting, for example `/config set automod.caps.percent 80` |
| `/settings` | Overview |
| `/help` | Command overview |
| `/about` | Version and support |
