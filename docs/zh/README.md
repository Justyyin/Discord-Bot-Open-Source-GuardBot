# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | **中文** | [日本語](../ja/README.md) | [한국어](../ko/README.md)

自行托管的 Discord 机器人，用于管理、安全和社区。开源、免费，数据只保存在你自己的电脑上。

<!-- toc -->

- [关于项目](#关于项目)
- [功能](#功能)
  - [安全](#安全)
  - [管理](#管理)
  - [日志](#日志)
  - [社区](#社区)
  - [运维](#运维)
- [运行要求](#运行要求)
- [快速开始](#快速开始)
- [仓库结构](#仓库结构)
- [命令](#命令)
- [配置](#配置)
- [路线图](#路线图)
- [隐私与安全](#隐私与安全)
- [支持](#支持)
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
- 古拉格频道：发布诈骗链接或图片的成员会被移入唯一的频道，并看到账号安全指引。管理员也可以使用 /jail 和 /unjail。

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

### 运维

- 每个模块和每个命令都可以按服务器开启或关闭。
- 自定义前缀、命令别名和可重命名的命令。
- 身份组和频道结构的备份与恢复。

## 运行要求

- Python 3.11 或更高版本
- 带有机器人令牌的 Discord 应用
- 一台持续在线的电脑或 VPS

## 快速开始

```
git clone https://github.com/YOUR-NAME/guardbot.git
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

完整的分步指南见 [GUIDE.md](GUIDE.md).

## 仓库结构

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
    cogs/                 one file per feature group
  docs/                   documentation in 12 languages
  deploy/                 systemd service, Dockerfile, compose file
  scripts/                maintenance scripts
  data/                   created at runtime, holds your settings and data
```

## 命令

大多数命令是斜杠命令，管理命令也支持前缀。完整列表见命令参考： [COMMANDS.md](../COMMANDS.md).

## 配置

全局选项在 settings.json 中设置。其余内容按服务器通过 /module、/command、/perms、/alias 和 /config 等命令配置。

要重命名命令，请把它加入 command_names 并重启机器人：

```json
{
  "prefix": "!",
  "command_names": {
    "warn": "verwarnen"
  }
}
```

## 路线图

- 在你自己的电脑上运行的本地网页控制台，无需任何托管服务即可修改设置。
- 机器人消息的多语言翻译。
- 设置的导出与导入。

## 隐私与安全

- 没有遥测，也没有外部服务。机器人只与 Discord 通信。
- 所有数据都保存在你电脑的 data 文件夹中：设置、经验、生日（仅日期和月份）以及管理记录。
- 机器人会忽略成员发来的私信。
- 令牌从 .env 文件读取。切勿分享或上传。
- 成员可以用 /birthday remove 自行删除自己的生日。

## 支持

错误、想法和建议：请在 Discord 上联系我，@justyyin，或在 GitHub 上提交 issue。

## 许可证

基于 MIT 许可证发布。参见 [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany

<!-- GuardBot (c) Justyn -->
