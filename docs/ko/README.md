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
  - [서버 관리](#서버-관리)
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
  - [구조, 멤버, 팀](#구조-멤버-팀)
- [대시보드](#대시보드)
  - [대시보드 설정](#대시보드-설정)
  - [명령어, 스킬, AI와 봇 프로필](#명령어-스킬-ai와-봇-프로필)
  - [보안](#보안-1)
  - [VPS에서 대시보드 사용](#vps에서-대시보드-사용)
- [명령어](#명령어)
  - [명령어 그룹](#명령어-그룹)
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
  - [수습 기간, 무리 탐지, 타임라인, 학습](#수습-기간-무리-탐지-타임라인-학습)
  - [패널](#패널)
  - [스킬과 AI](#스킬과-ai)
  - [메시지 빌더와 업데이트](#메시지-빌더와-업데이트)
  - [운영](#운영)
  - [서버 관리](#서버-관리-1)
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
- 굴라그 채널: 사기 링크나 이미지를 올린 멤버는 계정 보안 안내가 있는 단 하나의 채널로 이동합니다. 관리자는 /moderation jail과 /moderation unjail도 사용할 수 있습니다.
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
- 상점이 있는 경제, 버튼 또는 드롭다운 역할 메뉴, 예약 메시지, YouTube·Twitch·RSS 피드, 활동 통계, 안내형 /admin setup. 멤버에게 보이는 메시지는 12개 언어로 제공됩니다.

### 서버 관리

- 모든 모듈과 개별 명령어를 서버별로 켜고 끌 수 있습니다.
- 사용자 지정 접두사, 명령어 별칭, 이름을 바꿀 수 있는 명령어.
- 역할과 채널 구조의 백업 및 복원.
- 역할, 채널, 이모지, 웹훅의 예약 자동 백업과 부족한 것만 추가하는 복원 명령어.
- 대시보드: Discord로 로그인한 뒤 브라우저에서 각 서버의 설정을 바꿉니다. 서버를 관리하는 멤버만, 봇이 연결되어 있는 동안에만 사용할 수 있습니다.
- 스킬: 안전한 블록으로 만드는 나만의 명령어, 게임, 자동화. 본인의 키(Anthropic, OpenAI, Kimi)로 AI가 작성하게 할 수도 있습니다. 대시보드는 모든 명령어를 보여 주고 스킬, AI 설정, 봇 프로필을 편집합니다.

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

### 구조, 멤버, 팀

버전 1.5에는 서버를 구성하고 정돈된 상태로 유지하는 명령, 돌아온 멤버의 복원, 관리팀 운영을 위한 명령이 추가되었습니다. 각 기능에는 모듈 스위치(`/admin module`), 자체 설정, 대시보드의 자리가 있습니다.

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

- `/structure` 로 채널과 카테고리를 만들고, 복제하고, 이름을 바꾸고, 정렬하며 다른 채널의 권한을 복사할 수 있습니다. 비활성 채널은 보고되거나 보관용 카테고리로 이동됩니다(`/structure archive`). 역할은 기간을 정해 부여하고 템플릿으로 저장할 수 있으며, 템플릿은 적용하는 사람에게 없는 권한을 부여하지 않습니다.
- `/structure rules` 는 동의 버튼과 버전 번호가 있는 규칙을 게시합니다. `post new_version:True` 이후 새 버전에 동의하지 않은 멤버는 다이렉트 메시지로 한 번 알림을 받습니다.
- `/members stickyroles` 는 멤버가 돌아오면 역할을 돌려주고 타임아웃이나 뮤트를 복원합니다. `/members nickname` 은 목록 맨 위로 올라가려는 문자를 제거하고, 닉네임과 사용자 이름의 금지어를 검사하며, 위반자의 이름을 바꿉니다. 관찰 목록은 조용히 동작하며, 목록에 있는 사용자가 첫 메시지를 보내면 팀에 알림이 갑니다.
- 4인 승인(`/security approval`)은 차단, 추방, 타임아웃, 일괄 작업을 두 번째 관리자가 동의한 뒤에만 실행합니다. `/moderation case undo` 는 케이스와 그로 인한 후속 조치(예: 뮤트와 이어진 차단)까지 취소합니다. 경고는 일정 일수 후 만료되도록 할 수 있습니다(`/moderation escalation expiry`).
- `/admin history` 는 누가 언제 어떤 설정을 바꿨는지 보여 주고 섹션을 되돌립니다. 사람의 이름은 서버의 최근 명령과 대시보드 변경에서 추정한 값입니다. `/admin history copy` 는 봇으로 관리할 수 있는 다른 서버로 섹션을 복사하며, 처음에는 시험 실행으로 시작합니다. `/admin exceptions` 는 채널과 역할을 AutoMod 규칙과 스캠 방지에서 제외합니다. `/admin dashaccess` 는 역할에 대시보드 읽기 전용 또는 관리자 접근을 줍니다.
- `/team` 은 관리자별 작업(케이스, 티켓, 신고, 응답 시간, 비활성 멤버)을 보여 주고, 주간 보고서(요일과 시각은 UTC)를 게시하며, `/team duty away` 로 부재를 알리면 티켓과 멘션이 다른 사람에게 넘어가고, 양식과 팀 투표로 스태프 지원을 운영합니다.
- Discord는 그룹 안의 명령을 특정 멤버에게서 숨길 수 없습니다. 봇은 여전히 모든 호출을 확인합니다. 팀 통계 수치는 업데이트한 날부터 집계되며 그 이전의 작업은 포함되지 않습니다.

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

### 명령어, 스킬, AI와 봇 프로필

대시보드에는 다섯 개의 페이지가 더 있습니다. Panels(패널 항목 참고)와 다음 네 가지입니다. 명령어는 모든 슬래시 명령어, 접두사 명령어, 컨텍스트 메뉴를 모듈, 필요한 권한, 켜짐 여부와 함께 보여 줍니다. 관리자는 이를 켜고 끄고, 역할을 허용하거나 거부하며, 접두사 명령어에 짧은 이름을 붙일 수 있습니다. 접두사는 같은 페이지에서 바꿉니다. 스킬은 모든 스킬을 보여 주고 명령어와 같은 검사를 거쳐 JSON으로 편집합니다. AI는 모델과 제한을 설정하고 키를 저장합니다(쓰기 전용이며 페이지로 다시 보내지 않습니다). 봇 프로필은 이 서버에서 봇의 이름, 이미지, 배너, 소개 글을 바꿉니다. 봇 애플리케이션의 소유자 또는 settings.json의 `owner_ids`에 적힌 ID는 모든 곳에서도 바꿀 수 있습니다. Discord는 이름과 이미지를 바꿀 수 있는 빈도를 제한합니다. 모든 변경은 감사 로그에 기록됩니다.

모든 모듈은 플러그인으로 표시됩니다. Plugins 페이지는 카테고리별 카드로 보여 주고, 각 플러그인에는 활성 스위치, 열고 닫을 수 있는 상자 안의 설정, 스위치와 역할 편집기가 있는 명령어가 담긴 전용 페이지가 있습니다. 왼쪽 바는 카테고리별로 플러그인을 나열하며 점으로 켜짐 여부를 표시합니다. 대시보드는 어두운 디자인입니다.

대시보드는 봇의 12개 언어 모두로 표시할 수 있습니다. 언어는 오른쪽 위나 로그인 페이지에서 고릅니다. 선택은 브라우저에 저장되며 서버 언어는 바뀌지 않습니다. 대시보드 텍스트는 기계 번역입니다.

각 플러그인 페이지는 플러그인이 하는 일을 설명하고, 모든 기능을 개별 스위치와 짧은 설명과 함께 나열하며, 나머지 설정은 아래 상자에 둡니다. 플러그인 페이지와 개요에서 각 플러그인을 바로 켜고 끌 수 있습니다. 설정의 대시보드 모양 상자에서는 강조 색상, 배경, 상자, 글자 색을 바꾸고, 배경화면(원하는 만큼 어둡게, 흐리게)을 설정하며, 사이드바에 사용자 메뉴와 탭을 추가할 수 있습니다. 탭은 고른 플러그인을 모으거나, 페이지를 열거나, https 주소로 연결하거나, 메모를 보여 줄 수 있습니다. 모양은 서버별로 저장되며 그 서버의 대시보드를 여는 모든 사람에게 보입니다. 바닥글에는 저작권 표시와 Discord, GitHub 링크가 있습니다. 공식 로고를 표시하려면 Discord와 GitHub의 브랜드 페이지에서 받은 discord.svg와 github.svg를 guardbot/web/brand/에 넣으세요.

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

<!-- groups -->
### 명령어 그룹

슬래시 명령어 슬롯을 아끼기 위해(Discord는 봇당 최상위 명령어를 100개까지 허용합니다) 관련 명령어를 그룹으로 묶었습니다. 그룹을 먼저, 그다음 명령어를 입력합니다. 예: `/moderation ban`. 접두사를 쓰는 텍스트 명령어(예: `!ban`)는 그대로입니다. 권한, 별칭, 모듈 스위치는 계속 단순한 명령어 이름을 사용합니다.

| 그룹 | 포함 |
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

### 관리

경고, 뮤트, 추방, 차단은 슬래시 명령어와 접두사로 모두 사용할 수 있습니다(예: `!warn @User spam`). 모든 조치는 번호가 붙은 기록을 만듭니다.

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

### 굴라그(감금)

계정이 탈취된 멤버는 보안 안내가 있는 단 하나의 채널로 이동합니다. 풀려날 때 예전 역할이 복원됩니다.

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

명령어, AutoMod, 스캠 방지, 재참가, 또는 누군가 역할을 직접 부여한 경우 등 어떤 방식으로든 굴라그에 들어온 사람은 멘션과 함께 Account Security Required 안내를 받습니다. 굴라그에 누군가 있는 동안 채널 맨 아래에 Account Recovery Reminder가 유지되며 10분마다 새로 고쳐집니다. 굴라그에 있는 멤버가 굴라그 채널에 접두사와 해제 단어(예: `!unban`)를 쓰면 스태프용 Release, Keep 버튼이 있는 해제 요청이 만들어집니다. 봇이 스스로 누군가를 해제하지는 않습니다. `/access jailsetup reminder`로 각 부분을 켜고 끄며 간격과 단어를 정합니다.

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

감사 로그를 감시하고 누군가 서버를 파괴하면 대응합니다. 서버 소유자에게 다이렉트 메시지가 갑니다.

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

### 인증

새 멤버는 버튼을 누르거나 캡차를 풀기 전까지 인증 채널만 볼 수 있습니다.

```
/access verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/access verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/access verify panel channel:#verify                      # post the button again
/access verify apply                                      # apply the channel permissions again
/access verify member member:@User                        # verify someone manually
/access verify off
```

### 로그

카테고리마다 채널을 고르거나, 모든 것을 하나의 메인 채널에 기록합니다.

```
/server log set category:main channel:#logs               # fallback for every category
/server log set category:messages channel:#log-messages
/server log set category:moderation channel:#log-moderation
/server log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/server log sent enabled:False                            # stop logging every sent message
/server log show
```

### 환영, 작별, 부스터

메시지, 자동 역할, 서버 부스터 보상.

```
/community welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/community welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/community welcome autorole role:@Member                     # toggle, given to every new member
/community welcome botrole role:@Bots                        # toggle, given to every new bot
/community welcome test

/community booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/community booster role role:@Booster                        # toggle
```

### 티켓

멤버가 버튼으로 비공개 채널을 엽니다. 티켓을 닫으면 대화 기록이 전송됩니다.

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

### 투표와 경품 추첨

투표와 참여는 버튼으로 합니다. 기간은 30m, 2h, 1d 같은 값을 받습니다.

```
/engage poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/engage poll end poll_id:3
/engage poll list

/engage giveaway start prize:Nitro duration:2d winners:2 role:@Member
/engage giveaway end giveaway_id:1
/engage giveaway reroll giveaway_id:1
/engage giveaway list
```

### 건의와 스타보드

멤버가 올린 건의를 운영진이 승인하거나 거부할 수 있고, 인기 있는 메시지는 강조됩니다.

```
/suggestion setup set channel:#suggestions review_role:@Staff
/support suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/engage starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/engage starboard ignore channel:#spam
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

/info rank                                              # also: !rank, shows a rank card image
/info rank user:@User
/info leaderboard
```

### 반응 역할과 알림

원하는 이모지 반응으로 역할을 주고, 멤버가 알림 주제를 직접 고르게 합니다.

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
/community tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### 백업과 복원

백업에는 역할, 채널, 이모지, 웹훅, 멤버 역할이 들어 있습니다. 복원은 부족한 것만 추가합니다.

```
/server backup create name:before-update
/server backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/server backup list
/server backup download name:before-update
/server backup restore name:before-update member_roles:True   # only adds what is missing
/server backup delete name:before-update
```

### 데이터와 개인정보

멤버는 자신의 데이터를 내보내고 삭제할 수 있습니다. 관리자는 보관 기간을 정합니다.

```
/info mydata export                                     # members download their own data
/info mydata delete confirm:True                        # members delete their XP and birthday

/server privacy retention days:90                         # delete data of members who left after 90 days
/server privacy export user_id:123456789012345678
/server privacy delete user_id:123456789012345678 cases:True
```

### 관리자 도구

채널 정리, 역할 관리, 비공개 메모. 모든 작업은 로그에 기록됩니다.

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

### 정보

사용자, 서버, 역할, 봇에 대한 정보를 조회합니다.

```
/info userinfo user:@User
/server serverinfo
/server roleinfo role:@Moderator
/info avatar user:@User
/help command:ban                                  # explains one command
/info ping
/info botinfo
```

### 공지, 태그, 알림

봇 이름으로 글을 쓰고, 사용자 지정 명령어를 만들고, 메시지에 자동으로 답하고, 알림을 설정합니다.

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

### 기존 기능의 추가 옵션

티켓, 추첨, 음성 방, XP, 생일, 백업, 로그, 상태 보기에 대한 추가 기능입니다.

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
/team modwatch status
/team modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/team modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/team modwatch exclude member:@TrustedMod

/team permaudit run                                                  # roles with dangerous permissions and who holds them
/team permaudit watch enabled:True                                   # alarm when a role or member gets one
/team permaudit trust role:@Admin
```

### 신고와 초대 추적

멤버가 메시지를 운영진에게 신고하고, 봇은 각 신규 멤버가 어떤 초대로 들어왔는지 기록합니다.

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

### 진단과 디버깅

누락된 권한과 잘못된 설정을 찾고, 오류 보고를 채널에서 받고, 설정을 내보내거나 가져올 수 있습니다.

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

무손실: 직접 추가한 파일(FLAC, WAV, ALAC)과 FLAC을 제공하는 출처는 그대로 재생됩니다. YouTube, SoundCloud 등은 손실 오디오만 제공하며 나중에 무손실로 만들 수 없습니다. Discord는 음성을 Opus로 전송하며 봇은 음성 채널의 비트레이트를 사용합니다. 책임: 콘텐츠 다운로드와 재생은 사이트 약관이나 저작권법을 위반할 수 있습니다. 다운로드는 기본적으로 꺼져 있고 모듈도 활성화하기 전까지 꺼져 있습니다. 재생되고 저장되는 내용에 대한 책임은 봇 운영자에게 있습니다.

소스: YouTube와 SoundCloud의 링크와 검색은 바로 재생됩니다. Spotify, Apple Music, Tidal 링크도 받지만, 이 서비스들은 오디오를 제공하지 않습니다. 봇은 공개 페이지에서 제목과 아티스트를 읽고 검색 소스(YouTube 또는 SoundCloud, /music sources로 설정)에서 같은 곡을 재생합니다. Spotify와 Apple Music의 앨범과 재생목록은 공개 페이지에서 읽습니다. Tidal 앨범과 재생목록에는 developer.tidal.com의 무료 개발자 키를 .env에 넣어야 합니다(TIDAL_CLIENT_ID와 TIDAL_CLIENT_SECRET). 음악 폴더의 파일은 그대로 재생됩니다. 저장된 재생목록은 모든 소스를 섞을 수 있고, /music stay는 봇을 24시간 음성 채널에 머물게 하며 다시 시작한 뒤에도 재생목록을 반복 재생합니다.

Guard Music, 두 번째 봇: 음악을 별도의 봇 계정으로 실행할 수 있어서, 관리 기능에 영향을 주지 않고 항상 음성 채널에 머물 수 있습니다.

1. Discord Developer Portal에서 두 번째 애플리케이션을 만들고 이름을 Guard Music으로 정한 뒤 그 봇의 토큰을 복사합니다.
2. 토큰을 .env에 MUSIC_TOKEN으로 적고 settings.json에서 music_bot.enabled를 true로 설정합니다.
3. GuardBot을 다시 시작합니다. Guard Music은 같은 프로세스에서 시작되고 같은 설정과 데이터를 쓰며, 음악 명령어는 Guard Music으로 옮겨집니다.
4. 대시보드의 음악 페이지를 열고 그곳의 버튼으로 Guard Music을 서버에 추가합니다. MUSIC_TOKEN이 없으면 음악은 GuardBot에 남습니다.

사용에 따른 책임은 본인에게 있습니다. YouTube 등 서비스에서 스트리밍하면 해당 서비스의 이용 약관을 위반할 수 있으며, 재생되는 내용에는 저작권이 적용됩니다. Spotify, Apple Music, Tidal에서는 아무것도 다운로드하지 않으며 어떤 보호 장치도 우회하지 않습니다. 재생되는 내용에 대한 책임은 봇 운영자에게 있습니다. 대시보드의 음악 페이지에는 플레이어, 대기열, 재생목록, 24/7 모드, 소스와 이 안내가 표시됩니다.

### 설정과 상태 점검

안내형 도우미가 버튼과 메뉴로 가장 중요한 것을 설정합니다: 로그 채널, 환영 채널, 운영진 역할, 굴라그, AutoMod 프리셋(느슨함, 보통, 엄격), 서버 템플릿(커뮤니티, 게임, 지원), 그리고 언어. /server health는 무엇이 설정되었고 무엇이 남았는지 보여 줍니다. 언어를 바꾸면 기본 환영 메시지, AutoMod 알림, 인증, 티켓, 이의 신청, 모드메일, 역할 메뉴 등 멤버에게 보이는 문구가 바뀝니다. 관리자에게 보내는 고정 답변은 번역되어 있고, 이름과 숫자가 들어가는 답변은 영어로 유지됩니다.

```
/admin setup                                                         # buttons and menus, nothing is switched off by a template
/server health                                                        # what is set up, what is open, and the self-test
/admin language code:de
```

### 경제

일일 보상, 일하기, 송금, 순위표, 그리고 역할을 줄 수 있는 상점을 갖춘 서버 화폐입니다. economy 모듈로 켭니다. 명령어는 접두사로도 사용할 수 있습니다(예: !economy daily).

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

### 역할 메뉴, 예약 메시지, 피드

역할 메뉴는 버튼이나 드롭다운으로 역할을 줍니다. 예약 메시지는 한 번 게시되거나 매시간, 매일, 매주 반복됩니다. 피드는 YouTube 새 영상, Twitch 방송, RSS 항목을 게시합니다. YouTube는 채널 ID(UC로 시작)를 사용합니다. Twitch는 .env에 TWITCH_CLIENT_ID와 TWITCH_CLIENT_SECRET이 필요합니다. 시간은 in 2h, 18:30 또는 2026-12-24 18:00 같은 날짜와 시간으로, 서버의 시간대 기준으로 입력합니다. 피드의 첫 확인은 이미 있는 항목을 기억만 합니다.

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

### 활동, 일괄 작업, 케이스 검색

활동은 채널별 메시지 수와 일별 입장·퇴장 수를 세며, 내용이나 이름은 절대 저장하지 않습니다. 일괄 작업은 확인 후 최대 25명의 사용자를 차단, 추방 또는 타임아웃합니다. 케이스는 사용자, 유형, 이름, 사유, 관리자, 기간으로 검색할 수 있고, 메모를 차단 기록에 연결하는 것처럼 서로 연결할 수 있습니다.

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

### 사기 방지 및 암호화폐 방지

전형적인 MrBeast 사기 같은 가짜 경품 행사를 텍스트와 이미지에서 몇 밀리초 안에 삭제합니다. 즉시 목록의 이름은 어떤 철자로 쓰여도 바로 삭제됩니다(MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). 그 외에는 목록(이름, 미끼, 암호화폐, 링크, 금액)의 단어가 점수로 합산되어 기준에 도달하면 메시지가 삭제됩니다. 이미지는 OCR로 읽으며, 한 번 사기로 판정된 이미지는 다시 읽지 않고 삭제합니다. 이미지를 읽으려면 tesseract가 필요하며, 없으면 텍스트만 검사합니다. MrBeast 관련 서버는 즉시 목록에서 이름을 빼거나 /automod exemptchannel로 채널을 제외할 수 있습니다. 의지하기 전에 /security antiscam test로 먼저 시험해 보세요.

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

### 수습 기간, 무리 탐지, 타임라인, 학습

수습 기간은 새 멤버를 하나의 역할에 넣습니다. 설정한 수의 일반 메시지를 쓰거나 설정한 분이 지나기 전까지 링크, 초대, 파일은 짧은 안내와 함께 삭제됩니다. 레이드 방어는 무리도 알아봅니다. 이름 패턴이 같거나, 프로필 사진이 같거나, 몇 분 안에 만들어진 새 계정이 여럿인 경우입니다. 타임라인(/moderation case timeline)은 한 사용자의 계정 생성, 가입과 초대, 수습 기간, 케이스, 이의 신청을 시간순으로 모아 보여 줍니다. 메시지는 저장되지 않으므로 포함되지 않습니다. /security block, /security unblock, /security blocklist는 짧은 명령어로 AutoMod 차단 목록을 관리합니다. 운영진은 메시지의 컨텍스트 메뉴 항목 Mark as scam 또는 learn_emoji로 정한 이모지 반응으로 사기 방지 모듈을 학습시킬 수 있습니다. 메시지는 삭제되고, 그 이미지와 텍스트는 이후 즉시 삭제됩니다. 각 기능은 해당 모듈이나 설정에서 끌 수 있습니다.

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

### 패널

패널은 환영 글, 규칙, 역할 선택, 알림 버튼, 인증처럼 배너 이미지, 텍스트 상자, 버튼으로 이루어진 게시물입니다. `/panel` 또는 대시보드의 Panels 페이지에서 만듭니다. 이미지는 그곳이나 명령어 옵션으로 올리며, 봇이 `data/panels`에 저장하므로 계속 작동합니다.

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

템플릿: empty, welcome, rules, roles, notifications, verify. 텍스트는 서버 언어로 되어 있고 바꿀 수 있습니다. `/panel section`은 제목, 본문, 바닥글 입력 양식을 엽니다. 각 섹션은 하나의 메시지가 됩니다. 배너는 상자 위, 큰 이미지는 상자 안, 작은 이미지는 오른쪽 위에 표시됩니다. 버튼은 마지막 섹션 아래에 한 줄에 다섯 개씩 놓입니다. 역할 버튼은 역할을 주거나 다시 가져가며, `single`을 켜면 패널의 다른 역할은 제거됩니다. verify 버튼은 인증 모듈의 인증을 시작합니다(`/access verify setup`에서 버튼, 캡차, 계산 중에서 고릅니다). 텍스트에는 `{server}`와 `{count}`를 쓸 수 있습니다. 수정한 뒤 `/panel update`로 게시된 메시지를 바꿉니다. 서버당 한도: 패널 25개, 패널당 섹션 5개와 버튼 20개, 8 MB 이하 이미지 40장. 봇은 자신의 최고 역할보다 낮고 위험한 권한이 없는 역할만 제공합니다.

### 스킬과 AI

스킬은 서버가 안전한 블록으로 직접 만드는 명령어, 게임, 자동화입니다. AI가 필요 없고 코드를 실행하는 일도 결코 없습니다. AI는 선택 사항입니다. 본인의 키로 설명을 바탕으로 스킬을 작성하게 하거나, 스캠 방지 검사에서 2차 의견을 받을 수 있습니다.

AI 없는 스킬:

- `/support skill create kind:command name:hello`는 수정할 수 있는 작은 예시가 담긴 입력창을 엽니다. `/support skill edit`, `show`, `import`, `enable`, `disable`, `delete`, `list`, `stats`로 관리합니다. 누구나 `/support skill run` 또는 접두사(예: `!hello`)로 스킬을 사용합니다. `/support skill panel`은 스킬을 실행하는 버튼을 게시합니다.
- 종류: 명령어(동작 목록), 게임(주사위, 선택, 슬롯, 가위바위보, 퀴즈), 자동화(멤버가 들어오거나 나갈 때, 메시지에 특정 단어가 있을 때, 버튼을 누를 때 시작).
- 동작: 답장, 채널로 보내기, 개인 메시지, 로그, 역할 추가 또는 제거, 카운터 변경, 코인 지급, 무작위 선택. 동작에는 조건을 둘 수 있습니다: 역할 보유, 확률, 카운터와 숫자의 비교.
- 텍스트에는 `{user}`, `{user_name}`, `{server}`, `{channel}`, `{count}`, `{arg1}`, `{arg2}`, `{var:name}`, `{uvar:name}`, `{random:1-6}`을 쓸 수 있습니다.
- 제한: 서버당 스킬 50개, 스킬당 동작 10개, 역할 변경 3회, 메시지 4개. 봇은 자신의 최고 역할보다 낮고 위험한 권한이 없는 역할만 부여합니다. 코인을 지급하는 스킬은 최소 60초의 쿨다운이 필요합니다. 봇 명령어, 별칭, 태그의 이름은 사용할 수 없습니다.
- 스킬은 JSON으로 저장되며 설정 내보내기에 포함됩니다. 알 수 없는 필드는 거부되므로, 어디서 온 스킬이든 블록이 허용하는 일만 할 수 있습니다.

예시: 역할을 부여하고 사용 횟수를 세는 명령어(역할 ID를 바꾸세요):

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

AI 연결(선택):

- `/support ai setup provider:kimi agree:true`는 API 키를 입력하는 비공개 입력창을 엽니다. 제공업체는 Anthropic, OpenAI, Kimi(Moonshot)입니다. 모델이 제안되며 같은 명령어나 대시보드에서 바꿀 수 있습니다. 모델 이름은 제공업체에서 바뀌므로 해당 문서를 확인하세요. 비용은 제공업체에 직접 지불합니다.
- `/support ai make wish:...`는 AI에게 스킬을 요청하고, 가져온 스킬과 똑같이 엄격하게 응답을 검사한 뒤 미리보기를 보여 줍니다. 저장을 누르기 전에는 아무것도 저장되지 않습니다.
- `/support ai status`, `limits`(하루 요청 수, 사람당 요청 간격 초), `remove`로 구성이 완성됩니다. 키는 암호화되어 저장되며 비밀 값은 `data/ai.secret` 파일에 있습니다. 이 파일을 백업과 함께 보관하세요. 없으면 저장된 키를 읽을 수 없어 다시 입력해야 합니다. 키는 표시, 기록, 내보내기가 되지 않습니다. 제공업체는 새 키와 함께만 바꿀 수 있으므로 키가 다른 제공업체로 전송되는 일은 없습니다.
- 전송되는 내용: `/support ai make`의 요청 내용과, 2차 의견에서는 의심스러운 메시지의 텍스트입니다. 그 외에는 전송되지 않으며, `ai` 모듈이 켜져 있는 동안에만 해당합니다. [PRIVACY.md](../PRIVACY.md)를 참고하세요.

스캠 방지 학습:

- 학습 필터(`/security antiscam set learned:true`)는 서버마다 하나인 작은 분류기입니다. 관리자는 컨텍스트 메뉴 항목 "Mark as scam"과 "Not a scam"으로 학습시킵니다. 단어의 짧은 해시만 저장하고 텍스트는 저장하지 않으며, 스캠 8개와 정상 30개를 본 뒤에야 동작하고 그때도 95퍼센트를 넘을 때만 작동합니다. `ham_sampling`을 켜면 정상 메시지 열 개 중 하나에서도 학습합니다.
- 유사 이미지(`similar`, 기본 켜짐)는 이미지 지문을 알려진 스캠 이미지와 비교하므로, 다시 저장하거나 크기를 바꾼 사본도 찾아냅니다. Tesseract 없이 동작합니다.
- AI 2차 의견(`/support ai limits second_opinion:true`): 기준 바로 아래인 경우나 학습 필터가 의심스럽다고 본 경우에 AI에게 묻습니다. AI가 80퍼센트 이상의 확신으로 스캠이라고 답할 때만 메시지가 삭제되며, AI의 응답이 다른 일을 일으킬 수는 없습니다.

### 메시지 빌더와 업데이트

메시지 빌더는 JSON으로 여러 임베드와 링크 버튼이 있는 메시지를 게시합니다. Embed Generator 같은 임베드 생성기가 내보내는 JSON을 읽으므로, 그곳에서 메시지를 디자인하고 봇으로 게시할 수 있습니다. JSON은 텍스트, .json 파일, 또는 JSON을 바로 가리키는 https 링크(예: 저장소의 원본 파일)로 전달하세요. 리디렉션되는 링크는 거부됩니다. 링크 버튼만 만들어지고, 상호작용이 필요한 버튼은 건너뜁니다. 모든 링크는 http 또는 https여야 하고, 텍스트의 멘션은 알림을 보내지 않으며, Discord의 제한이 적용됩니다. /post message copy는 기존 메시지를 JSON으로 내보내고, /post message edit는 봇의 메시지를 수정하며, /post message preview는 결과를 나에게만 보여 줍니다. 웹 편집기의 공유 링크는 형식이 공개되어 있지 않으므로 열지 않습니다.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

봇은 12시간마다 update.repo(scripts/set_repo_url.py로 설정)의 GitHub 저장소에 더 새로운 릴리스가 있는지 확인합니다. 있으면 봇 소유자에게 릴리스 노트가 담긴 개인 메시지가 가고, 릴리스를 내려받아 검사합니다. 검사 항목은 릴리스의 SHA-256 체크섬, 압축 파일 안의 안전한 경로, 태그와 일치하는 버전입니다. 설치는 /server debug update action:install로 하거나, auto_install이 켜져 있으면 자동으로 이루어집니다. 설치 전에 교체될 파일이 data/update에 저장되고, 새 패키지가 설치되며, 새 코드를 시험 삼아 불러옵니다. 어느 단계든 실패하면 이전 파일이 복원됩니다. .env, settings.json, data, music은 절대 건드리지 않습니다. 이후 봇이 스스로 다시 시작합니다. Docker에서는 제자리 설치를 하지 않으니 이미지를 업데이트하세요. 업데이트는 저장소의 코드를 실행하므로 신뢰하는 저장소만 지정하세요. enabled를 false로 하면 끌 수 있습니다.

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

### 운영

봇은 몇 초마다 데이터를 저장하고 data/dbbackups에 데이터베이스 백업을 보관합니다(데이터 형식 변경 전 1개, 하루 1개). 음악 대기열, 고정 메시지, 관리자 카운터는 재시작 후에도 유지됩니다. 대형 봇은 여러 샤드로 실행할 수 있습니다. heartbeat 파일과 선택 사항인 상태 페이지는 모니터링 도구에 도움이 됩니다. 이 옵션은 settings.json에서 설정합니다:

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

로그는 data/guardbot.log 에 기록됩니다(순환 저장, log_max_mb 와 log_backups 참조). log_format 을 json 으로 설정하면 서버와 명령이 담긴 JSON 객체가 한 줄에 하나씩 기록됩니다. health_port 를 설정하면 /metrics 가 Prometheus 지표(가동 시간, 지연, 메모리, 데이터베이스 크기, 오류, 명령 사용 횟수와 소요 시간, 작업 레인)를 제공합니다. 숫자만 내보내며 이름이나 ID는 포함하지 않고, metrics_token 을 설정하면 bearer 토큰이 필요합니다. 무거운 작업(이미지 읽기, 카드 그리기, 음악 파일, 백업)은 스레드 수와 한도가 정해진 레인에서 실행됩니다(settings.json 의 workers). 레인이 가득 차면 작업을 쌓지 않고 바쁘다고 응답합니다. 모든 데이터베이스 백업은 만들어진 직후 열어서 검사합니다. 복원하려면 봇을 멈추고 다음을 실행하세요:

```
python scripts/restore_db.py data/dbbackups/guardbot-YYYYMMDD-HHMMSS-auto.db
python scripts/restore_db.py BACKUPFILE --check          # only check a backup
```

현재 데이터베이스는 before-restore 라는 이름의 백업으로 보관됩니다.

### 서버 관리

모듈과 명령어를 켜고 끄고, 접두사를 바꾸고, 별칭을 정하고, 명령어를 역할로 제한합니다.

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

## 메시지 자리표시자

설정한 텍스트 안에서 다음 자리표시자가 치환됩니다:

```
/community welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/community booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/community tempvoice setup     name                            {name}
/access jailsetup notice    text                            {staff}
```

## 설정

전역 옵션은 settings.json에서 설정합니다. 나머지는 /admin module, /admin command, /admin perms, /admin alias, /admin config 같은 명령어로 서버별로 설정합니다.

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

모든 설정은 /admin config로 읽고 바꿀 수 있습니다. 가장 자주 쓰는 경로는 다음과 같습니다:

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
    defaults/             default settings, one file per area (core, security, moderation, community) and base.py for modules and permissions
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature, in the folders security, moderation, server, community, tools
    skills.py             스킬 엔진: 스킬을 검사하고 실행
    ai.py                 AI 제공업체, 암호화된 키, 제한
    learner.py, imgsim.py 스캠 방지 학습 필터, 이미지 지문
    dashboard_manage.py   명령어, 스킬, AI, 프로필용 대시보드 페이지
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
- 멤버는 /info mydata로 자신의 데이터를 내보내고 삭제할 수 있습니다. 관리자는 떠난 멤버의 데이터를 얼마나 보관할지 정할 수 있습니다.
- AI 기능은 본인의 키를 추가하기 전까지 꺼져 있습니다. 추가한 뒤에도 선택한 제공업체로 전송되는 것은 `/support ai make`의 텍스트와 2차 의견의 의심스러운 메시지뿐입니다.
- [PRIVACY.md](../PRIVACY.md)

## 지원

버그, 아이디어, 제안은 Discord @justyyin 으로 연락하거나 GitHub에 issue를 등록해 주세요.

## 크레딧

GuardBot은 Merlin Fuchs의 [Embed Generator](https://github.com/merlinfuchs/embed-generator)(MIT 라이선스, message.style에서 제공)에서 영감을 받았습니다. 메시지 빌더는 같은 JSON 형식을 읽으므로 그곳에서 만든 메시지를 이 봇으로 게시할 수 있습니다. 해당 프로젝트의 코드는 포함되어 있지 않습니다. discord.py, aiohttp, Pillow, yt-dlp, mutagen, Tesseract의 제작자에게 감사드립니다.

## 라이선스

MIT 라이선스로 공개되어 있습니다. 참조: [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
