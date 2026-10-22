# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | **Português** | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Bot de Discord auto-hospedado para moderação, segurança e comunidade. Código aberto, gratuito, e os seus dados ficam no seu próprio computador.

> Beta: o GuardBot e o seu painel estão em fase beta. Não foram testados a fundo, sobretudo não em servidores grandes nem em todas as situações do Discord. Conte com erros, faça cópias da pasta data e comunique os problemas. Uso por sua conta e risco.

<!-- toc -->

- [Sobre o projeto](#sobre-o-projeto)
- [Recursos](#recursos)
  - [Segurança](#segurança)
  - [Moderação](#moderação)
  - [Registros](#registros)
  - [Comunidade](#comunidade)
  - [Administração](#administração)
- [Status do projeto](#status-do-projeto)
- [Requisitos](#requisitos)
- [Início rápido](#início-rápido)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Scripts de arranque e arranque automático](#scripts-de-arranque-e-arranque-automático)
  - [Atualizar](#atualizar)
- [Permissões do bot](#permissões-do-bot)
- [Primeiros passos no Discord](#primeiros-passos-no-discord)
- [Painel](#painel)
  - [Configurar o painel](#configurar-o-painel)
  - [Segurança](#segurança-1)
  - [Painel num VPS](#painel-num-vps)
- [Comandos](#comandos)
  - [Moderação](#moderação-1)
  - [Gulag (jail)](#gulag-jail)
  - [Moderação automática](#moderação-automática)
  - [Proteção anti-raid e lockdown](#proteção-anti-raid-e-lockdown)
  - [Anti-nuke](#anti-nuke)
  - [Verificação](#verificação)
  - [Registros](#registros-1)
  - [Boas-vindas, despedida e boosters](#boas-vindas-despedida-e-boosters)
  - [Tickets](#tickets)
  - [Enquetes e sorteios](#enquetes-e-sorteios)
  - [Sugestões e starboard](#sugestões-e-starboard)
  - [XP e níveis](#xp-e-níveis)
  - [Cargos por reação e notificações](#cargos-por-reação-e-notificações)
  - [Aniversários](#aniversários)
  - [Canais de voz temporários](#canais-de-voz-temporários)
  - [Backup e restauração](#backup-e-restauração)
  - [Dados e privacidade](#dados-e-privacidade)
  - [Ferramentas de moderação](#ferramentas-de-moderação)
  - [Informações](#informações)
  - [Anúncios, tags e lembretes](#anúncios-tags-e-lembretes)
  - [Mod-mail e recursos de banimento](#mod-mail-e-recursos-de-banimento)
  - [Canal de contagem, mensagens fixas e estatísticas](#canal-de-contagem-mensagens-fixas-e-estatísticas)
  - [Mais opções das funções existentes](#mais-opções-das-funções-existentes)
  - [Mais ferramentas do AutoMod](#mais-ferramentas-do-automod)
  - [Limites dos moderadores e auditoria de permissões](#limites-dos-moderadores-e-auditoria-de-permissões)
  - [Denúncias e rastreio de convites](#denúncias-e-rastreio-de-convites)
  - [Diagnóstico e depuração](#diagnóstico-e-depuração)
  - [Música](#música)
  - [Configuração e estado de saúde](#configuração-e-estado-de-saúde)
  - [Economia](#economia)
  - [Menus de cargos, mensagens agendadas e feeds](#menus-de-cargos-mensagens-agendadas-e-feeds)
  - [Atividade, ações em massa e pesquisa de casos](#atividade-ações-em-massa-e-pesquisa-de-casos)
  - [Anti-burla e anti-cripto](#anti-burla-e-anti-cripto)
  - [Período de prova, deteção de enxame, linha do tempo e aprendizagem](#período-de-prova-deteção-de-enxame-linha-do-tempo-e-aprendizagem)
  - [Criador de mensagens e atualizações](#criador-de-mensagens-e-atualizações)
  - [Operação](#operação)
  - [Administração](#administração-1)
- [Marcadores nas mensagens](#marcadores-nas-mensagens)
- [Configuração](#configuração)
- [Dados e armazenamento](#dados-e-armazenamento)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Traduções](#traduções)
- [Roteiro](#roteiro)
- [Privacidade e segurança](#privacidade-e-segurança)
- [Suporte](#suporte)
- [Créditos](#créditos)
- [Licença](#licença)

<!-- tocstop -->

## Sobre o projeto

O GuardBot reúne recursos pelos quais muitos servidores pagam em bots hospedados: moderação, registros, anti-raid, anti-nuke, tickets, níveis e mais. Você mesmo executa o bot, no seu computador ou em um VPS pequeno.

Bots hospedados armazenam dados do servidor, IDs de membros e, às vezes, e-mails com terceiros. Quando você hospeda o bot por conta própria, esses dados não saem da sua máquina. O GuardBot quer mostrar que qualquer pessoa pode rodar um bot completo sem assinatura.

## Recursos

### Segurança

- Moderação automática: filtro de palavras, filtro de maiúsculas, spam de menções, links de convite, domínios de phishing, dados pessoais, doxxing e ameaças. Todas as listas podem ser editadas.
- Anti-raid com detecção de ondas de entradas e bloqueio de todo o servidor.
- Anti-nuke: limites para exclusões e banimentos em massa, resposta automática e mensagem direta ao dono do servidor.
- Canal gulag: quem publica links ou imagens de golpe é movido para um único canal com instruções para proteger a conta. Moderadores também podem usar /jail e /unjail.
- Verificação por botão ou captcha, com remoção automática de quem não se verifica a tempo.
- O anti-nuke também monitora concessão de permissões, novos webhooks, bots adicionados e mudanças de nome do servidor.
- Anti-burla: sorteios falsos e burlas cripto são removidos em texto e imagens em milissegundos, incluindo a burla do MrBeast em qualquer grafia.

### Moderação

- Warn, mute, kick, ban e jail com histórico filtrável por menção, ID de usuário ou tipo.
- Escalonamento automático, por exemplo três avisos levam a um castigo temporário.
- Defina quais cargos ou usuários podem usar cada comando de moderação.

### Registros

- Mensagens enviadas, editadas e excluídas, incluindo imagens, GIFs e URLs, com canais de registro separados.
- Alterações de cargos, apelidos, banimentos, voz, canais e cargos do servidor.

### Comunidade

- Mensagens de boas-vindas e despedida, cargos automáticos e recompensas para boosters.
- Tickets, enquetes, sorteios e sugestões.
- Cargos por reação com qualquer emoji e tópicos de notificação que os membros ativam ou desativam.
- XP e níveis de 1 a 100 para chat e voz, cargos por nível e aniversários.
- Starboard e canais de voz temporários.
- Jail com duração, enquetes de múltipla escolha, cartões de rank em imagem e bônus de XP por cargo.
- Economia com loja, menus de cargos com botões ou lista suspensa, mensagens agendadas, feeds do YouTube, Twitch e RSS, estatísticas de atividade e um /setup guiado. As mensagens aos membros existem em 12 idiomas.

### Administração

- Cada módulo e cada comando pode ser ativado ou desativado por servidor.
- Prefixo próprio, apelidos de comandos e comandos renomeáveis.
- Backup e restauração de cargos e da estrutura de canais.
- Backups automáticos agendados de cargos, canais, emojis e webhooks, com um comando de restauração que só adiciona o que falta.
- Painel: altere as definições de cada servidor no navegador após iniciar sessão com o Discord, apenas para membros que gerem o servidor e apenas enquanto o bot estiver ligado.

## Status do projeto

O GuardBot é jovem e ainda não foi usado em servidores grandes. Os testes automáticos (`python -m unittest`) cobrem armazenamento, detecção de dados pessoais, cálculo de níveis, registro de comandos, verificações de permissão e os links da documentação. Tudo que precisa de um servidor Discord real, como lockdown, restauração de backup, verificação, anti-nuke e o gulag, não é coberto por eles. Teste esses recursos primeiro em um servidor de testes antes de depender deles. As traduções da documentação não foram revisadas por falantes nativos, correções são bem-vindas.

## Requisitos

- Python 3.11 ou mais recente
- Um aplicativo do Discord com token de bot
- Um computador ou VPS sempre online
- ffmpeg (apenas para o módulo de música)
- tesseract-ocr (opcional, apenas para ler texto em imagens)

## Início rápido

Escolha o seu sistema. Cada variante precisa de Python 3.11 ou mais recente e do token do seu bot. O guia detalhado passo a passo está em [GUIDE.md](GUIDE.md).

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

### Scripts de arranque e arranque automático

Os scripts de arranque criam o ambiente virtual, instalam os pacotes e iniciam o bot. Na primeira execução criam o ficheiro .env e param, para que introduza o token. Execute-os de novo depois.

```bash
./start.sh
```

```bat
start.bat
```

Para que o bot continue a funcionar após reiniciar o computador, use um serviço. Linux (systemd) e macOS (launchd):

```bash
sudo cp deploy/guardbot.service /etc/systemd/system/
sudo systemctl enable --now guardbot
journalctl -u guardbot -f
```

```bash
cp deploy/de.guardbot.plist ~/Library/LaunchAgents/de.guardbot.plist
launchctl load ~/Library/LaunchAgents/de.guardbot.plist
```

No Windows, crie uma tarefa no Agendador de Tarefas que execute start.bat ao iniciar sessão, ou use um invólucro de serviço como o NSSM. Para Docker, veja [GUIDE.md](GUIDE.md).

### Atualizar

Pare o bot, execute estes comandos e inicie-o de novo. Os seus dados na pasta data não são tocados, e o bot faz uma cópia da base de dados antes de cada alteração de formato.

```bash
git pull
.venv/bin/pip install -r requirements.txt
```

## Permissões do bot

O mais simples é a permissão de Administrador. Se preferir direitos mínimos, conceda estes e ative os intents Server Members e Message Content no Developer Portal:

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

## Primeiros passos no Discord

Uma configuração inicial sensata. Execute estes comandos no seu servidor e troque os canais e cargos pelos seus:

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

## Painel

O painel é uma página web que corre dentro do bot. Depois de iniciar sessão com o Discord, altera as definições dos seus servidores com interruptores, menus e campos em vez de comandos: módulos, canais, cargos, limites, textos, o prefixo e o idioma. Mostra também os últimos casos de moderação e exporta e importa definições. Funciona da mesma forma no seu computador e num VPS, e está desligado até o ativar.

### Configurar o painel

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

### Segurança

- Início de sessão apenas com o Discord (OAuth2, âmbito identify). O token de acesso é revogado de imediato e nunca é guardado.
- Só o dono de um servidor e os membros com a permissão Administrador ou Gerir servidor têm acesso, e apenas a esse servidor. A permissão é verificada de novo em cada pedido.
- Só podem ser abertos servidores a que o bot está ligado nesse momento. Se o bot estiver offline, fora do servidor ou ainda a arrancar, o painel recusa tudo. Corre dentro do bot e não tem base de dados nem serviço próprios.
- Por predefinição só escuta em 127.0.0.1, por isso mais ninguém na rede lhe consegue aceder. Um endereço público só é aceite com HTTPS; caso contrário o painel não arranca.
- As sessões usam um token aleatório num cookie HttpOnly com SameSite e, sob HTTPS, o prefixo __Host-. Terminam após 8 horas e existem apenas em memória, por isso um reinício termina todas as sessões.
- Cada alteração exige um token CSRF e uma Origin correspondente. O cabeçalho Host é verificado contra DNS rebinding. A página não carrega scripts externos, uma Content Security Policy rigorosa bloqueia código em linha, os pedidos têm limite de frequência e o corpo está limitado a 256 KB.
- Cada valor é verificado segundo o tipo da definição e os IDs do Discord têm de existir no servidor. O estado interno, como contadores, tickets e itens guardados, não pode ser editado. Cada alteração é escrita no canal de registo de segurança do servidor.
- O conteúdo das mensagens nunca é mostrado. Os casos de moderação são só de leitura.

### Painel num VPS

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

O editor mostra cada definição que seja um interruptor, um número, um texto, um canal, um cargo ou uma lista simples. O que se cria com comandos, como itens da loja, menus de cargos, feeds, tags e tickets, continua a ser feito por comandos. A página existe em inglês e alemão e segue o idioma do navegador. No Docker, publique a porta apenas em 127.0.0.1 (127.0.0.1:8080:8080) e defina no contentor host como 0.0.0.0 e allow_insecure_http como true.

## Comandos

A maioria dos comandos são comandos slash, os de moderação também funcionam com prefixo. A lista completa está na referência de comandos: [COMMANDS.md](../COMMANDS.md).

### Moderação

Avisos, silenciamentos, expulsões e banimentos funcionam como comandos slash e com prefixo, por exemplo `!warn @User spam`. Cada ação cria um caso numerado.

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

Membros com a conta invadida vão para um único canal com instruções de segurança. Ao serem libertados, recebem os cargos antigos de volta.

```
/jailsetup setup role:@Gulag channel:#gulag staff_role:@Moderator   # empty options are created for you
/jailsetup apply                                   # apply the channel permissions again
/jailsetup notice text:Custom text for {staff}     # empty text restores the security steps
/jailsetup preview

/jail member:@User reason:Hacked account           # also: !jail @User Hacked account
/jail member:@User duration:2h                     # released automatically after 2 hours
/unjail member:@User reason:Account secured
```

### Moderação automática

As regras apagam ou punem as mensagens correspondentes. Escolha a ação por regra: log, delete, warn, timeout ou jail.

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

### Proteção anti-raid e lockdown

Detecta muitas entradas em pouco tempo e pode bloquear o servidor. O modo channels altera cada canal, o modo role é instantâneo.

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

Monitora o registro de auditoria e reage quando alguém destrói o servidor. O dono recebe uma mensagem direta.

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

### Verificação

Membros novos só veem o canal de verificação até apertarem o botão ou resolverem o captcha.

```
/verify setup channel:#verify mode:captcha timeout_minutes:30 min_account_age_days:3
# modes: button, captcha (image), math; roles are created if you do not pass them
/verify setup channel:#verify verified_role:@Member unverified_role:@Unverified
/verify panel channel:#verify                      # post the button again
/verify apply                                      # apply the channel permissions again
/verify member member:@User                        # verify someone manually
/verify off
```

### Registros

Escolha um canal por categoria, ou um canal principal para tudo.

```
/log set category:main channel:#logs               # fallback for every category
/log set category:messages channel:#log-messages
/log set category:moderation channel:#log-moderation
/log set category:security channel:#log-security
# categories: main, messages, members, voice, server, moderation, security
/log sent enabled:False                            # stop logging every sent message
/log show
```

### Boas-vindas, despedida e boosters

Mensagens, cargos automáticos e recompensas para os boosters do servidor.

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

Os membros abrem canais privados com um botão. Ao fechar, uma transcrição é enviada.

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

### Enquetes e sorteios

Botões para votar e participar. As durações aceitam valores como 30m, 2h e 1d.

```
/poll create question:Best game? options:Chess; Go; Poker duration:1d multiple:True
/poll end poll_id:3
/poll list

/giveaway start prize:Nitro duration:2d winners:2 role:@Member
/giveaway end giveaway_id:1
/giveaway reroll giveaway_id:1
/giveaway list
```

### Sugestões e starboard

Os membros enviam sugestões que a equipe pode aprovar ou negar, e mensagens populares ganham destaque.

```
/suggestion setup set channel:#suggestions review_role:@Staff
/suggest text:Add a music channel                  # also: !suggest Add a music channel
/suggestion status suggestion_id:4 status:approved reason:Planned for next month
# status: approved, denied, considering, implemented

/starboard setup channel:#starboard emoji:<any emoji> threshold:3 self_star:False
/starboard ignore channel:#spam
```

### XP e níveis

XP por chat e voz, cargos por nível, bônus por cargo e cartões de rank.

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

### Cargos por reação e notificações

Dê cargos com qualquer emoji e deixe os membros escolherem seus tópicos de notificação.

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

### Aniversários

Os membros informam dia e mês, e o bot dá um cargo e publica uma mensagem no dia.

```
/birthday setup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthday setup set message:Happy birthday {user}!

/birthday set day:14 month:3                       # members enter day and month only
/birthday show user:@User
/birthday upcoming
/birthday remove
```

### Canais de voz temporários

Entrar no canal hub cria uma sala que desaparece quando fica vazia.

```
/tempvoice setup hub:#Join-to-create category:Voice name:{name}'s room limit:0
# joining the hub creates a room for the member, empty rooms are deleted
```

### Backup e restauração

Os backups incluem cargos, canais, emojis, webhooks e cargos dos membros. A restauração só adiciona o que falta.

```
/backup create name:before-update
/backup schedule enabled:True interval_hours:24 keep:7 include_members:True include_emojis:True
/backup list
/backup download name:before-update
/backup restore name:before-update member_roles:True   # only adds what is missing
/backup delete name:before-update
```

### Dados e privacidade

Os membros podem exportar e apagar seus dados. Os administradores controlam por quanto tempo são mantidos.

```
/mydata export                                     # members download their own data
/mydata delete confirm:True                        # members delete their XP and birthday

/privacy retention days:90                         # delete data of members who left after 90 days
/privacy export user_id:123456789012345678
/privacy delete user_id:123456789012345678 cases:True
```

### Ferramentas de moderação

Limpar canais, gerir cargos e guardar notas privadas. Cada ação é registada.

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

### Informações

Consultar utilizadores, o servidor, cargos e o bot.

```
/userinfo user:@User
/serverinfo
/roleinfo role:@Moderator
/avatar user:@User
/help command:ban                                  # explains one command
/ping
/botinfo
```

### Anúncios, tags e lembretes

Escrever em nome do bot, criar comandos próprios, responder automaticamente a mensagens e definir lembretes.

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

### Mod-mail e recursos de banimento

Os membros escrevem à equipa através de um canal privado no servidor. Ninguém precisa de enviar uma mensagem direta ao bot.

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

### Canal de contagem, mensagens fixas e estatísticas

Um jogo de contagem, mensagens que ficam no fim de um canal e canais que mostram números em tempo real.

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

### Mais opções das funções existentes

Extras para tickets, sorteios, salas de voz, XP, aniversários, backups, registos e vistas de estado.

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

### Mais ferramentas do AutoMod

Seguir links encurtados, limitar links de membros novos, detetar ghost pings e testar regras sem punir ninguém.

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

### Limites dos moderadores e auditoria de permissões

Receber um alarme quando um moderador bane ou expulsa demasiado e ver que cargos têm permissões perigosas.

```
/modwatch status
/modwatch limit kind:ban count:5 window:1h                     # count 0 = no limit
/modwatch action action:alert notify_owner:False               # alert, timeout, strip, none
/modwatch exclude member:@TrustedMod

/permaudit run                                                  # roles with dangerous permissions and who holds them
/permaudit watch enabled:True                                   # alarm when a role or member gets one
/permaudit trust role:@Admin
```

### Denúncias e rastreio de convites

Os membros denunciam mensagens à equipa e o bot regista que convite trouxe cada novo membro.

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

### Diagnóstico e depuração

Encontrar permissões em falta e configurações quebradas, receber relatórios de erro num canal e exportar ou importar as configurações.

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

### Música

Reproduz links e ficheiros da pasta music num canal de voz. Os downloads são guardados como music/Artista/Álbum/Faixa. Precisa de ffmpeg e dos pacotes de requirements.txt.

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

Sem perdas: os seus próprios ficheiros (FLAC, WAV, ALAC) e as fontes que oferecem FLAC são reproduzidos sem alterações. YouTube, SoundCloud e sites semelhantes só oferecem áudio com perdas, que não pode ser tornado sem perdas depois. O Discord transmite a voz como Opus; o bot usa a taxa de bits do canal de voz. Responsabilidade: descarregar e reproduzir conteúdo pode violar os termos de um site ou os direitos de autor. Os downloads estão desativados por padrão e o módulo fica desativado até o ativar. Quem opera o bot é responsável pelo que é reproduzido e guardado.

### Configuração e estado de saúde

Um assistente guiado configura o essencial com botões e menus: canal de registos, canal de boas-vindas, cargos da equipa, o gulag, uma predefinição do AutoMod (leve, normal, rígida), um modelo de servidor (comunidade, jogos, suporte) e o idioma. /health mostra o que está configurado e o que falta. O idioma altera os textos que os membros veem, como as mensagens de boas-vindas predefinidas, os avisos do AutoMod, a verificação, os tickets, os recursos, o mod-mail e os menus de cargos. As respostas fixas aos administradores estão traduzidas, as que contêm nomes e números continuam em inglês.

```
/setup                                                         # buttons and menus, nothing is switched off by a template
/health                                                        # what is set up, what is open, and the self-test
/language code:de
```

### Economia

Uma moeda do servidor com recompensa diária, trabalho, pagamentos, classificação e uma loja cujos artigos podem dar um cargo. Ative-a com o módulo economy. Os comandos também funcionam com o prefixo, por exemplo !economy daily.

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

### Menus de cargos, mensagens agendadas e feeds

Os menus de cargos dão cargos com botões ou uma lista suspensa. As mensagens agendadas são publicadas uma vez ou repetidas de hora a hora, todos os dias ou todas as semanas. Os feeds publicam novos vídeos do YouTube, transmissões da Twitch e itens RSS. Para o YouTube use o ID do canal (começa por UC). A Twitch precisa de TWITCH_CLIENT_ID e TWITCH_CLIENT_SECRET no ficheiro .env. As horas escrevem-se como in 2h, 18:30 ou como data com hora, por exemplo 2026-12-24 18:00, no fuso horário do servidor. A primeira verificação de um feed apenas memoriza o que já existe.

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

### Atividade, ações em massa e pesquisa de casos

A atividade conta mensagens por canal e entradas e saídas por dia, nunca conteúdo nem nomes. As ações em massa banem, expulsam ou silenciam até 25 utilizadores após uma confirmação. Os casos podem ser pesquisados por utilizador, tipo, nome, motivo, moderador e antiguidade, e ligados entre si, por exemplo uma nota a um banimento.

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

### Anti-burla e anti-cripto

Remove sorteios falsos, como a típica burla do MrBeast, em texto e imagens em milissegundos. Os nomes da lista imediata são removidos na hora em qualquer grafia (MrBeast, Mr Beast, M R B E A S T, Mr.B3ast). Caso contrário, as palavras das listas (nomes, iscos, cripto, links, valores) somam-se e a mensagem é removida ao atingir o limite. As imagens são lidas por OCR, e uma imagem já classificada como burla é removida sem ser lida outra vez. Ler imagens requer tesseract; sem ele só o texto é verificado. Um servidor sobre o MrBeast pode retirar o nome da lista imediata ou excluir canais com /automod exemptchannel. Experimente com /antiscam test antes de confiar nele.

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

### Período de prova, deteção de enxame, linha do tempo e aprendizagem

O período de prova coloca os novos membros num cargo. Até escreverem o número definido de mensagens normais ou passarem os minutos, as ligações, convites e ficheiros são removidos com um aviso curto. A proteção contra raids também reconhece um enxame: várias contas novas com o mesmo padrão de nome, a mesma foto de perfil ou criadas com minutos de diferença. A linha do tempo (/case timeline) reúne por ordem cronológica a criação da conta, a entrada e o convite, o período de prova, os casos e os recursos de um utilizador. As mensagens nunca são guardadas, por isso não fazem parte dela. /block, /unblock e /blocklist gerem a lista de bloqueio do AutoMod com comandos curtos. Os moderadores ensinam o módulo anti-burla com a entrada de menu de contexto Mark as scam numa mensagem ou com uma reação com o emoji de learn_emoji: a mensagem é apagada e as suas imagens e o seu texto passam a ser removidos de imediato. Cada parte desativa-se com o seu módulo ou as suas definições.

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

### Criador de mensagens e atualizações

O criador de mensagens publica mensagens com vários embeds e botões de ligação a partir de JSON. Lê o JSON que os geradores de embeds como o Embed Generator exportam, por isso desenha uma mensagem lá e publica-a com o bot. Indique o JSON como texto, como ficheiro .json ou como ligação https que aponte diretamente para o JSON, por exemplo o ficheiro bruto de um repositório (ligações com redirecionamento são recusadas). Só são criados botões de ligação, os botões que precisam de uma interação são ignorados. Cada ligação tem de ser http ou https, as menções no texto nunca notificam e aplicam-se os limites do Discord. /message copy exporta uma mensagem existente como JSON, /message edit altera uma mensagem do bot e /message preview mostra o resultado só a si. As ligações de partilha de editores web não são abertas, porque o seu formato não é público.

```json
{
  "content": "Rules were updated",
  "embeds": [{"title": "Rules", "description": "Read them here.", "color": "#5865f2"}],
  "components": [{"type": 1, "components": [{"type": 2, "style": 5, "label": "Open rules", "url": "https://example.com/rules"}]}]
}
```

De 12 em 12 horas o bot verifica se o repositório do GitHub indicado em update.repo (definido com scripts/set_repo_url.py) tem uma versão mais recente. Se tiver, o dono do bot recebe uma mensagem direta com as notas da versão, e a versão é descarregada e verificada: soma SHA-256 da versão, caminhos seguros dentro do arquivo e uma versão que corresponde à etiqueta. Instala-se com /debug update action:install, ou sozinha se auto_install estiver ativo. Antes de instalar, os ficheiros substituídos são guardados em data/update, os novos pacotes são instalados e o novo código é importado como teste. Se algo falhar, os ficheiros antigos são restaurados. O seu .env, settings.json, data e music nunca são tocados. Depois o bot reinicia-se sozinho. No Docker nada é instalado no local, atualize antes a imagem. Uma atualização executa código do repositório, por isso aponte-a apenas para um repositório de confiança. Desative-a com enabled em false.

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

### Operação

O bot guarda os dados a cada poucos segundos e mantém cópias de segurança da base de dados em data/dbbackups, uma antes de cada alteração do formato dos dados e uma por dia. A fila de música, as mensagens fixas e os contadores dos moderadores sobrevivem a um reinício. Bots grandes podem funcionar com vários shards. Um ficheiro heartbeat e uma página de estado opcional ajudam as ferramentas de monitorização. Estas opções definem-se em settings.json:

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

### Administração

Ativar ou desativar módulos e comandos, mudar o prefixo, definir apelidos e limitar comandos a cargos.

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

## Marcadores nas mensagens

Estes marcadores são substituídos nos textos que você configurar:

```
/welcome set        message, dm, goodbye_message    {user} {name} {server} {count}
/booster set         message                         {user} {name} {server} {count}
/xp config           message                         {user} {name} {level}
/birthday setup set   message                         {user} {name}
/tempvoice setup     name                            {name}
/jailsetup notice    text                            {staff}
```

## Configuração

As opções globais ficam em settings.json. Todo o resto é configurado por servidor com comandos como /module, /command, /perms, /alias e /config.

Para renomear um comando, adicione-o em command_names e reinicie o bot:

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

Cada configuração pode ser lida e alterada com /config. Estes são os caminhos que você mais vai usar:

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

## Dados e armazenamento

Tudo que o bot guarda fica na sua própria máquina:

```
data/guardbot.db          settings, XP, birthdays and moderation cases (SQLite)
data/backups/<server>/    backup files (.json.gz)
settings.json             global options
.env                      the bot token
```

## Estrutura do repositório

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

## Traduções

O inglês é o idioma original do projeto. Todas as traduções da documentação, do painel e das mensagens do bot foram criadas com tradução automática e não foram verificadas por falantes nativos. Conte com expressões estranhas e erros, e por favor comunique-os ou envie uma correção. Os ficheiros estão em docs/ e guardbot/locales/.

## Roteiro

- Gráficos de atividade e moderação no painel.
- Revisão de todas as traduções por falantes nativos.
- Mais textos de resposta fixos traduzidos.

## Privacidade e segurança

- Sem telemetria. O bot comunica com o Discord e, para a verificação de atualizações, com o GitHub (não são enviados dados pessoais, desative com update.enabled). As ligações que os administradores lhe dão, como feeds, música e ligações JSON, só são abertas a pedido.
- Todos os dados ficam na pasta data da sua máquina: configurações, XP, aniversários (apenas dia e mês) e casos de moderação.
- O bot ignora mensagens diretas de membros.
- O token é lido do arquivo .env. Nunca o compartilhe nem o publique.
- Os membros podem exportar e apagar os próprios dados com /mydata. Os administradores definem por quanto tempo os dados de quem saiu são mantidos.
- [PRIVACY.md](../PRIVACY.md)

## Suporte

Bugs, ideias e sugestões: fale comigo no Discord, @justyyin, ou abra uma issue no GitHub.

## Créditos

O GuardBot é inspirado no [Embed Generator](https://github.com/merlinfuchs/embed-generator) de Merlin Fuchs (licença MIT, alojado em message.style). O criador de mensagens lê o mesmo formato JSON, por isso as mensagens desenhadas lá podem ser publicadas com este bot. Não está incluído código desse projeto. Obrigado aos autores de discord.py, aiohttp, Pillow, yt-dlp, mutagen e Tesseract.

## Licença

Publicado sob a licença MIT. Veja [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
