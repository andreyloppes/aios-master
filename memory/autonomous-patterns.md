# Autonomous Agent Patterns Research (2026-02-15)

## Best Patterns Discovered (from 10+ systems analyzed)

### 1. Memory Persistence (ranked by sophistication)
- **File-based (OpenClaw)**: MEMORY.md + daily logs (YYYY-MM-DD.md), simple and grep-searchable
- **Progress files (Anthropic harness)**: claude-progress.txt + git history as external memory
- **SQLite-based (claude-flow)**: 12 tables with semantic search, pattern recognition
- **Session pooling (ccswarm)**: 93% token reduction through session reuse

### 2. Context Window Management
- **Progressive Disclosure (wshobson/agents)**: Three-tier: metadata always (~50 tokens), instructions on activation, resources on demand. ~300 tokens per plugin!
- **Compression (claude-mem)**: 10,000-token observations → 500 tokens (10x savings)
- **Token Optimization (claude-flow)**: 32.3% reduction via WASM, model routing

### 3. Multi-Agent Orchestration
- **Queen/Hive (claude-flow)**: Queen coordinator + specialized workers, shared SQLite memory
- **Master-Worker + Worktrees (ccswarm, Auto-Claude)**: Git worktree isolation for parallel work
- **@Mention Routing (Agentrooms)**: Direct @agent-name addressing
- **TeammateTool (Claude Code native)**: JSON inbox messaging, shared task queues

### 4. Continuous Operation
- **Heartbeat Daemon (OpenClaw)**: Background process, configurable intervals, HEARTBEAT.md checklist
- **Initializer + Loop (Anthropic)**: Each session reads progress file → works → updates file
- **ProactiveMaster (ccswarm)**: 30-second intervals, velocity tracking, auto task generation

### 5. System Prompt Architecture
- **Multi-file Assembly (OpenClaw)**: AGENTS.md + SOUL.md + IDENTITY.md + USER.md per-turn
- **YAML Frontmatter (claude-flow)**: Name, type, capabilities, hooks in YAML
- **CLAUDE.md Templates**: Project-type-specific, loaded by all agents

## Key Systems Analyzed
- OpenClaw (60k+ stars): Hub-spoke gateway, file-based memory, heartbeat daemon
- claude-flow (500k downloads): SQLite memory, 60+ agents, WASM optimization
- ccswarm (Rust): ProactiveMaster, git worktrees, 93% token reduction
- Auto-Claude: 12 parallel Claude terminals, git worktree isolation
- wshobson/agents: 112 agents, 3-tier progressive disclosure
- Anthropic's harness: Initializer + Coding agent, progress files
- Claude Code Agent Teams (native): TeammateTool, JSON inboxes, experimental

## Sources
See full report in task output: /private/tmp/claude-501/-Users-andreylopes/tasks/a6d000e.output
