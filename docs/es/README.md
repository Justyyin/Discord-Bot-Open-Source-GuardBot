# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | **Español** | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Bot de Discord autoalojado para moderación, seguridad y comunidad. Código abierto, gratuito, y tus datos se quedan en tu propio equipo.

> Beta: GuardBot y su panel de control están en fase beta. No se han probado a fondo, sobre todo no en servidores grandes ni ante todas las situaciones de Discord. Cuenta con errores, haz copias de la carpeta data e informa de los problemas. Uso bajo tu propia responsabilidad.

<!-- toc -->

- [Acerca del proyecto](#acerca-del-proyecto)
- [Funciones](#funciones)
  - [Seguridad](#seguridad)
  - [Moderación](#moderación)
  - [Registros](#registros)
  - [Comunidad](#comunidad)
  - [Administración](#administración)
- [Estado del proyecto](#estado-del-proyecto)
- [Requisitos](#requisitos)
- [Inicio rápido](#inicio-rápido)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Scripts de inicio y arranque automático](#scripts-de-inicio-y-arranque-automático)
  - [Actualizar](#actualizar)
- [Permisos del bot](#permisos-del-bot)
- [Primeros pasos en Discord](#primeros-pasos-en-discord)
  - [Estructura, miembros y equipo](#estructura-miembros-y-equipo)
- [Panel de control](#panel-de-control)
  - [Configurar el panel](#configurar-el-panel)
  - [Comandos, skills, IA y perfil del bot](#comandos-skills-ia-y-perfil-del-bot)
  - [Seguridad](#seguridad-1)
  - [Panel en un VPS](#panel-en-un-vps)
- [Comandos](#comandos)
  - [Grupos de comandos](#grupos-de-comandos)
  - [Moderación](#moderación-1)
  - [Gulag (jail)](#gulag-jail)
  - [Moderación automática](#moderación-automática)
  - [Protección anti-raid y bloqueo](#protección-anti-raid-y-bloqueo)
  - [Anti-nuke](#anti-nuke)
  - [Verificación](#verificación)
  - [Registros](#registros-1)
  - [Bienvenida, despedida y boosters](#bienvenida-despedida-y-boosters)
  - [Tickets](#tickets)
  - [Encuestas y sorteos](#encuestas-y-sorteos)
  - [Sugerencias y starboard](#sugerencias-y-starboard)
  - [XP y niveles](#xp-y-niveles)
  - [Roles por reacción y notificaciones](#roles-por-reacción-y-notificaciones)
  - [Cumpleaños](#cumpleaños)
  - [Canales de voz temporales](#canales-de-voz-temporales)
  - [Copia de seguridad y restauración](#copia-de-seguridad-y-restauración)
  - [Datos y privacidad](#datos-y-privacidad)
  - [Herramientas de moderación](#herramientas-de-moderación)
  - [Información](#información)
  - [Anuncios, etiquetas y recordatorios](#anuncios-etiquetas-y-recordatorios)
  - [Mod-mail y apelaciones de baneo](#mod-mail-y-apelaciones-de-baneo)
  - [Canal de conteo, mensajes fijos y estadísticas](#canal-de-conteo-mensajes-fijos-y-estadísticas)
  - [Más opciones de las funciones existentes](#más-opciones-de-las-funciones-existentes)
  - [Más herramientas de AutoMod](#más-herramientas-de-automod)
  - [Límites de moderadores y auditoría de permisos](#límites-de-moderadores-y-auditoría-de-permisos)
  - [Reportes y seguimiento de invitaciones](#reportes-y-seguimiento-de-invitaciones)
  - [Diagnóstico y depuración](#diagnóstico-y-depuración)
  - [Música](#música)
  - [Configuración y estado de salud](#configuración-y-estado-de-salud)
  - [Economía](#economía)
  - [Menús de roles, mensajes programados y feeds](#menús-de-roles-mensajes-programados-y-feeds)
  - [Actividad, acciones masivas y búsqueda de casos](#actividad-acciones-masivas-y-búsqueda-de-casos)
  - [Anti-estafa y anti-cripto](#anti-estafa-y-anti-cripto)
  - [Periodo de prueba, detección de enjambres, cronología y aprendizaje](#periodo-de-prueba-detección-de-enjambres-cronología-y-aprendizaje)
  - [Paneles](#paneles)
  - [Skills e IA](#skills-e-ia)
  - [Creador de mensajes y actualizaciones](#creador-de-mensajes-y-actualizaciones)
  - [Operación](#operación)
  - [Administración](#administración-1)
- [Marcadores en los mensajes](#marcadores-en-los-mensajes)
- [Configuración](#configuración)
- [Datos y almacenamiento](#datos-y-almacenamiento)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Traducciones](#traducciones)
- [Hoja de ruta](#hoja-de-ruta)
- [Privacidad y seguridad](#privacidad-y-seguridad)
- [Soporte](#soporte)
- [Créditos](#créditos)
- [Licencia](#licencia)

<!-- tocstop -->

## Acerca del proyecto

GuardBot reúne funciones por las que muchos servidores pagan con bots alojados: moderación, registros, anti-raid, anti-nuke, tickets, niveles y más. Lo ejecutas tú mismo, en tu ordenador o en un VPS pequeño.

Los bots alojados guardan datos del servidor, IDs de miembros y a veces correos electrónicos en manos de un tercero. Si alojas el bot tú mismo, esos datos no salen de tu equipo. GuardBot quiere demostrar que cualquiera puede ejecutar un bot completo sin suscripción.

## Funciones

### Seguridad

- Moderación automática: filtro de palabras, filtro de mayúsculas, spam de menciones, enlaces de invitación, dominios de phishing, datos personales, doxxing y amenazas. Todas las listas se pueden editar.
- Anti-raid con detección de oleadas de entradas y bloqueo de todo el servidor.
- Anti-nuke: límites para eliminaciones y baneos masivos, respuesta automática y mensaje directo al dueño del servidor.
- Canal gulag: quienes publican enlaces o imágenes de estafa pasan a un único canal con instrucciones para proteger su cuenta. Los moderadores también pueden usar /moderation jail y /moderation unjail.
- Verificación con botón o captcha, con expulsión automática de quienes no se verifican a tiempo.
- El anti-nuke vigila también la concesión de permisos, los nuevos webhooks, los bots añadidos y los cambios de nombre del servidor.
- Anti-estafa: los sorteos falsos y las estafas cripto se eliminan en texto e imágenes en milisegundos, incluida la estafa de MrBeast con cualquier ortografía.

### Moderación

- Warn, mute, kick, ban y jail con un historial filtrable por mención, ID de usuario o tipo.
- Escalada automática, por ejemplo tres advertencias provocan un aislamiento temporal.
- Elige qué roles o usuarios pueden usar cada comando de moderación.

### Registros

- Mensajes enviados, editados y eliminados, incluidas imágenes, GIF y URL, con canales de registro separados.
- Cambios de roles, apodos, baneos, voz, canales y roles del servidor.

### Comunidad

- Mensajes de bienvenida y despedida, roles automáticos y recompensas para boosters.
- Tickets, encuestas, sorteos y sugerencias.
- Roles por reacción con cualquier emoji y temas de notificación que los miembros activan o desactivan.
- XP y niveles del 1 al 100 para chat y voz, roles por nivel y cumpleaños.
- Starboard y canales de voz temporales.
- Jail con duración, encuestas de opción múltiple, tarjetas de rango como imagen y bonificaciones de XP por rol.
- Economía con tienda, menús de roles con botones o menú desplegable, mensajes programados, feeds de YouTube, Twitch y RSS, estadísticas de actividad y un /admin setup guiado. Los mensajes a los miembros están disponibles en 12 idiomas.

### Administración

- Cada módulo y cada comando se puede activar o desactivar por servidor.
- Prefijo propio, alias de comandos y comandos renombrables.
- Copia de seguridad y restauración de roles y estructura de canales.
- Copias de seguridad automáticas programadas de roles, canales, emojis y webhooks, con un comando de restauración que solo añade lo que falta.
- Panel de control: cambia los ajustes de cada servidor en el navegador tras iniciar sesión con Discord, solo para miembros que administran el servidor y solo mientras el bot esté conectado.
- Skills: comandos, juegos y automatizaciones propios a partir de bloques seguros, escritos opcionalmente por una IA con tu propia clave (Anthropic, OpenAI, Kimi). El panel muestra todos los comandos y edita skills, ajustes de IA y el perfil del bot.

## Estado del proyecto

GuardBot es joven y todavía no se ha usado en servidores grandes. Las pruebas automáticas (`python -m unittest`) cubren el almacenamiento, la detección de datos personales, el cálculo de niveles, el registro de comandos, las comprobaciones de permisos y los enlaces de la documentación. Todo lo que necesita un servidor de Discord real, como el bloqueo, la restauración de copias, la verificación, el anti-nuke y el gulag, no está cubierto. Prueba estas funciones primero en un servidor de pruebas antes de depender de ellas. Las traducciones de la documentación no han sido revisadas por hablantes nativos, se agradecen las correcciones.

## Requisitos

- Python 3.11 o superior
- Una aplicación de Discord con token de bot
- Un ordenador o VPS que permanezca en línea
- ffmpeg (solo para el módulo de música)
- tesseract-ocr (opcional, solo para leer texto en imágenes)

## Inicio rápido

Elige tu sistema. Cada variante necesita Python 3.11 o superior y el token de tu bot. La guía detallada paso a paso está en [GUIDE.md](GUIDE.md).

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

### Scripts de inicio y arranque automático

Los scripts de inicio crean el entorno virtual, instalan los paquetes y arrancan el bot. En la primera ejecución crean el archivo .env y se detienen para que introduzcas el token. Vuelve a ejecutarlos después.

```bash
./start.sh
```

```bat
start.bat
```

Para que el bot siga funcionando tras reiniciar el equipo, usa un servicio. Linux (systemd) y macOS (launchd):

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

En Windows, crea una tarea en el Programador de tareas que ejecute start.bat al iniciar sesión, o usa un envoltorio de servicio como NSSM. Para Docker, consulta [GUIDE.md](GUIDE.md).

### Actualizar

Detén el bot, ejecuta estos comandos y vuelve a iniciarlo. Tus datos de la carpeta data no se tocan, y el bot hace una copia de la base de datos antes de cada cambio de formato.

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

## Permisos del bot

Lo más sencillo es el permiso de Administrador. Si prefieres derechos mínimos, concede estos y activa los intents Server Members y Message Content en el Developer Portal:

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

## Primeros pasos en Discord

Una configuración inicial razonable. Ejecuta estos comandos en tu servidor y sustituye los canales y roles por los tuyos:

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

### Estructura, miembros y equipo

La versión 1.5 añade comandos para montar y mantener ordenado un servidor, restaurar a los miembros que vuelven y dirigir al equipo de moderación. Cada parte tiene un interruptor de módulo (`/admin module`), ajustes propios y un lugar en el panel.

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

- Con `/structure` se crean, clonan, renombran y ordenan canales y categorías y se copian los permisos de otro canal. Los canales inactivos se informan o se mueven a una categoría de archivo (`/structure archive`). Los roles pueden darse por tiempo limitado y guardarse como plantillas; una plantilla nunca concede un permiso que la persona que la aplica no tenga.
- `/structure rules` publica las reglas con un botón de aceptar y un número de versión. Tras `post new_version:True`, los miembros que no aceptaron la nueva versión reciben un único recordatorio por mensaje directo.
- `/members stickyroles` devuelve los roles y restaura un timeout o un mute cuando un miembro vuelve. `/members nickname` quita caracteres que suben al principio de la lista, comprueba palabras prohibidas en apodos y nombres de usuario y renombra a los infractores. La lista de vigilancia es silenciosa: el equipo recibe un aviso con el primer mensaje de un usuario de la lista.
- La aprobación de cuatro ojos (`/security approval`) solo ejecuta bans, kicks, timeouts y acciones masivas cuando un segundo moderador está de acuerdo. `/moderation case undo` revierte un caso, incluidas las acciones que provocó (por ejemplo un mute y el ban posterior). Las advertencias pueden caducar tras un número de días (`/moderation escalation expiry`).
- `/admin history` muestra quién cambió qué ajuste y cuándo, y restaura una sección. El nombre de la persona es una suposición a partir de los últimos comandos y cambios del panel en el servidor. `/admin history copy` copia secciones a otro servidor que puedas administrar con el bot; empieza como simulación. `/admin exceptions` deja canales y roles fuera de las reglas de AutoMod y del Anti-Scam. `/admin dashaccess` da a los roles acceso de solo lectura o de moderador al panel.
- `/team` muestra el trabajo de cada moderador (casos, tickets, reportes, tiempo de respuesta, miembros inactivos), publica un informe semanal (día y hora en UTC), permite a los moderadores ausentarse con `/team duty away` para que tickets y menciones vayan a otros, y gestiona solicitudes de staff con formulario y votación del equipo.
- Discord no puede ocultar los comandos de un grupo a ciertos miembros. El bot comprueba igualmente cada llamada. Las cifras de las estadísticas del equipo se cuentan desde el día de la actualización; las acciones anteriores no aparecen.

## Panel de control

El panel de control es una página web que se ejecuta dentro del bot. Tras iniciar sesión con Discord, cambias los ajustes de tus servidores con interruptores, menús y campos en lugar de comandos: módulos, canales, roles, umbrales, textos, el prefijo y el idioma. También muestra los últimos casos de moderación y exporta e importa ajustes. Funciona igual en tu propio equipo y en un VPS, y está desactivado hasta que lo actives.

### Configurar el panel

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

### Comandos, skills, IA y perfil del bot

El panel tiene cinco páginas más: Panels (ver la sección Paneles) y las cuatro siguientes. Comandos enumera cada comando slash, comando con prefijo y menú contextual con su módulo, el permiso necesario y su estado; los administradores los activan o desactivan, permiten o deniegan roles y dan nombres cortos a los comandos con prefijo. El prefijo se cambia en la misma página. Skills muestra todas las skills y las edita como JSON con las mismas comprobaciones que los comandos. IA ajusta el modelo y los límites y guarda una clave (solo escritura, nunca se devuelve a la página). Perfil del bot cambia el nombre, la imagen, el banner y el texto de presentación del bot en este servidor; el propietario de la aplicación del bot, o un ID incluido en `owner_ids` de settings.json, también puede cambiarlos en todas partes. Discord limita la frecuencia con la que se pueden cambiar el nombre y la imagen. Cada cambio queda en el registro de auditoría.

Cada módulo aparece como un plugin: la página Plugins los muestra como tarjetas por categoría, y cada plugin tiene su propia página con el interruptor Activo, sus ajustes en cuadros que se abren y cierran, y sus comandos con interruptor y editor de roles. La barra izquierda lista los plugins por categoría con un punto que indica si están activados. El panel usa un diseño oscuro.

El panel se puede mostrar en los 12 idiomas del bot. Elige el idioma arriba a la derecha o en la página de inicio de sesión; la elección se guarda en el navegador y no cambia el idioma del servidor. Los textos del panel están traducidos automáticamente.

Cada página de plugin explica qué hace el plugin, enumera todas sus funciones con su propio interruptor y una breve explicación, y deja los demás ajustes en cuadros debajo. En la página Plugins y en el resumen, cada plugin se puede activar o desactivar directamente. En Ajustes, el cuadro Apariencia del panel cambia el color de acento, el fondo, los cuadros y el texto, pone un fondo de pantalla (oscurecido y desenfocado a tu gusto) y añade menús y pestañas propias a la barra lateral: una pestaña puede reunir plugins elegidos, abrir una página, enlazar a una dirección https o mostrar una nota. La apariencia se guarda por servidor y la ven todos los que abren su panel. El pie de página muestra el copyright y enlaces a Discord y GitHub; para mostrar allí los logotipos oficiales, coloca discord.svg y github.svg de las páginas de marca de Discord y GitHub en guardbot/web/brand/.

### Seguridad

- Inicio de sesión solo con Discord (OAuth2, ámbito identify). El token de acceso se revoca al instante y nunca se guarda.
- Solo el propietario de un servidor y los miembros con el permiso Administrador o Administrar servidor tienen acceso, y solo a ese servidor. El permiso se vuelve a comprobar en cada petición.
- Solo se pueden abrir servidores a los que el bot está conectado en ese momento. Si el bot está sin conexión, no está en el servidor o aún está arrancando, el panel rechaza todo. Se ejecuta dentro del bot y no tiene base de datos ni servicio propios.
- Por defecto solo escucha en 127.0.0.1, así que nadie más en la red puede acceder. Una dirección pública solo se acepta con HTTPS; si no, el panel no arranca.
- Las sesiones usan un token aleatorio en una cookie HttpOnly con SameSite y, bajo HTTPS, el prefijo __Host-. Caducan a las 8 horas y solo viven en memoria, así que un reinicio cierra todas las sesiones.
- Cada cambio exige un token CSRF y un Origin válido. La cabecera Host se comprueba contra DNS rebinding. La página no carga scripts externos, una Content Security Policy estricta bloquea el código en línea, las peticiones tienen límite de frecuencia y el cuerpo está limitado a 256 KB.
- Cada valor se comprueba según el tipo del ajuste y los ID de Discord deben existir en el servidor. El estado interno, como contadores, tickets y elementos guardados, no se puede editar. Cada cambio se escribe en el canal de registro de seguridad del servidor.
- El contenido de los mensajes nunca se muestra. Los casos de moderación son de solo lectura.

### Panel en un VPS

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

El editor muestra cada ajuste que sea un interruptor, un número, un texto, un canal, un rol o una lista simple. Lo que se crea con comandos, como artículos de tienda, menús de roles, feeds, tags y tickets, sigue siendo cosa de comandos. La página está en inglés y alemán y sigue el idioma del navegador. En Docker, publica el puerto solo en 127.0.0.1 (127.0.0.1:8080:8080) y pon en el contenedor host en 0.0.0.0 y allow_insecure_http en true.

## Comandos

La mayoría de los comandos son comandos slash, los de moderación también funcionan con prefijo. La lista completa está en la referencia de comandos: [COMMANDS.md](../COMMANDS.md).

<!-- groups -->
### Grupos de comandos

Para ahorrar espacios de comandos slash (Discord permite 100 comandos de primer nivel por bot), los comandos relacionados están agrupados. Escribe primero el grupo y luego el comando, por ejemplo `/moderation ban`. Los comandos de texto con prefijo, por ejemplo `!ban`, no cambian. Los permisos, alias e interruptores de módulo siguen usando el nombre simple del comando.

| Grupo | Contiene |
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

### Moderación

Advertencias, silencios, expulsiones y baneos funcionan como comandos slash y con prefijo, por ejemplo `!warn @User spam`. Cada acción crea un caso con número.

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

### Gulag (jail)

Los miembros con la cuenta hackeada pasan a un único canal con instrucciones de seguridad. Al liberarlos recuperan sus roles.

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

Toda persona que entra en el gulag, por comando, por el AutoMod, por el anti-scam, al volver a unirse o porque alguien le dio el rol a mano, recibe el aviso Account Security Required con una mención. Mientras haya alguien en el gulag, un Account Recovery Reminder se queda al final del canal y se renueva cada 10 minutos. Un miembro del gulag que escribe el prefijo y la palabra de liberación (por ejemplo `!unban`) en el canal del gulag crea una solicitud de liberación con los botones Release y Keep para el equipo; el bot nunca libera a nadie por sí solo. `/access jailsetup reminder` activa o desactiva cada parte y fija el intervalo y la palabra.

### Moderación automática

Las reglas borran o sancionan los mensajes que coinciden. Elige la acción por regla: log, delete, warn, timeout o jail.

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

### Protección anti-raid y bloqueo

Detecta muchas entradas en poco tiempo y puede bloquear el servidor. El modo channels cambia cada canal, el modo role es inmediato.

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

### Anti-nuke

Vigila el registro de auditoría y reacciona cuando alguien destruye el servidor. El dueño recibe un mensaje directo.

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

### Verificación

Los miembros nuevos solo ven el canal de verificación hasta que pulsan el botón o resuelven el captcha.

```
/access verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/access verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/access verify panel channel:#verify                      # post the button again
/access verify apply                                      # apply the channel permissions again
/access verify member member:@User                        # verify someone manually
/access verify off
```

### Registros

Elige un canal por categoría, o un canal principal para todo.

```
/server log set category:main channel:#logs               # fallback for every category
/server log set category:messages channel:#log-messages
/server log set category:moderation channel:#log-moderation
/server log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/server log sent enabled:False                            # stop logging every sent message
/server log show
```

### Bienvenida, despedida y boosters

Mensajes, roles automáticos y recompensas para los boosters del servidor.

```
/community welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/community welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/community welcome autorole role:@Member                     # toggle, given to every new member
/community welcome botrole role:@Bots                        # toggle, given to every new bot
/community welcome test

/community booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/community booster role role:@Booster                        # toggle
```

### Tickets

Los miembros abren canales privados con un botón. Al cerrar se envía una transcripción.

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

### Encuestas y sorteos

Botones para votar y participar. Las duraciones aceptan valores como 30m, 2h y 1d.

```
/engage poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/engage poll end poll_id:3
/engage poll list

/engage giveaway start prize:Nitro duration:2d winners:2 role:@Member
/engage giveaway end giveaway_id:1
/engage giveaway reroll giveaway_id:1
/engage giveaway list
```

### Sugerencias y starboard

Los miembros publican sugerencias que el equipo puede aprobar o rechazar, y los mensajes populares se destacan.

```
/suggestion setup set channel:#suggestions review_role:@Staff
/support suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/engage starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/engage starboard ignore channel:#spam
```

### XP y niveles

XP por chat y voz, roles por nivel, bonificaciones por rol y tarjetas de rango.

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

### Roles por reacción y notificaciones

Da roles con cualquier emoji y deja que los miembros elijan sus temas de notificación.

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

### Cumpleaños

Los miembros guardan día y mes, el bot da un rol y publica un mensaje ese día.

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Canales de voz temporales

Al entrar en el canal hub se crea una sala que desaparece cuando queda vacía.

```
/community tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Copia de seguridad y restauración

Las copias incluyen roles, canales, emojis, webhooks y roles de los miembros. La restauración solo añade lo que falta.

```
/server backup create name:before-update
/server backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/server backup list
/server backup download name:before-update
/server backup restore name:before-update member_roles:True   # only adds what is missing
/server backup delete name:before-update
```

### Datos y privacidad

Los miembros pueden exportar y borrar sus datos. Los administradores controlan cuánto tiempo se conservan.

```
/info mydata export                                     # members download their own data
/info mydata delete confirm:True                        # members delete their XP and birthday

/server privacy retention days:90                         # delete data of members who left after 90 days
/server privacy export user_id:123456789012345678
/server privacy delete user_id:123456789012345678 cases:True
```

### Herramientas de moderación

Limpiar canales, gestionar roles y guardar notas privadas. Cada acción queda registrada.

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

### Información

Consultar usuarios, el servidor, los roles y el bot.

```
/info userinfo user:@User
/server serverinfo
/server roleinfo role:@Moderator
/info avatar user:@User
/help command:ban                                  # explains one command
/info ping
/info botinfo
```

### Anuncios, etiquetas y recordatorios

Escribir en nombre del bot, crear comandos propios, responder mensajes automáticamente y crear recordatorios.

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

### Mod-mail y apelaciones de baneo

Los miembros escriben al equipo mediante un canal privado del servidor. Nadie tiene que enviar un mensaje directo al bot.

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

### Canal de conteo, mensajes fijos y estadísticas

Un juego de conteo, mensajes que se quedan al final de un canal y canales que muestran cifras en directo.

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

### Más opciones de las funciones existentes

Ampliaciones de tickets, sorteos, salas de voz, XP, cumpleaños, copias de seguridad, registros y vistas de estado.

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

### Más herramientas de AutoMod

Seguir enlaces acortados, limitar los enlaces de los miembros nuevos, detectar ghost pings y probar reglas sin castigar a nadie.

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

### Límites de moderadores y auditoría de permisos

Recibir una alarma cuando un moderador banea o expulsa demasiado y ver qué roles tienen permisos peligrosos.

```
/team modwatch status
/team modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/team modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/team modwatch exclude member:@TrustedMod

/team permaudit run                                                  # roles with dangerous permissions and who holds them
/team permaudit watch enabled:True                                   # alarm when a role or member gets one
/team permaudit trust role:@Admin
```

### Reportes y seguimiento de invitaciones

Los miembros reportan mensajes al equipo y el bot registra qué invitación trajo a cada miembro nuevo.

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

### Diagnóstico y depuración

Encontrar permisos que faltan y ajustes rotos, recibir informes de error en un canal y exportar o importar los ajustes.

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

### Música

Reproduce enlaces y archivos de la carpeta music en un canal de voz. Las descargas se guardan como music/Artista/Álbum/Pista. Necesita ffmpeg y los paquetes de requirements.txt.

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

Sin pérdida: tus propios archivos (FLAC, WAV, ALAC) y las fuentes que ofrecen FLAC se reproducen sin cambios. YouTube, SoundCloud y sitios similares solo ofrecen audio con pérdida, y eso no se puede convertir después en sin pérdida. Discord transmite la voz como Opus; el bot usa la tasa de bits del canal de voz. Responsabilidad: descargar y reproducir contenido puede infringir las condiciones de un sitio o los derechos de autor. Las descargas están desactivadas por defecto y el módulo está desactivado hasta que lo actives. Quien opera el bot es responsable de lo que se reproduce y se guarda.

Fuentes: los enlaces y búsquedas de YouTube y SoundCloud se reproducen directamente. También se aceptan enlaces de Spotify, Apple Music y Tidal, pero estos servicios no entregan su audio: el bot lee el título y el artista de la página pública y reproduce la misma canción desde la fuente de búsqueda (YouTube o SoundCloud, se ajusta con /music sources). Los álbumes y listas de Spotify y Apple Music se leen de sus páginas públicas; los álbumes y listas de Tidal necesitan una clave de desarrollador gratuita de developer.tidal.com en .env (TIDAL_CLIENT_ID y TIDAL_CLIENT_SECRET). Los archivos de tu carpeta de música se reproducen tal cual. Las listas guardadas pueden mezclar todas las fuentes, y /music stay mantiene el bot en un canal de voz las 24 horas y reproduce una lista en bucle, también tras un reinicio.

Guard Music, el segundo bot: la música puede funcionar con su propia cuenta de bot, así puede quedarse siempre en un canal de voz sin afectar a la moderación.

1. Crea una segunda aplicación en el Discord Developer Portal, llámala Guard Music y copia el token de su bot.
2. Escribe el token en .env como MUSIC_TOKEN y pon music_bot.enabled en true en settings.json.
3. Reinicia GuardBot. Guard Music arranca en el mismo proceso, usa los mismos ajustes y datos, y los comandos de música pasan a él.
4. Abre la página Música del panel y añade Guard Music al servidor con el botón que aparece allí. Sin MUSIC_TOKEN la música se queda en GuardBot.

Uso bajo tu propio riesgo: transmitir desde YouTube y otros servicios puede incumplir sus condiciones de uso, y lo que se reproduce está sujeto a derechos de autor. No se descarga nada de Spotify, Apple Music ni Tidal y no se elude ninguna protección. El operador del bot es responsable de lo que se reproduce. La página Música del panel muestra el reproductor, la cola, las listas, el modo 24/7, las fuentes y esta guía.

### Configuración y estado de salud

Un asistente guiado configura lo más importante con botones y menús: canal de registros, canal de bienvenida, roles del equipo, el gulag, un ajuste preestablecido de AutoMod (suave, normal, estricto), una plantilla de servidor (comunidad, juegos, soporte) y el idioma. /server health muestra lo que está configurado y lo que falta. El idioma cambia los textos que ven los miembros, como los mensajes de bienvenida por defecto, los avisos de AutoMod, la verificación, los tickets, las apelaciones, el mod-mail y los menús de roles. Las respuestas fijas a los administradores están traducidas, las que llevan nombres y números siguen en inglés.

```
/admin setup                                                         # buttons and menus, nothing is switched off by a template
/server health                                                        # what is set up, what is open, and the self-test
/admin language code:de
```

### Economía

Una moneda del servidor con recompensa diaria, trabajo, pagos, clasificación y una tienda cuyos artículos pueden dar un rol. Actívala con el módulo economy. Los comandos también funcionan con el prefijo, por ejemplo !economy daily.

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

### Menús de roles, mensajes programados y feeds

Los menús de roles dan roles con botones o un menú desplegable. Los mensajes programados se publican una vez o se repiten cada hora, día o semana. Los feeds publican vídeos nuevos de YouTube, directos de Twitch y elementos RSS. Para YouTube usa el ID del canal (empieza por UC). Twitch necesita TWITCH_CLIENT_ID y TWITCH_CLIENT_SECRET en el archivo .env. Las horas se escriben como in 2h, 18:30 o como fecha con hora, por ejemplo 2026-12-24 18:00, en la zona horaria del servidor. La primera comprobación de un feed solo recuerda lo que ya existe.

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

### Actividad, acciones masivas y búsqueda de casos

La actividad cuenta mensajes por canal y entradas y salidas por día, nunca contenido ni nombres. Las acciones masivas banean, expulsan o aíslan hasta 25 usuarios tras una confirmación. Los casos se buscan por usuario, tipo, nombre, motivo, moderador y antigüedad, y se pueden enlazar entre sí, por ejemplo una nota con un baneo.

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

### Anti-estafa y anti-cripto

Elimina sorteos falsos, como la típica estafa de MrBeast, en texto e imágenes en milisegundos. Los nombres de la lista inmediata se eliminan al instante con cualquier ortografía (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Si no, las palabras de las listas (nombres, cebos, cripto, enlaces, importes) se suman y el mensaje se elimina al llegar al umbral. Las imágenes se leen con OCR, y una imagen ya juzgada como estafa se elimina sin volver a leerla. Leer imágenes necesita tesseract; sin él solo se revisa el texto. Un servidor sobre MrBeast puede quitar el nombre de la lista inmediata o excluir canales con /automod exemptchannel. Pruébalo con /security antiscam test antes de fiarte de él.

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

### Periodo de prueba, detección de enjambres, cronología y aprendizaje

El periodo de prueba pone a los miembros nuevos en un rol. Hasta que escriban el número de mensajes normales indicado o pasen los minutos, los enlaces, invitaciones y archivos se eliminan con un aviso breve. La protección contra raids también reconoce un enjambre: varias cuentas nuevas con el mismo patrón de nombre, la misma foto de perfil o creadas con minutos de diferencia. La cronología (/moderation case timeline) reúne en orden temporal la creación de la cuenta, la entrada y la invitación, el periodo de prueba, los casos y las apelaciones de un usuario. Los mensajes nunca se guardan, así que no forman parte de ella. /security block, /security unblock y /security blocklist gestionan la lista de bloqueo de AutoMod con comandos cortos. Los moderadores enseñan al módulo anti-estafa con la entrada de menú contextual Mark as scam en un mensaje o con una reacción con el emoji de learn_emoji: el mensaje se elimina y sus imágenes y su texto se eliminan al instante a partir de entonces. Cada parte se desactiva con su módulo o sus ajustes.

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

### Paneles

Los paneles son publicaciones como un mensaje de bienvenida, reglas, una elección de rol, botones de notificaciones o una verificación, con imágenes de banner, cuadros de texto y botones. Se crean con `/panel` o en el panel web, página Panels. Las imágenes se suben allí o como opciones del comando, y el bot las guarda en `data/panels` para que sigan funcionando.

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

Plantillas: empty, welcome, rules, roles, notifications y verify; sus textos están en el idioma del servidor y se pueden cambiar. `/panel section` abre un formulario para título, texto y pie. Cada sección se convierte en un mensaje: el banner encima del cuadro, la imagen grande dentro y la imagen pequeña arriba a la derecha. Los botones van bajo la última sección, cinco por fila. Un botón de rol da el rol o lo quita; con `single`, se quitan los demás roles del panel. El botón verify inicia la verificación del módulo de verificación (`/access verify setup` decide entre botón, captcha y cálculo). Los textos pueden usar `{server}` y `{count}`. `/panel update` cambia los mensajes publicados tras una edición. Límites por servidor: 25 paneles, 5 secciones y 20 botones por panel, 40 imágenes de hasta 8 MB. El bot solo ofrece roles que están por debajo de su rol más alto y no tienen permisos peligrosos.

### Skills e IA

Las skills son comandos, juegos y automatizaciones que un servidor construye por sí mismo con bloques seguros. No necesitan IA y nunca pueden ejecutar código. Una IA es opcional: con tu propia clave escribe una skill a partir de una descripción y da una segunda opinión en la comprobación anti-scam.

Skills sin IA:

- `/support skill create kind:command name:hello` abre un cuadro con un pequeño ejemplo que puedes cambiar. `/support skill edit`, `show`, `import`, `enable`, `disable`, `delete`, `list` y `stats` las gestionan. Todos usan una skill con `/support skill run` o con el prefijo, por ejemplo `!hello`. `/support skill panel` publica botones que ejecutan skills.
- Tipos: comando (una lista de acciones), juego (dado, elección, tragaperras, piedra papel tijera, quiz) y automatización (empieza cuando un miembro entra o sale, cuando un mensaje contiene palabras o cuando se pulsa un botón).
- Acciones: responder, enviar a un canal, mensaje directo, registro, añadir o quitar un rol, cambiar un contador, dar monedas, elegir al azar. Una acción puede tener condiciones: tiene un rol, probabilidad, un contador comparado con un número.
- Los textos pueden usar `{user}`, `{user_name}`, `{server}`, `{channel}`, `{count}`, `{arg1}`, `{arg2}`, `{var:name}`, `{uvar:name}` y `{random:1-6}`.
- Límites: 50 skills por servidor, 10 acciones por skill, 3 cambios de rol y 4 mensajes por skill. El bot solo da roles que estén por debajo de su propio rol más alto y no tengan permisos peligrosos. Una skill que da monedas necesita un enfriamiento de al menos 60 segundos. No se pueden usar nombres de comandos del bot, alias ni etiquetas.
- Las skills se guardan como JSON y forman parte de la exportación de ajustes. Los campos desconocidos se rechazan, así que una skill de cualquier origen solo puede hacer lo que permiten los bloques.

Ejemplo, un comando que da un rol y cuenta los usos (sustituye el ID del rol):

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

Conexión con una IA (opcional):

- `/support ai setup provider:kimi agree:true` abre un cuadro privado para tu clave de API. Los proveedores son Anthropic, OpenAI y Kimi (Moonshot). Se sugiere un modelo que puedes cambiar en el mismo comando o en el panel; los nombres de modelos cambian en los proveedores, así que consulta su documentación. Tú pagas a tu proveedor.
- `/support ai make wish:...` pide una skill a la IA, comprueba la respuesta con tanto rigor como una skill importada y muestra una vista previa. No se guarda nada hasta que pulses Guardar.
- `/support ai status`, `limits` (solicitudes por día, segundos entre solicitudes por persona) y `remove` completan el conjunto. La clave se guarda cifrada y el secreto está en el archivo `data/ai.secret`. Guarda ese archivo con tus copias de seguridad; sin él, una clave guardada no se puede leer y hay que introducirla de nuevo. La clave nunca se muestra, se registra ni se exporta. El proveedor solo cambia junto con una clave nueva, así que una clave nunca va a otro proveedor.
- Qué se envía: el deseo de `/support ai make` y, con la segunda opinión, el texto de un mensaje sospechoso. Nada más, y solo mientras el módulo `ai` esté activado. Consulta [PRIVACY.md](../PRIVACY.md).

Aprendizaje del anti-scam:

- El filtro aprendido (`/security antiscam set learned:true`) es un pequeño clasificador por servidor. Los moderadores lo entrenan con las entradas del menú contextual «Mark as scam» y «Not a scam». Solo guarda hashes cortos de palabras, nunca el texto, actúa únicamente tras ver 8 ejemplos de scam y 30 normales, y entonces solo por encima del 95 por ciento. Con `ham_sampling` también aprende de uno de cada diez mensajes normales.
- Las imágenes similares (`similar`, activado por defecto) comparan una huella de imagen con imágenes de scam conocidas, de modo que se encuentra también una copia guardada de nuevo o redimensionada. Funciona sin Tesseract.
- Segunda opinión de la IA (`/support ai limits second_opinion:true`): en casos justo por debajo del umbral o que el filtro aprendido considera sospechosos, se consulta a la IA. Un mensaje solo se elimina cuando la IA responde scam con al menos un 80 por ciento de confianza, y su respuesta no puede provocar nada más.

### Creador de mensajes y actualizaciones

El creador de mensajes publica mensajes con varios embeds y botones de enlace a partir de JSON. Lee el JSON que exportan los generadores de embeds como Embed Generator, así que diseñas un mensaje allí y lo publicas con el bot. Indica el JSON como texto, como archivo .json o como enlace https que apunte directamente al JSON, por ejemplo el archivo sin procesar de un repositorio (los enlaces con redirección se rechazan). Solo se crean botones de enlace, los botones que necesitan una interacción se omiten. Cada enlace debe ser http o https, las menciones del texto nunca avisan y se aplican los límites de Discord. /post message copy exporta un mensaje existente como JSON, /post message edit cambia un mensaje del bot y /post message preview muestra el resultado solo a ti. Los enlaces para compartir de editores web no se abren, porque su formato no es público.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Cada 12 horas el bot comprueba si el repositorio de GitHub indicado en update.repo (definido con scripts/set_repo_url.py) tiene una versión más reciente. Si la hay, el propietario del bot recibe un mensaje directo con las notas de la versión, y la versión se descarga y se comprueba: suma SHA-256 de la versión, rutas seguras dentro del archivo y una versión que coincide con la etiqueta. Se instala con /server debug update action:install, o sola si auto_install está activado. Antes de instalar, los archivos reemplazados se guardan en data/update, se instalan los paquetes nuevos y el código nuevo se importa de prueba. Si algo falla, se restauran los archivos antiguos. Tu .env, settings.json, data y music nunca se tocan. Después el bot se reinicia solo. En Docker no se instala nada en el sitio, actualiza la imagen. Una actualización ejecuta código del repositorio, así que apúntala solo a un repositorio de confianza. Desactívala con enabled en false.

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

### Operación

El bot guarda sus datos cada pocos segundos y conserva copias de la base de datos en data/dbbackups, una antes de cada cambio del formato de datos y una al día. La cola de música, los mensajes fijos y los contadores de moderadores sobreviven a un reinicio. Los bots grandes pueden funcionar con varios shards. Un archivo heartbeat y una página de estado opcional ayudan a las herramientas de monitorización. Estas opciones se configuran en settings.json:

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

Los registros se escriben en data/guardbot.log (con rotación, ver log_max_mb y log_backups). Con log_format en json se genera un objeto JSON por línea con el servidor y el comando. Si health_port está definido, /metrics ofrece métricas de Prometheus (tiempo activo, latencia, memoria, tamaño de la base de datos, errores, uso y duración de comandos, carriles de trabajo). Solo se exportan números, nunca nombres ni ID, y metrics_token exige un token bearer. El trabajo pesado (leer imágenes, dibujar tarjetas, archivos de música, copias de seguridad) se ejecuta en carriles con un número fijo de hilos y un límite (workers en settings.json). Cuando un carril está lleno, el bot avisa de que está ocupado en lugar de acumular trabajo. Cada copia de la base de datos se abre y se comprueba justo después de crearla. Para restaurar una, detén el bot y ejecuta:

```
python scripts/restore_db.py data/dbbackups/guardbot-YYYYMMDD-HHMMSS-auto.db
python scripts/restore_db.py BACKUPFILE --check          # only check a backup
```

La base de datos actual se conserva como copia llamada before-restore.

### Administración

Activar o desactivar módulos y comandos, cambiar el prefijo, definir alias y limitar comandos a roles.

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

## Marcadores en los mensajes

Estos marcadores se sustituyen en los textos que configures:

```
/community welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/community booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/community tempvoice setup     name                            {name}
/access jailsetup notice    text                            {staff}
```

## Configuración

Las opciones globales se establecen en settings.json. Todo lo demás se configura por servidor con comandos como /admin module, /admin command, /admin perms, /admin alias y /admin config.

Para renombrar un comando, añádelo en command_names y reinicia el bot:

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

Cada ajuste se puede leer y cambiar con /admin config. Estas son las rutas que más usarás:

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

## Datos y almacenamiento

Todo lo que guarda el bot está en tu propio equipo:

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

## Estructura del repositorio

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
    skills.py             motor de skills: comprueba y ejecuta skills
    ai.py                 proveedores de IA, claves cifradas, límites
    learner.py, imgsim.py filtro aprendido del anti-scam, huellas de imágenes
    dashboard_manage.py   páginas del panel para comandos, skills, IA y perfil
  docs/                   documentation in 12 languages, COMMANDS.md, PRIVACY.md
  deploy/                 systemd service, Dockerfile, compose file
  scripts/                maintenance scripts
  tests/                  automated tests (python -m unittest)
  data/                   created at runtime, holds your settings and data
```

## Traducciones

El inglés es el idioma original del proyecto. Todas las traducciones de la documentación, del panel y de los mensajes del bot se crearon con traducción automática y no han sido revisadas por hablantes nativos. Cuenta con expresiones torpes y errores, y por favor avísanos o envía una corrección. Los archivos están en docs/ y guardbot/locales/.

## Hoja de ruta

- Gráficos de actividad y moderación en el panel.
- Revisión de todas las traducciones por hablantes nativos.
- Más textos de respuesta fijos traducidos.

## Privacidad y seguridad

- Sin telemetría. El bot se comunica con Discord y, para comprobar actualizaciones, con GitHub (no se envían datos personales, desactívalo con update.enabled). Los enlaces que le dan los administradores, como feeds, música y enlaces JSON, solo se abren a petición.
- Todos los datos están en la carpeta data de tu equipo: ajustes, XP, cumpleaños (solo día y mes) y casos de moderación.
- El bot ignora los mensajes directos de los miembros.
- El token se lee del archivo .env. No lo compartas nunca ni lo subas.
- Los miembros pueden exportar y borrar sus propios datos con /info mydata. Los administradores definen cuánto tiempo se conservan los datos de quienes se fueron.
- Las funciones de IA están desactivadas hasta que añadas tu propia clave. Después solo se envían al proveedor elegido el texto de `/support ai make` y, con la segunda opinión, los mensajes sospechosos.
- [PRIVACY.md](../PRIVACY.md)

## Soporte

Errores, ideas y sugerencias: escríbeme en Discord, @justyyin, o abre un issue en GitHub.

## Créditos

GuardBot se inspira en [Embed Generator](https://github.com/merlinfuchs/embed-generator) de Merlin Fuchs (licencia MIT, alojado en message.style). El creador de mensajes lee el mismo formato JSON, así que los mensajes diseñados allí se pueden publicar con este bot. No se incluye código de ese proyecto. Gracias a los autores de discord.py, aiohttp, Pillow, yt-dlp, mutagen y Tesseract.

## Licencia

Publicado bajo la licencia MIT. Consulta [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
