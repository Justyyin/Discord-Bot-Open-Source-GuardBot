# GuardBot: セットアップガイド

このガイドでは、自分のコンピューターまたは VPS で GuardBot を動かす方法を説明します。所要時間は約 15 分です。

> ベータ版：GuardBot とそのダッシュボードはベータ段階です。十分にテストされておらず、特に大規模なサーバーや Discord のあらゆる状況では確認していません。不具合が起こりうるため、data フォルダーのバックアップを取り、問題を報告してください。自己責任でご利用ください。

<!-- toc -->

- [Discord ボットを作成する](#discord-ボットを作成する)
- [自分のコンピューターで動かす](#自分のコンピューターで動かす)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux と macOS](#linux-と-macos)
- [VPS で動かす](#vps-で動かす)
- [Docker で動かす](#docker-で動かす)
- [Discord での最初の手順](#discord-での最初の手順)
- [更新とバックアップ](#更新とバックアップ)
- [音楽（任意）](#音楽任意)
- [任意：画像の読み取りと言語](#任意画像の読み取りと言語)
- [ダッシュボード](#ダッシュボード)
- [トラブルシューティング](#トラブルシューティング)
- [サポート](#サポート)

<!-- tocstop -->

## Discord ボットを作成する

1. [Discord Developer Portal](https://discord.com/developers/applications) を開き、New Application をクリックします。
2. Bot タブを開き、Reset Token をクリックします。トークンをコピーし、他人に見せないでください。
3. 同じタブで Server Members Intent と Message Content Intent をオンにします。
4. OAuth2 の URL Generator を開き、スコープ bot と applications.commands を選びます。
5. 権限を選びます：Manage Roles、Manage Channels、Kick Members、Ban Members、Moderate Members、View Audit Log、Manage Messages、Send Messages、Embed Links、Attach Files、Read Message History、Add Reactions、Move Members。Administrator でも動作し、これが最も簡単です。
6. 生成された URL を開き、ボットをサーバーに追加します。
7. サーバー設定で、ボットのロールをロール一覧の一番上に移動します。ボットは自分のロールより下にあるロールしか管理できません。

次の招待 URL も使えます。YOUR_CLIENT_ID は Developer Portal の Application ID に置き換えてください：

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## 自分のコンピューターで動かす

Python 3.11 以降と Git をインストールし、ターミナルで次のコマンドを実行します。

### Windows (PowerShell)

```powershell
git clone <REPOSITORY_URL>
cd guardbot
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
python main.py
```

### Linux と macOS

```bash
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
```

.env ファイルを開き、プレースホルダーをボットのトークンに置き換えます。コンソールに online as で始まる行が表示されれば、ボットはオンラインです。ウィンドウを閉じるとボットも止まるので、開いたままにしてください。

## VPS で動かす

次のコマンドは Ubuntu または Debian 用で、ボットを自動起動するサービスとして設定します。

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0
sudo git clone <REPOSITORY_URL> /opt/guardbot
sudo useradd --system --no-create-home --shell /usr/sbin/nologin guardbot
cd /opt/guardbot
sudo python3 -m venv .venv
sudo .venv/bin/pip install -r requirements.txt
sudo cp .env.example .env
sudo nano .env
sudo mkdir -p data
sudo chown -R guardbot:guardbot /opt/guardbot
sudo chmod 600 .env
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now guardbot
sudo journalctl -u guardbot -f
```

状態は systemctl status guardbot で確認します。準備ができると、ログに online as で始まる行が表示されます。

## Docker で動かす

Docker は任意です。先に .env ファイルを作成し、次を実行します。

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## Discord での最初の手順

サーバーで次のコマンドを使い、チャンネル名を自分のものに置き換えてください。

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

すべての機能はコマンドリファレンスで説明しています： [COMMANDS.md](../COMMANDS.md).

## 更新とバックアップ

ボットを更新する：

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

data フォルダーをコピーして設定をバックアップします。例：

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## 音楽（任意）

音楽モジュールには、ボットを動かすコンピューターに ffmpeg が必要です。自分の音楽を music/ フォルダに アーティスト/アルバム/01 - 曲名.flac の形で置くか、ダウンロードを許可してください。フォルダは大きくなることがあるため、空き容量のあるディスクか Docker ボリュームに置いてください。

```
# Windows
winget install Gyan.FFmpeg
# macOS
brew install ffmpeg
# Ubuntu or Debian
sudo apt install -y ffmpeg libopus0

# in Discord
/module enable name:music
/music settings allow_download:True
```

## 任意：画像の読み取りと言語

詐欺対策モジュールに画像内の文字を読ませるには、ボットを動かすコンピューターに tesseract をインストールします（Docker イメージには含まれています）。その後 /antiscam status で準備できているか確認します。メンバーに表示されるメッセージの言語は /language で選びます。

```
# Ubuntu or Debian
sudo apt install -y tesseract-ocr
# macOS
brew install tesseract
# Windows
winget install UB-Mannheim.TesseractOCR

# in Discord
/antiscam status
/language code:de
```

## ダッシュボード

ダッシュボードはボットの中で動くウェブページです。Discord でログインすると、コマンドの代わりにスイッチ、メニュー、入力欄でサーバーの設定を変更できます。対象はモジュール、チャンネル、ロール、しきい値、テキスト、プレフィックス、言語です。直近のモデレーションケースの表示や、設定のエクスポートとインポートもできます。自分のコンピューターでも VPS でも同じように動作し、オンにするまでは無効です。

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

## トラブルシューティング

- スラッシュコマンドが表示されない：数分待ってから Discord を再起動し、ボットを applications.commands スコープ付きで招待したか確認してください。
- 特権 Intent のエラーでボットが停止する：Developer Portal で Server Members Intent と Message Content Intent をオンにしてください。
- Improper token：トークンをもう一度コピーし、.env の内容が DISCORD_TOKEN=トークン だけで、空白や引用符がないことを確認してください。
- I cannot assign that role：ボットのロールを、管理させたいロールより上に移動してください。
- 何も記録されない：/log set でチャンネルを設定し、ボットがそのチャンネルでメッセージ送信、リンク埋め込み、ファイル添付をできるか確認してください。
- Unknown timezone：pip install tzdata を実行してボットを再起動してください。
- 原因が分からないまま失敗する場合：エラーと警告はコンソールに出力されます。VPS では journalctl -u guardbot -f で確認できます。

## サポート

バグ、アイデア、提案：Discord の @justyyin または GitHub の issue へ。

Copyright (c) Justyn - made in Germany
