# GuardBot: Guia de instalação

Este guia mostra como executar o GuardBot no seu computador ou em um VPS. Leva cerca de 15 minutos.

<!-- toc -->

- [Criar o bot do Discord](#criar-o-bot-do-discord)
- [Executar no seu computador](#executar-no-seu-computador)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux e macOS](#linux-e-macos)
- [Executar em um VPS](#executar-em-um-vps)
- [Executar com Docker](#executar-com-docker)
- [Primeiros passos no Discord](#primeiros-passos-no-discord)
- [Atualizações e backups](#atualizações-e-backups)
- [Solução de problemas](#solução-de-problemas)
- [Suporte](#suporte)

<!-- tocstop -->

## Criar o bot do Discord

1. Abra o [Discord Developer Portal](https://discord.com/developers/applications) e clique em New Application.
2. Abra a aba Bot e clique em Reset Token. Copie o token e mantenha-o em segredo.
3. Na mesma aba, ative Server Members Intent e Message Content Intent.
4. Abra OAuth2, URL Generator. Selecione os scopes bot e applications.commands.
5. Selecione as permissões: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, View Audit Log, Manage Messages, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions, Move Members. Administrator também funciona e é a opção mais simples.
6. Abra a URL gerada e adicione o bot ao seu servidor.
7. Nas configurações do servidor, mova o cargo do bot para o topo da lista de cargos. O bot só pode gerenciar cargos abaixo do seu próprio cargo.

Como alternativa, use esta URL de convite. Substitua YOUR_CLIENT_ID pelo Application ID do Developer Portal:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=1099797228758
```

## Executar no seu computador

Instale Python 3.11 ou mais recente e o Git, depois execute estes comandos em um terminal.

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

### Linux e macOS

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

Abra o arquivo .env e troque o texto de exemplo pelo token do seu bot. O bot fica online assim que o console mostrar a linha que começa com online as. Mantenha a janela aberta, o bot para quando você a fecha.

## Executar em um VPS

Estes comandos valem para Ubuntu ou Debian e configuram o bot como um serviço que inicia automaticamente.

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

Verifique o estado com systemctl status guardbot. O log mostra a linha que começa com online as quando o bot está pronto.

## Executar com Docker

O Docker é opcional. Crie primeiro o arquivo .env e depois execute:

```bash
docker compose -f deploy/docker-compose.yml up -d --build
docker compose -f deploy/docker-compose.yml logs -f
```

## Primeiros passos no Discord

Use estes comandos no seu servidor e troque os nomes dos canais pelos seus.

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

Todos os recursos estão descritos na referência de comandos: [COMMANDS.md](../COMMANDS.md).

## Atualizações e backups

Atualizar o bot:

```bash
cd /opt/guardbot
sudo -u guardbot git pull
sudo .venv/bin/pip install -r requirements.txt
sudo systemctl restart guardbot
```

Faça backup das configurações copiando a pasta data, por exemplo:

```bash
tar czf guardbot-data-$(date +%F).tar.gz data
```

## Solução de problemas

- Os comandos slash não aparecem: aguarde alguns minutos, reinicie o Discord e confira se o bot foi convidado com o scope applications.commands.
- O bot para com um erro de intents privilegiados: ative Server Members Intent e Message Content Intent no Developer Portal.
- Improper token: copie o token novamente e confira se o .env contém exatamente DISCORD_TOKEN=token, sem espaços nem aspas.
- I cannot assign that role: mova o cargo do bot para acima do cargo que ele deve gerenciar.
- Nada é registrado: defina um canal com /log set e confira se o bot pode enviar mensagens, incorporar links e anexar arquivos nele.
- Unknown timezone: execute pip install tzdata e reinicie o bot.
- Algo falha sem motivo visível: erros e avisos são escritos no console. Em um VPS, leia-os com journalctl -u guardbot -f.

## Suporte

Bugs, ideias e sugestões: Discord @justyyin ou uma issue no GitHub.

Copyright (c) Justyn - made in Germany
