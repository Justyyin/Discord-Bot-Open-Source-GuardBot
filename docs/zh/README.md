# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | **中文** | [日本語](../ja/README.md) | [한국어](../ko/README.md)

自行托管的 Discord 机器人，用于管理、安全和社区。开源、免费，数据只保存在你自己的电脑上。

> 测试版：GuardBot 及其控制面板处于测试阶段，尚未经过充分测试，尤其没有在大型服务器上、也没有覆盖 Discord 上的所有情况。可能存在错误，请定期备份 data 文件夹并反馈问题。使用风险自负。

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
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [启动脚本与开机自启](#启动脚本与开机自启)
  - [更新](#更新)
- [机器人权限](#机器人权限)
- [在 Discord 中的第一步](#在-discord-中的第一步)
  - [结构、成员与团队](#结构成员与团队)
- [控制面板](#控制面板)
  - [设置控制面板](#设置控制面板)
  - [安全](#安全-1)
  - [在 VPS 上使用控制面板](#在-vps-上使用控制面板)
- [命令](#命令)
  - [命令分组](#命令分组)
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
  - [管理员工具](#管理员工具)
  - [信息查询](#信息查询)
  - [公告、标签与提醒](#公告标签与提醒)
  - [私信邮箱与封禁申诉](#私信邮箱与封禁申诉)
  - [计数频道、置底消息与统计](#计数频道置底消息与统计)
  - [现有功能的更多选项](#现有功能的更多选项)
  - [更多 AutoMod 工具](#更多-automod-工具)
  - [管理员限额与权限审计](#管理员限额与权限审计)
  - [举报与邀请追踪](#举报与邀请追踪)
  - [诊断与调试](#诊断与调试)
  - [音乐](#音乐)
  - [设置与健康检查](#设置与健康检查)
  - [经济](#经济)
  - [身份组菜单、定时消息与订阅源](#身份组菜单定时消息与订阅源)
  - [活跃度、批量操作与案件搜索](#活跃度批量操作与案件搜索)
  - [反诈骗与反加密货币](#反诈骗与反加密货币)
  - [试用期、集群检测、时间线与学习](#试用期集群检测时间线与学习)
  - [消息构建器与更新](#消息构建器与更新)
  - [运行](#运行)
  - [运维](#运维-1)
- [消息占位符](#消息占位符)
- [配置](#配置)
- [数据与存储](#数据与存储)
- [仓库结构](#仓库结构)
- [翻译](#翻译)
- [路线图](#路线图)
- [隐私与安全](#隐私与安全)
- [支持](#支持)
- [致谢](#致谢)
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
- 古拉格频道：发布诈骗链接或图片的成员会被移入唯一的频道，并看到账号安全指引。管理员也可以使用 /moderation jail 和 /moderation unjail。
- 通过按钮或验证码验证，并自动移除未及时验证的成员。
- 防破坏还会监控权限授予、新建 Webhook、被添加的机器人以及服务器改名。
- 反诈骗：虚假抽奖和加密货币骗局会在几毫秒内从文字和图片中删除，包括任何拼写的 MrBeast 骗局。

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
- 带商店的经济系统、按钮或下拉式身份组菜单、定时消息、YouTube、Twitch 和 RSS 订阅源、活跃度统计以及引导式 /admin setup。给成员看的消息支持 12 种语言。

### 运维

- 每个模块和每个命令都可以按服务器开启或关闭。
- 自定义前缀、命令别名和可重命名的命令。
- 身份组和频道结构的备份与恢复。
- 按计划自动备份身份组、频道、表情和 Webhook，并提供只补充缺失内容的恢复命令。
- 控制面板：用 Discord 登录后在浏览器中修改每个服务器的设置，仅限管理该服务器的成员，且仅在机器人已连接时可用。

## 项目状态

GuardBot 还很年轻，尚未在大型服务器上使用过。自动化测试（`python -m unittest`）覆盖存储、个人信息检测、等级计算、命令注册、权限检查以及文档链接。所有需要真实 Discord 服务器的功能，例如锁定、备份恢复、验证、防破坏和古拉格，都不在测试范围内。请先在测试服务器上试用这些功能，再依赖它们。文档的翻译尚未由母语者审阅，欢迎提出修改意见。

## 运行要求

- Python 3.11 或更高版本
- 带有机器人令牌的 Discord 应用
- 一台持续在线的电脑或 VPS
- ffmpeg（仅音乐模块需要）
- tesseract-ocr（可选，仅用于读取图片中的文字）

## 快速开始

请选择你的系统。每种方式都需要 Python 3.11 或更新版本以及你的机器人令牌。详细的分步指南见 [GUIDE.md](GUIDE.md)。

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

### 启动脚本与开机自启

启动脚本会创建虚拟环境、安装依赖并启动机器人。首次运行时它们会创建 .env 文件并停止，方便你填入令牌。之后再运行一次即可。

```bash
./start.sh
```

```bat
start.bat
```

要让机器人在电脑重启后继续运行，请使用服务。Linux（systemd）和 macOS（launchd）：

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

在 Windows 上，请在任务计划程序中创建一个登录时运行 start.bat 的任务，或使用 NSSM 之类的服务封装工具。Docker 请见 [GUIDE.md](GUIDE.md)。

### 更新

停止机器人，运行以下命令后重新启动。data 文件夹中的数据不会被改动，机器人在每次数据格式变更前都会备份数据库。

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

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

### 结构、成员与团队

1.5 版新增了用于搭建并保持服务器整洁、恢复回归成员以及管理版主团队的命令。每个部分都有模块开关(`/admin module`)、独立设置,并在控制面板中有对应位置。

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

- 使用 `/structure` 创建、克隆、重命名和排序频道与分类,并复制另一个频道的权限。不活跃的频道会被报告,或移到归档分类(`/structure archive`)。身份组可以限时授予并保存为模板;模板不会授予执行者自己没有的权限。
- `/structure rules` 发布带有接受按钮和版本号的规则。执行 `post new_version:True` 后,未接受新版本的成员会收到一次私信提醒。
- `/members stickyroles` 在成员回归时归还身份组并恢复禁言或超时。`/members nickname` 清除会让名字排到列表顶部的字符,检查昵称和用户名中的禁用词,并为违规者改名。观察名单是静默的:名单中的用户发出第一条消息时,团队会收到提醒。
- 四眼审批(`/security approval`)让封禁、踢出、超时和批量操作只在第二位版主同意后才执行。`/moderation case undo` 撤销一个案件,包括由它引起的后续操作(例如一次禁言和随后的封禁)。警告可以在若干天后失效(`/moderation escalation expiry`)。
- `/admin history` 显示谁在何时更改了哪项设置,并可回滚某个部分。操作者姓名是根据服务器上最近的命令和控制面板更改推测的。`/admin history copy` 把部分设置复制到你可用机器人管理的另一个服务器,默认先试运行。`/admin exceptions` 让频道和身份组不受 AutoMod 规则与反诈骗的影响。`/admin dashaccess` 为身份组授予控制面板的只读或版主权限。
- `/team` 显示每位版主的工作(案件、工单、举报、响应时间、不活跃成员),发送每周报告(日期和时间为 UTC),让版主用 `/team duty away` 报备离开,使工单和提及转给其他人,并通过表单和团队投票处理管理员申请。
- Discord 无法对个别成员隐藏分组内的命令,但机器人仍会检查每一次调用。团队统计的数字从更新当天开始计算,更早的操作不包含在内。

## 控制面板

控制面板是运行在机器人内部的网页。用 Discord 登录后，你可以用开关、菜单和输入框代替命令来修改服务器的设置：模块、频道、身份组、阈值、文本、前缀和语言。它还会显示最近的管理案件，并可导出和导入设置。它在你自己的电脑和 VPS 上的使用方式完全相同，在你开启之前处于关闭状态。

### 设置控制面板

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

### 安全

- 只能通过 Discord 登录（OAuth2，范围 identify）。访问令牌会立即被撤销，从不保存。
- 只有服务器所有者以及拥有“管理员”或“管理服务器”权限的成员可以访问，而且只能访问该服务器。每次请求都会重新检查权限。
- 只能打开机器人当前已连接的服务器。如果机器人离线、不在该服务器或仍在启动，控制面板会拒绝一切请求。它运行在机器人内部，没有独立的数据库或服务。
- 默认只监听 127.0.0.1，网络中的其他人无法访问。公开地址只有在使用 HTTPS 时才会被接受，否则控制面板不会启动。
- 会话使用 HttpOnly Cookie 中的随机令牌，带 SameSite，在 HTTPS 下还使用 __Host- 前缀。会话 8 小时后失效，只保存在内存中，因此重启会让所有人退出登录。
- 每次修改都需要 CSRF 令牌和匹配的 Origin。Host 头会被检查以防止 DNS 重绑定。页面不加载任何外部脚本，严格的内容安全策略会阻止内联代码，请求有频率限制，请求体限制为 256 KB。
- 每个值都会按设置的类型检查，Discord ID 必须存在于该服务器。计数器、工单和已保存条目等内部状态无法编辑。每次修改都会写入该服务器的安全日志频道。
- 从不显示消息内容。管理案件为只读。

### 在 VPS 上使用控制面板

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

编辑器会显示所有属于开关、数字、文本、频道、身份组或简单列表的设置。通过命令创建的内容，如商店物品、身份组菜单、订阅源、标签和工单，仍然使用命令。页面提供英语和德语，并跟随浏览器语言。在 Docker 中，只把端口发布到 127.0.0.1（127.0.0.1:8080:8080），并在容器内把 host 设为 0.0.0.0、allow_insecure_http 设为 true。

## 命令

大多数命令是斜杠命令，管理命令也支持前缀。完整列表见命令参考： [COMMANDS.md](../COMMANDS.md).

<!-- groups -->
### 命令分组

为了节省斜杠命令的名额(Discord 限制每个机器人最多 100 个顶层命令),相关命令已被分组。先输入分组,再输入命令,例如 `/moderation ban`。带前缀的文本命令(例如 `!ban`)不受影响。权限、别名和模块开关仍然使用原来的简单命令名。

| 分组 | 包含 |
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

### 管理

警告、禁言、踢出和封禁既可作为斜杠命令使用，也可用前缀，例如 `!warn @User spam`。每个操作都会生成一个带编号的记录。

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

### 古拉格（关押）

账号被盗的成员会被移到唯一的频道，并看到安全指引。释放时会恢复他们原来的身份组。

```
/access jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/access jailsetup apply                                   # apply the channel permissions again
/access jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/access jailsetup preview

/moderation jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/moderation jail member:@User duration:2h                     # released automatically after 2 hours
/moderation unjail member:@User reason:Account secured
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

### 防破坏

监控审计日志，在有人破坏服务器时作出反应。服务器所有者会收到私信。

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

### 验证

新成员在点击按钮或完成验证码之前，只能看到验证频道。

```
/access verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/access verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/access verify panel channel:#verify                      # post the button again
/access verify apply                                      # apply the channel permissions again
/access verify member member:@User                        # verify someone manually
/access verify off
```

### 日志

为每个类别选择一个频道，或用一个主频道记录全部内容。

```
/server log set category:main channel:#logs               # fallback for every category
/server log set category:messages channel:#log-messages
/server log set category:moderation channel:#log-moderation
/server log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/server log sent enabled:False                            # stop logging every sent message
/server log show
```

### 欢迎、告别与助力者

消息、自动身份组以及服务器助力者奖励。

```
/community welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/community welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/community welcome autorole role:@Member                     # toggle, given to every new member
/community welcome botrole role:@Bots                        # toggle, given to every new bot
/community welcome test

/community booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/community booster role role:@Booster                        # toggle
```

### 工单

成员通过按钮打开私密频道。关闭工单时会发送聊天记录。

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

### 投票与抽奖

用按钮投票和参与。时长支持 30m、2h、1d 等写法。

```
/engage poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/engage poll end poll_id:3
/engage poll list

/engage giveaway start prize:Nitro duration:2d winners:2 role:@Member
/engage giveaway end giveaway_id:1
/engage giveaway reroll giveaway_id:1
/engage giveaway list
```

### 建议与星标板

成员发布建议，管理团队可以批准或拒绝，热门消息会被突出显示。

```
/suggestion setup set channel:#suggestions review_role:@Staff
/support suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/engage starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/engage starboard ignore channel:#spam
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

### 反应身份组与通知

用任意表情通过反应发放身份组，并让成员自己选择通知主题。

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

### 生日

成员保存日期和月份，机器人当天发放身份组并发送消息。

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### 临时语音频道

加入中心频道会创建一个房间，房间空了就会消失。

```
/community tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### 备份与恢复

备份包含身份组、频道、表情、Webhook 和成员身份组。恢复只补充缺失的内容。

```
/server backup create name:before-update
/server backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/server backup list
/server backup download name:before-update
/server backup restore name:before-update member_roles:True   # only adds what is missing
/server backup delete name:before-update
```

### 数据与隐私

成员可以导出和删除自己的数据。管理员控制数据保留多久。

```
/info mydata export                                     # members download their own data
/info mydata delete confirm:True                        # members delete their XP and birthday

/server privacy retention days:90                         # delete data of members who left after 90 days
/server privacy export user_id:123456789012345678
/server privacy delete user_id:123456789012345678 cases:True
```

### 管理员工具

清理频道、管理身份组并记录私人备注。每个操作都会写入日志。

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

### 信息查询

查询用户、服务器、身份组和机器人的信息。

```
/info userinfo user:@User
/server serverinfo
/server roleinfo role:@Moderator
/info avatar user:@User
/help command:ban                                  # explains one command
/info ping
/info botinfo
```

### 公告、标签与提醒

以机器人的名义发消息，创建自定义命令，自动回复消息并设置提醒。

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

### 私信邮箱与封禁申诉

成员通过服务器内的私密频道联系管理组，无需给机器人发送私信。

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

### 计数频道、置底消息与统计

计数游戏、始终显示在频道底部的消息，以及显示实时数字的频道。

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

### 现有功能的更多选项

对工单、抽奖、语音房间、经验、生日、备份、日志和状态视图的补充。

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

### 更多 AutoMod 工具

跟踪短链接，限制新成员发链接，发现幽灵提及，并在不处罚任何人的情况下测试规则。

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

### 管理员限额与权限审计

当管理员封禁或踢出过多时发出警报，并列出拥有危险权限的身份组。

```
/team modwatch status
/team modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/team modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/team modwatch exclude member:@TrustedMod

/team permaudit run                                                  # roles with dangerous permissions and who holds them
/team permaudit watch enabled:True                                   # alarm when a role or member gets one
/team permaudit trust role:@Admin
```

### 举报与邀请追踪

成员向管理组举报消息，机器人记录每位新成员是通过哪个邀请加入的。

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

### 诊断与调试

找出缺失的权限和损坏的设置，在频道中接收错误报告，并导出或导入设置。

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

### 音乐

在语音频道播放链接和 music 文件夹中的文件。下载内容保存为 music/艺术家/专辑/曲目。需要 ffmpeg 和 requirements.txt 中的依赖包。

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

/music settings dj_role:@DJ volume:50 max_queue:100 per_user:25 max_minutes:60 idle_leave:120
/music settings allow_links:True allow_search:True allow_playlists:True library:True
/music settings allow_download:True download_format:best announce:True
/admin config set path:music.allowed_hosts value:bandcamp.com,archive.org
/music cleardj
/music status
```

无损：您自己添加的文件（FLAC、WAV、ALAC）以及提供 FLAC 的来源会原样播放。YouTube、SoundCloud 等网站只提供有损音频，事后无法变成无损。Discord 以 Opus 传输语音，机器人使用语音频道的比特率。责任：下载和播放内容可能违反网站的服务条款或著作权法。下载默认关闭，模块在您启用之前也是关闭的。机器人的运营者对播放和保存的内容负责。

### 设置与健康检查

引导式助手通过按钮和菜单完成最重要的设置：日志频道、欢迎频道、管理组身份组、古拉格、AutoMod 预设（宽松、普通、严格）、服务器模板（社区、游戏、支持）以及语言。/server health 会显示哪些已设置、哪些还没有。语言会改变成员看到的文字，例如默认欢迎消息、AutoMod 提示、验证、工单、申诉、私信管理邮箱和身份组菜单。给管理员的固定回复已翻译，带名称和数字的回复仍为英文。

```
/admin setup                                                         # buttons and menus, nothing is switched off by a template
/server health                                                        # what is set up, what is open, and the self-test
/admin language code:de
```

### 经济

服务器货币，包含每日奖励、打工、转账、排行榜，以及可以赠送身份组的商店。通过 economy 模块开启。命令也可以使用前缀，例如 !economy daily。

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

### 身份组菜单、定时消息与订阅源

身份组菜单通过按钮或下拉菜单发放身份组。定时消息可发送一次，或每小时、每天、每周重复。订阅源会发布 YouTube 新视频、Twitch 直播和 RSS 条目。YouTube 请使用频道 ID（以 UC 开头）。Twitch 需要在 .env 中设置 TWITCH_CLIENT_ID 和 TWITCH_CLIENT_SECRET。时间可写作 in 2h、18:30，或带时间的日期，如 2026-12-24 18:00，按服务器时区计算。订阅源第一次检查只会记住已有内容。

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

### 活跃度、批量操作与案件搜索

活跃度按频道统计消息数、按天统计加入和离开人数，从不记录内容或名字。批量操作在确认后可封禁、踢出或禁言最多 25 名用户。案件可按用户、类型、名称、原因、管理员和时间搜索，并可相互关联，例如把一条备注关联到一次封禁。

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

### 反诈骗与反加密货币

在几毫秒内删除文字和图片中的虚假抽奖，例如典型的 MrBeast 骗局。即时名单中的名字无论怎样拼写都会立即删除（MrBeast、Mr Beast、M R B E A S T、Mr.B3ast）。否则名单中的词（名字、诱饵、加密货币、链接、金额）会累计分数，达到阈值就删除消息。图片通过 OCR 读取，被判定为骗局的图片以后无需再次识别即可删除。读取图片需要 tesseract，没有它只检查文字。关于 MrBeast 的服务器可以把该名字从即时名单中移除，或用 /automod exemptchannel 排除频道。使用前请先用 /security antiscam test 试一试。

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

### 试用期、集群检测、时间线与学习

试用期会把新成员放入一个身份组。在他们发送设定数量的正常消息或设定的分钟数过去之前，链接、邀请和文件会被删除并附上简短提示。突袭防护还能识别集群：多个名称模式相同、头像相同或创建时间只相差几分钟的新账号。时间线（/moderation case timeline）按时间顺序汇总某个用户的账号创建、加入与邀请、试用期、案件和申诉。消息从不被保存，所以不包含在内。/security block、/security unblock 和 /security blocklist 用简短命令管理 AutoMod 的屏蔽列表。管理员可以用消息上的上下文菜单项 Mark as scam，或用 learn_emoji 设定的表情回应来训练反诈骗模块：消息会被删除，其图片和文字此后会被立即删除。每个部分都可以通过对应的模块或设置关闭。

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

### 消息构建器与更新

消息构建器可以根据 JSON 发布包含多个嵌入和链接按钮的消息。它读取 Embed Generator 等嵌入生成器导出的 JSON，所以你可以在那里设计消息，再用机器人发布。JSON 可以作为文本、.json 文件，或直接指向 JSON 的 https 链接提供，例如仓库的原始文件（会重定向的链接会被拒绝）。只会创建链接按钮，需要交互的按钮会被跳过。每个链接都必须是 http 或 https，文本中的提及不会通知任何人，并且遵守 Discord 的限制。/post message copy 把已有消息导出为 JSON，/post message edit 修改机器人发布的消息，/post message preview 只向你显示结果。网页编辑器的分享链接不会被打开，因为它们的格式并不公开。

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

机器人每 12 小时检查 update.repo（由 scripts/set_repo_url.py 设置）所指的 GitHub 仓库是否有更新的版本。如果有，机器人所有者会收到包含发布说明的私信，并下载和检查该版本：发布的 SHA-256 校验和、压缩包内的安全路径，以及与标签一致的版本号。用 /server debug update action:install 安装，开启 auto_install 时则自动安装。安装前，被替换的文件会保存到 data/update，新依赖会被安装，新代码会先试导入。任何一步失败，旧文件都会恢复。你的 .env、settings.json、data 和 music 永远不会被改动。之后机器人会自行重启。在 Docker 中不会原地安装，请改为更新镜像。更新会运行仓库中的代码，所以只应指向你信任的仓库。把 enabled 设为 false 即可关闭。

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

### 运行

机器人每隔几秒保存一次数据，并在 data/dbbackups 中保留数据库备份：每次数据格式变更前一份，每天一份。音乐队列、置顶消息和管理员计数在重启后仍然保留。大型机器人可以在多个分片上运行。心跳文件和可选的状态页面有助于监控工具。这些选项在 settings.json 中设置：

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

日志写入 data/guardbot.log(带轮转,见 log_max_mb 和 log_backups)。将 log_format 设为 json 后,每行是一个包含服务器和命令的 JSON 对象。设置 health_port 后,/metrics 提供 Prometheus 指标(运行时间、延迟、内存、数据库大小、错误、命令使用次数和耗时、工作通道)。只导出数字,从不导出名称或 ID,并且 metrics_token 会要求使用 bearer 令牌。繁重的工作(读取图片、绘制卡片、音乐文件、备份)在线程数固定且有上限的通道中运行(settings.json 中的 workers)。通道已满时,机器人会提示正忙,而不是堆积任务。每个数据库备份在创建后立即被打开并检查。要恢复备份,请先停止机器人,然后运行:

```
python scripts/restore_db.py data/dbbackups/guardbot-YYYYMMDD-HHMMSS-auto.db
python scripts/restore_db.py BACKUPFILE --check          # only check a backup
```

当前数据库会保留为名为 before-restore 的备份。

### 运维

开启或关闭模块和命令、更改前缀、设置别名，并把命令限制给指定身份组。

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

## 消息占位符

这些占位符会在你设置的文本中被替换：

```
/community welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/community booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/community tempvoice setup     name                            {name}
/access jailsetup notice    text                            {staff}
```

## 配置

全局选项在 settings.json 中设置。其余内容按服务器通过 /admin module、/admin command、/admin perms、/admin alias 和 /admin config 等命令配置。

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

每一项设置都可以用 /admin config 读取和修改。以下是最常用的路径：

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
    defaults/             default settings, one file per area (core, security, moderation, community) and base.py for modules and permissions
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature, in the folders security, moderation, server, community, tools
  docs/                   documentation in 12 languages, COMMANDS.md, PRIVACY.md
  deploy/                 systemd service, Dockerfile, compose file
  scripts/                maintenance scripts
  tests/                  automated tests (python -m unittest)
  data/                   created at runtime, holds your settings and data
```

## 翻译

英语是本项目的原始语言。文档、控制面板和机器人消息的所有翻译都是机器翻译，没有经过母语者校对。可能会有生硬的措辞和错误，欢迎反馈或提交修正。相关文件位于 docs/ 和 guardbot/locales/。

## 路线图

- 控制面板中的活动与管理图表。
- 由母语者校对所有翻译。
- 翻译更多固定回复文本。

## 隐私与安全

- 没有遥测。机器人与 Discord 通信，并为检查更新与 GitHub 通信（不发送任何个人数据，可用 update.enabled 关闭）。管理员提供的链接，如订阅源、音乐和 JSON 链接，只在请求时才会打开。
- 所有数据都保存在你电脑的 data 文件夹中：设置、经验、生日（仅日期和月份）以及管理记录。
- 机器人会忽略成员发来的私信。
- 令牌从 .env 文件读取。切勿分享或上传。
- 成员可以用 /info mydata 导出并删除自己的数据。管理员可设置已离开成员的数据保留多久。
- [PRIVACY.md](../PRIVACY.md)

## 支持

错误、想法和建议：请在 Discord 上联系我，@justyyin，或在 GitHub 上提交 issue。

## 致谢

GuardBot 的灵感来自 Merlin Fuchs 的 [Embed Generator](https://github.com/merlinfuchs/embed-generator)（MIT 许可证，托管于 message.style）。消息构建器读取相同的 JSON 格式，因此在那里设计的消息可以用本机器人发布。本项目不包含该项目的任何代码。感谢 discord.py、aiohttp、Pillow、yt-dlp、mutagen 和 Tesseract 的作者。

## 许可证

基于 MIT 许可证发布。参见 [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
