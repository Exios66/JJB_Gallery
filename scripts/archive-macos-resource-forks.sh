#!/usr/bin/env bash

################################################################################
# Archive macOS Resource Fork Files (._*)
#
# macOS can create AppleDouble "dot-underscore" files named `._*` when copying
# files onto non-HFS/APFS filesystems. These files should not live alongside
# source files, but we may still want to keep them around for inspection.
#
# This script moves any `._*` files/directories (excluding `.git/` and the
# `archives/` folder itself) into:
#   archives/macos-resource-forks/<original-relative-path>
#
# The archive directory is gitignored (except `archives/.gitkeep`).
#
# Usage:
#   ./scripts/archive-macos-resource-forks.sh [--dry-run] [--quiet]
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ARCHIVE_ROOT="$REPO_ROOT/archives/macos-resource-forks"

DRY_RUN=false
QUIET=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --quiet)
      QUIET=true
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: $0 [--dry-run] [--quiet]" >&2
      exit 2
      ;;
  esac
done

log() {
  if [[ "$QUIET" != "true" ]]; then
    echo "$@"
  fi
}

ensure_archive_dir() {
  if [[ "$DRY_RUN" == "true" ]]; then
    return 0
  fi
  mkdir -p "$ARCHIVE_ROOT"
  mkdir -p "$REPO_ROOT/archives"
  # Ensure .gitkeep exists so archives/ is tracked
  if [[ ! -f "$REPO_ROOT/archives/.gitkeep" ]]; then
    : > "$REPO_ROOT/archives/.gitkeep"
  fi
}

unique_dest_path() {
  local dest="$1"
  if [[ ! -e "$dest" ]]; then
    echo "$dest"
    return 0
  fi
  local ts
  ts="$(date +%Y%m%d_%H%M%S)"
  echo "${dest}.${ts}.$$"
}

move_one() {
  local src="$1"

  # Compute repo-relative path
  local rel="${src#"$REPO_ROOT"/}"
  local dest="$ARCHIVE_ROOT/$rel"
  local dest_dir
  dest_dir="$(dirname "$dest")"

  ensure_archive_dir

  if [[ "$DRY_RUN" == "true" ]]; then
    log "DRY RUN: mv -- '$src' '$dest'"
    return 0
  fi

  mkdir -p "$dest_dir"
  dest="$(unique_dest_path "$dest")"
  mv -- "$src" "$dest"
}

main() {
  log "Archiving macOS resource fork files (._*) into: $ARCHIVE_ROOT"

  # Nothing to do if archive folder is missing and we're dry-running? We still scan.
  local moved=0

  # Move files first (safe), then directories (using -depth).
  while IFS= read -r -d '' path; do
    move_one "$path"
    moved=$((moved + 1))
  done < <(
    find "$REPO_ROOT" \
      -name '._*' -type f \
      ! -path "$REPO_ROOT/.git/*" \
      ! -path "$REPO_ROOT/archives/*" \
      -print0 2>/dev/null
  )

  while IFS= read -r -d '' path; do
    move_one "$path"
    moved=$((moved + 1))
  done < <(
    find "$REPO_ROOT" -depth \
      -name '._*' -type d \
      ! -path "$REPO_ROOT/.git/*" \
      ! -path "$REPO_ROOT/archives/*" \
      -print0 2>/dev/null
  )

  if [[ "$moved" -eq 0 ]]; then
    log "No ._* files/directories found. Nothing to archive."
  else
    log "Archived $moved item(s)."
  fi
}

main

