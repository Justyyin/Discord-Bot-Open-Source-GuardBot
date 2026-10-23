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
  - [Struktur, medlemmar och team](#struktur-medlemmar-och-team)
- [Kontrollpanel](#kontrollpanel)
  - [Ställ in kontrollpanelen](#ställ-in-kontrollpanelen)
  - [Kommandon, skills, AI och botprofil](#kommandon-skills-ai-och-botprofil)
  - [Säkerhet](#säkerhet-1)
  - [Kontrollpanel på en VPS](#kontrollpanel-på-en-vps)
- [Kommandon](#kommandon)
  - [Kommandogrupper](#kommandogrupper)
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
  - [Paneler](#paneler)
  - [Skills och AI](#skills-och-ai)
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
- Gulag-kanal: den som postar bedrägerilänkar eller bilder flyttas till en enda kanal med instruktioner för att säkra kontot. Moderatorer kan också använda /moderation jail och /moderation unjail.
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
- Ekonomi med butik, rollmenyer med knappar eller rullgardin, schemalagda meddelanden, YouTube-, Twitch- och RSS-flöden, aktivitetsstatistik och en guidad /admin setup. Meddelanden till medlemmar finns på 12 språk.

### Administration

- Varje modul och varje enskilt kommando kan slås på eller av per server.
- Eget prefix, kommandoalias och kommandon som kan döpas om.
- Säkerhetskopiering och återställning av roller och kanalstruktur.
- Schemalagda automatiska säkerhetskopior av roller, kanaler, emojis och webhooks, med ett återställningskommando som bara lägger till det som saknas.
- Kontrollpanel: ändra inställningarna för varje server i webbläsaren efter inloggning med Discord, bara för medlemmar som hanterar servern och bara medan boten är ansluten.
- Skills: egna kommandon, spel och automatiseringar av säkra byggstenar, valfritt skrivna av en AI med din egen nyckel (Anthropic, OpenAI, Kimi). Instrumentpanelen listar alla kommandon och redigerar skills, AI-inställningar och botprofilen.

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

### Struktur, medlemmar och team

Version 1.5 lägger till kommandon för att bygga och hålla en server i ordning, återställa medlemmar som kommer tillbaka och leda modereringsteamet. Varje del har en modulströmbrytare (`/admin module`), egna inställningar och en plats i instrumentpanelen.

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

- Med `/structure` skapas, klonas, byts namn på och sorteras kanaler och kategorier, och behörigheter kopieras från en annan kanal. Inaktiva kanaler rapporteras eller flyttas till en arkivkategori (`/structure archive`). Roller kan ges tidsbegränsat och sparas som mallar; en mall ger aldrig en behörighet som den som använder den saknar.
- `/structure rules` publicerar reglerna med en godkänn-knapp och ett versionsnummer. Efter `post new_version:True` får medlemmar som inte godkänt den nya versionen en enda påminnelse via direktmeddelande.
- `/members stickyroles` ger tillbaka roller och återställer timeout eller mute när en medlem kommer tillbaka. `/members nickname` tar bort tecken som lyfter namnet överst i listan, kontrollerar förbjudna ord i smeknamn och användarnamn och byter namn på överträdare. Bevakningslistan är tyst: teamet larmas vid första meddelandet från en listad användare.
- Fyra-ögon-godkännande (`/security approval`) kör bannlysningar, kickar, timeouts och massåtgärder först när en andra moderator godkänner. `/moderation case undo` återtar ett ärende, även de åtgärder det gav upphov till (till exempel en mute och bannlysningen som följde). Varningar kan gå ut efter ett antal dagar (`/moderation escalation expiry`).
- `/admin history` visar vem som ändrade vilken inställning och när, och återställer ett avsnitt. Personens namn är en gissning utifrån de senaste kommandona och ändringarna i instrumentpanelen på servern. `/admin history copy` kopierar avsnitt till en annan server som du får hantera med boten; den börjar som en provkörning. `/admin exceptions` utesluter kanaler och roller från AutoMod-regler och Anti-Scam. `/admin dashaccess` ger roller skrivskyddad åtkomst eller moderatoråtkomst till instrumentpanelen.
- `/team` visar varje moderators arbete (ärenden, tickets, rapporter, svarstid, inaktiva medlemmar), skickar en veckorapport (dag och timme i UTC), låter moderatorer anmäla frånvaro med `/team duty away` så att ticket och omnämnanden går till andra, och sköter personalansökningar med formulär och omröstning i teamet.
- Discord kan inte dölja kommandon i en grupp för enskilda medlemmar. Boten kontrollerar ändå varje anrop. Siffrorna i teamstatistiken räknas från dagen för uppdateringen; äldre åtgärder saknas.

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

### Kommandon, skills, AI och botprofil

Instrumentpanelen har fem sidor till: Panels (se avsnittet Paneler) och följande fyra. Kommandon listar varje snedstreckskommando, prefixkommando och snabbmeny med modul, behörighet som krävs och om det är på; administratörer slår på eller av dem, tillåter eller nekar roller och ger prefixkommandon korta namn. Prefixet ändras på samma sida. Skills visar alla skills och redigerar dem som JSON med samma kontroller som kommandona. AI anger modell och gränser och sparar en nyckel (endast skrivning, den skickas aldrig tillbaka till sidan). Botprofil ändrar botens namn, bild, banner och beskrivning på den här servern; ägaren till botens applikation, eller ett ID i `owner_ids` i settings.json, kan också ändra dem överallt. Discord begränsar hur ofta namn och bild får ändras. Varje ändring skrivs i granskningsloggen.

Varje modul visas som ett plugin: sidan Plugins visar dem som kort per kategori, och varje plugin har en egen sida med reglaget Aktiv, sina inställningar i rutor som fälls ut och ihop och sina kommandon med reglage och rollredigerare. Vänsterfältet listar plugins per kategori med en punkt som visar om de är på. Instrumentpanelen har en mörk design.

Instrumentpanelen kan visas på botens alla 12 språk. Välj språk uppe till höger eller på inloggningssidan; valet sparas i webbläsaren och ändrar inte serverns språk. Instrumentpanelens texter är maskinöversatta.

Varje pluginsida förklarar vad pluginet gör, listar alla dess funktioner med eget reglage och en kort förklaring och visar övriga inställningar i rutor nedanför. På sidan Plugins och i översikten kan varje plugin slås på eller av direkt. I Inställningar ändrar rutan Instrumentpanelens utseende accentfärg, bakgrund, rutor och text, sätter en bakgrundsbild (mörkare och suddigare efter smak) och lägger till egna menyer och flikar i sidofältet: en flik kan samla valda plugins, öppna en sida, länka till en https-adress eller visa en anteckning. Utseendet sparas per server och syns för alla som öppnar dess instrumentpanel. Sidfoten visar upphovsrätten och länkar till Discord och GitHub; för att visa de officiella logotyperna där lägger du discord.svg och github.svg från varumärkessidorna för Discord och GitHub i guardbot/web/brand/.

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

<!-- groups -->
### Kommandogrupper

För att spara platser för snedstreckskommandon (Discord tillåter 100 kommandon på översta nivån per bot) är kommandon som hör ihop grupperade. Skriv först gruppen och sedan kommandot, till exempel `/moderation ban`. Textkommandon med prefix, till exempel `!ban`, påverkas inte. Behörigheter, alias och modulbrytare använder fortfarande det enkla kommandonamnet.

| Grupp | Innehåller |
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

### Moderering

Varningar, mute, kick och bann fungerar som snedstreckskommandon och med prefix, till exempel `!warn @User spam`. Varje åtgärd skapar ett numrerat ärende.

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

Medlemmar med kapat konto flyttas till en enda kanal med säkerhetsanvisningar. Vid frisläppning får de tillbaka sina gamla roller.

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

Alla som hamnar i gulag, via kommando, AutoMod, anti-scam, när de går med igen eller för att någon gav rollen för hand, får meddelandet Account Security Required med en omnämning. Så länge någon är i gulag ligger en Account Recovery Reminder längst ned i kanalen och förnyas var 10:e minut. En medlem i gulag som skriver prefixet och frisläppningsordet (till exempel `!unban`) i gulag-kanalen skapar en begäran om frisläppning med knapparna Release och Keep för personalen; boten släpper aldrig ut någon på egen hand. `/access jailsetup reminder` slår på eller av varje del och ställer in intervall och ord.

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

Bevakar granskningsloggen och reagerar när någon förstör servern. Serverägaren får ett direktmeddelande.

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

### Verifiering

Nya medlemmar ser bara verifieringskanalen tills de trycker på knappen eller löser captchan.

```
/access verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/access verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/access verify panel channel:#verify                      # post the button again
/access verify apply                                      # apply the channel permissions again
/access verify member member:@User                        # verify someone manually
/access verify off
```

### Loggning

Välj en kanal per kategori, eller en huvudkanal för allt.

```
/server log set category:main channel:#logs               # fallback for every category
/server log set category:messages channel:#log-messages
/server log set category:moderation channel:#log-moderation
/server log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/server log sent enabled:False                            # stop logging every sent message
/server log show
```

### Välkomst, avsked och boosters

Meddelanden, automatiska roller och belöningar för serverns boosters.

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

Medlemmar öppnar privata kanaler med en knapp. När ärendet stängs skickas en utskrift.

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

### Omröstningar och giveaways

Knappar för att rösta och delta. Tider accepterar värden som 30m, 2h och 1d.

```
/engage poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/engage poll end poll_id:3
/engage poll list

/engage giveaway start prize:Nitro duration:2d winners:2 role:@Member
/engage giveaway end giveaway_id:1
/engage giveaway reroll giveaway_id:1
/engage giveaway list
```

### Förslag och starboard

Medlemmar skickar förslag som teamet kan godkänna eller avslå, och populära meddelanden lyfts fram.

```
/suggestion setup set channel:#suggestions review_role:@Staff
/support suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/engage starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/engage starboard ignore channel:#spam
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

/info rank                                              # also: !rank, shows a rank card image
/info rank user:@User
/info leaderboard
```

### Reaktionsroller och aviseringar

Ge roller för reaktioner med valfri emoji och låt medlemmar välja sina aviseringsämnen.

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
/community tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Säkerhetskopiering och återställning

Kopior innehåller roller, kanaler, emojis, webhooks och medlemmarnas roller. Återställning lägger bara till det som saknas.

```
/server backup create name:before-update
/server backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/server backup list
/server backup download name:before-update
/server backup restore name:before-update member_roles:True   # only adds what is missing
/server backup delete name:before-update
```

### Data och integritet

Medlemmar kan exportera och radera sina data. Administratörer styr hur länge data sparas.

```
/info mydata export                                     # members download their own data
/info mydata delete confirm:True                        # members delete their XP and birthday

/server privacy retention days:90                         # delete data of members who left after 90 days
/server privacy export user_id:123456789012345678
/server privacy delete user_id:123456789012345678 cases:True
```

### Moderatorverktyg

Städa kanaler, hantera roller och för privata anteckningar. Varje åtgärd loggas.

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

Slå upp användare, servern, roller och boten.

```
/info userinfo user:@User
/server serverinfo
/server roleinfo role:@Moderator
/info avatar user:@User
/help command:ban                                  # explains one command
/info ping
/info botinfo
```

### Meddelanden, taggar och påminnelser

Skriv i botens namn, skapa egna kommandon, svara automatiskt på meddelanden och sätt påminnelser.

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

### Fler alternativ för befintliga funktioner

Tillägg för ärenden, giveaways, röstrum, XP, födelsedagar, säkerhetskopior, loggar och statusvyer.

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
/team modwatch status
/team modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/team modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/team modwatch exclude member:@TrustedMod

/team permaudit run                                                  # roles with dangerous permissions and who holds them
/team permaudit watch enabled:True                                   # alarm when a role or member gets one
/team permaudit trust role:@Admin
```

### Rapporter och inbjudningsspårning

Medlemmar rapporterar meddelanden till personalen och boten sparar vilken inbjudan som tog in varje ny medlem.

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

### Diagnos och felsökning

Hitta saknade behörigheter och trasiga inställningar, få felrapporter i en kanal och exportera eller importera inställningarna.

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

Förlustfritt: egna filer (FLAC, WAV, ALAC) och källor som erbjuder FLAC spelas upp oförändrade. YouTube, SoundCloud och liknande sajter erbjuder bara ljud med förlust, och det kan inte göras förlustfritt i efterhand. Discord överför röst som Opus, boten använder röstkanalens bitrate. Ansvar: att ladda ner och spela upp innehåll kan strida mot en webbplats villkor eller upphovsrätten. Nedladdningar är avstängda som standard och modulen är av tills du slår på den. Den som driver boten ansvarar för det som spelas och sparas.

Källor: länkar och sökningar från YouTube och SoundCloud spelas direkt. Länkar från Spotify, Apple Music och Tidal tas också emot, men de tjänsterna lämnar inte ut sitt ljud: boten läser titel och artist från den offentliga sidan och spelar samma låt från sökkällan (YouTube eller SoundCloud, ställs in med /music sources). Album och spellistor från Spotify och Apple Music läses från deras offentliga sidor; album och spellistor från Tidal kräver en gratis utvecklarnyckel från developer.tidal.com i .env (TIDAL_CLIENT_ID och TIDAL_CLIENT_SECRET). Filer i din musikmapp spelas som de är. Sparade spellistor kan blanda alla källor, och /music stay håller boten i en röstkanal dygnet runt och spelar en spellista i repris, även efter en omstart.

Guard Music, den andra boten: musiken kan köras på ett eget botkonto, så att den kan stanna i en röstkanal hela tiden utan att påverka modereringen.

1. Skapa en andra applikation i Discord Developer Portal, döp den till Guard Music och kopiera token för dess bot.
2. Skriv token i .env som MUSIC_TOKEN och sätt music_bot.enabled till true i settings.json.
3. Starta om GuardBot. Guard Music startar i samma process, använder samma inställningar och data, och musikkommandona flyttar till den.
4. Öppna sidan Musik i instrumentpanelen och lägg till Guard Music på servern med knappen där. Utan MUSIC_TOKEN stannar musiken i GuardBot.

Användning på egen risk: strömning från YouTube och andra tjänster kan bryta mot deras användarvillkor, och upphovsrätt gäller för det som spelas. Inget laddas ner från Spotify, Apple Music eller Tidal och inget skydd kringgås. Den som driver boten ansvarar för det som spelas. Instrumentpanelens sida Musik visar spelaren, kön, spellistorna, 24/7-läget, källorna och den här guiden.

### Installation och hälsokontroll

En guidad assistent ställer in det viktigaste med knappar och menyer: loggkanal, välkomstkanal, personalroller, gulagen, en AutoMod-förinställning (lös, normal, sträng), en servermall (community, spel, support) och språket. /server health visar vad som är klart och vad som återstår. Språket ändrar de texter som medlemmarna ser, som standardvälkomst, AutoMod-meddelanden, verifiering, tickets, överklaganden, mod-mail och rollmenyer. Fasta svar till administratörer är översatta, svar med namn och siffror förblir på engelska.

```
/admin setup                                                         # buttons and menus, nothing is switched off by a template
/server health                                                        # what is set up, what is open, and the self-test
/admin language code:de
```

### Ekonomi

En servervaluta med daglig belöning, arbete, betalningar, topplista och en butik vars varor kan ge en roll. Slå på den med modulen economy. Kommandona fungerar också med prefix, till exempel !economy daily.

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

### Rollmenyer, schemalagda meddelanden och flöden

Rollmenyer ger roller med knappar eller en rullgardinsmeny. Schemalagda meddelanden skickas en gång eller upprepas varje timme, dag eller vecka. Flöden postar nya YouTube-videor, Twitch-sändningar och RSS-inlägg. För YouTube används kanal-ID:t (det börjar med UC). Twitch kräver TWITCH_CLIENT_ID och TWITCH_CLIENT_SECRET i .env. Tider skrivs som in 2h, 18:30 eller som datum med klockslag, till exempel 2026-12-24 18:00, i serverns tidszon. Den första kontrollen av ett flöde minns bara det som redan finns.

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

### Aktivitet, massåtgärder och ärendesökning

Aktivitet räknar meddelanden per kanal samt inträden och utträden per dag, aldrig innehåll eller namn. Massåtgärder bannlyser, sparkar eller tystar upp till 25 användare efter en bekräftelse. Ärenden kan sökas efter användare, typ, namn, orsak, moderator och ålder och länkas till varandra, till exempel en anteckning till en bannlysning.

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

### Anti-bedrägeri och anti-krypto

Tar bort falska giveaways, som den typiska MrBeast-bluffen, i text och bilder inom millisekunder. Namn på direktlistan tas bort direkt i alla stavningar (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Annars läggs ord från listorna (namn, bete, krypto, länkar, belopp) ihop och meddelandet tas bort vid tröskelvärdet. Bilder läses med OCR, och en bild som en gång bedömts som bluff tas bort utan att läsas igen. För bilder krävs tesseract, utan det kontrolleras bara text. En server om MrBeast kan ta bort namnet från direktlistan eller undanta kanaler med /automod exemptchannel. Testa med /security antiscam test innan du litar på det.

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

### Prövotid, svärmigenkänning, tidslinje och inlärning

Prövotiden placerar nya medlemmar i en roll. Tills de har skrivit det inställda antalet vanliga meddelanden eller minuterna har gått tas länkar, inbjudningar och filer bort med ett kort meddelande. Raidskyddet känner också igen en svärm: flera nya konton med samma namnmönster, samma profilbild eller skapade med några minuters mellanrum. Tidslinjen (/moderation case timeline) sammanför kontots skapande, inträde och inbjudan, prövotid, ärenden och överklaganden för en användare i tidsordning. Meddelanden sparas aldrig och ingår därför inte. /security block, /security unblock och /security blocklist hanterar AutoMods blocklista med korta kommandon. Moderatorer lär anti-bedrägerimodulen med snabbmenyvalet Mark as scam på ett meddelande eller med en reaktion med emojin från learn_emoji: meddelandet raderas och dess bilder och text tas därefter bort direkt. Varje del stänger du av med sin modul eller sina inställningar.

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

### Paneler

Paneler är inlägg som ett välkomstinlägg, regler, ett rollval, aviseringsknappar eller en verifiering, med bannerbilder, textrutor och knappar. De byggs med `/panel` eller i instrumentpanelen på sidan Panels. Bilder laddas upp där eller som alternativ i kommandot och sparas av boten i `data/panels`, så att de fortsätter att fungera.

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

Mallar: empty, welcome, rules, roles, notifications och verify; texterna är på serverns språk och kan ändras. `/panel section` öppnar ett formulär för rubrik, text och sidfot. Varje avsnitt blir ett meddelande: bannern ovanför rutan, den stora bilden i den, den lilla bilden uppe till höger. Knapparna ligger under det sista avsnittet, fem per rad. En rollknapp ger rollen eller tar bort den; med `single` tas panelens andra roller bort. Knappen verify startar verifieringen i verifieringsmodulen (`/access verify setup` väljer knapp, captcha eller räkneuppgift). Texter kan använda `{server}` och `{count}`. `/panel update` ändrar de postade meddelandena efter en redigering. Gränser per server: 25 paneler, 5 avsnitt och 20 knappar per panel, 40 bilder på högst 8 MB. Boten erbjuder bara roller som ligger under dess egen högsta roll och saknar farliga behörigheter.

### Skills och AI

Skills är kommandon, spel och automatiseringar som en server bygger själv av säkra byggstenar. De behöver ingen AI och kan aldrig köra kod. En AI är valfri: med din egen nyckel skriver den en skill utifrån en beskrivning och ger en andra åsikt i anti-scam-kontrollen.

Skills utan AI:

- `/support skill create kind:command name:hello` öppnar en ruta med ett litet exempel som du ändrar. `/support skill edit`, `show`, `import`, `enable`, `disable`, `delete`, `list` och `stats` hanterar dem. Alla använder en skill med `/support skill run` eller med prefixet, till exempel `!hello`. `/support skill panel` postar knappar som kör skills.
- Typer: kommando (en lista med åtgärder), spel (tärning, val, spelautomat, sten sax påse, frågesport) och automatisering (startar när en medlem går med eller lämnar, när ett meddelande innehåller ord eller när en knapp trycks).
- Åtgärder: svara, skicka till en kanal, direktmeddelande, logga, ge eller ta bort en roll, ändra en räknare, ge mynt, välja slumpmässigt. En åtgärd kan ha villkor: har en roll, chans, en räknare jämförd med ett tal.
- Texter kan använda `{user}`, `{user_name}`, `{server}`, `{channel}`, `{count}`, `{arg1}`, `{arg2}`, `{var:name}`, `{uvar:name}` och `{random:1-6}`.
- Gränser: 50 skills per server, 10 åtgärder per skill, 3 rolländringar och 4 meddelanden per skill. Boten delar bara ut roller som ligger under dess egen högsta roll och saknar farliga behörigheter. En skill som ger mynt behöver en väntetid på minst 60 sekunder. Namn på botkommandon, alias och taggar kan inte användas.
- Skills lagras som JSON och ingår i exporten av inställningar. Okända fält avvisas, så en skill från var som helst kan bara göra det byggstenarna tillåter.

Exempel, ett kommando som ger en roll och räknar användningar (byt ut roll-ID:t):

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

AI-anslutning (valfritt):

- `/support ai setup provider:kimi agree:true` öppnar en privat ruta för din API-nyckel. Leverantörer är Anthropic, OpenAI och Kimi (Moonshot). En modell föreslås och kan ändras i samma kommando eller i instrumentpanelen; modellnamn ändras hos leverantörerna, så kontrollera deras dokumentation. Du betalar din leverantör.
- `/support ai make wish:...` ber AI:n om en skill, kontrollerar svaret lika strikt som en importerad skill och visar en förhandsvisning. Inget sparas innan du trycker på Spara.
- `/support ai status`, `limits` (förfrågningar per dag, sekunder mellan förfrågningar per person) och `remove` kompletterar uppsättningen. Nyckeln lagras krypterad, med filen `data/ai.secret` som hemlighet. Spara den filen tillsammans med dina säkerhetskopior; utan den går en lagrad nyckel inte att läsa och måste anges på nytt. Nyckeln visas, loggas eller exporteras aldrig. Leverantören kan bara ändras tillsammans med en ny nyckel, så en nyckel går aldrig till en annan leverantör.
- Det som skickas: önskemålet från `/support ai make` och, vid andra åsikten, texten i ett misstänkt meddelande. Inget annat, och bara medan modulen `ai` är på. Se [PRIVACY.md](../PRIVACY.md).

Inlärning i anti-scam:

- Det inlärda filtret (`/security antiscam set learned:true`) är en liten klassificerare per server. Moderatorer tränar det med snabbmenyposterna "Mark as scam" och "Not a scam". Det lagrar bara korta hashar av ord, aldrig texten, agerar först efter att ha sett 8 scam- och 30 vanliga exempel, och då bara över 95 procent. Med `ham_sampling` lär det sig också av vart tionde vanligt meddelande.
- Liknande bilder (`similar`, på som standard) jämför ett bildfingeravtryck med kända scam-bilder, så att även en omsparad eller förminskad kopia hittas. Det fungerar utan Tesseract.
- AI:ns andra åsikt (`/support ai limits second_opinion:true`): för fall strax under tröskeln eller som det inlärda filtret tycker är misstänkta tillfrågas AI:n. Ett meddelande tas bara bort när AI:n svarar scam med minst 80 procents säkerhet, och dess svar kan inte utlösa något annat.

### Meddelandebyggare och uppdateringar

Meddelandebyggaren postar meddelanden med flera embeds och länkknappar från JSON. Den läser den JSON som embed-generatorer som Embed Generator exporterar, så du utformar ett meddelande där och postar det med boten. Ange JSON som text, som .json-fil eller som https-länk som pekar direkt på JSON, till exempel råfilen i ett arkiv (länkar med omdirigering avvisas). Bara länkknappar skapas, knappar som kräver en interaktion hoppas över. Varje länk måste vara http eller https, omnämnanden i texten pingar aldrig och Discords gränser gäller. /post message copy exporterar ett befintligt meddelande som JSON, /post message edit ändrar ett meddelande från boten och /post message preview visar resultatet bara för dig. Delningslänkar från webbredigerare öppnas inte, eftersom deras format inte är offentligt.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Var 12:e timme kontrollerar boten GitHub-arkivet i update.repo (sätts med scripts/set_repo_url.py) efter en nyare version. Finns det en får botens ägare ett direktmeddelande med versionsanteckningarna, och versionen laddas ned och kontrolleras: SHA-256-kontrollsumma, säkra sökvägar i arkivet och en version som stämmer med taggen. Den installeras med /server debug update action:install, eller av sig själv om auto_install är på. Före installationen sparas de ersatta filerna i data/update, nya paket installeras och den nya koden importeras som test. Om något misslyckas återställs de gamla filerna. Din .env, settings.json, data och music rörs aldrig. Sedan startar boten om sig själv. I Docker installeras inget på plats, uppdatera avbilden i stället. En uppdatering kör kod från arkivet, så peka den bara mot ett arkiv du litar på. Stäng av den med enabled satt till false.

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

Boten sparar sina data var några sekunder och lagrar databassäkerhetskopior i data/dbbackups, en före varje ändring av dataformatet och en per dag. Musikkön, fästa meddelanden och moderatorräknare överlever en omstart. Stora botar kan köras på flera shards. En heartbeat-fil och en valfri statussida hjälper övervakningsverktyg. De här alternativen anges i settings.json:

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

Loggar skrivs till data/guardbot.log (roterande, se log_max_mb och log_backups). Med log_format satt till json blir varje rad ett JSON-objekt med servern och kommandot. Om health_port är satt levererar /metrics Prometheus-mått (drifttid, latens, minne, databasstorlek, fel, kommandoanvändning och -tider, arbetsfiler). Bara siffror exporteras, aldrig namn eller ID:n, och metrics_token kräver en bearer-token. Tungt arbete (läsa bilder, rita kort, musikfiler, säkerhetskopior) körs i filer med fast antal trådar och en gräns (workers i settings.json). När en fil är full säger boten att den är upptagen i stället för att stapla upp arbete. Varje databasbackup öppnas och kontrolleras direkt efter att den skapats. För att återställa en, stoppa boten och kör:

```
python scripts/restore_db.py data/dbbackups/guardbot-YYYYMMDD-HHMMSS-auto.db
python scripts/restore_db.py BACKUPFILE --check          # only check a backup
```

Den nuvarande databasen sparas som en backup med namnet before-restore.

### Administration

Slå på eller av moduler och kommandon, byt prefix, skapa alias och begränsa kommandon till roller.

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

## Platshållare i meddelanden

De här platshållarna ersätts i texterna du ställer in:

```
/community welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/community booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/community tempvoice setup     name                            {name}
/access jailsetup notice    text                            {staff}
```

## Konfiguration

Globala alternativ anges i settings.json. Allt annat konfigureras per server med kommandon som /admin module, /admin command, /admin perms, /admin alias och /admin config.

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

Varje inställning kan läsas och ändras med /admin config. Det här är de sökvägar du använder oftast:

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
    defaults/             default settings, one file per area (core, security, moderation, community) and base.py for modules and permissions
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature, in the folders security, moderation, server, community, tools
    skills.py             skillmotor: kontrollerar och kör skills
    ai.py                 AI-leverantörer, krypterade nycklar, gränser
    learner.py, imgsim.py inlärt anti-scam-filter, bildfingeravtryck
    dashboard_manage.py   panelsidor för kommandon, skills, AI och profil
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
- Medlemmar kan exportera och radera sina egna data med /info mydata. Administratörer bestämmer hur länge data från medlemmar som lämnat sparas.
- AI-funktionerna är av tills du lägger till din egen nyckel. Därefter skickas bara texten från `/support ai make` och, vid andra åsikten, misstänkta meddelanden till den valda leverantören.
- [PRIVACY.md](../PRIVACY.md)

## Support

Buggar, idéer och förslag: skriv till mig på Discord, @justyyin, eller skapa ett issue på GitHub.

## Tack till

GuardBot är inspirerad av [Embed Generator](https://github.com/merlinfuchs/embed-generator) av Merlin Fuchs (MIT-licens, värd på message.style). Meddelandebyggaren läser samma JSON-format, så meddelanden som utformats där kan postas med den här boten. Ingen kod från det projektet ingår. Tack till upphovspersonerna bakom discord.py, aiohttp, Pillow, yt-dlp, mutagen och Tesseract.

## Licens

Utgiven under MIT-licensen. Se [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
