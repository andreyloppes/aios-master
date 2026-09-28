#!/usr/bin/env bash
# sync-espelho.sh — exporta o ~/AIOS-MASTER para o espelho do time (o2-growth/aios-master).
# Uso: scripts/sync-espelho.sh [destino]   (padrão: ~/Desktop/O2/aios-master-o2)
# Idempotente. Depois: cd <destino> && git add -A && git commit && git push.
#
# Fonte da verdade é ~/AIOS-MASTER. O espelho é a versão portável: sem .git aninhado, sem segredos.
set -euo pipefail

SRC="${AIOS_SRC:-$HOME/AIOS-MASTER}"
CLAUDE="${CLAUDE_SRC:-$HOME/.claude}"
DST="$(cd "${1:-$HOME/Desktop/O2/aios-master-o2}" && pwd)"
[ -d "$DST/.git" ] || { echo "destino não é um repo git: $DST"; exit 1; }

[ -d "$SRC/skills" ] || { echo "fonte não encontrada: $SRC"; exit 1; }

RS=(rsync -a --copy-links --delete
    --exclude .DS_Store --exclude .git --exclude node_modules
    --exclude '.env' --exclude '.env.*' --exclude '.envrc' --exclude '.vercel'
    --include '.env.example')

# symlinks pendentes (alvo inexistente) quebram --copy-links: exclui antes
dangling() {  # dangling <dir>  → arquivo com caminhos relativos dos symlinks quebrados
  local base="$1" out; out=$(mktemp)
  find "$base" -type l -not -path '*/.git/*' 2>/dev/null | while read -r l; do
    [ -e "$l" ] || echo "/${l#"$base"/}"
  done > "$out"; echo "$out"
}
XS=$(dangling "$SRC/skills"); XA=$(dangling "$SRC/agents")
n=$(cat "$XS" "$XA" | wc -l | tr -d ' '); [ "$n" != "0" ] && echo "  (ignorando $n symlinks pendentes na fonte)"

echo "→ skills"     && "${RS[@]}" --exclude-from="$XS" --exclude synced "$SRC/skills/"   "$DST/skills/"
echo "→ commands"   && "${RS[@]}" "$SRC/commands/" "$DST/commands/"
echo "→ agents"     && "${RS[@]}" --exclude-from="$XA" "$SRC/agents/" "$DST/agents/"
echo "→ acervo"     && "${RS[@]}" "$SRC/acervo/"   "$DST/acervo/"
echo "→ aiox"       && "${RS[@]}" "$SRC/aiox/"     "$DST/aiox/"
echo "→ forge"      && "${RS[@]}" "$SRC/forge/" "$DST/forge/"
echo "→ pro"        && "${RS[@]}" --exclude 'license-service/data/*' "$SRC/pro/" "$DST/pro/"
echo "→ memory"     && "${RS[@]}" "$SRC/memory/"   "$DST/memory/"
echo "→ souls"      && "${RS[@]}" "$SRC/souls/"    "$DST/souls/"
echo "→ docs"       && cp "$SRC/docs/SETUP-CEREBRO-MASTER-CLAUDE-CODE.md" "$SRC/docs/UPSTREAM.md" "$DST/docs/"
cp "$SRC/LICENSE" "$SRC/ESTRUTURA.md" "$DST/"
# layout antigo: plugins vendorados e o próprio script de sync não moram mais no espelho
rm -rf "$DST/plugins" "$DST/scripts"

# ── config: statusline + settings sem nada pessoal ────────────────────────────
echo "→ config"
cp "$CLAUDE/statusline.sh" "$DST/config/statusline.sh"
[ -f "$CLAUDE/scripts/weekly_cost_report.py" ] && mkdir -p "$DST/config/scripts" && cp "$CLAUDE/scripts/weekly_cost_report.py" "$DST/config/scripts/"
python3 - "$CLAUDE/settings.json" "$DST/config/settings.example.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
d.pop("autoMode", None)                       # notas de ambiente geradas por sessão — pessoais
if "statusLine" in d:
    d["statusLine"]["command"] = "bash ~/.claude/statusline.sh"
json.dump(d, open(sys.argv[2], "w"), indent=2, ensure_ascii=False)
PY

# ── índices gerados a partir do frontmatter ───────────────────────────────────
echo "→ índices"
python3 - "$DST" <<'PY'
import os, re, sys, glob
root = sys.argv[1]

def frontmatter(path):
    try:
        txt = open(path, encoding="utf-8", errors="ignore").read()
    except Exception:
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---", txt, re.S)
    if not m:
        return {}
    fm, cur, out = m.group(1).splitlines(), None, {}
    for line in fm:
        if re.match(r"^[A-Za-z_-]+:", line):
            k, _, v = line.partition(":")
            v = v.strip()
            cur = k.strip()
            out[cur] = "" if v in (">", ">-", "|", "|-") else v.strip('"\'')
        elif cur and line.startswith((" ", "\t")):
            out[cur] = (out[cur] + " " + line.strip()).strip()
    return out

def first_sentence(s, n=160):
    s = re.sub(r"\s+", " ", s or "").strip()
    return (s[: n - 1] + "…") if len(s) > n else s

# skills
rows = []
for d in sorted(glob.glob(f"{root}/skills/*/")):
    if not os.path.exists(os.path.join(d, "SKILL.md")): continue
    name = os.path.basename(d.rstrip("/"))
    fm = frontmatter(os.path.join(d, "SKILL.md"))
    rows.append((name, first_sentence(fm.get("description", ""))))
