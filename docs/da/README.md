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
- [Botens rettigheder](#botens-rettigheder)
- [Første skridt i Discord](#første-skridt-i-discord)
- [Kommandoer](#kommandoer)
  - [Moderation](#moderation-1)
  - [Gulag (jail)](#gulag-jail)
  - [Automoderation](#automoderation)
  - [Raidbeskyttelse og låsning](#raidbeskyttelse-og-låsning)
  - [Anti-nuke](#anti-nuke)
  - [Verificering](#verificering)
  - [Logning](#logning-1)
  - [Velkomst, afsked og boosters](#velkomst-afsked-og-boosters)
  - [Tickets](#tickets)
  - [Afstemninger og giveaways](#afstemninger-og-giveaways)
  - [Forslag og starboard](#forslag-og-starboard)
  - [XP og niveauer](#xp-og-niveauer)
  - [Reaktionsroller og notifikationer](#reaktionsroller-og-notifikationer)
  - [Fødselsdage](#fødselsdage)
  - [Midlertidige stemmekanaler](#midlertidige-stemmekanaler)
  - [Backup og gendannelse](#backup-og-gendannelse)
  - [Data og privatliv](#data-og-privatliv)
  - [Administration](#administration-1)
- [Pladsholdere i beskeder](#pladsholdere-i-beskeder)
- [Konfiguration](#konfiguration)
- [Data og lagring](#data-og-lagring)
- [Repositoriets opbygning](#repositoriets-opbygning)
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

## Botens rettigheder

Det nemmeste er rettigheden Administrator. Hvis du foretrækker minimale rettigheder, så giv disse og slå intents Server Members og Message Content til i Developer Portal:

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

## Første skridt i Discord

En fornuftig startopsætning. Kør disse kommandoer på din server og erstat kanaler og roller med dine egne:

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

## Kommandoer

De fleste kommandoer er skråstregskommandoer, moderationskommandoer virker også med præfiks. Den fulde liste findes i kommandoreferencen: [COMMANDS.md](../COMMANDS.md).

### Moderation

Advarsler, mute, kick og bandlysning virker som skråstregskommandoer og med præfiks, for eksempel `!warn @User spam`. Hver handling opretter en nummereret sag.

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

Medlemmer med kapret konto flyttes til én kanal med sikkerhedsvejledning. Ved løsladelse får de deres gamle roller tilbage.

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
```

### Automoderation

Regler sletter eller straffer matchende beskeder. Vælg handling pr. regel: log, delete, warn, timeout eller jail.

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

### Raidbeskyttelse og låsning

Registrerer mange tilgange på kort tid og kan låse serveren. Tilstanden channels ændrer hver kanal, tilstanden role virker med det samme.

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

Overvåger revisionsloggen og reagerer, når nogen ødelægger serveren. Serverens ejer får en direkte besked.

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

### Verificering

Nye medlemmer kan kun se verificeringskanalen, indtil de trykker på knappen eller løser captchaen.

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### Logning

Vælg en kanal pr. kategori, eller én hovedkanal til alt.

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### Velkomst, afsked og boosters

Beskeder, automatiske roller og belønninger til serverens boosters.

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

Medlemmer åbner private kanaler med en knap. Når en ticket lukkes, sendes en udskrift.

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

### Afstemninger og giveaways

Knapper til at stemme og deltage. Varigheder accepterer værdier som 30m, 2h og 1d.

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### Forslag og starboard

Medlemmer sender forslag, som teamet kan godkende eller afvise, og populære beskeder fremhæves.

```
/suggestionsetup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
```

### XP og niveauer

XP for chat og stemme, niveauroller, boosts pr. rolle og rangkort.

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

### Reaktionsroller og notifikationer

Giv roller for reaktioner med vilkårlige emojis, og lad medlemmer vælge deres egne notifikationsemner.

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

### Fødselsdage

Medlemmer gemmer dag og måned, og botten giver en rolle og skriver en besked på dagen.

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Midlertidige stemmekanaler

Når man går ind i hub-kanalen, oprettes et rum, der forsvinder, når det er tomt.

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Backup og gendannelse

Backups indeholder roller, kanaler, emojis, webhooks og medlemmers roller. Gendannelse tilføjer kun det, der mangler.

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### Data og privatliv

Medlemmer kan eksportere og slette deres egne data. Administratorer styrer, hvor længe data gemmes.

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### Administration

Slå moduler og kommandoer til eller fra, skift præfiks, opret aliasser og begræns kommandoer til roller.

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

## Pladsholdere i beskeder

Disse pladsholdere erstattes i de tekster, du indstiller:

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthdaysetup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## Konfiguration

Globale indstillinger angives i settings.json. Alt andet konfigureres pr. server med kommandoer som /module, /command, /perms, /alias og /config.

Hvis du vil omdøbe en kommando, så tilføj den i command_names og genstart botten:

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

Hver enkelt indstilling kan læses og ændres med /config. Det er disse stier, du bruger mest:

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

## Data og lagring

Alt, hvad botten gemmer, ligger på din egen computer:

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

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
