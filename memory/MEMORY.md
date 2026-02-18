# Agent System Memory

## Multi-Agent System (Built 2026-02-15)
12 specialized agents available via `/agents:*` slash commands.
Based on Synkra AIOS architecture, adapted for native Claude Code operation.

### Available Agents
| Command | Agent | Name | Role |
|---------|-------|------|------|
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

### Workflows (8 total)
| Command | Purpose |
|---------|---------|
| `/workflows:greenfield` | Full-stack project from concept to code |
| `/workflows:brownfield` | Enhance existing project (assess → plan → implement) |
| `/workflows:story-cycle` | SM → Dev → QA → DevOps loop |
| `/workflows:qa-loop` | Automated review cycle until PASS (max 5 iterations) |
| `/workflows:spec-pipeline` | Gather → Assess → Research → Write → Critique → Plan |
| `/workflows:progress` | Session continuity - save/load progress between sessions |
| `/workflows:auto` | Autonomous development - execute stories with minimal intervention |
| `/workflows:team-status` | Project and agent status report |

### Team Commands
| Command | Purpose |
|---------|---------|
| `/team:delegate` | Smart routing to the right agent |
| `/team:plan` | Multi-agent execution plan |

### Agent Authority Rules
- Only `/agents:devops` can push, create PRs, deploy
- `/agents:pm` plans, never implements
- `/agents:sm` creates stories, never codes
- `/agents:qa` reviews, never implements features
- `/agents:master` orchestrates, never emulates other agents

### Architecture Inspiration
- Source: github.com/SynkraAI/aios-core (MIT license)
- Patterns: OpenClaw (persistent identity), Auto-Claude (parallel terminals)
- See: [agents-architecture.md](agents-architecture.md) for detailed design

## Design System Reference: shadcn/ui
- Path: `/Users/andreylopes/shadcn-ui/`
- Version: v4 (latest, cloned 2026-02-16)
- **57 UI components**: button, card, dialog, form, table, sidebar, etc.
- **28 block templates**: dashboard, login, signup, sidebar layouts
- **70+ chart components**: area, bar, line, pie, radar, radial, tooltip
- **235 examples**: usage patterns for every component
- **3 project templates**: monorepo-next, start-app, vite-app
- Key paths:
  - Components: `apps/v4/registry/new-york-v4/ui/`
  - Blocks: `apps/v4/registry/new-york-v4/blocks/`
  - Charts: `apps/v4/registry/new-york-v4/charts/`
  - Examples: `apps/v4/registry/new-york-v4/examples/`
  - Styles/CSS: `apps/v4/styles/`
  - Templates: `templates/`
  - CLI tool source: `packages/shadcn/`

## CSS Framework Reference: Tailwind CSS v4
- Path: `/Users/andreylopes/tailwindcss/`
- Version: v4 (latest, cloned 2026-02-16) — reescrito em Rust (Oxide engine)
- Key packages:
  - `packages/tailwindcss/` — core (theme, utilities, preflight, design-system)
  - `packages/@tailwindcss-vite/` — plugin Vite
  - `packages/@tailwindcss-postcss/` — plugin PostCSS
  - `packages/@tailwindcss-cli/` — CLI standalone
  - `packages/@tailwindcss-upgrade/` — migração v3→v4
  - `packages/@tailwindcss-browser/` — runtime browser
  - `packages/internal-example-plugin/` — exemplo de plugin custom
- Key source files:
  - `packages/tailwindcss/theme.css` — todos os design tokens (462 linhas)
  - `packages/tailwindcss/preflight.css` — CSS reset (393 linhas)
  - `packages/tailwindcss/utilities.css` — entry das utilities
  - `packages/tailwindcss/src/design-system.ts` — engine do design system
  - `packages/tailwindcss/src/compat/` — compatibilidade v3 (colors, config, plugins)
- Rust engine: `crates/` (oxide, node bindings, classification macros)
- Playgrounds: `playgrounds/` (nextjs, vite, v3)

## Native Agent Teams (Ativado 2026-02-16)
- Feature: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` em `~/.claude/settings.json`
- Arquitetura: Team Lead + Teammates (instâncias independentes com contexto próprio)
- Comunicação: task list compartilhada + mailbox entre teammates
- Modos de exibição: `in-process` (terminal único) | `tmux` (split panes) | `auto`
- Atalhos: `Shift+Up/Down` (selecionar teammate), `Ctrl+T` (task list), `Shift+Tab` (delegate mode)
- Uso: "Create an agent team to [tarefa]" — spawna teammates em paralelo
- Custo: ~Nx tokens por N teammates (cada um é uma sessão completa)
- Limitações: sem /resume de teammates, 1 team por sessão, sem teams aninhados
- Complementa nossos `/agents:*` — skills dão a persona, Agent Teams dá a infraestrutura paralela

## MCP Servers Configurados
- **Figma (oficial)**: Remote MCP via `https://mcp.figma.com/mcp` (HTTP transport, OAuth)
  - Configurado em: `~/.claude.json` → project `/Users/andreylopes` → mcpServers
  - Autenticação: via `/mcp` → selecionar figma → Authenticate (browser OAuth flow)
  - Uso: colar link de frame/layer do Figma no prompt para extrair design context
