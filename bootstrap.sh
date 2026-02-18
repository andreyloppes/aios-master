#!/usr/bin/env bash
# AIOS Master bootstrap (one-command install)
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/andreyloppes/aios-master/main/bootstrap.sh | bash
#   curl -fsSL ... | bash -s -- --edition pro --license-key "AIOSPRO...."

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/andreyloppes/aios-master.git}"
PRO_REPO_URL="${PRO_REPO_URL:-https://github.com/andreyloppes/aios-master-pro.git}"
BRANCH="${BRANCH:-main}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/claude-master}"
EDITION="${EDITION:-auto}"
MODE="${MODE:-customer}"
LICENSE_KEY="${LICENSE_KEY:-}"
LICENSE_SERVICE_URL="${LICENSE_SERVICE_URL:-}"
INSTALL_CORE="${INSTALL_CORE:-auto}"
DASHBOARD="${DASHBOARD:-yes}"
NON_INTERACTIVE=true
SKIP_LICENSE_VALIDATION=false
NO_UPDATE=false
DRY_RUN=false

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

log_info() {
  echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $*" >&2
}

die() {
  log_error "$*"
  exit 1
}

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

usage() {
  cat <<'EOF'
AIOS Master Bootstrap

Usage:
  ./bootstrap.sh --edition core
  ./bootstrap.sh --edition pro --license-key "AIOSPRO...."

Options:
  --edition <auto|core|pro>        Install target (default: auto)
  --core-only                      Shortcut for --edition core
  --pro                            Shortcut for --edition pro
  --license-key <key>              PRO license key
  --license-service-url <url>      URL for remote license validation
  --mode <customer|owner>          Install profile (default: customer)
  --install-dir <path>             Clone/update target (default: ~/claude-master)
  --repo-url <url>                 Git repository URL (Core)
  --pro-repo-url <url>             Git repository URL (PRO private repo)
  --branch <name>                  Git branch (default: main)
  --install-core <auto|yes|no>     Core setup mode (default: auto)
  --dashboard <yes|no>             Generate dashboard env file (default: yes)
  --skip-license-validation         Skip remote validation request
  --no-update                      Do not pull if repo already exists
  --interactive                    Run installer in interactive mode
  --dry-run                        Dry-run installer (clone/update still runs)
  -h, --help                       Show this help
EOF
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --edition)
        [[ $# -ge 2 ]] || die "Missing value for --edition"
        EDITION="$2"
        shift 2
        ;;
      --edition=*)
        EDITION="${1#*=}"
        shift
        ;;
      --core-only)
        EDITION="core"
        shift
        ;;
      --pro)
        EDITION="pro"
        shift
        ;;
      --license-key)
        [[ $# -ge 2 ]] || die "Missing value for --license-key"
        LICENSE_KEY="$2"
        shift 2
        ;;
      --license-key=*)
        LICENSE_KEY="${1#*=}"
        shift
        ;;
      --license-service-url)
        [[ $# -ge 2 ]] || die "Missing value for --license-service-url"
        LICENSE_SERVICE_URL="$2"
        shift 2
        ;;
      --license-service-url=*)
        LICENSE_SERVICE_URL="${1#*=}"
        shift
        ;;
      --mode)
        [[ $# -ge 2 ]] || die "Missing value for --mode"
        MODE="$2"
        shift 2
        ;;
      --mode=*)
        MODE="${1#*=}"
        shift
        ;;
      --install-dir)
        [[ $# -ge 2 ]] || die "Missing value for --install-dir"
        INSTALL_DIR="$2"
        shift 2
        ;;
      --install-dir=*)
        INSTALL_DIR="${1#*=}"
        shift
        ;;
      --repo-url)
        [[ $# -ge 2 ]] || die "Missing value for --repo-url"
        REPO_URL="$2"
        shift 2
        ;;
      --repo-url=*)
        REPO_URL="${1#*=}"
        shift
        ;;
      --pro-repo-url)
        [[ $# -ge 2 ]] || die "Missing value for --pro-repo-url"
        PRO_REPO_URL="$2"
        shift 2
        ;;
      --pro-repo-url=*)
        PRO_REPO_URL="${1#*=}"
        shift
        ;;
      --branch)
        [[ $# -ge 2 ]] || die "Missing value for --branch"
        BRANCH="$2"
        shift 2
        ;;
      --branch=*)
        BRANCH="${1#*=}"
        shift
        ;;
      --install-core)
        [[ $# -ge 2 ]] || die "Missing value for --install-core"
        INSTALL_CORE="$2"
        shift 2
        ;;
      --install-core=*)
        INSTALL_CORE="${1#*=}"
        shift
        ;;
      --dashboard)
        [[ $# -ge 2 ]] || die "Missing value for --dashboard"
        DASHBOARD="$2"
        shift 2
        ;;
      --dashboard=*)
        DASHBOARD="${1#*=}"
        shift
        ;;
      --skip-license-validation)
        SKIP_LICENSE_VALIDATION=true
        shift
        ;;
      --no-update)
        NO_UPDATE=true
        shift
        ;;
      --interactive)
        NON_INTERACTIVE=false
        shift
        ;;
      --dry-run)
        DRY_RUN=true
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        die "Unknown option: $1 (use --help)"
        ;;
    esac
  done
}

check_prerequisites() {
  command -v git >/dev/null 2>&1 || die "git is required"
  command -v bash >/dev/null 2>&1 || die "bash is required"
}

validate_mode() {
  case "${MODE}" in
    customer|owner) ;;
    *)
      die "Invalid mode: ${MODE} (expected customer|owner)"
      ;;
  esac
}

