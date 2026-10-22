# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | **한국어**

관리, 보안, 커뮤니티를 위한 자체 호스팅 Discord 봇. 오픈 소스이며 무료이고, 데이터는 내 컴퓨터에만 남습니다.

> 베타: GuardBot과 대시보드는 베타 단계입니다. 충분히 테스트되지 않았으며, 특히 대형 서버나 Discord의 모든 상황에서는 확인하지 않았습니다. 오류가 있을 수 있으니 data 폴더를 백업하고 문제를 알려 주세요. 사용에 따른 책임은 본인에게 있습니다.

<!-- toc -->

- [프로젝트 소개](#프로젝트-소개)
- [기능](#기능)
  - [보안](#보안)
  - [관리](#관리)
  - [로그](#로그)
  - [커뮤니티](#커뮤니티)
  - [수습 기간, 무리 탐지, 타임라인, 학습](#수습-기간-무리-탐지-타임라인-학습)
  - [메시지 빌더와 업데이트](#메시지-빌더와-업데이트)
  - [운영](#운영)
- [프로젝트 상태](#프로젝트-상태)
- [요구 사항](#요구-사항)
- [빠른 시작](#빠른-시작)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [시작 스크립트와 자동 실행](#시작-스크립트와-자동-실행)
  - [업데이트](#업데이트)
- [봇 권한](#봇-권한)
- [Discord에서의 첫 단계](#discord에서의-첫-단계)
- [대시보드](#대시보드)
  - [대시보드 설정](#대시보드-설정)
  - [보안](#보안-1)
  - [VPS에서 대시보드 사용](#vps에서-대시보드-사용)
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
  - [관리자 도구](#관리자-도구)
  - [정보](#정보)
  - [공지, 태그, 알림](#공지-태그-알림)
  - [모드메일과 차단 이의 신청](#모드메일과-차단-이의-신청)
  - [카운팅 채널, 고정 메시지, 통계](#카운팅-채널-고정-메시지-통계)
  - [기존 기능의 추가 옵션](#기존-기능의-추가-옵션)
  - [추가 AutoMod 도구](#추가-automod-도구)
  - [관리자 한도와 권한 감사](#관리자-한도와-권한-감사)
  - [신고와 초대 추적](#신고와-초대-추적)
  - [진단과 디버깅](#진단과-디버깅)
  - [음악](#음악)
  - [설정과 상태 점검](#설정과-상태-점검)
  - [경제](#경제)
  - [역할 메뉴, 예약 메시지, 피드](#역할-메뉴-예약-메시지-피드)
  - [활동, 일괄 작업, 케이스 검색](#활동-일괄-작업-케이스-검색)
  - [사기 방지 및 암호화폐 방지](#사기-방지-및-암호화폐-방지)
  - [운영](#운영-1)
  - [운영](#운영-2)
- [메시지 자리표시자](#메시지-자리표시자)
- [설정](#설정)
- [데이터와 저장 위치](#데이터와-저장-위치)
- [저장소 구조](#저장소-구조)
- [번역](#번역)
- [로드맵](#로드맵)
- [개인정보 및 보안](#개인정보-및-보안)
- [지원](#지원)
- [크레딧](#크레딧)
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
- 사기 방지: 가짜 경품과 암호화폐 사기를 텍스트와 이미지에서 몇 밀리초 안에 삭제하며, 어떤 철자의 MrBeast 사기도 포함합니다.

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
- 상점이 있는 경제, 버튼 또는 드롭다운 역할 메뉴, 예약 메시지, YouTube·Twitch·RSS 피드, 활동 통계, 안내형 /setup. 멤버에게 보이는 메시지는 12개 언어로 제공됩니다.

### 수습 기간, 무리 탐지, 타임라인, 학습

수습 기간은 새 멤버를 하나의 역할에 넣습니다. 설정한 수의 일반 메시지를 쓰거나 설정한 분이 지나기 전까지 링크, 초대, 파일은 짧은 안내와 함께 삭제됩니다. 레이드 방어는 무리도 알아봅니다. 이름 패턴이 같거나, 프로필 사진이 같거나, 몇 분 안에 만들어진 새 계정이 여럿인 경우입니다. 타임라인(/case timeline)은 한 사용자의 계정 생성, 가입과 초대, 수습 기간, 케이스, 이의 신청을 시간순으로 모아 보여 줍니다. 메시지는 저장되지 않으므로 포함되지 않습니다. /block, /unblock, /blocklist는 짧은 명령어로 AutoMod 차단 목록을 관리합니다. 운영진은 메시지의 컨텍스트 메뉴 항목 Mark as scam 또는 learn_emoji로 정한 이모지 반응으로 사기 방지 모듈을 학습시킬 수 있습니다. 메시지는 삭제되고, 그 이미지와 텍스트는 이후 즉시 삭제됩니다. 각 기능은 해당 모듈이나 설정에서 끌 수 있습니다.

```
/module enable name:probation
/probation setup minutes:10 messages:1 block_links:True block_files:True
/probation status
/probation release member:@User
/probation add member:@User

/raid swarm enabled:True minimum:4 minutes:10
/case timeline user:@User

/block kind:link value:evil.example
/blocklist
/unblock kind:link number:1
/antiscam set learn_emoji:X
```
- 대시보드: Discord로 로그인한 뒤 브라우저에서 각 서버의 설정을 바꿉니다. 서버를 관리하는 멤버만, 봇이 연결되어 있는 동안에만 사용할 수 있습니다.

### 메시지 빌더와 업데이트

메시지 빌더는 JSON으로 여러 임베드와 링크 버튼이 있는 메시지를 게시합니다. Embed Generator 같은 임베드 생성기가 내보내는 JSON을 읽으므로, 그곳에서 메시지를 디자인하고 봇으로 게시할 수 있습니다. JSON은 텍스트, .json 파일, 또는 JSON을 바로 가리키는 https 링크(예: 저장소의 원본 파일)로 전달하세요. 리디렉션되는 링크는 거부됩니다. 링크 버튼만 만들어지고, 상호작용이 필요한 버튼은 건너뜁니다. 모든 링크는 http 또는 https여야 하고, 텍스트의 멘션은 알림을 보내지 않으며, Discord의 제한이 적용됩니다. /message copy는 기존 메시지를 JSON으로 내보내고, /message edit는 봇의 메시지를 수정하며, /message preview는 결과를 나에게만 보여 줍니다. 웹 편집기의 공유 링크는 형식이 공개되어 있지 않으므로 열지 않습니다.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

봇은 12시간마다 update.repo(scripts/set_repo_url.py로 설정)의 GitHub 저장소에 더 새로운 릴리스가 있는지 확인합니다. 있으면 봇 소유자에게 릴리스 노트가 담긴 개인 메시지가 가고, 릴리스를 내려받아 검사합니다. 검사 항목은 릴리스의 SHA-256 체크섬, 압축 파일 안의 안전한 경로, 태그와 일치하는 버전입니다. 설치는 /debug update action:install로 하거나, auto_install이 켜져 있으면 자동으로 이루어집니다. 설치 전에 교체될 파일이 data/update에 저장되고, 새 패키지가 설치되며, 새 코드를 시험 삼아 불러옵니다. 어느 단계든 실패하면 이전 파일이 복원됩니다. .env, settings.json, data, music은 절대 건드리지 않습니다. 이후 봇이 스스로 다시 시작합니다. Docker에서는 제자리 설치를 하지 않으니 이미지를 업데이트하세요. 업데이트는 저장소의 코드를 실행하므로 신뢰하는 저장소만 지정하세요. enabled를 false로 하면 끌 수 있습니다.

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
/message send channel:#news url:https://example.com/message.json
/message send channel:#news file:message.json
/message preview url:https://example.com/message.json
/message edit message:https://discord.com/channels/1/2/3 url:https://example.com/message.json
/message copy message:https://discord.com/channels/1/2/3
/module disable name:builder
/debug update action:status
/debug update action:check
/debug update action:install
```

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
- ffmpeg (음악 모듈에만 필요)
- tesseract-ocr (선택, 이미지 속 글자를 읽을 때만)

## 빠른 시작

사용하는 시스템을 고르세요. 어느 방법이든 Python 3.11 이상과 봇 토큰이 필요합니다. 자세한 단계별 안내는 [GUIDE.md](GUIDE.md)에 있습니다.

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

### 시작 스크립트와 자동 실행

시작 스크립트는 가상 환경을 만들고, 패키지를 설치하고, 봇을 시작합니다. 처음 실행하면 .env 파일을 만들고 멈추므로 토큰을 입력하세요. 그런 다음 다시 실행합니다.

```bash
./start.sh
```

```bat
start.bat
```

컴퓨터를 다시 시작한 뒤에도 봇이 계속 동작하게 하려면 서비스를 사용하세요. Linux(systemd)와 macOS(launchd):

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

Windows에서는 작업 스케줄러에 로그인 시 start.bat을 실행하는 작업을 만들거나, NSSM 같은 서비스 래퍼를 사용하세요. Docker는 [GUIDE.md](GUIDE.md)를 참고하세요.

### 업데이트

봇을 멈추고 아래 명령을 실행한 뒤 다시 시작하세요. data 폴더의 데이터는 그대로 유지되며, 봇은 데이터 형식이 바뀌기 전마다 데이터베이스를 백업합니다.

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

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

## 대시보드

대시보드는 봇 안에서 동작하는 웹 페이지입니다. Discord로 로그인하면 명령어 대신 스위치, 메뉴, 입력란으로 서버 설정을 바꿀 수 있습니다. 모듈, 채널, 역할, 기준값, 텍스트, 접두사, 언어가 대상입니다. 최근 관리 케이스를 보여 주고, 설정을 내보내고 가져올 수도 있습니다. 내 컴퓨터에서도 VPS에서도 똑같이 동작하며, 켜기 전에는 꺼져 있습니다.

### 대시보드 설정

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

### 보안

- 로그인은 Discord로만 가능합니다(OAuth2, 범위 identify). 액세스 토큰은 즉시 폐기되며 저장되지 않습니다.
- 서버 소유자와 관리자 또는 서버 관리 권한이 있는 멤버만, 해당 서버에 한해 접근할 수 있습니다. 권한은 요청할 때마다 다시 확인합니다.
- 봇이 지금 연결된 서버만 열 수 있습니다. 봇이 오프라인이거나 서버에 없거나 아직 시작 중이면 대시보드는 모든 요청을 거부합니다. 대시보드는 봇 안에서 동작하며 별도의 데이터베이스나 서비스가 없습니다.
- 기본적으로 127.0.0.1에서만 대기하므로 네트워크의 다른 사람은 접근할 수 없습니다. 공개 주소는 HTTPS일 때만 허용되며, 그렇지 않으면 대시보드가 시작되지 않습니다.
- 세션은 SameSite가 지정된 HttpOnly 쿠키의 무작위 토큰을 사용하며, HTTPS에서는 __Host- 접두사도 붙습니다. 8시간 후 만료되고 메모리에만 있으므로 재시작하면 모두 로그아웃됩니다.
- 모든 변경에는 CSRF 토큰과 일치하는 Origin이 필요합니다. Host 헤더는 DNS 리바인딩을 막기 위해 검사합니다. 페이지는 외부 스크립트를 불러오지 않고, 엄격한 Content Security Policy가 인라인 코드를 차단하며, 요청에는 빈도 제한이 있고 본문은 256 KB로 제한됩니다.
- 모든 값은 설정의 유형에 맞게 검사하며, Discord ID는 해당 서버에 존재해야 합니다. 카운터, 티켓, 저장된 항목 같은 내부 상태는 편집할 수 없습니다. 모든 변경은 서버의 보안 로그 채널에 기록됩니다.
- 메시지 내용은 표시하지 않습니다. 관리 케이스는 읽기 전용입니다.

### VPS에서 대시보드 사용

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

편집기는 스위치, 숫자, 텍스트, 채널, 역할, 단순 목록에 해당하는 모든 설정을 보여 줍니다. 상점 아이템, 역할 메뉴, 피드, 태그, 티켓처럼 명령어로 만드는 것은 계속 명령어로 합니다. 페이지는 영어와 독일어로 제공되며 브라우저 언어를 따릅니다. Docker에서는 포트를 127.0.0.1에만 공개하고(127.0.0.1:8080:8080), 컨테이너 안에서 host를 0.0.0.0, allow_insecure_http를 true로 설정하세요.

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
/case view case_id:12

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
/suggestion setup set channel:#suggestions review_role:@Staff
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

/xp levelrole add level:10 role:@Active
/xp levelrole add level:50 role:@Veteran
/xp levelrole remove level:10
/xp levelrole list
/xp levelrole sync                                    # apply to everyone who already has XP

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

/notify topic add key:events role:@Events description:Server events
/notify topic panel channel:#roles title:Notifications   # one button per topic
/notify topic remove key:events
/notify subscribe topic:events                     # members choose for themselves
/notify unsubscribe topic:events
/notify list
```

### 생일

멤버가 일과 월을 저장하면 당일에 봇이 역할을 주고 메시지를 보냅니다.

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

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

### 관리자 도구

채널 정리, 역할 관리, 비공개 메모. 모든 작업은 로그에 기록됩니다.

```
/purge amount:50 user:@User kind:links           # kind: all, links, images, bots, attachments
/slowmode seconds:10 channel:#general              # 0 turns it off
/lockchannel channel:#general reason:Spam wave
/unlockchannel channel:#general

/role add member:@User role:@Member
/role remove member:@User role:@Member

/note user:@User text:Watch this member            # private, shown in /cases
/tempban user:@User duration:7d reason:Spam        # unbanned automatically
/jailed                                            # who is in the gulag right now

/case view case_id:12
/case edit case_id:12 reason:Corrected reason
/case delete case_id:12
```

### 정보

사용자, 서버, 역할, 봇에 대한 정보를 조회합니다.

```
/userinfo user:@User
/serverinfo
/roleinfo role:@Moderator
/avatar user:@User
/help command:ban                                  # explains one command
/ping
/botinfo
```

### 공지, 태그, 알림

봇 이름으로 글을 쓰고, 사용자 지정 명령어를 만들고, 메시지에 자동으로 답하고, 알림을 설정합니다.

```
/say channel:#news message:Maintenance tonight
/embed channel:#news title:Update description:New rules color:#5865F2

/tag create name:rules text:Be kind to each other
/tag show name:rules
/tag list
/tag info name:rules
/tag edit name:rules text:Be kind and read the pinned message
/tag delete name:rules

/autoresponder add trigger:server ip response:The IP is in #info mode:contains cooldown:30
/autoresponder list
/autoresponder remove id:1                         # mode: contains, word, exact, startswith

/remind set duration:2h text:Stream starts
/remind list
/remind cancel id:1
/afk reason:Lunch                                  # the bot tells others who mention you
```

### 모드메일과 차단 이의 신청

멤버는 서버 안의 비공개 채널로 운영진에게 연락합니다. 봇에게 다이렉트 메시지를 보낼 필요가 없습니다.

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

### 카운팅 채널, 고정 메시지, 통계

카운팅 게임, 채널 맨 아래에 남는 메시지, 실시간 숫자를 보여 주는 채널.

```
/counting setup channel:#counting reset_on_fail:True delete_wrong:True
/counting status
/counting set number:100
/counting off

/sticky set channel:#rules text:Read the rules before you write
/sticky list
/sticky remove channel:#rules

/stats create template:Members: {members} category:Statistics
/stats add channel:#info template:Boosts: {boosts}
/stats list
/stats refresh
/stats remove channel:#info
```

### 기존 기능의 추가 옵션

티켓, 추첨, 음성 방, XP, 생일, 백업, 로그, 상태 보기에 대한 추가 기능입니다.

```
/ticket claim
/ticket rename name:billing-help
/ticket list

/giveaway cancel giveaway_id:3
/giveaway edit giveaway_id:3 prize:Nitro winners:2 extend:1h

/voice rename name:Study room                      # only the owner of the room
/voice limit limit:4
/voice lock
/voice unlock
/voice kick member:@User
/voice transfer member:@User
/voice claim                                       # if the owner left

/xp channelboost channel:#chat multiplier:1.5
/xp resetall confirm:True
/leaderboard page:2

/birthday list
/birthday setup user member:@User day:14 month:3
/birthday setup clear member:@User

/backup info name:weekly
/log show
/log ignorechannel channel:#bots
/log ignoreuser user:@Bot
/log sent enabled:True

/automod status
/verify status
/raid status
/welcome show
/starboard show
```

### 추가 AutoMod 도구

단축 링크 추적, 신규 멤버의 링크 제한, 고스트 핑 감지, 아무도 처벌하지 않고 규칙 테스트.

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

### 관리자 한도와 권한 감사

관리자가 너무 많이 차단하거나 추방하면 경고하고, 위험한 권한을 가진 역할을 보여 줍니다.

```
/modwatch status
/modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/modwatch exclude member:@TrustedMod

/permaudit run                                                  # roles with dangerous permissions and who holds them
/permaudit watch enabled:True                                   # alarm when a role or member gets one
/permaudit trust role:@Admin
```

### 신고와 초대 추적

멤버가 메시지를 운영진에게 신고하고, 봇은 각 신규 멤버가 어떤 초대로 들어왔는지 기록합니다.

```
/report setup set channel:#reports ping_role:@Moderator cooldown:60 anonymous:False
/report setup ignorechannel channel:#staff
/report setup status

/report send message_link:https://discord.com/channels/1/2/3 reason:Spam
# or right click a message, Apps, Report message

/invites who member:@User
/invites stats user:@User
/invites top
/invites setup log:True alert_joins:5 alert_minutes:60
```

### 진단과 디버깅

누락된 권한과 잘못된 설정을 찾고, 오류 보고를 채널에서 받고, 설정을 내보내거나 가져올 수 있습니다.

```
/diagnose                                                       # permissions, role order, deleted channels and roles
/debug status
/debug errorchannel channel:#bot-errors
/debug errortest
/debug selftest enabled:True                                    # check at start-up
/debug usagestats enabled:True
/debug usage reset:False
/debug level level:DEBUG                                        # owner of the bot only
/debug db action:check                                          # owner of the bot only: check, vacuum, size

/config export
/config import file:guardbot-settings.json confirm:False        # first without confirm
```

### 음악

음성 채널에서 링크와 music 폴더의 파일을 재생합니다. 다운로드는 music/아티스트/앨범/트랙으로 저장됩니다. ffmpeg와 requirements.txt의 패키지가 필요합니다.

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
/config set path:music.allowed_hosts value:bandcamp.com,archive.org
/music cleardj
/music status
```

무손실: 직접 추가한 파일(FLAC, WAV, ALAC)과 FLAC을 제공하는 출처는 그대로 재생됩니다. YouTube, SoundCloud 등은 손실 오디오만 제공하며 나중에 무손실로 만들 수 없습니다. Discord는 음성을 Opus로 전송하며 봇은 음성 채널의 비트레이트를 사용합니다. 책임: 콘텐츠 다운로드와 재생은 사이트 약관이나 저작권법을 위반할 수 있습니다. 다운로드는 기본적으로 꺼져 있고 모듈도 활성화하기 전까지 꺼져 있습니다. 재생되고 저장되는 내용에 대한 책임은 봇 운영자에게 있습니다.

### 설정과 상태 점검

안내형 도우미가 버튼과 메뉴로 가장 중요한 것을 설정합니다: 로그 채널, 환영 채널, 운영진 역할, 굴라그, AutoMod 프리셋(느슨함, 보통, 엄격), 서버 템플릿(커뮤니티, 게임, 지원), 그리고 언어. /health는 무엇이 설정되었고 무엇이 남았는지 보여 줍니다. 언어를 바꾸면 기본 환영 메시지, AutoMod 알림, 인증, 티켓, 이의 신청, 모드메일, 역할 메뉴 등 멤버에게 보이는 문구가 바뀝니다. 관리자에게 보내는 고정 답변은 번역되어 있고, 이름과 숫자가 들어가는 답변은 영어로 유지됩니다.

```
/setup                                                         # buttons and menus, nothing is switched off by a template
/health                                                        # what is set up, what is open, and the self-test
/language code:de
```

### 경제

일일 보상, 일하기, 송금, 순위표, 그리고 역할을 줄 수 있는 상점을 갖춘 서버 화폐입니다. economy 모듈로 켭니다. 명령어는 접두사로도 사용할 수 있습니다(예: !economy daily).

```
/module enable name:economy
/economy balance member:@User                                  # same as !economy
/economy daily
/economy work
/economy pay member:@User amount:50
/economy leaderboard
/economy shop
/economy buy item:1
/economy inventory

/economy give member:@User amount:500                          # staff, a negative amount takes away
/economy shopadd name:VIP price:1000 role:@VIP stock:10
/economy shopremove item:1
/economy config name:gold daily:200 daily_hours:24 work_min:20 work_max:80 work_minutes:30
```

### 역할 메뉴, 예약 메시지, 피드

역할 메뉴는 버튼이나 드롭다운으로 역할을 줍니다. 예약 메시지는 한 번 게시되거나 매시간, 매일, 매주 반복됩니다. 피드는 YouTube 새 영상, Twitch 방송, RSS 항목을 게시합니다. YouTube는 채널 ID(UC로 시작)를 사용합니다. Twitch는 .env에 TWITCH_CLIENT_ID와 TWITCH_CLIENT_SECRET이 필요합니다. 시간은 in 2h, 18:30 또는 2026-12-24 18:00 같은 날짜와 시간으로, 서버의 시간대 기준으로 입력합니다. 피드의 첫 확인은 이미 있는 항목을 기억만 합니다.

```
/rolemenu create title:Pick your roles kind:buttons single:False channel:#roles
/rolemenu add menu:1 role:@Red label:Red
/rolemenu remove menu:1 role:@Red
/rolemenu delete menu:1
/rolemenu list

/schedule add channel:#news when:18:30 text:Daily reminder repeat:daily
/schedule add channel:#news when:in 2h text:Restart soon repeat:none
/schedule list
/schedule remove number:1
/schedule timezone name:Europe/Berlin

/feed add kind:youtube target:UCxxxxxxxxxxxxxxxxxxxxxx channel:#videos ping:@Subscribers
/feed add kind:twitch target:somestreamer channel:#live
/feed add kind:rss target:https://example.com/feed.xml channel:#news
/feed list
/feed check
/feed remove number:1
```

### 활동, 일괄 작업, 케이스 검색

활동은 채널별 메시지 수와 일별 입장·퇴장 수를 세며, 내용이나 이름은 절대 저장하지 않습니다. 일괄 작업은 확인 후 최대 25명의 사용자를 차단, 추방 또는 타임아웃합니다. 케이스는 사용자, 유형, 이름, 사유, 관리자, 기간으로 검색할 수 있고, 메모를 차단 기록에 연결하는 것처럼 서로 연결할 수 있습니다.

```
/module enable name:activity
/activity overview days:7
/activity channels days:30
/activity growth days:14
/activity reset

/bulk ban users:123456789012345678 223456789012345678 reason:Raid
/bulk kick users:123456789012345678 223456789012345678 reason:Spam
/bulk timeout users:123456789012345678 223456789012345678 duration:2h reason:Spam

/cases user:@User kind:ban text:scam moderator:@Mod days:30
/case link case_id:12 other:15
/case unlink case_id:12 other:15
```

### 사기 방지 및 암호화폐 방지

전형적인 MrBeast 사기 같은 가짜 경품 행사를 텍스트와 이미지에서 몇 밀리초 안에 삭제합니다. 즉시 목록의 이름은 어떤 철자로 쓰여도 바로 삭제됩니다(MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). 그 외에는 목록(이름, 미끼, 암호화폐, 링크, 금액)의 단어가 점수로 합산되어 기준에 도달하면 메시지가 삭제됩니다. 이미지는 OCR로 읽으며, 한 번 사기로 판정된 이미지는 다시 읽지 않고 삭제합니다. 이미지를 읽으려면 tesseract가 필요하며, 없으면 텍스트만 검사합니다. MrBeast 관련 서버는 즉시 목록에서 이름을 빼거나 /automod exemptchannel로 채널을 제외할 수 있습니다. 의지하기 전에 /antiscam test로 먼저 시험해 보세요.

```
/antiscam status
/antiscam set action:delete threshold:3 text:True images:True ocr_lang:eng max_images:3
/antiscam words action:add kind:instant word:mrbeast
/antiscam words action:remove kind:crypto word:token
/antiscam test text:MrBeast is giving away 1000 BTC, claim now
/antiscam testimage image:scam.png
/antiscam forget
/automod dryrun rule:antiscam enabled:True                     # only report, do not remove
```

### 운영

봇은 몇 초마다 데이터를 저장하고 data/dbbackups에 데이터베이스 백업을 보관합니다(데이터 형식 변경 전 1개, 하루 1개). 음악 대기열, 고정 메시지, 관리자 카운터는 재시작 후에도 유지됩니다. 대형 봇은 여러 샤드로 실행할 수 있습니다. heartbeat 파일과 선택 사항인 상태 페이지는 모니터링 도구에 도움이 됩니다. 이 옵션은 settings.json에서 설정합니다:

```json
{
  "shard_count": null,
  "db_backup_hours": 24,
  "db_backup_keep": 7,
  "health_port": 0,
  "health_host": "127.0.0.1",
  "tesseract": null,
  "music_generic": true
}
```

```
/debug db action:backup                                         # owner of the bot only, saved in data/dbbackups
/debug db action:list
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
/birthday setup set   message                         {user} {name}
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

## 번역

영어가 이 프로젝트의 원본 언어입니다. 문서, 대시보드, 봇 메시지의 모든 번역은 기계 번역으로 만들어졌으며 원어민의 검수를 받지 않았습니다. 어색한 표현이나 오류가 있을 수 있으니 발견하면 알려 주시거나 수정안을 보내 주세요. 파일은 docs/와 guardbot/locales/에 있습니다.

## 로드맵

- 대시보드에 활동 및 관리 차트 추가.
- 원어민의 모든 번역 검수.
- 고정 응답 텍스트 번역 확대.

## 개인정보 및 보안

- 원격 측정은 없습니다. 봇은 Discord와 통신하며, 업데이트 확인을 위해 GitHub와도 통신합니다(개인 데이터는 보내지 않으며 update.enabled로 끌 수 있습니다). 관리자가 건네는 링크(피드, 음악, JSON 링크 등)는 요청할 때만 엽니다.
- 모든 데이터는 내 컴퓨터의 data 폴더에 저장됩니다. 설정, XP, 생일(일과 월만), 관리 기록입니다.
- 봇은 멤버가 보내는 다이렉트 메시지를 무시합니다.
- 토큰은 .env 파일에서 읽습니다. 절대 공유하거나 업로드하지 마세요.
- 멤버는 /mydata로 자신의 데이터를 내보내고 삭제할 수 있습니다. 관리자는 떠난 멤버의 데이터를 얼마나 보관할지 정할 수 있습니다.
- [PRIVACY.md](../PRIVACY.md)

## 지원

버그, 아이디어, 제안은 Discord @justyyin 으로 연락하거나 GitHub에 issue를 등록해 주세요.

## 크레딧

GuardBot은 Merlin Fuchs의 [Embed Generator](https://github.com/merlinfuchs/embed-generator)(MIT 라이선스, message.style에서 제공)에서 영감을 받았습니다. 메시지 빌더는 같은 JSON 형식을 읽으므로 그곳에서 만든 메시지를 이 봇으로 게시할 수 있습니다. 해당 프로젝트의 코드는 포함되어 있지 않습니다. discord.py, aiohttp, Pillow, yt-dlp, mutagen, Tesseract의 제작자에게 감사드립니다.

## 라이선스

MIT 라이선스로 공개되어 있습니다. 참조: [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
