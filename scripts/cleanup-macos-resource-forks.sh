#!/bin/bash
# Cleanup macOS Resource Fork Files (._*)
# Removes all ._* files from the repository to reduce clutter
# These files are created by macOS when copying/moving files and are not needed

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🧹 Cleaning up macOS resource fork files (._*)..."
echo "Repository root: $REPO_ROOT"
echo ""

# Count files before cleanup
BEFORE_COUNT=$(find "$REPO_ROOT" -name "._*" -type f ! -path "$REPO_ROOT/.git/*" 2>/dev/null | wc -l | tr -d ' ')

if [ "$BEFORE_COUNT" -eq 0 ]; then
    echo "✅ No ._* files found outside .git directory. Nothing to clean."
    exit 0
fi

echo "Found $BEFORE_COUNT ._* files to remove (excluding .git directory)"
echo ""

# Ask for confirmation unless --force flag is provided
if [ "$1" != "--force" ]; then
    read -p "Continue with cleanup? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cleanup cancelled."
        exit 1
    fi
fi

# Remove all ._* files except in .git directory
# Using find with -delete is safer than rm -rf
find "$REPO_ROOT" -name "._*" -type f ! -path "$REPO_ROOT/.git/*" -delete 2>/dev/null || true

# Count files after cleanup
AFTER_COUNT=$(find "$REPO_ROOT" -name "._*" -type f ! -path "$REPO_ROOT/.git/*" 2>/dev/null | wc -l | tr -d ' ')

REMOVED=$((BEFORE_COUNT - AFTER_COUNT))

echo ""
echo "✅ Cleanup complete!"
echo "   Removed: $REMOVED files"
echo "   Remaining: $AFTER_COUNT files (likely in .git directory, which is normal)"
echo ""
echo "💡 Tip: To prevent future ._* file creation, run:"
echo "   export COPYFILE_DISABLE=1"
echo "   Or add it to your ~/.zshrc for permanent effect"
echo ""
echo "   You can also use the script: scripts/prevent-resource-forks.sh"
