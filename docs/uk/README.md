# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | **Українська** | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Бот для Discord, який ви розміщуєте самостійно, для модерації, безпеки та спільноти. Відкритий код, безкоштовно, а ваші дані залишаються на вашому комп'ютері.

> Бета: GuardBot і його панель керування перебувають у стадії бети. Їх не було ретельно протестовано, особливо на великих серверах і в усіх ситуаціях Discord. Можливі помилки, робіть резервні копії папки data та повідомляйте про проблеми. Використання на власний ризик.

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
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Скрипти запуску та автозапуск](#скрипти-запуску-та-автозапуск)
  - [Оновлення](#оновлення)
- [Права бота](#права-бота)
- [Перші кроки в Discord](#перші-кроки-в-discord)
- [Панель керування](#панель-керування)
  - [Налаштування панелі](#налаштування-панелі)
  - [Безпека](#безпека-1)
  - [Панель на VPS](#панель-на-vps)
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
  - [Інструменти модератора](#інструменти-модератора)
  - [Інформація](#інформація)
  - [Оголошення, теги та нагадування](#оголошення-теги-та-нагадування)
  - [Мод-пошта та апеляції на бан](#мод-пошта-та-апеляції-на-бан)
  - [Канал рахунку, закріплені повідомлення та статистика](#канал-рахунку-закріплені-повідомлення-та-статистика)
  - [Додаткові можливості наявних функцій](#додаткові-можливості-наявних-функцій)
  - [Інші інструменти AutoMod](#інші-інструменти-automod)
  - [Ліміти модераторів і аудит прав](#ліміти-модераторів-і-аудит-прав)
  - [Скарги та відстеження запрошень](#скарги-та-відстеження-запрошень)
  - [Діагностика та налагодження](#діагностика-та-налагодження)
  - [Музика](#музика)
  - [Налаштування та перевірка стану](#налаштування-та-перевірка-стану)
  - [Економіка](#економіка)
  - [Меню ролей, відкладені повідомлення та стрічки](#меню-ролей-відкладені-повідомлення-та-стрічки)
  - [Активність, масові дії та пошук справ](#активність-масові-дії-та-пошук-справ)
  - [Захист від шахрайства та крипто-скаму](#захист-від-шахрайства-та-крипто-скаму)
  - [Випробувальний термін, виявлення рою, хронологія та навчання](#випробувальний-термін-виявлення-рою-хронологія-та-навчання)
  - [Конструктор повідомлень та оновлення](#конструктор-повідомлень-та-оновлення)
  - [Експлуатація](#експлуатація)
  - [Адміністрування](#адміністрування-1)
- [Підстановки в повідомленнях](#підстановки-в-повідомленнях)
- [Налаштування](#налаштування)
- [Дані та зберігання](#дані-та-зберігання)
- [Структура репозиторію](#структура-репозиторію)
- [Переклади](#переклади)
- [Плани](#плани)
- [Конфіденційність і безпека](#конфіденційність-і-безпека)
- [Підтримка](#підтримка)
- [Подяки](#подяки)
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
- Захист від шахрайства: підроблені розіграші та крипто-скам видаляються в тексті й на зображеннях за мілісекунди, зокрема скам із MrBeast за будь-якого написання.

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
- Економіка з магазином, меню ролей із кнопками чи списком, відкладені повідомлення, стрічки YouTube, Twitch і RSS, статистика активності та покроковий /setup. Повідомлення для учасників доступні 12 мовами.

### Адміністрування

- Кожен модуль і кожну команду можна вмикати та вимикати для кожного сервера.
- Власний префікс, псевдоніми команд і перейменування команд.
- Резервне копіювання та відновлення ролей і структури каналів.
- Автоматичні резервні копії за розкладом для ролей, каналів, емодзі та вебхуків, із командою відновлення, яка додає лише те, чого бракує.
- Панель керування: зміна налаштувань кожного сервера в браузері після входу через Discord, лише для учасників, які керують сервером, і лише доки бот підключений.

## Стан проєкту

GuardBot ще молодий і поки що не використовувався на великих серверах. Автоматичні тести (`python -m unittest`) охоплюють сховище, виявлення особистих даних, розрахунок рівнів, реєстрацію команд, перевірки прав і посилання в документації. Усе, що потребує справжнього сервера Discord, наприклад блокування сервера, відновлення з копії, верифікація, захист від нюку та гулаг, тестами не охоплюється. Спершу перевірте ці функції на тестовому сервері, перш ніж на них покладатися. Переклади документації не перевіряли носії мови, виправлення вітаються.

## Вимоги

- Python 3.11 або новіший
- Застосунок Discord із токеном бота
- Комп'ютер або VPS, що завжди в мережі
- ffmpeg (лише для модуля музики)
- tesseract-ocr (необов'язково, лише для читання тексту на зображеннях)

## Швидкий старт

Оберіть свою систему. Для будь-якого варіанта потрібні Python 3.11 або новіший і токен вашого бота. Докладний покроковий посібник міститься в [GUIDE.md](GUIDE.md).

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

### Скрипти запуску та автозапуск

Скрипти запуску створюють віртуальне середовище, встановлюють пакети та запускають бота. Під час першого запуску вони створюють файл .env і зупиняються, щоб ви могли вписати токен. Після цього запустіть їх знову.

```bash
./start.sh
```

```bat
start.bat
```

Щоб бот працював і після перезавантаження комп'ютера, використовуйте службу. Linux (systemd) і macOS (launchd):

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

У Windows створіть у Планувальнику завдань завдання, яке запускає start.bat під час входу в систему, або скористайтеся оболонкою для служб, наприклад NSSM. Для Docker дивіться [GUIDE.md](GUIDE.md).

### Оновлення

Зупиніть бота, виконайте ці команди та запустіть його знову. Ваші дані в папці data залишаються недоторканими, а перед кожною зміною формату даних бот робить резервну копію бази.

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

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

## Панель керування

Панель керування — це вебсторінка, що працює всередині бота. Після входу через Discord ви змінюєте налаштування своїх серверів перемикачами, меню та полями замість команд: модулі, канали, ролі, порогові значення, тексти, префікс і мова. Вона також показує останні справи модерації, експортує та імпортує налаштування. Вона однаково працює на вашому комп'ютері та на VPS і вимкнена, доки ви її не ввімкнете.

### Налаштування панелі

1. Відкрийте свій застосунок у Developer Portal, перейдіть до OAuth2 і скопіюйте Client Secret у файл .env.
2. На тій самій сторінці додайте адресу перенаправлення http://localhost:8080/callback.
3. Увімкніть панель у settings.json.
4. Перезапустіть бота та відкрийте http://localhost:8080 у браузері. Увійдіть через Discord.

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

### Безпека

- Вхід лише через Discord (OAuth2, область identify). Токен доступу одразу відкликається й ніколи не зберігається.
- Доступ мають лише власник сервера та учасники з правом «Адміністратор» або «Керувати сервером», і лише до цього сервера. Право перевіряється заново під час кожного запиту.
- Відкрити можна лише сервери, до яких бот підключений саме зараз. Якщо бот не в мережі, не на сервері або ще запускається, панель відмовляє в усьому. Вона працює всередині бота й не має власної бази даних чи служби.
- За замовчуванням вона слухає лише 127.0.0.1, тому ніхто інший у мережі не може до неї дістатися. Публічна адреса приймається лише з HTTPS, інакше панель не запускається.
- Сесії використовують випадковий токен у cookie HttpOnly з SameSite і, за HTTPS, з префіксом __Host-. Вони закінчуються через 8 годин і зберігаються лише в пам'яті, тому перезапуск завершує всі сесії.
- Кожна зміна потребує CSRF-токена та відповідного Origin. Заголовок Host перевіряється проти DNS rebinding. Сторінка не завантажує зовнішніх скриптів, сувора Content Security Policy блокує вбудований код, запити обмежені за частотою, а тіло запиту обмежене 256 КБ.
- Кожне значення перевіряється за типом налаштування, а ID Discord мають існувати на сервері. Внутрішній стан, як-от лічильники, тікети та збережені записи, змінити не можна. Кожна зміна записується в канал журналу безпеки сервера.
- Вміст повідомлень ніколи не показується. Справи модерації доступні лише для читання.

### Панель на VPS

Залиште host рівним 127.0.0.1 і виберіть один із двох шляхів. Перший — SSH-тунель: назовні нічого не відкривається, а http://localhost:8080 ви відкриваєте на своєму комп'ютері, поки працює тунель.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Другий — HTTPS через зворотний проксі, наприклад Caddy, який сам отримує сертифікат (див. deploy/Caddyfile.example). Потім вкажіть у public_url свою https-адресу, додайте https://ваша-адреса/callback як перенаправлення в Developer Portal і встановіть trust_proxy у true:

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

Редактор показує кожне налаштування, що є перемикачем, числом, текстом, каналом, роллю або простим списком. Те, що створюється командами, наприклад товари магазину, меню ролей, стрічки, теги та тікети, залишається за командами. Сторінка доступна англійською та німецькою і слідує мові браузера. У Docker публікуйте порт лише на 127.0.0.1 (127.0.0.1:8080:8080), а в контейнері встановіть host у 0.0.0.0 і allow_insecure_http у true.

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
/case view case_id:12

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
/suggestion setup set channel:#suggestions review_role:@Staff
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

### Ролі за реакцію та сповіщення

Видавайте ролі за реакції з будь-якими емодзі й дозвольте учасникам обирати теми сповіщень.

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

### Дні народження

Учасники вказують день і місяць, бот видає роль і пише повідомлення цього дня.

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

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

### Інструменти модератора

Очищення каналів, керування ролями та особисті нотатки. Кожна дія записується в журнал.

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

### Інформація

Довідка про користувачів, сервер, ролі та бота.

```
/userinfo user:@User
/serverinfo
/roleinfo role:@Moderator
/avatar user:@User
/help command:ban                                  # explains one command
/ping
/botinfo
```

### Оголошення, теги та нагадування

Повідомлення від імені бота, власні команди, автовідповіді на повідомлення та нагадування.

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

### Мод-пошта та апеляції на бан

Учасники пишуть команді через приватний канал на сервері. Нікому не потрібно писати боту в особисті повідомлення.

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

### Канал рахунку, закріплені повідомлення та статистика

Гра в рахунок, повідомлення, що залишаються внизу каналу, та канали з живими числами.

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

### Додаткові можливості наявних функцій

Доповнення для тикетів, розіграшів, голосових кімнат, XP, днів народження, резервних копій, журналів та екранів стану.

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

### Інші інструменти AutoMod

Перевірка коротких посилань, обмеження посилань для новачків, пошук ghost ping і перевірка правил без покарань.

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

### Ліміти модераторів і аудит прав

Сигнал, якщо модератор надто часто банить або кікає, та огляд ролей із небезпечними правами.

```
/modwatch status
/modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/modwatch exclude member:@TrustedMod

/permaudit run                                                  # roles with dangerous permissions and who holds them
/permaudit watch enabled:True                                   # alarm when a role or member gets one
/permaudit trust role:@Admin
```

### Скарги та відстеження запрошень

Учасники скаржаться на повідомлення команді, а бот запам'ятовує, яке запрошення привело нового учасника.

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

### Діагностика та налагодження

Пошук відсутніх прав і хибних налаштувань, звіти про помилки в каналі, експорт та імпорт налаштувань.

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

### Музика

Відтворює посилання та файли з папки music у голосовому каналі. Завантаження зберігаються як music/Виконавець/Альбом/Трек. Потрібні ffmpeg і пакети з requirements.txt.

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

Без втрат: ваші власні файли (FLAC, WAV, ALAC) та джерела з FLAC відтворюються без змін. YouTube, SoundCloud та подібні сайти віддають лише звук із втратами, який неможливо потім зробити lossless. Discord передає голос у форматі Opus, бот використовує бітрейт голосового каналу. Відповідальність: завантаження та відтворення вмісту може порушувати правила сайту або авторське право. Завантаження типово вимкнені, модуль вимкнений, доки ви його не ввімкнете. За відтворюване та збережене відповідає оператор бота.

### Налаштування та перевірка стану

Покроковий помічник налаштовує найважливіше кнопками та меню: канал логів, канал привітань, ролі команди, гулаг, пресет AutoMod (м'який, звичайний, суворий), шаблон сервера (спільнота, ігри, підтримка) та мову. /health показує, що вже налаштовано і що ще лишилося. Мова змінює тексти, які бачать учасники: привітання за замовчуванням, сповіщення AutoMod, верифікацію, тікети, апеляції, мод-пошту та меню ролей. Фіксовані відповіді адміністраторам перекладено, відповіді з іменами та числами залишаються англійською.

```
/setup                                                         # buttons and menus, nothing is switched off by a template
/health                                                        # what is set up, what is open, and the self-test
/language code:de
```

### Економіка

Валюта сервера з щоденною нагородою, роботою, переказами, рейтингом і магазином, товари якого можуть видавати роль. Вмикається модулем economy. Команди працюють і з префіксом, наприклад !economy daily.

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

### Меню ролей, відкладені повідомлення та стрічки

Меню ролей видають ролі кнопками або випадним списком. Відкладені повідомлення публікуються один раз або повторюються щогодини, щодня чи щотижня. Стрічки публікують нові відео YouTube, трансляції Twitch і записи RSS. Для YouTube потрібен ID каналу (починається з UC). Для Twitch у файлі .env потрібні TWITCH_CLIENT_ID і TWITCH_CLIENT_SECRET. Час записується як in 2h, 18:30 або як дата з часом, наприклад 2026-12-24 18:00, у часовому поясі сервера. Перша перевірка стрічки лише запам'ятовує те, що вже є.

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

### Активність, масові дії та пошук справ

Активність рахує повідомлення за каналами та входи й виходи за днями, але ніколи не вміст і не імена. Масові дії банять, кікають або відправляють у тайм-аут до 25 користувачів після підтвердження. Справи можна шукати за користувачем, типом, ім'ям, причиною, модератором і давністю та пов'язувати між собою, наприклад нотатку з баном.

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

### Захист від шахрайства та крипто-скаму

Видаляє підроблені розіграші, як-от типовий скам із MrBeast, у тексті та на зображеннях за мілісекунди. Імена з миттєвого списку видаляються одразу за будь-якого написання (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Інакше слова зі списків (імена, приманки, крипто, посилання, суми) додаються, і повідомлення видаляється при досягненні порогу. Зображення читаються через OCR, а зображення, яке раз визнали скамом, видаляється без повторного читання. Для читання зображень потрібен tesseract, без нього перевіряється лише текст. Сервер про MrBeast може прибрати ім'я з миттєвого списку або виключити канали командою /automod exemptchannel. Перевірте роботу командою /antiscam test, перш ніж на неї покладатися.

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

### Випробувальний термін, виявлення рою, хронологія та навчання

Випробувальний термін поміщає нових учасників у роль. Поки вони не напишуть задану кількість звичайних повідомлень або не мине заданий час, посилання, запрошення та файли видаляються з коротким сповіщенням. Захист від рейдів також розпізнає рій: кілька нових облікових записів з однаковим шаблоном імені, однаковою аватаркою або створених з різницею в кілька хвилин. Хронологія (/case timeline) збирає в порядку часу створення облікового запису, вхід і запрошення, випробувальний термін, справи та апеляції одного користувача. Повідомлення ніколи не зберігаються, тому в неї не входять. /block, /unblock і /blocklist керують блок-списком AutoMod короткими командами. Модератори навчають модуль захисту від шахрайства через пункт контекстного меню Mark as scam біля повідомлення або реакцією з емодзі з learn_emoji: повідомлення видаляється, а його зображення й текст відтоді видаляються одразу. Кожну частину вимикають її модулем або налаштуваннями.

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

### Конструктор повідомлень та оновлення

Конструктор повідомлень публікує повідомлення з кількома ембедами та кнопками-посиланнями з JSON. Він читає JSON, який експортують генератори ембедів, як-от Embed Generator, тож ви створюєте повідомлення там і публікуєте його ботом. Передайте JSON текстом, файлом .json або https-посиланням, що веде прямо на JSON, наприклад на «сирий» файл репозиторію (посилання з перенаправленням відхиляються). Створюються лише кнопки-посилання, кнопки, що потребують взаємодії, пропускаються. Кожне посилання має бути http або https, згадки в тексті ніколи не сповіщають, діють обмеження Discord. /message copy експортує наявне повідомлення в JSON, /message edit змінює повідомлення бота, а /message preview показує результат лише вам. Посилання для поширення з вебредакторів не відкриваються, бо їхній формат не публічний.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Кожні 12 годин бот перевіряє репозиторій GitHub з update.repo (задається скриптом scripts/set_repo_url.py) на наявність новішої версії. Якщо вона є, власник бота отримує особисте повідомлення з описом релізу, а реліз завантажується й перевіряється: контрольна сума SHA-256, безпечні шляхи всередині архіву та версія, що збігається з тегом. Встановлюється командою /debug update action:install або сама, якщо ввімкнено auto_install. Перед встановленням замінювані файли зберігаються в data/update, встановлюються нові пакети, а новий код пробно імпортується. У разі помилки старі файли відновлюються. Ваші .env, settings.json, data і music ніколи не змінюються. Потім бот перезапускається сам. У Docker нічого не встановлюється на місці, оновіть образ. Оновлення виконує код із репозиторію, тому вказуйте лише репозиторій, якому довіряєте. Вимикається параметром enabled зі значенням false.

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

### Експлуатація

Бот зберігає дані кожні кілька секунд і тримає резервні копії бази в data/dbbackups: одну перед кожною зміною формату даних і одну на день. Черга музики, закріплені повідомлення та лічильники модераторів переживають перезапуск. Великі боти можуть працювати на кількох шардах. Файл heartbeat і необов'язкова сторінка стану допомагають системам моніторингу. Ці параметри задаються в settings.json:

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
/birthday setup set   message                         {user} {name}
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

## Переклади

Англійська — мова оригіналу проєкту. Усі переклади документації, панелі та повідомлень бота створені машинним перекладом і не перевірялися носіями мови. Можливі невдалі формулювання та помилки, будь ласка, повідомляйте про них або надсилайте виправлення. Файли містяться в docs/ та guardbot/locales/.

## Плани

- Графіки активності та модерації в панелі.
- Перевірка всіх перекладів носіями мови.
- Переклад більшої кількості фіксованих текстів відповідей.

## Конфіденційність і безпека

- Жодної телеметрії. Бот спілкується з Discord і, для перевірки оновлень, з GitHub (особисті дані не надсилаються, вимикається параметром update.enabled). Посилання, які дають адміністратори, як-от стрічки, музика й посилання на JSON, відкриваються лише на запит.
- Усі дані зберігаються в папці data на вашому комп'ютері: налаштування, XP, дні народження (лише день і місяць) та випадки модерації.
- Бот ігнорує приватні повідомлення від учасників.
- Токен читається з файлу .env. Нікому його не передавайте і не публікуйте.
- Учасники можуть експортувати й видаляти свої дані командою /mydata. Адміністратори задають, як довго зберігаються дані тих, хто пішов.
- [PRIVACY.md](../PRIVACY.md)

## Підтримка

Помилки, ідеї та пропозиції: пишіть мені в Discord, @justyyin, або створіть issue на GitHub.

## Подяки

GuardBot натхненний проєктом [Embed Generator](https://github.com/merlinfuchs/embed-generator) Мерліна Фукса (ліцензія MIT, розміщений на message.style). Конструктор повідомлень читає той самий формат JSON, тому повідомлення, створені там, можна публікувати цим ботом. Код того проєкту не включено. Дякуємо авторам discord.py, aiohttp, Pillow, yt-dlp, mutagen і Tesseract.

## Ліцензія

Опубліковано за ліцензією MIT. Див. [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
