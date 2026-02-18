# Agent System Memory

## Multi-Agent System
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
| `/workflows:brownfield` | Enhance existing project (assess -> plan -> implement) |
| `/workflows:story-cycle` | SM -> Dev -> QA -> DevOps loop |
| `/workflows:qa-loop` | Automated review cycle until PASS (max 5 iterations) |
| `/workflows:spec-pipeline` | Gather -> Assess -> Research -> Write -> Critique -> Plan |
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

## User Preferences
- Language: (your preferred language)
- Approach: (your working style)
- Interest: (your focus areas)
