# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | **Français** | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Bot Discord auto-hébergé pour la modération, la sécurité et la communauté. Open source, gratuit, et vos données restent sur votre propre machine.

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
- [Permissions du bot](#permissions-du-bot)
- [Premiers pas sur Discord](#premiers-pas-sur-discord)
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
  - [Administration](#administration-1)
- [Variables dans les messages](#variables-dans-les-messages)
- [Configuration](#configuration)
- [Données et stockage](#données-et-stockage)
- [Structure du dépôt](#structure-du-dépôt)
- [Feuille de route](#feuille-de-route)
- [Confidentialité et sécurité](#confidentialité-et-sécurité)
- [Assistance](#assistance)
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

### Administration

- Chaque module et chaque commande peut être activé ou désactivé par serveur.
- Préfixe personnalisé, alias de commandes et commandes renommables.
- Sauvegarde et restauration des rôles et de la structure des salons.
- Sauvegardes automatiques planifiées des rôles, salons, emojis et webhooks, avec une commande de restauration qui n'ajoute que ce qui manque.

## État du projet

GuardBot est jeune et n'a pas encore été utilisé sur de grands serveurs. Les tests automatiques (`python -m unittest`) couvrent le stockage, la détection des données personnelles, le calcul des niveaux, l'enregistrement des commandes, les contrôles de permissions et les liens de la documentation. Tout ce qui nécessite un vrai serveur Discord, comme le verrouillage, la restauration de sauvegarde, la vérification, l'anti-nuke et le goulag, n'est pas couvert. Essayez ces fonctions d'abord sur un serveur de test avant de vous y fier. Les traductions de la documentation n'ont pas été relues par des locuteurs natifs, les corrections sont les bienvenues.

## Prérequis

- Python 3.11 ou plus récent
- Une application Discord avec un jeton de bot
- Un ordinateur ou un VPS toujours en ligne

## Démarrage rapide

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Le guide complet étape par étape se trouve dans [GUIDE.md](GUIDE.md).

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
/case case_id:12

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
/suggestionsetup set channel:#suggestions review_role:@Staff
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

### Rôles par réaction et notifications

Donnez des rôles avec n'importe quel emoji et laissez les membres choisir leurs thèmes de notification.

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

### Anniversaires

Les membres indiquent le jour et le mois, le bot donne un rôle et poste un message le jour J.

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

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
/birthdaysetup set   message                         {user} {name}
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

## Feuille de route

- Tableau de bord web local qui tourne sur votre propre machine, pour modifier les réglages sans service hébergé.
- Messages du bot traduits.
- Export et import des réglages.

## Confidentialité et sécurité

- Aucune télémétrie et aucun service externe. Le bot ne communique qu'avec Discord.
- Toutes les données sont dans le dossier data de votre machine : réglages, XP, anniversaires (jour et mois uniquement) et cas de modération.
- Le bot ignore les messages privés des membres.
- Le jeton est lu depuis le fichier .env. Ne le partagez jamais et ne le publiez pas.
- Les membres peuvent exporter et supprimer leurs propres données avec /mydata. Les administrateurs définissent combien de temps les données des membres partis sont conservées.
- [PRIVACY.md](../PRIVACY.md)

## Assistance

Bugs, idées et suggestions : écrivez-moi sur Discord, @justyyin, ou ouvrez une issue sur GitHub.

## Licence

Publié sous licence MIT. Voir [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
