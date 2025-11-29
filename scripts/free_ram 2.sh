#!/usr/bin/env bash

# Script to free up unnecessary RAM by clearing caches and temporary files
# Works on macOS and Linux systems

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to format memory in MB/GB
format_memory() {
    local mem_kb=$1
    local mem_mb=$((mem_kb / 1024))
    if [ "$mem_mb" -gt 1024 ]; then
        echo "$(awk "BEGIN {printf \"%.2f\", $mem_mb/1024}") GB"
    else
        echo "${mem_mb} MB"
    fi
}

print_info "Starting RAM cleanup process..."
echo ""

# Get initial memory stats
print_info "Initial memory status:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    vm_stat | grep -E "Pages free|Pages active|Pages inactive|Pages speculative|Pages wired down" || true
else
    free -h || true
fi
echo ""

# Track freed space
TOTAL_FREED=0

# 1. Clear Python cache files
print_info "Clearing Python cache files (__pycache__, *.pyc, *.pyo)..."
PYTHON_COUNT=$(find "$REPO_ROOT" -type d -name "__pycache__" 2>/dev/null | wc -l | tr -d ' ')
if [ "$PYTHON_COUNT" -gt 0 ]; then
    PYTHON_SIZE=$(find "$REPO_ROOT" -type d -name "__pycache__" -exec du -sk {} + 2>/dev/null | awk '{sum+=$1} END {print sum+0}' || echo "0")
    find "$REPO_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$REPO_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
    find "$REPO_ROOT" -type f -name "*.pyo" -delete 2>/dev/null || true
    print_success "Cleared Python cache files (~${PYTHON_SIZE}KB)"
    TOTAL_FREED=$((TOTAL_FREED + PYTHON_SIZE))
else
    print_info "No Python cache files found"
fi
echo ""

# 2. Clear Jupyter/IPython checkpoints
print_info "Clearing Jupyter/IPython checkpoints..."
JUPYTER_COUNT=$(find "$REPO_ROOT" -type d -name ".ipynb_checkpoints" 2>/dev/null | wc -l | tr -d ' ')
if [ "$JUPYTER_COUNT" -gt 0 ]; then
    JUPYTER_SIZE=$(find "$REPO_ROOT" -type d -name ".ipynb_checkpoints" -exec du -sk {} + 2>/dev/null | awk '{sum+=$1} END {print sum+0}' || echo "0")
    find "$REPO_ROOT" -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
    print_success "Cleared Jupyter checkpoints (~${JUPYTER_SIZE}KB)"
    TOTAL_FREED=$((TOTAL_FREED + JUPYTER_SIZE))
else
    print_info "No Jupyter checkpoints found"
fi
echo ""

# 3. Clear Quarto cache and artifacts
print_info "Clearing Quarto cache and freeze directories..."
QUARTO_FREEZE="$REPO_ROOT/Quarto/_freeze"
if [ -d "$QUARTO_FREEZE" ]; then
    QUARTO_SIZE=$(du -sk "$QUARTO_FREEZE" 2>/dev/null | awk '{print $1}' || echo "0")
    rm -rf "$QUARTO_FREEZE" 2>/dev/null || true
    if [ "$QUARTO_SIZE" -gt 0 ]; then
        print_success "Cleared Quarto freeze cache (~${QUARTO_SIZE}KB)"
        TOTAL_FREED=$((TOTAL_FREED + QUARTO_SIZE))
    fi
fi

QUARTO_CACHE="$HOME/.quarto"
if [ -d "$QUARTO_CACHE" ] && [ -d "$QUARTO_CACHE/cache" ]; then
    QUARTO_USER_SIZE=$(du -sk "$QUARTO_CACHE/cache" 2>/dev/null | awk '{print $1}' || echo "0")
    rm -rf "$QUARTO_CACHE/cache"/* 2>/dev/null || true
    if [ "$QUARTO_USER_SIZE" -gt 0 ]; then
        print_success "Cleared Quarto user cache (~${QUARTO_USER_SIZE}KB)"
        TOTAL_FREED=$((TOTAL_FREED + QUARTO_USER_SIZE))
    fi
fi
echo ""

# 4. Clear pip cache
print_info "Clearing pip cache..."
if command -v pip &> /dev/null; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        PIP_CACHE_DIR="${PIP_CACHE_DIR:-$HOME/Library/Caches/pip}"
    else
        PIP_CACHE_DIR="${PIP_CACHE_DIR:-$HOME/.cache/pip}"
    fi
    
    if [ -d "$PIP_CACHE_DIR" ]; then
        PIP_SIZE=$(du -sk "$PIP_CACHE_DIR" 2>/dev/null | awk '{print $1}' || echo "0")
        pip cache purge 2>/dev/null || rm -rf "$PIP_CACHE_DIR"/* 2>/dev/null || true
        if [ "$PIP_SIZE" -gt 0 ]; then
            print_success "Cleared pip cache (~${PIP_SIZE}KB)"
            TOTAL_FREED=$((TOTAL_FREED + PIP_SIZE))
        fi
    else
        print_info "No pip cache found"
    fi
else
    print_warning "pip not found, skipping pip cache cleanup"
fi
echo ""

# 5. Clear Python bytecode cache
print_info "Clearing additional Python bytecode..."
find "$REPO_ROOT" -type f -name "*.py[cod]" -delete 2>/dev/null || true
print_success "Python bytecode cleared"
echo ""

# 6. Clear system page cache (Linux only, requires sudo)
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_info "Attempting to clear system page cache (requires sudo)..."
    if [ "$EUID" -eq 0 ] || sudo -n true 2>/dev/null; then
        sync
        echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null 2>&1 && \
            print_success "System page cache cleared" || \
            print_warning "Could not clear system page cache"
    else
        print_warning "Skipping system page cache (requires sudo privileges)"
        print_info "Run manually: sudo sync; sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'"
    fi
    echo ""
fi

# 7. Clear macOS user caches (optional)
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_info "macOS detected - clearing user caches..."
    USER_CACHE="$HOME/Library/Caches"
    if [ -d "$USER_CACHE" ]; then
        CACHE_DIRS=("pip" "pypoetry" "pipx")
        for cache_dir in "${CACHE_DIRS[@]}"; do
            if [ -d "$USER_CACHE/$cache_dir" ]; then
                CACHE_SIZE=$(du -sk "$USER_CACHE/$cache_dir" 2>/dev/null | awk '{print $1}' || echo "0")
                rm -rf "$USER_CACHE/$cache_dir"/* 2>/dev/null || true
                if [ "$CACHE_SIZE" -gt 0 ]; then
                    print_success "Cleared $cache_dir cache (~${CACHE_SIZE}KB)"
                    TOTAL_FREED=$((TOTAL_FREED + CACHE_SIZE))
                fi
            fi
        done
    fi
    echo ""
fi

# Summary
echo ""
print_info "Cleanup Summary:"
FREED_MB=$((TOTAL_FREED / 1024))
FREED_FORMATTED=$(format_memory "$TOTAL_FREED")
print_success "Total space freed: ~${FREED_FORMATTED}"

echo ""
print_info "Final memory status:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    vm_stat | grep -E "Pages free|Pages active|Pages inactive|Pages speculative|Pages wired down" || true
else
    free -h || true
fi

echo ""
print_success "RAM cleanup completed!"
print_info "Note: Some system-level caches may require sudo privileges to clear."
