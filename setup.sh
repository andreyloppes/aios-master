#!/bin/bash
# Claude Master - Setup Script
# Recria os symlinks do ~/.claude/ apontando para este diretorio.
# Rode apos clonar/mover o claude-master para um novo local.

set -e

MASTER_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
PROJECT_DIR="$CLAUDE_DIR/projects/-Users-$(whoami)"

echo "Claude Master Setup"
echo "==================="
echo "Master dir: $MASTER_DIR"
echo "Claude dir: $CLAUDE_DIR"
echo ""

# Funcao para criar symlink com seguranca
create_symlink() {
    local source="$1"
    local target="$2"
    local name="$3"

    if [ -L "$target" ]; then
        echo "  Removendo symlink antigo: $target"
        rm "$target"
    elif [ -d "$target" ]; then
        echo "  AVISO: $target e um diretorio real. Movendo para ${target}.bak"
        mv "$target" "${target}.bak"
    elif [ -f "$target" ]; then
        echo "  AVISO: $target e um arquivo. Movendo para ${target}.bak"
        mv "$target" "${target}.bak"
    fi

    ln -s "$source" "$target"
    echo "  OK: $name -> $source"
}

# Garantir que os diretorios existem
mkdir -p "$CLAUDE_DIR"
mkdir -p "$PROJECT_DIR"

echo "Criando symlinks..."
echo ""

# Commands (agents, workflows, team, design system)
create_symlink "$MASTER_DIR/commands" "$CLAUDE_DIR/commands" "commands"

# Skills (interface-design)
create_symlink "$MASTER_DIR/skills" "$CLAUDE_DIR/skills" "skills"

# Memory (MEMORY.md, architecture, patterns)
create_symlink "$MASTER_DIR/memory" "$PROJECT_DIR/memory" "memory"

echo ""
echo "Setup completo!"
echo ""
echo "Verificando..."
ls -la "$CLAUDE_DIR/commands" | head -1
ls -la "$CLAUDE_DIR/skills" | head -1
ls -la "$PROJECT_DIR/memory" | head -1
echo ""
echo "Tudo pronto. O Claude Code ja esta usando os arquivos de $MASTER_DIR"
