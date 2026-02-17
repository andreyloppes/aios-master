# Agent System Architecture

## Design Philosophy
Our multi-agent system is built on these principles (adapted from Synkra AIOS and OpenClaw):

### 1. Slash Command Activation
Each agent is a `/agents:name` command that injects a persona and behavioral instructions.
Located at: `~/.claude/commands/agents/`

### 2. Authority Boundaries
Each agent has a clear scope. Work outside scope is delegated to the appropriate agent.
This prevents context pollution and maintains quality.

### 3. Workflow Orchestration
Complex projects follow structured workflows (greenfield, story-cycle).
Located at: `~/.claude/commands/workflows/`

### 4. Memory Persistence
Cross-session state stored in `~/.claude/projects/*/memory/`
Each project can have its own memory context.

### 5. Cross-Project Operation
All commands are global (`~/.claude/commands/`), working across ANY project.
Project-specific context comes from the working directory.

## Agent Dependency Graph
```
                    Orion (Master)
                   /    |    \
                  /     |     \
    Morgan (PM) → River (SM) → Dex (Dev)
         |              |           |
    Atlas (Analyst)     |      Quinn (QA)
         |              |           |
    Uma (UX)      Pax (PO)    Gage (DevOps)
         |                          |
    Aria (Architect) ← Dara (Data)  |
         |                          |
         └──────── Craft (Squad) ───┘
```

## Workflow: Greenfield Full-Stack
```
Phase 0: devops → environment setup
Phase 1: analyst → pm → ux → architect → po (validate)
Phase 2: po → shard documents
Phase 3: sm → dev → qa → devops (repeat per story)
```

## File Locations
- Agent commands: ~/.claude/commands/agents/*.md
- Workflow commands: ~/.claude/commands/workflows/*.md
- Team commands: ~/.claude/commands/team/*.md
- Memory: ~/.claude/projects/-Users-andreylopes/memory/
- AIOS reference: /tmp/aios-core/ (cloned repo)

## Source Material
- 12 agent definitions extracted from github.com/SynkraAI/aios-core
- Workflow patterns from greenfield-fullstack.yaml
- Team coordination from agent-teams/team-all.yaml
- Autonomous patterns from OpenClaw, Auto-Claude, claude-flow research
