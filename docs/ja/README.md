# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | **日本語** | [한국어](../ko/README.md)

モデレーション、セキュリティ、コミュニティのための自己ホスト型 Discord ボット。オープンソースで無料、データは自分のコンピューターに残ります。

> ベータ版：GuardBot とそのダッシュボードはベータ段階です。十分にテストされておらず、特に大規模なサーバーや Discord のあらゆる状況では確認していません。不具合が起こりうるため、data フォルダーのバックアップを取り、問題を報告してください。自己責任でご利用ください。

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
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [起動スクリプトと自動起動](#起動スクリプトと自動起動)
  - [更新](#更新)
- [ボットの権限](#ボットの権限)
- [Discord での最初の手順](#discord-での最初の手順)
  - [構成、メンバー、チーム](#構成メンバーチーム)
- [ダッシュボード](#ダッシュボード)
  - [ダッシュボードの設定](#ダッシュボードの設定)
  - [コマンド、スキル、AI、ボットのプロフィール](#コマンドスキルaiボットのプロフィール)
  - [セキュリティ](#セキュリティ-1)
  - [VPS でのダッシュボード](#vps-でのダッシュボード)
- [コマンド](#コマンド)
  - [コマンドグループ](#コマンドグループ)
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
  - [モデレーター用ツール](#モデレーター用ツール)
  - [情報](#情報)
  - [お知らせ、タグ、リマインダー](#お知らせタグリマインダー)
  - [モデメールとBAN異議申し立て](#モデメールとban異議申し立て)
  - [カウントチャンネル、固定メッセージ、統計](#カウントチャンネル固定メッセージ統計)
  - [既存機能の追加オプション](#既存機能の追加オプション)
  - [その他の AutoMod ツール](#その他の-automod-ツール)
  - [モデレーターの上限と権限監査](#モデレーターの上限と権限監査)
  - [通報と招待の追跡](#通報と招待の追跡)
  - [診断とデバッグ](#診断とデバッグ)
  - [音楽](#音楽)
  - [セットアップとヘルスチェック](#セットアップとヘルスチェック)
  - [経済](#経済)
  - [ロールメニュー、予約メッセージ、フィード](#ロールメニュー予約メッセージフィード)
  - [アクティビティ、一括操作、ケース検索](#アクティビティ一括操作ケース検索)
  - [詐欺対策・暗号資産対策](#詐欺対策暗号資産対策)
  - [仮参加期間、群れの検出、タイムライン、学習](#仮参加期間群れの検出タイムライン学習)
  - [パネル](#パネル)
  - [スキルとAI](#スキルとai)
  - [メッセージビルダーと更新](#メッセージビルダーと更新)
  - [運用](#運用)
  - [管理](#管理-1)
- [メッセージのプレースホルダー](#メッセージのプレースホルダー)
- [設定](#設定)
- [データと保存場所](#データと保存場所)
- [リポジトリの構成](#リポジトリの構成)
- [翻訳](#翻訳)
- [ロードマップ](#ロードマップ)
- [プライバシーとセキュリティ](#プライバシーとセキュリティ)
- [サポート](#サポート)
- [クレジット](#クレジット)
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
- グラグチャンネル：詐欺リンクや画像を投稿したメンバーは、アカウント保護の手順が書かれた専用チャンネルだけに移されます。モデレーターは /moderation jail と /moderation unjail も使えます。
- ボタンまたはキャプチャによる認証と、期限内に認証しないメンバーの自動削除。
- Anti-Nuke は、権限の付与、新しい Webhook、追加されたボット、サーバー名の変更も監視します。
- 詐欺対策：偽のプレゼント企画や暗号資産詐欺を、テキストでも画像でも数ミリ秒で削除します。どんな綴りの MrBeast 詐欺にも対応します。

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
- ショップ付きの経済、ボタンまたはドロップダウンのロールメニュー、予約メッセージ、YouTube・Twitch・RSS フィード、アクティビティ統計、ガイド付きの /admin setup。メンバー向けメッセージは12言語に対応します。

### 管理

- すべてのモジュールと各コマンドをサーバーごとにオン・オフできます。
- 独自のプレフィックス、コマンドのエイリアス、コマンド名の変更。
- ロールとチャンネル構成のバックアップと復元。
- ロール、チャンネル、絵文字、Webhook のスケジュール自動バックアップと、足りないものだけを追加する復元コマンド。
- ダッシュボード：Discord でログインしたあと、ブラウザーで各サーバーの設定を変更できます。対象はサーバーを管理するメンバーのみで、ボットが接続している間だけ使えます。
- スキル：安全なブロックで作る独自のコマンド、ゲーム、自動化。自分のキー（Anthropic、OpenAI、Kimi）でAIに書かせることもできます。ダッシュボードはすべてのコマンドを一覧表示し、スキル、AI設定、ボットのプロフィールを編集できます。

## プロジェクトの状況

GuardBot はまだ新しく、大規模なサーバーでは使われていません。自動テスト（`python -m unittest`）は、ストレージ、個人情報の検出、レベル計算、コマンド登録、権限チェック、ドキュメントのリンクを対象としています。ロックダウン、バックアップの復元、認証、Anti-Nuke、グラグなど、実際の Discord サーバーが必要な機能はテストの対象外です。頼りにする前に、まずテスト用サーバーで試してください。ドキュメントの翻訳はネイティブスピーカーによる確認を受けていません。修正の提案を歓迎します。

## 動作要件

- Python 3.11 以降
- ボットトークンを持つ Discord アプリケーション
- 常時オンラインのコンピューターまたは VPS
- ffmpeg（音楽モジュールのみ）
- tesseract-ocr（任意、画像内の文字を読み取る場合のみ）

## クイックスタート

お使いのシステムを選んでください。どの方法でも Python 3.11 以上とボットのトークンが必要です。詳しい手順は [GUIDE.md](GUIDE.md) にあります。

### Linux

```bash
sudo apt install -y python3 python3-venv python3-pip git ffmpeg tesseract-ocr
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
```

### macOS

```bash
brew install python@3.12 git ffmpeg tesseract
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
open -e .env
python main.py
```

### Windows

```powershell
winget install Python.Python.3.12 Git.Git Gyan.FFmpeg UB-Mannheim.TesseractOCR
git clone <REPOSITORY_URL>
cd guardbot
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
python main.py
```

### 起動スクリプトと自動起動

起動スクリプトは仮想環境を作成し、パッケージをインストールして、ボットを起動します。初回は .env ファイルを作成して停止するので、トークンを入力してください。その後、もう一度実行します。

```bash
./start.sh
```

```bat
start.bat
```

コンピューターの再起動後もボットを動かし続けるには、サービスを使います。Linux（systemd）と macOS（launchd）：

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

Windows では、タスクスケジューラでログオン時に start.bat を実行するタスクを作るか、NSSM などのサービスラッパーを使います。Docker については [GUIDE.md](GUIDE.md) を参照してください。

### 更新

ボットを止めて、次のコマンドを実行し、再び起動します。data フォルダーのデータには手を加えず、データ形式を変更する前にボットがデータベースをバックアップします。

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

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
/server log set category:main channel:#logs
/access jailsetup setup
/automod toggle rule:phishing enabled:True action:jail
/automod toggle rule:words enabled:True
/automod add name:words value:example
/security raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3
/security antinuke setup enabled:True action:strip
/access verify setup channel:#verify mode:captcha timeout_minutes:30
/community welcome set channel:#welcome message:Welcome {user} to {server}!
/server backup schedule enabled:True interval_hours:24 keep:7
/xp config enabled:True
/admin module list
```

### 構成、メンバー、チーム

バージョン1.5では、サーバーを組み立てて整理し続けるためのコマンド、戻ってきたメンバーの復元、モデレーションチームの運営が加わりました。各機能にはモジュールのスイッチ(`/admin module`)、専用の設定、ダッシュボード上の場所があります。

```
/structure channel create name:news kind:text category:Info private:False
/structure channel clone channel:#news name:news-2
/structure channel rename channel:#news name:announcements
/structure channel move channel:#news category:Info position:1
/structure channel sort category:Info
/structure channel copyperms source:#news target:#rules whole_category:False
/structure category create name:Events private:False
/structure category clone category:Events name:Events 2
/structure category sort
/structure category sync category:Events
/structure archive setup action:report days:60 report_channel:#staff interval_hours:24
/structure archive ignore channel:#news
/structure archive scan action:report
/structure temprole give member:@User role:@Event duration:7d reason:Contest
/structure temprole list
/structure roletemplate save name:mod role:@Moderator
/structure roletemplate apply name:mod role_name:Trial Mod
/structure rules setup channel:#rules role:@Member remind:True remind_hours:24
/structure rules add text:Be kind to each other.
/structure rules post new_version:True
/structure rules status

/members stickyroles setup roles:True days:30 punishments:True dangerous:False
/members stickyroles status
/members stickyroles forget user:@User
/members nickname setup dehoist:True usernames:True rename_to:Renamed notify:True
/members nickname word word:badword
/members nickname check name:!!hoisted
/members nickname scan
/members watch setup channel:#staff ping_role:@Moderator repeat:False
/members watch add user:@User reason:Suspicious
/members watch list
/members reason add name:spam action:mute text:Spam duration:1h
/members reason use name:spam user:@User

/security approval setup channel:#staff role:@Moderator ban:True bulk:True minutes:30 owner_bypass:True
/security approval list
/security approval cancel request_id:3
/moderation case undo case_id:12 reason:Mistake follow:True batch:False
/moderation escalation expiry days:90

/admin history list
/admin history show number:5
/admin history rollback number:5 section:welcome
/admin history keep count:200
/admin history copy source:123456789012345678 sections:welcome,tickets dry_run:True
/admin exceptions add rule:invites channel:#media role:@Artist
/admin exceptions list
/admin dashaccess add role:@Helper level:viewer
/admin dashaccess list

/team teamstats overview days:30
/team teamstats member user:@User
/team teamstats inactive days:14
/team weekly setup channel:#staff day:Monday hour:9
/team weekly now days:7
/team duty away duration:3d reason:Holiday
/team duty back
/team duty route feature:tickets enabled:True
/team duty roster role:@Moderator
/team apply setup channel:#applications staff_role:@Moderator accept_role:@Trial votes:3 open:True cooldown_days:30
/team apply question action:add text:Why do you want to join?
/team apply start
/team apply list
/team apply decide number:4 decision:accept
```

- `/structure` でチャンネルとカテゴリの作成、複製、名前変更、並べ替え、別チャンネルの権限のコピーができます。非アクティブなチャンネルは報告されるか、アーカイブ用カテゴリに移されます(`/structure archive`)。ロールは期限付きで付与でき、テンプレートとして保存できます。テンプレートは、適用する人が持たない権限を付与しません。
- `/structure rules` は同意ボタンとバージョン番号付きでルールを投稿します。`post new_version:True` の後、新しい版に同意していないメンバーにはダイレクトメッセージで一度だけリマインドが届きます。
- `/members stickyroles` はメンバーが戻ったときにロールを返し、タイムアウトやミュートを復元します。`/members nickname` はリストの先頭に来るための文字を取り除き、ニックネームとユーザー名の禁止語を確認し、違反者の名前を変更します。監視リストは静かに動作し、リストのユーザーが最初に発言したときにチームへ通知されます。
- 4つの目による承認(`/security approval`)では、BAN、キック、タイムアウト、一括操作は2人目のモデレーターが同意して初めて実行されます。`/moderation case undo` はケースを取り消し、それが引き起こした操作(例えばミュートとその後のBAN)も取り消します。警告は一定日数で失効させられます(`/moderation escalation expiry`)。
- `/admin history` は誰がいつどの設定を変えたかを表示し、セクションを元に戻します。人物名は、サーバー上の直近のコマンドとダッシュボードの変更からの推測です。`/admin history copy` はボットで管理できる別のサーバーへセクションをコピーし、最初は試行のみです。`/admin exceptions` はチャンネルとロールを AutoMod のルールとアンチスキャムの対象外にします。`/admin dashaccess` はロールに閲覧のみまたはモデレーターのダッシュボード権限を与えます。
- `/team` は各モデレーターの作業(ケース、チケット、報告、応答時間、非アクティブなメンバー)を表示し、週次レポート(曜日と時刻はUTC)を投稿し、`/team duty away` で不在を届け出るとチケットやメンションが他の人に回り、フォームとチーム投票でスタッフ応募を運営します。
- Discord はグループ内のコマンドを特定のメンバーから隠せません。ボットは引き続きすべての呼び出しを確認します。チーム統計の数字は更新した日から数えられ、それ以前の操作は含まれません。

## ダッシュボード

ダッシュボードはボットの中で動くウェブページです。Discord でログインすると、コマンドの代わりにスイッチ、メニュー、入力欄でサーバーの設定を変更できます。対象はモジュール、チャンネル、ロール、しきい値、テキスト、プレフィックス、言語です。直近のモデレーションケースの表示や、設定のエクスポートとインポートもできます。自分のコンピューターでも VPS でも同じように動作し、オンにするまでは無効です。

### ダッシュボードの設定

1. Developer Portal でアプリケーションを開き、OAuth2 に進んで、Client Secret を .env ファイルにコピーします。
2. 同じページでリダイレクトアドレス http://localhost:8080/callback を追加します。
3. settings.json でダッシュボードをオンにします。
4. ボットを再起動し、ブラウザで http://localhost:8080 を開いて Discord でログインします。

```
DISCORD_TOKEN=your-bot-token
DISCORD_CLIENT_SECRET=your-oauth2-client-secret
```

```json
{
  "dashboard": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 8080,
    "public_url": "http://localhost:8080"
  }
}
```

### コマンド、スキル、AI、ボットのプロフィール

ダッシュボードにはさらに5つのページがあります。Panels（「パネル」の項を参照）と、次の4つです。「コマンド」は、すべてのスラッシュコマンド、プレフィックスコマンド、コンテキストメニューを、モジュール、必要な権限、オンかどうかとともに一覧表示します。管理者はオン・オフの切り替え、ロールの許可や拒否、プレフィックスコマンドの短い名前の設定ができます。プレフィックスも同じページで変更します。「スキル」はすべてのスキルを表示し、コマンドと同じ検査のもとでJSONとして編集します。「AI」はモデルと制限を設定し、キーを保存します（書き込み専用で、ページに返されることはありません）。「ボットのプロフィール」は、このサーバーでのボットの名前、画像、バナー、紹介文を変更します。ボットのアプリケーションの所有者、またはsettings.jsonの `owner_ids` に載っているIDは、すべての場所でも変更できます。Discordは名前と画像の変更頻度を制限しています。すべての変更は監査ログに記録されます。

各モジュールはプラグインとして表示されます。Plugins ページではカテゴリごとにカードで並び、各プラグインには「有効」スイッチ、開閉できるボックスに入った設定、スイッチとロール編集付きのコマンドを備えた専用ページがあります。左のバーはカテゴリごとにプラグインを並べ、点でオンかどうかを示します。ダッシュボードはダークデザインです。

ダッシュボードはボットの 12 言語すべてで表示できます。言語は右上またはログインページで選びます。選択はブラウザに保存され、サーバーの言語は変わりません。ダッシュボードの文章は機械翻訳です。

各プラグインページでは、そのプラグインができることを説明し、すべての機能を個別のスイッチと短い説明付きで一覧にし、その他の設定は下のボックスにまとめます。「プラグイン」ページと概要では、各プラグインを直接オン・オフできます。「設定」の「ダッシュボードの外観」ボックスでは、アクセントカラー、背景、ボックス、文字の色を変え、壁紙 (好みで暗くしたりぼかしたり) を設定し、サイドバーに独自のメニューとタブを追加できます。タブには選んだプラグインをまとめる、ページを開く、https のアドレスにリンクする、メモを表示する、のいずれかを設定できます。外観はサーバーごとに保存され、そのダッシュボードを開く全員に表示されます。フッターには著作権表示と Discord・GitHub へのリンクがあります。公式ロゴを表示するには、Discord と GitHub のブランドページから入手した discord.svg と github.svg を guardbot/web/brand/ に置いてください。

### セキュリティ

- ログインは Discord のみです（OAuth2、スコープ identify）。アクセストークンはすぐに無効化され、保存されません。
- アクセスできるのは、サーバーの所有者と「管理者」または「サーバー管理」権限を持つメンバーだけで、そのサーバーに限ります。権限はリクエストのたびに再確認されます。
- 開けるのは、ボットが現在接続しているサーバーだけです。ボットがオフライン、サーバーにいない、または起動中の場合、ダッシュボードはすべて拒否します。ダッシュボードはボットの中で動き、独自のデータベースやサービスは持ちません。
- 初期設定では 127.0.0.1 だけで待ち受けるため、ネットワーク上の他の人は接続できません。公開アドレスは HTTPS の場合にのみ受け付けられ、そうでなければダッシュボードは起動しません。
- セッションは、SameSite 付きの HttpOnly Cookie に入れたランダムなトークンを使い、HTTPS では __Host- プレフィックスも付きます。8 時間で終了し、メモリ上にだけ存在するため、再起動すると全員がログアウトされます。
- 変更のたびに CSRF トークンと一致する Origin が必要です。Host ヘッダーは DNS リバインディング対策として検査されます。ページは外部スクリプトを読み込まず、厳格な Content Security Policy がインラインコードを遮断し、リクエストには頻度制限があり、本文は 256 KB に制限されます。
- すべての値は設定の型に照らして検査され、Discord の ID はそのサーバーに存在する必要があります。カウンター、チケット、保存済みの項目などの内部状態は編集できません。変更はすべてサーバーのセキュリティログチャンネルに記録されます。
- メッセージの内容は表示されません。モデレーションケースは閲覧専用です。

### VPS でのダッシュボード

host は 127.0.0.1 のままにして、2 つの方法から選びます。1 つ目は SSH トンネルです。何も公開せず、トンネルが動いている間、自分のコンピューターで http://localhost:8080 を開きます。

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

2 つ目は Caddy のようなリバースプロキシを使った HTTPS です。証明書は自動で取得されます（deploy/Caddyfile.example を参照）。その場合は public_url を https アドレスにし、Developer Portal に https://あなたのアドレス/callback をリダイレクトとして追加し、trust_proxy を true にします：

```
dashboard.example.com {
	reverse_proxy 127.0.0.1:8080
}
```

```json
{
  "dashboard": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 8080,
    "public_url": "https://dashboard.example.com",
    "trust_proxy": true
  }
}
```

エディターには、スイッチ、数値、テキスト、チャンネル、ロール、単純なリストにあたるすべての設定が表示されます。ショップの商品、ロールメニュー、フィード、タグ、チケットなど、コマンドで作るものは引き続きコマンドで行います。ページは英語とドイツ語で表示され、ブラウザーの言語に従います。Docker ではポートを 127.0.0.1 にだけ公開し（127.0.0.1:8080:8080）、コンテナ内で host を 0.0.0.0、allow_insecure_http を true にします。

## コマンド

ほとんどのコマンドはスラッシュコマンドで、モデレーションコマンドはプレフィックスでも使えます。完全な一覧はコマンドリファレンスにあります： [COMMANDS.md](../COMMANDS.md).

<!-- groups -->
### コマンドグループ

スラッシュコマンドの枠を節約するため(Discord ではボット 1 つにつき最上位コマンドは 100 個まで)、関連するコマンドをグループにまとめています。先にグループ、次にコマンドを入力します。例: `/moderation ban`。プレフィックス付きのテキストコマンド(例: `!ban`)は変わりません。権限、エイリアス、モジュールのスイッチは引き続き単純なコマンド名を使います。

| グループ | 含まれるもの |
| --- | --- |
| `/moderation` | `warn`, `unwarn`, `warnings`, `clearwarns`, `note`, `mute`, `unmute`, `kick`, `ban`, `unban`, `tempban`, `jail`, `unjail`, `jailed`, `role`, `case`, `cases`, `bulk`, `escalation`, `purge`, `slowmode` |
| `/security` | `antinuke`, `antiscam`, `raid`, `block`, `unblock`, `blocklist`, `approval` |
| `/access` | `verify`, `probation`, `lockdown`, `lockdownconfig`, `unlock`, `lockchannel`, `unlockchannel`, `jailsetup` |
| `/server` | `log`, `backup`, `privacy`, `invites`, `stats`, `serverinfo`, `roleinfo`, `health`, `diagnose`, `debug` |
| `/admin` | `settings`, `config`, `module`, `command`, `perms`, `alias`, `prefix`, `language`, `setup`, `history`, `exceptions`, `dashaccess` |
| `/info` | `about`, `avatar`, `botinfo`, `ping`, `userinfo`, `mydata`, `leaderboard`, `rank`, `find` |
| `/community` | `welcome`, `booster`, `afk`, `remind`, `activity`, `tempvoice`, `voice` |
| `/engage` | `economy`, `giveaway`, `poll`, `counting`, `starboard` |
| `/support` | `ticket`, `suggest`, `tag`, `autoresponder` |
| `/members` | `stickyroles`, `nickname`, `watch`, `reason` |
| `/structure` | `channel`, `category`, `archive`, `temprole`, `roletemplate`, `rules` |
| `/team` | `teamstats`, `weekly`, `duty`, `apply`, `modwatch`, `permaudit` |
| `/post` | `say`, `embed`, `message`, `sticky`, `schedule`, `feed`, `reactionrole`, `rolemenu` |
| | `/help`, `/play`, `/automod`, `/music`, `/xp`, `/modmail`, `/appeal`, `/report`, `/suggestion`, `/birthday`, `/notify` |

### モデレーション

警告、ミュート、キック、BAN はスラッシュコマンドでもプレフィックスでも使えます（例：`!warn @User spam`）。すべての操作で番号付きのケースが作られます。

```
/moderation warn member:@User reason:Spam                    # also: !warn @User Spam
/moderation unwarn case_id:12                                 # remove one warning
/moderation clearwarns user:@User                             # remove all active warnings
/moderation mute member:@User duration:30m reason:Spam        # also: !mute @User 30m Spam
/moderation unmute member:@User
/moderation kick member:@User reason:Advertising
/moderation ban user:@User reason:Raid                        # user can also be an ID
/moderation unban user:123456789012345678

/moderation cases user:@User                                  # history, filter by mention or ID
/moderation cases kind:ban page:2                             # filter by type
/moderation cases search:john                                 # filter by part of a name
/moderation warnings user:@User
/moderation case view case_id:12

/moderation escalation list
/moderation escalation set warns:3 action:timeout minutes:60  # 3 warnings = 1 hour timeout
/moderation escalation set warns:5 action:kick
/moderation escalation set warns:7 action:ban                 # actions: timeout, kick, ban, jail
/moderation escalation remove warns:5
```

### グラグ（ジェイル）

アカウントが乗っ取られたメンバーは、セキュリティ手順が書かれた専用チャンネルに移されます。解放時には元のロールが戻ります。

```
/access jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/access jailsetup apply                                   # apply the channel permissions again
/access jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/access jailsetup preview
/access jailsetup reminder notice:True reminder:True minutes:10 requests:True word:unban

/moderation jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/moderation jail member:@User duration:2h                     # released automatically after 2 hours
/moderation unjail member:@User reason:Account secured
```

グラグに入った人は、コマンド、AutoMod、スキャム対策、再参加、または誰かが手動でロールを付けた場合のいずれでも、メンション付きで Account Security Required の通知を受け取ります。グラグに誰かいる間は、チャンネルの一番下に Account Recovery Reminder が置かれ、10分ごとに更新されます。グラグにいるメンバーがグラグのチャンネルでプレフィックスと解放ワード（例：`!unban`）を書くと、スタッフ向けに Release と Keep のボタン付きの解放リクエストが作られます。ボットが自分で誰かを解放することはありません。`/access jailsetup reminder` で各部分のオン・オフ、間隔、ワードを設定できます。

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
/security raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3 lockdown:True
# 5 joins within 10 seconds count as a raid, accounts younger than 3 days are punished,
# actions: alert, timeout, kick

/access lockdown mode:role reason:Raid                    # instant, edits only the @everyone role
/access lockdown mode:channels reason:Raid                # thorough, edits every channel
/access unlock

/access lockdownconfig mode mode:role                     # default mode
/access lockdownconfig lockrole role:@Member              # extra role locked in role mode
/access lockdownconfig bypassrole role:@Moderator         # can still write in channels mode
/access lockdownconfig exempt channel:#announcements
```

### Anti-Nuke

監査ログを監視し、誰かがサーバーを破壊したときに対応します。サーバーオーナーにダイレクトメッセージが届きます。

```
/security antinuke setup enabled:True action:strip notify_owner:True   # actions: alert, strip, kick, ban
/security antinuke limit kind:channel_delete count:3 seconds:10
# kinds: channel_delete, role_delete, channel_create, ban, kick,
#        role_perm, role_grant, webhook_create, bot_add, guild_update
/security antinuke whitelist user:@TrustedAdmin             # toggle, never checked
/security antinuke staffrole role:@Moderator                # toggle, shown in alerts
/security antinuke servername name:MyServer                 # extra name for the nuke talk detection
/security antinuke newbots kick:True                        # kick bots added by untrusted users
/security antinuke restore member:@User                     # give back roles that were removed
/security antinuke status
```

### 認証

新しいメンバーは、ボタンを押すかキャプチャを解くまで認証チャンネルしか見えません。

```
/access verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/access verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/access verify panel channel:#verify                      # post the button again
/access verify apply                                      # apply the channel permissions again
/access verify member member:@User                        # verify someone manually
/access verify off
```

### ログ

カテゴリごとにチャンネルを選ぶか、すべてをまとめて 1 つのメインチャンネルに記録します。

```
/server log set category:main channel:#logs               # fallback for every category
/server log set category:messages channel:#log-messages
/server log set category:moderation channel:#log-moderation
/server log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/server log sent enabled:False                            # stop logging every sent message
/server log show
```

### ようこそ・さようならとブースター

メッセージ、自動ロール、サーバーブースター向けの特典。

```
/community welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/community welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/community welcome autorole role:@Member                     # toggle, given to every new member
/community welcome botrole role:@Bots                        # toggle, given to every new bot
/community welcome test

/community booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/community booster role role:@Booster                        # toggle
```

### チケット

メンバーはボタンで非公開チャンネルを開きます。閉じるとトランスクリプトが送信されます。

```
/support ticket setup category:Tickets support_role:@Support log_channel:#ticket-logs max_open:1
/support ticket addtype key:report label:Report description:Report a member
/support ticket removetype key:report
/support ticket panel channel:#support title:Support description:Press a button to open a ticket

# inside a ticket
/support ticket add member:@User
/support ticket remove member:@User
/support ticket close
```

### 投票とプレゼント企画

投票や参加はボタンで行います。期間は 30m、2h、1d のように指定できます。

```
/engage poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/engage poll end poll_id:3
/engage poll list

/engage giveaway start prize:Nitro duration:2d winners:2 role:@Member
/engage giveaway end giveaway_id:1
/engage giveaway reroll giveaway_id:1
/engage giveaway list
```

### 提案とスターボード

メンバーが投稿した提案をスタッフが承認または却下でき、人気のメッセージは強調表示されます。

```
/suggestion setup set channel:#suggestions review_role:@Staff
/support suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/engage starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/engage starboard ignore channel:#spam
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

/xp levelrole add level:10 role:@Active
/xp levelrole add level:50 role:@Veteran
/xp levelrole remove level:10
/xp levelrole list
/xp levelrole sync                                    # apply to everyone who already has XP

/xp give user:@User amount:500
/xp take user:@User amount:100
/xp setlevel user:@User level:20
/xp reset user:@User

/info rank                                              # also: !rank, shows a rank card image
/info rank user:@User
/info leaderboard
```

### リアクションロールと通知

好きな絵文字のリアクションでロールを付与し、メンバーが通知トピックを自分で選べます。

```
/post reactionrole panel channel:#roles title:Pick your roles description:React below
/post reactionrole add message:<message link> emoji:<any emoji> role:@Gamer
/post reactionrole add message:<message link> emoji:<any emoji> role:@Artist mode:unique
# mode unique: only one role of that message at a time
/post reactionrole remove message:<message link> emoji:<any emoji>
/post reactionrole list

/notify topic add key:events role:@Events description:Server events
/notify topic panel channel:#roles title:Notifications   # one button per topic
/notify topic remove key:events
/notify subscribe topic:events                     # members choose for themselves
/notify unsubscribe topic:events
/notify list
```

### 誕生日

メンバーが日と月を登録すると、当日にボットがロールを付与してメッセージを送ります。

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### 一時ボイスチャンネル

ハブチャンネルに入るとルームが作られ、空になると消えます。

```
/community tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### バックアップと復元

バックアップにはロール、チャンネル、絵文字、Webhook、メンバーのロールが含まれます。復元は足りないものだけを追加します。

```
/server backup create name:before-update
/server backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/server backup list
/server backup download name:before-update
/server backup restore name:before-update member_roles:True   # only adds what is missing
/server backup delete name:before-update
```

### データとプライバシー

メンバーは自分のデータをエクスポートおよび削除できます。管理者は保存期間を管理します。

```
/info mydata export                                     # members download their own data
/info mydata delete confirm:True                        # members delete their XP and birthday

/server privacy retention days:90                         # delete data of members who left after 90 days
/server privacy export user_id:123456789012345678
/server privacy delete user_id:123456789012345678 cases:True
```

### モデレーター用ツール

チャンネルの整理、ロール管理、非公開メモ。すべての操作はログに記録されます。

```
/moderation purge amount:50 user:@User kind:links           # kind: all, links, images, bots, attachments
/moderation slowmode seconds:10 channel:#general              # 0 turns it off
/access lockchannel channel:#general reason:Spam wave
/access unlockchannel channel:#general

/moderation role add member:@User role:@Member
/moderation role remove member:@User role:@Member

/moderation note user:@User text:Watch this member            # private, shown in /moderation cases
/moderation tempban user:@User duration:7d reason:Spam        # unbanned automatically
/moderation jailed                                            # who is in the gulag right now

/moderation case view case_id:12
/moderation case edit case_id:12 reason:Corrected reason
/moderation case delete case_id:12
```

### 情報

ユーザー、サーバー、ロール、ボットの情報を確認します。

```
/info userinfo user:@User
/server serverinfo
/server roleinfo role:@Moderator
/info avatar user:@User
/help command:ban                                  # explains one command
/info ping
/info botinfo
```

### お知らせ、タグ、リマインダー

ボットの名前で投稿し、独自コマンドを作り、メッセージに自動で返信し、リマインダーを設定します。

```
/post say channel:#news message:Maintenance tonight
/post embed channel:#news title:Update description:New rules color:#5865F2

/support tag create name:rules text:Be kind to each other
/support tag show name:rules
/support tag list
/support tag info name:rules
/support tag edit name:rules text:Be kind and read the pinned message
/support tag delete name:rules

/support autoresponder add trigger:server ip response:The IP is in #info mode:contains cooldown:30
/support autoresponder list
/support autoresponder remove id:1                         # mode: contains, word, exact, startswith

/community remind set duration:2h text:Stream starts
/community remind list
/community remind cancel id:1
/community afk reason:Lunch                                  # the bot tells others who mention you
```

### モデメールとBAN異議申し立て

メンバーはサーバー内の非公開チャンネルでスタッフに連絡します。ボットへのダイレクトメッセージは不要です。

```
/modmail setup set category:Mod-mail staff_role:@Moderator log_channel:#modmail-log anonymous:False
/modmail setup panel channel:#help text:Press the button to write to the staff
/modmail setup block member:@User                   # toggles
/modmail setup status

/modmail send text:I need help with my account     # inside a mod-mail channel
/modmail close reason:Solved

/appeal setup set main_server_id:123456789012345678 staff_channel:#appeals cooldown_days:7
/appeal setup set invite:https://discord.gg/example rejoin_invite:https://discord.gg/example
/appeal setup status
/appeal send text:I understand the rule now and ask for a second chance
```

### カウントチャンネル、固定メッセージ、統計

カウントゲーム、チャンネルの最下部に残るメッセージ、リアルタイムの数値を表示するチャンネル。

```
/engage counting setup channel:#counting reset_on_fail:True delete_wrong:True
/engage counting status
/engage counting set number:100
/engage counting off

/post sticky set channel:#rules text:Read the rules before you write
/post sticky list
/post sticky remove channel:#rules

/server stats create template:Members: {members} category:Statistics
/server stats add channel:#info template:Boosts: {boosts}
/server stats list
/server stats refresh
/server stats remove channel:#info
```

### 既存機能の追加オプション

チケット、抽選、ボイスルーム、XP、誕生日、バックアップ、ログ、状態表示への追加機能です。

```
/support ticket claim
/support ticket rename name:billing-help
/support ticket list

/engage giveaway cancel giveaway_id:3
/engage giveaway edit giveaway_id:3 prize:Nitro winners:2 extend:1h

/community voice rename name:Study room                      # only the owner of the room
/community voice limit limit:4
/community voice lock
/community voice unlock
/community voice kick member:@User
/community voice transfer member:@User
/community voice claim                                       # if the owner left

/xp channelboost channel:#chat multiplier:1.5
/xp resetall confirm:True
/info leaderboard page:2

/birthday list
/birthday setup user member:@User day:14 month:3
/birthday setup clear member:@User

/server backup info name:weekly
/server log show
/server log ignorechannel channel:#bots
/server log ignoreuser user:@Bot
/server log sent enabled:True

/automod status
/access verify status
/security raid status
/community welcome show
/engage starboard show
```

### その他の AutoMod ツール

短縮リンクの追跡、新規メンバーのリンク制限、ゴーストピングの検出、誰も処罰せずにルールをテストできます。

```
/automod toggle rule:shortlinks enabled:True action:delete    # follow short links and judge the target
/automod set rule:shortlinks option:resolve value:true         # false = block short links outright
/automod set rule:shortlinks option:block_unresolved value:false
/automod add name:shortlink_domains value:example.link

/automod toggle rule:newlinks enabled:True action:delete       # new members may not post links
/automod set rule:newlinks option:hours value:48
/automod add name:newlinks_allow value:tenor.com

/automod ghostping enabled:True notify:True max_age:120
/automod dryrun rule:words enabled:True                        # report only, rule: all, words, caps, phishing, flood ...
/automod test text:free nitro at bit.ly/example member:@User
```

### モデレーターの上限と権限監査

モデレーターがBANやキックをしすぎたときに警告し、危険な権限を持つロールを一覧表示します。

```
/team modwatch status
/team modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/team modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/team modwatch exclude member:@TrustedMod

/team permaudit run                                                  # roles with dangerous permissions and who holds them
/team permaudit watch enabled:True                                   # alarm when a role or member gets one
/team permaudit trust role:@Admin
```

### 通報と招待の追跡

メンバーがメッセージをスタッフに通報し、ボットは新規メンバーがどの招待で参加したかを記録します。

```
/report setup set channel:#reports ping_role:@Moderator cooldown:60 anonymous:False
/report setup ignorechannel channel:#staff
/report setup status

/report send message_link:https://discord.com/channels/1/2/3 reason:Spam
# or right click a message, Apps, Report message

/server invites who member:@User
/server invites stats user:@User
/server invites top
/server invites setup log:True alert_joins:5 alert_minutes:60
```

### 診断とデバッグ

不足している権限や壊れた設定を見つけ、エラーレポートをチャンネルで受け取り、設定をエクスポート・インポートできます。

```
/server diagnose                                                       # permissions, role order, deleted channels and roles
/server debug status
/server debug errorchannel channel:#bot-errors
/server debug errortest
/server debug selftest enabled:True                                    # check at start-up
/server debug usagestats enabled:True
/server debug usage reset:False
/server debug level level:DEBUG                                        # owner of the bot only
/server debug db action:check                                          # owner of the bot only: check, vacuum, size

/admin config export
/admin config import file:guardbot-settings.json confirm:False        # first without confirm
```

### 音楽

リンクと music フォルダ内のファイルをボイスチャンネルで再生します。ダウンロードは music/アーティスト/アルバム/曲 として保存されます。ffmpeg と requirements.txt のパッケージが必要です。

```
/play query:daft punk one more time                            # library first, then the web
/play query:https://example.com/track                           # a link that yt-dlp supports

/music queue page:1
/music nowplaying
/music skip
/music pause
/music resume
/music stop
/music volume percent:70
/music loop mode:queue
/music shuffle
/music remove number:3
/music clear
/music seek position:1:30
/music join
/music leave

/music library search query:discovery
/music library list artist:Daft Punk
/music library play query:one more time
/music library scan                                             # after you copied files into music/
/music library info
/music library download url:https://example.com/track format:best

/music sources spotify:True apple_music:True tidal:True search:youtube
/music playlist save name:Evening
/music playlist play name:Evening shuffle:True
/music stay enabled:True channel:#Lounge playlist:Evening

/music settings dj_role:@DJ volume:50 max_queue:100 per_user:25 max_minutes:60 idle_leave:120
/music settings allow_links:True allow_search:True allow_playlists:True library:True
/music settings allow_download:True download_format:best announce:True
/admin config set path:music.allowed_hosts value:bandcamp.com,archive.org
/music cleardj
/music status
```

ロスレス：自分で追加したファイル（FLAC、WAV、ALAC）やFLACを提供するソースはそのまま再生されます。YouTubeやSoundCloudなどは非可逆音声しか提供しておらず、後からロスレスにすることはできません。Discordは音声をOpusで送信し、ボットはボイスチャンネルのビットレートを使います。責任：コンテンツのダウンロードや再生はサイトの利用規約や著作権法に違反する場合があります。ダウンロードは初期設定でオフで、モジュールも有効にするまでオフです。再生・保存される内容の責任はボットの運営者にあります。

ソース: YouTube と SoundCloud のリンクと検索はそのまま再生されます。Spotify、Apple Music、Tidal のリンクも受け付けますが、これらのサービスは音声を提供しません。ボットは公開ページからタイトルとアーティストを読み取り、検索ソース (YouTube または SoundCloud、/music sources で設定) から同じ曲を再生します。Spotify と Apple Music のアルバムやプレイリストは公開ページから読み取ります。Tidal のアルバムとプレイリストには developer.tidal.com の無料開発者キーを .env に入れる必要があります (TIDAL_CLIENT_ID と TIDAL_CLIENT_SECRET)。音楽フォルダのファイルはそのまま再生されます。保存したプレイリストにはすべてのソースを混ぜられ、/music stay はボットを 24 時間ボイスチャンネルに留め、再起動後もプレイリストを繰り返し再生します。

Guard Music (2 つ目のボット): 音楽を専用のボットアカウントで動かせるので、モデレーションに影響せず常にボイスチャンネルに留まれます。

1. Discord Developer Portal で 2 つ目のアプリケーションを作成し、Guard Music と名付けて、そのボットのトークンをコピーします。
2. トークンを .env に MUSIC_TOKEN として書き込み、settings.json の music_bot.enabled を true にします。
3. GuardBot を再起動します。Guard Music は同じプロセスで起動し、同じ設定とデータを使い、音楽コマンドは Guard Music に移ります。
4. ダッシュボードの「音楽」ページを開き、そこにあるボタンで Guard Music をサーバーに追加します。MUSIC_TOKEN がなければ音楽は GuardBot に残ります。

利用は自己責任です。YouTube などのサービスからのストリーミングは各サービスの利用規約に反する場合があり、再生する内容には著作権が適用されます。Spotify、Apple Music、Tidal からは何もダウンロードせず、保護を回避することもありません。再生内容の責任はボットの運営者にあります。ダッシュボードの「音楽」ページには、プレイヤー、キュー、プレイリスト、24/7 モード、ソース、このガイドが表示されます。

### セットアップとヘルスチェック

ガイド付きアシスタントが、ボタンとメニューで重要な設定を行います：ログチャンネル、ウェルカムチャンネル、スタッフロール、ラーゲリ、AutoMod のプリセット（緩め、標準、厳しめ）、サーバーテンプレート（コミュニティ、ゲーム、サポート）、そして言語です。/server health で設定済みの項目と残りの項目を確認できます。言語を変えると、既定のウェルカムメッセージ、AutoMod の通知、認証、チケット、異議申し立て、モッドメール、ロールメニューなど、メンバーに表示される文章が変わります。管理者への定型の返信は翻訳され、名前や数字を含む返信は英語のままです。

```
/admin setup                                                         # buttons and menus, nothing is switched off by a template
/server health                                                        # what is set up, what is open, and the self-test
/admin language code:de
```

### 経済

毎日の報酬、仕事、送金、ランキング、そしてロールを付与できる商品を扱うショップを備えたサーバー通貨です。economy モジュールで有効にします。コマンドはプレフィックスでも使えます（例：!economy daily）。

```
/admin module enable name:economy
/engage economy balance member:@User                                  # same as !economy
/engage economy daily
/engage economy work
/engage economy pay member:@User amount:50
/engage economy leaderboard
/engage economy shop
/engage economy buy item:1
/engage economy inventory

/engage economy give member:@User amount:500                          # staff, a negative amount takes away
/engage economy shopadd name:VIP price:1000 role:@VIP stock:10
/engage economy shopremove item:1
/engage economy config name:gold daily:200 daily_hours:24 work_min:20 work_max:80 work_minutes:30
```

### ロールメニュー、予約メッセージ、フィード

ロールメニューはボタンまたはドロップダウンでロールを付与します。予約メッセージは一度だけ、または毎時・毎日・毎週繰り返して投稿されます。フィードは YouTube の新着動画、Twitch の配信、RSS の記事を投稿します。YouTube にはチャンネル ID（UC で始まる）を使います。Twitch には .env に TWITCH_CLIENT_ID と TWITCH_CLIENT_SECRET が必要です。時刻は in 2h、18:30、または 2026-12-24 18:00 のような日付と時刻で、サーバーのタイムゾーンに従って指定します。フィードの最初のチェックでは、すでにあるものを記憶するだけです。

```
/post rolemenu create title:Pick your roles kind:buttons single:False channel:#roles
/post rolemenu add menu:1 role:@Red label:Red
/post rolemenu remove menu:1 role:@Red
/post rolemenu delete menu:1
/post rolemenu list

/post schedule add channel:#news when:18:30 text:Daily reminder repeat:daily
/post schedule add channel:#news when:in 2h text:Restart soon repeat:none
/post schedule list
/post schedule remove number:1
/post schedule timezone name:Europe/Berlin

/post feed add kind:youtube target:UCxxxxxxxxxxxxxxxxxxxxxx channel:#videos ping:@Subscribers
/post feed add kind:twitch target:somestreamer channel:#live
/post feed add kind:rss target:https://example.com/feed.xml channel:#news
/post feed list
/post feed check
/post feed remove number:1
```

### アクティビティ、一括操作、ケース検索

アクティビティはチャンネルごとのメッセージ数と、日ごとの参加・退出数を数え、内容や名前は記録しません。一括操作は確認の後、最大25人のユーザーをBAN、キック、またはタイムアウトします。ケースはユーザー、種類、名前、理由、モデレーター、経過日数で検索でき、メモをBANに関連付けるなど、相互にリンクできます。

```
/admin module enable name:activity
/community activity overview days:7
/community activity channels days:30
/community activity growth days:14
/community activity reset

/moderation bulk ban users:123456789012345678 223456789012345678 reason:Raid
/moderation bulk kick users:123456789012345678 223456789012345678 reason:Spam
/moderation bulk timeout users:123456789012345678 223456789012345678 duration:2h reason:Spam

/moderation cases user:@User kind:ban text:scam moderator:@Mod days:30
/moderation case link case_id:12 other:15
/moderation case unlink case_id:12 other:15
```

### 詐欺対策・暗号資産対策

典型的な MrBeast 詐欺のような偽のプレゼント企画を、テキストでも画像でも数ミリ秒で削除します。即時リストの名前は、どんな綴りでもその場で削除されます（MrBeast、Mr Beast、M R B E A S T、Mr.B3ast）。それ以外はリスト（名前、釣り文句、暗号資産、リンク、金額）の語が加点され、しきい値に達するとメッセージが削除されます。画像は OCR で読み取られ、一度詐欺と判定された画像は再度読み取らずに削除されます。画像の読み取りには tesseract が必要で、なければテキストだけが検査されます。MrBeast のサーバーは、即時リストから名前を外すか、/automod exemptchannel でチャンネルを除外できます。頼る前に /security antiscam test で試してください。

```
/security antiscam status
/security antiscam set action:delete threshold:3 text:True images:True ocr_lang:eng max_images:3
/security antiscam words action:add kind:instant word:mrbeast
/security antiscam words action:remove kind:crypto word:token
/security antiscam test text:MrBeast is giving away 1000 BTC, claim now
/security antiscam testimage image:scam.png
/security antiscam forget
/automod dryrun rule:antiscam enabled:True                     # only report, do not remove
```

### 仮参加期間、群れの検出、タイムライン、学習

仮参加期間は、新しいメンバーをロールに入れます。設定した数の通常メッセージを書くか、設定した分数が過ぎるまで、リンク、招待、ファイルは短い通知とともに削除されます。レイド対策は群れも検出します。名前のパターンが同じ、プロフィール画像が同じ、または作成時刻が数分以内の新しいアカウントが複数ある場合です。タイムライン（/moderation case timeline）は、1人のユーザーのアカウント作成、参加と招待、仮参加期間、ケース、異議申し立てを時系列でまとめます。メッセージは保存されないため含まれません。/security block、/security unblock、/security blocklist は短いコマンドで AutoMod のブロックリストを管理します。モデレーターは、メッセージのコンテキストメニュー項目 Mark as scam、または learn_emoji で設定した絵文字のリアクションで詐欺対策モジュールに覚えさせられます。メッセージは削除され、その画像とテキストは以後すぐに削除されます。各機能は、それぞれのモジュールまたは設定でオフにできます。

```
/admin module enable name:probation
/access probation setup minutes:10 messages:1 block_links:True block_files:True
/access probation status
/access probation release member:@User
/access probation add member:@User

/security raid swarm enabled:True minimum:4 minutes:10
/moderation case timeline user:@User

/security block kind:link value:evil.example
/security blocklist
/security unblock kind:link number:1
/security antiscam set learn_emoji:X
```

### パネル

パネルは、ようこそ投稿、ルール、ロール選択、通知ボタン、認証などの投稿で、バナー画像、テキストボックス、ボタンで構成されます。`/panel` またはダッシュボードの Panels ページで作成します。画像はそこで、またはコマンドのオプションでアップロードし、ボットが `data/panels` に保存するので、リンク切れになりません。

```
/panel create name:welcome template:welcome channel:#welcome
/panel section name:welcome banner:image.png
/panel section name:welcome number:1 color:#5865f2 thumbnail:logo.png
/panel create name:origin template:roles
/panel button name:origin kind:role label:KL role:@KL
/panel button name:origin kind:role label:Kreis role:@Kreis
/panel single name:origin value:True
/panel create name:check template:verify
/panel button name:welcome kind:link label:Website url:https://example.com
/panel preview name:welcome
/panel post name:welcome
/panel update name:welcome
/panel list
/panel show name:welcome
/panel removesection name:welcome number:2
/panel removebutton name:origin number:1
/panel delete name:welcome messages:True
```

テンプレート：empty、welcome、rules、roles、notifications、verify。テキストはサーバーの言語で、変更できます。`/panel section` はタイトル、本文、フッターのフォームを開きます。各セクションは1つのメッセージになり、バナーはボックスの上、大きな画像はボックス内、小さな画像は右上に表示されます。ボタンは最後のセクションの下に1行5個まで並びます。ロールボタンはロールを付与または解除し、`single` がオンならパネルのほかのロールは外されます。verify ボタンは認証モジュールの認証を開始します（ボタン、キャプチャ、計算は `/access verify setup` で選びます）。テキストでは `{server}` と `{count}` を使えます。編集後は `/panel update` で投稿済みのメッセージを更新します。サーバーごとの上限：パネル25個、1パネルにつきセクション5個とボタン20個、8 MBまでの画像40枚。ボットは自分の最上位ロールより下で、危険な権限を持たないロールだけを提供します。

### スキルとAI

スキルは、サーバー自身が安全なブロックから組み立てるコマンド、ゲーム、自動化です。AIは不要で、コードを実行することは決してありません。AIは任意です。自分のキーを使うと、説明からスキルを書いてくれたり、スキャム対策のチェックでセカンドオピニオンを出してくれたりします。

AIなしのスキル：

- `/support skill create kind:command name:hello` は、変更できる小さな例の入った入力欄を開きます。`/support skill edit`、`show`、`import`、`enable`、`disable`、`delete`、`list`、`stats` で管理します。誰でも `/support skill run` またはプレフィックス（例：`!hello`）でスキルを使えます。`/support skill panel` はスキルを実行するボタンを投稿します。
- 種類：コマンド（アクションの一覧）、ゲーム（サイコロ、選択、スロット、じゃんけん、クイズ）、自動化（メンバーの参加や退出、メッセージに特定の語が含まれたとき、ボタンが押されたときに開始）。
- アクション：返信、チャンネルへ送信、DM、ログ、ロールの付与や削除、カウンターの変更、コインの付与、ランダム選択。アクションには条件を付けられます：ロールを持つ、確率、カウンターと数値の比較。
- テキストでは `{user}`、`{user_name}`、`{server}`、`{channel}`、`{count}`、`{arg1}`、`{arg2}`、`{var:name}`、`{uvar:name}`、`{random:1-6}` を使えます。
- 制限：サーバーあたり50スキル、1スキルあたり10アクション、ロール変更3回、メッセージ4件。ボットは、自身の最上位ロールより下にあり、危険な権限を持たないロールだけを付与します。コインを付与するスキルには60秒以上のクールダウンが必要です。ボットのコマンド、エイリアス、タグの名前は使えません。
- スキルはJSONとして保存され、設定のエクスポートに含まれます。未知のフィールドは拒否されるため、どこから来たスキルでもブロックが許すことしかできません。

例：ロールを付与して使用回数を数えるコマンド（ロールIDを置き換えてください）：

```json
{
  "name": "join-team",
  "kind": "command",
  "description": "Join the team once",
  "cooldown": 60,
  "actions": [
    {"do": "add_role", "role": 123456789012345678, "if": [{"not": {"has_role": 123456789012345678}}]},
    {"do": "add_var", "name": "joined", "amount": 1},
    {"do": "reply", "text": "Welcome, {user}! {var:joined} members joined so far."}
  ]
}
```

AI接続（任意）：

- `/support ai setup provider:kimi agree:true` は、APIキー用の非公開の入力欄を開きます。プロバイダーはAnthropic、OpenAI、Kimi（Moonshot）です。モデルが提案され、同じコマンドまたはダッシュボードで変更できます。モデル名はプロバイダー側で変わるため、各ドキュメントを確認してください。料金はプロバイダーに支払います。
- `/support ai make wish:...` はAIにスキルを依頼し、インポートしたスキルと同じ厳しさで回答を検査してプレビューを表示します。保存を押すまで何も保存されません。
- `/support ai status`、`limits`（1日のリクエスト数、1人あたりのリクエスト間隔の秒数）、`remove` で一式です。キーは暗号化して保存され、その秘密はファイル `data/ai.secret` にあります。このファイルはバックアップと一緒に保管してください。ないと保存したキーは読めず、入力し直す必要があります。キーが表示、記録、エクスポートされることはありません。プロバイダーは新しいキーと一緒にしか変更できないため、キーが別のプロバイダーに送られることはありません。
- 送信される内容：`/support ai make` の依頼文と、セカンドオピニオンでは疑わしいメッセージのテキストです。それ以外は送信されず、モジュール `ai` がオンの間だけです。[PRIVACY.md](../PRIVACY.md) を参照してください。

スキャム対策の学習：

- 学習フィルター（`/security antiscam set learned:true`）は、サーバーごとの小さな分類器です。モデレーターはコンテキストメニューの「Mark as scam」と「Not a scam」で学習させます。保存するのは語の短いハッシュだけでテキストは保存せず、スキャム8件と通常30件を見てから初めて動作し、その後も95パーセントを超えたときだけ動きます。`ham_sampling` を使うと、通常メッセージの10件に1件からも学習します。
- 類似画像（`similar`、既定でオン）は、画像のフィンガープリントを既知のスキャム画像と比較するため、保存し直したりサイズを変えたりしたコピーも見つかります。Tesseractなしで動作します。
- AIのセカンドオピニオン（`/support ai limits second_opinion:true`）：しきい値のすぐ下のケースや、学習フィルターが疑わしいと判断したケースでAIに尋ねます。AIが80パーセント以上の確信度でスキャムと答えたときだけメッセージが削除され、その回答が他のことを引き起こすことはありません。

### メッセージビルダーと更新

メッセージビルダーは、JSON から複数の埋め込みとリンクボタンを含むメッセージを投稿します。Embed Generator などの埋め込みジェネレーターが書き出す JSON を読み取るので、そこでメッセージを作り、ボットで投稿できます。JSON は、テキスト、.json ファイル、または JSON を直接指す https リンク（たとえばリポジトリの生ファイル）で渡します。リダイレクトするリンクは拒否されます。作成されるのはリンクボタンだけで、操作が必要なボタンはスキップされます。リンクはすべて http か https である必要があり、テキスト内のメンションは通知されず、Discord の制限が適用されます。/post message copy は既存のメッセージを JSON として書き出し、/post message edit はボットのメッセージを変更し、/post message preview は結果をあなただけに表示します。ウェブエディターの共有リンクは、形式が公開されていないため開きません。

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

ボットは 12 時間ごとに、update.repo（scripts/set_repo_url.py で設定）の GitHub リポジトリに新しいリリースがないか確認します。ある場合、ボットの所有者にリリースノート付きのダイレクトメッセージが届き、リリースがダウンロードされて検査されます。検査内容は、リリースの SHA-256 チェックサム、アーカイブ内の安全なパス、タグと一致するバージョンです。インストールは /server debug update action:install で行うか、auto_install がオンなら自動で行われます。インストール前に、置き換えられるファイルは data/update に保存され、新しいパッケージがインストールされ、新しいコードが試験的にインポートされます。どこかで失敗すると、古いファイルが復元されます。.env、settings.json、data、music には一切手を加えません。その後ボットは自動で再起動します。Docker ではその場にはインストールされないので、イメージを更新してください。更新はリポジトリのコードを実行するため、信頼できるリポジトリだけを指定してください。enabled を false にすると無効になります。

```json
{
  "update": {
    "enabled": true,
    "repo": "NAME/guardbot",
    "check_hours": 12,
    "auto_install": false,
    "require_checksum": false
  }
}
```

```
/post message send channel:#news url:https://example.com/message.json
/post message send channel:#news file:message.json
/post message preview url:https://example.com/message.json
/post message edit message:https://discord.com/channels/1/2/3 url:https://example.com/message.json
/post message copy message:https://discord.com/channels/1/2/3
/admin module disable name:builder
/server debug update action:status
/server debug update action:check
/server debug update action:install
```

### 運用

ボットは数秒ごとにデータを保存し、data/dbbackups にデータベースのバックアップを保持します（データ形式の変更前に1つ、毎日1つ）。音楽キュー、固定メッセージ、モデレーターのカウンターは再起動後も残ります。大規模なボットは複数のシャードで動かせます。ハートビートファイルと任意のステータスページは監視ツールの助けになります。これらのオプションは settings.json で設定します：

```json
{
  "shard_count": null,
  "message_cache": 10000,
  "members_intent": true,
  "chunk_guilds": true,
  "db_backup_hours": 24,
  "db_backup_keep": 7,
  "health_port": 0,
  "health_host": "127.0.0.1",
  "metrics_token": "",
  "log_format": "text",
  "log_max_mb": 2,
  "log_backups": 3,
  "workers": {"ocr": {"threads": 2, "limit": 20}},
  "tesseract": null,
  "music_generic": true
}
```

```
/server debug db action:backup                                         # owner of the bot only, saved in data/dbbackups
/server debug db action:list
```

ログは data/guardbot.log に書き込まれます(ローテーションあり。log_max_mb と log_backups を参照)。log_format を json にすると、サーバーとコマンドを含む1行1JSONオブジェクトになります。health_port を設定すると、/metrics が Prometheus 形式のメトリクス(稼働時間、遅延、メモリ、データベースサイズ、エラー、コマンドの使用回数と所要時間、作業レーン)を返します。出力されるのは数値だけで、名前やIDは含まれません。metrics_token を設定すると bearer トークンが必要になります。重い処理(画像の読み取り、カードの描画、音楽ファイル、バックアップ)は、スレッド数と上限が決まったレーンで実行されます(settings.json の workers)。レーンが満杯のときは、作業をためずに「混み合っています」と返します。データベースのバックアップは、作成直後に開いて検証されます。復元するには、ボットを停止して次を実行します:

```
python scripts/restore_db.py data/dbbackups/guardbot-YYYYMMDD-HHMMSS-auto.db
python scripts/restore_db.py BACKUPFILE --check          # only check a backup
```

現在のデータベースは before-restore という名前のバックアップとして残ります。

### 管理

モジュールとコマンドのオン・オフ、プレフィックスの変更、エイリアスの設定、ロールによるコマンド制限。

```
/admin module list
/admin module disable name:starboard
/admin module enable name:tickets
/admin command disable name:ban                          # single commands
/admin command enable name:ban
/admin command list

/admin prefix new_prefix:?                               # text commands now start with ?
/admin alias add alias:w command:warn                    # ?w @User Spam
/admin alias remove alias:w
/admin alias list

/admin perms allow command:ban target:@HeadModerator     # only this role may use /moderation ban
/admin perms deny command:warn target:@Trainee
/admin perms reset command:ban
/admin perms show

/admin settings
/help
/info about
```

## メッセージのプレースホルダー

設定したテキストの中で、次のプレースホルダーが置き換えられます：

```
/community welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/community booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/community tempvoice setup     name                            {name}
/access jailsetup notice    text                            {staff}
```

## 設定

全体の設定は settings.json で行います。それ以外はサーバーごとに /admin module、/admin command、/admin perms、/admin alias、/admin config などのコマンドで設定します。

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

すべての設定は /admin config で読み取りと変更ができます。よく使うパスは次のとおりです：

```
/admin config get path:automod.caps.percent
/admin config set path:automod.caps.percent value:80
/admin config set path:mod.dm_user value:false             # no direct message on punishments
/admin config set path:mod.warn_expiry_days value:30       # warnings expire after 30 days
/admin config set path:mod.default_mute_minutes value:120
/admin config set path:automod.mentions.max value:5
/admin config set path:automod.phishing.lookalike value:true
/admin config set path:raid.joins value:8
/admin config set path:xp.cooldown value:45
/admin config set path:tickets.max_open value:2
/admin config set path:privacy.retention_days value:90
/admin config reset section:welcome                        # back to the defaults of one section
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
    defaults/             default settings, one file per area (core, security, moderation, community) and base.py for modules and permissions
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature, in the folders security, moderation, server, community, tools
    skills.py             スキルエンジン：スキルを検査して実行
    ai.py                 AIプロバイダー、暗号化されたキー、制限
    learner.py, imgsim.py スキャム対策の学習フィルター、画像フィンガープリント
    dashboard_manage.py   コマンド、スキル、AI、プロフィールのダッシュボードページ
  docs/                   documentation in 12 languages, COMMANDS.md, PRIVACY.md
  deploy/                 systemd service, Dockerfile, compose file
  scripts/                maintenance scripts
  tests/                  automated tests (python -m unittest)
  data/                   created at runtime, holds your settings and data
```

## 翻訳

英語がこのプロジェクトの原文です。ドキュメント、ダッシュボード、ボットのメッセージのすべての翻訳は機械翻訳で作成されており、ネイティブスピーカーによる確認は受けていません。不自然な表現や誤りがありえますので、見つけたらご報告いただくか、修正をお送りください。ファイルは docs/ と guardbot/locales/ にあります。

## ロードマップ

- ダッシュボードにアクティビティとモデレーションのグラフを追加。
- すべての翻訳のネイティブスピーカーによる確認。
- 固定の返信テキストの翻訳を増やす。

## プライバシーとセキュリティ

- テレメトリーはありません。ボットは Discord と通信し、更新の確認のために GitHub とも通信します（個人データは送りません。update.enabled でオフにできます）。管理者が渡したリンク（フィード、音楽、JSON のリンクなど）は、要求があったときだけ開きます。
- すべてのデータは、お使いのコンピューターの data フォルダーに保存されます。設定、XP、誕生日（日と月のみ）、モデレーション記録です。
- ボットはメンバーからのダイレクトメッセージを無視します。
- トークンは .env ファイルから読み込まれます。共有したり公開したりしないでください。
- メンバーは /info mydata で自分のデータをエクスポートおよび削除できます。管理者は、退出したメンバーのデータを保持する期間を設定できます。
- AI機能は自分のキーを追加するまでオフです。追加後も、選んだプロバイダーに送信されるのは `/support ai make` のテキストと、セカンドオピニオンでの疑わしいメッセージだけです。
- [PRIVACY.md](../PRIVACY.md)

## サポート

バグ、アイデア、提案は Discord の @justyyin に連絡するか、GitHub で issue を作成してください。

## クレジット

GuardBot は Merlin Fuchs 氏の [Embed Generator](https://github.com/merlinfuchs/embed-generator)（MIT ライセンス、message.style で公開）に着想を得ています。メッセージビルダーは同じ JSON 形式を読み取るため、そこで作ったメッセージをこのボットで投稿できます。そのプロジェクトのコードは含まれていません。discord.py、aiohttp、Pillow、yt-dlp、mutagen、Tesseract の作者に感謝します。

## ライセンス

MIT ライセンスで公開されています。参照： [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
