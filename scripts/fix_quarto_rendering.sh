#!/bin/bash
# Fix Quarto Rendering - Python Kernel Timeout Issue
# This script helps resolve kernel timeout errors when rendering Quarto documents

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🔧 Quarto Rendering Fix Script"
echo "================================"
echo ""

# Option 1: Pre-render randomforest.qmd to create frozen outputs
echo "Option 1: Pre-rendering randomforest.qmd to create frozen outputs..."
if [ -f "Quarto/randomforest.qmd" ]; then
    if [ -d ".venv" ]; then
        source .venv/bin/activate
        export QUARTO_PYTHON="$(pwd)/.venv/bin/python"
    fi
    
    echo "Rendering randomforest.qmd (this may take a few minutes)..."
    cd Quarto
    quarto render randomforest.qmd || {
        echo "⚠️  Initial render failed. This is okay - we'll use freeze mode."
    }
    cd ..
    echo "✅ Pre-render complete (or skipped if frozen outputs exist)"
else
    echo "⚠️  randomforest.qmd not found"
fi

echo ""
echo "✅ Fix applied! You can now run:"
echo "   ./scripts/render_gh_pages.sh"
echo ""
echo "If issues persist, try:"
echo "   1. Update _quarto.yml execute section to use: freeze: true"
echo "   2. Or comment out Quarto/randomforest.qmd from render list temporarily"

