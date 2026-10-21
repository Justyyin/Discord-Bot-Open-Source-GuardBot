# GuardBot: Guide d'installation

Ce guide explique comment faire fonctionner GuardBot sur votre ordinateur ou sur un VPS. Comptez environ 15 minutes.

<!-- toc -->

- [Créer le bot Discord](#créer-le-bot-discord)
- [Exécuter sur votre ordinateur](#exécuter-sur-votre-ordinateur)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux et macOS](#linux-et-macos)
- [Exécuter sur un VPS](#exécuter-sur-un-vps)
- [Exécuter avec Docker](#exécuter-avec-docker)
- [Premiers pas sur Discord](#premiers-pas-sur-discord)
- [Mises à jour et sauvegardes](#mises-à-jour-et-sauvegardes)
- [Dépannage](#dépannage)
- [Assistance](#assistance)

<!-- tocstop -->

## Créer le bot Discord

1. Ouvrez le [Discord Developer Portal](https://discord.com/developers/applications) et cliquez sur New Application.
2. Ouvrez l'onglet Bot et cliquez sur Reset Token. Copiez le jeton et gardez-le secret.
3. Sur le même onglet, activez Server Members Intent et Message Content Intent.
4. Ouvrez OAuth2, URL Generator. Sélectionnez les scopes bot et applications.commands.
5. Sélectionnez les permissions : Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, View Audit Log, Manage Messages, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Move Members. Administrator fonctionne aussi et reste le choix le plus simple.
6. Ouvrez l'URL générée et ajoutez le bot à votre serveur.
7. Dans les paramètres du serveur, placez le rôle du bot tout en haut de la liste des rôles. Le bot ne peut gérer que les rôles situés sous son propre rôle.

Vous pouvez aussi utiliser cette URL d'invitation. Remplacez YOUR_CLIENT_ID par l'Application ID du Developer Portal :

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## Exécuter sur votre ordinateur

Installez Python 3.11 ou plus récent et Git, puis exécutez ces commandes dans un terminal.

### Windows (PowerShell)

```powershell
git clone <REPOSITORY_URL>
cd guardbot
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
python main.py
```

### Linux et macOS

```bash
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
```

Ouvrez le fichier .env et remplacez l'exemple par le jeton de votre bot. Le bot est en ligne dès que la console affiche la ligne commençant par online as. Laissez la fenêtre ouverte, le bot s'arrête quand vous la fermez.

## Exécuter sur un VPS

Ces commandes concernent Ubuntu ou Debian et installent le bot comme service qui démarre automatiquement.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
sudo git clone <REPOSITORY_URL> /opt/guardbot
sudo useradd --system --no-create-home --shell /usr/sbin/nologin guardbot
cd /opt/guardbot
sudo python3 -m venv .venv
sudo .venv/bin/pip install -r requirements.txt
sudo cp .env.example .env
sudo nano .env
sudo mkdir -p data
sudo chown -R guardbot:guardbot /opt/guardbot
sudo chmod 600 .env
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now guardbot
sudo journalctl -u guardbot -f
```

Vérifiez l'état avec systemctl status guardbot. Le journal affiche la ligne commençant par online as quand le bot est prêt.

## Exécuter avec Docker

Docker est facultatif. Créez d'abord le fichier .env, puis lancez :

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## Premiers pas sur Discord

Utilisez ces commandes sur votre serveur et remplacez les noms de salons par les vôtres.

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

Toutes les fonctions sont décrites dans la référence des commandes : [COMMANDS.md](../COMMANDS.md).

## Mises à jour et sauvegardes

Mettre le bot à jour :

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

Sauvegardez vos réglages en copiant le dossier data, par exemple :

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## Dépannage

- Les commandes slash n'apparaissent pas : attendez quelques minutes, redémarrez Discord et vérifiez que le bot a été invité avec le scope applications.commands.
- Le bot s'arrête avec une erreur d'intents privilégiés : activez Server Members Intent et Message Content Intent dans le Developer Portal.
- Improper token : copiez à nouveau le jeton et vérifiez que .env contient exactement DISCORD_TOKEN=jeton, sans espace ni guillemets.
- I cannot assign that role : placez le rôle du bot au-dessus du rôle qu'il doit gérer.
- Rien n'est journalisé : définissez un salon avec /log set et vérifiez que le bot peut y envoyer des messages, intégrer des liens et joindre des fichiers.
- Unknown timezone : exécutez pip install tzdata et redémarrez le bot.
- Quelque chose échoue sans raison visible : les erreurs et avertissements sont écrits dans la console. Sur un VPS, lisez-les avec journalctl -u guardbot -f.

## Assistance

Bugs, idées et suggestions : Discord @justyyin ou une issue GitHub.

Copyright (c) Justyn - made in Germany
