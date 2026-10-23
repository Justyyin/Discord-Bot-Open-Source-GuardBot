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
  - [Структура, учасники та команда](#структура-учасники-та-команда)
- [Панель керування](#панель-керування)
  - [Налаштування панелі](#налаштування-панелі)
  - [Команди, скіли, ШІ та профіль бота](#команди-скіли-ші-та-профіль-бота)
  - [Безпека](#безпека-1)
  - [Панель на VPS](#панель-на-vps)
- [Команди](#команди)
  - [Групи команд](#групи-команд)
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
  - [Панелі](#панелі)
  - [Скіли та ШІ](#скіли-та-ші)
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
- Канал «гулаг»: учасники, які публікують шахрайські посилання чи зображення, переміщуються в один канал з інструкцією із захисту акаунта. Модератори також можуть використовувати /moderation jail і /moderation unjail.
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
- Економіка з магазином, меню ролей із кнопками чи списком, відкладені повідомлення, стрічки YouTube, Twitch і RSS, статистика активності та покроковий /admin setup. Повідомлення для учасників доступні 12 мовами.

### Адміністрування

- Кожен модуль і кожну команду можна вмикати та вимикати для кожного сервера.
- Власний префікс, псевдоніми команд і перейменування команд.
- Резервне копіювання та відновлення ролей і структури каналів.
- Автоматичні резервні копії за розкладом для ролей, каналів, емодзі та вебхуків, із командою відновлення, яка додає лише те, чого бракує.
- Панель керування: зміна налаштувань кожного сервера в браузері після входу через Discord, лише для учасників, які керують сервером, і лише доки бот підключений.
- Скіли: власні команди, ігри й автоматизації з безпечних блоків, за бажанням написані ШІ з твоїм власним ключем (Anthropic, OpenAI, Kimi). Панель показує всі команди й редагує скіли, налаштування ШІ та профіль бота.

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

### Структура, учасники та команда

Версія 1.5 додає команди для створення й підтримання порядку на сервері, відновлення учасників, що повернулися, і керування командою модерації. Кожна частина має перемикач модуля (`/admin module`), власні налаштування та місце в панелі.

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

- За допомогою `/structure` канали й категорії створюються, клонуються, перейменовуються, сортуються, а права копіюються з іншого каналу. Про неактивні канали повідомляється, або їх переносять до категорії архіву (`/structure archive`). Ролі можна видавати на обмежений час і зберігати як шаблони; шаблон ніколи не надає право, якого немає в того, хто його застосовує.
- `/structure rules` публікує правила з кнопкою прийняття та номером версії. Після `post new_version:True` учасники, які не прийняли нову версію, отримують одне нагадування в особисті повідомлення.
- `/members stickyroles` повертає ролі та відновлює таймаут або м'ют, коли учасник повертається. `/members nickname` прибирає символи, що піднімають ім'я на початок списку, перевіряє заборонені слова в нікнеймах і іменах користувачів та перейменовує порушників. Список спостереження тихий: команда отримує сповіщення при першому повідомленні користувача зі списку.
- Погодження в чотири очі (`/security approval`) виконує бани, кіки, таймаути та масові дії лише після згоди другого модератора. `/moderation case undo` скасовує випадок разом із діями, які він спричинив (наприклад, м'ют і наступний бан). Попередження можуть спливати через задану кількість днів (`/moderation escalation expiry`).
- `/admin history` показує, хто і коли змінив налаштування, та відкочує розділ. Ім'я людини визначається припущенням за останніми командами та змінами в панелі на сервері. `/admin history copy` копіює розділи на інший сервер, яким ви можете керувати через бота; спочатку виконується пробний запуск. `/admin exceptions` виключає канали та ролі з правил AutoMod і Anti-Scam. `/admin dashaccess` дає ролям доступ до панелі лише для читання або як модератору.
- `/team` показує роботу кожного модератора (випадки, тікети, скарги, час реакції, неактивні учасники), публікує щотижневий звіт (день і година за UTC), дозволяє модераторам відмітити відсутність через `/team duty away`, щоб тікети й згадки йшли іншим, і веде заявки до команди з формою та голосуванням.
- Discord не вміє приховувати команди всередині групи від окремих учасників. Бот усе одно перевіряє кожен виклик. Цифри статистики команди рахуються з дня оновлення; раніші дії не враховуються.

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

### Команди, скіли, ШІ та профіль бота

У панелі ще п'ять сторінок: Panels (див. розділ «Панелі») і наступні чотири. «Команди» перелічує кожну слеш-команду, команду з префіксом і контекстне меню з модулем, потрібним правом і станом; адміністратори вмикають і вимикають їх, дозволяють або забороняють ролі та дають командам із префіксом короткі назви. Префікс змінюється на тій самій сторінці. «Скіли» показує всі скіли й редагує їх як JSON з тими самими перевірками, що й команди. «ШІ» задає модель і обмеження та зберігає ключ (лише запис, на сторінку він ніколи не повертається). «Профіль бота» змінює ім'я, картинку, банер і опис бота на цьому сервері; власник застосунку бота або ID із `owner_ids` у settings.json може змінювати їх і всюди. Discord обмежує, як часто можна змінювати ім'я та картинку. Кожна зміна записується в журнал аудиту.

Кожен модуль показано як плагін: сторінка Plugins виводить їх картками за категоріями, а кожен плагін має власну сторінку з перемикачем «Активно», налаштуваннями в розгортних блоках і командами з перемикачем і редактором ролей. Ліва панель перелічує плагіни за категоріями, крапка показує, чи вони ввімкнені. Панель керування має темне оформлення.

Панель керування доступна всіма 12 мовами бота. Мову вибирають угорі праворуч або на сторінці входу; вибір зберігається в браузері й не змінює мову сервера. Тексти панелі перекладено машинно.

Кожна сторінка плагіна пояснює, що робить плагін, перелічує всі його функції з окремим перемикачем і коротким поясненням, а решту налаштувань тримає в блоках нижче. На сторінці «Плагіни» й в огляді кожен плагін можна ввімкнути чи вимкнути напряму. У «Налаштуваннях» блок «Вигляд панелі» змінює акцентний колір, тло, блоки й текст, ставить шпалери (затемнені й розмиті на ваш смак) і додає до бічної панелі власні меню та вкладки: вкладка може збирати вибрані плагіни, відкривати сторінку, вести на https-адресу чи показувати нотатку. Вигляд зберігається для кожного сервера й видимий усім, хто відкриває його панель. У нижньому колонтитулі показано копірайт і посилання на Discord і GitHub; щоб там з'явилися офіційні логотипи, покладіть discord.svg і github.svg зі сторінок брендів Discord і GitHub у guardbot/web/brand/.

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

<!-- groups -->
### Групи команд

Щоб заощадити слоти слеш-команд (Discord дозволяє 100 команд верхнього рівня на бота), пов'язані команди об'єднано в групи. Спочатку вводиться група, потім команда, наприклад `/moderation ban`. Текстові команди з префіксом, наприклад `!ban`, не змінюються. Права, псевдоніми та перемикачі модулів, як і раніше, використовують просту назву команди.

| Група | Містить |
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

### Модерація

Попередження, м'юти, кіки та бани працюють як слеш-команди й з префіксом, наприклад `!warn @User spam`. Кожна дія створює пронумерований випадок.

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

Учасники зі зламаним акаунтом переміщуються в один канал з інструкцією щодо безпеки. Під час звільнення їм повертаються колишні ролі.

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

Кожен, хто потрапляє до ГУЛАГу — командою, через AutoMod, через антискам, під час повторного входу або тому, що хтось видав роль вручну, — отримує сповіщення Account Security Required зі згадкою. Поки в ГУЛАГу хтось є, унизу каналу висить Account Recovery Reminder, яке оновлюється кожні 10 хвилин. Учасник у ГУЛАГу, який напише в каналі ГУЛАГу префікс і слово для звільнення (наприклад `!unban`), створює запит на звільнення з кнопками Release і Keep для команди; сам бот нікого не звільняє. `/access jailsetup reminder` вмикає й вимикає кожну частину та задає інтервал і слово.

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

### Захист від нюку

Стежить за журналом аудиту й реагує, коли хтось руйнує сервер. Власник отримує приватне повідомлення.

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

### Верифікація

Нові учасники бачать лише канал верифікації, доки не натиснуть кнопку або не розв'яжуть капчу.

```
/access verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/access verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/access verify panel channel:#verify                      # post the button again
/access verify apply                                      # apply the channel permissions again
/access verify member member:@User                        # verify someone manually
/access verify off
```

### Журналювання

Оберіть канал для кожної категорії або один основний канал для всього.

```
/server log set category:main channel:#logs               # fallback for every category
/server log set category:messages channel:#log-messages
/server log set category:moderation channel:#log-moderation
/server log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/server log sent enabled:False                            # stop logging every sent message
/server log show
```

### Привітання, прощання та бустери

Повідомлення, авторолі та нагороди для бустерів сервера.

```
/community welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/community welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/community welcome autorole role:@Member                     # toggle, given to every new member
/community welcome botrole role:@Bots                        # toggle, given to every new bot
/community welcome test

/community booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/community booster role role:@Booster                        # toggle
```

### Тікети

Учасники відкривають приватні канали кнопкою. Під час закриття надсилається стенограма.

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

### Опитування та розіграші

Кнопки для голосування й участі. Тривалість приймає значення на кшталт 30m, 2h і 1d.

```
/engage poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/engage poll end poll_id:3
/engage poll list

/engage giveaway start prize:Nitro duration:2d winners:2 role:@Member
/engage giveaway end giveaway_id:1
/engage giveaway reroll giveaway_id:1
/engage giveaway list
```

### Пропозиції та starboard

Учасники публікують пропозиції, які команда може схвалити або відхилити, а популярні повідомлення виділяються.

```
/suggestion setup set channel:#suggestions review_role:@Staff
/support suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/engage starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/engage starboard ignore channel:#spam
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

/info rank                                              # also: !rank, shows a rank card image
/info rank user:@User
/info leaderboard
```

### Ролі за реакцію та сповіщення

Видавайте ролі за реакції з будь-якими емодзі й дозвольте учасникам обирати теми сповіщень.

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
/community tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Резервні копії та відновлення

Копії містять ролі, канали, емодзі, вебхуки та ролі учасників. Відновлення додає лише те, чого бракує.

```
/server backup create name:before-update
/server backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/server backup list
/server backup download name:before-update
/server backup restore name:before-update member_roles:True   # only adds what is missing
/server backup delete name:before-update
```

### Дані та конфіденційність

Учасники можуть експортувати й видаляти свої дані. Адміністратори задають строк зберігання.

```
/info mydata export                                     # members download their own data
/info mydata delete confirm:True                        # members delete their XP and birthday

/server privacy retention days:90                         # delete data of members who left after 90 days
/server privacy export user_id:123456789012345678
/server privacy delete user_id:123456789012345678 cases:True
```

### Інструменти модератора

Очищення каналів, керування ролями та особисті нотатки. Кожна дія записується в журнал.

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

### Інформація

Довідка про користувачів, сервер, ролі та бота.

```
/info userinfo user:@User
/server serverinfo
/server roleinfo role:@Moderator
/info avatar user:@User
/help command:ban                                  # explains one command
/info ping
/info botinfo
```

### Оголошення, теги та нагадування

Повідомлення від імені бота, власні команди, автовідповіді на повідомлення та нагадування.

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

### Додаткові можливості наявних функцій

Доповнення для тикетів, розіграшів, голосових кімнат, XP, днів народження, резервних копій, журналів та екранів стану.

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
/team modwatch status
/team modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/team modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/team modwatch exclude member:@TrustedMod

/team permaudit run                                                  # roles with dangerous permissions and who holds them
/team permaudit watch enabled:True                                   # alarm when a role or member gets one
/team permaudit trust role:@Admin
```

### Скарги та відстеження запрошень

Учасники скаржаться на повідомлення команді, а бот запам'ятовує, яке запрошення привело нового учасника.

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

### Діагностика та налагодження

Пошук відсутніх прав і хибних налаштувань, звіти про помилки в каналі, експорт та імпорт налаштувань.

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

Без втрат: ваші власні файли (FLAC, WAV, ALAC) та джерела з FLAC відтворюються без змін. YouTube, SoundCloud та подібні сайти віддають лише звук із втратами, який неможливо потім зробити lossless. Discord передає голос у форматі Opus, бот використовує бітрейт голосового каналу. Відповідальність: завантаження та відтворення вмісту може порушувати правила сайту або авторське право. Завантаження типово вимкнені, модуль вимкнений, доки ви його не ввімкнете. За відтворюване та збережене відповідає оператор бота.

Джерела: посилання й пошук YouTube і SoundCloud відтворюються напряму. Посилання Spotify, Apple Music і Tidal теж приймаються, але ці сервіси не віддають своє аудіо: бот читає назву й виконавця з публічної сторінки та грає ту саму пісню з джерела пошуку (YouTube або SoundCloud, налаштовується через /music sources). Альбоми й плейлисти Spotify і Apple Music читаються з їхніх публічних сторінок; для альбомів і плейлистів Tidal потрібен безкоштовний ключ розробника з developer.tidal.com у .env (TIDAL_CLIENT_ID і TIDAL_CLIENT_SECRET). Файли з вашої папки з музикою відтворюються як є. Збережені плейлисти можуть змішувати всі джерела, а /music stay тримає бота в голосовому каналі цілодобово й грає плейлист по колу, зокрема після перезапуску.

Guard Music, другий бот: музика може працювати на окремому акаунті бота, щоб постійно залишатися в голосовому каналі, не зачіпаючи модерацію.

1. Створіть другий застосунок у Discord Developer Portal, назвіть його Guard Music і скопіюйте токен його бота.
2. Запишіть токен у .env як MUSIC_TOKEN і встановіть music_bot.enabled у true в settings.json.
3. Перезапустіть GuardBot. Guard Music запускається в тому самому процесі, використовує ті самі налаштування й дані, і музичні команди переходять до нього.
4. Відкрийте в панелі сторінку «Музика» й додайте Guard Music на сервер кнопкою там. Без MUSIC_TOKEN музика залишається в GuardBot.

Використовуйте на власний ризик: трансляція з YouTube та інших сервісів може порушувати їхні умови користування, а на те, що звучить, поширюється авторське право. Зі Spotify, Apple Music і Tidal нічого не завантажується, і жоден захист не обходиться. За те, що звучить, відповідає власник бота. Сторінка «Музика» в панелі показує плеєр, чергу, плейлисти, режим 24/7, джерела й цю інструкцію.

### Налаштування та перевірка стану

Покроковий помічник налаштовує найважливіше кнопками та меню: канал логів, канал привітань, ролі команди, гулаг, пресет AutoMod (м'який, звичайний, суворий), шаблон сервера (спільнота, ігри, підтримка) та мову. /server health показує, що вже налаштовано і що ще лишилося. Мова змінює тексти, які бачать учасники: привітання за замовчуванням, сповіщення AutoMod, верифікацію, тікети, апеляції, мод-пошту та меню ролей. Фіксовані відповіді адміністраторам перекладено, відповіді з іменами та числами залишаються англійською.

```
/admin setup                                                         # buttons and menus, nothing is switched off by a template
/server health                                                        # what is set up, what is open, and the self-test
/admin language code:de
```

### Економіка

Валюта сервера з щоденною нагородою, роботою, переказами, рейтингом і магазином, товари якого можуть видавати роль. Вмикається модулем economy. Команди працюють і з префіксом, наприклад !economy daily.

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

### Меню ролей, відкладені повідомлення та стрічки

Меню ролей видають ролі кнопками або випадним списком. Відкладені повідомлення публікуються один раз або повторюються щогодини, щодня чи щотижня. Стрічки публікують нові відео YouTube, трансляції Twitch і записи RSS. Для YouTube потрібен ID каналу (починається з UC). Для Twitch у файлі .env потрібні TWITCH_CLIENT_ID і TWITCH_CLIENT_SECRET. Час записується як in 2h, 18:30 або як дата з часом, наприклад 2026-12-24 18:00, у часовому поясі сервера. Перша перевірка стрічки лише запам'ятовує те, що вже є.

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

### Активність, масові дії та пошук справ

Активність рахує повідомлення за каналами та входи й виходи за днями, але ніколи не вміст і не імена. Масові дії банять, кікають або відправляють у тайм-аут до 25 користувачів після підтвердження. Справи можна шукати за користувачем, типом, ім'ям, причиною, модератором і давністю та пов'язувати між собою, наприклад нотатку з баном.

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

### Захист від шахрайства та крипто-скаму

Видаляє підроблені розіграші, як-от типовий скам із MrBeast, у тексті та на зображеннях за мілісекунди. Імена з миттєвого списку видаляються одразу за будь-якого написання (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Інакше слова зі списків (імена, приманки, крипто, посилання, суми) додаються, і повідомлення видаляється при досягненні порогу. Зображення читаються через OCR, а зображення, яке раз визнали скамом, видаляється без повторного читання. Для читання зображень потрібен tesseract, без нього перевіряється лише текст. Сервер про MrBeast може прибрати ім'я з миттєвого списку або виключити канали командою /automod exemptchannel. Перевірте роботу командою /security antiscam test, перш ніж на неї покладатися.

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

### Випробувальний термін, виявлення рою, хронологія та навчання

Випробувальний термін поміщає нових учасників у роль. Поки вони не напишуть задану кількість звичайних повідомлень або не мине заданий час, посилання, запрошення та файли видаляються з коротким сповіщенням. Захист від рейдів також розпізнає рій: кілька нових облікових записів з однаковим шаблоном імені, однаковою аватаркою або створених з різницею в кілька хвилин. Хронологія (/moderation case timeline) збирає в порядку часу створення облікового запису, вхід і запрошення, випробувальний термін, справи та апеляції одного користувача. Повідомлення ніколи не зберігаються, тому в неї не входять. /security block, /security unblock і /security blocklist керують блок-списком AutoMod короткими командами. Модератори навчають модуль захисту від шахрайства через пункт контекстного меню Mark as scam біля повідомлення або реакцією з емодзі з learn_emoji: повідомлення видаляється, а його зображення й текст відтоді видаляються одразу. Кожну частину вимикають її модулем або налаштуваннями.

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

### Панелі

Панелі — це публікації на кшталт привітання, правил, вибору ролі, кнопок сповіщень або верифікації, з банерами, текстовими блоками й кнопками. Їх створюють командою `/panel` або в панелі керування на сторінці Panels. Картинки завантажуються там або як параметри команди, бот зберігає їх у `data/panels`, тож вони не зникають.

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

Шаблони: empty, welcome, rules, roles, notifications і verify; їхні тексти мовою сервера і їх можна змінювати. `/panel section` відкриває форму для заголовка, тексту й підпису. Кожен розділ стає окремим повідомленням: банер над блоком, велика картинка всередині, маленька — праворуч угорі. Кнопки розташовані під останнім розділом, по п'ять у ряд. Кнопка ролі видає роль або забирає її; з `single` інші ролі панелі знімаються. Кнопка verify запускає перевірку модуля верифікації (`/access verify setup` обирає кнопку, капчу чи приклад). У текстах можна використовувати `{server}` і `{count}`. `/panel update` змінює опубліковані повідомлення після редагування. Обмеження на сервер: 25 панелей, 5 розділів і 20 кнопок на панель, 40 картинок до 8 МБ. Бот пропонує лише ролі нижче за свою найвищу роль і без небезпечних прав.

### Скіли та ШІ

Скіли — це команди, ігри й автоматизації, які сервер збирає сам із безпечних блоків. Їм не потрібен ШІ, і вони ніколи не виконують код. ШІ необов'язковий: з твоїм власним ключем він пише скіл за описом і дає другу думку в перевірці антискаму.

Скіли без ШІ:

- `/support skill create kind:command name:hello` відкриває вікно з невеликим прикладом, який ти змінюєш. `/support skill edit`, `show`, `import`, `enable`, `disable`, `delete`, `list` і `stats` керують ними. Усі користуються скілом через `/support skill run` або з префіксом, наприклад `!hello`. `/support skill panel` публікує кнопки, що запускають скіли.
- Види: команда (список дій), гра (кубик, вибір, слоти, камінь-ножиці-папір, вікторина) та автоматизація (запускається, коли учасник приєднується чи йде, коли повідомлення містить слова або коли натиснуто кнопку).
- Дії: відповісти, надіслати в канал, особисте повідомлення, запис у журнал, видати чи забрати роль, змінити лічильник, видати монети, вибрати випадково. Дія може мати умови: має роль, ймовірність, лічильник порівняно з числом.
- У текстах можна використовувати `{user}`, `{user_name}`, `{server}`, `{channel}`, `{count}`, `{arg1}`, `{arg2}`, `{var:name}`, `{uvar:name}` і `{random:1-6}`.
- Обмеження: 50 скілів на сервер, 10 дій на скіл, 3 зміни ролей і 4 повідомлення на скіл. Бот видає лише ролі нижче за власну найвищу роль і без небезпечних прав. Скілу, що видає монети, потрібна пауза не менше 60 секунд. Не можна використовувати назви команд бота, аліасів і тегів.
- Скіли зберігаються як JSON і входять в експорт налаштувань. Невідомі поля відхиляються, тож скіл з будь-якого джерела може робити лише те, що дозволяють блоки.

Приклад: команда, що видає роль і рахує використання (заміни ID ролі):

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

Підключення ШІ (необов'язково):

- `/support ai setup provider:kimi agree:true` відкриває приватне вікно для твого ключа API. Провайдери: Anthropic, OpenAI і Kimi (Moonshot). Модель пропонується автоматично й змінюється в тій самій команді або в панелі; назви моделей у провайдерів змінюються, тож перевіряй їхню документацію. Ти платиш своєму провайдеру.
- `/support ai make wish:...` просить ШІ написати скіл, перевіряє відповідь так само суворо, як імпортований скіл, і показує попередній перегляд. Нічого не зберігається, доки ти не натиснеш «Зберегти».
- `/support ai status`, `limits` (запитів на день, секунд між запитами однієї людини) і `remove` доповнюють набір. Ключ зберігається в зашифрованому вигляді, секрет лежить у файлі `data/ai.secret`. Зберігай цей файл разом із резервними копіями; без нього збережений ключ не прочитати, і його доведеться ввести знову. Ключ ніколи не показується, не пишеться в журнал і не експортується. Провайдер змінюється лише разом із новим ключем, тож ключ ніколи не потрапляє до іншого провайдера.
- Що надсилається: побажання з `/support ai make` і, під час другої думки, текст підозрілого повідомлення. Більше нічого, і лише поки ввімкнено модуль `ai`. Див. [PRIVACY.md](../PRIVACY.md).

Навчання антискаму:

- Навчений фільтр (`/security antiscam set learned:true`) — невеликий класифікатор для кожного сервера. Модератори навчають його пунктами контекстного меню «Mark as scam» і «Not a scam». Він зберігає лише короткі хеші слів, ніколи сам текст, починає діяти лише після 8 прикладів скаму і 30 звичайних, і тоді лише за впевненості понад 95 відсотків. З `ham_sampling` він також вчиться на кожному десятому звичайному повідомленні.
- Схожі зображення (`similar`, типово ввімкнено) порівнюють відбиток картинки з відомими скам-картинками, тож знаходиться і пересохранена, і зменшена копія. Це працює без Tesseract.
- Друга думка ШІ (`/support ai limits second_opinion:true`): у випадках трохи нижче порога або тих, що навчений фільтр вважає підозрілими, питають ШІ. Повідомлення видаляється, лише якщо ШІ відповідає «скам» із упевненістю не нижче 80 відсотків, а його відповідь не може викликати нічого іншого.

### Конструктор повідомлень та оновлення

Конструктор повідомлень публікує повідомлення з кількома ембедами та кнопками-посиланнями з JSON. Він читає JSON, який експортують генератори ембедів, як-от Embed Generator, тож ви створюєте повідомлення там і публікуєте його ботом. Передайте JSON текстом, файлом .json або https-посиланням, що веде прямо на JSON, наприклад на «сирий» файл репозиторію (посилання з перенаправленням відхиляються). Створюються лише кнопки-посилання, кнопки, що потребують взаємодії, пропускаються. Кожне посилання має бути http або https, згадки в тексті ніколи не сповіщають, діють обмеження Discord. /post message copy експортує наявне повідомлення в JSON, /post message edit змінює повідомлення бота, а /post message preview показує результат лише вам. Посилання для поширення з вебредакторів не відкриваються, бо їхній формат не публічний.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Кожні 12 годин бот перевіряє репозиторій GitHub з update.repo (задається скриптом scripts/set_repo_url.py) на наявність новішої версії. Якщо вона є, власник бота отримує особисте повідомлення з описом релізу, а реліз завантажується й перевіряється: контрольна сума SHA-256, безпечні шляхи всередині архіву та версія, що збігається з тегом. Встановлюється командою /server debug update action:install або сама, якщо ввімкнено auto_install. Перед встановленням замінювані файли зберігаються в data/update, встановлюються нові пакети, а новий код пробно імпортується. У разі помилки старі файли відновлюються. Ваші .env, settings.json, data і music ніколи не змінюються. Потім бот перезапускається сам. У Docker нічого не встановлюється на місці, оновіть образ. Оновлення виконує код із репозиторію, тому вказуйте лише репозиторій, якому довіряєте. Вимикається параметром enabled зі значенням false.

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

### Експлуатація

Бот зберігає дані кожні кілька секунд і тримає резервні копії бази в data/dbbackups: одну перед кожною зміною формату даних і одну на день. Черга музики, закріплені повідомлення та лічильники модераторів переживають перезапуск. Великі боти можуть працювати на кількох шардах. Файл heartbeat і необов'язкова сторінка стану допомагають системам моніторингу. Ці параметри задаються в settings.json:

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

Журнали записуються в data/guardbot.log (з ротацією, див. log_max_mb і log_backups). Якщо log_format = json, кожен рядок — це JSON-об'єкт із сервером і командою. Якщо задано health_port, /metrics віддає метрики Prometheus (час роботи, затримка, пам'ять, розмір бази даних, помилки, використання та тривалість команд, лінії обробки). Експортуються лише числа, ніколи імена чи ID, а metrics_token вимагає bearer-токен. Важка робота (читання зображень, малювання карток, музичні файли, резервні копії) виконується в лініях із фіксованою кількістю потоків і лімітом (workers у settings.json). Коли лінія заповнена, бот повідомляє, що зайнятий, замість накопичення роботи. Кожна резервна копія бази даних відкривається та перевіряється відразу після створення. Щоб відновити копію, зупиніть бота і виконайте:

```
python scripts/restore_db.py data/dbbackups/guardbot-YYYYMMDD-HHMMSS-auto.db
python scripts/restore_db.py BACKUPFILE --check          # only check a backup
```

Поточна база даних зберігається як копія з назвою before-restore.

### Адміністрування

Вмикання й вимикання модулів і команд, зміна префікса, псевдоніми та обмеження команд за ролями.

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

## Підстановки в повідомленнях

Ці підстановки замінюються в налаштованих вами текстах:

```
/community welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/community booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/community tempvoice setup     name                            {name}
/access jailsetup notice    text                            {staff}
```

## Налаштування

Глобальні параметри задаються в settings.json. Усе інше налаштовується для кожного сервера командами /admin module, /admin command, /admin perms, /admin alias і /admin config.

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

Будь-яке налаштування можна прочитати й змінити командою /admin config. Ось шляхи, які знадобляться найчастіше:

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
    defaults/             default settings, one file per area (core, security, moderation, community) and base.py for modules and permissions
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature, in the folders security, moderation, server, community, tools
    skills.py             рушій скілів: перевіряє й виконує скіли
    ai.py                 провайдери ШІ, зашифровані ключі, обмеження
    learner.py, imgsim.py навчений фільтр антискаму, відбитки картинок
    dashboard_manage.py   сторінки панелі для команд, скілів, ШІ та профілю
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
- Учасники можуть експортувати й видаляти свої дані командою /info mydata. Адміністратори задають, як довго зберігаються дані тих, хто пішов.
- Функції ШІ вимкнені, доки ти не додаси свій ключ. Після цього обраному провайдеру надсилаються лише текст `/support ai make` і, під час другої думки, підозрілі повідомлення.
- [PRIVACY.md](../PRIVACY.md)

## Підтримка

Помилки, ідеї та пропозиції: пишіть мені в Discord, @justyyin, або створіть issue на GitHub.

## Подяки

GuardBot натхненний проєктом [Embed Generator](https://github.com/merlinfuchs/embed-generator) Мерліна Фукса (ліцензія MIT, розміщений на message.style). Конструктор повідомлень читає той самий формат JSON, тому повідомлення, створені там, можна публікувати цим ботом. Код того проєкту не включено. Дякуємо авторам discord.py, aiohttp, Pillow, yt-dlp, mutagen і Tesseract.

## Ліцензія

Опубліковано за ліцензією MIT. Див. [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
