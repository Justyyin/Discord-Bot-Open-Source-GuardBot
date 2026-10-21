# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | **한국어**

관리, 보안, 커뮤니티를 위한 자체 호스팅 Discord 봇. 오픈 소스이며 무료이고, 데이터는 내 컴퓨터에만 남습니다.

<!-- toc -->

- [프로젝트 소개](#프로젝트-소개)
- [기능](#기능)
  - [보안](#보안)
  - [관리](#관리)
  - [로그](#로그)
  - [커뮤니티](#커뮤니티)
  - [운영](#운영)
- [프로젝트 상태](#프로젝트-상태)
- [요구 사항](#요구-사항)
- [빠른 시작](#빠른-시작)
- [봇 권한](#봇-권한)
- [Discord에서의 첫 단계](#discord에서의-첫-단계)
- [명령어](#명령어)
  - [관리](#관리-1)
  - [굴라그(감금)](#굴라그감금)
  - [자동 관리](#자동-관리)
  - [레이드 방지와 락다운](#레이드-방지와-락다운)
  - [Anti-Nuke](#anti-nuke)
  - [인증](#인증)
  - [로그](#로그-1)
  - [환영, 작별, 부스터](#환영-작별-부스터)
  - [티켓](#티켓)
  - [투표와 경품 추첨](#투표와-경품-추첨)
  - [건의와 스타보드](#건의와-스타보드)
  - [XP와 레벨](#xp와-레벨)
  - [반응 역할과 알림](#반응-역할과-알림)
  - [생일](#생일)
  - [임시 음성 채널](#임시-음성-채널)
  - [백업과 복원](#백업과-복원)
  - [데이터와 개인정보](#데이터와-개인정보)
  - [운영](#운영-1)
- [메시지 자리표시자](#메시지-자리표시자)
- [설정](#설정)
- [데이터와 저장 위치](#데이터와-저장-위치)
- [저장소 구조](#저장소-구조)
- [로드맵](#로드맵)
- [개인정보 및 보안](#개인정보-및-보안)
- [지원](#지원)
- [라이선스](#라이선스)

<!-- tocstop -->

## 프로젝트 소개

GuardBot은 많은 서버가 호스팅 봇에 비용을 내고 쓰는 기능을 한데 모았습니다. 관리, 로그, Anti-Raid(레이드 방지), Anti-Nuke(서버 파괴 방지), 티켓, 레벨 등입니다. 내 컴퓨터나 작은 VPS에서 직접 운영합니다.

호스팅 봇은 서버 데이터, 멤버 ID, 때로는 이메일 주소를 제3자에게 저장합니다. 직접 호스팅하면 그 데이터는 내 컴퓨터를 떠나지 않습니다. GuardBot은 누구나 구독 없이 모든 기능을 갖춘 봇을 운영할 수 있다는 것을 보여 주려는 프로젝트입니다.

## 기능

### 보안

- 자동 관리: 단어 필터, 대문자 필터, 멘션 도배, 초대 링크, 피싱 도메인, 개인정보, 신상 공개, 협박. 모든 목록을 편집할 수 있습니다.
- 짧은 시간에 몰리는 입장을 감지하는 Anti-Raid와 모든 채널을 잠그는 서버 락다운.
- Anti-Nuke: 대량 삭제와 대량 차단의 한도, 자동 대응, 서버 소유자에게 보내는 다이렉트 메시지.
- 굴라그 채널: 사기 링크나 이미지를 올린 멤버는 계정 보안 안내가 있는 단 하나의 채널로 이동합니다. 관리자는 /jail과 /unjail도 사용할 수 있습니다.
- 버튼 또는 캡차 인증과, 제때 인증하지 않은 멤버의 자동 제거.
- Anti-Nuke는 권한 부여, 새 웹훅, 추가된 봇, 서버 이름 변경도 감시합니다.

### 관리

- 경고, 뮤트, 추방, 차단, 감금과 멘션·사용자 ID·유형으로 필터링할 수 있는 기록.
- 자동 단계 상향. 예를 들어 경고 3회면 타임아웃됩니다.
- 각 관리 명령어를 사용할 수 있는 역할이나 사용자를 정할 수 있습니다.

### 로그

- 전송, 수정, 삭제된 메시지(이미지, GIF, URL 포함)를 별도의 로그 채널에 기록합니다.
- 역할, 닉네임, 차단, 음성, 채널, 서버 역할의 변경.

### 커뮤니티

- 환영 및 작별 메시지, 자동 역할, 부스터 보상.
- 티켓, 투표, 경품 추첨, 건의.
- 원하는 이모지를 쓰는 반응 역할과 멤버가 직접 켜고 끄는 알림 주제.
- 채팅과 음성의 XP 및 1~100 레벨, 레벨 역할, 생일.
- 스타보드와 임시 음성 채널.
- 기간이 있는 감금, 복수 선택 투표, 이미지 형태의 랭크 카드, 역할별 XP 부스트.

### 운영

- 모든 모듈과 개별 명령어를 서버별로 켜고 끌 수 있습니다.
- 사용자 지정 접두사, 명령어 별칭, 이름을 바꿀 수 있는 명령어.
- 역할과 채널 구조의 백업 및 복원.
- 역할, 채널, 이모지, 웹훅의 예약 자동 백업과 부족한 것만 추가하는 복원 명령어.

## 프로젝트 상태

GuardBot은 아직 새로운 프로젝트이며 대규모 서버에서 사용된 적이 없습니다. 자동 테스트(`python -m unittest`)는 저장소, 개인정보 감지, 레벨 계산, 명령어 등록, 권한 확인, 문서 링크를 다룹니다. 락다운, 백업 복원, 인증, Anti-Nuke, 굴라그처럼 실제 Discord 서버가 필요한 기능은 테스트에 포함되지 않습니다. 의존하기 전에 먼저 테스트 서버에서 시험해 보세요. 문서 번역은 원어민의 검토를 받지 않았습니다. 수정 제안을 환영합니다.

## 요구 사항

- Python 3.11 이상
- 봇 토큰이 있는 Discord 애플리케이션
- 항상 켜져 있는 컴퓨터 또는 VPS

## 빠른 시작

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

자세한 단계별 안내는 다음 문서에 있습니다: [GUIDE.md](GUIDE.md).

## 봇 권한

가장 간단한 방법은 관리자 권한을 주는 것입니다. 최소 권한을 원한다면 다음 권한을 부여하고, Developer Portal에서 Server Members Intent와 Message Content Intent를 켜세요:

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

## Discord에서의 첫 단계

무난한 초기 설정입니다. 서버에서 다음 명령어를 실행하고 채널과 역할을 내 것으로 바꾸세요:

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

## 명령어

대부분의 명령어는 슬래시 명령어이며, 관리 명령어는 접두사로도 사용할 수 있습니다. 전체 목록은 명령어 참조에 있습니다: [COMMANDS.md](../COMMANDS.md).

### 관리

경고, 뮤트, 추방, 차단은 슬래시 명령어와 접두사로 모두 사용할 수 있습니다(예: `!warn @User spam`). 모든 조치는 번호가 붙은 기록을 만듭니다.

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

### 굴라그(감금)

계정이 탈취된 멤버는 보안 안내가 있는 단 하나의 채널로 이동합니다. 풀려날 때 예전 역할이 복원됩니다.

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
```

### 자동 관리

규칙에 맞는 메시지를 삭제하거나 처벌합니다. 조치는 규칙마다 log, delete, warn, timeout, jail 중에서 고릅니다.

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

### 레이드 방지와 락다운

짧은 시간에 몰리는 입장을 감지하고 서버를 잠글 수 있습니다. channels 모드는 모든 채널을 수정하고, role 모드는 즉시 적용됩니다.

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

### Anti-Nuke

감사 로그를 감시하고 누군가 서버를 파괴하면 대응합니다. 서버 소유자에게 다이렉트 메시지가 갑니다.

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

### 인증

새 멤버는 버튼을 누르거나 캡차를 풀기 전까지 인증 채널만 볼 수 있습니다.

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### 로그

카테고리마다 채널을 고르거나, 모든 것을 하나의 메인 채널에 기록합니다.

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### 환영, 작별, 부스터

메시지, 자동 역할, 서버 부스터 보상.

```
/welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/welcome autorole role:@Member                     # toggle, given to every new member
/welcome botrole role:@Bots                        # toggle, given to every new bot
/welcome test

/booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/booster role role:@Booster                        # toggle
```

### 티켓

멤버가 버튼으로 비공개 채널을 엽니다. 티켓을 닫으면 대화 기록이 전송됩니다.

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

### 투표와 경품 추첨

투표와 참여는 버튼으로 합니다. 기간은 30m, 2h, 1d 같은 값을 받습니다.

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### 건의와 스타보드

멤버가 올린 건의를 운영진이 승인하거나 거부할 수 있고, 인기 있는 메시지는 강조됩니다.

```
/suggestionsetup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
```

### XP와 레벨

채팅과 음성 XP, 레벨 역할, 역할별 부스트, 랭크 카드.

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

### 반응 역할과 알림

원하는 이모지 반응으로 역할을 주고, 멤버가 알림 주제를 직접 고르게 합니다.

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

### 생일

멤버가 일과 월을 저장하면 당일에 봇이 역할을 주고 메시지를 보냅니다.

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### 임시 음성 채널

허브 채널에 들어가면 방이 만들어지고, 비면 사라집니다.

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### 백업과 복원

백업에는 역할, 채널, 이모지, 웹훅, 멤버 역할이 들어 있습니다. 복원은 부족한 것만 추가합니다.

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### 데이터와 개인정보

멤버는 자신의 데이터를 내보내고 삭제할 수 있습니다. 관리자는 보관 기간을 정합니다.

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### 운영

모듈과 명령어를 켜고 끄고, 접두사를 바꾸고, 별칭을 정하고, 명령어를 역할로 제한합니다.

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

## 메시지 자리표시자

설정한 텍스트 안에서 다음 자리표시자가 치환됩니다:

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthdaysetup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## 설정

전역 옵션은 settings.json에서 설정합니다. 나머지는 /module, /command, /perms, /alias, /config 같은 명령어로 서버별로 설정합니다.

명령어 이름을 바꾸려면 command_names에 추가하고 봇을 다시 시작하세요:

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

모든 설정은 /config로 읽고 바꿀 수 있습니다. 가장 자주 쓰는 경로는 다음과 같습니다:

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

## 데이터와 저장 위치

봇이 저장하는 모든 것은 내 컴퓨터에 있습니다:

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

## 저장소 구조

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

## 로드맵

- 내 컴퓨터에서 실행되는 로컬 웹 대시보드. 호스팅 서비스 없이 설정을 바꿀 수 있습니다.
- 봇 메시지 번역.
- 설정 내보내기 및 가져오기.

## 개인정보 및 보안

- 원격 측정도 외부 서비스도 없습니다. 봇은 Discord와만 통신합니다.
- 모든 데이터는 내 컴퓨터의 data 폴더에 저장됩니다. 설정, XP, 생일(일과 월만), 관리 기록입니다.
- 봇은 멤버가 보내는 다이렉트 메시지를 무시합니다.
- 토큰은 .env 파일에서 읽습니다. 절대 공유하거나 업로드하지 마세요.
- 멤버는 /mydata로 자신의 데이터를 내보내고 삭제할 수 있습니다. 관리자는 떠난 멤버의 데이터를 얼마나 보관할지 정할 수 있습니다.
- [PRIVACY.md](../PRIVACY.md)

## 지원

버그, 아이디어, 제안은 Discord @justyyin 으로 연락하거나 GitHub에 issue를 등록해 주세요.

## 라이선스

MIT 라이선스로 공개되어 있습니다. 참조: [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
