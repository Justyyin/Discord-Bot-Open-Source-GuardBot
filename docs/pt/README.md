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
- [Estrutura do repositório](#estrutura-do-repositório)
- [Comandos](#comandos)
- [Configuração](#configuração)
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

## Comandos

A maioria dos comandos são comandos slash, os de moderação também funcionam com prefixo. A lista completa está na referência de comandos: [COMMANDS.md](../COMMANDS.md).

## Configuração

As opções globais ficam em settings.json. Todo o resto é configurado por servidor com comandos como /module, /command, /perms, /alias e /config.

Para renomear um comando, adicione-o em command_names e reinicie o bot:

```json
{
  "prefix": "!",
  "command_names": {
    "warn": "verwarnen"
  }
}
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
