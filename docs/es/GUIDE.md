# GuardBot: Guía de instalación

Esta guía muestra cómo ejecutar GuardBot en tu ordenador o en un VPS. Lleva unos 15 minutos.

<!-- toc -->

- [Crear el bot de Discord](#crear-el-bot-de-discord)
- [Ejecutarlo en tu ordenador](#ejecutarlo-en-tu-ordenador)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux y macOS](#linux-y-macos)
- [Ejecutarlo en un VPS](#ejecutarlo-en-un-vps)
- [Ejecutarlo con Docker](#ejecutarlo-con-docker)
- [Primeros pasos en Discord](#primeros-pasos-en-discord)
- [Actualizaciones y copias de seguridad](#actualizaciones-y-copias-de-seguridad)
- [Solución de problemas](#solución-de-problemas)
- [Soporte](#soporte)

<!-- tocstop -->

## Crear el bot de Discord

1. Abre el [Discord Developer Portal](https://discord.com/developers/applications) y haz clic en New Application.
2. Abre la pestaña Bot y haz clic en Reset Token. Copia el token y mantenlo en secreto.
3. En la misma pestaña, activa Server Members Intent y Message Content Intent.
4. Abre OAuth2, URL Generator. Selecciona los scopes bot y applications.commands.
5. Selecciona los permisos: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, View Audit Log, Manage Messages, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Move Members. Administrator también funciona y es la opción más sencilla.
6. Abre la URL generada y añade el bot a tu servidor.
7. En los ajustes del servidor, mueve el rol del bot a lo más alto de la lista de roles. El bot solo puede gestionar roles que estén por debajo de su propio rol.

También puedes usar esta URL de invitación. Sustituye YOUR_CLIENT_ID por el Application ID del Developer Portal:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## Ejecutarlo en tu ordenador

Instala Python 3.11 o superior y Git, y ejecuta estos comandos en una terminal.

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

### Linux y macOS

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

Abre el archivo .env y sustituye el marcador por el token de tu bot. El bot está en línea cuando la consola muestra la línea que empieza por online as. Deja la ventana abierta, el bot se detiene al cerrarla.

## Ejecutarlo en un VPS

Estos comandos son para Ubuntu o Debian y configuran el bot como un servicio que arranca automáticamente.

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

Comprueba el estado con systemctl status guardbot. El registro muestra la línea que empieza por online as cuando el bot está listo.

## Ejecutarlo con Docker

Docker es opcional. Crea primero el archivo .env y luego ejecuta:

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## Primeros pasos en Discord

Usa estos comandos en tu servidor y sustituye los nombres de canal por los tuyos.

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

Todas las funciones se describen en la referencia de comandos: [COMMANDS.md](../COMMANDS.md).

## Actualizaciones y copias de seguridad

Actualizar el bot:

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

Guarda tus ajustes copiando la carpeta data, por ejemplo:

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## Solución de problemas

- Los comandos slash no aparecen: espera unos minutos, reinicia Discord y comprueba que el bot se invitó con el scope applications.commands.
- El bot se detiene con un error de intents privilegiados: activa Server Members Intent y Message Content Intent en el Developer Portal.
- Improper token: copia el token de nuevo y comprueba que .env contiene exactamente DISCORD_TOKEN=token, sin espacios ni comillas.
- I cannot assign that role: mueve el rol del bot por encima del rol que debe gestionar.
- No se registra nada: define un canal con /log set y comprueba que el bot puede enviar mensajes, insertar enlaces y adjuntar archivos allí.
- Unknown timezone: ejecuta pip install tzdata y reinicia el bot.
- Algo falla sin motivo visible: los errores y avisos se escriben en la consola. En un VPS léelos con journalctl -u guardbot -f.

## Soporte

Errores, ideas y sugerencias: Discord @justyyin o un issue de GitHub.

Copyright (c) Justyn - made in Germany
