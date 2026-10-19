# GuardBot: 安装指南

本指南介绍如何在自己的电脑或 VPS 上运行 GuardBot，大约需要 15 分钟。

<!-- toc -->

- [创建 Discord 机器人](#创建-discord-机器人)
- [在自己的电脑上运行](#在自己的电脑上运行)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux 和 macOS](#linux-和-macos)
- [在 VPS 上运行](#在-vps-上运行)
- [使用 Docker 运行](#使用-docker-运行)
- [在 Discord 中的第一步](#在-discord-中的第一步)
- [更新与备份](#更新与备份)
- [故障排除](#故障排除)
- [支持](#支持)

<!-- tocstop -->

## 创建 Discord 机器人

1. 打开 [Discord Developer Portal](https://discord.com/developers/applications)，点击 New Application。
2. 打开 Bot 选项卡，点击 Reset Token。复制令牌并妥善保密。
3. 在同一选项卡中开启 Server Members Intent 和 Message Content Intent。
4. 打开 OAuth2 的 URL Generator，选择 scopes：bot 和 applications.commands。
5. 选择权限：Manage Roles、Manage Channels、Kick Members、Ban Members、Moderate Members、View Audit Log、Manage Messages、Send Messages、Embed Links、Attach Files、Read Message History、Add Reactions、Move Members。直接选择 Administrator 也可以，这是最简单的方式。
6. 打开生成的链接，把机器人添加到你的服务器。
7. 在服务器设置中，把机器人的身份组移到身份组列表的最上方。机器人只能管理位于它自己身份组之下的身份组。

也可以使用下面的邀请链接，把 YOUR_CLIENT_ID 替换为 Developer Portal 中的 Application ID：

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## 在自己的电脑上运行

安装 Python 3.11 或更高版本以及 Git，然后在终端中执行以下命令。

### Windows (PowerShell)

```powershell
git clone https://github.com/YOUR-NAME/guardbot.git
cd guardbot
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
python main.py
```

### Linux 和 macOS

```bash
git clone https://github.com/YOUR-NAME/guardbot.git
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
```

打开 .env 文件，把占位符替换为你的机器人令牌。控制台出现以 online as 开头的一行时，机器人即已上线。请保持窗口打开，关闭窗口后机器人会停止。

## 在 VPS 上运行

以下命令适用于 Ubuntu 或 Debian，会把机器人设置为开机自动启动的服务。

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
sudo git clone https://github.com/YOUR-NAME/guardbot.git /opt/guardbot
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

用 systemctl status guardbot 查看状态。机器人就绪后，日志中会出现以 online as 开头的一行。

## 使用 Docker 运行

Docker 是可选的。先创建 .env 文件，然后执行：

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## 在 Discord 中的第一步

在你的服务器中使用这些命令，并把频道名称替换为你自己的。

```
/log set category:main channel:#logs
/jailsetup setup
/automod toggle rule:phishing enabled:True action:jail
/automod toggle rule:words enabled:True
/automod add name:words value:example
/raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3
/antinuke setup enabled:True action:strip
/xp config enabled:True
/module list
```

所有功能都在命令参考中说明： [COMMANDS.md](../COMMANDS.md).

## 更新与备份

更新机器人：

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

复制 data 文件夹即可备份设置，例如：

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## 故障排除

- 斜杠命令没有出现：请等待几分钟，重启 Discord，并确认邀请机器人时包含 applications.commands 范围。
- 机器人因特权 Intents 错误而停止：请在 Developer Portal 中开启 Server Members Intent 和 Message Content Intent。
- Improper token：请重新复制令牌，并确认 .env 中恰好是 DISCORD_TOKEN=令牌，没有空格或引号。
- I cannot assign that role：请把机器人的身份组移到它要管理的身份组之上。
- 没有任何日志：用 /log set 设置频道，并确认机器人在该频道有发送消息、嵌入链接和附加文件的权限。
- Unknown timezone：执行 pip install tzdata 并重启机器人。

## 支持

错误、想法和建议：Discord @justyyin 或 GitHub issue。

Copyright (c) Justyn - made in Germany

<!-- GuardBot (c) Justyn -->
