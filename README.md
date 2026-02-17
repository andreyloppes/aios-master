# Claude Master

Sistema multi-agente completo para Claude Code, construido em Fevereiro de 2026.

Baseado na arquitetura [Synkra AIOS](https://github.com/SynkraAI/aios-core), adaptado para operacao nativa no Claude Code CLI.

## Estrutura

```
claude-master/
├── commands/                    # Slash commands (symlink → ~/.claude/commands/)
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
│   │   ├── greenfield.md        # Projeto do zero (conceito → codigo)
│   │   ├── brownfield.md        # Melhorar projeto existente
│   │   ├── story-cycle.md       # SM → Dev → QA → DevOps loop
│   │   ├── qa-loop.md           # Review automatico ate PASS (max 5x)
│   │   ├── spec-pipeline.md     # Gather → Assess → Research → Write → Critique → Plan
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
├── skills/                      # Skills (symlink → ~/.claude/skills/)
│   └── interface-design/        # Design de interfaces (dashboards, apps, tools)
│       ├── SKILL.md
│       └── references/
│           ├── critique.md
│           ├── example.md
│           ├── principles.md
│           └── validation.md
├── memory/                      # Memoria persistente (symlink → ~/.claude/projects/.../memory/)
│   ├── MEMORY.md                # Memoria principal (carregada no system prompt)
│   ├── agents-architecture.md   # Design detalhado do sistema de agentes
│   └── autonomous-patterns.md   # Padroes de operacao autonoma
├── config/                      # Backup das configuracoes (copia, nao symlink)
│   ├── settings.json            # Settings globais (Agent Teams habilitado)
│   ├── settings.local.json      # Permissoes locais
│   └── claude.json              # Config raiz (~/.claude.json) com MCP servers
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
| `/workflows:greenfield` | Projeto do zero: conceito → arquitetura → stories → codigo |
| `/workflows:brownfield` | Projeto existente: avaliar → planejar → implementar |
| `/workflows:story-cycle` | Ciclo: SM cria story → Dev implementa → QA revisa → DevOps entrega |
| `/workflows:qa-loop` | Loop de qualidade: review → fix → re-review ate PASS (max 5x) |
| `/workflows:spec-pipeline` | Pipeline: requisitos → avaliacao → pesquisa → spec → critica → plano |
| `/workflows:progress` | Salvar/carregar progresso entre sessoes |
| `/workflows:auto` | Modo autonomo: executa stories com intervencao minima |
| `/workflows:team-status` | Relatorio de status do projeto e agentes |

## Comandos de Equipe

| Comando | Descricao |
|---------|-----------|
| `/team:delegate` | Descreva a tarefa → roteamento automatico para o agente certo |
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

O sistema usa `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` para habilitar equipes nativas do Claude Code:

- **Skills** dao a persona e expertise a cada agente
- **Agent Teams** dao a infraestrutura de execucao paralela
- Comunicacao via task list compartilhada + mailbox
- Modos: `in-process` | `tmux` | `auto`

## MCP Servers

- **Figma (oficial)**: Remote MCP via OAuth para extrair design context
- **Figma-Context-MCP (Framelink)**: Simplifica dados do Figma para geracao de codigo

## Referencias Locais

- **shadcn/ui v4**: `/Users/andreylopes/shadcn-ui/` (57 components, 28 blocks, 70+ charts)
- **Tailwind CSS v4**: `/Users/andreylopes/tailwindcss/` (Oxide engine, Rust)

## Como Funciona

Este diretorio e a **fonte de verdade** de todo o sistema. O Claude Code acessa os arquivos via symlinks:

```
~/.claude/commands    → ~/claude-master/commands
~/.claude/skills      → ~/claude-master/skills
~/.claude/projects/-Users-andreylopes/memory → ~/claude-master/memory
```

Para recriar os symlinks (ex: apos mover a pasta), rode `./setup.sh`.

## Open-Core + Pro MVP

Para referencia de produto/licenciamento, existe um MVP executavel em:

`open-core-pro-mvp/`

Ele demonstra:

1. `core/` aberto sempre ativo.
2. `pro/` habilitado por `PRO_LICENSE_KEY`.
3. Feature flags com fallback seguro para core quando a licenca nao e valida.

Guia rapido:

```bash
cd open-core-pro-mvp
node cli.js status
node scripts/generate-demo-license.js advanced 2099-12-31 acme
```
