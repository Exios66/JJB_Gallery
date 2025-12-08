#!/usr/bin/env bash

################################################################################
# Cleanup macOS Resource Fork Files
#
# This script removes all ._* files (macOS resource fork files) from the
# repository. These files are automatically created by macOS when copying
# files to non-HFS+ filesystems and can cause issues with Quarto rendering.
#
# Usage:
#   ./scripts/cleanup_resource_forks.sh
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Cleaning up macOS resource fork files and directories (._*)..."

# Count and remove ._ files and directories (excluding .git to avoid breaking git)
count=$(find "$REPO_ROOT" -name "._*" \( -type f -o -type d \) ! -path "*/.git/*" 2>/dev/null | wc -l | tr -d ' ')

if [[ "$count" -gt 0 ]]; then
    find "$REPO_ROOT" -name "._*" \( -type f -o -type d \) ! -path "*/.git/*" -delete 2>/dev/null
    echo -e "${GREEN}✓${NC} Removed $count resource fork files and directories"
else
    echo -e "${YELLOW}ℹ${NC} No resource fork files or directories found"
fi

echo "Done!"
