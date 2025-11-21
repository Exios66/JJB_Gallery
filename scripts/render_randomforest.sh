#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOC_PATH="$REPO_ROOT/Quarto/randomforest.qmd"
FREEZE_DIR="$REPO_ROOT/Quarto/_freeze"
ARTIFACT_DIR="$REPO_ROOT/Quarto/randomforest_files"
HTML_OUTPUT="$REPO_ROOT/Quarto/randomforest.html"
PDF_OUTPUT="$REPO_ROOT/Quarto/randomforest.pdf"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-4343}"

if [[ ! -f "$DOC_PATH" ]]; then
  echo "Document not found at $DOC_PATH" >&2
  exit 1
fi

echo "Purging previous Quarto artifacts..."
rm -rf "$FREEZE_DIR" "$ARTIFACT_DIR" "$HTML_OUTPUT" "$PDF_OUTPUT"

if [[ -d "$REPO_ROOT/.venv" ]]; then
  # shellcheck disable=SC1091
  source "$REPO_ROOT/.venv/bin/activate"
  export QUARTO_PYTHON="$REPO_ROOT/.venv/bin/python"
else
  echo "Warning: .venv not found; falling back to system python." >&2
fi

echo "Rendering $DOC_PATH ..."
quarto render "$DOC_PATH"

echo "Starting Quarto preview on http://$HOST:$PORT ..."
quarto preview "$DOC_PATH" --no-browser --host "$HOST" --port "$PORT" &
SERVER_PID=$!

cleanup() {
  if ps -p "$SERVER_PID" >/dev/null 2>&1; then
    kill "$SERVER_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

PREVIEW_URL="http://$HOST:$PORT"

if command -v open >/dev/null 2>&1; then
  open "$PREVIEW_URL"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$PREVIEW_URL"
else
  echo "Please open $PREVIEW_URL manually." >&2
fi

echo "Quarto preview running (PID $SERVER_PID). Press Ctrl+C to stop."
wait "$SERVER_PID"

