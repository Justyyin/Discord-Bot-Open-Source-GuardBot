# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | **Українська** | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Бот для Discord, який ви розміщуєте самостійно, для модерації, безпеки та спільноти. Відкритий код, безкоштовно, а ваші дані залишаються на вашому комп'ютері.

<!-- toc -->

- [Про проєкт](#про-проєкт)
- [Можливості](#можливості)
  - [Безпека](#безпека)
  - [Модерація](#модерація)
  - [Журналювання](#журналювання)
  - [Спільнота](#спільнота)
  - [Адміністрування](#адміністрування)
- [Стан проєкту](#стан-проєкту)
- [Вимоги](#вимоги)
- [Швидкий старт](#швидкий-старт)
- [Права бота](#права-бота)
- [Перші кроки в Discord](#перші-кроки-в-discord)
- [Команди](#команди)
  - [Модерація](#модерація-1)
  - [Гулаг (jail)](#гулаг-jail)
  - [Автомодерація](#автомодерація)
  - [Захист від рейдів і блокування](#захист-від-рейдів-і-блокування)
  - [Захист від нюку](#захист-від-нюку)
  - [Верифікація](#верифікація)
  - [Журналювання](#журналювання-1)
  - [Привітання, прощання та бустери](#привітання-прощання-та-бустери)
  - [Тікети](#тікети)
  - [Опитування та розіграші](#опитування-та-розіграші)
  - [Пропозиції та starboard](#пропозиції-та-starboard)
  - [XP і рівні](#xp-і-рівні)
  - [Ролі за реакцію та сповіщення](#ролі-за-реакцію-та-сповіщення)
  - [Дні народження](#дні-народження)
  - [Тимчасові голосові канали](#тимчасові-голосові-канали)
  - [Резервні копії та відновлення](#резервні-копії-та-відновлення)
  - [Дані та конфіденційність](#дані-та-конфіденційність)
  - [Адміністрування](#адміністрування-1)
- [Підстановки в повідомленнях](#підстановки-в-повідомленнях)
- [Налаштування](#налаштування)
- [Дані та зберігання](#дані-та-зберігання)
- [Структура репозиторію](#структура-репозиторію)
- [Плани](#плани)
- [Конфіденційність і безпека](#конфіденційність-і-безпека)
- [Підтримка](#підтримка)
- [Ліцензія](#ліцензія)

<!-- tocstop -->

## Про проєкт

GuardBot об'єднує функції, за які багато серверів платять у розміщених ботів: модерацію, журналювання, захист від рейдів і нюків, тікети, рівні та багато іншого. Ви запускаєте бота самі, на власному комп'ютері або на невеликому VPS.

Розміщені боти зберігають дані сервера, ID учасників і подекуди адреси електронної пошти в третьої сторони. Якщо ви розміщуєте бота самі, ці дані не залишають ваш комп'ютер. GuardBot має показати, що будь-хто може запустити повноцінного бота без підписки.

## Можливості

### Безпека

- Автомодерація: фільтр слів, фільтр великих літер, спам згадками, запрошувальні посилання, фішингові домени, особисті дані, доксинг і погрози. Усі списки можна редагувати.
- Захист від рейдів з виявленням хвиль входів і блокування всього сервера.
- Захист від нюку: ліміти на масові видалення та бани, автоматична реакція і приватне повідомлення власнику сервера.
- Канал «гулаг»: учасники, які публікують шахрайські посилання чи зображення, переміщуються в один канал з інструкцією із захисту акаунта. Модератори також можуть використовувати /jail і /unjail.
- Верифікація кнопкою або капчею з автоматичним видаленням учасників, які не пройшли її вчасно.
- Захист від нюку також стежить за видачею прав, новими вебхуками, доданими ботами та перейменуванням сервера.

### Модерація

- Warn, mute, kick, ban і jail з історією, яку можна фільтрувати за згадкою, ID користувача або типом.
- Автоматична ескалація, наприклад три попередження призводять до тайм-ауту.
- Налаштування того, які ролі чи користувачі можуть застосовувати кожну команду модерації.

### Журналювання

- Надіслані, змінені та видалені повідомлення, зокрема зображення, GIF і URL, з окремими каналами журналу.
- Зміни ролей, нікнеймів, бани, голосові канали, канали та ролі сервера.

### Спільнота

- Привітання й прощання, авторолі та нагороди для бустерів.
- Тікети, опитування, розіграші та пропозиції.
- Ролі за реакцію з будь-якими емодзі та теми сповіщень, які учасники вмикають і вимикають самі.
- XP і рівні від 1 до 100 за чат і голос, ролі за рівні та дні народження.
- Starboard і тимчасові голосові канали.
- Гулаг на заданий час, опитування з множинним вибором, картки рангу у вигляді зображень і бонуси XP для ролей.

### Адміністрування

- Кожен модуль і кожну команду можна вмикати та вимикати для кожного сервера.
- Власний префікс, псевдоніми команд і перейменування команд.
- Резервне копіювання та відновлення ролей і структури каналів.
- Автоматичні резервні копії за розкладом для ролей, каналів, емодзі та вебхуків, із командою відновлення, яка додає лише те, чого бракує.

## Стан проєкту

GuardBot ще молодий і поки що не використовувався на великих серверах. Автоматичні тести (`python -m unittest`) охоплюють сховище, виявлення особистих даних, розрахунок рівнів, реєстрацію команд, перевірки прав і посилання в документації. Усе, що потребує справжнього сервера Discord, наприклад блокування сервера, відновлення з копії, верифікація, захист від нюку та гулаг, тестами не охоплюється. Спершу перевірте ці функції на тестовому сервері, перш ніж на них покладатися. Переклади документації не перевіряли носії мови, виправлення вітаються.

## Вимоги

- Python 3.11 або новіший
- Застосунок Discord із токеном бота
- Комп'ютер або VPS, що завжди в мережі

## Швидкий старт

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Повний покроковий посібник міститься в [GUIDE.md](GUIDE.md).

## Права бота

Найпростіше видати право Адміністратор. Якщо потрібні мінімальні права, видайте ці та увімкніть інтенти Server Members і Message Content у Developer Portal:

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

## Перші кроки в Discord

Розумне початкове налаштування. Виконайте ці команди на своєму сервері та замініть канали й ролі своїми:

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

## Команди

Більшість команд є слеш-командами, команди модерації працюють і з префіксом. Повний список міститься в довіднику команд: [COMMANDS.md](../COMMANDS.md).

### Модерація

Попередження, м'юти, кіки та бани працюють як слеш-команди й з префіксом, наприклад `!warn @User spam`. Кожна дія створює пронумерований випадок.

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

Учасники зі зламаним акаунтом переміщуються в один канал з інструкцією щодо безпеки. Під час звільнення їм повертаються колишні ролі.

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
```

### Автомодерація

Правила видаляють повідомлення або карають за них. Дію обирають для кожного правила: log, delete, warn, timeout або jail.

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

### Захист від рейдів і блокування

Виявляє багато входів за короткий час і може заблокувати сервер. Режим channels змінює кожен канал, режим role діє миттєво.

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

### Захист від нюку

Стежить за журналом аудиту й реагує, коли хтось руйнує сервер. Власник отримує приватне повідомлення.

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

### Верифікація

Нові учасники бачать лише канал верифікації, доки не натиснуть кнопку або не розв'яжуть капчу.

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### Журналювання

Оберіть канал для кожної категорії або один основний канал для всього.

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### Привітання, прощання та бустери

Повідомлення, авторолі та нагороди для бустерів сервера.

```
/welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/welcome autorole role:@Member                     # toggle, given to every new member
/welcome botrole role:@Bots                        # toggle, given to every new bot
/welcome test

/booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/booster role role:@Booster                        # toggle
```

### Тікети

Учасники відкривають приватні канали кнопкою. Під час закриття надсилається стенограма.

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

### Опитування та розіграші

Кнопки для голосування й участі. Тривалість приймає значення на кшталт 30m, 2h і 1d.

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### Пропозиції та starboard

Учасники публікують пропозиції, які команда може схвалити або відхилити, а популярні повідомлення виділяються.

```
/suggestionsetup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
```

### XP і рівні

XP за чат і голос, ролі за рівні, бонуси для ролей і картки рангу.

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

### Ролі за реакцію та сповіщення

Видавайте ролі за реакції з будь-якими емодзі й дозвольте учасникам обирати теми сповіщень.

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

### Дні народження

Учасники вказують день і місяць, бот видає роль і пише повідомлення цього дня.

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Тимчасові голосові канали

Вхід у канал-хаб створює кімнату, яка зникає, коли порожніє.

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Резервні копії та відновлення

Копії містять ролі, канали, емодзі, вебхуки та ролі учасників. Відновлення додає лише те, чого бракує.

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### Дані та конфіденційність

Учасники можуть експортувати й видаляти свої дані. Адміністратори задають строк зберігання.

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### Адміністрування

Вмикання й вимикання модулів і команд, зміна префікса, псевдоніми та обмеження команд за ролями.

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

## Підстановки в повідомленнях

Ці підстановки замінюються в налаштованих вами текстах:

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthdaysetup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## Налаштування

Глобальні параметри задаються в settings.json. Усе інше налаштовується для кожного сервера командами /module, /command, /perms, /alias і /config.

Щоб перейменувати команду, додайте її до command_names і перезапустіть бота:

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

Будь-яке налаштування можна прочитати й змінити командою /config. Ось шляхи, які знадобляться найчастіше:

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

## Дані та зберігання

Усе, що зберігає бот, міститься на вашому комп'ютері:

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

## Структура репозиторію

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

## Плани

- Локальна веб-панель, що працює на вашому комп'ютері, щоб змінювати налаштування без розміщених сервісів.
- Перекладені повідомлення бота.
- Експорт та імпорт налаштувань.

## Конфіденційність і безпека

- Жодної телеметрії та зовнішніх сервісів. Бот спілкується лише з Discord.
- Усі дані зберігаються в папці data на вашому комп'ютері: налаштування, XP, дні народження (лише день і місяць) та випадки модерації.
- Бот ігнорує приватні повідомлення від учасників.
- Токен читається з файлу .env. Нікому його не передавайте і не публікуйте.
- Учасники можуть експортувати й видаляти свої дані командою /mydata. Адміністратори задають, як довго зберігаються дані тих, хто пішов.
- [PRIVACY.md](../PRIVACY.md)

## Підтримка

Помилки, ідеї та пропозиції: пишіть мені в Discord, @justyyin, або створіть issue на GitHub.

## Ліцензія

Опубліковано за ліцензією MIT. Див. [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
