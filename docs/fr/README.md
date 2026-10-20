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
- [Structure du dépôt](#structure-du-dépôt)
- [Commandes](#commandes)
- [Configuration](#configuration)
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

## Commandes

La plupart des commandes sont des commandes slash, les commandes de modération fonctionnent aussi avec un préfixe. La liste complète se trouve dans la référence des commandes : [COMMANDS.md](../COMMANDS.md).

## Configuration

Les options globales se règlent dans settings.json. Tout le reste se configure par serveur avec des commandes comme /module, /command, /perms, /alias et /config.

Pour renommer une commande, ajoutez-la dans command_names et redémarrez le bot :

```json
{
  "prefix": "!",
  "command_names": {
    "warn": "verwarnen"
  }
}
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
