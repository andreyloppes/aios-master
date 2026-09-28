---
name: obsidian
description: "Interact with Obsidian vault via CLI - capture notes, search knowledge, log decisions, manage daily journal"
---

# Obsidian Vault Integration

You have access to the user's Obsidian vault via CLI. The Obsidian app must be running.

## Quick Actions

Based on what the user asks, execute the appropriate action:

### "capture" / "anotar" / "salvar nota"
Create a note in INBOX:
```bash
obsidian create path="INBOX/$(date +%Y-%m-%d)-<slug>.md" content="---\ntags: [inbox]\ndate: $(date +%Y-%m-%d)\n---\n\n<content>"
```

### "buscar" / "search" / "procurar"
Search the vault:
```bash
obsidian search:context query="<term>"
```

### "daily" / "diário"
Read or append to daily note:
```bash
obsidian daily:read
obsidian daily:append content="\n<content>"
```

### "ler" / "read"
Read a specific note:
```bash
obsidian read file="<name>"
```

### "decisão" / "decision"
Log an architectural/product decision:
```bash
obsidian create path="PROJECTS/<project>/decisions/$(date +%Y-%m-%d)-<slug>.md" content="---\ntags: [decision]\ndate: $(date +%Y-%m-%d)\n---\n\n# <title>\n\n## Contexto\n<context>\n\n## Decisão\n<decision>\n\n## Consequências\n<consequences>"
```

### "recurso" / "resource" / "referência"
Save reference material:
```bash
obsidian create path="RESOURCES/<category>/<topic>.md" content="---\ntags: [resource, <domain>]\ndate: $(date +%Y-%m-%d)\n---\n\n# <Topic>\n\n<content>"
```

### "tarefas" / "tasks"
List pending tasks:
```bash
obsidian tasks todo
```

## Rules
- PARA structure: INBOX (capture) → PROJECTS (active) → AREAS (ongoing) → RESOURCES (reference) → ARCHIVES (done)
- Always add frontmatter with tags and date
- Search before creating to avoid duplicates
- Never delete without asking
- Obsidian app must be running for CLI to work
