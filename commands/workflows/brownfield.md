---
name: workflows:brownfield
description: "Enhance an existing project - analyze, plan improvements, and implement changes"
---

You are now executing the **Brownfield Enhancement Workflow** — a structured process to improve existing projects.

## Workflow Overview
```
Phase 0: Discovery & Assessment    → /agents:analyst + /agents:architect
Phase 1: Enhancement Planning      → /agents:pm + /agents:po
Phase 2: Implementation Cycle      → /agents:sm → /agents:dev → /agents:qa → /agents:devops
```

## Phase Detection
Scan the project to determine state:
- Has existing code but no docs/ → Start at Phase 0
- Has docs/brownfield-assessment.md → Phase 0 done
- Has docs/prd.md with enhancement epics → Phase 1 done
- Has stories/ folder → Phase 2 active

## Phase 0: Discovery & Assessment

### Step 0.1: Codebase Analysis
**Agent:** `/agents:analyst` (Atlas)
**Actions:**
1. Scan project structure (package.json, framework, dependencies)
2. Identify tech stack and patterns used
3. Map code organization and architecture
4. Identify tech debt and improvement areas
**Output:** `docs/brownfield-assessment.md`

### Step 0.2: Architecture Review
**Agent:** `/agents:architect` (Aria)
**Actions:**
1. Review current architecture against best practices
2. Identify scalability bottlenecks
3. Assess security posture
4. Recommend architecture improvements
**Output:** `docs/architecture-review.md`

### Step 0.3: Database Audit (if applicable)
**Agent:** `/agents:data-engineer` (Dara)
**Actions:**
1. Review schema design and indexes
2. Check for N+1 queries, missing indexes
3. Assess migration history
4. Recommend optimizations
**Output:** `docs/database-audit.md`

## Phase 1: Enhancement Planning

### Step 1.1: Create Enhancement PRD
**Agent:** `/agents:pm` (Morgan)
**Input:** Assessment documents from Phase 0
**Actions:**
1. Prioritize improvements by impact/effort
2. Create enhancement PRD with epics
3. Define success metrics
**Output:** `docs/prd.md`

### Step 1.2: Validate Plan
**Agent:** `/agents:po` (Pax)
**Input:** Enhancement PRD
**Actions:**
1. Validate completeness and consistency
2. Prioritize backlog
3. Shard into dev-ready chunks
**Output:** Validated PRD + sharded docs

## Phase 2: Implementation Cycle
Same as greenfield Phase 3:
```
/agents:sm → Create story from enhancement epic
/agents:dev → Implement changes
/agents:qa → Review (critical for brownfield - regression risk!)
/agents:devops → Push and PR
```

**CRITICAL for Brownfield:**
- QA review is MANDATORY (not optional) — regression risk is high
- Every change must include tests for existing behavior
- Incremental PRs — small, focused changes, not big rewrites

## Activation
1. Scan the existing project structure
2. Determine current phase
3. Guide user to the next agent
