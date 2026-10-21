# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | **Português** | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | [日本語](../ja/README.md) | [한국어](../ko/README.md)

Bot de Discord auto-hospedado para moderação, segurança e comunidade. Código aberto, gratuito, e os seus dados ficam no seu próprio computador.

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
- [Permissões do bot](#permissões-do-bot)
- [Primeiros passos no Discord](#primeiros-passos-no-discord)
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
  - [Administração](#administração-1)
- [Marcadores nas mensagens](#marcadores-nas-mensagens)
- [Configuração](#configuração)
- [Dados e armazenamento](#dados-e-armazenamento)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Roteiro](#roteiro)
- [Privacidade e segurança](#privacidade-e-segurança)
- [Suporte](#suporte)
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

### Administração

- Cada módulo e cada comando pode ser ativado ou desativado por servidor.
- Prefixo próprio, apelidos de comandos e comandos renomeáveis.
- Backup e restauração de cargos e da estrutura de canais.
- Backups automáticos agendados de cargos, canais, emojis e webhooks, com um comando de restauração que só adiciona o que falta.

## Status do projeto

O GuardBot é jovem e ainda não foi usado em servidores grandes. Os testes automáticos (`python -m unittest`) cobrem armazenamento, detecção de dados pessoais, cálculo de níveis, registro de comandos, verificações de permissão e os links da documentação. Tudo que precisa de um servidor Discord real, como lockdown, restauração de backup, verificação, anti-nuke e o gulag, não é coberto por eles. Teste esses recursos primeiro em um servidor de testes antes de depender deles. As traduções da documentação não foram revisadas por falantes nativos, correções são bem-vindas.

## Requisitos

- Python 3.11 ou mais recente
- Um aplicativo do Discord com token de bot
- Um computador ou VPS sempre online

## Início rápido

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

O guia completo passo a passo está em [GUIDE.md](GUIDE.md).

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
/case case_id:12

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
/suggestionsetup set channel:#suggestions review_role:@Staff
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

### Cargos por reação e notificações

Dê cargos com qualquer emoji e deixe os membros escolherem seus tópicos de notificação.

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

### Aniversários

Os membros informam dia e mês, e o bot dá um cargo e publica uma mensagem no dia.

```
/birthdaysetup set enabled:True role:@Birthday channel:#birthdays timezone:Europe/Berlin
/birthdaysetup set message:Happy birthday {user}!

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
/birthdaysetup set   message                         {user} {name}
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

## Roteiro

- Painel web local que roda na sua própria máquina, para alterar configurações sem nenhum serviço hospedado.
- Mensagens do bot traduzidas.
- Exportação e importação de configurações.

## Privacidade e segurança

- Sem telemetria e sem serviços externos. O bot só se comunica com o Discord.
- Todos os dados ficam na pasta data da sua máquina: configurações, XP, aniversários (apenas dia e mês) e casos de moderação.
- O bot ignora mensagens diretas de membros.
- O token é lido do arquivo .env. Nunca o compartilhe nem o publique.
- Os membros podem exportar e apagar os próprios dados com /mydata. Os administradores definem por quanto tempo os dados de quem saiu são mantidos.
- [PRIVACY.md](../PRIVACY.md)

## Suporte

Bugs, ideias e sugestões: fale comigo no Discord, @justyyin, ou abra uma issue no GitHub.

## Licença

Publicado sob a licença MIT. Veja [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
