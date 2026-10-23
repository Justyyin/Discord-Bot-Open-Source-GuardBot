# GuardBot: 安装指南

本指南介绍如何在自己的电脑或 VPS 上运行 GuardBot，大约需要 15 分钟。

> 测试版：GuardBot 及其控制面板处于测试阶段，尚未经过充分测试，尤其没有在大型服务器上、也没有覆盖 Discord 上的所有情况。可能存在错误，请定期备份 data 文件夹并反馈问题。使用风险自负。

<!-- toc -->

- [创建 Discord 机器人](#创建-discord-机器人)
- [在自己的电脑上运行](#在自己的电脑上运行)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux 和 macOS](#linux-和-macos)
- [在 VPS 上运行](#在-vps-上运行)
- [使用 Docker 运行](#使用-docker-运行)
- [在 Discord 中的第一步](#在-discord-中的第一步)
- [结构、团队与概览(1.5)](#结构团队与概览15)
- [更新与备份](#更新与备份)
- [音乐（可选）](#音乐可选)
- [可选：读取图片与语言](#可选读取图片与语言)
- [控制面板](#控制面板)
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
git clone <REPOSITORY_URL>
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
git clone <REPOSITORY_URL>
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

所有功能都在命令参考中说明： [COMMANDS.md](../COMMANDS.md).

## 结构、团队与概览(1.5)

这些步骤用于设置较新的功能。每项功能都可以用 /admin module 关闭,前缀和文本也仍可按服务器修改。

1. 查看已配置的内容:`/admin module overview` 列出每个模块的状态以及是否已设置。控制面板的设置面板显示相同内容。
2. 查找命令:`/info find text:ban` 按词搜索所有命令,`/help` 显示分组。
3. 发布带接受按钮的规则:先 `/structure rules setup`,再 `/structure rules add`,然后 `/structure rules post`。未接受新版本的成员每隔几小时会收到提醒。
4. 告诉机器人谁是管理团队:`/team duty roster`。可用人员列表以及工单和警报的路由都会用到它。
5. 整理闲置频道:先 `/structure archive setup`,再 `/structure archive scan`。
6. 为回归的成员恢复身份组:`/members stickyroles setup`。
7. 保持名称可读:`/members nickname setup`,在 `/members nickname scan` 之前先用 `/members nickname check` 测试。
8. 进行大改动前,用 `/admin config export` 导出设置,并用 `/server diagnose` 检查身份组和频道。

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

## 音乐（可选）

音乐模块需要在运行机器人的电脑上安装 ffmpeg。把自己的音乐放进 music/ 文件夹，格式为 艺术家/专辑/01 - 曲名.flac，或允许下载。文件夹可能变得很大，请放在有空间的磁盘或 Docker 卷中。

```
# Windows
winget install Gyan.FFmpeg
# macOS
brew install ffmpeg
# Ubuntu or Debian
sudo apt install -y ffmpeg libopus0

# in Discord
/admin module enable name:music
/music settings allow_download:True
```

## 可选：读取图片与语言

要让反诈骗模块读取图片中的文字，请在运行机器人的电脑上安装 tesseract（Docker 镜像已包含）。然后用 /security antiscam status 检查是否就绪。用 /admin language 选择成员看到的消息语言。

```
# Ubuntu or Debian
sudo apt install -y tesseract-ocr
# macOS
brew install tesseract
# Windows
winget install UB-Mannheim.TesseractOCR

# in Discord
/security antiscam status
/admin language code:de
```

## 控制面板

控制面板是运行在机器人内部的网页。用 Discord 登录后，你可以用开关、菜单和输入框代替命令来修改服务器的设置：模块、频道、身份组、阈值、文本、前缀和语言。它还会显示最近的管理案件，并可导出和导入设置。它在你自己的电脑和 VPS 上的使用方式完全相同，在你开启之前处于关闭状态。

1. 在 Developer Portal 中打开你的应用，进入 OAuth2，把 Client Secret 复制到 .env 文件中。
2. 在同一页面添加重定向地址 http://localhost:8080/callback。
3. 在 settings.json 中开启控制面板。
4. 重启机器人，在浏览器中打开 http://localhost:8080，用 Discord 登录。

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

保持 host 为 127.0.0.1，并在两种方式中选一种。第一种是 SSH 隧道：不对外暴露任何东西，隧道运行期间在你的电脑上打开 http://localhost:8080 即可。

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

第二种是通过 Caddy 之类的反向代理使用 HTTPS，它会自动获取证书（见 deploy/Caddyfile.example）。然后把 public_url 设为你的 https 地址，在 Developer Portal 中添加 https://你的地址/callback 作为重定向，并把 trust_proxy 设为 true：

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

## 故障排除

- 斜杠命令没有出现：请等待几分钟，重启 Discord，并确认邀请机器人时包含 applications.commands 范围。
- 机器人因特权 Intents 错误而停止：请在 Developer Portal 中开启 Server Members Intent 和 Message Content Intent。
- Improper token：请重新复制令牌，并确认 .env 中恰好是 DISCORD_TOKEN=令牌，没有空格或引号。
- I cannot assign that role：请把机器人的身份组移到它要管理的身份组之上。
- 没有任何日志：用 /server log set 设置频道，并确认机器人在该频道有发送消息、嵌入链接和附加文件的权限。
- Unknown timezone：执行 pip install tzdata 并重启机器人。
- 出现无明显原因的失败：错误和警告会输出到控制台。在 VPS 上可用 journalctl -u guardbot -f 查看。

## 支持

错误、想法和建议：Discord @justyyin 或 GitHub issue。

Copyright (c) Justyn - made in Germany
