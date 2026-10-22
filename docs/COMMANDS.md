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
- [Information and utility](#information-and-utility)
- [Mod-mail and ban appeals](#mod-mail-and-ban-appeals)
- [Counting, sticky messages and statistics](#counting-sticky-messages-and-statistics)
- [Security and diagnostics](#security-and-diagnostics)
- [Music](#music)
- [Setup and languages](#setup-and-languages)
- [Economy](#economy)
- [Role menus, scheduled messages and feeds](#role-menus-scheduled-messages-and-feeds)
- [Activity and bulk moderation](#activity-and-bulk-moderation)
- [Anti-scam](#anti-scam)
- [Probation and blocklist](#probation-and-blocklist)
- [Message builder and updates](#message-builder-and-updates)
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
| `/case view`, `edit`, `delete` | Show a case, change its reason, delete it | Timeout members |
| `/note user text` | Private moderator note about a user | Timeout members |
| `/tempban user duration reason` | Ban for a limited time, lifted automatically | Ban members |
| `/purge amount user kind` | Delete many messages, filter by user or type | Manage messages |
| `/slowmode seconds channel` | Slowmode of a channel | Manage channels |
| `/lockchannel`, `/unlockchannel` | Lock or unlock one channel | Manage channels |
| `/role add`, `remove` | Give or take a role | Manage roles |
| `/jailed` | Members in the gulag right now | Timeout members |
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
| `/automod ghostping` | Report messages that pinged someone and were deleted quickly |
| `/automod dryrun rule enabled` | A rule only reports what it would do |
| `/automod test text member` | Show which rule a text would trigger, nothing is deleted |
| `/automod toggle rule:shortlinks`, `rule:newlinks` | Follow short links, no links for new members |
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
| `/notify topic add`, `remove`, `panel` and `/notify subscribe`, `unsubscribe`, `list` | Notification topics |
| `/ticket setup`, `panel`, `addtype`, `removetype`, `add`, `remove`, `claim`, `rename`, `list`, `close` | Tickets |
| `/poll create`, `end`, `list` | Polls, optionally with multiple choices |
| `/giveaway start`, `end`, `reroll`, `cancel`, `edit`, `list` | Giveaways |
| `/starboard setup`, `ignore`, `show` | Starboard |
| `/tempvoice setup` | Temporary voice channels |
| `/voice rename`, `limit`, `lock`, `unlock`, `kick`, `transfer`, `claim` | Owner commands for your own voice room |
| `/suggest text`, `/suggestion status`, `/suggestion setup set` | Suggestions |
| `/xp config`, `show`, `boost`, `channelboost`, `resetall`, `give`, `take`, `setlevel`, `reset`, `ignore` | XP system, rank card on or off, XP boost per role |
| `/xp levelrole add`, `remove`, `list`, `sync` | Roles for levels |
| `/rank`, `/leaderboard` | Level as an image card and top list |
| `/birthday set`, `remove`, `show`, `upcoming`, `list` and `/birthday setup set`, `user`, `clear` | Birthdays |

## Information and utility

| Command | Description |
| --- | --- |
| `/userinfo`, `/serverinfo`, `/roleinfo`, `/avatar` | Look up users, the server and roles |
| `/ping`, `/botinfo` | Latency, version, uptime and statistics |
| `/help command` | List commands or explain one |
| `/say channel message` | Send a message in the name of the bot |
| `/embed channel title description` | Post an announcement embed |
| `/tag create`, `edit`, `delete`, `show`, `list`, `info` | Custom commands |
| `/autoresponder add`, `remove`, `list` | Automatic answers to trigger words |
| `/remind set`, `list`, `cancel` | Reminders |
| `/afk reason` | Away status |

## Mod-mail and ban appeals

| Command | Description |
| --- | --- |
| `/modmail setup set`, `panel`, `block`, `status` | Configure mod-mail and post the button |
| `/modmail send`, `close` | Write in a conversation, close it |
| `/appeal setup set`, `status` | Configure ban appeals |
| `/appeal send` | Ask the staff of the main server to lift your ban (used on the appeal server) |

## Counting, sticky messages and statistics

| Command | Description |
| --- | --- |
| `/counting setup`, `status`, `set`, `off` | Counting game |
| `/sticky set`, `remove`, `list` | Messages that stay at the bottom of a channel |
| `/stats create`, `add`, `remove`, `list`, `refresh` | Channels that show live numbers |

## Security and diagnostics

| Command | Description | Default permission |
| --- | --- | --- |
| `/modwatch status`, `limit`, `action`, `exclude` | Alarm when a moderator bans, kicks or times out too often | Administrator |
| `/permaudit run`, `watch`, `trust` | Roles with dangerous permissions, alarm for new ones | Administrator |
| `/report send message_link reason` and the menu entry "Report message" | Report a message to the staff | Everyone |
| `/report setup set`, `clearping`, `ignorechannel`, `status` | Report channel, ping role, cooldown | Manage server |
| `/invites who`, `stats`, `top`, `setup` | Which invite brought a member, top inviters | Timeout members |
| `/diagnose` | Check permissions, role order, channels and roles | Manage server |
| `/debug status`, `errorchannel`, `errortest`, `selftest`, `usagestats`, `usage` | Error reports, start-up check, statistics | Administrator |
| `/debug level`, `/debug db` | Log level, database check and vacuum (owner of the bot only) | Administrator |
| `/config export`, `import` | Download or load the settings of a server | Administrator |

## Music

| Command | Description |
| --- | --- |
| `/play query` | Play a link, or search the library and then the web |
| `/music queue`, `nowplaying`, `skip`, `pause`, `resume`, `stop`, `join`, `leave` | Control playback |
| `/music volume`, `loop`, `shuffle`, `remove`, `clear`, `seek` | Volume, repeat, order, jump to a position |
| `/music library search`, `list`, `play`, `scan`, `info` | The music folder |
| `/music library download url format` | Save a link in the library as Artist/Album/Track (off by default) |
| `/music settings`, `cleardj`, `status` | DJ role, limits, allowed features |

## Setup and languages

| Command | Description | Default permission |
| --- | --- | --- |
| `/setup` | Guided setup with buttons and menus: log channel, welcome channel, staff roles, gulag, AutoMod preset, server template, language | Manage server |
| `/health` | What is set up, what is open, and the self-test | Manage server |
| `/language code` | Language of the texts that members see (12 languages) | Manage server |

## Economy

| Command | Description | Default permission |
| --- | --- | --- |
| `/economy balance`, `daily`, `work`, `pay`, `leaderboard`, `inventory` | Balance, rewards, payments and ranking | Everyone |
| `/economy shop` and `/economy buy item` | The shop and buying from it | Everyone |
| `/economy give`, `shopadd`, `shopremove`, `config` | Staff: balances, shop items and currency settings | Manage server |

## Role menus, scheduled messages and feeds

| Command | Description | Default permission |
| --- | --- | --- |
| `/rolemenu create`, `add`, `remove`, `delete`, `list` | Menus with buttons or a dropdown that give roles | Manage server |
| `/schedule add`, `list`, `remove`, `timezone` | Messages posted later or repeated hourly, daily, weekly | Manage server |
| `/feed add`, `list`, `check`, `remove` | New YouTube videos, Twitch streams and RSS items | Manage server |

## Activity and bulk moderation

| Command | Description | Default permission |
| --- | --- | --- |
| `/activity overview`, `channels`, `growth`, `reset` | Messages, busiest channels, joins and leaves (counts only) | Manage server |
| `/bulk ban`, `kick`, `timeout` | Up to 25 users at once after a confirmation | The permission of the action |
| `/cases user kind search text moderator days` | Search the moderation history | Timeout members |
| `/case link` and `/case unlink` | Link two cases, for example a note to a ban | Timeout members |

## Anti-scam

| Command | Description | Default permission |
| --- | --- | --- |
| `/antiscam status`, `set`, `words`, `forget` | Settings, word lists and remembered scam images | Manage server |
| `/antiscam test text` and `/antiscam testimage image` | See the score of a text or the text read from an image | Manage server |
| `/antiscam set learn_emoji` | Emoji with which a moderator reacts to a message to teach it as scam | Manage server |
| Context menu `Mark as scam` | Delete the message and remember its images and text | Manage messages |

## Probation and blocklist

| Command | Description | Default permission |
| --- | --- | --- |
| `/probation setup`, `status`, `release`, `add` | New members get a role and may not post links or files until minutes or normal messages passed | Manage server |
| `/raid swarm` | Detect groups of new accounts with the same name, picture or creation time | Manage server |
| `/case timeline user` | Account, join and invite, probation, cases and appeals of one user in time order | Timeout members |
| `/block kind value image`, `/unblock kind number`, `/blocklist` | Short commands for the AutoMod blocklist (links, message texts, images) | Manage messages |

## Message builder and updates

| Command | Description | Default permission |
| --- | --- | --- |
| `/message send channel json file url` | Post a message with embeds and link buttons from JSON, a file or a https link | Manage messages |
| `/message edit message json file url` | Change a message of the bot | Manage messages |
| `/message preview json file url` | Show the result only to you | Manage messages |
| `/message copy message` | Export a message of this server as JSON | Manage messages |
| `/debug update action` | Show the update state, check GitHub, or install a newer version (owner of the bot) | Owner of the bot |

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
