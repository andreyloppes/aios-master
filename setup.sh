#!/bin/bash
# AIOS Master - Setup Script
# Creates symlinks from ~/.claude/ pointing to this directory.
# Run after cloning or moving the aios-master directory.

set -e

MASTER_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
PROJECT_DIR="$CLAUDE_DIR/projects/-Users-$(whoami)"

# Colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

show_banner() {
    echo ""
    echo -e "${RED}"
    cat << 'BANNER'
     █████╗ ██╗ ██████╗ ███████╗
    ██╔══██╗██║██╔═══██╗██╔════╝
    ███████║██║██║   ██║███████╗
    ██╔══██║██║██║   ██║╚════██║
    ██║  ██║██║╚██████╔╝███████║
    ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚══════╝
    ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗
    ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
    ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
BANNER
    echo -e "${NC}"
    echo -e "    ${DIM}Multi-Agent System for Claude Code${NC}"
    echo -e "    ${DIM}v1.0.0 — github.com/andreyloppes/aios-master${NC}"
    echo ""
}

show_banner

echo -e "${BOLD}Installing AIOS Master...${NC}"
echo -e "${DIM}Source:  ${MASTER_DIR}${NC}"
echo -e "${DIM}Target:  ${CLAUDE_DIR}${NC}"
echo ""

# Safe symlink creation
create_symlink() {
    local source="$1"
    local target="$2"
    local name="$3"

    if [ -L "$target" ]; then
        rm "$target"
    elif [ -d "$target" ]; then
        mv "$target" "${target}.bak"
        echo -e "  ${YELLOW}!${NC} Backed up existing dir: ${target}.bak"
    elif [ -f "$target" ]; then
        mv "$target" "${target}.bak"
        echo -e "  ${YELLOW}!${NC} Backed up existing file: ${target}.bak"
    fi

    ln -s "$source" "$target"
    echo -e "  ${GREEN}✓${NC} ${name}"
}

# Ensure directories exist
mkdir -p "$CLAUDE_DIR"
mkdir -p "$PROJECT_DIR"

echo -e "${CYAN}Creating symlinks...${NC}"

# Commands (agents, workflows, team, design system)
create_symlink "$MASTER_DIR/commands" "$CLAUDE_DIR/commands" "commands  →  12 agents, 8 workflows, team commands"

# Skills (interface-design)
create_symlink "$MASTER_DIR/skills" "$CLAUDE_DIR/skills" "skills    →  interface-design skill"

# Memory (MEMORY.md, architecture, patterns)
create_symlink "$MASTER_DIR/memory" "$PROJECT_DIR/memory" "memory    →  persistent agent memory"

echo ""
echo -e "${GREEN}${BOLD}  ✓ AIOS Master installed successfully!${NC}"
echo ""
echo -e "  ${BOLD}Open Claude Code and try:${NC}"
echo ""
echo -e "    ${CYAN}/agents:master${NC}           →  Orion, the Orchestrator"
echo -e "    ${CYAN}/agents:dev${NC}              →  Dex, Full Stack Developer"
echo -e "    ${CYAN}/workflows:greenfield${NC}    →  Build a project from scratch"
echo -e "    ${CYAN}/team:delegate${NC}           →  Auto-route to the right agent"
echo ""
echo -e "  ${DIM}12 agents  ·  8 workflows  ·  1 skill  ·  ready to go${NC}"
echo ""
