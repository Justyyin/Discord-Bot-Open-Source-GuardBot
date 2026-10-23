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
  - [Структура, участники и команда](#структура-участники-и-команда)
- [Панель управления](#панель-управления)
  - [Настройка панели](#настройка-панели)
  - [Команды, скиллы, ИИ и профиль бота](#команды-скиллы-ии-и-профиль-бота)
  - [Безопасность](#безопасность-1)
  - [Панель на VPS](#панель-на-vps)
- [Команды](#команды)
  - [Группы команд](#группы-команд)
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
  - [Панели](#панели)
  - [Скиллы и ИИ](#скиллы-и-ии)
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
- Канал «гулаг»: участники, публикующие мошеннические ссылки или изображения, перемещаются в один канал с инструкцией по защите аккаунта. Модераторы также могут использовать /moderation jail и /moderation unjail.
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
- Экономика с магазином, меню ролей с кнопками или списком, отложенные сообщения, ленты YouTube, Twitch и RSS, статистика активности и пошаговый /admin setup. Сообщения для участников доступны на 12 языках.

### Администрирование

- Каждый модуль и каждую команду можно включать и выключать для каждого сервера.
- Собственный префикс, псевдонимы команд и переименование команд.
- Резервное копирование и восстановление ролей и структуры каналов.
- Автоматические резервные копии по расписанию для ролей, каналов, эмодзи и вебхуков, с командой восстановления, которая добавляет только недостающее.
- Панель управления: изменение настроек каждого сервера в браузере после входа через Discord, только для участников, управляющих сервером, и только пока бот подключён.
- Скиллы: свои команды, игры и автоматизации из безопасных блоков, по желанию написанные ИИ с твоим собственным ключом (Anthropic, OpenAI, Kimi). Панель показывает все команды и редактирует скиллы, настройки ИИ и профиль бота.

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

### Структура, участники и команда

Версия 1.5 добавляет команды для создания и поддержания порядка на сервере, восстановления вернувшихся участников и управления командой модерации. У каждой части есть переключатель модуля (`/admin module`), собственные настройки и место в панели.

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

- С помощью `/structure` каналы и категории создаются, клонируются, переименовываются, сортируются, а права копируются с другого канала. О неактивных каналах сообщается, либо они переносятся в категорию архива (`/structure archive`). Роли можно выдавать на ограниченный срок и сохранять как шаблоны; шаблон никогда не даёт право, которого нет у применяющего его.
- `/structure rules` публикует правила с кнопкой принятия и номером версии. После `post new_version:True` участники, не принявшие новую версию, получают одно напоминание в личные сообщения.
- `/members stickyroles` возвращает роли и восстанавливает таймаут или мьют при возвращении участника. `/members nickname` убирает символы, поднимающие имя в начало списка, проверяет запрещённые слова в никнеймах и именах пользователей и переименовывает нарушителей. Список наблюдения работает тихо: команда получает оповещение при первом сообщении пользователя из списка.
- Согласование в четыре глаза (`/security approval`) выполняет баны, кики, таймауты и массовые действия только после согласия второго модератора. `/moderation case undo` отменяет случай вместе с вызванными им действиями (например, мьют и последовавший бан). Предупреждения могут истекать через заданное число дней (`/moderation escalation expiry`).
- `/admin history` показывает, кто и когда изменил настройку, и откатывает раздел. Имя человека определяется предположительно по последним командам и изменениям в панели на сервере. `/admin history copy` копирует разделы на другой сервер, которым вы можете управлять через бота; сначала выполняется пробный прогон. `/admin exceptions` исключает каналы и роли из правил AutoMod и Anti-Scam. `/admin dashaccess` даёт ролям доступ к панели только для чтения или как модератору.
- `/team` показывает работу каждого модератора (случаи, тикеты, жалобы, время реакции, неактивные участники), публикует еженедельный отчёт (день и час по UTC), позволяет модераторам отметить отсутствие через `/team duty away`, чтобы тикеты и упоминания шли другим, и ведёт заявки в команду с формой и голосованием.
- Discord не умеет скрывать команды внутри группы от отдельных участников. Бот всё равно проверяет каждый вызов. Цифры статистики команды считаются со дня обновления; более ранние действия не учитываются.

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

### Команды, скиллы, ИИ и профиль бота

В панели ещё пять страниц: Panels (см. раздел «Панели») и следующие четыре. «Команды» перечисляет каждую слэш-команду, команду с префиксом и контекстное меню с модулем, нужным правом и состоянием; администраторы включают и выключают их, разрешают или запрещают роли и дают командам с префиксом короткие имена. Префикс меняется на той же странице. «Скиллы» показывает все скиллы и редактирует их как JSON с теми же проверками, что и команды. «ИИ» задаёт модель и ограничения и сохраняет ключ (только запись, на страницу он никогда не возвращается). «Профиль бота» меняет имя, картинку, баннер и описание бота на этом сервере; владелец приложения бота или ID из `owner_ids` в settings.json может менять их и везде. Discord ограничивает, как часто можно менять имя и картинку. Каждое изменение записывается в журнал аудита.

Каждый модуль показан как плагин: страница Plugins выводит их карточками по категориям, а у каждого плагина есть своя страница с переключателем «Активно», настройками в раскрывающихся блоках и командами с переключателем и редактором ролей. Левая панель перечисляет плагины по категориям, точка показывает, включены ли они. Панель управления выполнена в тёмном оформлении.

Панель управления доступна на всех 12 языках бота. Язык выбирается справа вверху или на странице входа; выбор сохраняется в браузере и не меняет язык сервера. Тексты панели переведены машинным способом.

Каждая страница плагина объясняет, что делает плагин, перечисляет все его функции с отдельным переключателем и кратким пояснением, а остальные настройки держит в блоках ниже. На странице «Плагины» и в обзоре каждый плагин можно включить или выключить напрямую. В «Настройках» блок «Оформление панели» меняет акцентный цвет, фон, блоки и текст, ставит обои (затемнённые и размытые по желанию) и добавляет в боковую панель свои меню и вкладки: вкладка может собирать выбранные плагины, открывать страницу, вести на https-адрес или показывать заметку. Оформление хранится для каждого сервера и видно всем, кто открывает его панель. В подвале показаны копирайт и ссылки на Discord и GitHub; чтобы там отображались официальные логотипы, положите discord.svg и github.svg со страниц брендов Discord и GitHub в guardbot/web/brand/.

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

<!-- groups -->
### Группы команд

Чтобы экономить слоты слеш-команд (Discord допускает 100 команд верхнего уровня на бота), связанные команды объединены в группы. Сначала вводится группа, затем команда, например `/moderation ban`. Текстовые команды с префиксом, например `!ban`, не меняются. Права, псевдонимы и переключатели модулей по-прежнему используют простое имя команды.

| Группа | Содержит |
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

### Модерация

Предупреждения, мьюты, кики и баны работают как слэш-команды и с префиксом, например `!warn @User spam`. Каждое действие создаёт нумерованный случай.

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

### Гулаг (jail)

Участники со взломанным аккаунтом перемещаются в один канал с инструкцией по безопасности. При освобождении им возвращаются прежние роли.

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

Каждый, кто попадает в ГУЛАГ — командой, через AutoMod, через антискам, при повторном входе или потому что кто-то выдал роль вручную, — получает уведомление Account Security Required с упоминанием. Пока в ГУЛАГе кто-то есть, внизу канала висит Account Recovery Reminder, которое обновляется каждые 10 минут. Участник в ГУЛАГе, написавший в канале ГУЛАГа префикс и слово для освобождения (например `!unban`), создаёт запрос на освобождение с кнопками Release и Keep для команды; сам бот никого не освобождает. `/access jailsetup reminder` включает и выключает каждую часть и задаёт интервал и слово.

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

### Защита от нюка

Следит за журналом аудита и реагирует, когда кто-то разрушает сервер. Владелец получает личное сообщение.

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

### Верификация

Новые участники видят только канал верификации, пока не нажмут кнопку или не решат капчу.

```
/access verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/access verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/access verify panel channel:#verify                      # post the button again
/access verify apply                                      # apply the channel permissions again
/access verify member member:@User                        # verify someone manually
/access verify off
```

### Журналирование

Выберите канал для каждой категории или один основной канал для всего.

```
/server log set category:main channel:#logs               # fallback for every category
/server log set category:messages channel:#log-messages
/server log set category:moderation channel:#log-moderation
/server log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/server log sent enabled:False                            # stop logging every sent message
/server log show
```

### Приветствия, прощания и бустеры

Сообщения, автороли и награды для бустеров сервера.

```
/community welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/community welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/community welcome autorole role:@Member                     # toggle, given to every new member
/community welcome botrole role:@Bots                        # toggle, given to every new bot
/community welcome test

/community booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/community booster role role:@Booster                        # toggle
```

### Тикеты

Участники открывают личные каналы кнопкой. При закрытии отправляется стенограмма.

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

### Опросы и розыгрыши

Кнопки для голосования и участия. Длительность принимает значения вроде 30m, 2h и 1d.

```
/engage poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/engage poll end poll_id:3
/engage poll list

/engage giveaway start prize:Nitro duration:2d winners:2 role:@Member
/engage giveaway end giveaway_id:1
/engage giveaway reroll giveaway_id:1
/engage giveaway list
```

### Предложения и starboard

Участники публикуют предложения, которые команда может принять или отклонить, а популярные сообщения выделяются.

```
/suggestion setup set channel:#suggestions review_role:@Staff
/support suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/engage starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/engage starboard ignore channel:#spam
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

/info rank                                              # also: !rank, shows a rank card image
/info rank user:@User
/info leaderboard
```

### Роли по реакции и уведомления

Выдавайте роли за реакции с любыми эмодзи и позволяйте участникам выбирать темы уведомлений.

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
/community tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Резервные копии и восстановление

Копии содержат роли, каналы, эмодзи, вебхуки и роли участников. Восстановление добавляет только недостающее.

```
/server backup create name:before-update
/server backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/server backup list
/server backup download name:before-update
/server backup restore name:before-update member_roles:True   # only adds what is missing
/server backup delete name:before-update
```

### Данные и конфиденциальность

Участники могут экспортировать и удалять свои данные. Администраторы задают срок хранения.

```
/info mydata export                                     # members download their own data
/info mydata delete confirm:True                        # members delete their XP and birthday

/server privacy retention days:90                         # delete data of members who left after 90 days
/server privacy export user_id:123456789012345678
/server privacy delete user_id:123456789012345678 cases:True
```

### Инструменты модератора

Очистка каналов, управление ролями и личные заметки. Каждое действие записывается в журнал.

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

### Информация

Справка о пользователях, сервере, ролях и боте.

```
/info userinfo user:@User
/server serverinfo
/server roleinfo role:@Moderator
/info avatar user:@User
/help command:ban                                  # explains one command
/info ping
/info botinfo
```

### Объявления, теги и напоминания

Сообщения от имени бота, собственные команды, автоответы на сообщения и напоминания.

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

### Дополнительные возможности существующих функций

Дополнения для тикетов, розыгрышей, голосовых комнат, XP, дней рождения, резервных копий, журналов и экранов состояния.

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
/team modwatch status
/team modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/team modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/team modwatch exclude member:@TrustedMod

/team permaudit run                                                  # roles with dangerous permissions and who holds them
/team permaudit watch enabled:True                                   # alarm when a role or member gets one
/team permaudit trust role:@Admin
```

### Жалобы и отслеживание приглашений

Участники жалуются на сообщения команде, а бот запоминает, какое приглашение привело нового участника.

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

### Диагностика и отладка

Поиск недостающих прав и неверных настроек, отчёты об ошибках в канале, экспорт и импорт настроек.

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

Без потерь: ваши собственные файлы (FLAC, WAV, ALAC) и источники с FLAC воспроизводятся без изменений. YouTube, SoundCloud и похожие сайты отдают только звук с потерями, который нельзя потом сделать lossless. Discord передаёт голос в формате Opus, бот использует битрейт голосового канала. Ответственность: загрузка и воспроизведение контента может нарушать правила сайта или авторское право. Загрузки по умолчанию выключены, модуль выключен, пока вы его не включите. За воспроизводимое и сохраняемое отвечает оператор бота.

Источники: ссылки и поиск YouTube и SoundCloud воспроизводятся напрямую. Ссылки Spotify, Apple Music и Tidal тоже принимаются, но эти сервисы не отдают своё аудио: бот читает название и исполнителя с публичной страницы и играет ту же песню из источника поиска (YouTube или SoundCloud, настраивается через /music sources). Альбомы и плейлисты Spotify и Apple Music читаются с их публичных страниц; для альбомов и плейлистов Tidal нужен бесплатный ключ разработчика с developer.tidal.com в .env (TIDAL_CLIENT_ID и TIDAL_CLIENT_SECRET). Файлы из вашей папки с музыкой воспроизводятся как есть. Сохранённые плейлисты могут смешивать все источники, а /music stay держит бота в голосовом канале круглосуточно и играет плейлист по кругу, в том числе после перезапуска.

Guard Music, второй бот: музыка может работать на отдельном аккаунте бота, чтобы постоянно оставаться в голосовом канале, не затрагивая модерацию.

1. Создайте второе приложение в Discord Developer Portal, назовите его Guard Music и скопируйте токен его бота.
2. Запишите токен в .env как MUSIC_TOKEN и установите music_bot.enabled в true в settings.json.
3. Перезапустите GuardBot. Guard Music запускается в том же процессе, использует те же настройки и данные, и музыкальные команды переходят к нему.
4. Откройте в панели страницу «Музыка» и добавьте Guard Music на сервер кнопкой там. Без MUSIC_TOKEN музыка остаётся в GuardBot.

Используйте на свой страх и риск: трансляция с YouTube и других сервисов может нарушать их условия использования, а на воспроизводимое распространяется авторское право. Из Spotify, Apple Music и Tidal ничего не скачивается, и никакая защита не обходится. За воспроизводимое отвечает владелец бота. Страница «Музыка» в панели показывает плеер, очередь, плейлисты, режим 24/7, источники и эту инструкцию.

### Настройка и проверка состояния

Пошаговый помощник настраивает самое важное кнопками и меню: канал логов, канал приветствий, роли команды, гулаг, пресет AutoMod (мягкий, обычный, строгий), шаблон сервера (сообщество, игры, поддержка) и язык. /server health показывает, что уже настроено и что ещё осталось. Язык меняет тексты, которые видят участники: приветствия по умолчанию, уведомления AutoMod, верификацию, тикеты, апелляции, мод-почту и меню ролей. Фиксированные ответы администраторам переведены, ответы с именами и числами остаются на английском.

```
/admin setup                                                         # buttons and menus, nothing is switched off by a template
/server health                                                        # what is set up, what is open, and the self-test
/admin language code:de
```

### Экономика

Валюта сервера с ежедневной наградой, работой, переводами, рейтингом и магазином, товары которого могут выдавать роль. Включается модулем economy. Команды работают и с префиксом, например !economy daily.

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

### Меню ролей, отложенные сообщения и ленты

Меню ролей выдают роли кнопками или выпадающим списком. Отложенные сообщения публикуются один раз или повторяются каждый час, день или неделю. Ленты публикуют новые видео YouTube, трансляции Twitch и записи RSS. Для YouTube нужен ID канала (начинается с UC). Для Twitch в файле .env нужны TWITCH_CLIENT_ID и TWITCH_CLIENT_SECRET. Время записывается как in 2h, 18:30 или как дата со временем, например 2026-12-24 18:00, в часовом поясе сервера. Первая проверка ленты лишь запоминает то, что уже есть.

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

### Активность, массовые действия и поиск дел

Активность считает сообщения по каналам и входы и выходы по дням, но никогда не содержимое и не имена. Массовые действия банят, кикают или отправляют в тайм-аут до 25 пользователей после подтверждения. Дела можно искать по пользователю, типу, имени, причине, модератору и давности и связывать друг с другом, например заметку с баном.

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

### Защита от мошенничества и крипто-скама

Удаляет поддельные розыгрыши, такие как типичный скам с MrBeast, в тексте и на изображениях за миллисекунды. Имена из мгновенного списка удаляются сразу при любом написании (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Иначе слова из списков (имена, приманки, крипто, ссылки, суммы) суммируются, и сообщение удаляется по достижении порога. Изображения читаются через OCR, а изображение, однажды признанное скамом, удаляется без повторного чтения. Для чтения изображений нужен tesseract, без него проверяется только текст. Сервер о MrBeast может убрать имя из мгновенного списка или исключить каналы командой /automod exemptchannel. Проверьте работу командой /security antiscam test, прежде чем полагаться на неё.

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

### Испытательный срок, обнаружение роя, хронология и обучение

Испытательный срок помещает новых участников в роль. Пока они не напишут заданное число обычных сообщений или не пройдёт заданное время, ссылки, приглашения и файлы удаляются с коротким уведомлением. Защита от рейдов также распознаёт рой: несколько новых аккаунтов с одинаковым шаблоном имени, одинаковой аватаркой или созданных с разницей в несколько минут. Хронология (/moderation case timeline) собирает в порядке времени создание аккаунта, вход и приглашение, испытательный срок, дела и апелляции одного пользователя. Сообщения никогда не хранятся, поэтому в неё не входят. /security block, /security unblock и /security blocklist управляют блок-листом AutoMod короткими командами. Модераторы обучают модуль защиты от мошенничества через пункт контекстного меню Mark as scam у сообщения или реакцией с эмодзи из learn_emoji: сообщение удаляется, а его изображения и текст с этого момента удаляются сразу. Каждая часть отключается своим модулем или настройками.

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

### Панели

Панели — это публикации вроде приветствия, правил, выбора роли, кнопок уведомлений или верификации, с баннерами, текстовыми блоками и кнопками. Их создают командой `/panel` или в панели управления на странице Panels. Картинки загружаются там или как параметры команды, бот хранит их в `data/panels`, поэтому они не пропадают.

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

Шаблоны: empty, welcome, rules, roles, notifications и verify; их тексты на языке сервера и их можно менять. `/panel section` открывает форму для заголовка, текста и подписи. Каждый раздел становится отдельным сообщением: баннер над блоком, большая картинка внутри, маленькая — справа вверху. Кнопки находятся под последним разделом, по пять в ряд. Кнопка роли выдаёт роль или забирает её; при `single` остальные роли панели снимаются. Кнопка verify запускает проверку модуля верификации (`/access verify setup` выбирает кнопку, капчу или пример). В текстах можно использовать `{server}` и `{count}`. `/panel update` меняет опубликованные сообщения после правки. Ограничения на сервер: 25 панелей, 5 разделов и 20 кнопок на панель, 40 картинок до 8 МБ. Бот предлагает только роли ниже своей высшей роли и без опасных прав.

### Скиллы и ИИ

Скиллы — это команды, игры и автоматизации, которые сервер собирает сам из безопасных блоков. Им не нужен ИИ, и они никогда не выполняют код. ИИ необязателен: с твоим собственным ключом он пишет скилл по описанию и даёт второе мнение в проверке антискама.

Скиллы без ИИ:

- `/support skill create kind:command name:hello` открывает окно с небольшим примером, который ты меняешь. `/support skill edit`, `show`, `import`, `enable`, `disable`, `delete`, `list` и `stats` управляют ими. Все используют скилл через `/support skill run` или с префиксом, например `!hello`. `/support skill panel` публикует кнопки, запускающие скиллы.
- Виды: команда (список действий), игра (кубик, выбор, слоты, камень-ножницы-бумага, викторина) и автоматизация (запускается, когда участник заходит или уходит, когда сообщение содержит слова или когда нажата кнопка).
- Действия: ответить, отправить в канал, личное сообщение, запись в журнал, выдать или забрать роль, изменить счётчик, выдать монеты, выбрать случайно. У действия могут быть условия: есть роль, вероятность, счётчик в сравнении с числом.
- В текстах можно использовать `{user}`, `{user_name}`, `{server}`, `{channel}`, `{count}`, `{arg1}`, `{arg2}`, `{var:name}`, `{uvar:name}` и `{random:1-6}`.
- Ограничения: 50 скиллов на сервер, 10 действий на скилл, 3 изменения ролей и 4 сообщения на скилл. Бот выдаёт только роли ниже своей высшей роли и без опасных прав. Скиллу, который выдаёт монеты, нужна пауза не менее 60 секунд. Нельзя использовать имена команд бота, алиасов и тегов.
- Скиллы хранятся как JSON и входят в экспорт настроек. Неизвестные поля отклоняются, поэтому скилл из любого источника может делать только то, что позволяют блоки.

Пример: команда, которая выдаёт роль и считает использования (замени ID роли):

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

Подключение ИИ (необязательно):

- `/support ai setup provider:kimi agree:true` открывает приватное окно для твоего ключа API. Провайдеры: Anthropic, OpenAI и Kimi (Moonshot). Модель предлагается автоматически и меняется в той же команде или в панели; названия моделей у провайдеров меняются, поэтому проверяй их документацию. Ты платишь своему провайдеру.
- `/support ai make wish:...` просит ИИ написать скилл, проверяет ответ так же строго, как импортированный скилл, и показывает предпросмотр. Ничего не сохраняется, пока ты не нажмёшь «Сохранить».
- `/support ai status`, `limits` (запросов в день, секунд между запросами одного человека) и `remove` дополняют набор. Ключ хранится в зашифрованном виде, секрет лежит в файле `data/ai.secret`. Храни этот файл вместе с резервными копиями; без него сохранённый ключ не прочитать, и его придётся ввести заново. Ключ никогда не показывается, не пишется в журнал и не экспортируется. Провайдер меняется только вместе с новым ключом, поэтому ключ никогда не уходит другому провайдеру.
- Что отправляется: пожелание из `/support ai make` и, при втором мнении, текст подозрительного сообщения. Больше ничего, и только пока включён модуль `ai`. См. [PRIVACY.md](../PRIVACY.md).

Обучение антискама:

- Обучаемый фильтр (`/security antiscam set learned:true`) — небольшой классификатор для каждого сервера. Модераторы обучают его пунктами контекстного меню «Mark as scam» и «Not a scam». Он хранит только короткие хеши слов, никогда не сам текст, начинает действовать лишь после 8 примеров скама и 30 обычных, и тогда только при уверенности выше 95 процентов. С `ham_sampling` он также учится на каждом десятом обычном сообщении.
- Похожие изображения (`similar`, по умолчанию включено) сравнивают отпечаток картинки с известными скам-картинками, поэтому находится и пересохранённая, и уменьшенная копия. Это работает без Tesseract.
- Второе мнение ИИ (`/support ai limits second_opinion:true`): в случаях чуть ниже порога или тех, что обучаемый фильтр считает подозрительными, спрашивают ИИ. Сообщение удаляется, только если ИИ отвечает «скам» с уверенностью не ниже 80 процентов, и его ответ не может вызвать ничего другого.

### Конструктор сообщений и обновления

Конструктор сообщений публикует сообщения с несколькими эмбедами и кнопками-ссылками из JSON. Он читает JSON, который экспортируют генераторы эмбедов, такие как Embed Generator, так что вы создаёте сообщение там и публикуете его ботом. Передайте JSON текстом, файлом .json или https-ссылкой, ведущей прямо на JSON, например на «сырой» файл репозитория (ссылки с перенаправлением отклоняются). Создаются только кнопки-ссылки, кнопки, требующие взаимодействия, пропускаются. Каждая ссылка должна быть http или https, упоминания в тексте никогда не уведомляют, действуют ограничения Discord. /post message copy экспортирует существующее сообщение в JSON, /post message edit изменяет сообщение бота, а /post message preview показывает результат только вам. Ссылки для обмена из веб-редакторов не открываются, потому что их формат не публичен.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Каждые 12 часов бот проверяет репозиторий GitHub из update.repo (задаётся скриптом scripts/set_repo_url.py) на наличие более новой версии. Если она есть, владелец бота получает личное сообщение с описанием релиза, а релиз скачивается и проверяется: контрольная сумма SHA-256, безопасные пути внутри архива и версия, совпадающая с тегом. Устанавливается командой /server debug update action:install или сама, если включён auto_install. Перед установкой заменяемые файлы сохраняются в data/update, устанавливаются новые пакеты, а новый код пробно импортируется. При любой ошибке старые файлы восстанавливаются. Ваши .env, settings.json, data и music никогда не затрагиваются. Затем бот перезапускается сам. В Docker на месте ничего не устанавливается, обновите образ. Обновление выполняет код из репозитория, поэтому указывайте только репозиторий, которому доверяете. Отключается параметром enabled со значением false.

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

### Эксплуатация

Бот сохраняет данные каждые несколько секунд и хранит резервные копии базы в data/dbbackups: одну перед каждым изменением формата данных и одну в день. Очередь музыки, закреплённые сообщения и счётчики модераторов переживают перезапуск. Крупные боты могут работать на нескольких шардах. Файл heartbeat и необязательная страница состояния помогают системам мониторинга. Эти параметры задаются в settings.json:

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

Журналы пишутся в data/guardbot.log (с ротацией, см. log_max_mb и log_backups). При log_format = json каждая строка — это JSON-объект с сервером и командой. Если задан health_port, /metrics отдаёт метрики Prometheus (время работы, задержка, память, размер базы данных, ошибки, использование и длительность команд, линии обработки). Экспортируются только числа, никогда имена или ID, а metrics_token требует bearer-токен. Тяжёлая работа (чтение изображений, рисование карточек, музыкальные файлы, резервные копии) выполняется в линиях с фиксированным числом потоков и лимитом (workers в settings.json). Когда линия заполнена, бот сообщает, что занят, вместо накопления работы. Каждая резервная копия базы данных открывается и проверяется сразу после создания. Чтобы восстановить копию, остановите бота и выполните:

```
python scripts/restore_db.py data/dbbackups/guardbot-YYYYMMDD-HHMMSS-auto.db
python scripts/restore_db.py BACKUPFILE --check          # only check a backup
```

Текущая база данных сохраняется как копия с именем before-restore.

### Администрирование

Включение и выключение модулей и команд, смена префикса, псевдонимы и ограничение команд по ролям.

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

## Подстановки в сообщениях

Эти подстановки заменяются в настраиваемых вами текстах:

```
/community welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/community booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/community tempvoice setup     name                            {name}
/access jailsetup notice    text                            {staff}
```

## Настройка

Глобальные параметры задаются в settings.json. Всё остальное настраивается для каждого сервера командами /admin module, /admin command, /admin perms, /admin alias и /admin config.

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

Любую настройку можно прочитать и изменить командой /admin config. Вот пути, которые понадобятся чаще всего:

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
    defaults/             default settings, one file per area (core, security, moderation, community) and base.py for modules and permissions
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature, in the folders security, moderation, server, community, tools
    skills.py             движок скиллов: проверяет и выполняет скиллы
    ai.py                 провайдеры ИИ, зашифрованные ключи, ограничения
    learner.py, imgsim.py обучаемый фильтр антискама, отпечатки картинок
    dashboard_manage.py   страницы панели для команд, скиллов, ИИ и профиля
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
- Участники могут экспортировать и удалять свои данные командой /info mydata. Администраторы задают, как долго хранятся данные ушедших участников.
- Функции ИИ выключены, пока ты не добавишь свой ключ. После этого выбранному провайдеру отправляются только текст `/support ai make` и, при втором мнении, подозрительные сообщения.
- [PRIVACY.md](../PRIVACY.md)

## Поддержка

Ошибки, идеи и предложения: пишите мне в Discord, @justyyin, или создайте issue на GitHub.

## Благодарности

GuardBot вдохновлён проектом [Embed Generator](https://github.com/merlinfuchs/embed-generator) Мерлина Фукса (лицензия MIT, размещён на message.style). Конструктор сообщений читает тот же формат JSON, поэтому сообщения, созданные там, можно публиковать этим ботом. Код того проекта не включён. Спасибо авторам discord.py, aiohttp, Pillow, yt-dlp, mutagen и Tesseract.

## Лицензия

Опубликовано под лицензией MIT. См. [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
