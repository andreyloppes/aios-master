# Upstream — de onde veio o que é de terceiros

Nada daqui é carregado direto. O conteúdo útil foi copiado para `skills/`, `commands/` e `agents/` e é mantido como nosso.
Para atualizar uma peça: `scripts/upstream.sh <repo>` clona o upstream no `/tmp` e mostra o diff contra a nossa cópia.

| Repo | URL | Commit de referência | O que usamos |
|---|---|---|---|
| `agentsys` | https://github.com/avifenesh/agentsys.git | `b18e85b` | nada — referência |
| `alirezarezvani-claude-skills` | https://github.com/alirezarezvani/claude-skills.git | `110348f` | nada — referência |
| `ccusage` | https://github.com/ryoppippi/ccusage.git | `0adbb4f` | nada — referência |
| `claudekit` | https://github.com/carlrannaberg/claudekit.git | `3926abc` | `commands/claudekit/` + 28 subagentes em `agents/` |
| `devops-skills` | https://github.com/akin-ozer/cc-devops-skills.git | `7fe7595` | nada — referência |
| `fullstack-skills` | https://github.com/jeffallan/claude-skills.git | `3bf9a24` | 66 skills (linguagens, frameworks, infra) |
| `glebis-claude-skills` | https://github.com/glebis/claude-skills.git | `c4d1abd` | 34 skills (produtividade, mídia, integrações) |
| `inference-sh-skills` | https://github.com/inference-sh/skills.git | `2c19448` | nada — referência |
| `levnikolaevich-claude-code-skills` | https://github.com/levnikolaevich/claude-code-skills.git | `f3e18aa` | nada — referência |
| `parry` | https://github.com/vaporif/parry.git | `9a3795f` | nada — referência |
| `recall` | https://github.com/zippoxer/recall.git | `e605ab9` | nada — referência |
| `riper-workflow` | https://github.com/tony/claude-code-riper-5.git | `29277fa` | `commands/riper/` + 3 subagentes (research-innovate, plan-execute, review) |
| `scientific-skills` | https://github.com/K-Dense-AI/claude-scientific-skills.git | `c84622c` | 15 skills (dados, visualização, escrita) |
| `second-brain-skills` | https://github.com/coleam00/second-brain-skills.git | `75e1e9c` | 5 skills (sop-creator, brand-voice-generator, pptx-generator, mcp-client, remotion) |
| `superclaude` | https://github.com/SuperClaude-Org/SuperClaude_Framework.git | `b061b2f` | nada — referência |
| `trailofbits-security` | https://github.com/trailofbits/skills.git | `c609769` | usado só pelo port Codex (`Cerebro central/import/claude-home/plugins`). No Claude Code, instalar como marketplace: `/plugin marketplace add trailofbits/skills` |
