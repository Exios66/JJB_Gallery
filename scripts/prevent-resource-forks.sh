#!/usr/bin/env bash
# Prevent macOS Resource Fork File Creation
# Configures your shell environment to reduce `._*` file creation on macOS.
# This is a one-time setup script.

set -euo pipefail

echo "Configuring shell to prevent macOS resource fork file creation..."
echo ""

# Prefer the rc file matching the current shell; fall back to bash/zsh defaults.
RC_FILE=""
CURRENT_SHELL="${SHELL:-}"

if [[ "$CURRENT_SHELL" == *"zsh" ]]; then
  RC_FILE="$HOME/.zshrc"
elif [[ "$CURRENT_SHELL" == *"bash" ]]; then
  RC_FILE="$HOME/.bashrc"
else
  if [[ -f "$HOME/.zshrc" ]]; then
    RC_FILE="$HOME/.zshrc"
  else
    RC_FILE="$HOME/.bashrc"
  fi
fi

if [[ -z "$RC_FILE" ]]; then
  echo "Error: Could not determine shell rc file." >&2
  exit 1
fi

if grep -q "COPYFILE_DISABLE" "$RC_FILE" 2>/dev/null; then
  echo "COPYFILE_DISABLE is already configured in $RC_FILE"
  echo ""
  echo "To apply changes, run: source $RC_FILE"
  exit 0
fi

echo "Adding COPYFILE_DISABLE=1 to $RC_FILE..."
{
  echo ""
  echo "# Prevent macOS resource fork files (._*)"
  echo "export COPYFILE_DISABLE=1"
  echo "export COPY_EXTENDED_ATTRIBUTES_DISABLE=1"
} >> "$RC_FILE"

echo ""
echo "Done. To apply immediately, run:"
echo "  source $RC_FILE"
echo ""
echo "Note: This only affects new operations. Existing ._* files can be archived via:"
echo "  ./scripts/cleanup-macos-resource-forks.sh"
