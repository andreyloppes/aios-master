#!/usr/bin/env bash
# checar.sh — saúde do AIOS-MASTER. Sem argumentos; sai com 1 se achar problema.
# Verifica: ligações do ~/.claude, symlinks quebrados, arquivos zerados, skills sem SKILL.md,
# nomes de skill repetidos e comandos que sombreiam comandos nativos do Claude Code.
set -o pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE="$HOME/.claude"
R=$'\033[31m'; G=$'\033[32m'; D=$'\033[2m'; N=$'\033[0m'
bad=0
fail() { echo "${R}✗${N} $1"; shift; for l in "$@"; do echo "    $l"; done; bad=1; }
ok()   { echo "${G}✓${N} $1"; }

# 1. ~/.claude/{skills,commands,agents} apontam para cá
for d in skills commands agents; do
  [ "$(readlink "$CLAUDE/$d")" = "$ROOT/$d" ] && ok "~/.claude/$d → $d/" || fail "~/.claude/$d não aponta para $ROOT/$d"
done

# 2. symlinks quebrados
L=(); while IFS= read -r x; do L+=("$x"); done < <(find "$ROOT" -type l -not -path '*/.git/*' ! -exec test -e {} \; -print)
[ ${#L[@]} -eq 0 ] && ok "nenhum symlink quebrado" || fail "${#L[@]} symlinks quebrados" "${L[@]}"

# 3. arquivos zerados (corrupção silenciosa já aconteceu uma vez)
Z=(); while IFS= read -r x; do Z+=("$x"); done < <(find "$ROOT" -type f -size 0 -not -path '*/.git/*' -not -path '*/node_modules/*' \
  -not -path "$ROOT/skills/synced/*" -not -name '__init__.py' -not -name '.gitkeep' -not -name '.env')
[ ${#Z[@]} -eq 0 ] && ok "nenhum arquivo zerado" || fail "${#Z[@]} arquivos zerados" "${Z[@]:0:20}"

# 4. skills sem SKILL.md
M=(); for d in "$ROOT"/skills/*/; do n=$(basename "$d"); [ "$n" = synced ] && continue; [ -f "$d/SKILL.md" ] || M+=("$n"); done
[ ${#M[@]} -eq 0 ] && ok "$(ls -d "$ROOT"/skills/*/ | grep -vc /synced/) skills, todas com SKILL.md" || fail "skills sem SKILL.md" "${M[@]}"

# 5. nome de skill repetido (frontmatter) — inclui as oficiais em skills/synced
DUP=(); while IFS= read -r x; do DUP+=("$x"); done < <(grep -h '^name:' "$ROOT"/skills/*/SKILL.md "$ROOT"/skills/synced/*/*/SKILL.md 2>/dev/null \
  | sed 's/^name:[[:space:]]*//; s/["'\'']//g' | sort | uniq -d)
[ ${#DUP[@]} -eq 0 ] && ok "nenhum nome de skill repetido" || fail "nomes de skill repetidos" "${DUP[@]}"

# 6. comando na raiz de commands/ com nome de comando nativo
NATIVOS="init status review help config clear compact cost doctor login logout memory model permissions resume agents mcp hooks plugin skills"
S=(); for f in "$ROOT"/commands/*.md; do n=$(basename "$f" .md); [[ " $NATIVOS " == *" $n "* ]] && S+=("$n"); done
[ ${#S[@]} -eq 0 ] && ok "nenhum comando sombreando nativo" || fail "comandos que sombreiam nativos" "${S[@]}"

echo "${D}skills=$(ls -d "$ROOT"/skills/*/ | grep -vc /synced/)  comandos=$(find "$ROOT/commands" -name '*.md' | wc -l | tr -d ' ')  subagentes=$(find "$ROOT/agents" -name '*.md' | wc -l | tr -d ' ')${N}"
exit $bad
