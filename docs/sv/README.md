# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | **Svenska** | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Självhostad Discord-bot för moderering, säkerhet och community. Öppen källkod, gratis, och dina data stannar på din egen dator.

> Beta: GuardBot och dess kontrollpanel är i en betafas. De har inte testats grundligt, särskilt inte på stora servrar eller i alla situationer på Discord. Räkna med buggar, säkerhetskopiera mappen data och rapportera problem. Användning på egen risk.

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
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Startskript och autostart](#startskript-och-autostart)
  - [Uppdatera](#uppdatera)
- [Botens behörigheter](#botens-behörigheter)
- [Första stegen i Discord](#första-stegen-i-discord)
- [Kontrollpanel](#kontrollpanel)
  - [Ställ in kontrollpanelen](#ställ-in-kontrollpanelen)
  - [Säkerhet](#säkerhet-1)
  - [Kontrollpanel på en VPS](#kontrollpanel-på-en-vps)
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
  - [Moderatorverktyg](#moderatorverktyg)
  - [Information](#information)
  - [Meddelanden, taggar och påminnelser](#meddelanden-taggar-och-påminnelser)
  - [Mod-mail och överklagan av avstängning](#mod-mail-och-överklagan-av-avstängning)
  - [Räknekanal, fasta meddelanden och statistik](#räknekanal-fasta-meddelanden-och-statistik)
  - [Fler alternativ för befintliga funktioner](#fler-alternativ-för-befintliga-funktioner)
  - [Fler AutoMod-verktyg](#fler-automod-verktyg)
  - [Moderatorgränser och behörighetsgranskning](#moderatorgränser-och-behörighetsgranskning)
  - [Rapporter och inbjudningsspårning](#rapporter-och-inbjudningsspårning)
  - [Diagnos och felsökning](#diagnos-och-felsökning)
  - [Musik](#musik)
  - [Installation och hälsokontroll](#installation-och-hälsokontroll)
  - [Ekonomi](#ekonomi)
  - [Rollmenyer, schemalagda meddelanden och flöden](#rollmenyer-schemalagda-meddelanden-och-flöden)
  - [Aktivitet, massåtgärder och ärendesökning](#aktivitet-massåtgärder-och-ärendesökning)
  - [Anti-bedrägeri och anti-krypto](#anti-bedrägeri-och-anti-krypto)
  - [Prövotid, svärmigenkänning, tidslinje och inlärning](#prövotid-svärmigenkänning-tidslinje-och-inlärning)
  - [Meddelandebyggare och uppdateringar](#meddelandebyggare-och-uppdateringar)
  - [Drift](#drift)
  - [Administration](#administration-1)
- [Platshållare i meddelanden](#platshållare-i-meddelanden)
- [Konfiguration](#konfiguration)
- [Data och lagring](#data-och-lagring)
- [Repositoriets struktur](#repositoriets-struktur)
- [Översättningar](#översättningar)
- [Färdplan](#färdplan)
- [Integritet och säkerhet](#integritet-och-säkerhet)
- [Support](#support)
- [Tack till](#tack-till)
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
- Anti-bedrägeri: falska giveaways och kryptobluffar tas bort i text och bilder inom millisekunder, även MrBeast-bluffen i alla stavningar.

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
- Ekonomi med butik, rollmenyer med knappar eller rullgardin, schemalagda meddelanden, YouTube-, Twitch- och RSS-flöden, aktivitetsstatistik och en guidad /setup. Meddelanden till medlemmar finns på 12 språk.

### Administration

- Varje modul och varje enskilt kommando kan slås på eller av per server.
- Eget prefix, kommandoalias och kommandon som kan döpas om.
- Säkerhetskopiering och återställning av roller och kanalstruktur.
- Schemalagda automatiska säkerhetskopior av roller, kanaler, emojis och webhooks, med ett återställningskommando som bara lägger till det som saknas.
- Kontrollpanel: ändra inställningarna för varje server i webbläsaren efter inloggning med Discord, bara för medlemmar som hanterar servern och bara medan boten är ansluten.

## Projektstatus

GuardBot är ungt och har ännu inte använts på stora servrar. De automatiska testerna (`python -m unittest`) täcker lagring, upptäckt av personuppgifter, nivåberäkning, kommandoregistrering, behörighetskontroller och länkarna i dokumentationen. Allt som kräver en riktig Discord-server, som låsning, återställning av säkerhetskopior, verifiering, anti-nuke och gulag, täcks inte av dem. Prova de här funktionerna på en testserver innan du förlitar dig på dem. Översättningarna av dokumentationen har inte granskats av modersmålstalare, rättelser är välkomna.

## Krav

- Python 3.11 eller senare
- En Discord-applikation med bot-token
- En dator eller VPS som är online hela tiden
- ffmpeg (bara för musikmodulen)
- tesseract-ocr (valfritt, bara för att läsa text i bilder)

## Snabbstart

Välj ditt system. Varje variant kräver Python 3.11 eller nyare och din bots token. Den utförliga steg-för-steg-guiden finns i [GUIDE.md](GUIDE.md).

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

### Startskript och autostart

Startskripten skapar den virtuella miljön, installerar paketen och startar boten. Vid första körningen skapar de filen .env och stannar, så att du kan skriva in token. Kör dem igen efteråt.

```bash
./start.sh
```

```bat
start.bat
```

För att boten ska fortsätta köra efter en omstart av datorn, använd en tjänst. Linux (systemd) och macOS (launchd):

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

I Windows skapar du en uppgift i Schemaläggaren som kör start.bat vid inloggning, eller använder ett tjänsteomslag som NSSM. För Docker, se [GUIDE.md](GUIDE.md).

### Uppdatera

Stoppa boten, kör dessa kommandon och starta den igen. Dina data i mappen data berörs inte, och boten tar en databassäkerhetskopia före varje ändring av dataformatet.

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

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

## Kontrollpanel

Kontrollpanelen är en webbsida som körs inuti boten. Efter inloggning med Discord ändrar du inställningarna för dina servrar med reglage, menyer och fält i stället för kommandon: moduler, kanaler, roller, tröskelvärden, texter, prefixet och språket. Den visar också de senaste moderationsärendena samt exporterar och importerar inställningar. Den fungerar likadant på din egen dator och på en VPS och är avstängd tills du slår på den.

### Ställ in kontrollpanelen

1. Öppna din applikation i Developer Portal, gå till OAuth2 och kopiera Client Secret till filen .env.
2. Lägg till omdirigeringsadressen http://localhost:8080/callback på samma sida.
3. Slå på kontrollpanelen i settings.json.
4. Starta om boten och öppna http://localhost:8080 i webbläsaren. Logga in med Discord.

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

### Säkerhet

- Inloggning endast med Discord (OAuth2, omfång identify). Åtkomsttoken återkallas direkt och sparas aldrig.
- Endast serverns ägare och medlemmar med behörigheten Administratör eller Hantera server får åtkomst, och bara till den servern. Behörigheten kontrolleras på nytt vid varje förfrågan.
- Endast servrar som boten är ansluten till just nu kan öppnas. Om boten är offline, inte på servern eller fortfarande startar, vägrar kontrollpanelen allt. Den körs inuti boten och har ingen egen databas eller tjänst.
- Som standard lyssnar den bara på 127.0.0.1, så ingen annan i nätverket kan nå den. En offentlig adress accepteras bara med HTTPS, annars startar inte kontrollpanelen.
- Sessioner använder en slumpmässig token i en HttpOnly-cookie med SameSite och, under HTTPS, prefixet __Host-. De upphör efter 8 timmar och finns bara i minnet, så en omstart loggar ut alla.
- Varje ändring kräver en CSRF-token och en matchande Origin. Host-huvudet kontrolleras mot DNS rebinding. Sidan laddar inga externa skript, en strikt Content Security Policy blockerar inbäddad kod, förfrågningar är hastighetsbegränsade och innehållet är begränsat till 256 KB.
- Varje värde kontrolleras mot inställningens typ och Discord-ID:n måste finnas på servern. Internt tillstånd som räknare, ärenden och sparade poster kan inte redigeras. Varje ändring skrivs till serverns säkerhetsloggkanal.
- Meddelandeinnehåll visas aldrig. Moderationsärenden är skrivskyddade.

### Kontrollpanel på en VPS

Låt host vara 127.0.0.1 och välj en av två vägar. Först en SSH-tunnel: ingenting exponeras och du öppnar http://localhost:8080 på din dator medan tunneln körs.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Sedan HTTPS via en omvänd proxy som Caddy, som skaffar ett certifikat själv (se deploy/Caddyfile.example). Sätt då public_url till din https-adress, lägg till https://din-adress/callback som omdirigering i Developer Portal och sätt trust_proxy till true:

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

Redigeraren visar varje inställning som är ett reglage, ett tal, en text, en kanal, en roll eller en enkel lista. Sådant som skapas med kommandon, till exempel butiksartiklar, rollmenyer, flöden, taggar och ärenden, förblir kommandon. Sidan finns på engelska och tyska och följer webbläsarens språk. I Docker publicerar du porten bara på 127.0.0.1 (127.0.0.1:8080:8080) och sätter i containern host till 0.0.0.0 och allow_insecure_http till true.

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
/case view case_id:12

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
/suggestion setup set channel:#suggestions review_role:@Staff
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

/xp levelrole add level:10 role:@Active
/xp levelrole add level:50 role:@Veteran
/xp levelrole remove level:10
/xp levelrole list
/xp levelrole sync                                    # apply to everyone who already has XP

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

/notify topic add key:events role:@Events description:Server events
/notify topic panel channel:#roles title:Notifications   # one button per topic
/notify topic remove key:events
/notify subscribe topic:events                     # members choose for themselves
/notify unsubscribe topic:events
/notify list
```

### Födelsedagar

Medlemmar sparar dag och månad, boten ger en roll och skriver ett meddelande på dagen.

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

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

### Moderatorverktyg

Städa kanaler, hantera roller och för privata anteckningar. Varje åtgärd loggas.

```
/purge amount:50 user:@User kind:links           # kind: all, links, images, bots, attachments
/slowmode seconds:10 channel:#general              # 0 turns it off
/lockchannel channel:#general reason:Spam wave
/unlockchannel channel:#general

/role add member:@User role:@Member
/role remove member:@User role:@Member

/note user:@User text:Watch this member            # private, shown in /cases
/tempban user:@User duration:7d reason:Spam        # unbanned automatically
/jailed                                            # who is in the gulag right now

/case view case_id:12
/case edit case_id:12 reason:Corrected reason
/case delete case_id:12
```

### Information

Slå upp användare, servern, roller och boten.

```
/userinfo user:@User
/serverinfo
/roleinfo role:@Moderator
/avatar user:@User
/help command:ban                                  # explains one command
/ping
/botinfo
```

### Meddelanden, taggar och påminnelser

Skriv i botens namn, skapa egna kommandon, svara automatiskt på meddelanden och sätt påminnelser.

```
/say channel:#news message:Maintenance tonight
/embed channel:#news title:Update description:New rules color:#5865F2

/tag create name:rules text:Be kind to each other
/tag show name:rules
/tag list
/tag info name:rules
/tag edit name:rules text:Be kind and read the pinned message
/tag delete name:rules

/autoresponder add trigger:server ip response:The IP is in #info mode:contains cooldown:30
/autoresponder list
/autoresponder remove id:1                         # mode: contains, word, exact, startswith

/remind set duration:2h text:Stream starts
/remind list
/remind cancel id:1
/afk reason:Lunch                                  # the bot tells others who mention you
```

### Mod-mail och överklagan av avstängning

Medlemmar skriver till personalen via en privat kanal på servern. Ingen behöver skicka ett direktmeddelande till boten.

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

### Räknekanal, fasta meddelanden och statistik

Ett räknespel, meddelanden som stannar längst ned i en kanal och kanaler som visar siffror i realtid.

```
/counting setup channel:#counting reset_on_fail:True delete_wrong:True
/counting status
/counting set number:100
/counting off

/sticky set channel:#rules text:Read the rules before you write
/sticky list
/sticky remove channel:#rules

/stats create template:Members: {members} category:Statistics
/stats add channel:#info template:Boosts: {boosts}
/stats list
/stats refresh
/stats remove channel:#info
```

### Fler alternativ för befintliga funktioner

Tillägg för ärenden, giveaways, röstrum, XP, födelsedagar, säkerhetskopior, loggar och statusvyer.

```
/ticket claim
/ticket rename name:billing-help
/ticket list

/giveaway cancel giveaway_id:3
/giveaway edit giveaway_id:3 prize:Nitro winners:2 extend:1h

/voice rename name:Study room                      # only the owner of the room
/voice limit limit:4
/voice lock
/voice unlock
/voice kick member:@User
/voice transfer member:@User
/voice claim                                       # if the owner left

/xp channelboost channel:#chat multiplier:1.5
/xp resetall confirm:True
/leaderboard page:2

/birthday list
/birthday setup user member:@User day:14 month:3
/birthday setup clear member:@User

/backup info name:weekly
/log show
/log ignorechannel channel:#bots
/log ignoreuser user:@Bot
/log sent enabled:True

/automod status
/verify status
/raid status
/welcome show
/starboard show
```

### Fler AutoMod-verktyg

Följ förkortade länkar, begränsa länkar för nya medlemmar, hitta ghost pings och testa regler utan att straffa någon.

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

### Moderatorgränser och behörighetsgranskning

Få larm när en moderator bannlyser eller sparkar för mycket, och se vilka roller som har farliga behörigheter.

```
/modwatch status
/modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/modwatch exclude member:@TrustedMod

/permaudit run                                                  # roles with dangerous permissions and who holds them
/permaudit watch enabled:True                                   # alarm when a role or member gets one
/permaudit trust role:@Admin
```

### Rapporter och inbjudningsspårning

Medlemmar rapporterar meddelanden till personalen och boten sparar vilken inbjudan som tog in varje ny medlem.

```
/report setup set channel:#reports ping_role:@Moderator cooldown:60 anonymous:False
/report setup ignorechannel channel:#staff
/report setup status

/report send message_link:https://discord.com/channels/1/2/3 reason:Spam
# or right click a message, Apps, Report message

/invites who member:@User
/invites stats user:@User
/invites top
/invites setup log:True alert_joins:5 alert_minutes:60
```

### Diagnos och felsökning

Hitta saknade behörigheter och trasiga inställningar, få felrapporter i en kanal och exportera eller importera inställningarna.

```
/diagnose                                                       # permissions, role order, deleted channels and roles
/debug status
/debug errorchannel channel:#bot-errors
/debug errortest
/debug selftest enabled:True                                    # check at start-up
/debug usagestats enabled:True
/debug usage reset:False
/debug level level:DEBUG                                        # owner of the bot only
/debug db action:check                                          # owner of the bot only: check, vacuum, size

/config export
/config import file:guardbot-settings.json confirm:False        # first without confirm
```

### Musik

Spelar länkar och filer från mappen music i en röstkanal. Nedladdningar sparas som music/Artist/Album/Spår. Kräver ffmpeg och paketen i requirements.txt.

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

/music settings dj_role:@DJ volume:50 max_queue:100 per_user:25 max_minutes:60 idle_leave:120
/music settings allow_links:True allow_search:True allow_playlists:True library:True
/music settings allow_download:True download_format:best announce:True
/config set path:music.allowed_hosts value:bandcamp.com,archive.org
/music cleardj
/music status
```

Förlustfritt: egna filer (FLAC, WAV, ALAC) och källor som erbjuder FLAC spelas upp oförändrade. YouTube, SoundCloud och liknande sajter erbjuder bara ljud med förlust, och det kan inte göras förlustfritt i efterhand. Discord överför röst som Opus, boten använder röstkanalens bitrate. Ansvar: att ladda ner och spela upp innehåll kan strida mot en webbplats villkor eller upphovsrätten. Nedladdningar är avstängda som standard och modulen är av tills du slår på den. Den som driver boten ansvarar för det som spelas och sparas.

### Installation och hälsokontroll

En guidad assistent ställer in det viktigaste med knappar och menyer: loggkanal, välkomstkanal, personalroller, gulagen, en AutoMod-förinställning (lös, normal, sträng), en servermall (community, spel, support) och språket. /health visar vad som är klart och vad som återstår. Språket ändrar de texter som medlemmarna ser, som standardvälkomst, AutoMod-meddelanden, verifiering, tickets, överklaganden, mod-mail och rollmenyer. Fasta svar till administratörer är översatta, svar med namn och siffror förblir på engelska.

```
/setup                                                         # buttons and menus, nothing is switched off by a template
/health                                                        # what is set up, what is open, and the self-test
/language code:de
```

### Ekonomi

En servervaluta med daglig belöning, arbete, betalningar, topplista och en butik vars varor kan ge en roll. Slå på den med modulen economy. Kommandona fungerar också med prefix, till exempel !economy daily.

```
/module enable name:economy
/economy balance member:@User                                  # same as !economy
/economy daily
/economy work
/economy pay member:@User amount:50
/economy leaderboard
/economy shop
/economy buy item:1
/economy inventory

/economy give member:@User amount:500                          # staff, a negative amount takes away
/economy shopadd name:VIP price:1000 role:@VIP stock:10
/economy shopremove item:1
/economy config name:gold daily:200 daily_hours:24 work_min:20 work_max:80 work_minutes:30
```

### Rollmenyer, schemalagda meddelanden och flöden

Rollmenyer ger roller med knappar eller en rullgardinsmeny. Schemalagda meddelanden skickas en gång eller upprepas varje timme, dag eller vecka. Flöden postar nya YouTube-videor, Twitch-sändningar och RSS-inlägg. För YouTube används kanal-ID:t (det börjar med UC). Twitch kräver TWITCH_CLIENT_ID och TWITCH_CLIENT_SECRET i .env. Tider skrivs som in 2h, 18:30 eller som datum med klockslag, till exempel 2026-12-24 18:00, i serverns tidszon. Den första kontrollen av ett flöde minns bara det som redan finns.

```
/rolemenu create title:Pick your roles kind:buttons single:False channel:#roles
/rolemenu add menu:1 role:@Red label:Red
/rolemenu remove menu:1 role:@Red
/rolemenu delete menu:1
/rolemenu list

/schedule add channel:#news when:18:30 text:Daily reminder repeat:daily
/schedule add channel:#news when:in 2h text:Restart soon repeat:none
/schedule list
/schedule remove number:1
/schedule timezone name:Europe/Berlin

/feed add kind:youtube target:UCxxxxxxxxxxxxxxxxxxxxxx channel:#videos ping:@Subscribers
/feed add kind:twitch target:somestreamer channel:#live
/feed add kind:rss target:https://example.com/feed.xml channel:#news
/feed list
/feed check
/feed remove number:1
```

### Aktivitet, massåtgärder och ärendesökning

Aktivitet räknar meddelanden per kanal samt inträden och utträden per dag, aldrig innehåll eller namn. Massåtgärder bannlyser, sparkar eller tystar upp till 25 användare efter en bekräftelse. Ärenden kan sökas efter användare, typ, namn, orsak, moderator och ålder och länkas till varandra, till exempel en anteckning till en bannlysning.

```
/module enable name:activity
/activity overview days:7
/activity channels days:30
/activity growth days:14
/activity reset

/bulk ban users:123456789012345678 223456789012345678 reason:Raid
/bulk kick users:123456789012345678 223456789012345678 reason:Spam
/bulk timeout users:123456789012345678 223456789012345678 duration:2h reason:Spam

/cases user:@User kind:ban text:scam moderator:@Mod days:30
/case link case_id:12 other:15
/case unlink case_id:12 other:15
```

### Anti-bedrägeri och anti-krypto

Tar bort falska giveaways, som den typiska MrBeast-bluffen, i text och bilder inom millisekunder. Namn på direktlistan tas bort direkt i alla stavningar (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Annars läggs ord från listorna (namn, bete, krypto, länkar, belopp) ihop och meddelandet tas bort vid tröskelvärdet. Bilder läses med OCR, och en bild som en gång bedömts som bluff tas bort utan att läsas igen. För bilder krävs tesseract, utan det kontrolleras bara text. En server om MrBeast kan ta bort namnet från direktlistan eller undanta kanaler med /automod exemptchannel. Testa med /antiscam test innan du litar på det.

```
/antiscam status
/antiscam set action:delete threshold:3 text:True images:True ocr_lang:eng max_images:3
/antiscam words action:add kind:instant word:mrbeast
/antiscam words action:remove kind:crypto word:token
/antiscam test text:MrBeast is giving away 1000 BTC, claim now
/antiscam testimage image:scam.png
/antiscam forget
/automod dryrun rule:antiscam enabled:True                     # only report, do not remove
```

### Prövotid, svärmigenkänning, tidslinje och inlärning

Prövotiden placerar nya medlemmar i en roll. Tills de har skrivit det inställda antalet vanliga meddelanden eller minuterna har gått tas länkar, inbjudningar och filer bort med ett kort meddelande. Raidskyddet känner också igen en svärm: flera nya konton med samma namnmönster, samma profilbild eller skapade med några minuters mellanrum. Tidslinjen (/case timeline) sammanför kontots skapande, inträde och inbjudan, prövotid, ärenden och överklaganden för en användare i tidsordning. Meddelanden sparas aldrig och ingår därför inte. /block, /unblock och /blocklist hanterar AutoMods blocklista med korta kommandon. Moderatorer lär anti-bedrägerimodulen med snabbmenyvalet Mark as scam på ett meddelande eller med en reaktion med emojin från learn_emoji: meddelandet raderas och dess bilder och text tas därefter bort direkt. Varje del stänger du av med sin modul eller sina inställningar.

```
/module enable name:probation
/probation setup minutes:10 messages:1 block_links:True block_files:True
/probation status
/probation release member:@User
/probation add member:@User

/raid swarm enabled:True minimum:4 minutes:10
/case timeline user:@User

/block kind:link value:evil.example
/blocklist
/unblock kind:link number:1
/antiscam set learn_emoji:X
```

### Meddelandebyggare och uppdateringar

Meddelandebyggaren postar meddelanden med flera embeds och länkknappar från JSON. Den läser den JSON som embed-generatorer som Embed Generator exporterar, så du utformar ett meddelande där och postar det med boten. Ange JSON som text, som .json-fil eller som https-länk som pekar direkt på JSON, till exempel råfilen i ett arkiv (länkar med omdirigering avvisas). Bara länkknappar skapas, knappar som kräver en interaktion hoppas över. Varje länk måste vara http eller https, omnämnanden i texten pingar aldrig och Discords gränser gäller. /message copy exporterar ett befintligt meddelande som JSON, /message edit ändrar ett meddelande från boten och /message preview visar resultatet bara för dig. Delningslänkar från webbredigerare öppnas inte, eftersom deras format inte är offentligt.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Var 12:e timme kontrollerar boten GitHub-arkivet i update.repo (sätts med scripts/set_repo_url.py) efter en nyare version. Finns det en får botens ägare ett direktmeddelande med versionsanteckningarna, och versionen laddas ned och kontrolleras: SHA-256-kontrollsumma, säkra sökvägar i arkivet och en version som stämmer med taggen. Den installeras med /debug update action:install, eller av sig själv om auto_install är på. Före installationen sparas de ersatta filerna i data/update, nya paket installeras och den nya koden importeras som test. Om något misslyckas återställs de gamla filerna. Din .env, settings.json, data och music rörs aldrig. Sedan startar boten om sig själv. I Docker installeras inget på plats, uppdatera avbilden i stället. En uppdatering kör kod från arkivet, så peka den bara mot ett arkiv du litar på. Stäng av den med enabled satt till false.

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
/message send channel:#news url:https://example.com/message.json
/message send channel:#news file:message.json
/message preview url:https://example.com/message.json
/message edit message:https://discord.com/channels/1/2/3 url:https://example.com/message.json
/message copy message:https://discord.com/channels/1/2/3
/module disable name:builder
/debug update action:status
/debug update action:check
/debug update action:install
```

### Drift

Boten sparar sina data var några sekunder och lagrar databassäkerhetskopior i data/dbbackups, en före varje ändring av dataformatet och en per dag. Musikkön, fästa meddelanden och moderatorräknare överlever en omstart. Stora botar kan köras på flera shards. En heartbeat-fil och en valfri statussida hjälper övervakningsverktyg. De här alternativen anges i settings.json:

```json
{
  "shard_count": null,
  "db_backup_hours": 24,
  "db_backup_keep": 7,
  "health_port": 0,
  "health_host": "127.0.0.1",
  "tesseract": null,
  "music_generic": true
}
```

```
/debug db action:backup                                         # owner of the bot only, saved in data/dbbackups
/debug db action:list
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
/birthday setup set   message                         {user} {name}
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

## Översättningar

Engelska är projektets originalspråk. Alla översättningar av dokumentationen, kontrollpanelen och botens meddelanden har skapats med maskinöversättning och har inte granskats av personer med språket som modersmål. Räkna med klumpiga formuleringar och fel, och rapportera dem gärna eller skicka en rättelse. Filerna finns i docs/ och guardbot/locales/.

## Färdplan

- Diagram för aktivitet och moderation i kontrollpanelen.
- Granskning av alla översättningar av personer med språket som modersmål.
- Fler fasta svarstexter översatta.

## Integritet och säkerhet

- Ingen telemetri. Boten pratar med Discord och, för uppdateringskontrollen, med GitHub (inga personuppgifter skickas, stäng av med update.enabled). Länkar som administratörer ger den, som flöden, musik och JSON-länkar, öppnas bara på begäran.
- All data ligger i mappen data på din dator: inställningar, XP, födelsedagar (endast dag och månad) och modereringsärenden.
- Boten ignorerar direktmeddelanden från medlemmar.
- Token läses från filen .env. Dela den aldrig och ladda inte upp den.
- Medlemmar kan exportera och radera sina egna data med /mydata. Administratörer bestämmer hur länge data från medlemmar som lämnat sparas.
- [PRIVACY.md](../PRIVACY.md)

## Support

Buggar, idéer och förslag: skriv till mig på Discord, @justyyin, eller skapa ett issue på GitHub.

## Tack till

GuardBot är inspirerad av [Embed Generator](https://github.com/merlinfuchs/embed-generator) av Merlin Fuchs (MIT-licens, värd på message.style). Meddelandebyggaren läser samma JSON-format, så meddelanden som utformats där kan postas med den här boten. Ingen kod från det projektet ingår. Tack till upphovspersonerna bakom discord.py, aiohttp, Pillow, yt-dlp, mutagen och Tesseract.

## Licens

Utgiven under MIT-licensen. Se [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
