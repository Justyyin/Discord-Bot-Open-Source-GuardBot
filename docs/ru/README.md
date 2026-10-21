# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | **Русский** | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Самостоятельно размещаемый Discord-бот для модерации, безопасности и сообщества. Открытый исходный код, бесплатно, а ваши данные остаются на вашем компьютере.

<!-- toc -->

- [О проекте](#о-проекте)
- [Возможности](#возможности)
  - [Безопасность](#безопасность)
  - [Модерация](#модерация)
  - [Журналирование](#журналирование)
  - [Сообщество](#сообщество)
  - [Администрирование](#администрирование)
- [Состояние проекта](#состояние-проекта)
- [Требования](#требования)
- [Быстрый старт](#быстрый-старт)
- [Права бота](#права-бота)
- [Первые шаги в Discord](#первые-шаги-в-discord)
- [Команды](#команды)
  - [Модерация](#модерация-1)
  - [Гулаг (jail)](#гулаг-jail)
  - [Автомодерация](#автомодерация)
  - [Защита от рейдов и блокировка](#защита-от-рейдов-и-блокировка)
  - [Защита от нюка](#защита-от-нюка)
  - [Верификация](#верификация)
  - [Журналирование](#журналирование-1)
  - [Приветствия, прощания и бустеры](#приветствия-прощания-и-бустеры)
  - [Тикеты](#тикеты)
  - [Опросы и розыгрыши](#опросы-и-розыгрыши)
  - [Предложения и starboard](#предложения-и-starboard)
  - [XP и уровни](#xp-и-уровни)
  - [Роли по реакции и уведомления](#роли-по-реакции-и-уведомления)
  - [Дни рождения](#дни-рождения)
  - [Временные голосовые каналы](#временные-голосовые-каналы)
  - [Резервные копии и восстановление](#резервные-копии-и-восстановление)
  - [Данные и конфиденциальность](#данные-и-конфиденциальность)
  - [Администрирование](#администрирование-1)
- [Подстановки в сообщениях](#подстановки-в-сообщениях)
- [Настройка](#настройка)
- [Данные и хранение](#данные-и-хранение)
- [Структура репозитория](#структура-репозитория)
- [Планы](#планы)
- [Конфиденциальность и безопасность](#конфиденциальность-и-безопасность)
- [Поддержка](#поддержка)
- [Лицензия](#лицензия)

<!-- tocstop -->

## О проекте

GuardBot объединяет функции, за которые многие серверы платят у размещённых ботов: модерацию, журналирование, защиту от рейдов и нюков, тикеты, уровни и многое другое. Вы запускаете бота сами, на своём компьютере или на небольшом VPS.

Размещённые боты хранят данные сервера, ID участников и иногда адреса электронной почты у третьей стороны. Если вы запускаете бота сами, эти данные не покидают ваш компьютер. GuardBot должен показать, что любой может запустить полноценного бота без подписки.

## Возможности

### Безопасность

- Автомодерация: фильтр слов, фильтр заглавных букв, спам упоминаниями, ссылки-приглашения, фишинговые домены, личные данные, доксинг и угрозы. Все списки можно редактировать.
- Защита от рейдов с обнаружением волн входов и блокировка всего сервера.
- Защита от нюка: лимиты на массовые удаления и баны, автоматическая реакция и личное сообщение владельцу сервера.
- Канал «гулаг»: участники, публикующие мошеннические ссылки или изображения, перемещаются в один канал с инструкцией по защите аккаунта. Модераторы также могут использовать /jail и /unjail.
- Верификация кнопкой или капчей с автоматическим удалением участников, которые не прошли её вовремя.
- Защита от нюка также следит за выдачей прав, новыми вебхуками, добавленными ботами и переименованием сервера.

### Модерация

- Warn, mute, kick, ban и jail с историей, которую можно фильтровать по упоминанию, ID пользователя или типу.
- Автоматическая эскалация, например три предупреждения приводят к тайм-ауту.
- Настройка того, какие роли или пользователи могут применять каждую команду модерации.

### Журналирование

- Отправленные, изменённые и удалённые сообщения, включая изображения, GIF и URL, с отдельными каналами журнала.
- Изменения ролей, никнеймов, баны, голосовые каналы, каналы и роли сервера.

### Сообщество

- Приветствия и прощания, автороли и награды для бустеров.
- Тикеты, опросы, розыгрыши и предложения.
- Роли по реакции с любыми эмодзи и темы уведомлений, которые участники включают и выключают сами.
- XP и уровни от 1 до 100 за чат и голос, роли за уровни и дни рождения.
- Starboard и временные голосовые каналы.
- Гулаг на заданное время, опросы с множественным выбором, карточки ранга в виде изображений и бонусы XP для ролей.

### Администрирование

- Каждый модуль и каждую команду можно включать и выключать для каждого сервера.
- Собственный префикс, псевдонимы команд и переименование команд.
- Резервное копирование и восстановление ролей и структуры каналов.
- Автоматические резервные копии по расписанию для ролей, каналов, эмодзи и вебхуков, с командой восстановления, которая добавляет только недостающее.

## Состояние проекта

GuardBot ещё молод и пока не использовался на больших серверах. Автоматические тесты (`python -m unittest`) покрывают хранилище, обнаружение личных данных, расчёт уровней, регистрацию команд, проверки прав и ссылки в документации. Всё, что требует настоящего сервера Discord, например блокировка сервера, восстановление из копии, верификация, защита от нюка и гулаг, тестами не покрывается. Сначала проверьте эти функции на тестовом сервере, прежде чем на них полагаться. Переводы документации не проверялись носителями языка, исправления приветствуются.

## Требования

- Python 3.11 или новее
- Приложение Discord с токеном бота
- Компьютер или VPS, который всегда в сети

## Быстрый старт

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Полное пошаговое руководство находится в [GUIDE.md](GUIDE.md).

## Права бота

Проще всего выдать право Администратор. Если нужны минимальные права, выдайте эти и включите интенты Server Members и Message Content в Developer Portal:

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

## Первые шаги в Discord

Разумная начальная настройка. Выполните эти команды на своём сервере и замените каналы и роли своими:

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

## Команды

Большинство команд являются слэш-командами, команды модерации работают и с префиксом. Полный список находится в справочнике команд: [COMMANDS.md](../COMMANDS.md).

### Модерация

Предупреждения, мьюты, кики и баны работают как слэш-команды и с префиксом, например `!warn @User spam`. Каждое действие создаёт нумерованный случай.

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
/case case_id:12

/escalation list
/escalation set warns:3 action:timeout minutes:60  # 3 warnings = 1 hour timeout
/escalation set warns:5 action:kick
/escalation set warns:7 action:ban                 # actions: timeout, kick, ban, jail
/escalation remove warns:5
```

### Гулаг (jail)

Участники со взломанным аккаунтом перемещаются в один канал с инструкцией по безопасности. При освобождении им возвращаются прежние роли.

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
```

### Автомодерация

Правила удаляют сообщения или наказывают за них. Действие выбирается для каждого правила: log, delete, warn, timeout или jail.

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

### Защита от рейдов и блокировка

Обнаруживает много входов за короткое время и может заблокировать сервер. Режим channels меняет каждый канал, режим role действует мгновенно.

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

### Защита от нюка

Следит за журналом аудита и реагирует, когда кто-то разрушает сервер. Владелец получает личное сообщение.

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

### Верификация

Новые участники видят только канал верификации, пока не нажмут кнопку или не решат капчу.

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### Журналирование

Выберите канал для каждой категории или один основной канал для всего.

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### Приветствия, прощания и бустеры

Сообщения, автороли и награды для бустеров сервера.

```
/welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/welcome autorole role:@Member                     # toggle, given to every new member
/welcome botrole role:@Bots                        # toggle, given to every new bot
/welcome test

/booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/booster role role:@Booster                        # toggle
```

### Тикеты

Участники открывают личные каналы кнопкой. При закрытии отправляется стенограмма.

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

### Опросы и розыгрыши

Кнопки для голосования и участия. Длительность принимает значения вроде 30m, 2h и 1d.

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### Предложения и starboard

Участники публикуют предложения, которые команда может принять или отклонить, а популярные сообщения выделяются.

```
/suggestionsetup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
```

### XP и уровни

XP за чат и голос, роли за уровни, бонусы для ролей и карточки ранга.

```
/xp config enabled:True min_xp:15 max_xp:25 cooldown:60 voice_xp:10 multiplier:1.5
/xp config max_level:100 stack_roles:True card:True
/xp config announce:channel announce_channel:#levels message:{user} reached level {level}!
/xp show
/xp boost role:@Booster multiplier:1.5             # 1.0 removes the boost
/xp ignore channel:#spam                           # toggle

/levelrole add level:10 role:@Active
/levelrole add level:50 role:@Veteran
/levelrole remove level:10
/levelrole list
/levelrole sync                                    # apply to everyone who already has XP

/xp give user:@User amount:500
/xp take user:@User amount:100
/xp setlevel user:@User level:20
/xp reset user:@User

/rank                                              # also: !rank, shows a rank card image
/rank user:@User
/leaderboard
```

### Роли по реакции и уведомления

Выдавайте роли за реакции с любыми эмодзи и позволяйте участникам выбирать темы уведомлений.

```
/reactionrole panel channel:#roles title:Pick your roles description:React below
/reactionrole add message:<message link> emoji:<any emoji> role:@Gamer
/reactionrole add message:<message link> emoji:<any emoji> role:@Artist mode:unique
# mode unique: only one role of that message at a time
/reactionrole remove message:<message link> emoji:<any emoji>
/reactionrole list

/notifytopic add key:events role:@Events description:Server events
/notifytopic panel channel:#roles title:Notifications   # one button per topic
/notifytopic remove key:events
/notify subscribe topic:events                     # members choose for themselves
/notify unsubscribe topic:events
/notify list
```

### Дни рождения

Участники указывают день и месяц, бот выдаёт роль и пишет сообщение в этот день.

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Временные голосовые каналы

Вход в канал-хаб создаёт комнату, которая исчезает, когда пустеет.

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Резервные копии и восстановление

Копии содержат роли, каналы, эмодзи, вебхуки и роли участников. Восстановление добавляет только недостающее.

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### Данные и конфиденциальность

Участники могут экспортировать и удалять свои данные. Администраторы задают срок хранения.

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### Администрирование

Включение и выключение модулей и команд, смена префикса, псевдонимы и ограничение команд по ролям.

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

## Подстановки в сообщениях

Эти подстановки заменяются в настраиваемых вами текстах:

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthdaysetup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## Настройка

Глобальные параметры задаются в settings.json. Всё остальное настраивается для каждого сервера командами /module, /command, /perms, /alias и /config.

Чтобы переименовать команду, добавьте её в command_names и перезапустите бота:

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

Любую настройку можно прочитать и изменить командой /config. Вот пути, которые понадобятся чаще всего:

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

## Данные и хранение

Всё, что сохраняет бот, находится на вашем компьютере:

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

## Структура репозитория

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

## Планы

- Локальная веб-панель, которая работает на вашем компьютере, чтобы менять настройки без размещённых сервисов.
- Переведённые сообщения бота.
- Экспорт и импорт настроек.

## Конфиденциальность и безопасность

- Нет телеметрии и внешних сервисов. Бот общается только с Discord.
- Все данные хранятся в папке data на вашем компьютере: настройки, XP, дни рождения (только день и месяц) и случаи модерации.
- Бот игнорирует личные сообщения от участников.
- Токен читается из файла .env. Никому его не передавайте и не публикуйте.
- Участники могут экспортировать и удалять свои данные командой /mydata. Администраторы задают, как долго хранятся данные ушедших участников.
- [PRIVACY.md](../PRIVACY.md)

## Поддержка

Ошибки, идеи и предложения: пишите мне в Discord, @justyyin, или создайте issue на GitHub.

## Лицензия

Опубликовано под лицензией MIT. См. [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
