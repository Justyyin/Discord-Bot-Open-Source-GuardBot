# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | **Dansk** | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Selvhostet Discord-bot til moderation, sikkerhed og fællesskab. Open source, gratis, og dine data bliver på din egen computer.

<!-- toc -->

- [Om projektet](#om-projektet)
- [Funktioner](#funktioner)
  - [Sikkerhed](#sikkerhed)
  - [Moderation](#moderation)
  - [Logning](#logning)
  - [Fællesskab](#fællesskab)
  - [Administration](#administration)
- [Projektstatus](#projektstatus)
- [Krav](#krav)
- [Hurtig start](#hurtig-start)
- [Repositoriets opbygning](#repositoriets-opbygning)
- [Kommandoer](#kommandoer)
- [Konfiguration](#konfiguration)
- [Køreplan](#køreplan)
- [Privatliv og sikkerhed](#privatliv-og-sikkerhed)
- [Support](#support)
- [Licens](#licens)

<!-- tocstop -->

## Om projektet

GuardBot samler funktioner, som mange servere betaler for hos hostede bots: moderation, logning, anti-raid, anti-nuke, tickets, niveauer og mere. Du kører botten selv, på din egen computer eller på en lille VPS.

Hostede bots gemmer serverdata, medlems-id'er og nogle gange e-mailadresser hos en tredjepart. Når du selv hoster botten, forlader de data aldrig din computer. GuardBot skal vise, at alle kan køre en komplet bot uden abonnement.

## Funktioner

### Sikkerhed

- Automoderation: ordfilter, versalfilter, mention-spam, invitationslinks, phishing-domæner, personlige oplysninger, doxxing og trusler. Alle lister kan redigeres.
- Anti-raid med registrering af tilstrømning og låsning af hele serveren.
- Anti-nuke: grænser for massesletninger og bandlysninger, automatisk reaktion og en direkte besked til serverens ejer.
- Gulag-kanal: den, der poster svindellinks eller billeder, flyttes til én kanal med vejledning i at sikre kontoen. Moderatorer kan også bruge /jail og /unjail.
- Verificering med knap eller captcha, med automatisk fjernelse af medlemmer, der ikke når at verificere sig.
- Anti-nuke overvåger også tildeling af rettigheder, nye webhooks, tilføjede bots og navneskift på serveren.

### Moderation

- Warn, mute, kick, ban og jail med historik, der kan filtreres efter omtale, bruger-id eller type.
- Automatisk eskalering, for eksempel fører tre advarsler til en timeout.
- Vælg, hvilke roller eller brugere der må bruge hver moderationskommando.

### Logning

- Sendte, redigerede og slettede beskeder inklusive billeder, GIF'er og URL'er, med separate logkanaler.
- Ændringer af roller, kaldenavne, bandlysninger, stemme, kanaler og serverroller.

### Fællesskab

- Velkomst- og afskedsbeskeder, automatiske roller og belønninger til boosters.
- Tickets, afstemninger, giveaways og forslag.
- Reaktionsroller med vilkårlige emojis og notifikationsemner, som medlemmer selv slår til eller fra.
- XP og niveauer fra 1 til 100 for chat og stemme, niveauroller og fødselsdage.
- Starboard og midlertidige stemmekanaler.
- Jail med varighed, afstemninger med flere valg, rangkort som billede og XP-boosts pr. rolle.

### Administration

- Hvert modul og hver enkelt kommando kan slås til eller fra pr. server.
- Eget præfiks, kommandoaliasser og kommandoer, der kan omdøbes.
- Backup og gendannelse af roller og kanalstruktur.
- Planlagte automatiske backups af roller, kanaler, emojis og webhooks, med en gendannelseskommando, der kun tilføjer det, der mangler.

## Projektstatus

GuardBot er ungt og er endnu ikke brugt på store servere. De automatiske tests (`python -m unittest`) dækker lagring, registrering af personlige oplysninger, niveauberegning, kommandoregistrering, rettighedstjek og linksene i dokumentationen. Alt, der kræver en rigtig Discord-server, som låsning, gendannelse af backup, verificering, anti-nuke og gulag, er ikke dækket. Prøv disse funktioner på en testserver, før du stoler på dem. Oversættelserne af dokumentationen er ikke gennemgået af modersmålstalere, rettelser er velkomne.

## Krav

- Python 3.11 eller nyere
- En Discord-applikation med bot-token
- En computer eller VPS, der er online hele tiden

## Hurtig start

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Den fulde trin-for-trin-vejledning findes i [GUIDE.md](GUIDE.md).

## Repositoriets opbygning

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

## Kommandoer

De fleste kommandoer er skråstregskommandoer, moderationskommandoer virker også med præfiks. Den fulde liste findes i kommandoreferencen: [COMMANDS.md](../COMMANDS.md).

## Konfiguration

Globale indstillinger angives i settings.json. Alt andet konfigureres pr. server med kommandoer som /module, /command, /perms, /alias og /config.

Hvis du vil omdøbe en kommando, så tilføj den i command_names og genstart botten:

```json
{
  "prefix": "!",
  "command_names": {
    "warn": "verwarnen"
  }
}
```

## Køreplan

- Lokalt webdashboard, der kører på din egen computer, så indstillinger kan ændres uden en hostet tjeneste.
- Oversatte botbeskeder.
- Eksport og import af indstillinger.

## Privatliv og sikkerhed

- Ingen telemetri og ingen eksterne tjenester. Botten taler kun med Discord.
- Alle data ligger i mappen data på din computer: indstillinger, XP, fødselsdage (kun dag og måned) og moderationssager.
- Botten ignorerer direkte beskeder fra medlemmer.
- Tokenet læses fra filen .env. Del det aldrig, og upload det ikke.
- Medlemmer kan eksportere og slette deres egne data med /mydata. Administratorer bestemmer, hvor længe data fra medlemmer, der er gået, gemmes.
- [PRIVACY.md](../PRIVACY.md)

## Support

Fejl, idéer og forslag: skriv til mig på Discord, @justyyin, eller opret et issue på GitHub.

## Licens

Udgivet under MIT-licensen. Se [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
