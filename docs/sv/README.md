# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | **Svenska** | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Självhostad Discord-bot för moderering, säkerhet och community. Öppen källkod, gratis, och dina data stannar på din egen dator.

<!-- toc -->

- [Om projektet](#om-projektet)
- [Funktioner](#funktioner)
  - [Säkerhet](#säkerhet)
  - [Moderering](#moderering)
  - [Loggning](#loggning)
  - [Community](#community)
  - [Administration](#administration)
- [Krav](#krav)
- [Snabbstart](#snabbstart)
- [Repositoriets struktur](#repositoriets-struktur)
- [Kommandon](#kommandon)
- [Konfiguration](#konfiguration)
- [Färdplan](#färdplan)
- [Integritet och säkerhet](#integritet-och-säkerhet)
- [Support](#support)
- [Licens](#licens)

<!-- tocstop -->

## Om projektet

GuardBot samlar funktioner som många servrar betalar för hos hostade botar: moderering, loggning, anti-raid, anti-nuke, tickets, nivåer och mer. Du kör boten själv, på din egen dator eller på en liten VPS.

Hostade botar lagrar serverdata, medlems-ID och ibland e-postadresser hos en tredje part. När du hostar boten själv lämnar de uppgifterna aldrig din dator. GuardBot ska visa att vem som helst kan köra en fullständig bot utan prenumeration.

## Funktioner

### Säkerhet

- Automoderering: ordfilter, versalfilter, mention-spam, inbjudningslänkar, nätfiskedomäner, personuppgifter, doxxing och hot. Alla listor kan redigeras.
- Anti-raid med upptäckt av inströmning och låsning av hela servern.
- Anti-nuke: gränser för massborttagningar och bannlysningar, automatisk reaktion och ett direktmeddelande till serverägaren.
- Gulag-kanal: den som postar bedrägerilänkar eller bilder flyttas till en enda kanal med instruktioner för att säkra kontot. Moderatorer kan också använda /jail och /unjail.

### Moderering

- Warn, mute, kick, ban och jail med historik som kan filtreras på omnämnande, användar-ID eller typ.
- Automatisk eskalering, till exempel leder tre varningar till en timeout.
- Välj vilka roller eller användare som får använda varje modereringskommando.

### Loggning

- Skickade, redigerade och raderade meddelanden inklusive bilder, GIF:ar och URL:er, med separata loggkanaler.
- Ändringar av roller, smeknamn, bannlysningar, röst, kanaler och serverroller.

### Community

- Välkomst- och avskedsmeddelanden, automatiska roller och belöningar för boosters.
- Tickets, omröstningar, giveaways och förslag.
- Reaktionsroller med valfri emoji och aviseringsämnen som medlemmar slår på eller av själva.
- XP och nivåer från 1 till 100 för chatt och röst, nivåroller och födelsedagar.
- Starboard och tillfälliga röstkanaler.

### Administration

- Varje modul och varje enskilt kommando kan slås på eller av per server.
- Eget prefix, kommandoalias och kommandon som kan döpas om.
- Säkerhetskopiering och återställning av roller och kanalstruktur.

## Krav

- Python 3.11 eller senare
- En Discord-applikation med bot-token
- En dator eller VPS som är online hela tiden

## Snabbstart

```
git clone https://github.com/YOUR-NAME/guardbot.git
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Den fullständiga steg-för-steg-guiden finns i [GUIDE.md](GUIDE.md).

## Repositoriets struktur

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

## Kommandon

De flesta kommandon är snedstreckskommandon, modereringskommandon fungerar även med prefix. Den fullständiga listan finns i kommandoreferensen: [COMMANDS.md](../COMMANDS.md).

## Konfiguration

Globala alternativ anges i settings.json. Allt annat konfigureras per server med kommandon som /module, /command, /perms, /alias och /config.

Om du vill döpa om ett kommando lägger du till det i command_names och startar om boten:

```json
{
  "prefix": "!",
  "command_names": {
    "warn": "verwarnen"
  }
}
```

## Färdplan

- Lokal webbpanel som körs på din egen dator, så att inställningar kan ändras utan någon hostad tjänst.
- Översatta botmeddelanden.
- Export och import av inställningar.

## Integritet och säkerhet

- Ingen telemetri och inga externa tjänster. Boten pratar bara med Discord.
- All data ligger i mappen data på din dator: inställningar, XP, födelsedagar (endast dag och månad) och modereringsärenden.
- Boten ignorerar direktmeddelanden från medlemmar.
- Token läses från filen .env. Dela den aldrig och ladda inte upp den.
- Medlemmar kan själva ta bort sin födelsedag med /birthday remove.

## Support

Buggar, idéer och förslag: skriv till mig på Discord, @justyyin, eller skapa ett issue på GitHub.

## Licens

Utgiven under MIT-licensen. Se [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany

<!-- GuardBot (c) Justyn -->
