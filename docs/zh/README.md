# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | **中文** | [日本語](../ja/README.md) | [한국어](../ko/README.md)

自行托管的 Discord 机器人，用于管理、安全和社区。开源、免费，数据只保存在你自己的电脑上。

<!-- toc -->

- [关于项目](#关于项目)
- [功能](#功能)
  - [安全](#安全)
  - [管理](#管理)
  - [日志](#日志)
  - [社区](#社区)
  - [运维](#运维)
- [项目状态](#项目状态)
- [运行要求](#运行要求)
- [快速开始](#快速开始)
- [机器人权限](#机器人权限)
- [在 Discord 中的第一步](#在-discord-中的第一步)
- [命令](#命令)
  - [管理](#管理-1)
  - [古拉格（关押）](#古拉格关押)
  - [自动管理](#自动管理)
  - [防袭击与锁定](#防袭击与锁定)
  - [防破坏](#防破坏)
  - [验证](#验证)
  - [日志](#日志-1)
  - [欢迎、告别与助力者](#欢迎告别与助力者)
  - [工单](#工单)
  - [投票与抽奖](#投票与抽奖)
  - [建议与星标板](#建议与星标板)
  - [经验与等级](#经验与等级)
  - [反应身份组与通知](#反应身份组与通知)
  - [生日](#生日)
  - [临时语音频道](#临时语音频道)
  - [备份与恢复](#备份与恢复)
  - [数据与隐私](#数据与隐私)
  - [运维](#运维-1)
- [消息占位符](#消息占位符)
- [配置](#配置)
- [数据与存储](#数据与存储)
- [仓库结构](#仓库结构)
- [路线图](#路线图)
- [隐私与安全](#隐私与安全)
- [支持](#支持)
- [许可证](#许可证)

<!-- tocstop -->

## 关于项目

GuardBot 集成了许多服务器在托管机器人上付费使用的功能：管理、日志、防袭击（Anti-Raid）、防破坏（Anti-Nuke）、工单、等级等。你可以自己运行它，在自己的电脑或小型 VPS 上。

托管机器人会把服务器数据、成员 ID，有时还有电子邮件地址保存在第三方手中。自己托管时，这些数据不会离开你的电脑。GuardBot 想证明，任何人都可以不付订阅费就运行功能完整的机器人。

## 功能

### 安全

- 自动管理：词语过滤、大写过滤、提及刷屏、邀请链接、钓鱼域名、个人信息、人肉搜索和威胁。所有列表都可以编辑。
- 防袭击：检测短时间内的大量加入，并可锁定整个服务器。
- 防破坏：限制批量删除和封禁，自动响应，并私信服务器所有者。
- 古拉格频道：发布诈骗链接或图片的成员会被移入唯一的频道，并看到账号安全指引。管理员也可以使用 /jail 和 /unjail。
- 通过按钮或验证码验证，并自动移除未及时验证的成员。
- 防破坏还会监控权限授予、新建 Webhook、被添加的机器人以及服务器改名。

### 管理

- 警告、禁言、踢出、封禁和关押，历史记录可按提及、用户 ID 或类型筛选。
- 自动升级处罚，例如三次警告后自动超时。
- 可设置哪些身份组或用户可以使用各个管理命令。

### 日志

- 记录已发送、已编辑和已删除的消息，包括图片、GIF 和链接，并支持分开的日志频道。
- 记录身份组、昵称、封禁、语音、频道和服务器身份组的变更。

### 社区

- 欢迎与告别消息、自动身份组和助力者奖励。
- 工单、投票、抽奖和建议。
- 支持任意表情的反应身份组，以及成员可自行开关的通知主题。
- 聊天和语音的经验与 1 到 100 级、等级身份组和生日。
- 星标板和临时语音频道。
- 限时关押、多选投票、图片形式的等级卡以及按身份组的经验加成。

### 运维

- 每个模块和每个命令都可以按服务器开启或关闭。
- 自定义前缀、命令别名和可重命名的命令。
- 身份组和频道结构的备份与恢复。
- 按计划自动备份身份组、频道、表情和 Webhook，并提供只补充缺失内容的恢复命令。

## 项目状态

GuardBot 还很年轻，尚未在大型服务器上使用过。自动化测试（`python -m unittest`）覆盖存储、个人信息检测、等级计算、命令注册、权限检查以及文档链接。所有需要真实 Discord 服务器的功能，例如锁定、备份恢复、验证、防破坏和古拉格，都不在测试范围内。请先在测试服务器上试用这些功能，再依赖它们。文档的翻译尚未由母语者审阅，欢迎提出修改意见。

## 运行要求

- Python 3.11 或更高版本
- 带有机器人令牌的 Discord 应用
- 一台持续在线的电脑或 VPS

## 快速开始

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

完整的分步指南见 [GUIDE.md](GUIDE.md).

## 机器人权限

最简单的方式是授予管理员权限。如果想使用最小权限，请授予下列权限，并在 Developer Portal 中开启 Server Members 和 Message Content 两个 Intent：

```
Basics
  View Channels, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions
Moderation
  Moderate Members (timeouts), Kick Members, Ban Members, Manage Messages
Roles and channels
  Manage Roles, Manage Channels (gulag, lockdown, verification, tickets, backup)
Optional
  View Audit Log (who did what in logs and anti-nuke), Move Members, Manage Webhooks, Create Expressions
```

## 在 Discord 中的第一步

一个合理的初始配置。在你的服务器中执行这些命令，并把频道和身份组替换为你自己的：

```
/log set category:main channel:#logs
/jailsetup setup
/automod toggle rule:phishing enabled:True action:jail
/automod toggle rule:words enabled:True
/automod add name:words value:example
/raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3
/antinuke setup enabled:True action:strip
/verify setup channel:#verify mode:captcha timeout_minutes:30
/welcome set channel:#welcome message:Welcome {user} to {server}!
/backup schedule enabled:True interval_hours:24 keep:7
/xp config enabled:True
/module list
```

## 命令

大多数命令是斜杠命令，管理命令也支持前缀。完整列表见命令参考： [COMMANDS.md](../COMMANDS.md).

### 管理

警告、禁言、踢出和封禁既可作为斜杠命令使用，也可用前缀，例如 `!warn @User spam`。每个操作都会生成一个带编号的记录。

```
/warn member:@User reason:Spam                    # also: !warn @User Spam
/unwarn case_id:12                                 # remove one warning
/clearwarns user:@User                             # remove all active warnings
/mute member:@User duration:30m reason:Spam        # also: !mute @User 30m Spam
/unmute member:@User
/kick member:@User reason:Advertising
/ban user:@User reason:Raid                        # user can also be an ID
/unban user:123456789012345678

/cases user:@User                                  # history, filter by mention or ID
/cases kind:ban page:2                             # filter by type
/cases search:john                                 # filter by part of a name
/warnings user:@User
/case case_id:12

/escalation list
/escalation set warns:3 action:timeout minutes:60  # 3 warnings = 1 hour timeout
/escalation set warns:5 action:kick
/escalation set warns:7 action:ban                 # actions: timeout, kick, ban, jail
/escalation remove warns:5
```

### 古拉格（关押）

账号被盗的成员会被移到唯一的频道，并看到安全指引。释放时会恢复他们原来的身份组。

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
```

### 自动管理

规则会删除或处罚匹配的消息。每条规则可选择动作：log、delete、warn、timeout 或 jail。

```
/automod toggle rule:words enabled:True action:delete
/automod toggle rule:phishing enabled:True action:jail
/automod toggle rule:pii enabled:True action:delete
# rules: words, caps, mentions, invites, phishing, pii, doxxing, threats
# actions: log, delete, warn, timeout, jail

/automod add name:words value:badword              # lists: words, phishing, phishing_allow,
/automod remove name:words value:badword           #        invites_allow, doxxing, threats
/automod show name:phishing
/automod import name:phishing file:<upload a .txt, one entry per line>

/automod set rule:caps option:percent value:80
/automod set rule:caps option:min_len value:15
/automod set rule:mentions option:max value:5
/automod set rule:phishing option:lookalike value:True

/automod channel channel:#media images:True videos:True links:False
/automod channel links:True                        # no channel = all channels without own rule
/automod unchannel channel:#media

/automod block kind:link value:evil.example
/automod block kind:message value:free nitro
/automod block kind:image image:<upload a picture>
/automod blocklist
/automod unblock kind:link number:1

/automod flood enabled:True count:5 seconds:5 timeout:10
/automod exemptrole role:@Moderator
/automod exemptchannel channel:#bot-commands
```

### 防袭击与锁定

检测短时间内的大量加入，并可锁定服务器。channels 模式会修改每个频道，role 模式立即生效。

```
/raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3 lockdown:True
# 5 joins within 10 seconds count as a raid, accounts younger than 3 days are punished,
# actions: alert, timeout, kick

/lockdown mode:role reason:Raid                    # instant, edits only the @everyone role
/lockdown mode:channels reason:Raid                # thorough, edits every channel
/unlock

/lockdownconfig mode mode:role                     # default mode
/lockdownconfig lockrole role:@Member              # extra role locked in role mode
/lockdownconfig bypassrole role:@Moderator         # can still write in channels mode
/lockdownconfig exempt channel:#announcements
```

### 防破坏

监控审计日志，在有人破坏服务器时作出反应。服务器所有者会收到私信。

```
/antinuke setup enabled:True action:strip notify_owner:True   # actions: alert, strip, kick, ban
/antinuke limit kind:channel_delete count:3 seconds:10
# kinds: channel_delete, role_delete, channel_create, ban, kick,
#        role_perm, role_grant, webhook_create, bot_add, guild_update
/antinuke whitelist user:@TrustedAdmin             # toggle, never checked
/antinuke staffrole role:@Moderator                # toggle, shown in alerts
/antinuke servername name:MyServer                 # extra name for the nuke talk detection
/antinuke newbots kick:True                        # kick bots added by untrusted users
/antinuke restore member:@User                     # give back roles that were removed
/antinuke status
```

### 验证

新成员在点击按钮或完成验证码之前，只能看到验证频道。

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### 日志

为每个类别选择一个频道，或用一个主频道记录全部内容。

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### 欢迎、告别与助力者

消息、自动身份组以及服务器助力者奖励。

```
/welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/welcome autorole role:@Member                     # toggle, given to every new member
/welcome botrole role:@Bots                        # toggle, given to every new bot
/welcome test

/booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/booster role role:@Booster                        # toggle
```

### 工单

成员通过按钮打开私密频道。关闭工单时会发送聊天记录。

```
/ticket setup category:Tickets support_role:@Support log_channel:#ticket-logs max_open:1
/ticket addtype key:report label:Report description:Report a member
/ticket removetype key:report
/ticket panel channel:#support title:Support description:Press a button to open a ticket

# inside a ticket
/ticket add member:@User
/ticket remove member:@User
/ticket close
```

### 投票与抽奖

用按钮投票和参与。时长支持 30m、2h、1d 等写法。

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### 建议与星标板

成员发布建议，管理团队可以批准或拒绝，热门消息会被突出显示。

```
/suggestionsetup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
```

### 经验与等级

聊天和语音经验、等级身份组、身份组加成和等级卡。

```
/xp config enabled:True min_xp:15 max_xp:25 cooldown:60 voice_xp:10 multiplier:1.5
/xp config max_level:100 stack_roles:True card:True
/xp config announce:channel announce_channel:#levels message:{user} reached level {level}!
/xp show
/xp boost role:@Booster multiplier:1.5             # 1.0 removes the boost
/xp ignore channel:#spam                           # toggle

/levelrole add level:10 role:@Active
/levelrole add level:50 role:@Veteran
/levelrole remove level:10
/levelrole list
/levelrole sync                                    # apply to everyone who already has XP

/xp give user:@User amount:500
/xp take user:@User amount:100
/xp setlevel user:@User level:20
/xp reset user:@User

/rank                                              # also: !rank, shows a rank card image
/rank user:@User
/leaderboard
```

### 反应身份组与通知

用任意表情通过反应发放身份组，并让成员自己选择通知主题。

```
/reactionrole panel channel:#roles title:Pick your roles description:React below
/reactionrole add message:<message link> emoji:<any emoji> role:@Gamer
/reactionrole add message:<message link> emoji:<any emoji> role:@Artist mode:unique
# mode unique: only one role of that message at a time
/reactionrole remove message:<message link> emoji:<any emoji>
/reactionrole list

/notifytopic add key:events role:@Events description:Server events
/notifytopic panel channel:#roles title:Notifications   # one button per topic
/notifytopic remove key:events
/notify subscribe topic:events                     # members choose for themselves
/notify unsubscribe topic:events
/notify list
```

### 生日

成员保存日期和月份，机器人当天发放身份组并发送消息。

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### 临时语音频道

加入中心频道会创建一个房间，房间空了就会消失。

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### 备份与恢复

备份包含身份组、频道、表情、Webhook 和成员身份组。恢复只补充缺失的内容。

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### 数据与隐私

成员可以导出和删除自己的数据。管理员控制数据保留多久。

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### 运维

开启或关闭模块和命令、更改前缀、设置别名，并把命令限制给指定身份组。

```
/module list
/module disable name:starboard
/module enable name:tickets
/command disable name:ban                          # single commands
/command enable name:ban
/command list

/prefix new_prefix:?                               # text commands now start with ?
/alias add alias:w command:warn                    # ?w @User Spam
/alias remove alias:w
/alias list

/perms allow command:ban target:@HeadModerator     # only this role may use /ban
/perms deny command:warn target:@Trainee
/perms reset command:ban
/perms show

/settings
/help
/about
```

## 消息占位符

这些占位符会在你设置的文本中被替换：

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthdaysetup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## 配置

全局选项在 settings.json 中设置。其余内容按服务器通过 /module、/command、/perms、/alias 和 /config 等命令配置。

要重命名命令，请把它加入 command_names 并重启机器人：

```json
{
  "prefix": "!",
  "data_dir": "data",
  "force_sync": false,
  "purge_on_guild_leave": false,
  "command_names": {
    "warn": "verwarnen",
    "ban": "sperren"
  }
}
```

每一项设置都可以用 /config 读取和修改。以下是最常用的路径：

```
/config get path:automod.caps.percent
/config set path:automod.caps.percent value:80
/config set path:mod.dm_user value:false             # no direct message on punishments
/config set path:mod.warn_expiry_days value:30       # warnings expire after 30 days
/config set path:mod.default_mute_minutes value:120
/config set path:automod.mentions.max value:5
/config set path:automod.phishing.lookalike value:true
/config set path:raid.joins value:8
/config set path:xp.cooldown value:45
/config set path:tickets.max_open value:2
/config set path:privacy.retention_days value:90
/config reset section:welcome                        # back to the defaults of one section
```

## 数据与存储

机器人保存的所有内容都在你自己的电脑上：

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

## 仓库结构

```
guardbot/
  main.py                 entry point
  requirements.txt
  settings.example.json   global options
  .env.example            token placeholder
  guardbot/
    core.py               bot class, storage, permission checks
    defaults.py           default settings of every module
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature group
  docs/                   documentation in 12 languages, COMMANDS.md, PRIVACY.md
  deploy/                 systemd service, Dockerfile, compose file
  scripts/                maintenance scripts
  tests/                  automated tests (python -m unittest)
  data/                   created at runtime, holds your settings and data
```

## 路线图

- 在你自己的电脑上运行的本地网页控制台，无需任何托管服务即可修改设置。
- 机器人消息的多语言翻译。
- 设置的导出与导入。

## 隐私与安全

- 没有遥测，也没有外部服务。机器人只与 Discord 通信。
- 所有数据都保存在你电脑的 data 文件夹中：设置、经验、生日（仅日期和月份）以及管理记录。
- 机器人会忽略成员发来的私信。
- 令牌从 .env 文件读取。切勿分享或上传。
- 成员可以用 /mydata 导出并删除自己的数据。管理员可设置已离开成员的数据保留多久。
- [PRIVACY.md](../PRIVACY.md)

## 支持

错误、想法和建议：请在 Discord 上联系我，@justyyin，或在 GitHub 上提交 issue。

## 许可证

基于 MIT 许可证发布。参见 [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
