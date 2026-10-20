# GuardBot: Руководство по установке

Это руководство показывает, как запустить GuardBot на своём компьютере или на VPS. Это займёт около 15 минут.

<!-- toc -->

- [Создание Discord-бота](#создание-discord-бота)
- [Запуск на своём компьютере](#запуск-на-своём-компьютере)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux и macOS](#linux-и-macos)
- [Запуск на VPS](#запуск-на-vps)
- [Запуск через Docker](#запуск-через-docker)
- [Первые шаги в Discord](#первые-шаги-в-discord)
- [Обновления и резервные копии](#обновления-и-резервные-копии)
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
sudo apt install -y python3 python3-venv python3-pip git
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
/log set category:main channel:#logs
/jailsetup setup
/automod toggle rule:phishing enabled:True action:jail
/automod toggle rule:words enabled:True
/automod add name:words value:example
/raid setup enabled:True joins:5 seconds:10 action:timeout min_age_days:3
/antinuke setup enabled:True action:strip
/verify setup channel:#verify mode:captcha timeout_minutes:30
/backup schedule enabled:True interval_hours:24 keep:7
/xp config enabled:True
/module list
```

Все функции описаны в справочнике команд: [COMMANDS.md](../COMMANDS.md).

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

## Устранение неполадок

- Слэш-команды не появляются: подождите несколько минут, перезапустите Discord и убедитесь, что бот приглашён со scope applications.commands.
- Бот останавливается с ошибкой привилегированных интентов: включите Server Members Intent и Message Content Intent в Developer Portal.
- Improper token: скопируйте токен заново и убедитесь, что в .env записано ровно DISCORD_TOKEN=токен, без пробелов и кавычек.
- I cannot assign that role: поместите роль бота выше роли, которой он должен управлять.
- Ничего не журналируется: задайте канал командой /log set и убедитесь, что бот может в нём отправлять сообщения, встраивать ссылки и прикреплять файлы.
- Unknown timezone: выполните pip install tzdata и перезапустите бота.
- Что-то не работает без видимой причины: ошибки и предупреждения выводятся в консоль. На VPS читайте их командой journalctl -u guardbot -f.

## Поддержка

Ошибки, идеи и предложения: Discord @justyyin или issue на GitHub.

Copyright (c) Justyn - made in Germany