with open(f"{root}/docs/INDICE-SKILLS.md", "w") as f:
    f.write(f"# Índice — {len(rows)} skills\n\nGerado por `~/AIOS-MASTER/scripts/sync-espelho.sh` a partir do frontmatter de cada `SKILL.md`. Invoque com `/nome-da-skill` ou deixe o Claude escolher.\n\n| Skill | O que faz |\n|---|---|\n")
    for n, d in rows:
        f.write(f"| `{n}` | {d} |\n")

# commands
rows = []
for p in sorted(glob.glob(f"{root}/commands/**/*.md", recursive=True)):
    rel = os.path.relpath(p, f"{root}/commands")[:-3]
    parts = rel.split("/")
    slash = "/" + (":".join(parts) if len(parts) > 1 else parts[0])
    fm = frontmatter(p)
    rows.append((slash, first_sentence(fm.get("description", ""))))
with open(f"{root}/docs/INDICE-COMANDOS.md", "w") as f:
    f.write(f"# Índice — {len(rows)} comandos\n\nDigite o comando no prompt do Claude Code.\n\n| Comando | O que faz |\n|---|---|\n")
    for n, d in rows:
        f.write(f"| `{n}` | {d} |\n")

# agents
rows = []
for p in sorted(glob.glob(f"{root}/agents/**/*.md", recursive=True)):
    fm = frontmatter(p)
    rel = os.path.relpath(p, f"{root}/agents")
    rows.append((fm.get("name") or rel[:-3], rel, first_sentence(fm.get("description", ""))))
with open(f"{root}/docs/INDICE-AGENTS.md", "w") as f:
    f.write(f"# Índice — {len(rows)} subagentes\n\nDisponíveis para o Claude delegar via Agent tool (`subagent_type`).\n\n| Agente | Arquivo | Quando usar |\n|---|---|---|\n")
    for n, rel, d in rows:
        f.write(f"| `{n}` | `{rel}` | {d} |\n")
print(f"  skills={len(glob.glob(f'{root}/skills/*/'))} commands={len(glob.glob(f'{root}/commands/**/*.md', recursive=True))} agents={len(glob.glob(f'{root}/agents/**/*.md', recursive=True))}")
PY

# ── carimbo ───────────────────────────────────────────────────────────────────
src_sha=$(git -C "$SRC" rev-parse --short HEAD 2>/dev/null || echo "—")
cat > "$DST/docs/SYNC.md" <<MD
# Última sincronização

| | |
|---|---|
| Data | $(date '+%Y-%m-%d %H:%M %Z') |
| Fonte | \`~/AIOS-MASTER\` @ \`$src_sha\` |
| Skills | $(ls -1 "$DST/skills" | wc -l | tr -d ' ') |
| Comandos | $(find "$DST/commands" -name '*.md' | wc -l | tr -d ' ') |
| Subagentes | $(find "$DST/agents" -name '*.md' | wc -l | tr -d ' ') |

Para atualizar: \`~/AIOS-MASTER/scripts/sync-espelho.sh && git add -A && git commit -m "sync $(date +%Y-%m-%d)" && git push\`.
MD

# ── guarda-corpo: nada pessoal ou secreto pode sair daqui ─────────────────────
echo "→ varredura"
bad=0
home_lit="$HOME"   # caminho pessoal da máquina de origem, nunca pode aparecer no conteúdo
if grep -rIlF "$home_lit" "$DST" --exclude-dir=.git -q 2>/dev/null; then
  echo "  ✗ caminho absoluto pessoal encontrado:"; grep -rIlF "$home_lit" "$DST" --exclude-dir=.git | head; bad=1
fi
# tokens de API: linha a linha, fora de testes/scanners/exemplos, descartando placeholders conhecidos
pat='(sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{40,}|gh[pousr]_[A-Za-z0-9]{30,}|xox[bp]-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16})'
hits=$(grep -rInE "$pat" "$DST" --exclude-dir=.git 2>/dev/null \
       | grep -vE '/(tests?|__tests__|spec|fixtures?|examples?)/|_test\.|\.test\.|scanner|secrets\.rs|slop-patterns' \
       | grep -vE 'AKIAIOSFODNN7EXAMPLE|EXAMPLE|placeholder|your[_-]|xxx|regex' || true)
if [ -n "$hits" ]; then echo "  ✗ possível token:"; echo "$hits" | cut -c1-160 | head -20; bad=1; fi
# chaves privadas: só conta se o cabeçalho for seguido de corpo base64 real (cabeçalho solto em doc/teste não é chave)
keys=$(grep -rIzlE -- '-----BEGIN [A-Z ]*PRIVATE KEY-----[[:space:]]*\n[A-Za-z0-9+/=]{40,}' "$DST" --exclude-dir=.git 2>/dev/null || true)
if [ -n "$keys" ]; then echo "  ✗ chave privada com corpo:"; echo "$keys" | head; bad=1; fi
if find "$DST" -mindepth 2 -name .git -not -path "$DST/.git/*" | grep -q .; then echo "  ✗ .git aninhado"; bad=1; fi
if find -L "$DST" -type l -not -path '*/.git/*' | grep -q .; then echo "  ✗ symlink quebrado:"; find -L "$DST" -type l -not -path '*/.git/*' | head; bad=1; fi
[ $bad -eq 0 ] && echo "  ✓ limpo" || { echo "  abortando"; exit 2; }
echo "pronto: $DST"
