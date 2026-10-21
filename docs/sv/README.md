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
- [Projektstatus](#projektstatus)
- [Krav](#krav)
- [Snabbstart](#snabbstart)
- [Botens behörigheter](#botens-behörigheter)
- [Första stegen i Discord](#första-stegen-i-discord)
- [Kommandon](#kommandon)
  - [Moderering](#moderering-1)
  - [Gulag (jail)](#gulag-jail)
  - [Automoderering](#automoderering)
  - [Raidskydd och låsning](#raidskydd-och-låsning)
  - [Anti-nuke](#anti-nuke)
  - [Verifiering](#verifiering)
  - [Loggning](#loggning-1)
  - [Välkomst, avsked och boosters](#välkomst-avsked-och-boosters)
  - [Tickets](#tickets)
  - [Omröstningar och giveaways](#omröstningar-och-giveaways)
  - [Förslag och starboard](#förslag-och-starboard)
  - [XP och nivåer](#xp-och-nivåer)
  - [Reaktionsroller och aviseringar](#reaktionsroller-och-aviseringar)
  - [Födelsedagar](#födelsedagar)
  - [Tillfälliga röstkanaler](#tillfälliga-röstkanaler)
  - [Säkerhetskopiering och återställning](#säkerhetskopiering-och-återställning)
  - [Data och integritet](#data-och-integritet)
  - [Administration](#administration-1)
- [Platshållare i meddelanden](#platshållare-i-meddelanden)
- [Konfiguration](#konfiguration)
- [Data och lagring](#data-och-lagring)
- [Repositoriets struktur](#repositoriets-struktur)
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
- Verifiering med knapp eller captcha, med automatisk borttagning av medlemmar som inte verifierar sig i tid.
- Anti-nuke bevakar också beviljade behörigheter, nya webhooks, tillagda botar och namnbyten på servern.

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
- Jail med tidsgräns, omröstningar med flerval, rankkort som bild och XP-boostar per roll.

### Administration

- Varje modul och varje enskilt kommando kan slås på eller av per server.
- Eget prefix, kommandoalias och kommandon som kan döpas om.
- Säkerhetskopiering och återställning av roller och kanalstruktur.
- Schemalagda automatiska säkerhetskopior av roller, kanaler, emojis och webhooks, med ett återställningskommando som bara lägger till det som saknas.

## Projektstatus

GuardBot är ungt och har ännu inte använts på stora servrar. De automatiska testerna (`python -m unittest`) täcker lagring, upptäckt av personuppgifter, nivåberäkning, kommandoregistrering, behörighetskontroller och länkarna i dokumentationen. Allt som kräver en riktig Discord-server, som låsning, återställning av säkerhetskopior, verifiering, anti-nuke och gulag, täcks inte av dem. Prova de här funktionerna på en testserver innan du förlitar dig på dem. Översättningarna av dokumentationen har inte granskats av modersmålstalare, rättelser är välkomna.

## Krav

- Python 3.11 eller senare
- En Discord-applikation med bot-token
- En dator eller VPS som är online hela tiden

## Snabbstart

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Den fullständiga steg-för-steg-guiden finns i [GUIDE.md](GUIDE.md).

## Botens behörigheter

Enklast är behörigheten Administratör. Om du föredrar minimala rättigheter ger du dessa och slår på intenten Server Members och Message Content i Developer Portal:

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

## Första stegen i Discord

En vettig startkonfiguration. Kör de här kommandona på din server och byt ut kanaler och roller mot dina egna:

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

## Kommandon

De flesta kommandon är snedstreckskommandon, modereringskommandon fungerar även med prefix. Den fullständiga listan finns i kommandoreferensen: [COMMANDS.md](../COMMANDS.md).

### Moderering

Varningar, mute, kick och bann fungerar som snedstreckskommandon och med prefix, till exempel `!warn @User spam`. Varje åtgärd skapar ett numrerat ärende.

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

Medlemmar med kapat konto flyttas till en enda kanal med säkerhetsanvisningar. Vid frisläppning får de tillbaka sina gamla roller.

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
```

### Automoderering

Regler raderar eller bestraffar matchande meddelanden. Välj åtgärd per regel: log, delete, warn, timeout eller jail.

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

### Raidskydd och låsning

Upptäcker många inträden på kort tid och kan låsa servern. Läget channels ändrar varje kanal, läget role verkar direkt.

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

Bevakar granskningsloggen och reagerar när någon förstör servern. Serverägaren får ett direktmeddelande.

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

### Verifiering

Nya medlemmar ser bara verifieringskanalen tills de trycker på knappen eller löser captchan.

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### Loggning

Välj en kanal per kategori, eller en huvudkanal för allt.

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### Välkomst, avsked och boosters

Meddelanden, automatiska roller och belöningar för serverns boosters.

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

Medlemmar öppnar privata kanaler med en knapp. När ärendet stängs skickas en utskrift.

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

### Omröstningar och giveaways

Knappar för att rösta och delta. Tider accepterar värden som 30m, 2h och 1d.

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### Förslag och starboard

Medlemmar skickar förslag som teamet kan godkänna eller avslå, och populära meddelanden lyfts fram.

```
/suggestionsetup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
```

### XP och nivåer

XP för chatt och röst, nivåroller, boostar per roll och rankkort.

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

### Reaktionsroller och aviseringar

Ge roller för reaktioner med valfri emoji och låt medlemmar välja sina aviseringsämnen.

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

### Födelsedagar

Medlemmar sparar dag och månad, boten ger en roll och skriver ett meddelande på dagen.

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Tillfälliga röstkanaler

Att gå in i hubbkanalen skapar ett rum som försvinner när det är tomt.

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Säkerhetskopiering och återställning

Kopior innehåller roller, kanaler, emojis, webhooks och medlemmarnas roller. Återställning lägger bara till det som saknas.

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### Data och integritet

Medlemmar kan exportera och radera sina data. Administratörer styr hur länge data sparas.

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### Administration

Slå på eller av moduler och kommandon, byt prefix, skapa alias och begränsa kommandon till roller.

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

## Platshållare i meddelanden

De här platshållarna ersätts i texterna du ställer in:

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthdaysetup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## Konfiguration

Globala alternativ anges i settings.json. Allt annat konfigureras per server med kommandon som /module, /command, /perms, /alias och /config.

Om du vill döpa om ett kommando lägger du till det i command_names och startar om boten:

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

Varje inställning kan läsas och ändras med /config. Det här är de sökvägar du använder oftast:

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

## Data och lagring

Allt som boten sparar ligger på din egen dator:

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

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
    images.py             rank cards and captcha images
    cogs/                 one file per feature group
  docs/                   documentation in 12 languages, COMMANDS.md, PRIVACY.md
  deploy/                 systemd service, Dockerfile, compose file
  scripts/                maintenance scripts
  tests/                  automated tests (python -m unittest)
  data/                   created at runtime, holds your settings and data
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
- Medlemmar kan exportera och radera sina egna data med /mydata. Administratörer bestämmer hur länge data från medlemmar som lämnat sparas.
- [PRIVACY.md](../PRIVACY.md)

## Support

Buggar, idéer och förslag: skriv till mig på Discord, @justyyin, eller skapa ett issue på GitHub.

## Licens

Utgiven under MIT-licensen. Se [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
