---
name: workflows:qa-loop
description: "Automated QA review cycle: review → fix → re-review until PASS"
---

You are now running the **QA Review Loop** — an iterative quality cycle.

## The Loop
```
1. /agents:qa reviews code → PASS/CONCERNS/FAIL
2. If FAIL: /agents:dev fixes issues
3. Re-review (max 5 iterations)
4. If still FAIL after 5: escalate to /agents:architect
```

## Process

### Iteration 1: Initial Review
**Agent:** `/agents:qa` (Quinn)
- Run full 10-phase review
- Produce verdict with specific findings

### On PASS:
- Done! Proceed to `/agents:devops` for push/PR

### On CONCERNS:
- List concerns for user decision
- User can: fix now, fix later, or accept as-is

### On FAIL:
- `/agents:dev` addresses CRITICAL and IMPORTANT findings
- Focus on specific file:line references from QA report
- Run tests to verify fixes

### Re-Review (Iterations 2-5):
- `/agents:qa` re-reviews ONLY the changed files
- Checks that previous findings are resolved
- May find new issues from the fixes

### Escalation (After 5 FAILs):
- Escalate to `/agents:architect` for design-level review
- The issue may be architectural, not just code quality

## Quality Gate Criteria
```
PASS requirements:
- [ ] No CRITICAL findings
- [ ] No IMPORTANT security findings
- [ ] Test coverage >= 80% on new code
- [ ] All existing tests still pass
- [ ] No new TypeScript/linting errors
```

## Activation
1. Identify what code needs review (files, PR, or story implementation)
2. Start the QA loop with `/agents:qa`
3. Track iteration count
4. Guide through fix → re-review cycle
