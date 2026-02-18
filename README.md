# Claude Master

> A complete multi-agent system for Claude Code CLI.

Sistema multi-agente completo para Claude Code, construido em Fevereiro de 2026.

Baseado na arquitetura [Synkra AIOS](https://github.com/SynkraAI/aios-core), adaptado para operacao nativa no Claude Code CLI.

## Estrutura

```
claude-master/
├── commands/                    # Slash commands (symlink -> ~/.claude/commands/)
│   ├── agents/                  # 12 agentes especializados
│   │   ├── dev.md               # Dex - Full Stack Developer
│   │   ├── qa.md                # Quinn - Quality & Review
│   │   ├── architect.md         # Aria - System Architect
│   │   ├── pm.md                # Morgan - Product Manager
│   │   ├── sm.md                # River - Scrum Master
│   │   ├── analyst.md           # Atlas - Business Analyst
│   │   ├── devops.md            # Gage - DevOps Engineer
│   │   ├── po.md                # Pax - Product Owner
│   │   ├── data-engineer.md     # Dara - Database Architect
│   │   ├── ux.md                # Uma - UX/UI Designer
│   │   ├── master.md            # Orion - Orchestrator
│   │   └── squad.md             # Craft - Squad Creator
│   ├── workflows/               # 8 workflows automatizados
│   │   ├── greenfield.md        # Projeto do zero (conceito -> codigo)
│   │   ├── brownfield.md        # Melhorar projeto existente
│   │   ├── story-cycle.md       # SM -> Dev -> QA -> DevOps loop
│   │   ├── qa-loop.md           # Review automatico ate PASS (max 5x)
│   │   ├── spec-pipeline.md     # Gather -> Assess -> Research -> Write -> Critique -> Plan
│   │   ├── progress.md          # Continuidade entre sessoes
│   │   ├── auto.md              # Desenvolvimento autonomo
│   │   └── team-status.md       # Status do projeto e agentes
│   ├── team/                    # Comandos de equipe
│   │   ├── delegate.md          # Roteamento inteligente
│   │   └── plan.md              # Plano multi-agente
│   ├── audit.md                 # Auditoria de design system
│   ├── critique.md              # Critica e rebuild de UI
│   ├── extract.md               # Extrair padroes de codigo existente
│   ├── init.md                  # Inicializar UI com consistencia
│   └── status.md                # Estado atual do design system
├── skills/                      # Skills (symlink -> ~/.claude/skills/)
│   └── interface-design/        # Design de interfaces (dashboards, apps, tools)
│       ├── SKILL.md
│       └── references/
│           ├── critique.md
│           ├── example.md
│           ├── principles.md
│           └── validation.md
├── memory/                      # Memoria persistente do sistema
│   ├── MEMORY.md                # Memoria principal (carregada no system prompt)
│   ├── agents-architecture.md   # Design detalhado do sistema de agentes
│   └── autonomous-patterns.md   # Padroes de operacao autonoma
├── LICENSE                      # MIT License
├── README.md                    # Este arquivo
└── setup.sh                     # Script para recriar symlinks
```

## Agentes

| Comando | Agente | Nome | Papel |
|---------|--------|------|-------|
| `/agents:dev` | dev | Dex | Full Stack Developer |
| `/agents:qa` | qa | Quinn | Quality & Review |
| `/agents:architect` | architect | Aria | System Architect |
| `/agents:pm` | pm | Morgan | Product Manager |
| `/agents:sm` | sm | River | Scrum Master |
| `/agents:analyst` | analyst | Atlas | Business Analyst |
| `/agents:devops` | devops | Gage | DevOps Engineer |
| `/agents:po` | po | Pax | Product Owner |
| `/agents:data-engineer` | data-eng | Dara | Database Architect |
| `/agents:ux` | ux | Uma | UX/UI Designer |
| `/agents:master` | master | Orion | Orchestrator |
| `/agents:squad` | squad | Craft | Squad Creator |

### Regras de Autoridade

- Somente **Gage** (`/agents:devops`) pode: push, criar PRs, deploy
- **Morgan** (`/agents:pm`) planeja, nunca implementa
- **River** (`/agents:sm`) cria stories, nunca codifica
- **Quinn** (`/agents:qa`) revisa, nunca implementa features
- **Orion** (`/agents:master`) orquestra, nunca emula outros agentes

## Workflows

| Comando | Descricao |
|---------|-----------|
| `/workflows:greenfield` | Projeto do zero: conceito -> arquitetura -> stories -> codigo |
| `/workflows:brownfield` | Projeto existente: avaliar -> planejar -> implementar |
| `/workflows:story-cycle` | Ciclo: SM cria story -> Dev implementa -> QA revisa -> DevOps entrega |
| `/workflows:qa-loop` | Loop de qualidade: review -> fix -> re-review ate PASS (max 5x) |
| `/workflows:spec-pipeline` | Pipeline: requisitos -> avaliacao -> pesquisa -> spec -> critica -> plano |
| `/workflows:progress` | Salvar/carregar progresso entre sessoes |
| `/workflows:auto` | Modo autonomo: executa stories com intervencao minima |
| `/workflows:team-status` | Relatorio de status do projeto e agentes |

## Comandos de Equipe

| Comando | Descricao |
|---------|-----------|
| `/team:delegate` | Descreva a tarefa -> roteamento automatico para o agente certo |
| `/team:plan` | Crie um plano de execucao multi-agente para tarefas complexas |

## Design System (Skills)

| Comando | Descricao |
|---------|-----------|
| `/init` | Construir UI com craft e consistencia |
| `/critique` | Criticar build e reconstruir o que ficou generico |
| `/audit` | Verificar codigo contra design system |
| `/extract` | Extrair padroes de codigo existente |
| `/status` | Mostrar estado atual do design system |

## Integracao com Agent Teams

O sistema suporta `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` para habilitar equipes nativas do Claude Code:

- **Skills** dao a persona e expertise a cada agente
- **Agent Teams** dao a infraestrutura de execucao paralela
- Comunicacao via task list compartilhada + mailbox
- Modos: `in-process` | `tmux` | `auto`

## Como Funciona

Este diretorio e a **fonte de verdade** de todo o sistema. O Claude Code acessa os arquivos via symlinks:

```
~/.claude/commands    -> ~/claude-master/commands
~/.claude/skills      -> ~/claude-master/skills
~/.claude/projects/<project>/memory -> ~/claude-master/memory
```

Para recriar os symlinks (ex: apos mover a pasta), rode `./setup.sh`.

## Instalacao

Clone o repositorio e execute o setup:

```bash
git clone https://github.com/andreyloppes/claude-master.git ~/claude-master
cd ~/claude-master
chmod +x setup.sh
./setup.sh
```

Ou instale via bootstrap (1 comando):

```bash
curl -fsSL https://raw.githubusercontent.com/andreyloppes/claude-master/main/bootstrap.sh | \
  bash -s -- --edition core
```

## PRO Module

Quer ir alem? O **Claude Master PRO** adiciona ao Core:

- **5 comandos PRO**: status, metrics, squad, cost, report
- **4 workflows avancados**: client-onboarding, sprint-retro, cost-report, deploy-pipeline
- **3 skills especializadas**: cost-optimizer, analytics, client-report
- **5 squads de industria**: healthcare, marketing-agency, saas-startup, ecommerce, freelancer
- **5 conectores MCP**: Google Sheets, Notion, Slack/Discord, Stripe, Database
- **Dashboard**: Next.js + shadcn/ui com metricas em tempo real
- **Scripts de producao**: session-logger, cost-tracker, health-check, backup, cron e mais

Para mais informacoes sobre o PRO, visite: [https://github.com/andreyloppes/claude-master-pro](https://github.com/andreyloppes/claude-master-pro)

## Licenca

[MIT](LICENSE) - Use, modifique, distribua livremente.
