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
- [Requisitos](#requisitos)
- [Inicio rápido](#inicio-rápido)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Comandos](#comandos)
- [Configuración](#configuración)
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

### Administración

- Cada módulo y cada comando se puede activar o desactivar por servidor.
- Prefijo propio, alias de comandos y comandos renombrables.
- Copia de seguridad y restauración de roles y estructura de canales.

## Requisitos

- Python 3.11 o superior
- Una aplicación de Discord con token de bot
- Un ordenador o VPS que permanezca en línea

## Inicio rápido

```
git clone https://github.com/YOUR-NAME/guardbot.git
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

La guía completa paso a paso está en [GUIDE.md](GUIDE.md).

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
    cogs/                 one file per feature group
  docs/                   documentation in 12 languages
  deploy/                 systemd service, Dockerfile, compose file
  scripts/                maintenance scripts
  data/                   created at runtime, holds your settings and data
```

## Comandos

La mayoría de los comandos son comandos slash, los de moderación también funcionan con prefijo. La lista completa está en la referencia de comandos: [COMMANDS.md](../COMMANDS.md).

## Configuración

Las opciones globales se establecen en settings.json. Todo lo demás se configura por servidor con comandos como /module, /command, /perms, /alias y /config.

Para renombrar un comando, añádelo en command_names y reinicia el bot:

```json
{
  "prefix": "!",
  "command_names": {
    "warn": "verwarnen"
  }
}
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
- Los miembros pueden borrar su cumpleaños con /birthday remove.

## Soporte

Errores, ideas y sugerencias: escríbeme en Discord, @justyyin, o abre un issue en GitHub.

## Licencia

Publicado bajo la licencia MIT. Consulta [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany

<!-- GuardBot (c) Justyn -->
