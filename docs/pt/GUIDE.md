# GuardBot: Guia de instalação

Este guia mostra como executar o GuardBot no seu computador ou em um VPS. Leva cerca de 15 minutos.

> Beta: o GuardBot e o seu painel estão em fase beta. Não foram testados a fundo, sobretudo não em servidores grandes nem em todas as situações do Discord. Conte com erros, faça cópias da pasta data e comunique os problemas. Uso por sua conta e risco.

<!-- toc -->

- [Criar o bot do Discord](#criar-o-bot-do-discord)
- [Executar no seu computador](#executar-no-seu-computador)
  - [Windows (PowerShell)](#windows-powershell)
  - [Linux e macOS](#linux-e-macos)
- [Executar em um VPS](#executar-em-um-vps)
- [Executar com Docker](#executar-com-docker)
- [Primeiros passos no Discord](#primeiros-passos-no-discord)
- [Estrutura, equipa e visão geral (1.5)](#estrutura-equipa-e-visão-geral-15)
- [Atualizações e backups](#atualizações-e-backups)
- [Música (opcional)](#música-opcional)
- [Opcional: ler imagens e idiomas](#opcional-ler-imagens-e-idiomas)
- [Painel](#painel)
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

Todos os recursos estão descritos na referência de comandos: [COMMANDS.md](../COMMANDS.md).

## Estrutura, equipa e visão geral (1.5)

Estes passos configuram as funções mais recentes. Cada uma pode ser desativada com /admin module, e o prefixo e os textos continuam editáveis por servidor.

1. Ver o que está configurado: `/admin module overview` lista cada módulo com o estado e se está configurado. O painel web mostra o mesmo no seu painel de configuração.
2. Encontrar um comando: `/info find text:ban` procura em todos os comandos por palavra, `/help` mostra os grupos.
3. Publicar as regras com botão de aceitar: `/structure rules setup`, depois `/structure rules add`, depois `/structure rules post`. Quem não aceitou uma nova versão é lembrado de poucas em poucas horas.
4. Dizer ao bot quem é da equipa: `/team duty roster`. As listas de pessoal disponível e o encaminhamento de tickets e alertas usam isto.
5. Arrumar canais inativos: `/structure archive setup`, depois `/structure archive scan`.
6. Devolver os cargos aos membros que regressam: `/members stickyroles setup`.
7. Manter os nomes legíveis: `/members nickname setup`, teste com `/members nickname check` antes de `/members nickname scan`.
8. Antes de grandes alterações, exporte as definições com `/admin config export` e verifique cargos e canais com `/server diagnose`.

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

## Música (opcional)

O módulo de música precisa de ffmpeg no computador onde o bot corre. Coloque a sua música na pasta music/ como Artista/Álbum/01 - Título.flac, ou permita downloads. A pasta pode crescer muito: guarde-a num disco com espaço ou num volume Docker.

```
# Windows
winget install Gyan.FFmpeg
# macOS
brew install ffmpeg
# Ubuntu or Debian
sudo apt install -y ffmpeg libopus0

# in Discord
/admin module enable name:music
/music settings allow_download:True
```

## Opcional: ler imagens e idiomas

Para que o módulo anti-burla leia o texto das imagens, instale o tesseract no computador onde o bot corre (a imagem Docker já o inclui). Depois verifique com /security antiscam status se está pronto. Escolha o idioma das mensagens que os membros veem com /admin language.

```
# Ubuntu or Debian
sudo apt install -y tesseract-ocr
# macOS
brew install tesseract
# Windows
winget install UB-Mannheim.TesseractOCR

# in Discord
/security antiscam status
/admin language code:de
```

## Painel

O painel é uma página web que corre dentro do bot. Depois de iniciar sessão com o Discord, altera as definições dos seus servidores com interruptores, menus e campos em vez de comandos: módulos, canais, cargos, limites, textos, o prefixo e o idioma. Mostra também os últimos casos de moderação e exporta e importa definições. Funciona da mesma forma no seu computador e num VPS, e está desligado até o ativar.

1. Abra a sua aplicação no Developer Portal, vá a OAuth2 e copie o Client Secret para o ficheiro .env.
2. Na mesma página, adicione o endereço de redirecionamento http://localhost:8080/callback.
3. Ative o painel em settings.json.
4. Reinicie o bot e abra http://localhost:8080 no navegador. Inicie sessão com o Discord.

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

Deixe host em 127.0.0.1 e escolha um de dois caminhos. Primeiro, um túnel SSH: nada é exposto e abre http://localhost:8080 no seu computador enquanto o túnel estiver ativo.

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Segundo, HTTPS através de um proxy inverso como o Caddy, que obtém o seu próprio certificado (veja deploy/Caddyfile.example). Depois defina public_url com o seu endereço https, adicione https://o-seu-endereco/callback como redirecionamento no Developer Portal e ponha trust_proxy em true:

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

## Solução de problemas

- Os comandos slash não aparecem: aguarde alguns minutos, reinicie o Discord e confira se o bot foi convidado com o scope applications.commands.
- O bot para com um erro de intents privilegiados: ative Server Members Intent e Message Content Intent no Developer Portal.
- Improper token: copie o token novamente e confira se o .env contém exatamente DISCORD_TOKEN=token, sem espaços nem aspas.
- I cannot assign that role: mova o cargo do bot para acima do cargo que ele deve gerenciar.
- Nada é registrado: defina um canal com /server log set e confira se o bot pode enviar mensagens, incorporar links e anexar arquivos nele.
- Unknown timezone: execute pip install tzdata e reinicie o bot.
- Algo falha sem motivo visível: erros e avisos são escritos no console. Em um VPS, leia-os com journalctl -u guardbot -f.

## Suporte

Bugs, ideias e sugestões: Discord @justyyin ou uma issue no GitHub.

Copyright (c) Justyn - made in Germany
