# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | **Français** | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Bot Discord auto-hébergé pour la modération, la sécurité et la communauté. Open source, gratuit, et vos données restent sur votre propre machine.

> Bêta : GuardBot et son tableau de bord sont en phase bêta. Ils n'ont pas été testés à fond, surtout pas sur de grands serveurs ni face à toutes les situations de Discord. Attendez-vous à des bugs, sauvegardez le dossier data et signalez les problèmes. Utilisation à vos risques.

<!-- toc -->

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
  - [Sécurité](#sécurité)
  - [Modération](#modération)
  - [Journalisation](#journalisation)
  - [Communauté](#communauté)
  - [Administration](#administration)
- [État du projet](#état-du-projet)
- [Prérequis](#prérequis)
- [Démarrage rapide](#démarrage-rapide)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Scripts de démarrage et démarrage automatique](#scripts-de-démarrage-et-démarrage-automatique)
  - [Mise à jour](#mise-à-jour)
- [Permissions du bot](#permissions-du-bot)
- [Premiers pas sur Discord](#premiers-pas-sur-discord)
- [Tableau de bord](#tableau-de-bord)
  - [Configurer le tableau de bord](#configurer-le-tableau-de-bord)
  - [Sécurité](#sécurité-1)
  - [Tableau de bord sur un VPS](#tableau-de-bord-sur-un-vps)
- [Commandes](#commandes)
  - [Modération](#modération-1)
  - [Goulag (jail)](#goulag-jail)
  - [Modération automatique](#modération-automatique)
  - [Protection anti-raid et verrouillage](#protection-anti-raid-et-verrouillage)
  - [Anti-nuke](#anti-nuke)
  - [Vérification](#vérification)
  - [Journalisation](#journalisation-1)
  - [Bienvenue, au revoir et boosters](#bienvenue-au-revoir-et-boosters)
  - [Tickets](#tickets)
  - [Sondages et concours](#sondages-et-concours)
  - [Suggestions et starboard](#suggestions-et-starboard)
  - [XP et niveaux](#xp-et-niveaux)
  - [Rôles par réaction et notifications](#rôles-par-réaction-et-notifications)
  - [Anniversaires](#anniversaires)
  - [Salons vocaux temporaires](#salons-vocaux-temporaires)
  - [Sauvegarde et restauration](#sauvegarde-et-restauration)
  - [Données et confidentialité](#données-et-confidentialité)
  - [Outils de modération](#outils-de-modération)
  - [Informations](#informations)
  - [Annonces, tags et rappels](#annonces-tags-et-rappels)
  - [Mod-mail et demandes de débannissement](#mod-mail-et-demandes-de-débannissement)
  - [Salon de comptage, messages épinglés et statistiques](#salon-de-comptage-messages-épinglés-et-statistiques)
  - [Autres options des fonctions existantes](#autres-options-des-fonctions-existantes)
  - [Autres outils AutoMod](#autres-outils-automod)
  - [Limites des modérateurs et audit des permissions](#limites-des-modérateurs-et-audit-des-permissions)
  - [Signalements et suivi des invitations](#signalements-et-suivi-des-invitations)
  - [Diagnostic et débogage](#diagnostic-et-débogage)
  - [Musique](#musique)
  - [Configuration et état de santé](#configuration-et-état-de-santé)
  - [Économie](#économie)
  - [Menus de rôles, messages programmés et flux](#menus-de-rôles-messages-programmés-et-flux)
  - [Activité, actions groupées et recherche de cas](#activité-actions-groupées-et-recherche-de-cas)
  - [Anti-arnaque et anti-crypto](#anti-arnaque-et-anti-crypto)
  - [Période d'essai, détection d'essaim, chronologie et apprentissage](#période-dessai-détection-dessaim-chronologie-et-apprentissage)
  - [Créateur de messages et mises à jour](#créateur-de-messages-et-mises-à-jour)
  - [Exploitation](#exploitation)
  - [Administration](#administration-1)
- [Variables dans les messages](#variables-dans-les-messages)
- [Configuration](#configuration)
- [Données et stockage](#données-et-stockage)
- [Structure du dépôt](#structure-du-dépôt)
- [Traductions](#traductions)
- [Feuille de route](#feuille-de-route)
- [Confidentialité et sécurité](#confidentialité-et-sécurité)
- [Assistance](#assistance)
- [Crédits](#crédits)
- [Licence](#licence)

<!-- tocstop -->

## À propos

GuardBot regroupe des fonctions que beaucoup de serveurs paient chez des bots hébergés : modération, journalisation, anti-raid, anti-nuke, tickets, niveaux et plus encore. Vous l'exécutez vous-même, sur votre ordinateur ou sur un petit VPS.

Les bots hébergés stockent les données du serveur, les identifiants des membres et parfois des adresses e-mail chez un tiers. Quand vous hébergez le bot vous-même, ces données ne quittent jamais votre machine. GuardBot veut montrer que n'importe qui peut faire fonctionner un bot complet sans abonnement.

## Fonctionnalités

### Sécurité

- Modération automatique : filtre de mots, filtre de majuscules, spam de mentions, liens d'invitation, domaines de phishing, données personnelles, doxxing et menaces. Toutes les listes sont modifiables.
- Anti-raid avec détection des vagues d'arrivées et verrouillage de tout le serveur.
- Anti-nuke : limites pour les suppressions et bannissements en masse, réaction automatique et message privé au propriétaire du serveur.
- Salon goulag : les membres qui publient des liens ou images d'arnaque sont déplacés dans un seul salon avec les étapes pour sécuriser leur compte. Les modérateurs peuvent aussi utiliser /jail et /unjail.
- Vérification par bouton ou captcha, avec retrait automatique des membres qui ne se vérifient pas à temps.
- L'anti-nuke surveille aussi l'attribution de permissions, les nouveaux webhooks, les bots ajoutés et les changements de nom du serveur.
- Anti-arnaque : les faux concours et les arnaques crypto sont supprimés dans le texte et les images en quelques millisecondes, y compris l'arnaque MrBeast sous toutes ses orthographes.

### Modération

- Warn, mute, kick, ban et jail avec un historique filtrable par mention, ID utilisateur ou type.
- Escalade automatique, par exemple trois avertissements entraînent une exclusion temporaire.
- Choix des rôles ou utilisateurs autorisés pour chaque commande de modération.

### Journalisation

- Messages envoyés, modifiés et supprimés, y compris images, GIF et URL, avec des salons de logs séparés.
- Changements de rôles, de pseudos, bannissements, vocal, salons et rôles du serveur.

### Communauté

- Messages de bienvenue et d'au revoir, rôles automatiques et récompenses pour les boosters.
- Tickets, sondages, concours et suggestions.
- Rôles par réaction avec n'importe quel emoji et thèmes de notification que les membres activent ou désactivent.
- XP et niveaux de 1 à 100 pour le chat et le vocal, rôles de niveau et anniversaires.
- Starboard et salons vocaux temporaires.
- Jail avec durée, sondages à choix multiples, cartes de rang en image et boosts d'XP par rôle.
- Économie avec boutique, menus de rôles avec boutons ou liste déroulante, messages programmés, flux YouTube, Twitch et RSS, statistiques d'activité et un /setup guidé. Les messages aux membres existent en 12 langues.

### Administration

- Chaque module et chaque commande peut être activé ou désactivé par serveur.
- Préfixe personnalisé, alias de commandes et commandes renommables.
- Sauvegarde et restauration des rôles et de la structure des salons.
- Sauvegardes automatiques planifiées des rôles, salons, emojis et webhooks, avec une commande de restauration qui n'ajoute que ce qui manque.
- Tableau de bord : modifier les réglages de chaque serveur dans le navigateur après une connexion Discord, uniquement pour les membres qui gèrent le serveur et seulement tant que le bot est connecté.

## État du projet

GuardBot est jeune et n'a pas encore été utilisé sur de grands serveurs. Les tests automatiques (`python -m unittest`) couvrent le stockage, la détection des données personnelles, le calcul des niveaux, l'enregistrement des commandes, les contrôles de permissions et les liens de la documentation. Tout ce qui nécessite un vrai serveur Discord, comme le verrouillage, la restauration de sauvegarde, la vérification, l'anti-nuke et le goulag, n'est pas couvert. Essayez ces fonctions d'abord sur un serveur de test avant de vous y fier. Les traductions de la documentation n'ont pas été relues par des locuteurs natifs, les corrections sont les bienvenues.

## Prérequis

- Python 3.11 ou plus récent
- Une application Discord avec un jeton de bot
- Un ordinateur ou un VPS toujours en ligne
- ffmpeg (seulement pour le module musique)
- tesseract-ocr (facultatif, seulement pour lire le texte des images)

## Démarrage rapide

Choisissez votre système. Chaque variante nécessite Python 3.11 ou plus récent et le jeton de votre bot. Le guide détaillé étape par étape est dans [GUIDE.md](GUIDE.md).

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

### Scripts de démarrage et démarrage automatique

Les scripts de démarrage créent l'environnement virtuel, installent les paquets et lancent le bot. Au premier lancement, ils créent le fichier .env et s'arrêtent pour que vous puissiez saisir le jeton. Relancez-les ensuite.

```bash
./start.sh
```

```bat
start.bat
```

Pour que le bot continue de tourner après un redémarrage de l'ordinateur, utilisez un service. Linux (systemd) et macOS (launchd) :

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

Sous Windows, créez une tâche dans le Planificateur de tâches qui lance start.bat à l'ouverture de session, ou utilisez un outil de service comme NSSM. Pour Docker, voir [GUIDE.md](GUIDE.md).

### Mise à jour

Arrêtez le bot, exécutez ces commandes et relancez-le. Vos données dans le dossier data restent intactes, et le bot fait une sauvegarde de la base avant chaque changement de format.

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

## Permissions du bot

Le plus simple est la permission Administrateur. Si vous préférez des droits minimaux, accordez ceux-ci et activez les intents Server Members et Message Content dans le Developer Portal :

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

## Premiers pas sur Discord

Une configuration de départ raisonnable. Exécutez ces commandes sur votre serveur et remplacez les salons et les rôles par les vôtres :

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

## Tableau de bord

Le tableau de bord est une page web qui s'exécute dans le bot. Après connexion avec Discord, vous modifiez les réglages de vos serveurs avec des interrupteurs, des menus et des champs au lieu de commandes : modules, salons, rôles, seuils, textes, préfixe et langue. Il affiche aussi les derniers cas de modération et exporte et importe les réglages. Il fonctionne de la même façon sur votre ordinateur et sur un VPS, et reste désactivé tant que vous ne l'activez pas.

### Configurer le tableau de bord

1. Ouvrez votre application dans le Developer Portal, allez dans OAuth2 et copiez le Client Secret dans le fichier .env.
2. Sur la même page, ajoutez l'adresse de redirection http://localhost:8080/callback.
3. Activez le tableau de bord dans settings.json.
4. Redémarrez le bot et ouvrez http://localhost:8080 dans votre navigateur. Connectez-vous avec Discord.

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

### Sécurité

- Connexion uniquement avec Discord (OAuth2, portée identify). Le jeton d'accès est révoqué aussitôt et jamais stocké.
- Seuls le propriétaire d'un serveur et les membres ayant la permission Administrateur ou Gérer le serveur ont accès, et uniquement à ce serveur. La permission est revérifiée à chaque requête.
- Seuls les serveurs auxquels le bot est connecté à cet instant peuvent être ouverts. Si le bot est hors ligne, absent du serveur ou en cours de démarrage, le tableau de bord refuse tout. Il s'exécute dans le bot et n'a ni base de données ni service propre.
- Par défaut, il n'écoute que sur 127.0.0.1, donc personne d'autre sur le réseau ne peut l'atteindre. Une adresse publique n'est acceptée qu'avec HTTPS, sinon le tableau de bord ne démarre pas.
- Les sessions utilisent un jeton aléatoire dans un cookie HttpOnly avec SameSite et, sous HTTPS, le préfixe __Host-. Elles expirent après 8 heures et n'existent qu'en mémoire : un redémarrage déconnecte tout le monde.
- Chaque modification exige un jeton CSRF et une origine correspondante. L'en-tête Host est vérifié contre le DNS rebinding. La page ne charge aucun script externe, une Content Security Policy stricte bloque le code en ligne, les requêtes sont limitées en débit et les corps à 256 Ko.
- Chaque valeur est vérifiée selon le type du réglage et les ID Discord doivent exister sur le serveur. L'état interne (compteurs, tickets, éléments enregistrés) n'est pas modifiable. Chaque changement est écrit dans le salon de logs de sécurité du serveur.
- Le contenu des messages n'est jamais affiché. Les cas de modération sont en lecture seule.

### Tableau de bord sur un VPS

Laissez host sur 127.0.0.1 et choisissez l'une des deux méthodes. D'abord un tunnel SSH : rien n'est exposé, vous ouvrez http://localhost:8080 sur votre ordinateur tant que le tunnel est actif.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Ensuite HTTPS via un reverse proxy comme Caddy, qui obtient seul un certificat (voir deploy/Caddyfile.example). Réglez alors public_url sur votre adresse https, ajoutez https://votre-adresse/callback comme redirection dans le Developer Portal et mettez trust_proxy sur true :

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

L'éditeur affiche chaque réglage qui est un interrupteur, un nombre, un texte, un salon, un rôle ou une liste simple. Ce qui se crée par commandes (articles de boutique, menus de rôles, flux, tags, tickets) reste des commandes. La page existe en anglais et en allemand et suit la langue du navigateur. Avec Docker, publiez le port uniquement sur 127.0.0.1 (127.0.0.1:8080:8080), puis mettez host sur 0.0.0.0 et allow_insecure_http sur true dans le conteneur.

## Commandes

La plupart des commandes sont des commandes slash, les commandes de modération fonctionnent aussi avec un préfixe. La liste complète se trouve dans la référence des commandes : [COMMANDS.md](../COMMANDS.md).

### Modération

Avertissements, mutes, expulsions et bannissements fonctionnent en commandes slash et avec le préfixe, par exemple `!warn @User spam`. Chaque action crée un cas numéroté.

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

### Goulag (jail)

Les membres au compte piraté sont déplacés dans un seul salon avec des consignes de sécurité. Leurs anciens rôles sont rendus à la libération.

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
```

### Modération automatique

Les règles suppriment ou sanctionnent les messages concernés. Choisissez l'action par règle : log, delete, warn, timeout ou jail.

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

### Protection anti-raid et verrouillage

Détecte de nombreuses arrivées en peu de temps et peut verrouiller le serveur. Le mode channels modifie chaque salon, le mode role agit immédiatement.

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

Surveille le journal d'audit et réagit quand quelqu'un détruit le serveur. Le propriétaire reçoit un message privé.

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

### Vérification

Les nouveaux membres ne voient que le salon de vérification jusqu'à ce qu'ils appuient sur le bouton ou résolvent le captcha.

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### Journalisation

Choisissez un salon par catégorie, ou un salon principal pour tout.

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### Bienvenue, au revoir et boosters

Messages, rôles automatiques et récompenses pour les boosters du serveur.

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

Les membres ouvrent des salons privés avec un bouton. La fermeture envoie une transcription.

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

### Sondages et concours

Des boutons pour voter et participer. Les durées acceptent des valeurs comme 30m, 2h et 1d.

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### Suggestions et starboard

Les membres postent des suggestions que l'équipe peut accepter ou refuser, et les messages populaires sont mis en avant.

```
/suggestion setup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
```

### XP et niveaux

XP pour le chat et le vocal, rôles de niveau, boosts par rôle et cartes de rang.

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

### Rôles par réaction et notifications

Donnez des rôles avec n'importe quel emoji et laissez les membres choisir leurs thèmes de notification.

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

### Anniversaires

Les membres indiquent le jour et le mois, le bot donne un rôle et poste un message le jour J.

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Salons vocaux temporaires

Rejoindre le salon hub crée une salle qui disparaît quand elle est vide.

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Sauvegarde et restauration

Les sauvegardes contiennent rôles, salons, emojis, webhooks et rôles des membres. La restauration n'ajoute que ce qui manque.

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### Données et confidentialité

Les membres peuvent exporter et supprimer leurs données. Les administrateurs règlent la durée de conservation.

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### Outils de modération

Nettoyer les salons, gérer les rôles et garder des notes privées. Chaque action est journalisée.

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

### Informations

Consulter les utilisateurs, le serveur, les rôles et le bot.

```
/userinfo user:@User
/serverinfo
/roleinfo role:@Moderator
/avatar user:@User
/help command:ban                                  # explains one command
/ping
/botinfo
```

### Annonces, tags et rappels

Écrire au nom du bot, créer des commandes personnalisées, répondre automatiquement aux messages et définir des rappels.

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

### Mod-mail et demandes de débannissement

Les membres écrivent à l'équipe par un salon privé du serveur. Personne n'a besoin d'envoyer un message privé au bot.

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

### Salon de comptage, messages épinglés et statistiques

Un jeu de comptage, des messages qui restent en bas d'un salon et des salons qui affichent des chiffres en direct.

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

### Autres options des fonctions existantes

Ajouts pour les tickets, concours, salons vocaux, XP, anniversaires, sauvegardes, journaux et affichages d'état.

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

### Autres outils AutoMod

Suivre les liens raccourcis, limiter les liens des nouveaux membres, repérer les ghost pings et tester les règles sans punir personne.

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

### Limites des modérateurs et audit des permissions

Recevoir une alerte quand un modérateur bannit ou expulse trop, et voir quels rôles ont des permissions dangereuses.

```
/modwatch status
/modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/modwatch exclude member:@TrustedMod

/permaudit run                                                  # roles with dangerous permissions and who holds them
/permaudit watch enabled:True                                   # alarm when a role or member gets one
/permaudit trust role:@Admin
```

### Signalements et suivi des invitations

Les membres signalent des messages à l'équipe, et le bot enregistre quelle invitation a amené chaque nouveau membre.

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

### Diagnostic et débogage

Trouver les permissions manquantes et les réglages cassés, recevoir les rapports d'erreur dans un salon et exporter ou importer les réglages.

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

### Musique

Lit des liens et des fichiers du dossier music dans un salon vocal. Les téléchargements sont enregistrés sous music/Artiste/Album/Titre. ffmpeg et les paquets de requirements.txt sont nécessaires.

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

Sans perte : vos propres fichiers (FLAC, WAV, ALAC) et les sources qui proposent du FLAC sont lus tels quels. YouTube, SoundCloud et les sites similaires ne proposent que de l'audio avec perte, qu'on ne peut pas rendre sans perte après coup. Discord transmet la voix en Opus, le bot utilise le débit du salon vocal. Responsabilité : télécharger et lire des contenus peut enfreindre les conditions d'un site ou le droit d'auteur. Les téléchargements sont désactivés par défaut et le module reste désactivé tant que vous ne l'activez pas. L'exploitant du bot est responsable de ce qui est lu et enregistré.

### Configuration et état de santé

Un assistant guidé configure l'essentiel avec des boutons et des menus : salon de logs, salon de bienvenue, rôles de l'équipe, le goulag, un préréglage AutoMod (souple, normal, strict), un modèle de serveur (communauté, jeux, support) et la langue. /health montre ce qui est configuré et ce qui reste à faire. La langue change les textes que voient les membres, comme les messages de bienvenue par défaut, les avis d'AutoMod, la vérification, les tickets, les recours, le mod-mail et les menus de rôles. Les réponses fixes aux administrateurs sont traduites, celles qui contiennent des noms et des nombres restent en anglais.

```
/setup                                                         # buttons and menus, nothing is switched off by a template
/health                                                        # what is set up, what is open, and the self-test
/language code:de
```

### Économie

Une monnaie de serveur avec récompense quotidienne, travail, paiements, classement et une boutique dont les articles peuvent donner un rôle. Activez-la avec le module economy. Les commandes fonctionnent aussi avec le préfixe, par exemple !economy daily.

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

### Menus de rôles, messages programmés et flux

Les menus de rôles donnent des rôles avec des boutons ou une liste déroulante. Les messages programmés sont publiés une fois ou répétés chaque heure, jour ou semaine. Les flux publient les nouvelles vidéos YouTube, les streams Twitch et les éléments RSS. Pour YouTube, utilisez l'ID de la chaîne (il commence par UC). Twitch nécessite TWITCH_CLIENT_ID et TWITCH_CLIENT_SECRET dans le fichier .env. Les heures s'écrivent in 2h, 18:30 ou sous forme de date avec heure comme 2026-12-24 18:00 dans le fuseau horaire du serveur. La première vérification d'un flux mémorise seulement ce qui existe déjà.

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

### Activité, actions groupées et recherche de cas

L'activité compte les messages par salon et les arrivées et départs par jour, jamais le contenu ni les noms. Les actions groupées bannissent, expulsent ou mettent en sourdine jusqu'à 25 utilisateurs après confirmation. Les cas se recherchent par utilisateur, type, nom, motif, modérateur et ancienneté, et peuvent être liés entre eux, par exemple une note à un bannissement.

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

### Anti-arnaque et anti-crypto

Supprime les faux concours, comme la fameuse arnaque MrBeast, dans le texte et les images en quelques millisecondes. Les noms de la liste immédiate sont supprimés sur-le-champ, quelle que soit l'orthographe (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Sinon, les mots des listes (noms, appâts, crypto, liens, montants) s'additionnent et le message est supprimé au seuil. Les images sont lues par OCR, et une image déjà jugée comme arnaque est supprimée sans être relue. La lecture des images nécessite tesseract, sans lui seul le texte est vérifié. Un serveur consacré à MrBeast peut retirer le nom de la liste immédiate ou exclure des salons avec /automod exemptchannel. Essayez avec /antiscam test avant de vous y fier.

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

### Période d'essai, détection d'essaim, chronologie et apprentissage

La période d'essai place les nouveaux membres dans un rôle. Tant qu'ils n'ont pas écrit le nombre réglé de messages normaux ou que les minutes ne sont pas écoulées, les liens, invitations et fichiers sont supprimés avec un court avertissement. La protection anti-raid reconnaît aussi un essaim : plusieurs nouveaux comptes avec le même motif de nom, la même photo de profil ou créés à quelques minutes d'intervalle. La chronologie (/case timeline) réunit dans l'ordre du temps la création du compte, l'arrivée et l'invitation, la période d'essai, les cas et les recours d'un utilisateur. Les messages ne sont jamais stockés, ils n'en font donc pas partie. /block, /unblock et /blocklist gèrent la liste de blocage d'AutoMod avec des commandes courtes. Les modérateurs entraînent le module anti-arnaque avec l'entrée de menu contextuel Mark as scam sur un message ou avec une réaction portant l'émoji défini par learn_emoji : le message est supprimé, et ses images et son texte sont ensuite supprimés immédiatement. Chaque partie se désactive avec son module ou ses réglages.

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

### Créateur de messages et mises à jour

Le créateur de messages publie des messages avec plusieurs embeds et des boutons de lien à partir de JSON. Il lit le JSON qu'exportent les générateurs d'embeds comme Embed Generator : vous concevez un message là-bas et le publiez avec le bot. Fournissez le JSON sous forme de texte, de fichier .json ou de lien https pointant directement vers le JSON, par exemple le fichier brut d'un dépôt (les liens avec redirection sont refusés). Seuls des boutons de lien sont créés, les boutons qui exigent une interaction sont ignorés. Chaque lien doit être http ou https, les mentions dans le texte ne notifient jamais, et les limites de Discord s'appliquent. /message copy exporte un message existant en JSON, /message edit modifie un message du bot et /message preview n'affiche le résultat qu'à vous. Les liens de partage des éditeurs web ne sont pas ouverts, car leur format n'est pas public.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

Toutes les 12 heures, le bot vérifie s'il existe une version plus récente dans le dépôt GitHub indiqué par update.repo (défini par scripts/set_repo_url.py). S'il y en a une, le propriétaire du bot reçoit un message privé avec les notes de version, puis la version est téléchargée et vérifiée : somme SHA-256 de la version, chemins sûrs dans l'archive et numéro de version conforme à l'étiquette. Elle s'installe avec /debug update action:install, ou automatiquement si auto_install est activé. Avant l'installation, les fichiers remplacés sont sauvegardés dans data/update, les nouveaux paquets sont installés et le nouveau code est importé à titre d'essai. En cas d'échec, les anciens fichiers sont restaurés. Votre .env, settings.json, data et music ne sont jamais touchés. Ensuite, le bot redémarre seul. Avec Docker, rien n'est installé sur place, mettez plutôt l'image à jour. Une mise à jour exécute du code du dépôt : ne la dirigez que vers un dépôt de confiance. Désactivez-la avec enabled sur false.

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

### Exploitation

Le bot enregistre ses données toutes les quelques secondes et conserve des sauvegardes de la base dans data/dbbackups, une avant chaque changement du format des données et une par jour. La file de musique, les messages épinglés et les compteurs des modérateurs survivent à un redémarrage. Les grands bots peuvent fonctionner sur plusieurs shards. Un fichier heartbeat et une page d'état facultative aident les outils de supervision. Ces options se règlent dans settings.json :

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

Activer ou désactiver modules et commandes, changer le préfixe, définir des alias et limiter des commandes à des rôles.

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

## Variables dans les messages

Ces variables sont remplacées dans les textes que vous configurez :

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## Configuration

Les options globales se règlent dans settings.json. Tout le reste se configure par serveur avec des commandes comme /module, /command, /perms, /alias et /config.

Pour renommer une commande, ajoutez-la dans command_names et redémarrez le bot :

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

Chaque réglage peut être lu et modifié avec /config. Voici les chemins que vous utiliserez le plus :

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

## Données et stockage

Tout ce que le bot enregistre se trouve sur votre propre machine :

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

## Structure du dépôt

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

## Traductions

L'anglais est la langue d'origine du projet. Toutes les traductions de la documentation, du tableau de bord et des messages du bot ont été créées par traduction automatique et n'ont pas été vérifiées par des locuteurs natifs. Attendez-vous à des formulations maladroites et à des erreurs, et signalez-les ou envoyez une correction. Les fichiers sont dans docs/ et guardbot/locales/.

## Feuille de route

- Graphiques d'activité et de modération dans le tableau de bord.
- Relecture de toutes les traductions par des locuteurs natifs.
- Davantage de textes de réponse fixes traduits.

## Confidentialité et sécurité

- Aucune télémétrie. Le bot communique avec Discord et, pour la vérification des mises à jour, avec GitHub (aucune donnée personnelle n'est envoyée, désactivez-la avec update.enabled). Les liens que lui donnent les administrateurs, comme les flux, la musique et les liens JSON, ne sont ouverts que sur demande.
- Toutes les données sont dans le dossier data de votre machine : réglages, XP, anniversaires (jour et mois uniquement) et cas de modération.
- Le bot ignore les messages privés des membres.
- Le jeton est lu depuis le fichier .env. Ne le partagez jamais et ne le publiez pas.
- Les membres peuvent exporter et supprimer leurs propres données avec /mydata. Les administrateurs définissent combien de temps les données des membres partis sont conservées.
- [PRIVACY.md](../PRIVACY.md)

## Assistance

Bugs, idées et suggestions : écrivez-moi sur Discord, @justyyin, ou ouvrez une issue sur GitHub.

## Crédits

GuardBot s'inspire d'[Embed Generator](https://github.com/merlinfuchs/embed-generator) de Merlin Fuchs (licence MIT, hébergé sur message.style). Le créateur de messages lit le même format JSON, les messages conçus là-bas peuvent donc être publiés avec ce bot. Aucun code de ce projet n'est inclus. Merci aux auteurs de discord.py, aiohttp, Pillow, yt-dlp, mutagen et Tesseract.

## Licence

Publié sous licence MIT. Voir [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
