# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | **한국어**

관리, 보안, 커뮤니티를 위한 자체 호스팅 Discord 봇. 오픈 소스이며 무료이고, 데이터는 내 컴퓨터에만 남습니다.

<!-- toc -->

- [프로젝트 소개](#프로젝트-소개)
- [기능](#기능)
  - [보안](#보안)
  - [관리](#관리)
  - [로그](#로그)
  - [커뮤니티](#커뮤니티)
  - [운영](#운영)
- [프로젝트 상태](#프로젝트-상태)
- [요구 사항](#요구-사항)
- [빠른 시작](#빠른-시작)
- [저장소 구조](#저장소-구조)
- [명령어](#명령어)
- [설정](#설정)
- [로드맵](#로드맵)
- [개인정보 및 보안](#개인정보-및-보안)
- [지원](#지원)
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

## 빠른 시작

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

자세한 단계별 안내는 다음 문서에 있습니다: [GUIDE.md](GUIDE.md).

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

## 명령어

대부분의 명령어는 슬래시 명령어이며, 관리 명령어는 접두사로도 사용할 수 있습니다. 전체 목록은 명령어 참조에 있습니다: [COMMANDS.md](../COMMANDS.md).

## 설정

전역 옵션은 settings.json에서 설정합니다. 나머지는 /module, /command, /perms, /alias, /config 같은 명령어로 서버별로 설정합니다.

명령어 이름을 바꾸려면 command_names에 추가하고 봇을 다시 시작하세요:

```json
{
  "prefix": "!",
  "command_names": {
    "warn": "verwarnen"
  }
}
```

## 로드맵

- 내 컴퓨터에서 실행되는 로컬 웹 대시보드. 호스팅 서비스 없이 설정을 바꿀 수 있습니다.
- 봇 메시지 번역.
- 설정 내보내기 및 가져오기.

## 개인정보 및 보안

- 원격 측정도 외부 서비스도 없습니다. 봇은 Discord와만 통신합니다.
- 모든 데이터는 내 컴퓨터의 data 폴더에 저장됩니다. 설정, XP, 생일(일과 월만), 관리 기록입니다.
- 봇은 멤버가 보내는 다이렉트 메시지를 무시합니다.
- 토큰은 .env 파일에서 읽습니다. 절대 공유하거나 업로드하지 마세요.
- 멤버는 /mydata로 자신의 데이터를 내보내고 삭제할 수 있습니다. 관리자는 떠난 멤버의 데이터를 얼마나 보관할지 정할 수 있습니다.
- [PRIVACY.md](../PRIVACY.md)

## 지원

버그, 아이디어, 제안은 Discord @justyyin 으로 연락하거나 GitHub에 issue를 등록해 주세요.

## 라이선스

MIT 라이선스로 공개되어 있습니다. 참조: [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
