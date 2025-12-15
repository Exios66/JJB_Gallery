#!/usr/bin/env bash
# Archive macOS Resource Fork Files (._*)
#
# Historically this script deleted `._*` files. It now archives them into
# `archives/macos-resource-forks/` to keep the repo clean while retaining the
# artifacts for inspection.
#
# Usage:
#   ./scripts/cleanup-macos-resource-forks.sh [--dry-run] [--quiet]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ARCHIVER="$REPO_ROOT/scripts/archive-macos-resource-forks.sh"

if [[ ! -f "$ARCHIVER" ]]; then
  echo "Error: archiver script not found: $ARCHIVER" >&2
  exit 1
fi

exec bash "$ARCHIVER" "$@"
