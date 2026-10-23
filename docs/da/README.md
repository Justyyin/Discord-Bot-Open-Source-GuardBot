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
  - [Struktur, medlemmer og team](#struktur-medlemmer-og-team)
- [Dashboard](#dashboard)
  - [Opsæt dashboardet](#opsæt-dashboardet)
  - [Sikkerhed](#sikkerhed-1)
  - [Dashboard på en VPS](#dashboard-på-en-vps)
- [Kommandoer](#kommandoer)
  - [Kommandogrupper](#kommandogrupper)
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
- Gulag-kanal: den, der poster svindellinks eller billeder, flyttes til én kanal med vejledning i at sikre kontoen. Moderatorer kan også bruge /moderation jail og /moderation unjail.
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
- Økonomi med butik, rollemenuer med knapper eller rullemenu, planlagte beskeder, YouTube-, Twitch- og RSS-feeds, aktivitetsstatistik og en guidet /admin setup. Beskeder til medlemmer findes på 12 sprog.

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

### Struktur, medlemmer og team

Version 1.5 tilføjer kommandoer til at bygge og holde en server ryddelig, gendanne medlemmer der vender tilbage og lede modereringsteamet. Hver del har en modulkontakt (`/admin module`), egne indstillinger og en plads i dashboardet.

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

- Med `/structure` oprettes, klones, omdøbes og sorteres kanaler og kategorier, og rettigheder kopieres fra en anden kanal. Inaktive kanaler rapporteres eller flyttes til en arkivkategori (`/structure archive`). Roller kan gives tidsbegrænset og gemmes som skabeloner; en skabelon giver aldrig en rettighed, som den der bruger den ikke selv har.
- `/structure rules` udgiver reglerne med en accepter-knap og et versionsnummer. Efter `post new_version:True` får medlemmer, der ikke har accepteret den nye version, én påmindelse som direkte besked.
- `/members stickyroles` giver roller tilbage og gendanner timeout eller mute, når et medlem vender tilbage. `/members nickname` fjerner tegn, der løfter navnet øverst på listen, tjekker forbudte ord i kaldenavne og brugernavne og omdøber overtrædere. Overvågningslisten er stille: teamet får besked ved første besked fra en opført bruger.
- Fire-øjne-godkendelse (`/security approval`) kører bans, kicks, timeouts og massehandlinger først, når en anden moderator er enig. `/moderation case undo` tager en sag tilbage, også de handlinger den førte med sig (for eksempel en mute og den ban, der fulgte). Advarsler kan udløbe efter et antal dage (`/moderation escalation expiry`).
- `/admin history` viser, hvem der ændrede hvilken indstilling og hvornår, og ruller et afsnit tilbage. Personens navn er et gæt ud fra de seneste kommandoer og dashboard-ændringer på serveren. `/admin history copy` kopierer afsnit til en anden server, som du må styre med botten; den starter som en prøvekørsel. `/admin exceptions` holder kanaler og roller uden for AutoMod-regler og Anti-Scam. `/admin dashaccess` giver roller skrivebeskyttet adgang eller moderatoradgang til dashboardet.
- `/team` viser hver moderators arbejde (sager, tickets, rapporter, svartid, inaktive medlemmer), sender en ugerapport (dag og time i UTC), lader moderatorer melde sig fra med `/team duty away`, så tickets og pings går til andre, og styrer ansøgninger til teamet med formular og afstemning.
- Discord kan ikke skjule kommandoer i en gruppe for enkelte medlemmer. Botten kontrollerer stadig hvert kald. Tallene i teamstatistikken tælles fra dagen for opdateringen; ældre handlinger mangler.

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

<!-- groups -->
### Kommandogrupper

For at spare pladser til skråstregskommandoer (Discord tillader 100 kommandoer på øverste niveau pr. bot) er kommandoer, der hører sammen, grupperet. Skriv først gruppen og derefter kommandoen, for eksempel `/moderation ban`. Tekstkommandoer med præfiks, for eksempel `!ban`, er upåvirkede. Rettigheder, aliasser og modulkontakter bruger stadig det enkle kommandonavn.

| Gruppe | Indeholder |
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

### Moderation

Advarsler, mute, kick og bandlysning virker som skråstregskommandoer og med præfiks, for eksempel `!warn @User spam`. Hver handling opretter en nummereret sag.

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

Medlemmer med kapret konto flyttes til én kanal med sikkerhedsvejledning. Ved løsladelse får de deres gamle roller tilbage.

```
/access jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/access jailsetup apply                                   # apply the channel permissions again
/access jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/access jailsetup preview

/moderation jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/moderation jail member:@User duration:2h                     # released automatically after 2 hours
/moderation unjail member:@User reason:Account secured
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

Overvåger revisionsloggen og reagerer, når nogen ødelægger serveren. Serverens ejer får en direkte besked.

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

### Verificering

Nye medlemmer kan kun se verificeringskanalen, indtil de trykker på knappen eller løser captchaen.

```
/access verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/access verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/access verify panel channel:#verify                      # post the button again
/access verify apply                                      # apply the channel permissions again
/access verify member member:@User                        # verify someone manually
/access verify off
```

### Logning

Vælg en kanal pr. kategori, eller én hovedkanal til alt.

```
/server log set category:main channel:#logs               # fallback for every category
/server log set category:messages channel:#log-messages
/server log set category:moderation channel:#log-moderation
/server log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/server log sent enabled:False                            # stop logging every sent message
/server log show
```

### Velkomst, afsked og boosters

Beskeder, automatiske roller og belønninger til serverens boosters.

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

Medlemmer åbner private kanaler med en knap. Når en ticket lukkes, sendes en udskrift.

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

### Afstemninger og giveaways

Knapper til at stemme og deltage. Varigheder accepterer værdier som 30m, 2h og 1d.

```
/engage poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/engage poll end poll_id:3
/engage poll list

/engage giveaway start prize:Nitro duration:2d winners:2 role:@Member
/engage giveaway end giveaway_id:1
/engage giveaway reroll giveaway_id:1
/engage giveaway list
```

### Forslag og starboard

Medlemmer sender forslag, som teamet kan godkende eller afvise, og populære beskeder fremhæves.

```
/suggestion setup set channel:#suggestions review_role:@Staff
/support suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/engage starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/engage starboard ignore channel:#spam
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

/info rank                                              # also: !rank, shows a rank card image
/info rank user:@User
/info leaderboard
```

### Reaktionsroller og notifikationer

Giv roller for reaktioner med vilkårlige emojis, og lad medlemmer vælge deres egne notifikationsemner.

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
/community tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Backup og gendannelse

Backups indeholder roller, kanaler, emojis, webhooks og medlemmers roller. Gendannelse tilføjer kun det, der mangler.

```
/server backup create name:before-update
/server backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/server backup list
/server backup download name:before-update
/server backup restore name:before-update member_roles:True   # only adds what is missing
/server backup delete name:before-update
```

### Data og privatliv

Medlemmer kan eksportere og slette deres egne data. Administratorer styrer, hvor længe data gemmes.

```
/info mydata export                                     # members download their own data
/info mydata delete confirm:True                        # members delete their XP and birthday

/server privacy retention days:90                         # delete data of members who left after 90 days
/server privacy export user_id:123456789012345678
/server privacy delete user_id:123456789012345678 cases:True
```

### Moderatorværktøjer

Ryd op i kanaler, administrer roller og før private noter. Hver handling logges.

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

### Information

Slå brugere, serveren, roller og botten op.

```
/info userinfo user:@User
/server serverinfo
/server roleinfo role:@Moderator
/info avatar user:@User
/help command:ban                                  # explains one command
/info ping
/info botinfo
```

### Meddelelser, tags og påmindelser

Skriv i bottens navn, opret egne kommandoer, svar automatisk på beskeder og sæt påmindelser.

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

### Flere muligheder i eksisterende funktioner

Tilføjelser til tickets, giveaways, stemmerum, XP, fødselsdage, sikkerhedskopier, logs og statusvisninger.

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
/team modwatch status
/team modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/team modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/team modwatch exclude member:@TrustedMod

/team permaudit run                                                  # roles with dangerous permissions and who holds them
/team permaudit watch enabled:True                                   # alarm when a role or member gets one
/team permaudit trust role:@Admin
```

### Rapporter og invitationssporing

Medlemmer rapporterer beskeder til staben, og botten gemmer hvilken invitation der bragte hvert nyt medlem.

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

### Diagnose og fejlfinding

Find manglende rettigheder og ødelagte indstillinger, få fejlrapporter i en kanal og eksporter eller importer indstillingerne.

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
/admin config set path:music.allowed_hosts value:bandcamp.com,archive.org
/music cleardj
/music status
```

Tabsfrit: egne filer (FLAC, WAV, ALAC) og kilder med FLAC afspilles uændret. YouTube, SoundCloud og lignende sider tilbyder kun lyd med tab, og det kan ikke gøres tabsfrit bagefter. Discord sender stemme som Opus, botten bruger stemmekanalens bitrate. Ansvar: at downloade og afspille indhold kan bryde et websteds vilkår eller ophavsretten. Downloads er slået fra som standard, og modulet er slukket, indtil du aktiverer det. Den, der driver botten, er ansvarlig for det, der afspilles og gemmes.

### Opsætning og sundhedstjek

En guidet assistent sætter det vigtigste op med knapper og menuer: logkanal, velkomstkanal, staberoller, gulagen, en AutoMod-forudindstilling (løs, normal, streng), en serverskabelon (fællesskab, gaming, support) og sproget. /server health viser, hvad der er sat op, og hvad der mangler. Sproget ændrer de tekster, medlemmerne ser, som standardvelkomst, AutoMod-beskeder, verificering, tickets, klager, mod-mail og rollemenuer. Faste svar til administratorer er oversat, svar med navne og tal forbliver på engelsk.

```
/admin setup                                                         # buttons and menus, nothing is switched off by a template
/server health                                                        # what is set up, what is open, and the self-test
/admin language code:de
```

### Økonomi

En servervaluta med daglig belønning, arbejde, betalinger, rangliste og en butik, hvis varer kan give en rolle. Slå den til med modulet economy. Kommandoerne virker også med præfiks, for eksempel !economy daily.

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

### Rollemenuer, planlagte beskeder og feeds

Rollemenuer giver roller med knapper eller en rullemenu. Planlagte beskeder sendes én gang eller gentages hver time, dag eller uge. Feeds poster nye YouTube-videoer, Twitch-streams og RSS-indlæg. Til YouTube bruges kanal-ID'et (det starter med UC). Twitch kræver TWITCH_CLIENT_ID og TWITCH_CLIENT_SECRET i .env. Tider skrives som in 2h, 18:30 eller som dato med klokkeslæt, for eksempel 2026-12-24 18:00, i serverens tidszone. Den første kontrol af et feed husker kun det, der allerede findes.

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

### Aktivitet, massehandlinger og sagssøgning

Aktivitet tæller beskeder pr. kanal samt tilmeldinger og afgange pr. dag, aldrig indhold eller navne. Massehandlinger udelukker, smider ud eller sætter op til 25 brugere i timeout efter en bekræftelse. Sager kan søges efter bruger, type, navn, årsag, moderator og alder og kobles sammen, for eksempel en note til en udelukkelse.

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

### Anti-svindel og anti-krypto

Fjerner falske giveaways, som den typiske MrBeast-svindel, i tekst og billeder inden for millisekunder. Navne på direkte-listen fjernes med det samme i enhver stavemåde (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Ellers lægges ord fra listerne (navne, lokkemad, krypto, links, beløb) sammen, og beskeden fjernes ved tærskelværdien. Billeder læses med OCR, og et billede, der én gang er dømt som svindel, fjernes uden at blive læst igen. Billeder kræver tesseract, uden det kontrolleres kun tekst. En server om MrBeast kan fjerne navnet fra direkte-listen eller undtage kanaler med /automod exemptchannel. Prøv med /security antiscam test, før du stoler på det.

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

### Prøvetid, svarmgenkendelse, tidslinje og indlæring

Prøvetiden placerer nye medlemmer i en rolle. Indtil de har skrevet det indstillede antal almindelige beskeder, eller minutterne er gået, fjernes links, invitationer og filer med en kort besked. Raidbeskyttelsen genkender også en svarm: flere nye konti med samme navnemønster, samme profilbillede eller oprettet med få minutters mellemrum. Tidslinjen (/moderation case timeline) samler kontoens oprettelse, tilgang og invitation, prøvetid, sager og klager for en bruger i tidsrækkefølge. Beskeder gemmes aldrig og er derfor ikke med. /security block, /security unblock og /security blocklist styrer AutoMods blokliste med korte kommandoer. Moderatorer lærer anti-svindel-modulet noget med kontekstmenuen Mark as scam på en besked eller med en reaktion med emojien fra learn_emoji: beskeden slettes, og dens billeder og tekst fjernes derefter med det samme. Hver del slår du fra med sit modul eller sine indstillinger.

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

### Beskedbygger og opdateringer

Beskedbyggeren sender beskeder med flere embeds og linkknapper ud fra JSON. Den læser den JSON, som embed-generatorer som Embed Generator eksporterer, så du designer en besked dér og sender den med botten. Angiv JSON som tekst, som .json-fil eller som https-link, der peger direkte på JSON, for eksempel råfilen i et repository (links med omdirigering afvises). Kun linkknapper oprettes, knapper der kræver en interaktion springes over. Hvert link skal være http eller https, omtaler i teksten pinger aldrig, og Discords grænser gælder. /post message copy eksporterer en eksisterende besked som JSON, /post message edit ændrer en besked fra botten, og /post message preview viser resultatet kun for dig. Delingslinks fra webeditorer åbnes ikke, fordi deres format ikke er offentligt.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Hver 12. time tjekker botten GitHub-repositoryet i update.repo (sættes med scripts/set_repo_url.py) for en nyere version. Findes der en, får botens ejer en direkte besked med udgivelsesnoterne, og versionen hentes og kontrolleres: SHA-256-kontrolsum, sikre stier i arkivet og en version, der passer til tagget. Den installeres med /server debug update action:install eller af sig selv, hvis auto_install er slået til. Før installationen gemmes de erstattede filer i data/update, nye pakker installeres, og den nye kode importeres som test. Fejler noget, gendannes de gamle filer. Din .env, settings.json, data og music røres aldrig. Derefter genstarter botten sig selv. I Docker installeres intet på stedet, opdater i stedet billedet. En opdatering kører kode fra repositoryet, så peg den kun på et repository, du stoler på. Slå den fra med enabled sat til false.

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

### Drift

Botten gemmer sine data hvert par sekunder og opbevarer databasesikkerhedskopier i data/dbbackups, én før hver ændring af dataformatet og én om dagen. Musikkøen, fastgjorte beskeder og moderatortællere overlever en genstart. Store bots kan køre på flere shards. En heartbeat-fil og en valgfri statusside hjælper overvågningsværktøjer. Disse indstillinger sættes i settings.json:

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

Logs skrives til data/guardbot.log (med rotation, se log_max_mb og log_backups). Med log_format sat til json bliver hver linje et JSON-objekt med serveren og kommandoen. Hvis health_port er sat, leverer /metrics Prometheus-målinger (driftstid, latens, hukommelse, databasestørrelse, fejl, kommandobrug og -tid, arbejdsbaner). Der eksporteres kun tal, aldrig navne eller ID'er, og metrics_token kræver et bearer-token. Tungt arbejde (læse billeder, tegne kort, musikfiler, sikkerhedskopier) kører i baner med et fast antal tråde og en grænse (workers i settings.json). Når en bane er fuld, siger botten, at den er optaget, i stedet for at stable arbejde op. Hver databasebackup åbnes og kontrolleres lige efter, den er lavet. For at gendanne en, stop botten og kør:

```
python scripts/restore_db.py data/dbbackups/guardbot-YYYYMMDD-HHMMSS-auto.db
python scripts/restore_db.py BACKUPFILE --check          # only check a backup
```

Den nuværende database gemmes som en backup med navnet before-restore.

### Administration

Slå moduler og kommandoer til eller fra, skift præfiks, opret aliasser og begræns kommandoer til roller.

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

## Pladsholdere i beskeder

Disse pladsholdere erstattes i de tekster, du indstiller:

```
/community welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/community booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/community tempvoice setup     name                            {name}
/access jailsetup notice    text                            {staff}
```

## Konfiguration

Globale indstillinger angives i settings.json. Alt andet konfigureres pr. server med kommandoer som /admin module, /admin command, /admin perms, /admin alias og /admin config.

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

Hver enkelt indstilling kan læses og ændres med /admin config. Det er disse stier, du bruger mest:

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
    defaults/             default settings, one file per area (core, security, moderation, community) and base.py for modules and permissions
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature, in the folders security, moderation, server, community, tools
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
- Medlemmer kan eksportere og slette deres egne data med /info mydata. Administratorer bestemmer, hvor længe data fra medlemmer, der er gået, gemmes.
- [PRIVACY.md](../PRIVACY.md)

## Support

Fejl, idéer og forslag: skriv til mig på Discord, @justyyin, eller opret et issue på GitHub.

## Tak til

GuardBot er inspireret af [Embed Generator](https://github.com/merlinfuchs/embed-generator) af Merlin Fuchs (MIT-licens, hostet på message.style). Beskedbyggeren læser det samme JSON-format, så beskeder designet dér kan sendes med denne bot. Der er ingen kode fra det projekt med. Tak til forfatterne bag discord.py, aiohttp, Pillow, yt-dlp, mutagen og Tesseract.

## Licens

Udgivet under MIT-licensen. Se [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
