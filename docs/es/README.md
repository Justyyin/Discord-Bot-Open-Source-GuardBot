# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | **Español** | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Bot de Discord autoalojado para moderación, seguridad y comunidad. Código abierto, gratuito, y tus datos se quedan en tu propio equipo.

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
- [Permisos del bot](#permisos-del-bot)
- [Primeros pasos en Discord](#primeros-pasos-en-discord)
- [Comandos](#comandos)
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
  - [Administración](#administración-1)
- [Marcadores en los mensajes](#marcadores-en-los-mensajes)
- [Configuración](#configuración)
- [Datos y almacenamiento](#datos-y-almacenamiento)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Hoja de ruta](#hoja-de-ruta)
- [Privacidad y seguridad](#privacidad-y-seguridad)
- [Soporte](#soporte)
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
- Canal gulag: quienes publican enlaces o imágenes de estafa pasan a un único canal con instrucciones para proteger su cuenta. Los moderadores también pueden usar /jail y /unjail.
- Verificación con botón o captcha, con expulsión automática de quienes no se verifican a tiempo.
- El anti-nuke vigila también la concesión de permisos, los nuevos webhooks, los bots añadidos y los cambios de nombre del servidor.

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

### Administración

- Cada módulo y cada comando se puede activar o desactivar por servidor.
- Prefijo propio, alias de comandos y comandos renombrables.
- Copia de seguridad y restauración de roles y estructura de canales.
- Copias de seguridad automáticas programadas de roles, canales, emojis y webhooks, con un comando de restauración que solo añade lo que falta.

## Estado del proyecto

GuardBot es joven y todavía no se ha usado en servidores grandes. Las pruebas automáticas (`python -m unittest`) cubren el almacenamiento, la detección de datos personales, el cálculo de niveles, el registro de comandos, las comprobaciones de permisos y los enlaces de la documentación. Todo lo que necesita un servidor de Discord real, como el bloqueo, la restauración de copias, la verificación, el anti-nuke y el gulag, no está cubierto. Prueba estas funciones primero en un servidor de pruebas antes de depender de ellas. Las traducciones de la documentación no han sido revisadas por hablantes nativos, se agradecen las correcciones.

## Requisitos

- Python 3.11 o superior
- Una aplicación de Discord con token de bot
- Un ordenador o VPS que permanezca en línea

## Inicio rápido

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

La guía completa paso a paso está en [GUIDE.md](GUIDE.md).

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

## Comandos

La mayoría de los comandos son comandos slash, los de moderación también funcionan con prefijo. La lista completa está en la referencia de comandos: [COMMANDS.md](../COMMANDS.md).

### Moderación

Advertencias, silencios, expulsiones y baneos funcionan como comandos slash y con prefijo, por ejemplo `!warn @User spam`. Cada acción crea un caso con número.

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
/case case_id:12

/escalation list
/escalation set warns:3 action:timeout minutes:60  # 3 warnings = 1 hour timeout
/escalation set warns:5 action:kick
/escalation set warns:7 action:ban                 # actions: timeout, kick, ban, jail
/escalation remove warns:5
```

### Gulag (jail)

Los miembros con la cuenta hackeada pasan a un único canal con instrucciones de seguridad. Al liberarlos recuperan sus roles.

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
```

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

### Anti-nuke

Vigila el registro de auditoría y reacciona cuando alguien destruye el servidor. El dueño recibe un mensaje directo.

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

### Verificación

Los miembros nuevos solo ven el canal de verificación hasta que pulsan el botón o resuelven el captcha.

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### Registros

Elige un canal por categoría, o un canal principal para todo.

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### Bienvenida, despedida y boosters

Mensajes, roles automáticos y recompensas para los boosters del servidor.

```
/welcome set channel:#welcome message:Welcome {user} to {server}! dm:Please read the rules.
/welcome set goodbye_channel:#goodbye goodbye_message:{name} left the server.
/welcome autorole role:@Member                     # toggle, given to every new member
/welcome botrole role:@Bots                        # toggle, given to every new bot
/welcome test

/booster set channel:#boosts message:Thank you {user}! remove_on_stop:True
/booster role role:@Booster                        # toggle
```

### Tickets

Los miembros abren canales privados con un botón. Al cerrar se envía una transcripción.

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

### Encuestas y sorteos

Botones para votar y participar. Las duraciones aceptan valores como 30m, 2h y 1d.

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### Sugerencias y starboard

Los miembros publican sugerencias que el equipo puede aprobar o rechazar, y los mensajes populares se destacan.

```
/suggestionsetup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
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

/levelrole add level:10 role:@Active
/levelrole add level:50 role:@Veteran
/levelrole remove level:10
/levelrole list
/levelrole sync                                    # apply to everyone who already has XP

/xp give user:@User amount:500
/xp take user:@User amount:100
/xp setlevel user:@User level:20
/xp reset user:@User

/rank                                              # also: !rank, shows a rank card image
/rank user:@User
/leaderboard
```

### Roles por reacción y notificaciones

Da roles con cualquier emoji y deja que los miembros elijan sus temas de notificación.

```
/reactionrole panel channel:#roles title:Pick your roles description:React below
/reactionrole add message:<message link> emoji:<any emoji> role:@Gamer
/reactionrole add message:<message link> emoji:<any emoji> role:@Artist mode:unique
# mode unique: only one role of that message at a time
/reactionrole remove message:<message link> emoji:<any emoji>
/reactionrole list

/notifytopic add key:events role:@Events description:Server events
/notifytopic panel channel:#roles title:Notifications   # one button per topic
/notifytopic remove key:events
/notify subscribe topic:events                     # members choose for themselves
/notify unsubscribe topic:events
/notify list
```

### Cumpleaños

Los miembros guardan día y mes, el bot da un rol y publica un mensaje ese día.

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Canales de voz temporales

Al entrar en el canal hub se crea una sala que desaparece cuando queda vacía.

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Copia de seguridad y restauración

Las copias incluyen roles, canales, emojis, webhooks y roles de los miembros. La restauración solo añade lo que falta.

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### Datos y privacidad

Los miembros pueden exportar y borrar sus datos. Los administradores controlan cuánto tiempo se conservan.

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### Administración

Activar o desactivar módulos y comandos, cambiar el prefijo, definir alias y limitar comandos a roles.

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

## Marcadores en los mensajes

Estos marcadores se sustituyen en los textos que configures:

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthdaysetup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## Configuración

Las opciones globales se establecen en settings.json. Todo lo demás se configura por servidor con comandos como /module, /command, /perms, /alias y /config.

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

Cada ajuste se puede leer y cambiar con /config. Estas son las rutas que más usarás:

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

## Hoja de ruta

- Panel web local que se ejecuta en tu propio equipo, para cambiar ajustes sin ningún servicio alojado.
- Mensajes del bot traducidos.
- Exportación e importación de ajustes.

## Privacidad y seguridad

- Sin telemetría y sin servicios externos. El bot solo se comunica con Discord.
- Todos los datos están en la carpeta data de tu equipo: ajustes, XP, cumpleaños (solo día y mes) y casos de moderación.
- El bot ignora los mensajes directos de los miembros.
- El token se lee del archivo .env. No lo compartas nunca ni lo subas.
- Los miembros pueden exportar y borrar sus propios datos con /mydata. Los administradores definen cuánto tiempo se conservan los datos de quienes se fueron.
- [PRIVACY.md](../PRIVACY.md)

## Soporte

Errores, ideas y sugerencias: escríbeme en Discord, @justyyin, o abre un issue en GitHub.

## Licencia

Publicado bajo la licencia MIT. Consulta [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
