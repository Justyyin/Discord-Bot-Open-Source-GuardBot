# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | **日本語** | [한국어](../ko/README.md)

モデレーション、セキュリティ、コミュニティのための自己ホスト型 Discord ボット。オープンソースで無料、データは自分のコンピューターに残ります。

<!-- toc -->

- [プロジェクトについて](#プロジェクトについて)
- [機能](#機能)
  - [セキュリティ](#セキュリティ)
  - [モデレーション](#モデレーション)
  - [ログ](#ログ)
  - [コミュニティ](#コミュニティ)
  - [管理](#管理)
- [プロジェクトの状況](#プロジェクトの状況)
- [動作要件](#動作要件)
- [クイックスタート](#クイックスタート)
- [ボットの権限](#ボットの権限)
- [Discord での最初の手順](#discord-での最初の手順)
- [コマンド](#コマンド)
  - [モデレーション](#モデレーション-1)
  - [グラグ（ジェイル）](#グラグジェイル)
  - [自動モデレーション](#自動モデレーション)
  - [レイド対策とロックダウン](#レイド対策とロックダウン)
  - [Anti-Nuke](#anti-nuke)
  - [認証](#認証)
  - [ログ](#ログ-1)
  - [ようこそ・さようならとブースター](#ようこそさようならとブースター)
  - [チケット](#チケット)
  - [投票とプレゼント企画](#投票とプレゼント企画)
  - [提案とスターボード](#提案とスターボード)
  - [XP とレベル](#xp-とレベル)
  - [リアクションロールと通知](#リアクションロールと通知)
  - [誕生日](#誕生日)
  - [一時ボイスチャンネル](#一時ボイスチャンネル)
  - [バックアップと復元](#バックアップと復元)
  - [データとプライバシー](#データとプライバシー)
  - [管理](#管理-1)
- [メッセージのプレースホルダー](#メッセージのプレースホルダー)
- [設定](#設定)
- [データと保存場所](#データと保存場所)
- [リポジトリの構成](#リポジトリの構成)
- [ロードマップ](#ロードマップ)
- [プライバシーとセキュリティ](#プライバシーとセキュリティ)
- [サポート](#サポート)
- [ライセンス](#ライセンス)

<!-- tocstop -->

## プロジェクトについて

GuardBot は、多くのサーバーがホスト型ボットで有料利用している機能をまとめています。モデレーション、ログ、Anti-Raid（レイド対策）、Anti-Nuke（サーバー破壊対策）、チケット、レベルなどです。自分のコンピューターか小さな VPS で、自分で運用します。

ホスト型ボットは、サーバーのデータやメンバー ID、場合によってはメールアドレスを第三者に保存します。自分でホストすれば、それらのデータはコンピューターの外に出ません。GuardBot は、誰でもサブスクリプションなしで高機能なボットを運用できることを示すためのものです。

## 機能

### セキュリティ

- 自動モデレーション：単語フィルター、大文字フィルター、メンションスパム、招待リンク、フィッシングドメイン、個人情報、ドキシング、脅迫。すべてのリストを編集できます。
- 短時間の大量参加を検知するレイド対策と、全チャンネルのサーバーロックダウン。
- Anti-Nuke：大量削除や大量 BAN の上限、自動対応、サーバーオーナーへのダイレクトメッセージ。
- グラグチャンネル：詐欺リンクや画像を投稿したメンバーは、アカウント保護の手順が書かれた専用チャンネルだけに移されます。モデレーターは /jail と /unjail も使えます。
- ボタンまたはキャプチャによる認証と、期限内に認証しないメンバーの自動削除。
- Anti-Nuke は、権限の付与、新しい Webhook、追加されたボット、サーバー名の変更も監視します。

### モデレーション

- 警告、ミュート、キック、BAN、ジェイルと、メンション・ユーザー ID・種類で絞り込める履歴。
- 自動エスカレーション。たとえば警告 3 回でタイムアウトにできます。
- 各モデレーションコマンドを使えるロールやユーザーを設定できます。

### ログ

- 送信、編集、削除されたメッセージ（画像、GIF、URL を含む）を、別々のログチャンネルに記録します。
- ロール、ニックネーム、BAN、ボイス、チャンネル、サーバーロールの変更。

### コミュニティ

- ようこそ・さようならメッセージ、自動ロール、ブースター特典。
- チケット、投票、プレゼント企画、提案。
- 好きな絵文字で使えるリアクションロールと、メンバーが自分で切り替えられる通知トピック。
- チャットとボイスの XP とレベル 1〜100、レベルロール、誕生日。
- スターボードと一時ボイスチャンネル。
- 期限付きジェイル、複数選択の投票、画像のランクカード、ロールごとの XP ブースト。

### 管理

- すべてのモジュールと各コマンドをサーバーごとにオン・オフできます。
- 独自のプレフィックス、コマンドのエイリアス、コマンド名の変更。
- ロールとチャンネル構成のバックアップと復元。
- ロール、チャンネル、絵文字、Webhook のスケジュール自動バックアップと、足りないものだけを追加する復元コマンド。

## プロジェクトの状況

GuardBot はまだ新しく、大規模なサーバーでは使われていません。自動テスト（`python -m unittest`）は、ストレージ、個人情報の検出、レベル計算、コマンド登録、権限チェック、ドキュメントのリンクを対象としています。ロックダウン、バックアップの復元、認証、Anti-Nuke、グラグなど、実際の Discord サーバーが必要な機能はテストの対象外です。頼りにする前に、まずテスト用サーバーで試してください。ドキュメントの翻訳はネイティブスピーカーによる確認を受けていません。修正の提案を歓迎します。

## 動作要件

- Python 3.11 以降
- ボットトークンを持つ Discord アプリケーション
- 常時オンラインのコンピューターまたは VPS

## クイックスタート

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

詳しい手順は次のガイドにあります： [GUIDE.md](GUIDE.md).

## ボットの権限

最も簡単なのは管理者権限を付与することです。最小限の権限にしたい場合は、次の権限を付与し、Developer Portal で Server Members Intent と Message Content Intent をオンにしてください：

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

## Discord での最初の手順

無理のない初期設定です。サーバーで次のコマンドを実行し、チャンネルとロールを自分のものに置き換えてください：

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

## コマンド

ほとんどのコマンドはスラッシュコマンドで、モデレーションコマンドはプレフィックスでも使えます。完全な一覧はコマンドリファレンスにあります： [COMMANDS.md](../COMMANDS.md).

### モデレーション

警告、ミュート、キック、BAN はスラッシュコマンドでもプレフィックスでも使えます（例：`!warn @User spam`）。すべての操作で番号付きのケースが作られます。

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

### グラグ（ジェイル）

アカウントが乗っ取られたメンバーは、セキュリティ手順が書かれた専用チャンネルに移されます。解放時には元のロールが戻ります。

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
```

### 自動モデレーション

ルールに一致するメッセージを削除または処罰します。動作はルールごとに log、delete、warn、timeout、jail から選びます。

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

### レイド対策とロックダウン

短時間の大量参加を検知し、サーバーをロックできます。channels モードは全チャンネルを変更し、role モードは即座に効きます。

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

監査ログを監視し、誰かがサーバーを破壊したときに対応します。サーバーオーナーにダイレクトメッセージが届きます。

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

### 認証

新しいメンバーは、ボタンを押すかキャプチャを解くまで認証チャンネルしか見えません。

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### ログ

カテゴリごとにチャンネルを選ぶか、すべてをまとめて 1 つのメインチャンネルに記録します。

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### ようこそ・さようならとブースター

メッセージ、自動ロール、サーバーブースター向けの特典。

```
/welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/welcome autorole role:@Member                     # toggle, given to every new member
/welcome botrole role:@Bots                        # toggle, given to every new bot
/welcome test

/booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/booster role role:@Booster                        # toggle
```

### チケット

メンバーはボタンで非公開チャンネルを開きます。閉じるとトランスクリプトが送信されます。

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

### 投票とプレゼント企画

投票や参加はボタンで行います。期間は 30m、2h、1d のように指定できます。

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### 提案とスターボード

メンバーが投稿した提案をスタッフが承認または却下でき、人気のメッセージは強調表示されます。

```
/suggestionsetup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
```

### XP とレベル

チャットとボイスの XP、レベルロール、ロール別ブースト、ランクカード。

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

### リアクションロールと通知

好きな絵文字のリアクションでロールを付与し、メンバーが通知トピックを自分で選べます。

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

### 誕生日

メンバーが日と月を登録すると、当日にボットがロールを付与してメッセージを送ります。

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### 一時ボイスチャンネル

ハブチャンネルに入るとルームが作られ、空になると消えます。

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### バックアップと復元

バックアップにはロール、チャンネル、絵文字、Webhook、メンバーのロールが含まれます。復元は足りないものだけを追加します。

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### データとプライバシー

メンバーは自分のデータをエクスポートおよび削除できます。管理者は保存期間を管理します。

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### 管理

モジュールとコマンドのオン・オフ、プレフィックスの変更、エイリアスの設定、ロールによるコマンド制限。

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

## メッセージのプレースホルダー

設定したテキストの中で、次のプレースホルダーが置き換えられます：

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthdaysetup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## 設定

全体の設定は settings.json で行います。それ以外はサーバーごとに /module、/command、/perms、/alias、/config などのコマンドで設定します。

コマンド名を変えるには、command_names に追加してボットを再起動します。

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

すべての設定は /config で読み取りと変更ができます。よく使うパスは次のとおりです：

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

## データと保存場所

ボットが保存するものはすべてあなたのコンピューター上にあります：

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

## リポジトリの構成

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

## ロードマップ

- 自分のコンピューターで動くローカルウェブダッシュボード。ホスト型サービスなしで設定を変更できます。
- ボットメッセージの翻訳。
- 設定のエクスポートとインポート。

## プライバシーとセキュリティ

- テレメトリーも外部サービスもありません。ボットは Discord とだけ通信します。
- すべてのデータは、お使いのコンピューターの data フォルダーに保存されます。設定、XP、誕生日（日と月のみ）、モデレーション記録です。
- ボットはメンバーからのダイレクトメッセージを無視します。
- トークンは .env ファイルから読み込まれます。共有したり公開したりしないでください。
- メンバーは /mydata で自分のデータをエクスポートおよび削除できます。管理者は、退出したメンバーのデータを保持する期間を設定できます。
- [PRIVACY.md](../PRIVACY.md)

## サポート

バグ、アイデア、提案は Discord の @justyyin に連絡するか、GitHub で issue を作成してください。

## ライセンス

MIT ライセンスで公開されています。参照： [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
