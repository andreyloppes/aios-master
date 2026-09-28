# ESTRUTURA — mapa do AIOS-MASTER

**Regra:** o sistema inteiro mora aqui, uma vez. Não há cópia, symlink interno nem pasta de terceiros.
O Claude Code enxerga este repo por três links: `~/.claude/{skills,commands,agents}` → `~/AIOS-MASTER/{skills,commands,agents}`.
Tudo o que existe fora daqui é **gerado** a partir daqui ou **aponta** para cá.

```
AIOS-MASTER/
├── skills/        ← ~/.claude/skills     12 skills ativas — núcleo curado, carregado em toda sessão
│   └── synced/                           anthropic-skills:* — gerido pelo claude.ai, não editar
├── commands/      ← ~/.claude/commands   18 slash commands; pasta = namespace
│   ├── agents/           /agents:*            12  personas do squad (Orion master, Dex, Quinn, Aria…)
│   ├── interface-design/ /interface-design:*   5  init, audit, critique, extract, status
│   └── squad-activate.md
├── agents/        ← ~/.claude/agents      9 subagentes do stack da casa (o Claude delega via Agent tool)
├── acervo/                               fora de uso, NÃO carregado: 118 skills, 51 comandos, 22 subagentes
├── souls/                                SOULs do Paperclip: orion-ceo, cto, cmo + briefings
├── aiox/                                 biblioteca de metodologia SynkraAI/aiox-core v5: tasks, templates, checklists
├── pro/                                  infraestrutura PRO: dashboard, license-service, connectors, squads, scripts, tmux
├── forge/                                forge.py — CLI local de mídia (a skill está em acervo/skills/forge-tools)
├── memory/                               memória dos agentes, instalada pelo setup.sh
├── docs/                                 SETUP-CEREBRO (guia original) · UPSTREAM.md (origem do que é de terceiros)
├── scripts/
│   ├── checar.sh         saúde: links, symlinks quebrados, arquivos zerados, SKILL.md, nomes repetidos
│   ├── sync-espelho.sh   gera o espelho do time
│   └── upstream.sh       compara uma skill nossa com o repo de origem (clone temporário)
└── setup.sh · bootstrap.sh · README.md · LICENSE
```

## Fora daqui (e por quê)

| Lugar | Papel | Relação com a fonte |
|---|---|---|
| `~/.claude/chia/` | contexto da empresa (CHIA) | independente — é o que a O2 **é**; o AIOS é o que o Claude **faz** |
| `~/Desktop/O2/aios-master-o2` | espelho portável pro time (`o2-growth/aios-master`) | **gerado** por `scripts/sync-espelho.sh`. Nunca editar lá |
| `~/Desktop/Cerebro central` | ponte pro Codex | só links + gerador. `./install-codex-skills.sh` recria `~/.codex/skills/cerebro-import` a partir do núcleo |
| `~/Projetos/O2-AIOS` | produto próprio (engine Bun + dashboard) | repo separado, com squads próprios |
| `~/Backups/aios-reorg-2026-09-28.tar.gz` · `cerebro-reorg2-20260928-0947.tar.gz` | estado antes de cada rodada de reorganização | restauração: `tar xzf` na home |

## Núcleo × acervo

Tudo que o Claude Code carrega custa token em **toda** sessão (nome + descrição). Por isso o carregado é só o núcleo:
de ~15k para ~2,5k tokens (rodada 2: subagentes 23→9, comandos 46→18, react-expert/typescript-pro viraram só subagente). O acervo guarda o resto, organizado igual (`acervo/skills`, `acervo/commands`, `acervo/agents`).

Critério para estar no núcleo — precisa passar nos quatro:
1. **Uso** — acionado no histórico, ou peça própria da O2.
2. **Aderência** — stack da casa (Vite/React/TS/Supabase), consultoria CFO, IA.
3. **Funciona aqui** — nenhuma chave ou ferramenta ausente (sem OpenAI/Firecrawl/Gemini/ElevenLabs/Cerebras key, sem `pandoc`).
4. **Não duplica** — nada que um recurso nativo, plugin ou MCP já cobre (Gmail/Drive/Canva/Higgsfield MCP, plugin supabase, `/code-review`, `/security-review`, `/rewind`, `dataviz`, `anthropic-skills:*`).

Origem das 130 skills (12 ativas + 118 no acervo): jeffallan/claude-skills 66 · glebis/claude-skills 34 · K-Dense scientific 15 · coleam00/second-brain 5 · PRO 3 · próprias O2 7. URLs e commits em `docs/UPSTREAM.md`.

## Como mexer

| Quero… | Faço |
|---|---|
| Nova skill | `skills/<nome>/SKILL.md` (frontmatter `name` + `description`). Tem que passar no critério acima |
| Reativar do acervo | `mv acervo/skills/<x> skills/` (idem `commands/`, `agents/`) |
| Aposentar | `mv skills/<x> acervo/skills/` |
| Skill de terceiro | copiar para `acervo/skills/` (ou `skills/` se entrar no núcleo) e registrar a origem em `docs/UPSTREAM.md` |
| Atualizar do upstream | `scripts/upstream.sh <repo>` → ver o diff → `cp -R` do que valer a pena |
| Novo comando | `commands/<namespace>/<nome>.md` → `/<namespace>:<nome>`. Nunca na raiz com nome nativo (`init`, `status`, `review`…) |
| Novo subagente | `agents/<grupo>/<nome>.md` |
| Plugin de marketplace (ex.: Trail of Bits) | `/plugin marketplace add <org>/<repo>` — nunca copiar pasta para `~/.claude/plugins` |
| Publicar pro time | `scripts/sync-espelho.sh` → commit/push no espelho |
| Levar pro Codex | `~/Desktop/Cerebro\ central/install-codex-skills.sh` |
| Depois de qualquer mudança | `scripts/checar.sh` |

## O que é público

Este repo (`andreyloppes/aios-master`) é o Core MIT. O `.gitignore` mantém fora dele: `pro/`, `souls/`, `commands/pro/`, os 6 workflows PRO, as 3 skills PRO (inclusive a que está no acervo), `config/` e `skills/synced/`.
