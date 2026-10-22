# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | **Русский** | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Самостоятельно размещаемый Discord-бот для модерации, безопасности и сообщества. Открытый исходный код, бесплатно, а ваши данные остаются на вашем компьютере.

> Бета: GuardBot и его панель управления находятся в стадии беты. Они не были тщательно протестированы, особенно на больших серверах и во всех ситуациях Discord. Возможны ошибки, делайте резервные копии папки data и сообщайте о проблемах. Использование на свой риск.

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
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Скрипты запуска и автозапуск](#скрипты-запуска-и-автозапуск)
  - [Обновление](#обновление)
- [Права бота](#права-бота)
- [Первые шаги в Discord](#первые-шаги-в-discord)
- [Панель управления](#панель-управления)
  - [Настройка панели](#настройка-панели)
  - [Безопасность](#безопасность-1)
  - [Панель на VPS](#панель-на-vps)
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
  - [Инструменты модератора](#инструменты-модератора)
  - [Информация](#информация)
  - [Объявления, теги и напоминания](#объявления-теги-и-напоминания)
  - [Мод-почта и апелляции на бан](#мод-почта-и-апелляции-на-бан)
  - [Канал счёта, закреплённые сообщения и статистика](#канал-счёта-закреплённые-сообщения-и-статистика)
  - [Дополнительные возможности существующих функций](#дополнительные-возможности-существующих-функций)
  - [Другие инструменты AutoMod](#другие-инструменты-automod)
  - [Лимиты модераторов и аудит прав](#лимиты-модераторов-и-аудит-прав)
  - [Жалобы и отслеживание приглашений](#жалобы-и-отслеживание-приглашений)
  - [Диагностика и отладка](#диагностика-и-отладка)
  - [Музыка](#музыка)
  - [Настройка и проверка состояния](#настройка-и-проверка-состояния)
  - [Экономика](#экономика)
  - [Меню ролей, отложенные сообщения и ленты](#меню-ролей-отложенные-сообщения-и-ленты)
  - [Активность, массовые действия и поиск дел](#активность-массовые-действия-и-поиск-дел)
  - [Защита от мошенничества и крипто-скама](#защита-от-мошенничества-и-крипто-скама)
  - [Испытательный срок, обнаружение роя, хронология и обучение](#испытательный-срок-обнаружение-роя-хронология-и-обучение)
  - [Конструктор сообщений и обновления](#конструктор-сообщений-и-обновления)
  - [Эксплуатация](#эксплуатация)
  - [Администрирование](#администрирование-1)
- [Подстановки в сообщениях](#подстановки-в-сообщениях)
- [Настройка](#настройка)
- [Данные и хранение](#данные-и-хранение)
- [Структура репозитория](#структура-репозитория)
- [Переводы](#переводы)
- [Планы](#планы)
- [Конфиденциальность и безопасность](#конфиденциальность-и-безопасность)
- [Поддержка](#поддержка)
- [Благодарности](#благодарности)
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
- Защита от мошенничества: поддельные розыгрыши и крипто-скам удаляются в тексте и на изображениях за миллисекунды, включая скам с MrBeast при любом написании.

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
- Экономика с магазином, меню ролей с кнопками или списком, отложенные сообщения, ленты YouTube, Twitch и RSS, статистика активности и пошаговый /setup. Сообщения для участников доступны на 12 языках.

### Администрирование

- Каждый модуль и каждую команду можно включать и выключать для каждого сервера.
- Собственный префикс, псевдонимы команд и переименование команд.
- Резервное копирование и восстановление ролей и структуры каналов.
- Автоматические резервные копии по расписанию для ролей, каналов, эмодзи и вебхуков, с командой восстановления, которая добавляет только недостающее.
- Панель управления: изменение настроек каждого сервера в браузере после входа через Discord, только для участников, управляющих сервером, и только пока бот подключён.

## Состояние проекта

GuardBot ещё молод и пока не использовался на больших серверах. Автоматические тесты (`python -m unittest`) покрывают хранилище, обнаружение личных данных, расчёт уровней, регистрацию команд, проверки прав и ссылки в документации. Всё, что требует настоящего сервера Discord, например блокировка сервера, восстановление из копии, верификация, защита от нюка и гулаг, тестами не покрывается. Сначала проверьте эти функции на тестовом сервере, прежде чем на них полагаться. Переводы документации не проверялись носителями языка, исправления приветствуются.

## Требования

- Python 3.11 или новее
- Приложение Discord с токеном бота
- Компьютер или VPS, который всегда в сети
- ffmpeg (только для модуля музыки)
- tesseract-ocr (необязательно, только для чтения текста на изображениях)

## Быстрый старт

Выберите свою систему. Для любого варианта нужны Python 3.11 или новее и токен вашего бота. Подробное пошаговое руководство находится в [GUIDE.md](GUIDE.md).

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

### Скрипты запуска и автозапуск

Скрипты запуска создают виртуальное окружение, устанавливают пакеты и запускают бота. При первом запуске они создают файл .env и останавливаются, чтобы вы могли вписать токен. После этого запустите их снова.

```bash
./start.sh
```

```bat
start.bat
```

Чтобы бот продолжал работать после перезагрузки компьютера, используйте службу. Linux (systemd) и macOS (launchd):

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

В Windows создайте в Планировщике заданий задачу, которая запускает start.bat при входе в систему, или используйте обёртку для служб, например NSSM. Для Docker см. [GUIDE.md](GUIDE.md).

### Обновление

Остановите бота, выполните эти команды и запустите его снова. Ваши данные в папке data остаются нетронутыми, а перед каждым изменением формата данных бот делает резервную копию базы.

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

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

## Панель управления

Панель управления — это веб-страница, которая работает внутри бота. После входа через Discord вы меняете настройки своих серверов переключателями, меню и полями вместо команд: модули, каналы, роли, пороговые значения, тексты, префикс и язык. Она также показывает последние дела модерации, экспортирует и импортирует настройки. Она одинаково работает на вашем компьютере и на VPS и выключена, пока вы её не включите.

### Настройка панели

1. Откройте своё приложение в Developer Portal, перейдите в OAuth2 и скопируйте Client Secret в файл .env.
2. На той же странице добавьте адрес перенаправления http://localhost:8080/callback.
3. Включите панель в settings.json.
4. Перезапустите бота и откройте http://localhost:8080 в браузере. Войдите через Discord.

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

### Безопасность

- Вход только через Discord (OAuth2, область identify). Токен доступа сразу отзывается и никогда не сохраняется.
- Доступ имеют только владелец сервера и участники с правом «Администратор» или «Управлять сервером», и только к этому серверу. Право проверяется заново при каждом запросе.
- Открыть можно только серверы, к которым бот подключён в данный момент. Если бот не в сети, не на сервере или ещё запускается, панель отказывает во всём. Она работает внутри бота и не имеет собственной базы данных или службы.
- По умолчанию она слушает только 127.0.0.1, поэтому больше никто в сети не может к ней обратиться. Публичный адрес принимается только с HTTPS, иначе панель не запускается.
- Сессии используют случайный токен в cookie HttpOnly с SameSite и, при HTTPS, с префиксом __Host-. Они заканчиваются через 8 часов и хранятся только в памяти, поэтому перезапуск завершает все сессии.
- Каждое изменение требует CSRF-токен и подходящий Origin. Заголовок Host проверяется против DNS rebinding. Страница не загружает внешние скрипты, строгая Content Security Policy блокирует встроенный код, запросы ограничены по частоте, а тело запроса ограничено 256 КБ.
- Каждое значение проверяется по типу настройки, а ID Discord должны существовать на сервере. Внутреннее состояние, такое как счётчики, тикеты и сохранённые записи, изменить нельзя. Каждое изменение записывается в канал журнала безопасности сервера.
- Содержимое сообщений никогда не показывается. Дела модерации доступны только для чтения.

### Панель на VPS

Оставьте host равным 127.0.0.1 и выберите один из двух путей. Первый — SSH-туннель: ничего не открывается наружу, а http://localhost:8080 вы открываете на своём компьютере, пока работает туннель.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Второй — HTTPS через обратный прокси, например Caddy, который сам получает сертификат (см. deploy/Caddyfile.example). Затем укажите в public_url свой https-адрес, добавьте https://ваш-адрес/callback как перенаправление в Developer Portal и установите trust_proxy в true:

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

Редактор показывает каждую настройку, которая является переключателем, числом, текстом, каналом, ролью или простым списком. То, что создаётся командами, например товары магазина, меню ролей, ленты, теги и тикеты, остаётся за командами. Страница доступна на английском и немецком и следует языку браузера. В Docker публикуйте порт только на 127.0.0.1 (127.0.0.1:8080:8080), а в контейнере установите host в 0.0.0.0 и allow_insecure_http в true.

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
/case view case_id:12

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
/suggestion setup set channel:#suggestions review_role:@Staff
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

### Роли по реакции и уведомления

Выдавайте роли за реакции с любыми эмодзи и позволяйте участникам выбирать темы уведомлений.

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

### Дни рождения

Участники указывают день и месяц, бот выдаёт роль и пишет сообщение в этот день.

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

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

### Инструменты модератора

Очистка каналов, управление ролями и личные заметки. Каждое действие записывается в журнал.

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

### Информация

Справка о пользователях, сервере, ролях и боте.

```
/userinfo user:@User
/serverinfo
/roleinfo role:@Moderator
/avatar user:@User
/help command:ban                                  # explains one command
/ping
/botinfo
```

### Объявления, теги и напоминания

Сообщения от имени бота, собственные команды, автоответы на сообщения и напоминания.

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

### Мод-почта и апелляции на бан

Участники пишут команде через приватный канал на сервере. Никому не нужно писать боту в личные сообщения.

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

### Канал счёта, закреплённые сообщения и статистика

Игра в счёт, сообщения, которые остаются внизу канала, и каналы с живыми числами.

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

### Дополнительные возможности существующих функций

Дополнения для тикетов, розыгрышей, голосовых комнат, XP, дней рождения, резервных копий, журналов и экранов состояния.

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

### Другие инструменты AutoMod

Проверка коротких ссылок, ограничение ссылок для новичков, поиск ghost ping и проверка правил без наказаний.

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

### Лимиты модераторов и аудит прав

Сигнал, если модератор слишком часто банит или кикает, и обзор ролей с опасными правами.

```
/modwatch status
/modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/modwatch exclude member:@TrustedMod

/permaudit run                                                  # roles with dangerous permissions and who holds them
/permaudit watch enabled:True                                   # alarm when a role or member gets one
/permaudit trust role:@Admin
```

### Жалобы и отслеживание приглашений

Участники жалуются на сообщения команде, а бот запоминает, какое приглашение привело нового участника.

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

### Диагностика и отладка

Поиск недостающих прав и неверных настроек, отчёты об ошибках в канале, экспорт и импорт настроек.

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

### Музыка

Воспроизводит ссылки и файлы из папки music в голосовом канале. Загрузки сохраняются как music/Исполнитель/Альбом/Трек. Нужны ffmpeg и пакеты из requirements.txt.

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

Без потерь: ваши собственные файлы (FLAC, WAV, ALAC) и источники с FLAC воспроизводятся без изменений. YouTube, SoundCloud и похожие сайты отдают только звук с потерями, который нельзя потом сделать lossless. Discord передаёт голос в формате Opus, бот использует битрейт голосового канала. Ответственность: загрузка и воспроизведение контента может нарушать правила сайта или авторское право. Загрузки по умолчанию выключены, модуль выключен, пока вы его не включите. За воспроизводимое и сохраняемое отвечает оператор бота.

### Настройка и проверка состояния

Пошаговый помощник настраивает самое важное кнопками и меню: канал логов, канал приветствий, роли команды, гулаг, пресет AutoMod (мягкий, обычный, строгий), шаблон сервера (сообщество, игры, поддержка) и язык. /health показывает, что уже настроено и что ещё осталось. Язык меняет тексты, которые видят участники: приветствия по умолчанию, уведомления AutoMod, верификацию, тикеты, апелляции, мод-почту и меню ролей. Фиксированные ответы администраторам переведены, ответы с именами и числами остаются на английском.

```
/setup                                                         # buttons and menus, nothing is switched off by a template
/health                                                        # what is set up, what is open, and the self-test
/language code:de
```

### Экономика

Валюта сервера с ежедневной наградой, работой, переводами, рейтингом и магазином, товары которого могут выдавать роль. Включается модулем economy. Команды работают и с префиксом, например !economy daily.

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

### Меню ролей, отложенные сообщения и ленты

Меню ролей выдают роли кнопками или выпадающим списком. Отложенные сообщения публикуются один раз или повторяются каждый час, день или неделю. Ленты публикуют новые видео YouTube, трансляции Twitch и записи RSS. Для YouTube нужен ID канала (начинается с UC). Для Twitch в файле .env нужны TWITCH_CLIENT_ID и TWITCH_CLIENT_SECRET. Время записывается как in 2h, 18:30 или как дата со временем, например 2026-12-24 18:00, в часовом поясе сервера. Первая проверка ленты лишь запоминает то, что уже есть.

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

### Активность, массовые действия и поиск дел

Активность считает сообщения по каналам и входы и выходы по дням, но никогда не содержимое и не имена. Массовые действия банят, кикают или отправляют в тайм-аут до 25 пользователей после подтверждения. Дела можно искать по пользователю, типу, имени, причине, модератору и давности и связывать друг с другом, например заметку с баном.

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

### Защита от мошенничества и крипто-скама

Удаляет поддельные розыгрыши, такие как типичный скам с MrBeast, в тексте и на изображениях за миллисекунды. Имена из мгновенного списка удаляются сразу при любом написании (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Иначе слова из списков (имена, приманки, крипто, ссылки, суммы) суммируются, и сообщение удаляется по достижении порога. Изображения читаются через OCR, а изображение, однажды признанное скамом, удаляется без повторного чтения. Для чтения изображений нужен tesseract, без него проверяется только текст. Сервер о MrBeast может убрать имя из мгновенного списка или исключить каналы командой /automod exemptchannel. Проверьте работу командой /antiscam test, прежде чем полагаться на неё.

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

### Испытательный срок, обнаружение роя, хронология и обучение

Испытательный срок помещает новых участников в роль. Пока они не напишут заданное число обычных сообщений или не пройдёт заданное время, ссылки, приглашения и файлы удаляются с коротким уведомлением. Защита от рейдов также распознаёт рой: несколько новых аккаунтов с одинаковым шаблоном имени, одинаковой аватаркой или созданных с разницей в несколько минут. Хронология (/case timeline) собирает в порядке времени создание аккаунта, вход и приглашение, испытательный срок, дела и апелляции одного пользователя. Сообщения никогда не хранятся, поэтому в неё не входят. /block, /unblock и /blocklist управляют блок-листом AutoMod короткими командами. Модераторы обучают модуль защиты от мошенничества через пункт контекстного меню Mark as scam у сообщения или реакцией с эмодзи из learn_emoji: сообщение удаляется, а его изображения и текст с этого момента удаляются сразу. Каждая часть отключается своим модулем или настройками.

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

### Конструктор сообщений и обновления

Конструктор сообщений публикует сообщения с несколькими эмбедами и кнопками-ссылками из JSON. Он читает JSON, который экспортируют генераторы эмбедов, такие как Embed Generator, так что вы создаёте сообщение там и публикуете его ботом. Передайте JSON текстом, файлом .json или https-ссылкой, ведущей прямо на JSON, например на «сырой» файл репозитория (ссылки с перенаправлением отклоняются). Создаются только кнопки-ссылки, кнопки, требующие взаимодействия, пропускаются. Каждая ссылка должна быть http или https, упоминания в тексте никогда не уведомляют, действуют ограничения Discord. /message copy экспортирует существующее сообщение в JSON, /message edit изменяет сообщение бота, а /message preview показывает результат только вам. Ссылки для обмена из веб-редакторов не открываются, потому что их формат не публичен.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Каждые 12 часов бот проверяет репозиторий GitHub из update.repo (задаётся скриптом scripts/set_repo_url.py) на наличие более новой версии. Если она есть, владелец бота получает личное сообщение с описанием релиза, а релиз скачивается и проверяется: контрольная сумма SHA-256, безопасные пути внутри архива и версия, совпадающая с тегом. Устанавливается командой /debug update action:install или сама, если включён auto_install. Перед установкой заменяемые файлы сохраняются в data/update, устанавливаются новые пакеты, а новый код пробно импортируется. При любой ошибке старые файлы восстанавливаются. Ваши .env, settings.json, data и music никогда не затрагиваются. Затем бот перезапускается сам. В Docker на месте ничего не устанавливается, обновите образ. Обновление выполняет код из репозитория, поэтому указывайте только репозиторий, которому доверяете. Отключается параметром enabled со значением false.

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

### Эксплуатация

Бот сохраняет данные каждые несколько секунд и хранит резервные копии базы в data/dbbackups: одну перед каждым изменением формата данных и одну в день. Очередь музыки, закреплённые сообщения и счётчики модераторов переживают перезапуск. Крупные боты могут работать на нескольких шардах. Файл heartbeat и необязательная страница состояния помогают системам мониторинга. Эти параметры задаются в settings.json:

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
/birthday setup set   message                         {user} {name}
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

## Переводы

Английский — исходный язык проекта. Все переводы документации, панели и сообщений бота выполнены машинным переводом и не проверялись носителями языка. Возможны неловкие формулировки и ошибки, пожалуйста, сообщайте о них или присылайте исправления. Файлы находятся в docs/ и guardbot/locales/.

## Планы

- Графики активности и модерации в панели.
- Проверка всех переводов носителями языка.
- Перевод большего числа фиксированных текстов ответов.

## Конфиденциальность и безопасность

- Нет телеметрии. Бот общается с Discord и, для проверки обновлений, с GitHub (личные данные не отправляются, отключается параметром update.enabled). Ссылки, которые дают администраторы, например ленты, музыка и ссылки на JSON, открываются только по запросу.
- Все данные хранятся в папке data на вашем компьютере: настройки, XP, дни рождения (только день и месяц) и случаи модерации.
- Бот игнорирует личные сообщения от участников.
- Токен читается из файла .env. Никому его не передавайте и не публикуйте.
- Участники могут экспортировать и удалять свои данные командой /mydata. Администраторы задают, как долго хранятся данные ушедших участников.
- [PRIVACY.md](../PRIVACY.md)

## Поддержка

Ошибки, идеи и предложения: пишите мне в Discord, @justyyin, или создайте issue на GitHub.

## Благодарности

GuardBot вдохновлён проектом [Embed Generator](https://github.com/merlinfuchs/embed-generator) Мерлина Фукса (лицензия MIT, размещён на message.style). Конструктор сообщений читает тот же формат JSON, поэтому сообщения, созданные там, можно публиковать этим ботом. Код того проекта не включён. Спасибо авторам discord.py, aiohttp, Pillow, yt-dlp, mutagen и Tesseract.

## Лицензия

Опубликовано под лицензией MIT. См. [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