normalize_edition() {
  case "${EDITION}" in
    auto|"")
      if [[ -n "${LICENSE_KEY}" ]]; then
        EDITION="pro"
      else
        EDITION="core"
      fi
      ;;
    core|free|gratuito)
      EDITION="core"
      ;;
    pro|premium)
      EDITION="pro"
      ;;
    *)
      die "Invalid edition: ${EDITION} (expected auto|core|pro)"
      ;;
  esac
}

sync_repo() {
  if [[ ! -e "$INSTALL_DIR" ]]; then
    log_info "Cloning ${REPO_URL} (${BRANCH}) into ${INSTALL_DIR}"
    git clone --branch "$BRANCH" --depth 1 "$REPO_URL" "$INSTALL_DIR"
    return 0
  fi

  if [[ ! -d "${INSTALL_DIR}/.git" ]]; then
    die "Install dir exists but is not a git repo: ${INSTALL_DIR}"
  fi

  if [[ "$NO_UPDATE" == "true" ]]; then
    log_info "Skipping repository update (--no-update)"
    return 0
  fi

  local dirty
  dirty="$(git -C "$INSTALL_DIR" status --porcelain)"
  if [[ -n "$dirty" ]]; then
    log_warn "Repo has local changes; skipping pull: ${INSTALL_DIR}"
    return 0
  fi

  log_info "Updating repository in ${INSTALL_DIR}"
  git -C "$INSTALL_DIR" fetch origin "$BRANCH"
  git -C "$INSTALL_DIR" checkout "$BRANCH"
  git -C "$INSTALL_DIR" pull --ff-only origin "$BRANCH"
}

sync_pro_repo() {
    local pro_dir="${INSTALL_DIR}/pro"

    if [[ ! -e "$pro_dir" ]]; then
        log_info "Cloning PRO module from ${PRO_REPO_URL}"

        if ! git clone --branch "$BRANCH" --depth 1 "$PRO_REPO_URL" "$pro_dir" 2>/dev/null; then
            echo ""
            log_error "Failed to clone PRO repository."
            echo ""
            echo "Possible causes:"
            echo "  1. You don't have access to the private PRO repo"
            echo "  2. Git credentials are not configured for this repo"
            echo ""
            echo "To configure access:"
            echo "  gh auth login"
            echo "  OR set a personal access token:"
            echo "  git config --global credential.helper store"
            echo ""
            echo "To purchase PRO access: [contact info placeholder]"
            exit 1
        fi
        return 0
    fi

    # If already exists, update
    if [[ "$NO_UPDATE" == "true" ]]; then
        log_info "Skipping PRO update (--no-update)"
        return 0
    fi

    # Check if it's a git repo (might have been manually placed)
    if [[ -d "${pro_dir}/.git" ]]; then
        local dirty
        dirty="$(git -C "$pro_dir" status --porcelain 2>/dev/null)"
        if [[ -n "$dirty" ]]; then
            log_warn "PRO repo has local changes; skipping pull"
            return 0
        fi
        log_info "Updating PRO module"
        git -C "$pro_dir" pull --ff-only origin "$BRANCH" 2>/dev/null || log_warn "PRO update failed; using existing version"
    else
        log_info "PRO directory exists (not a git repo); using as-is"
    fi
}

run_pro_installer() {
  local installer="${INSTALL_DIR}/pro/install.sh"
  [[ -f "$installer" ]] || die "Installer not found: ${installer}"

  local args=()
  args+=(--mode "$MODE")
  args+=(--install-core "$INSTALL_CORE")
  args+=(--dashboard "$DASHBOARD")

  if [[ "$NON_INTERACTIVE" == "true" ]]; then
    args+=(--non-interactive)
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    args+=(--dry-run)
  fi

  if [[ "$SKIP_LICENSE_VALIDATION" == "true" ]]; then
    args+=(--skip-license-validation)
  fi

  if [[ -n "$LICENSE_KEY" ]]; then
    args+=(--license-key "$LICENSE_KEY")
  fi

  if [[ -n "$LICENSE_SERVICE_URL" ]]; then
    args+=(--license-service-url "$LICENSE_SERVICE_URL")
  fi

  log_info "Running PRO installer with mode=${MODE}"
  bash "$installer" "${args[@]}"
}

run_core_installer() {
  local installer="${INSTALL_DIR}/setup.sh"
  [[ -f "$installer" ]] || die "Core installer not found: ${installer}"

  log_info "Running Core installer"
  if [[ "$DRY_RUN" == "true" ]]; then
    log_info "[dry-run] bash ${installer}"
    return 0
  fi

  bash "$installer"
}

main() {
  parse_args "$@"
  check_prerequisites
  validate_mode
  normalize_edition

  if [[ "$EDITION" == "pro" && "$NON_INTERACTIVE" == "true" && -z "$LICENSE_KEY" ]]; then
    die "For PRO in non-interactive mode, pass --license-key \"AIOSPRO...\""
  fi

  show_banner

  echo -e "  ${DIM}Edition:  ${EDITION}${NC}"
  echo -e "  ${DIM}Branch:   ${BRANCH}${NC}"
  echo -e "  ${DIM}Target:   ${INSTALL_DIR}${NC}"
  if [[ "$EDITION" == "pro" ]]; then
    echo -e "  ${DIM}PRO repo: ${PRO_REPO_URL}${NC}"
  fi
  echo ""

  log_info "Downloading AIOS Master..."
  sync_repo

  if [[ "$EDITION" == "core" ]]; then
    run_core_installer
  else
    log_info "Downloading PRO module..."
    sync_pro_repo
    run_pro_installer
  fi
}

main "$@"
