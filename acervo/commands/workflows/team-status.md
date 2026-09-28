---
name: workflows:team-status
description: "Show the status of all agents and current project progress"
---

You are providing a **Team Status Report** for the current project.

## Instructions
1. Scan the current project directory structure
2. Check for planning documents in `docs/`
3. Check for stories in `stories/`
4. Check git status for recent activity
5. Present a comprehensive status report

## Report Format

```markdown
# Team Status Report
**Project:** [detected from directory/package.json]
**Date:** [current date]

## Project Phase
[Phase 0/1/2/3] — [phase name and description]

## Planning Artifacts
| Document | Status | Location |
|----------|--------|----------|
| Project Brief | [exists/missing] | docs/project-brief.md |
| PRD | [exists/missing] | docs/prd.md |
| Frontend Spec | [exists/missing] | docs/front-end-spec.md |
| Architecture | [exists/missing] | docs/fullstack-architecture.md |
| Sharded Docs | [exists/missing] | docs/prd/ |

## Stories Progress
| Epic | Total Stories | Done | In Progress | Pending |
|------|-------------|------|-------------|---------|
| [epic] | [n] | [n] | [n] | [n] |

## Recent Activity
[Last 5 git commits or file changes]

## Next Steps
1. [What should happen next]
2. [Which agent to invoke]

## Available Agents
| Command | Agent | Ready |
|---------|-------|-------|
| /agents:dev | Dex (Developer) | Ready |
| /agents:qa | Quinn (QA) | Ready |
| /agents:architect | Aria (Architect) | Ready |
| /agents:pm | Morgan (PM) | Ready |
| /agents:sm | River (SM) | Ready |
| /agents:analyst | Atlas (Analyst) | Ready |
| /agents:devops | Gage (DevOps) | Ready |
| /agents:po | Pax (PO) | Ready |
| /agents:data-engineer | Dara (Data Eng) | Ready |
| /agents:ux | Uma (UX/UI) | Ready |
| /agents:master | Orion (Orchestrator) | Ready |
| /agents:squad | Craft (Squad Creator) | Ready |
```

## Activation
Immediately scan the project and generate the status report. No greeting needed — just deliver the report.
