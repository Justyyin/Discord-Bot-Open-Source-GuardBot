# GuardBot: 설치 가이드

이 가이드는 내 컴퓨터나 VPS에서 GuardBot을 실행하는 방법을 설명합니다. 약 15분이 걸립니다.

> 베타: GuardBot과 대시보드는 베타 단계입니다. 충분히 테스트되지 않았으며, 특히 대형 서버나 Discord의 모든 상황에서는 확인하지 않았습니다. 오류가 있을 수 있으니 data 폴더를 백업하고 문제를 알려 주세요. 사용에 따른 책임은 본인에게 있습니다.

<!-- toc -->

- [Discord 봇 만들기](#discord-봇-만들기)
- [내 컴퓨터에서 실행하기](#내-컴퓨터에서-실행하기)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux 및 macOS](#linux-및-macos)
- [VPS에서 실행하기](#vps에서-실행하기)
- [Docker로 실행하기](#docker로-실행하기)
- [Discord에서의 첫 단계](#discord에서의-첫-단계)
- [구조, 팀, 개요(1.5)](#구조-팀-개요15)
- [업데이트와 백업](#업데이트와-백업)
- [음악 (선택)](#음악-선택)
- [선택: 이미지 읽기와 언어](#선택-이미지-읽기와-언어)
- [대시보드](#대시보드)
- [스킬, AI와 봇 프로필(선택)](#스킬-ai와-봇-프로필선택)
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
git clone <REPOSITORY_URL>
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
git clone <REPOSITORY_URL>
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

모든 기능은 명령어 참조에 설명되어 있습니다: [COMMANDS.md](../COMMANDS.md).

## 구조, 팀, 개요(1.5)

이 단계로 새로운 기능을 설정합니다. 각 기능은 /admin module 로 끌 수 있고, 접두사와 문구는 서버별로 계속 수정할 수 있습니다.

1. 설정 상태 보기: `/admin module overview` 는 각 모듈의 상태와 설정 여부를 보여 줍니다. 대시보드의 설정 패널에도 같은 내용이 나옵니다.
2. 명령 찾기: `/info find text:ban` 은 단어로 모든 명령을 검색하고, `/help` 는 그룹을 보여 줍니다.
3. 동의 버튼이 있는 규칙 게시: `/structure rules setup`, `/structure rules add`, `/structure rules post` 순서로 실행합니다. 새 버전에 동의하지 않은 멤버에게는 몇 시간마다 알림이 갑니다.
4. 봇에게 누가 스태프인지 알려 주기: `/team duty roster`. 근무 가능한 스태프 목록과 티켓·경고 전달에 사용됩니다.
5. 사용하지 않는 채널 정리: `/structure archive setup` 후 `/structure archive scan`.
6. 돌아온 멤버에게 역할 돌려주기: `/members stickyroles setup`.
7. 이름을 읽기 쉽게 유지: `/members nickname setup`, `/members nickname scan` 전에 `/members nickname check` 로 시험해 보세요.
8. 큰 변경 전에 `/admin config export` 로 설정을 내보내고 `/server diagnose` 로 역할과 채널을 확인하세요.

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

## 음악 (선택)

음악 모듈은 봇을 실행하는 컴퓨터에 ffmpeg가 필요합니다. 내 음악을 music/ 폴더에 아티스트/앨범/01 - 제목.flac 형태로 넣거나 다운로드를 허용하세요. 폴더가 커질 수 있으니 여유 공간이 있는 디스크나 Docker 볼륨에 두세요.

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

Guard Music: 24시간 음성 채널에 머물 수 있는 별도의 봇으로 음악을 실행하려면 Discord Developer Portal에서 두 번째 애플리케이션을 만들고, 그 토큰을 .env에 MUSIC_TOKEN으로 적고, settings.json에서 music_bot.enabled를 true로 설정합니다. 다시 시작하면 대시보드의 음악 페이지에 Guard Music을 서버에 추가하는 버튼이 나타납니다. Spotify, Apple Music, Tidal 링크는 YouTube 또는 SoundCloud로 재생됩니다. Tidal 앨범과 재생목록에는 .env의 TIDAL_CLIENT_ID와 TIDAL_CLIENT_SECRET도 필요합니다. 사용에 따른 책임은 본인에게 있으며, README의 음악 섹션을 참고하세요.

## 선택: 이미지 읽기와 언어

사기 방지 모듈이 이미지 속 글자를 읽게 하려면 봇을 실행하는 컴퓨터에 tesseract를 설치하세요(Docker 이미지에는 이미 들어 있습니다). 그런 다음 /security antiscam status로 준비되었는지 확인합니다. 멤버에게 보이는 메시지의 언어는 /admin language로 고릅니다.

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

## 대시보드

대시보드는 봇 안에서 동작하는 웹 페이지입니다. Discord로 로그인하면 명령어 대신 스위치, 메뉴, 입력란으로 서버 설정을 바꿀 수 있습니다. 모듈, 채널, 역할, 기준값, 텍스트, 접두사, 언어가 대상입니다. 최근 관리 케이스를 보여 주고, 설정을 내보내고 가져올 수도 있습니다. 내 컴퓨터에서도 VPS에서도 똑같이 동작하며, 켜기 전에는 꺼져 있습니다.

1. Developer Portal에서 애플리케이션을 열고 OAuth2로 이동해 Client Secret을 .env 파일에 복사합니다.
2. 같은 페이지에서 리디렉션 주소 http://localhost:8080/callback 을 추가합니다.
3. settings.json에서 대시보드를 켭니다.
4. 봇을 다시 시작하고 브라우저에서 http://localhost:8080 을 열어 Discord로 로그인합니다.

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

host는 127.0.0.1로 두고 두 가지 방법 중 하나를 고르세요. 첫째는 SSH 터널입니다. 아무것도 공개하지 않고, 터널이 켜져 있는 동안 내 컴퓨터에서 http://localhost:8080 을 엽니다.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

둘째는 Caddy 같은 리버스 프록시를 통한 HTTPS입니다. 인증서는 알아서 발급받습니다(deploy/Caddyfile.example 참고). 그런 다음 public_url을 https 주소로 설정하고, Developer Portal에 https://내-주소/callback 을 리디렉션으로 추가하고, trust_proxy를 true로 설정하세요:

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

## 스킬, AI와 봇 프로필(선택)

스킬에는 봇만 있으면 됩니다. `/support skill create`로 시작하세요. AI를 쓰려면 Anthropic, OpenAI 또는 Kimi(Moonshot)의 계정과 API 키가 필요합니다. `/support ai setup`을 실행하고 비공개 입력창에 키를 붙여 넣으세요. `data/ai.secret` 파일을 백업과 함께 보관하세요. 봇의 이름, 이미지, 배너는 대시보드의 봇 프로필에서 바꿀 수 있습니다. 모든 곳에서 바꾸려면 본인의 Discord ID를 `settings.json`의 `owner_ids`에 추가하세요(또는 애플리케이션의 소유자가 되세요). 자세한 내용은 README의 스킬과 AI 항목에 있습니다.

## 문제 해결

- 슬래시 명령어가 보이지 않음: 몇 분 기다린 뒤 Discord를 다시 시작하고, 봇을 applications.commands scope로 초대했는지 확인하세요.
- 권한 있는 Intent 오류로 봇이 멈춤: Developer Portal에서 Server Members Intent와 Message Content Intent를 켜세요.
- Improper token: 토큰을 다시 복사하고 .env에 DISCORD_TOKEN=토큰 만 있고 공백이나 따옴표가 없는지 확인하세요.
- I cannot assign that role: 봇의 역할을 관리해야 할 역할보다 위로 옮기세요.
- 아무것도 기록되지 않음: /server log set으로 채널을 지정하고, 봇이 그 채널에서 메시지 전송, 링크 삽입, 파일 첨부를 할 수 있는지 확인하세요.
- Unknown timezone: pip install tzdata를 실행하고 봇을 다시 시작하세요.
- 이유 없이 실패하는 경우: 오류와 경고는 콘솔에 출력됩니다. VPS에서는 journalctl -u guardbot -f 로 확인하세요.

## 지원

버그, 아이디어, 제안: Discord @justyyin 또는 GitHub issue.

Copyright (c) Justyn - made in Germany
