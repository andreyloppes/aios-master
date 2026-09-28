---
name: obsidian
description: "Obsidian CLI integration for reading, writing, searching, and managing notes in the user's vault. Use when agents need to capture knowledge, log decisions, search existing notes, or interact with the Obsidian vault."
license: MIT
metadata:
  author: https://github.com/andreyloppes
  version: "1.0.0"
  domain: knowledge-management
  triggers: obsidian, vault, notes, knowledge, brain, cerebro, daily, journal
  role: specialist
  scope: integration
  output-format: markdown
  related-skills: markdown-mermaid-writing, prompt-engineer
---

# Obsidian CLI Integration

Bridge between AIOS-MASTER agents and the Obsidian vault via CLI v1.12+.

## Prerequisites

- Obsidian Desktop v1.12.4+ installed at `/Applications/Obsidian.app`
- CLI enabled in Settings > General > Advanced > Command line interface
- PATH configured: `/Applications/Obsidian.app/Contents/MacOS`
- Obsidian app must be running for CLI to work

## Vault Structure (PARA)

```
Documents/                 # Vault root (iCloud sync)
├── INBOX/                 # Quick capture, unprocessed
├── JOURNAL/Daily/         # Daily notes
├── PROJECTS/              # Active projects
├── AREAS/                 # Ongoing responsibilities
├── RESOURCES/             # Reference material
├── ARCHIVES/              # Completed/inactive
├── DASHBOARDS/            # MOCs and overviews
└── TEMPLATES/             # Note templates
```

## CLI Base Command

All commands use: `obsidian <command> [options]`

Files resolve by name (like wikilinks) or exact path.

## Core Operations

### 1. Create Note

```bash
# Quick capture to INBOX
obsidian create path="INBOX/note-name.md" content="---\ntags: [capture]\ndate: $(date +%Y-%m-%d)\n---\n\nContent here"

# Project note
obsidian create path="PROJECTS/project-name/note.md" content="content" template="template-name"
```

### 2. Read Note

```bash
obsidian read file="note-name"
obsidian read path="PROJECTS/O2/note.md"
```

### 3. Append/Prepend to Note

```bash
obsidian append file="note-name" content="\n## New Section\nContent"
obsidian prepend file="note-name" content="Updated: $(date +%Y-%m-%d)\n"
```

### 4. Daily Note

```bash
obsidian daily:read                    # Read today's daily
obsidian daily:append content="text"   # Append to daily
obsidian daily:prepend content="text"  # Prepend to daily
obsidian daily:path                    # Get daily note path
```

### 5. Search

```bash
obsidian search query="search term"              # File paths only
obsidian search:context query="search term"       # With matching lines
obsidian search query="term" path="PROJECTS"      # Scoped to folder
```

### 6. Tags & Properties

```bash
obsidian tags                                     # List all tags
obsidian tags file="note-name"                    # Tags for specific file
obsidian property:set name="status" value="done" file="note"
obsidian property:read name="status" file="note"
```

### 7. Tasks

```bash
obsidian tasks todo                               # All incomplete tasks
obsidian tasks done                               # All completed tasks
obsidian tasks file="note-name"                   # Tasks in specific file
obsidian task file="note" line=5 toggle           # Toggle task status
```

### 8. Files & Folders

```bash
obsidian files folder="PROJECTS"                  # List files in folder
obsidian folders                                  # List all folders
obsidian file file="note-name"                    # File info
obsidian move file="note" to="ARCHIVES"           # Move file
obsidian delete file="note"                       # Delete (to trash)
```

### 9. Backlinks & Links

```bash
obsidian backlinks file="note-name"               # Who links to this
obsidian links file="note-name"                   # Outgoing links
obsidian orphans                                  # Files with no backlinks
obsidian deadends                                 # Files with no outgoing links
```

## Agent Integration Patterns

### Pattern 1: Agent Decision Log

When an agent makes an important architectural or product decision:

```bash
obsidian create path="PROJECTS/<project>/decisions/$(date +%Y-%m-%d)-<slug>.md" content="---\ntags: [decision, <agent>]\ndate: $(date +%Y-%m-%d)\nagent: <agent-name>\nstatus: decided\n---\n\n# Decision: <title>\n\n## Context\n<why this decision was needed>\n\n## Decision\n<what was decided>\n\n## Consequences\n<trade-offs and implications>"
```

### Pattern 2: Daily Standup Capture

Agents append their progress to the daily note:

```bash
obsidian daily:append content="\n## Agent: <name> | $(date +%H:%M)\n- **Status**: <what was done>\n- **Next**: <what's planned>\n- **Blockers**: <any issues>"
```

### Pattern 3: Knowledge Capture

When research or learning happens during a session:

```bash
obsidian create path="RESOURCES/<category>/<topic>.md" content="---\ntags: [resource, <domain>]\ndate: $(date +%Y-%m-%d)\nsource: <url-or-context>\n---\n\n# <Topic>\n\n<content>"
```

### Pattern 4: Quick Inbox Capture

Fast capture for processing later:

```bash
obsidian create path="INBOX/$(date +%Y-%m-%d)-<slug>.md" content="---\ntags: [inbox]\ndate: $(date +%Y-%m-%d)\n---\n\n<content>"
```

### Pattern 5: Search Before Create

Always check if a note exists before creating duplicates:

```bash
obsidian search query="topic name" path="RESOURCES"
# If no results, then create
```

## Constraints

### MUST DO
- Always check if Obsidian app is running before CLI calls
- Use `path=` for exact locations, `file=` for name-based resolution
- Escape special characters in content (quotes, newlines)
- Search before creating to avoid duplicates
- Follow PARA structure for note placement
- Use frontmatter (YAML) with tags and date on every new note

### MUST NOT
- Never delete notes without explicit user confirmation
- Never modify notes in ARCHIVES without asking
- Never create notes outside the PARA structure
- Never run `obsidian restart` or `obsidian reload` without asking
- Never use `permanent` flag on delete (always use trash)

## Quick Reference

| Action | Command |
|--------|---------|
| Capture idea | `obsidian create path="INBOX/..."` |
| Log to daily | `obsidian daily:append content="..."` |
| Search vault | `obsidian search query="..."` |
| Read note | `obsidian read file="..."` |
| Add to note | `obsidian append file="..." content="..."` |
| Move note | `obsidian move file="..." to="..."` |
| List tasks | `obsidian tasks todo` |
| Check backlinks | `obsidian backlinks file="..."` |
