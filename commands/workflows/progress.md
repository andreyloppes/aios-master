---
name: workflows:progress
description: "Session continuity system - save/load progress between sessions (inspired by Anthropic's harness pattern)"
---

You are managing **Session Continuity** — ensuring work persists across conversation sessions.

## The Pattern (from Anthropic's Long-Running Agent Harness)
External artifacts become the agent's memory. Progress files and git history persist across sessions. Each new session reconstructs context from these artifacts.

## On Session Start (Loading)
1. Check if `docs/claude-progress.md` exists in the current project
2. If yes, read it to understand:
   - What was accomplished in previous sessions
   - What remains to be done
   - Any blockers or decisions pending
   - Current project phase
3. Check recent git log for additional context
4. Present a brief status summary to the user

## On Session End (Saving)
When the user says they're done or asks to save progress:

1. Create/update `docs/claude-progress.md` with:

```markdown
# Project Progress

## Last Updated: [date]

## Current Phase
[Phase name and description]

## Completed
- [x] [What was accomplished with dates]

## In Progress
- [ ] [What's currently being worked on]

## Next Steps
1. [What should happen next]
2. [Which agent to invoke]

## Decisions Made
- [Decision]: [Rationale] (date)

## Blockers
- [Any blocking issues]

## Files Changed (This Session)
- [file]: [what changed]

## Notes for Next Session
[Any context the next session needs to know]
```

2. Suggest committing the progress file to git

## Activation
Check if `docs/claude-progress.md` exists:
- If YES: Load it and present status summary
- If NO: Ask if user wants to start tracking progress, then create the file
