# GuardBot: 설치 가이드

이 가이드는 내 컴퓨터나 VPS에서 GuardBot을 실행하는 방법을 설명합니다. 약 15분이 걸립니다.

<!-- toc -->

- [Discord 봇 만들기](#discord-봇-만들기)
- [내 컴퓨터에서 실행하기](#내-컴퓨터에서-실행하기)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux 및 macOS](#linux-및-macos)
- [VPS에서 실행하기](#vps에서-실행하기)
- [Docker로 실행하기](#docker로-실행하기)
- [Discord에서의 첫 단계](#discord에서의-첫-단계)
- [업데이트와 백업](#업데이트와-백업)
- [문제 해결](#문제-해결)
- [지원](#지원)

<!-- tocstop -->

## Discord 봇 만들기

1. [Discord Developer Portal](https://discord.com/developers/applications)을 열고 New Application을 클릭합니다.
2. Bot 탭을 열고 Reset Token을 클릭합니다. 토큰을 복사하고 비밀로 유지하세요.
3. 같은 탭에서 Server Members Intent와 Message Content Intent를 켭니다.
4. OAuth2의 URL Generator를 열고 scope로 bot과 applications.commands를 선택합니다.
5. 권한을 선택합니다: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, View Audit Log, Manage Messages, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Move Members. Administrator도 동작하며 가장 간단한 선택입니다.
6. 생성된 URL을 열고 봇을 서버에 추가합니다.
7. 서버 설정에서 봇의 역할을 역할 목록 맨 위로 옮깁니다. 봇은 자신의 역할보다 아래에 있는 역할만 관리할 수 있습니다.

다음 초대 URL을 사용할 수도 있습니다. YOUR_CLIENT_ID를 Developer Portal의 Application ID로 바꾸세요:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## 내 컴퓨터에서 실행하기

Python 3.11 이상과 Git을 설치한 뒤 터미널에서 다음 명령을 실행합니다.

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

### Linux 및 macOS

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

.env 파일을 열고 자리표시자를 봇 토큰으로 바꿉니다. 콘솔에 online as로 시작하는 줄이 나타나면 봇이 온라인 상태입니다. 창을 닫으면 봇도 멈추므로 열어 두세요.

## VPS에서 실행하기

다음 명령은 Ubuntu 또는 Debian용이며, 봇을 자동으로 시작되는 서비스로 설정합니다.

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

상태는 systemctl status guardbot으로 확인합니다. 봇이 준비되면 로그에 online as로 시작하는 줄이 나타납니다.

## Docker로 실행하기

Docker는 선택 사항입니다. 먼저 .env 파일을 만든 다음 실행합니다:

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## Discord에서의 첫 단계

서버에서 다음 명령어를 사용하고 채널 이름을 내 채널로 바꾸세요.

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

모든 기능은 명령어 참조에 설명되어 있습니다: [COMMANDS.md](../COMMANDS.md).

## 업데이트와 백업

봇 업데이트:

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

data 폴더를 복사해 설정을 백업합니다. 예:

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## 문제 해결

- 슬래시 명령어가 보이지 않음: 몇 분 기다린 뒤 Discord를 다시 시작하고, 봇을 applications.commands scope로 초대했는지 확인하세요.
- 권한 있는 Intent 오류로 봇이 멈춤: Developer Portal에서 Server Members Intent와 Message Content Intent를 켜세요.
- Improper token: 토큰을 다시 복사하고 .env에 DISCORD_TOKEN=토큰 만 있고 공백이나 따옴표가 없는지 확인하세요.
- I cannot assign that role: 봇의 역할을 관리해야 할 역할보다 위로 옮기세요.
- 아무것도 기록되지 않음: /log set으로 채널을 지정하고, 봇이 그 채널에서 메시지 전송, 링크 삽입, 파일 첨부를 할 수 있는지 확인하세요.
- Unknown timezone: pip install tzdata를 실행하고 봇을 다시 시작하세요.

## 지원

버그, 아이디어, 제안: Discord @justyyin 또는 GitHub issue.

Copyright (c) Justyn - made in Germany

<!-- GuardBot (c) Justyn -->
