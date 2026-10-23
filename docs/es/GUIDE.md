# GuardBot: Guía de instalación

Esta guía muestra cómo ejecutar GuardBot en tu ordenador o en un VPS. Lleva unos 15 minutos.

> Beta: GuardBot y su panel de control están en fase beta. No se han probado a fondo, sobre todo no en servidores grandes ni ante todas las situaciones de Discord. Cuenta con errores, haz copias de la carpeta data e informa de los problemas. Uso bajo tu propia responsabilidad.

<!-- toc -->

- [Crear el bot de Discord](#crear-el-bot-de-discord)
- [Ejecutarlo en tu ordenador](#ejecutarlo-en-tu-ordenador)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux y macOS](#linux-y-macos)
- [Ejecutarlo en un VPS](#ejecutarlo-en-un-vps)
- [Ejecutarlo con Docker](#ejecutarlo-con-docker)
- [Primeros pasos en Discord](#primeros-pasos-en-discord)
- [Estructura, equipo y resumen (1.5)](#estructura-equipo-y-resumen-15)
- [Actualizaciones y copias de seguridad](#actualizaciones-y-copias-de-seguridad)
- [Música (opcional)](#música-opcional)
- [Opcional: leer imágenes e idiomas](#opcional-leer-imágenes-e-idiomas)
- [Panel de control](#panel-de-control)
- [Skills, IA y perfil del bot (opcional)](#skills-ia-y-perfil-del-bot-opcional)
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

Todas las funciones se describen en la referencia de comandos: [COMMANDS.md](../COMMANDS.md).

## Estructura, equipo y resumen (1.5)

Estos pasos configuran las funciones más nuevas. Cada una se puede desactivar con /admin module, y el prefijo y los textos siguen siendo editables por servidor.

1. Ver qué está configurado: `/admin module overview` lista cada módulo con su estado y si está configurado. El panel web muestra lo mismo en su panel de configuración.
2. Encontrar un comando: `/info find text:ban` busca en todos los comandos por palabra, `/help` muestra los grupos.
3. Publicar las reglas con botón de aceptar: `/structure rules setup`, luego `/structure rules add`, luego `/structure rules post`. A quien no haya aceptado una versión nueva se le recuerda cada pocas horas.
4. Decirle al bot quién es del equipo: `/team duty roster`. Las listas de personal disponible y el enrutamiento de tickets y avisos lo usan.
5. Ordenar canales inactivos: `/structure archive setup`, luego `/structure archive scan`.
6. Devolver sus roles a los miembros que vuelven: `/members stickyroles setup`.
7. Mantener los nombres legibles: `/members nickname setup`, prueba con `/members nickname check` antes de `/members nickname scan`.
8. Antes de cambios grandes, exporta los ajustes con `/admin config export` y revisa roles y canales con `/server diagnose`.

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

## Música (opcional)

El módulo de música necesita ffmpeg en el equipo que ejecuta el bot. Coloca tu música en la carpeta music/ como Artista/Álbum/01 - Título.flac, o permite las descargas. La carpeta puede crecer mucho: mantenla en un disco con espacio o en un volumen de Docker.

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

Guard Music: para que la música funcione en un bot propio que pueda quedarse las 24 horas en un canal de voz, crea una segunda aplicación en el Discord Developer Portal, escribe su token en .env como MUSIC_TOKEN y pon music_bot.enabled en true en settings.json. Tras un reinicio, la página Música del panel muestra un botón que añade Guard Music al servidor. Los enlaces de Spotify, Apple Music y Tidal se reproducen mediante YouTube o SoundCloud; los álbumes y listas de Tidal además necesitan TIDAL_CLIENT_ID y TIDAL_CLIENT_SECRET en .env. Uso bajo tu propio riesgo, consulta la sección Música del README.

## Opcional: leer imágenes e idiomas

Para que el módulo anti-estafa lea el texto de las imágenes, instala tesseract en el equipo que ejecuta el bot (la imagen de Docker ya lo incluye). Después comprueba con /security antiscam status que está listo. Elige el idioma de los mensajes que ven los miembros con /admin language.

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

## Panel de control

El panel de control es una página web que se ejecuta dentro del bot. Tras iniciar sesión con Discord, cambias los ajustes de tus servidores con interruptores, menús y campos en lugar de comandos: módulos, canales, roles, umbrales, textos, el prefijo y el idioma. También muestra los últimos casos de moderación y exporta e importa ajustes. Funciona igual en tu propio equipo y en un VPS, y está desactivado hasta que lo actives.

1. Abre tu aplicación en el Developer Portal, ve a OAuth2 y copia el Client Secret en el archivo .env.
2. En la misma página añade la dirección de redirección http://localhost:8080/callback.
3. Activa el panel en settings.json.
4. Reinicia el bot y abre http://localhost:8080 en el navegador. Inicia sesión con Discord.

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

Deja host en 127.0.0.1 y elige una de dos vías. Primero, un túnel SSH: no se expone nada y abres http://localhost:8080 en tu equipo mientras el túnel está activo.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Segundo, HTTPS mediante un proxy inverso como Caddy, que obtiene su propio certificado (consulta deploy/Caddyfile.example). Entonces pon public_url con tu dirección https, añade https://tu-direccion/callback como redirección en el Developer Portal y pon trust_proxy en true:

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

## Skills, IA y perfil del bot (opcional)

Las skills solo necesitan el bot: empieza con `/support skill create`. Para la IA necesitas una cuenta y una clave de API en Anthropic, OpenAI o Kimi (Moonshot); ejecuta `/support ai setup` y pega la clave en el cuadro privado. Guarda el archivo `data/ai.secret` junto con tus copias de seguridad. El nombre, la imagen y el banner del bot se cambian en el panel, en Perfil del bot; para cambiarlos en todas partes, añade tu ID de Discord como `owner_ids` en `settings.json` (o sé el propietario de la aplicación). Los detalles están en el README, sección Skills e IA.

## Solución de problemas

- Los comandos slash no aparecen: espera unos minutos, reinicia Discord y comprueba que el bot se invitó con el scope applications.commands.
- El bot se detiene con un error de intents privilegiados: activa Server Members Intent y Message Content Intent en el Developer Portal.
- Improper token: copia el token de nuevo y comprueba que .env contiene exactamente DISCORD_TOKEN=token, sin espacios ni comillas.
- I cannot assign that role: mueve el rol del bot por encima del rol que debe gestionar.
- No se registra nada: define un canal con /server log set y comprueba que el bot puede enviar mensajes, insertar enlaces y adjuntar archivos allí.
- Unknown timezone: ejecuta pip install tzdata y reinicia el bot.
- Algo falla sin motivo visible: los errores y avisos se escriben en la consola. En un VPS léelos con journalctl -u guardbot -f.

## Soporte

Errores, ideas y sugerencias: Discord @justyyin o un issue de GitHub.

Copyright (c) Justyn - made in Germany
