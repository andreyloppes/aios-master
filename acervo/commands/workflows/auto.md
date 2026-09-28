---
name: workflows:auto
description: "Autonomous development mode - execute multiple stories with minimal human intervention"
---

You are now in **Autonomous Development Mode** — executing stories with minimal human intervention.

## How It Works (inspired by Auto-Claude, ccswarm, and Anthropic's harness)

In this mode, you will:
1. Read the next story from the backlog
2. Implement it fully (code + tests)
3. Self-review using QA checklist
4. Fix any issues found
5. Commit with clear message
6. Move to the next story
7. Update progress after each story

## Prerequisites
- `docs/prd.md` or sharded docs in `docs/prd/` must exist
- `docs/fullstack-architecture.md` or equivalent must exist
- Stories must be created (in `stories/` folder)
- Git repo initialized

## Autonomous Loop

```
FOR each pending story:
  1. READ story requirements
  2. ANALYZE files that need changes
  3. IMPLEMENT the changes
  4. WRITE/UPDATE tests
  5. RUN tests (self-validate)
  6. SELF-REVIEW against checklist:
     - [ ] Acceptance criteria met?
     - [ ] Tests passing?
     - [ ] No lint errors?
     - [ ] No security issues?
     - [ ] Matches architecture?
  7. FIX any self-review issues
  8. GIT COMMIT with conventional message
  9. UPDATE docs/claude-progress.md
  10. REPORT: "Story X.Y complete. Moving to X.Z."
```

## Safety Rails
- **STOP if:** Test suite breaks completely (>50% failure)
- **STOP if:** Architecture violation detected
- **STOP if:** Security vulnerability introduced
- **ASK if:** Story is ambiguous or missing information
- **ASK if:** Need to add a new dependency
- **ASK if:** Need to modify shared infrastructure

## Quality Self-Check (after each story)
Before marking a story as done, verify:
1. All acceptance criteria from the story file are met
2. New code has tests
3. Existing tests still pass
4. No TypeScript/lint errors introduced
5. Code matches project patterns and conventions

## Context Management
- After every 3 stories, summarize progress to docs/claude-progress.md
- Use git commits as checkpoints (can rollback if needed)
- Keep implementation focused — don't refactor beyond story scope

## Activation
1. Scan `stories/` folder for pending stories
2. Present the list and ask: "Ready to start autonomous development? I'll implement stories sequentially and report after each one."
3. On confirmation, begin the loop
4. After each story, briefly report and continue unless there's a blocker
