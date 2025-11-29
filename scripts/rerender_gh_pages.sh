#!/usr/bin/env bash

# Script to properly purge and re-render the Quarto page for GitHub Pages
# This script will:
# 1. Clean up old artifacts
# 2. Render the Quarto document
# 3. Move the output to index.html in the repo root
# 4. Ensure resource files are in the correct location

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOC_PATH="$REPO_ROOT/Quarto/randomforest.qmd"
QUARTO_DIR="$REPO_ROOT/Quarto"
DEST_INDEX="$REPO_ROOT/index.html"

# Check if Quarto is installed
if ! command -v quarto &> /dev/null; then
    echo "Error: Quarto CLI is not installed or not in PATH."
    echo "Please install Quarto: https://quarto.org/docs/get-started/"
    exit 1
fi

echo "Cleaning up previous artifacts..."
# Remove old index.html
rm -f "$DEST_INDEX"

# Remove Quarto cache/freeze directories to ensure a fresh build
rm -rf "$QUARTO_DIR/_freeze"
rm -rf "$QUARTO_DIR/.quarto"
rm -rf "$QUARTO_DIR/randomforest_files"
rm -f "$QUARTO_DIR/randomforest.html"

# Ensure we're using the correct python environment if it exists
if [[ -d "$REPO_ROOT/.venv" ]]; then
    echo "Activating virtual environment..."
    # shellcheck disable=SC1091
    source "$REPO_ROOT/.venv/bin/activate"
    export QUARTO_PYTHON="$REPO_ROOT/.venv/bin/python"
elif [[ -d "$REPO_ROOT/venv" ]]; then
    echo "Activating virtual environment..."
    # shellcheck disable=SC1091
    source "$REPO_ROOT/venv/bin/activate"
    export QUARTO_PYTHON="$REPO_ROOT/venv/bin/python"
fi

echo "Rendering Quarto document..."
cd "$QUARTO_DIR"
quarto render randomforest.qmd --to html

echo "Moving output to root index.html..."
if [[ -f "randomforest.html" ]]; then
    mv "randomforest.html" "$DEST_INDEX"
    
    # Move or copy the support files if they exist
    if [[ -d "randomforest_files" ]]; then
        # If a directory with the same name exists in root, remove it first
        rm -rf "$REPO_ROOT/randomforest_files"
        mv "randomforest_files" "$REPO_ROOT/"
    fi
    
    echo "Success! Document rendered to $DEST_INDEX"
    echo "Ready to be pushed to GitHub for Pages deployment."
else
    echo "Error: Rendering failed, randomforest.html not found."
    exit 1
fi

