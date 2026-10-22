# GuardBot: Посібник із встановлення

Цей посібник показує, як запустити GuardBot на власному комп'ютері або на VPS. Це займе близько 15 хвилин.

> Бета: GuardBot і його панель керування перебувають у стадії бети. Їх не було ретельно протестовано, особливо на великих серверах і в усіх ситуаціях Discord. Можливі помилки, робіть резервні копії папки data та повідомляйте про проблеми. Використання на власний ризик.

<!-- toc -->

- [Створення Discord-бота](#створення-discord-бота)
- [Запуск на власному комп'ютері](#запуск-на-власному-компютері)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux і macOS](#linux-і-macos)
- [Запуск на VPS](#запуск-на-vps)
- [Запуск через Docker](#запуск-через-docker)
- [Перші кроки в Discord](#перші-кроки-в-discord)
- [Оновлення та резервні копії](#оновлення-та-резервні-копії)
- [Музика (необов'язково)](#музика-необовязково)
- [Необов'язково: читання зображень і мови](#необовязково-читання-зображень-і-мови)
- [Панель керування](#панель-керування)
- [Усунення несправностей](#усунення-несправностей)
- [Підтримка](#підтримка)

<!-- tocstop -->

## Створення Discord-бота

1. Відкрийте [Discord Developer Portal](https://discord.com/developers/applications) і натисніть New Application.
2. Відкрийте вкладку Bot і натисніть Reset Token. Скопіюйте токен і тримайте його в таємниці.
3. На тій самій вкладці увімкніть Server Members Intent і Message Content Intent.
4. Відкрийте OAuth2, URL Generator. Виберіть scopes bot і applications.commands.
5. Виберіть права: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, View Audit Log, Manage Messages, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Move Members. Administrator теж підходить і є найпростішим варіантом.
6. Відкрийте створене посилання та додайте бота на свій сервер.
7. У налаштуваннях сервера перемістіть роль бота на самий верх списку ролей. Бот може керувати лише ролями, що розташовані нижче за його власну.

Також можна скористатися цим посиланням-запрошенням. Замініть YOUR_CLIENT_ID на Application ID із Developer Portal:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## Запуск на власному комп'ютері

Встановіть Python 3.11 або новіший і Git, потім виконайте ці команди в терміналі.

### Windows (PowerShell)

```powershell
git clone <REPOSITORY_URL>
cd guardbot
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
python main.py
```

### Linux і macOS

```bash
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
```

Відкрийте файл .env і замініть зразок токеном вашого бота. Бот буде в мережі, щойно в консолі з'явиться рядок, що починається з online as. Не закривайте вікно: бот зупиняється разом із ним.

## Запуск на VPS

Ці команди підходять для Ubuntu та Debian і налаштовують бота як службу з автозапуском.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0
sudo git clone <REPOSITORY_URL> /opt/guardbot
sudo useradd --system --no-create-home --shell /usr/sbin/nologin guardbot
cd /opt/guardbot
sudo python3 -m venv .venv
sudo .venv/bin/pip install -r requirements.txt
sudo cp .env.example .env
sudo nano .env
sudo mkdir -p data
sudo chown -R guardbot:guardbot /opt/guardbot
sudo chmod 600 .env
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now guardbot
sudo journalctl -u guardbot -f
```

Стан перевіряється командою systemctl status guardbot. Коли бот готовий, у журналі з'являється рядок, що починається з online as.

## Запуск через Docker

Docker необов'язковий. Спершу створіть файл .env, потім виконайте:

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## Перші кроки в Discord

Використовуйте ці команди на своєму сервері та замініть назви каналів своїми.

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

Усі функції описано в довіднику команд: [COMMANDS.md](../COMMANDS.md).

## Оновлення та резервні копії

Оновлення бота:

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

Збережіть налаштування, скопіювавши папку data, наприклад:

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## Музика (необов'язково)

Для модуля музики потрібен ffmpeg на комп'ютері, де працює бот. Покладіть свою музику в папку music/ як Виконавець/Альбом/01 - Назва.flac або дозвольте завантаження. Папка може стати великою, тому тримайте її на диску з місцем або в томі Docker.

```
# Windows
winget install Gyan.FFmpeg
# macOS
brew install ffmpeg
# Ubuntu or Debian
sudo apt install -y ffmpeg libopus0

# in Discord
/module enable name:music
/music settings allow_download:True
```

## Необов'язково: читання зображень і мови

Щоб модуль захисту від шахрайства читав текст на зображеннях, встановіть tesseract на комп'ютері, де працює бот (в образі Docker він уже є). Потім перевірте командою /antiscam status, що він готовий. Мову повідомлень, які бачать учасники, обирають командою /language.

```
# Ubuntu or Debian
sudo apt install -y tesseract-ocr
# macOS
brew install tesseract
# Windows
winget install UB-Mannheim.TesseractOCR

# in Discord
/antiscam status
/language code:de
```

## Панель керування

Панель керування — це вебсторінка, що працює всередині бота. Після входу через Discord ви змінюєте налаштування своїх серверів перемикачами, меню та полями замість команд: модулі, канали, ролі, порогові значення, тексти, префікс і мова. Вона також показує останні справи модерації, експортує та імпортує налаштування. Вона однаково працює на вашому комп'ютері та на VPS і вимкнена, доки ви її не ввімкнете.

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

## Усунення несправностей

- Слеш-команди не з'являються: зачекайте кілька хвилин, перезапустіть Discord і переконайтеся, що бота запрошено зі scope applications.commands.
- Бот зупиняється з помилкою привілейованих інтентів: увімкніть Server Members Intent і Message Content Intent у Developer Portal.
- Improper token: скопіюйте токен знову й переконайтеся, що в .env записано саме DISCORD_TOKEN=токен, без пробілів і лапок.
- I cannot assign that role: розмістіть роль бота вище за роль, якою він має керувати.
- Нічого не журналюється: задайте канал командою /log set і переконайтеся, що бот може в ньому надсилати повідомлення, вбудовувати посилання та прикріплювати файли.
- Unknown timezone: виконайте pip install tzdata і перезапустіть бота.
- Щось не працює без видимої причини: помилки та попередження виводяться в консоль. На VPS читайте їх командою journalctl -u guardbot -f.

## Підтримка

Помилки, ідеї та пропозиції: Discord @justyyin або issue на GitHub.

Copyright (c) Justyn - made in Germany
