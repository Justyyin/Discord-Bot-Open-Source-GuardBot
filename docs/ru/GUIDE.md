# GuardBot: Руководство по установке

Это руководство показывает, как запустить GuardBot на своём компьютере или на VPS. Это займёт около 15 минут.

> Бета: GuardBot и его панель управления находятся в стадии беты. Они не были тщательно протестированы, особенно на больших серверах и во всех ситуациях Discord. Возможны ошибки, делайте резервные копии папки data и сообщайте о проблемах. Использование на свой риск.

<!-- toc -->

- [Создание Discord-бота](#создание-discord-бота)
- [Запуск на своём компьютере](#запуск-на-своём-компьютере)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux и macOS](#linux-и-macos)
- [Запуск на VPS](#запуск-на-vps)
- [Запуск через Docker](#запуск-через-docker)
- [Первые шаги в Discord](#первые-шаги-в-discord)
- [Структура, команда и обзор (1.5)](#структура-команда-и-обзор-15)
- [Обновления и резервные копии](#обновления-и-резервные-копии)
- [Музыка (необязательно)](#музыка-необязательно)
- [Необязательно: чтение изображений и языки](#необязательно-чтение-изображений-и-языки)
- [Панель управления](#панель-управления)
- [Устранение неполадок](#устранение-неполадок)
- [Поддержка](#поддержка)

<!-- tocstop -->

## Создание Discord-бота

1. Откройте [Discord Developer Portal](https://discord.com/developers/applications) и нажмите New Application.
2. Откройте вкладку Bot и нажмите Reset Token. Скопируйте токен и держите его в секрете.
3. На той же вкладке включите Server Members Intent и Message Content Intent.
4. Откройте OAuth2, URL Generator. Выберите scopes bot и applications.commands.
5. Выберите права: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, View Audit Log, Manage Messages, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Move Members. Administrator тоже подходит и является самым простым вариантом.
6. Откройте созданную ссылку и добавьте бота на свой сервер.
7. В настройках сервера переместите роль бота в самый верх списка ролей. Бот может управлять только ролями, которые находятся ниже его собственной.

Либо используйте эту ссылку-приглашение. Замените YOUR_CLIENT_ID на Application ID из Developer Portal:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## Запуск на своём компьютере

Установите Python 3.11 или новее и Git, затем выполните эти команды в терминале.

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

### Linux и macOS

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

Откройте файл .env и замените образец токеном вашего бота. Бот будет в сети, как только в консоли появится строка, начинающаяся с online as. Не закрывайте окно: бот останавливается вместе с ним.

## Запуск на VPS

Эти команды подходят для Ubuntu и Debian и настраивают бота как службу с автозапуском.

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

Состояние проверяется командой systemctl status guardbot. Когда бот готов, в журнале появляется строка, начинающаяся с online as.

## Запуск через Docker

Docker необязателен. Сначала создайте файл .env, затем выполните:

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## Первые шаги в Discord

Используйте эти команды на своём сервере и замените названия каналов своими.

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

Все функции описаны в справочнике команд: [COMMANDS.md](../COMMANDS.md).

## Структура, команда и обзор (1.5)

Эти шаги настраивают новые функции. Каждую можно отключить через /admin module, а префикс и тексты остаются настраиваемыми для каждого сервера.

1. Посмотреть, что настроено: `/admin module overview` показывает каждый модуль с состоянием и статусом настройки. Панель управления показывает то же в разделе настройки.
2. Найти команду: `/info find text:ban` ищет по всем командам по слову, `/help` показывает группы.
3. Опубликовать правила с кнопкой принятия: `/structure rules setup`, затем `/structure rules add`, затем `/structure rules post`. Тем, кто не принял новую версию, напоминают каждые несколько часов.
4. Указать боту, кто входит в команду: `/team duty roster`. Это используют списки доступных сотрудников и маршрутизация тикетов и оповещений.
5. Навести порядок в неактивных каналах: `/structure archive setup`, затем `/structure archive scan`.
6. Возвращать роли вернувшимся участникам: `/members stickyroles setup`.
7. Следить за читаемостью имён: `/members nickname setup`, перед `/members nickname scan` проверьте через `/members nickname check`.
8. Перед крупными изменениями экспортируйте настройки через `/admin config export` и проверьте роли и каналы через `/server diagnose`.

## Обновления и резервные копии

Обновление бота:

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

Сохраните настройки, скопировав папку data, например:

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## Музыка (необязательно)

Для модуля музыки нужен ffmpeg на компьютере, где работает бот. Положите свою музыку в папку music/ как Исполнитель/Альбом/01 - Название.flac или разрешите загрузки. Папка может стать большой, поэтому держите её на диске с местом или в томе Docker.

```
# Windows
winget install Gyan.FFmpeg
# macOS
brew install ffmpeg
# Ubuntu or Debian
sudo apt install -y ffmpeg libopus0

# in Discord
/admin module enable name:music
/music settings allow_download:True
```

## Необязательно: чтение изображений и языки

Чтобы модуль защиты от мошенничества читал текст на изображениях, установите tesseract на компьютер, где работает бот (в образе Docker он уже есть). Затем проверьте командой /security antiscam status, что он готов. Язык сообщений, которые видят участники, выбирается командой /admin language.

```
# Ubuntu or Debian
sudo apt install -y tesseract-ocr
# macOS
brew install tesseract
# Windows
winget install UB-Mannheim.TesseractOCR

# in Discord
/security antiscam status
/admin language code:de
```

## Панель управления

Панель управления — это веб-страница, которая работает внутри бота. После входа через Discord вы меняете настройки своих серверов переключателями, меню и полями вместо команд: модули, каналы, роли, пороговые значения, тексты, префикс и язык. Она также показывает последние дела модерации, экспортирует и импортирует настройки. Она одинаково работает на вашем компьютере и на VPS и выключена, пока вы её не включите.

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

## Устранение неполадок

- Слэш-команды не появляются: подождите несколько минут, перезапустите Discord и убедитесь, что бот приглашён со scope applications.commands.
- Бот останавливается с ошибкой привилегированных интентов: включите Server Members Intent и Message Content Intent в Developer Portal.
- Improper token: скопируйте токен заново и убедитесь, что в .env записано ровно DISCORD_TOKEN=токен, без пробелов и кавычек.
- I cannot assign that role: поместите роль бота выше роли, которой он должен управлять.
- Ничего не журналируется: задайте канал командой /server log set и убедитесь, что бот может в нём отправлять сообщения, встраивать ссылки и прикреплять файлы.
- Unknown timezone: выполните pip install tzdata и перезапустите бота.
- Что-то не работает без видимой причины: ошибки и предупреждения выводятся в консоль. На VPS читайте их командой journalctl -u guardbot -f.

## Поддержка

Ошибки, идеи и предложения: Discord @justyyin или issue на GitHub.

Copyright (c) Justyn - made in Germany
