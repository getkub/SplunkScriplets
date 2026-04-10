#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRIGGER_FILE_REL="${1:-config/build.yml}"
PY_SCRIPT="$SCRIPT_DIR/compile_content.py"
FALLBACK_SCRIPT="$SCRIPT_DIR/compile_content_fallback.sh"

ts() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

log_info() {
  echo "[$(ts)] [INFO] $*"
}

log_warn() {
  echo "[$(ts)] [WARN] $*" >&2
}

log_error() {
  echo "[$(ts)] [ERROR] $*" >&2
}

if [[ ! -f "$FALLBACK_SCRIPT" ]]; then
  log_error "Missing fallback script: $FALLBACK_SCRIPT"
  exit 1
fi

run_fallback() {
  log_info "Running fallback compiler using trigger: $TRIGGER_FILE_REL"
  bash "$FALLBACK_SCRIPT" "$TRIGGER_FILE_REL"
  log_info "Fallback compiler completed successfully"
}

log_info "Starting compile launcher"
log_info "Trigger config: $TRIGGER_FILE_REL"

if [[ -f "$PY_SCRIPT" ]]; then
  log_info "Python compiler script found: $PY_SCRIPT"

  if command -v python3 >/dev/null 2>&1; then
    log_info "Attempting Python compiler with python3"
    if python3 "$PY_SCRIPT" "$TRIGGER_FILE_REL"; then
      log_info "Python compiler completed successfully"
      exit 0
    fi
    log_warn "Python compile failed; falling back"
    run_fallback
    exit 0
  fi

  if command -v python >/dev/null 2>&1; then
    log_info "Attempting Python compiler with python"
    if python "$PY_SCRIPT" "$TRIGGER_FILE_REL"; then
      log_info "Python compiler completed successfully"
      exit 0
    fi
    log_warn "Python compile failed; falling back"
    run_fallback
    exit 0
  fi

  log_warn "No Python interpreter available"
else
  log_warn "Python compiler script not found"
fi

log_warn "Using fallback compiler"
run_fallback
