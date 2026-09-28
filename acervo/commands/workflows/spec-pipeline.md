---
name: workflows:spec-pipeline
description: "Full spec pipeline: gather requirements → assess → research → write spec → critique → plan"
---

You are now running the **Spec Pipeline** — a 6-phase process to turn ideas into actionable specifications.

## Pipeline Overview
```
Phase 1: Gather    → /agents:pm (Morgan) — elicit requirements
Phase 2: Assess    → /agents:architect (Aria) — assess complexity
Phase 3: Research  → /agents:analyst (Atlas) — research dependencies & patterns
Phase 4: Write     → /agents:pm (Morgan) — write formal spec
Phase 5: Critique  → /agents:qa (Quinn) — review spec quality
Phase 6: Plan      → /agents:sm (River) — break into stories
```

## Complexity Branching
After Phase 2 (Assess), route based on complexity:

**Simple** (1-2 stories, single domain):
→ Skip Phase 3 (Research), go directly to Phase 4 (Write)

**Medium** (3-5 stories, some unknowns):
→ Light research in Phase 3, then Phase 4

**Complex** (6+ stories, cross-domain, new tech):
→ Full research in Phase 3, architecture review, then Phase 4

## Phase Details

### Phase 1: Gather Requirements
**Agent:** `/agents:pm` (Morgan)
- Elicit user's vision, goals, constraints
- Identify personas and use cases
- Document functional and non-functional requirements
- **Output:** Requirements document

### Phase 2: Assess Complexity
**Agent:** `/agents:architect` (Aria)
- Evaluate technical complexity
- Identify architectural implications
- Flag unknowns and risks
- **Output:** Complexity assessment (Simple/Medium/Complex)

### Phase 3: Research (if Medium/Complex)
**Agent:** `/agents:analyst` (Atlas)
- Research technical dependencies
- Explore similar implementations
- Evaluate library/framework options
- **Output:** Research findings

### Phase 4: Write Specification
**Agent:** `/agents:pm` (Morgan)
- Create formal PRD/spec document
- Include all requirements, constraints, decisions
- Reference research findings
- **Output:** `docs/prd.md` or `docs/spec.md`

### Phase 5: Critique
**Agent:** `/agents:qa` (Quinn)
- Review spec for completeness
- Check for ambiguities and contradictions
- Verify testability of requirements
- **Output:** Critique report with suggested improvements

### Phase 6: Plan
**Agent:** `/agents:sm` (River)
- Break spec into implementable stories
- Define story sequence and dependencies
- Estimate complexity per story
- **Output:** Story backlog ready for development

## Activation
1. Ask the user what they want to build
2. Start with Phase 1 (Gather) using `/agents:pm`
3. Progress through phases based on complexity assessment
