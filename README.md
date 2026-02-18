<p align="center">
  <pre>
     █████╗ ██╗ ██████╗ ███████╗
    ██╔══██╗██║██╔═══██╗██╔════╝
    ███████║██║██║   ██║███████╗
    ██╔══██║██║██║   ██║╚════██║
    ██║  ██║██║╚██████╔╝███████║
    ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚══════╝
    ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗
    ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
    ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
  </pre>
</p>

<p align="center">
  <strong>Multi-Agent System for Claude Code CLI</strong><br>
  <em>12 agents · 8 workflows · 1 skill · ready to go</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/install-1%20command-green.svg" alt="Quick Install"></a>
</p>

---

## Quick Start

**One command** — paste in your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/andreyloppes/aios-master/main/bootstrap.sh | bash
```

Or install manually:

```bash
git clone https://github.com/andreyloppes/aios-master.git ~/claude-master
cd ~/claude-master && ./setup.sh
```

Then open **Claude Code** and use:

```
/agents:dev       build a REST API with Node.js
/agents:master    orchestrate the full team
/workflows:greenfield   create a new project from scratch
```

That's it. Your agents are ready.

---

## What You Get

### 12 Specialized Agents

| Command | Name | Role |
|---------|------|------|
| `/agents:dev` | **Dex** | Full Stack Developer |
| `/agents:qa` | **Quinn** | Quality Assurance & Code Review |
| `/agents:architect` | **Aria** | System Architect |
| `/agents:pm` | **Morgan** | Product Manager |
| `/agents:sm` | **River** | Scrum Master |
| `/agents:analyst` | **Atlas** | Business Analyst |
| `/agents:devops` | **Gage** | DevOps Engineer |
| `/agents:po` | **Pax** | Product Owner |
| `/agents:data-engineer` | **Dara** | Database Architect |
| `/agents:ux` | **Uma** | UX/UI Designer |
| `/agents:master` | **Orion** | Orchestrator (coordinates all agents) |
| `/agents:squad` | **Craft** | Squad Creator (assembles custom teams) |

Each agent has a persistent identity, defined expertise, and strict authority rules. They don't overlap — Dex codes, Quinn reviews, Gage deploys.

### 8 Automated Workflows

| Command | What it does |
|---------|-------------|
| `/workflows:greenfield` | New project from concept → architecture → stories → code |
| `/workflows:brownfield` | Improve existing project: assess → plan → implement |
| `/workflows:story-cycle` | Full cycle: SM creates story → Dev builds → QA reviews → DevOps ships |
| `/workflows:qa-loop` | Automated quality loop: review → fix → re-review until PASS (max 5x) |
| `/workflows:spec-pipeline` | Requirements → assessment → research → spec → critique → plan |
| `/workflows:progress` | Save/load session progress across conversations |
| `/workflows:auto` | Autonomous mode: executes stories with minimal intervention |
| `/workflows:team-status` | Project and agent status report |

### Team Commands

| Command | What it does |
|---------|-------------|
| `/team:delegate` | Describe a task → auto-routes to the right agent |
| `/team:plan` | Create a multi-agent execution plan for complex tasks |

### Design System Skill

| Command | What it does |
|---------|-------------|
| `/init` | Build UI with craft and consistency |
| `/critique` | Review and rebuild generic-looking UI |
| `/audit` | Check code against design system standards |
| `/extract` | Extract patterns from existing code |
| `/status` | Show current design system state |

---

## How It Works

AIOS Master installs via symlinks into Claude Code's configuration directory:

```
~/.claude/commands  →  ~/claude-master/commands
~/.claude/skills    →  ~/claude-master/skills
```

When you type `/agents:dev` in Claude Code, it loads the agent definition from the symlinked file. The agent's personality, expertise, rules, and memory are all defined in markdown — no external services, no API keys, no runtime dependencies.

### Authority Rules

Not every agent can do everything:

- **Only Gage** (`/agents:devops`) can push, create PRs, and deploy
- **Morgan** (`/agents:pm`) plans but never implements
- **River** (`/agents:sm`) creates stories but never codes
- **Quinn** (`/agents:qa`) reviews but never implements features
- **Orion** (`/agents:master`) orchestrates but never emulates other agents

### Agent Teams Integration

Works with Claude Code's native Agent Teams feature (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`):

- **AIOS agents** provide the persona and domain expertise
- **Agent Teams** provide parallel execution infrastructure
- Communication via shared task list + mailbox between teammates

---

## Project Structure

```
claude-master/
├── commands/
│   ├── agents/        # 12 agent definitions (.md)
│   ├── workflows/     # 8 workflow definitions (.md)
│   ├── team/          # delegate.md, plan.md
│   ├── audit.md       # Design system commands
│   ├── critique.md
│   ├── extract.md
│   ├── init.md
│   └── status.md
├── skills/
│   └── interface-design/
│       ├── SKILL.md
│       └── references/
├── memory/
│   ├── MEMORY.md                # Agent system memory
│   ├── agents-architecture.md   # Architecture design
│   └── autonomous-patterns.md   # Autonomy patterns
├── bootstrap.sh       # One-command installer
├── setup.sh           # Symlink creator
├── LICENSE            # MIT
└── README.md
```

---

## Updating

Pull the latest version:

```bash
cd ~/claude-master && git pull
```

Symlinks stay intact — the new files are immediately available in Claude Code.

---

## Uninstall

```bash
rm ~/.claude/commands ~/.claude/skills
rm -rf ~/claude-master
```

---

## PRO Module

Want more? **AIOS Master PRO** adds on top of Core:

- **5 PRO commands** — system status, metrics, cost tracking, reports
- **4 advanced workflows** — client onboarding, sprint retro, deploy pipeline
- **3 specialized skills** — cost optimizer, analytics, client reports
- **5 industry squads** — healthcare, marketing, SaaS, e-commerce, freelancer
- **5 MCP connectors** — Google Sheets, Notion, Slack, Stripe, Database
- **Production scripts** — session logger, cost tracker, health check, backup
- **Monitoring dashboard** — Next.js + real-time metrics

[Contact for PRO access →](https://github.com/andreyloppes)

---

## Credits

Architecture inspired by [Synkra AIOS](https://github.com/SynkraAI/aios-core) (MIT).

## License

[MIT](LICENSE) — use, modify, distribute freely.
