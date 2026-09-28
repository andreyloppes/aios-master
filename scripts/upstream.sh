#!/usr/bin/env bash
# upstream.sh — compara nossas cópias com o repo de origem, sem guardar clone na árvore.
# Uso: scripts/upstream.sh <repo>        ex.: scripts/upstream.sh fullstack-skills
#      scripts/upstream.sh               lista os repos de docs/UPSTREAM.md
# Clona raso em /tmp, mostra o que mudou em cada skill nossa que veio dali. Não copia nada.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MAN="$ROOT/docs/UPSTREAM.md"

if [ $# -eq 0 ]; then
  grep -E '^\| `' "$MAN" | awk -F'|' '{gsub(/[ `]/,"",$2); print $2}'; exit 0
fi

url=$(grep -E "^\| \`$1\` " "$MAN" | awk -F'|' '{gsub(/ /,"",$3); print $3}')
[ -n "$url" ] || { echo "repo não encontrado em docs/UPSTREAM.md: $1"; exit 1; }

tmp=$(mktemp -d "/tmp/upstream-$1.XXXX")
git clone -q --depth 1 "$url" "$tmp"
echo "upstream: $url @ $(git -C "$tmp" rev-parse --short HEAD)  →  $tmp"

for d in "$ROOT"/skills/*/ "$ROOT"/acervo/skills/*/; do
  n=$(basename "$d")
  src=$(find "$tmp" -type d -name "$n" -not -path '*/.git/*' -exec test -f {}/SKILL.md \; -print -quit)
  [ -n "$src" ] || continue
  if diff -rq "$d" "$src" >/dev/null 2>&1; then echo "  = $n"; else echo "  ≠ $n   (diff -r $d $src)"; fi
done
echo "Para adotar uma versão nova: cp -R <origem>/. skills/<nome>/  — depois scripts/checar.sh"
