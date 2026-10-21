# GuardBot: セットアップガイド

このガイドでは、自分のコンピューターまたは VPS で GuardBot を動かす方法を説明します。所要時間は約 15 分です。

<!-- toc -->

- [Discord ボットを作成する](#discord-ボットを作成する)
- [自分のコンピューターで動かす](#自分のコンピューターで動かす)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux と macOS](#linux-と-macos)
- [VPS で動かす](#vps-で動かす)
- [Docker で動かす](#docker-で動かす)
- [Discord での最初の手順](#discord-での最初の手順)
- [更新とバックアップ](#更新とバックアップ)
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
sudo apt install -y python3 python3-venv python3-pip git
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
