---
name: workflows:story-cycle
description: "Run the Story Development Cycle: create → implement → review → ship"
---

You are now coordinating the **Story Development Cycle** — the repeating loop that turns stories into shipped code.

## The Cycle
```
1. /agents:sm (River)    → Create the story with full details
2. /agents:dev (Dex)     → Implement the story
3. /agents:qa (Quinn)    → Review the implementation
4. /agents:devops (Gage) → Push and create PR
```

## How to Run

### Step 1: Identify the Next Story
Check:
- `docs/prd/` for the next epic
- `stories/` folder for existing stories and their status
- Find the next story that is NOT "Done"

### Step 2: Create Story (if not exists)
Tell user: "Invoke `/agents:sm` to create the next story from [epic-name]"

### Step 3: Implement
Tell user: "Invoke `/agents:dev` to implement [story-name]"

### Step 4: Review
Tell user: "Invoke `/agents:qa` to review the implementation"
- If PASS → Continue to Step 5
- If FAIL → Back to Step 3 with QA feedback
- If CONCERNS → User decides to fix or proceed

### Step 5: Ship
Tell user: "Invoke `/agents:devops` to push and create PR"

### Step 6: Next Story
Check if more stories remain. If yes, back to Step 1.
If all stories in epic are done, report epic completion.

## Status Tracking
After each step, update the story file status:
- Draft → Approved → In Progress → Review → Done

## Activation
1. Scan `stories/` and `docs/prd/` to find current progress
2. Determine which step of the cycle we're on
3. Guide user to the next action
