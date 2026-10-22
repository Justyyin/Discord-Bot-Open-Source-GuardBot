# GuardBot: Guide d'installation

Ce guide explique comment faire fonctionner GuardBot sur votre ordinateur ou sur un VPS. Comptez environ 15 minutes.

> Bêta : GuardBot et son tableau de bord sont en phase bêta. Ils n'ont pas été testés à fond, surtout pas sur de grands serveurs ni face à toutes les situations de Discord. Attendez-vous à des bugs, sauvegardez le dossier data et signalez les problèmes. Utilisation à vos risques.

<!-- toc -->

- [Créer le bot Discord](#créer-le-bot-discord)
- [Exécuter sur votre ordinateur](#exécuter-sur-votre-ordinateur)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux et macOS](#linux-et-macos)
- [Exécuter sur un VPS](#exécuter-sur-un-vps)
- [Exécuter avec Docker](#exécuter-avec-docker)
- [Premiers pas sur Discord](#premiers-pas-sur-discord)
- [Mises à jour et sauvegardes](#mises-à-jour-et-sauvegardes)
- [Musique (facultatif)](#musique-facultatif)
- [Facultatif : lire les images et les langues](#facultatif--lire-les-images-et-les-langues)
- [Tableau de bord](#tableau-de-bord)
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
sudo apt install -y python3 python3-venv python3-pip git ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0 ffmpeg libopus0
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

## Musique (facultatif)

Le module musique nécessite ffmpeg sur l'ordinateur qui exécute le bot. Placez votre musique dans le dossier music/ sous la forme Artiste/Album/01 - Titre.flac, ou autorisez les téléchargements. Le dossier peut devenir volumineux : gardez-le sur un disque avec de la place ou dans un volume Docker.

```
# Windows
winget install Gyan.FFmpeg
# macOS
brew install ffmpeg
# Ubuntu or Debian
sudo apt install -y ffmpeg libopus0

# in Discord
/module enable name:music
/music settings allow_download:True
```

## Facultatif : lire les images et les langues

Pour que le module anti-arnaque lise le texte des images, installez tesseract sur l'ordinateur qui exécute le bot (l'image Docker le contient déjà). Vérifiez ensuite avec /antiscam status qu'il est prêt. Choisissez la langue des messages que voient les membres avec /language.

```
# Ubuntu or Debian
sudo apt install -y tesseract-ocr
# macOS
brew install tesseract
# Windows
winget install UB-Mannheim.TesseractOCR

# in Discord
/antiscam status
/language code:de
```

## Tableau de bord

Le tableau de bord est une page web qui s'exécute dans le bot. Après connexion avec Discord, vous modifiez les réglages de vos serveurs avec des interrupteurs, des menus et des champs au lieu de commandes : modules, salons, rôles, seuils, textes, préfixe et langue. Il affiche aussi les derniers cas de modération et exporte et importe les réglages. Il fonctionne de la même façon sur votre ordinateur et sur un VPS, et reste désactivé tant que vous ne l'activez pas.

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
