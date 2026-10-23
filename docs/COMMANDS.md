# Command reference

Commands marked with a slash work as slash commands. Moderation commands also work with the prefix (default `!`), for example `!warn @user spam`.

The complete list of all slash commands with their options is in [REFERENCE.md](REFERENCE.md) (generated).

Every command name can be changed in `settings.json` under `command_names`, and every module or single command can be turned off per server with `/admin module` and `/admin command`.

<!-- toc -->

- [Command groups](#command-groups)
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
- [Panels](#panels)
- [Skills and AI](#skills-and-ai)
- [Probation and blocklist](#probation-and-blocklist)
- [Message builder and updates](#message-builder-and-updates)
- [Privacy](#privacy)
- [Structure, members and team](#structure-members-and-team)
- [Administration](#administration)

<!-- tocstop -->

<!-- groups -->
## Command groups

To save slash command slots (Discord allows 100 top-level commands per bot), related commands are grouped. Type the group first, then the command, for example `/moderation ban`. Text commands with the prefix, for example `!ban`, are not affected. Permissions, aliases and module switches keep using the plain command name.

| Group | Contains |
| --- | --- |
| `/moderation` | `warn`, `unwarn`, `warnings`, `clearwarns`, `note`, `mute`, `unmute`, `kick`, `ban`, `unban`, `tempban`, `jail`, `unjail`, `jailed`, `role`, `case`, `cases`, `bulk`, `escalation`, `purge`, `slowmode` |
| `/security` | `antinuke`, `antiscam`, `raid`, `block`, `unblock`, `blocklist`, `approval` |
| `/access` | `verify`, `probation`, `lockdown`, `lockdownconfig`, `unlock`, `lockchannel`, `unlockchannel`, `jailsetup` |
| `/server` | `log`, `backup`, `privacy`, `invites`, `stats`, `serverinfo`, `roleinfo`, `health`, `diagnose`, `debug` |
| `/admin` | `settings`, `config`, `module`, `command`, `perms`, `alias`, `prefix`, `language`, `setup`, `history`, `exceptions`, `dashaccess` |
| `/info` | `about`, `avatar`, `botinfo`, `ping`, `userinfo`, `mydata`, `leaderboard`, `rank`, `find` |
| `/community` | `welcome`, `booster`, `afk`, `remind`, `activity`, `tempvoice`, `voice` |
| `/engage` | `economy`, `giveaway`, `poll`, `counting`, `starboard` |
| `/support` | `ticket`, `suggest`, `tag`, `autoresponder`, `skill`, `ai` |
| `/members` | `stickyroles`, `nickname`, `watch`, `reason` |
| `/structure` | `channel`, `category`, `archive`, `temprole`, `roletemplate`, `rules` |
| `/team` | `teamstats`, `weekly`, `duty`, `apply`, `modwatch`, `permaudit` |
| `/post` | `say`, `embed`, `message`, `sticky`, `schedule`, `feed`, `reactionrole`, `rolemenu` |
| | `/help`, `/play`, `/automod`, `/music`, `/xp`, `/modmail`, `/appeal`, `/report`, `/suggestion`, `/birthday`, `/notify` |

## Moderation

| Command | Description | Default permission |
| --- | --- | --- |
| `/moderation warn member reason` | Warn a member, reason is optional | Timeout members |
| `/moderation unwarn case_id` | Remove one warning | Timeout members |
| `/moderation clearwarns user` | Remove all active warnings of a user | Timeout members |
| `/moderation mute member duration reason` | Timeout, for example `30m`, `2h`, `1d` | Timeout members |
| `/moderation unmute member` | Remove a timeout | Timeout members |
| `/moderation kick member reason` | Kick a member | Kick members |
| `/moderation ban user reason` | Ban a user, also by ID | Ban members |
| `/moderation unban user` | Unban a user by ID | Ban members |
| `/moderation cases user kind search page` | History, filter by mention, user ID, type or part of a name | Timeout members |
| `/moderation warnings user` | Warnings of one user | Timeout members |
| `/moderation case view`, `edit`, `delete` | Show a case, change its reason, delete it | Timeout members |
| `/moderation note user text` | Private moderator note about a user | Timeout members |
| `/moderation tempban user duration reason` | Ban for a limited time, lifted automatically | Ban members |
| `/moderation purge amount user kind` | Delete many messages, filter by user or type | Manage messages |
| `/moderation slowmode seconds channel` | Slowmode of a channel | Manage channels |
| `/access lockchannel`, `/access unlockchannel` | Lock or unlock one channel | Manage channels |
| `/moderation role add`, `remove` | Give or take a role | Manage roles |
| `/moderation jailed` | Members in the gulag right now | Timeout members |
| `/moderation escalation list`, `set`, `remove` | Automatic punishments, for example 3 warnings = timeout | Manage server |

Who may use these commands can be changed with `/admin perms allow`, `/admin perms deny`, `/admin perms reset` and `/admin perms show`.

## Gulag (jail)

| Command | Description |
| --- | --- |
| `/moderation jail member duration reason` | Send a member to the gulag channel, duration (`30m`, `2h`, `1d`) and reason are optional |
| `/moderation unjail member reason` | Release a member and give the old roles back |
| `/access jailsetup setup` | Create or select role, channel and staff role |
| `/access jailsetup apply` | Apply the channel permissions again |
| `/access jailsetup notice` | Set a custom notice, empty restores the default security steps |
| `/access jailsetup preview` | Show the notice and the reminder |
| `/access jailsetup reminder` | Notice with mention for everyone in the gulag, reminder every few minutes, release requests with the release word |

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
| `/access lockdown mode reason` and `/access unlock` | Lock or unlock the server. Mode `channels` edits every channel, mode `role` edits only the @everyone role and is instant |
| `/access lockdownconfig mode`, `lockrole`, `bypassrole`, `exempt` | Default mode, extra roles locked in role mode, roles that can still write, channels that stay open |
| `/access verify setup`, `panel`, `apply`, `member`, `off` | Verification gate with button, captcha or math question, optional kick after a timeout |
| `/security raid setup` | Join-rate detection, minimum account age, automatic lockdown |
| `/security antinuke setup`, `limit`, `newbots`, `whitelist`, `staffrole`, `servername`, `restore`, `status` | Mass deletions, bans, kicks, permission grants, new webhooks, added bots, server renames and nuke talk |
| `/server backup create`, `schedule`, `list`, `download`, `delete`, `restore` | Roles with order, channels with member overwrites, emojis, webhooks and member roles. Backups can run automatically |

## Logging

| Command | Description |
| --- | --- |
| `/server log set category channel` | Categories: main, messages, members, voice, server, moderation, security |
| `/server log sent enabled` | Log every sent message on or off |
| `/server log show` | Show the log channels |

## Community

| Command | Description |
| --- | --- |
| `/community welcome set`, `autorole`, `botrole`, `test` | Welcome and goodbye messages, auto roles |
| `/community booster set`, `role` | Booster rewards |
| `/post reactionrole add`, `remove`, `list`, `panel` | Reaction roles with any emoji |
| `/notify topic add`, `remove`, `panel` and `/notify subscribe`, `unsubscribe`, `list` | Notification topics |
| `/support ticket setup`, `panel`, `addtype`, `removetype`, `add`, `remove`, `claim`, `rename`, `list`, `close` | Tickets |
| `/engage poll create`, `end`, `list` | Polls, optionally with multiple choices |
| `/engage giveaway start`, `end`, `reroll`, `cancel`, `edit`, `list` | Giveaways |
| `/engage starboard setup`, `ignore`, `show` | Starboard |
| `/community tempvoice setup` | Temporary voice channels |
| `/community voice rename`, `limit`, `lock`, `unlock`, `kick`, `transfer`, `claim` | Owner commands for your own voice room |
| `/support suggest text`, `/suggestion status`, `/suggestion setup set` | Suggestions |
| `/xp config`, `show`, `boost`, `channelboost`, `resetall`, `give`, `take`, `setlevel`, `reset`, `ignore` | XP system, rank card on or off, XP boost per role |
| `/xp levelrole add`, `remove`, `list`, `sync` | Roles for levels |
| `/info rank`, `/info leaderboard` | Level as an image card and top list |
| `/birthday set`, `remove`, `show`, `upcoming`, `list` and `/birthday setup set`, `user`, `clear` | Birthdays |

## Information and utility

| Command | Description |
| --- | --- |
| `/info userinfo`, `/server serverinfo`, `/server roleinfo`, `/info avatar` | Look up users, the server and roles |
| `/info ping`, `/info botinfo` | Latency, version, uptime and statistics |
| `/help command` | List commands or explain one |
| `/post say channel message` | Send a message in the name of the bot |
| `/post embed channel title description` | Post an announcement embed |
| `/support tag create`, `edit`, `delete`, `show`, `list`, `info` | Custom commands |
| `/support autoresponder add`, `remove`, `list` | Automatic answers to trigger words |
| `/community remind set`, `list`, `cancel` | Reminders |
| `/community afk reason` | Away status |

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
| `/engage counting setup`, `status`, `set`, `off` | Counting game |
| `/post sticky set`, `remove`, `list` | Messages that stay at the bottom of a channel |
| `/server stats create`, `add`, `remove`, `list`, `refresh` | Channels that show live numbers |

## Security and diagnostics

| Command | Description | Default permission |
| --- | --- | --- |
| `/team modwatch status`, `limit`, `action`, `exclude` | Alarm when a moderator bans, kicks or times out too often | Administrator |
| `/team permaudit run`, `watch`, `trust` | Roles with dangerous permissions, alarm for new ones | Administrator |
| `/report send message_link reason` and the menu entry "Report message" | Report a message to the staff | Everyone |
| `/report setup set`, `clearping`, `ignorechannel`, `status` | Report channel, ping role, cooldown | Manage server |
| `/server invites who`, `stats`, `top`, `setup` | Which invite brought a member, top inviters | Timeout members |
| `/server diagnose` | Check permissions, role order, channels and roles | Manage server |
| `/server debug status`, `errorchannel`, `errortest`, `selftest`, `usagestats`, `usage` | Error reports, start-up check, statistics | Administrator |
| `/server debug level`, `/server debug db` | Log level, database check and vacuum (owner of the bot only) | Administrator |
| `/admin config export`, `import` | Download or load the settings of a server | Administrator |

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
| `/admin setup` | Guided setup with buttons and menus: log channel, welcome channel, staff roles, gulag, AutoMod preset, server template, language | Manage server |
| `/server health` | What is set up, what is open, and the self-test | Manage server |
| `/admin language code` | Language of the texts that members see (12 languages) | Manage server |

## Economy

| Command | Description | Default permission |
| --- | --- | --- |
| `/engage economy balance`, `daily`, `work`, `pay`, `leaderboard`, `inventory` | Balance, rewards, payments and ranking | Everyone |
| `/engage economy shop` and `/engage economy buy item` | The shop and buying from it | Everyone |
| `/engage economy give`, `shopadd`, `shopremove`, `config` | Staff: balances, shop items and currency settings | Manage server |

## Role menus, scheduled messages and feeds

| Command | Description | Default permission |
| --- | --- | --- |
| `/post rolemenu create`, `add`, `remove`, `delete`, `list` | Menus with buttons or a dropdown that give roles | Manage server |
| `/post schedule add`, `list`, `remove`, `timezone` | Messages posted later or repeated hourly, daily, weekly | Manage server |
| `/post feed add`, `list`, `check`, `remove` | New YouTube videos, Twitch streams and RSS items | Manage server |

## Activity and bulk moderation

| Command | Description | Default permission |
| --- | --- | --- |
| `/community activity overview`, `channels`, `growth`, `reset` | Messages, busiest channels, joins and leaves (counts only) | Manage server |
| `/moderation bulk ban`, `kick`, `timeout` | Up to 25 users at once after a confirmation | The permission of the action |
| `/moderation cases user kind search text moderator days` | Search the moderation history | Timeout members |
| `/moderation case link` and `/moderation case unlink` | Link two cases, for example a note to a ban | Timeout members |

## Anti-scam

| Command | Description | Default permission |
| --- | --- | --- |
| `/security antiscam status`, `set`, `words`, `forget` | Settings, word lists and remembered scam images | Manage server |
| `/security antiscam test text` and `/security antiscam testimage image` | See the score of a text or the text read from an image | Manage server |
| `/security antiscam set learn_emoji` | Emoji with which a moderator reacts to a message to teach it as scam | Manage server |
| `/security antiscam set learned`, `similar`, `ham_sampling` | Learned filter, similar images and learning from normal messages | Manage server |
| Context menu `Mark as scam` | Delete the message and remember its images and text | Manage messages |
| Context menu `Not a scam` | Teach the learned filter that a message is fine | Manage messages |

## Panels

| Command | Description | Default permission |
| --- | --- | --- |
| `/panel create` | New panel, empty or from a template (welcome, rules, roles, notifications, verify) | Manage server |
| `/panel section`, `removesection` | Banner, title, text, colour, pictures and footer of a section | Manage server |
| `/panel button`, `removebutton`, `single` | Role, verify and link buttons, one role at a time | Manage server |
| `/panel post`, `update`, `preview`, `list`, `show`, `delete` | Post, change in place, look at and manage panels | Manage server |

## Skills and AI

| Command | Description | Default permission |
| --- | --- | --- |
| `/support skill run`, `list` | Use a skill, list the skills | Everyone |
| `/support skill create`, `edit`, `show`, `import`, `enable`, `disable`, `delete`, `panel`, `stats` | Build and manage skills | Manage server |
| `/support ai setup`, `status`, `limits`, `remove`, `privacy` | Connect a provider with your own key and set limits | Manage server |
| `/support ai make wish` | Let the AI build a skill, with a preview before saving | Manage server |

## Probation and blocklist

| Command | Description | Default permission |
| --- | --- | --- |
| `/access probation setup`, `status`, `release`, `add` | New members get a role and may not post links or files until minutes or normal messages passed | Manage server |
| `/security raid swarm` | Detect groups of new accounts with the same name, picture or creation time | Manage server |
| `/moderation case timeline user` | Account, join and invite, probation, cases and appeals of one user in time order | Timeout members |
| `/security block kind value image`, `/security unblock kind number`, `/security blocklist` | Short commands for the AutoMod blocklist (links, message texts, images) | Manage messages |

## Message builder and updates

| Command | Description | Default permission |
| --- | --- | --- |
| `/post message send channel json file url` | Post a message with embeds and link buttons from JSON, a file or a https link | Manage messages |
| `/post message edit message json file url` | Change a message of the bot | Manage messages |
| `/post message preview json file url` | Show the result only to you | Manage messages |
| `/post message copy message` | Export a message of this server as JSON | Manage messages |
| `/server debug update action` | Show the update state, check GitHub, or install a newer version (owner of the bot) | Owner of the bot |

## Privacy

| Command | Description |
| --- | --- |
| `/info mydata export` and `/info mydata delete` | Members export or delete their own stored data |
| `/server privacy retention`, `delete`, `export` | Retention time for members who left, deletion and export by user ID |

Details are in [PRIVACY.md](PRIVACY.md).

## Structure, members and team

| Command | Description |
| --- | --- |
| `/structure channel create`, `clone`, `rename`, `move`, `sort`, `copyperms` | Manage channels |
| `/structure category create`, `clone`, `rename`, `sort`, `sync` | Manage categories |
| `/structure archive setup`, `ignore`, `scan`, `status` | Report or move inactive channels |
| `/structure temprole give`, `remove`, `list` | Roles for a limited time |
| `/structure roletemplate save`, `apply`, `list`, `delete` | Role templates |
| `/structure rules setup`, `add`, `edit`, `remove`, `list`, `post`, `status` | Rules with accept button and version |
| `/members stickyroles setup`, `exclude`, `status`, `forget` | Restore roles and punishments of returning members |
| `/members nickname setup`, `word`, `exempt`, `list`, `check`, `scan` | Name moderation |
| `/members watch add`, `remove`, `list`, `setup` | Silent watch list |
| `/members reason add`, `remove`, `list`, `use` | Reason templates with fixed punishment |
| `/security approval setup`, `list`, `cancel` | Four-eyes approval |
| `/moderation case undo` | Take a case back with its follow-up actions |
| `/moderation escalation expiry` | Days until warnings expire |
| `/admin history list`, `show`, `rollback`, `keep`, `copy` | Settings history, rollback and copy to another server |
| `/admin exceptions add`, `remove`, `list` | Channels and roles left out of AutoMod and Anti-Scam |
| `/admin dashaccess add`, `remove`, `list` | Dashboard roles viewer and mod |
| `/team teamstats overview`, `member`, `inactive` | Work of the moderators |
| `/team weekly setup`, `now` | Weekly report |
| `/team duty away`, `back`, `list`, `route`, `roster` | Sign off and route tickets, mod-mail and reports |
| `/team apply start`, `setup`, `question`, `list`, `decide` | Staff applications with a team vote |

## Administration

| Command | Description |
| --- | --- |
| `/admin module list`, `enable`, `disable` | Turn features on or off |
| `/admin command list`, `enable`, `disable` | Turn single commands on or off |
| `/admin prefix` | Change the prefix of text commands |
| `/admin alias add`, `remove`, `list` | Short names for text commands |
| `/admin perms allow`, `deny`, `reset`, `show` | Who may use which command |
| `/admin config get`, `set`, `reset` | Read and change any setting, for example `/admin config set automod.caps.percent 80` |
| `/admin settings` | Overview |
| `/help` | Command overview |
| `/info about` | Version and support |
