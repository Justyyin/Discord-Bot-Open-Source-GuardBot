# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | **Dansk** | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Selvhostet Discord-bot til moderation, sikkerhed og fællesskab. Open source, gratis, og dine data bliver på din egen computer.

> Beta: GuardBot og dets dashboard er i en betafase. De er ikke testet grundigt, især ikke på store servere eller i alle situationer på Discord. Regn med fejl, tag sikkerhedskopier af mappen data og meld problemer. Brug på eget ansvar.

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
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Startscripts og autostart](#startscripts-og-autostart)
  - [Opdatering](#opdatering)
- [Botens rettigheder](#botens-rettigheder)
- [Første skridt i Discord](#første-skridt-i-discord)
- [Dashboard](#dashboard)
  - [Opsæt dashboardet](#opsæt-dashboardet)
  - [Sikkerhed](#sikkerhed-1)
  - [Dashboard på en VPS](#dashboard-på-en-vps)
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
  - [Moderatorværktøjer](#moderatorværktøjer)
  - [Information](#information)
  - [Meddelelser, tags og påmindelser](#meddelelser-tags-og-påmindelser)
  - [Mod-mail og anke af udelukkelse](#mod-mail-og-anke-af-udelukkelse)
  - [Tællekanal, faste beskeder og statistik](#tællekanal-faste-beskeder-og-statistik)
  - [Flere muligheder i eksisterende funktioner](#flere-muligheder-i-eksisterende-funktioner)
  - [Flere AutoMod-værktøjer](#flere-automod-værktøjer)
  - [Moderatorgrænser og rettighedsrevision](#moderatorgrænser-og-rettighedsrevision)
  - [Rapporter og invitationssporing](#rapporter-og-invitationssporing)
  - [Diagnose og fejlfinding](#diagnose-og-fejlfinding)
  - [Musik](#musik)
  - [Opsætning og sundhedstjek](#opsætning-og-sundhedstjek)
  - [Økonomi](#økonomi)
  - [Rollemenuer, planlagte beskeder og feeds](#rollemenuer-planlagte-beskeder-og-feeds)
  - [Aktivitet, massehandlinger og sagssøgning](#aktivitet-massehandlinger-og-sagssøgning)
  - [Anti-svindel og anti-krypto](#anti-svindel-og-anti-krypto)
  - [Prøvetid, svarmgenkendelse, tidslinje og indlæring](#prøvetid-svarmgenkendelse-tidslinje-og-indlæring)
  - [Beskedbygger og opdateringer](#beskedbygger-og-opdateringer)
  - [Drift](#drift)
  - [Administration](#administration-1)
- [Pladsholdere i beskeder](#pladsholdere-i-beskeder)
- [Konfiguration](#konfiguration)
- [Data og lagring](#data-og-lagring)
- [Repositoriets opbygning](#repositoriets-opbygning)
- [Oversættelser](#oversættelser)
- [Køreplan](#køreplan)
- [Privatliv og sikkerhed](#privatliv-og-sikkerhed)
- [Support](#support)
- [Tak til](#tak-til)
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
- Anti-svindel: falske giveaways og kryptosvindel fjernes i tekst og billeder inden for millisekunder, også MrBeast-svindlen i enhver stavemåde.

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
- Økonomi med butik, rollemenuer med knapper eller rullemenu, planlagte beskeder, YouTube-, Twitch- og RSS-feeds, aktivitetsstatistik og en guidet /setup. Beskeder til medlemmer findes på 12 sprog.

### Administration

- Hvert modul og hver enkelt kommando kan slås til eller fra pr. server.
- Eget præfiks, kommandoaliasser og kommandoer, der kan omdøbes.
- Backup og gendannelse af roller og kanalstruktur.
- Planlagte automatiske backups af roller, kanaler, emojis og webhooks, med en gendannelseskommando, der kun tilføjer det, der mangler.
- Dashboard: ændr indstillingerne for hver server i browseren efter login med Discord, kun for medlemmer, der administrerer serveren, og kun mens botten er forbundet.

## Projektstatus

GuardBot er ungt og er endnu ikke brugt på store servere. De automatiske tests (`python -m unittest`) dækker lagring, registrering af personlige oplysninger, niveauberegning, kommandoregistrering, rettighedstjek og linksene i dokumentationen. Alt, der kræver en rigtig Discord-server, som låsning, gendannelse af backup, verificering, anti-nuke og gulag, er ikke dækket. Prøv disse funktioner på en testserver, før du stoler på dem. Oversættelserne af dokumentationen er ikke gennemgået af modersmålstalere, rettelser er velkomne.

## Krav

- Python 3.11 eller nyere
- En Discord-applikation med bot-token
- En computer eller VPS, der er online hele tiden
- ffmpeg (kun til musikmodulet)
- tesseract-ocr (valgfrit, kun til at læse tekst i billeder)

## Hurtig start

Vælg dit system. Hver variant kræver Python 3.11 eller nyere og din bots token. Den udførlige trin-for-trin-guide findes i [GUIDE.md](GUIDE.md).

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

### Startscripts og autostart

Startscripts opretter det virtuelle miljø, installerer pakkerne og starter botten. Ved første kørsel opretter de filen .env og stopper, så du kan indtaste token. Kør dem igen bagefter.

```bash
./start.sh
```

```bat
start.bat
```

For at botten kan køre videre efter en genstart af computeren, brug en tjeneste. Linux (systemd) og macOS (launchd):

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

På Windows opretter du en opgave i Opgavestyring (Task Scheduler), der kører start.bat ved login, eller bruger en tjenesteindpakning som NSSM. For Docker, se [GUIDE.md](GUIDE.md).

### Opdatering

Stop botten, kør disse kommandoer og start den igen. Dine data i mappen data bliver ikke rørt, og botten tager en databasesikkerhedskopi før hver ændring af dataformatet.

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

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

## Dashboard

Dashboardet er en webside, der kører inde i botten. Efter login med Discord ændrer du indstillingerne for dine servere med kontakter, menuer og felter i stedet for kommandoer: moduler, kanaler, roller, tærskelværdier, tekster, præfikset og sproget. Det viser også de seneste moderationssager samt eksporterer og importerer indstillinger. Det virker på samme måde på din egen computer og på en VPS og er slået fra, indtil du tænder det.

### Opsæt dashboardet

1. Åbn din applikation i Developer Portal, gå til OAuth2 og kopier Client Secret ind i filen .env.
2. Tilføj omdirigeringsadressen http://localhost:8080/callback på samme side.
3. Slå dashboardet til i settings.json.
4. Genstart botten og åbn http://localhost:8080 i browseren. Log ind med Discord.

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

### Sikkerhed

- Login kun med Discord (OAuth2, scope identify). Adgangstokenet tilbagekaldes med det samme og gemmes aldrig.
- Kun serverens ejer og medlemmer med tilladelsen Administrator eller Administrer server får adgang, og kun til den server. Tilladelsen kontrolleres igen ved hver forespørgsel.
- Kun servere, som botten er forbundet til lige nu, kan åbnes. Hvis botten er offline, ikke på serveren eller stadig starter, afviser dashboardet alt. Det kører inde i botten og har ingen egen database eller tjeneste.
- Som standard lytter det kun på 127.0.0.1, så ingen andre på netværket kan nå det. En offentlig adresse accepteres kun med HTTPS, ellers starter dashboardet ikke.
- Sessioner bruger et tilfældigt token i en HttpOnly-cookie med SameSite og, under HTTPS, præfikset __Host-. De udløber efter 8 timer og findes kun i hukommelsen, så en genstart logger alle ud.
- Hver ændring kræver et CSRF-token og en matchende Origin. Host-headeren kontrolleres mod DNS rebinding. Siden indlæser ingen eksterne scripts, en streng Content Security Policy blokerer inline-kode, forespørgsler er hastighedsbegrænsede, og indholdet er begrænset til 256 KB.
- Hver værdi kontrolleres mod indstillingens type, og Discord-ID'er skal findes på serveren. Intern tilstand som tællere, tickets og gemte poster kan ikke redigeres. Hver ændring skrives til serverens sikkerhedslogkanal.
- Beskedindhold vises aldrig. Moderationssager er skrivebeskyttede.

### Dashboard på en VPS

Lad host stå på 127.0.0.1 og vælg en af to veje. Først en SSH-tunnel: Intet eksponeres, og du åbner http://localhost:8080 på din computer, mens tunnelen kører.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Dernæst HTTPS via en omvendt proxy som Caddy, der selv henter et certifikat (se deploy/Caddyfile.example). Sæt så public_url til din https-adresse, tilføj https://din-adresse/callback som omdirigering i Developer Portal og sæt trust_proxy til true:

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

Editoren viser hver indstilling, der er en kontakt, et tal, en tekst, en kanal, en rolle eller en simpel liste. Det, der oprettes med kommandoer, for eksempel butiksvarer, rollemenuer, feeds, tags og tickets, forbliver kommandoer. Siden findes på engelsk og tysk og følger browserens sprog. I Docker publicerer du kun porten på 127.0.0.1 (127.0.0.1:8080:8080) og sætter i containeren host til 0.0.0.0 og allow_insecure_http til true.

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
/case view case_id:12

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
/suggestion setup set channel:#suggestions review_role:@Staff
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

### Reaktionsroller og notifikationer

Giv roller for reaktioner med vilkårlige emojis, og lad medlemmer vælge deres egne notifikationsemner.

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

### Fødselsdage

Medlemmer gemmer dag og måned, og botten giver en rolle og skriver en besked på dagen.

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

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

### Moderatorværktøjer

Ryd op i kanaler, administrer roller og før private noter. Hver handling logges.

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

Slå brugere, serveren, roller og botten op.

```
/userinfo user:@User
/serverinfo
/roleinfo role:@Moderator
/avatar user:@User
/help command:ban                                  # explains one command
/ping
/botinfo
```

### Meddelelser, tags og påmindelser

Skriv i bottens navn, opret egne kommandoer, svar automatisk på beskeder og sæt påmindelser.

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

### Mod-mail og anke af udelukkelse

Medlemmer skriver til staben via en privat kanal på serveren. Ingen behøver sende en direkte besked til botten.

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

### Tællekanal, faste beskeder og statistik

Et tællespil, beskeder der bliver nederst i en kanal og kanaler med tal i realtid.

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

### Flere muligheder i eksisterende funktioner

Tilføjelser til tickets, giveaways, stemmerum, XP, fødselsdage, sikkerhedskopier, logs og statusvisninger.

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

### Flere AutoMod-værktøjer

Følg forkortede links, begræns links for nye medlemmer, find ghost pings og test regler uden at straffe nogen.

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

### Moderatorgrænser og rettighedsrevision

Få alarm, når en moderator udelukker eller smider for mange ud, og se hvilke roller der har farlige rettigheder.

```
/modwatch status
/modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/modwatch exclude member:@TrustedMod

/permaudit run                                                  # roles with dangerous permissions and who holds them
/permaudit watch enabled:True                                   # alarm when a role or member gets one
/permaudit trust role:@Admin
```

### Rapporter og invitationssporing

Medlemmer rapporterer beskeder til staben, og botten gemmer hvilken invitation der bragte hvert nyt medlem.

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

### Diagnose og fejlfinding

Find manglende rettigheder og ødelagte indstillinger, få fejlrapporter i en kanal og eksporter eller importer indstillingerne.

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

Afspiller links og filer fra mappen music i en stemmekanal. Downloads gemmes som music/Kunstner/Album/Nummer. Kræver ffmpeg og pakkerne i requirements.txt.

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

Tabsfrit: egne filer (FLAC, WAV, ALAC) og kilder med FLAC afspilles uændret. YouTube, SoundCloud og lignende sider tilbyder kun lyd med tab, og det kan ikke gøres tabsfrit bagefter. Discord sender stemme som Opus, botten bruger stemmekanalens bitrate. Ansvar: at downloade og afspille indhold kan bryde et websteds vilkår eller ophavsretten. Downloads er slået fra som standard, og modulet er slukket, indtil du aktiverer det. Den, der driver botten, er ansvarlig for det, der afspilles og gemmes.

### Opsætning og sundhedstjek

En guidet assistent sætter det vigtigste op med knapper og menuer: logkanal, velkomstkanal, staberoller, gulagen, en AutoMod-forudindstilling (løs, normal, streng), en serverskabelon (fællesskab, gaming, support) og sproget. /health viser, hvad der er sat op, og hvad der mangler. Sproget ændrer de tekster, medlemmerne ser, som standardvelkomst, AutoMod-beskeder, verificering, tickets, klager, mod-mail og rollemenuer. Faste svar til administratorer er oversat, svar med navne og tal forbliver på engelsk.

```
/setup                                                         # buttons and menus, nothing is switched off by a template
/health                                                        # what is set up, what is open, and the self-test
/language code:de
```

### Økonomi

En servervaluta med daglig belønning, arbejde, betalinger, rangliste og en butik, hvis varer kan give en rolle. Slå den til med modulet economy. Kommandoerne virker også med præfiks, for eksempel !economy daily.

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

### Rollemenuer, planlagte beskeder og feeds

Rollemenuer giver roller med knapper eller en rullemenu. Planlagte beskeder sendes én gang eller gentages hver time, dag eller uge. Feeds poster nye YouTube-videoer, Twitch-streams og RSS-indlæg. Til YouTube bruges kanal-ID'et (det starter med UC). Twitch kræver TWITCH_CLIENT_ID og TWITCH_CLIENT_SECRET i .env. Tider skrives som in 2h, 18:30 eller som dato med klokkeslæt, for eksempel 2026-12-24 18:00, i serverens tidszone. Den første kontrol af et feed husker kun det, der allerede findes.

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

### Aktivitet, massehandlinger og sagssøgning

Aktivitet tæller beskeder pr. kanal samt tilmeldinger og afgange pr. dag, aldrig indhold eller navne. Massehandlinger udelukker, smider ud eller sætter op til 25 brugere i timeout efter en bekræftelse. Sager kan søges efter bruger, type, navn, årsag, moderator og alder og kobles sammen, for eksempel en note til en udelukkelse.

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

### Anti-svindel og anti-krypto

Fjerner falske giveaways, som den typiske MrBeast-svindel, i tekst og billeder inden for millisekunder. Navne på direkte-listen fjernes med det samme i enhver stavemåde (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Ellers lægges ord fra listerne (navne, lokkemad, krypto, links, beløb) sammen, og beskeden fjernes ved tærskelværdien. Billeder læses med OCR, og et billede, der én gang er dømt som svindel, fjernes uden at blive læst igen. Billeder kræver tesseract, uden det kontrolleres kun tekst. En server om MrBeast kan fjerne navnet fra direkte-listen eller undtage kanaler med /automod exemptchannel. Prøv med /antiscam test, før du stoler på det.

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

### Prøvetid, svarmgenkendelse, tidslinje og indlæring

Prøvetiden placerer nye medlemmer i en rolle. Indtil de har skrevet det indstillede antal almindelige beskeder, eller minutterne er gået, fjernes links, invitationer og filer med en kort besked. Raidbeskyttelsen genkender også en svarm: flere nye konti med samme navnemønster, samme profilbillede eller oprettet med få minutters mellemrum. Tidslinjen (/case timeline) samler kontoens oprettelse, tilgang og invitation, prøvetid, sager og klager for en bruger i tidsrækkefølge. Beskeder gemmes aldrig og er derfor ikke med. /block, /unblock og /blocklist styrer AutoMods blokliste med korte kommandoer. Moderatorer lærer anti-svindel-modulet noget med kontekstmenuen Mark as scam på en besked eller med en reaktion med emojien fra learn_emoji: beskeden slettes, og dens billeder og tekst fjernes derefter med det samme. Hver del slår du fra med sit modul eller sine indstillinger.

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

### Beskedbygger og opdateringer

Beskedbyggeren sender beskeder med flere embeds og linkknapper ud fra JSON. Den læser den JSON, som embed-generatorer som Embed Generator eksporterer, så du designer en besked dér og sender den med botten. Angiv JSON som tekst, som .json-fil eller som https-link, der peger direkte på JSON, for eksempel råfilen i et repository (links med omdirigering afvises). Kun linkknapper oprettes, knapper der kræver en interaktion springes over. Hvert link skal være http eller https, omtaler i teksten pinger aldrig, og Discords grænser gælder. /message copy eksporterer en eksisterende besked som JSON, /message edit ændrer en besked fra botten, og /message preview viser resultatet kun for dig. Delingslinks fra webeditorer åbnes ikke, fordi deres format ikke er offentligt.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Hver 12. time tjekker botten GitHub-repositoryet i update.repo (sættes med scripts/set_repo_url.py) for en nyere version. Findes der en, får botens ejer en direkte besked med udgivelsesnoterne, og versionen hentes og kontrolleres: SHA-256-kontrolsum, sikre stier i arkivet og en version, der passer til tagget. Den installeres med /debug update action:install eller af sig selv, hvis auto_install er slået til. Før installationen gemmes de erstattede filer i data/update, nye pakker installeres, og den nye kode importeres som test. Fejler noget, gendannes de gamle filer. Din .env, settings.json, data og music røres aldrig. Derefter genstarter botten sig selv. I Docker installeres intet på stedet, opdater i stedet billedet. En opdatering kører kode fra repositoryet, så peg den kun på et repository, du stoler på. Slå den fra med enabled sat til false.

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

Botten gemmer sine data hvert par sekunder og opbevarer databasesikkerhedskopier i data/dbbackups, én før hver ændring af dataformatet og én om dagen. Musikkøen, fastgjorte beskeder og moderatortællere overlever en genstart. Store bots kan køre på flere shards. En heartbeat-fil og en valgfri statusside hjælper overvågningsværktøjer. Disse indstillinger sættes i settings.json:

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
/birthday setup set   message                         {user} {name}
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

## Oversættelser

Engelsk er projektets originalsprog. Alle oversættelser af dokumentationen, dashboardet og botbeskederne er lavet med maskinoversættelse og er ikke gennemgået af personer med sproget som modersmål. Regn med klodsede formuleringer og fejl, og meld dem gerne eller send en rettelse. Filerne ligger i docs/ og guardbot/locales/.

## Køreplan

- Diagrammer for aktivitet og moderation i dashboardet.
- Gennemgang af alle oversættelser af personer med sproget som modersmål.
- Flere faste svartekster oversat.

## Privatliv og sikkerhed

- Ingen telemetri. Botten taler med Discord og, til opdateringstjekket, med GitHub (der sendes ingen personlige data, slå det fra med update.enabled). Links, som administratorer giver den, som feeds, musik og JSON-links, åbnes kun efter anmodning.
- Alle data ligger i mappen data på din computer: indstillinger, XP, fødselsdage (kun dag og måned) og moderationssager.
- Botten ignorerer direkte beskeder fra medlemmer.
- Tokenet læses fra filen .env. Del det aldrig, og upload det ikke.
- Medlemmer kan eksportere og slette deres egne data med /mydata. Administratorer bestemmer, hvor længe data fra medlemmer, der er gået, gemmes.
- [PRIVACY.md](../PRIVACY.md)

## Support

Fejl, idéer og forslag: skriv til mig på Discord, @justyyin, eller opret et issue på GitHub.

## Tak til

GuardBot er inspireret af [Embed Generator](https://github.com/merlinfuchs/embed-generator) af Merlin Fuchs (MIT-licens, hostet på message.style). Beskedbyggeren læser det samme JSON-format, så beskeder designet dér kan sendes med denne bot. Der er ingen kode fra det projekt med. Tak til forfatterne bag discord.py, aiohttp, Pillow, yt-dlp, mutagen og Tesseract.

## Licens

Udgivet under MIT-licensen. Se [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