- **Figma-Context-MCP (Framelink)**: Repo clonado em `/Users/andreylopes/figma-mcp-server/`
  - Source: github.com/GLips/Figma-Context-MCP
  - Uso alternativo via npx: `npx -y figma-developer-mcp --figma-api-key=KEY --stdio`
  - Simplifica dados do Figma para AI gerar código mais preciso

## PRO Module (Built 2026-02-17)
- Path: `~/claude-master/pro/` — 129 files, open-core premium layer
- Install: `./pro/setup.sh` (creates symlinks for PRO commands/workflows/skills)
- Data dir: `~/.claude-master-pro/data/` (sessions.jsonl, costs, backups)

### PRO Commands (5)
| Command | Purpose |
|---------|---------|
| `/pro:status` | System health and component status |
| `/pro:metrics` | Session analytics and performance metrics |
| `/pro:squad` | Activate industry squad overlay |
| `/pro:cost` | Token cost tracking and optimization |
| `/pro:report` | Generate professional reports (5 types) |

### PRO Workflows (4)
| Command | Purpose |
|---------|---------|
| `/workflows:client-onboarding` | 5-phase client pipeline |
| `/workflows:sprint-retro` | Automated retrospective from git/session data |
| `/workflows:cost-report` | Weekly cost analysis |
| `/workflows:deploy-pipeline` | 5-phase CI/CD (validate→quality→staging→prod→verify) |

### PRO Skills (3)
| Skill | Purpose |
|-------|---------|
| `cost-optimizer` | Token tracking, model routing, cache optimization |
| `analytics` | Velocity, quality, efficiency metrics |
| `client-report` | Professional report generation |

### Industry Squads (5)
| Squad | Agents | Domain |
|-------|--------|--------|
| `healthcare` | Clinix, Vera, Medis, Nexus | HIPAA/LGPD, HL7/FHIR, EHR |
| `marketing-agency` | Pixel, Dash, Campfire, Prism | Social APIs, A/B, UTM |
| `saas-startup` | Scaler, Pulse, Tenon, Funnel | Stripe, multi-tenant, PLG |
| `ecommerce` | Shelf, Catalog, Convert, Gate | PCI-DSS, checkout, inventory |
| `freelancer` | Solo, Brief, Scope, Ledger | Proposals, invoicing, tax |

### MCP Connectors (5)
google-sheets, notion, slack-discord, stripe, database — configs + setup + docs

### Production Scripts (8)
session-logger, cost-tracker, health-check, backup, cron-scheduler, webhook-receiver + 3 libs

### Dashboard
- Path: `~/claude-master/pro/dashboard/`
- Stack: Next.js 15 + shadcn/ui v4 + Tailwind v4 + Recharts
- Pages: Overview, Agents, Costs, Sessions

### Open-Core Licensing
- Path: `~/claude-master/open-core-pro-mvp/`
- Model: Core (MIT, free) + PRO (premium, licensed)
- Features: HMAC-SHA256 signed license keys, feature gates, tier system

## User Preferences
- Language: Portuguese (pt-BR) for communication
- Approach: Practical, hands-on, wants things working
- Interest: Automation, multi-agent systems, full-stack development

## PRO Monetization + Deploy Status (2026-02-17)
- Public pricing + checkout flow implemented in dashboard (`pro/dashboard/src/app/pricing`)
- License backend with public checkout + auto renewal/revocation via Stripe webhooks implemented in `pro/license-service`
- Stripe account status endpoint implemented: `GET /api/v1/admin/stripe/account`
- Admin dashboard now shows connected Stripe account/mode/webhook status

### Deploy done now
- Dashboard deployed to Vercel (account: `andreyloppes`)
- Production URL (project internal): `https://dashboard-nufzuw6sv-andreyloppes-projects.vercel.app`
- Public alias URL (working 200): `https://dashboard-five-kappa-84.vercel.app`

### Pending for next session
- Deploy `pro/license-service` to Hetzner/Railway/Render (user preferred Hetzner later)
- Configure real Stripe keys (`STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`)
- Point dashboard envs to license service (`LICENSE_SERVICE_URL`, `LICENSE_SERVICE_TOKEN`)
- Configure Stripe webhook endpoint in production

### Resale visibility mode
- Dashboard now supports visibility mode via env:
  - `NEXT_PUBLIC_DASHBOARD_MODE=owner` (Pricing + Admin visible)
  - `NEXT_PUBLIC_DASHBOARD_MODE=customer` (only Overview/Agents/Costs/Sessions)
- In `customer` mode, direct access to `/admin/*` and `/pricing` is blocked (404)
- Verified locally on 2026-02-17: `/` -> 200, `/admin` -> 404, `/pricing` -> 404 in `customer` mode

### Terminal Delivery (Version B) - 2026-02-18
- Added guided installer: `pro/install.sh`
- Installer supports `customer` vs `owner` profile, optional dashboard env generation, and dry-run mode
- Supports non-interactive resale flow:
  - `./install.sh --non-interactive --mode customer --license-key ... --license-service-url ...`
- `pro/setup.sh` now accepts license env checks:
  - `PRO_LICENSE_KEY`, `PRO_LICENSE_SERVICE_URL`, `SKIP_LICENSE_CHECK`
