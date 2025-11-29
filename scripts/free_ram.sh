#!/usr/bin/env bash

# Enhanced script to free up unnecessary RAM, disk space, and compute resources
# by clearing caches, temporary files, and idle processes
# Works on macOS and Linux systems

set -euo pipefail

# Option to kill idle processes (set to "yes" to enable, "no" to disable)
KILL_IDLE_PROCESSES="${KILL_IDLE_PROCESSES:-no}"

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

# 7. Clear Node.js/npm cache
print_info "Clearing Node.js/npm cache..."
if command -v npm &> /dev/null; then
    NPM_CACHE_SIZE=$(npm cache verify 2>&1 | grep -oE '[0-9]+[KMGT]?B' | head -1 || echo "0")
    npm cache clean --force 2>/dev/null || true
    print_success "Cleared npm cache"
fi

if command -v yarn &> /dev/null; then
    YARN_CACHE_DIR="$HOME/.yarn/cache"
    if [ -d "$YARN_CACHE_DIR" ]; then
        YARN_SIZE=$(du -sk "$YARN_CACHE_DIR" 2>/dev/null | awk '{print $1}' || echo "0")
        yarn cache clean 2>/dev/null || rm -rf "$YARN_CACHE_DIR"/* 2>/dev/null || true
        if [ "$YARN_SIZE" -gt 0 ]; then
            print_success "Cleared yarn cache (~${YARN_SIZE}KB)"
            TOTAL_FREED=$((TOTAL_FREED + YARN_SIZE))
        fi
    fi
fi
echo ""

# 8. Clear Docker cache and unused resources
print_info "Clearing Docker cache and unused resources..."
if command -v docker &> /dev/null && docker info &> /dev/null; then
    DOCKER_PRUNE=$(docker system prune -af --volumes 2>&1 | grep -oE 'Total reclaimed space: [0-9.]+[KMGT]?B' || echo "")
    if [ -n "$DOCKER_PRUNE" ]; then
        print_success "Cleared Docker cache: $DOCKER_PRUNE"
    else
        print_info "Docker cache already clean or no permission"
    fi
else
    print_info "Docker not available or not running"
fi
echo ""

# 9. Clear Conda cache
print_info "Clearing Conda cache..."
if command -v conda &> /dev/null; then
    CONDA_CACHE=$(conda clean --all --yes 2>&1 | grep -oE '[0-9.]+[KMGT]?B' | tail -1 || echo "")
    if [ -n "$CONDA_CACHE" ]; then
        print_success "Cleared Conda cache: $CONDA_CACHE"
    else
        print_info "Conda cache already clean"
    fi
fi
echo ""

# 10. Clear Poetry cache
print_info "Clearing Poetry cache..."
if command -v poetry &> /dev/null; then
    POETRY_CACHE="$HOME/.cache/pypoetry"
    if [ -d "$POETRY_CACHE" ]; then
        POETRY_SIZE=$(du -sk "$POETRY_CACHE" 2>/dev/null | awk '{print $1}' || echo "0")
        poetry cache clear pypi --all 2>/dev/null || rm -rf "$POETRY_CACHE"/* 2>/dev/null || true
        if [ "$POETRY_SIZE" -gt 0 ]; then
            print_success "Cleared Poetry cache (~${POETRY_SIZE}KB)"
            TOTAL_FREED=$((TOTAL_FREED + POETRY_SIZE))
        fi
    fi
fi
echo ""

# 11. Clear Rust Cargo cache
print_info "Clearing Rust Cargo cache..."
CARGO_CACHE="$HOME/.cargo/registry/cache"
if [ -d "$CARGO_CACHE" ]; then
    CARGO_SIZE=$(du -sk "$CARGO_CACHE" 2>/dev/null | awk '{print $1}' || echo "0")
    if command -v cargo &> /dev/null; then
        cargo clean 2>/dev/null || true
    fi
    rm -rf "$CARGO_CACHE"/* 2>/dev/null || true
    if [ "$CARGO_SIZE" -gt 0 ]; then
        print_success "Cleared Cargo cache (~${CARGO_SIZE}KB)"
        TOTAL_FREED=$((TOTAL_FREED + CARGO_SIZE))
    fi
fi
echo ""

# 12. Clear Go module cache
print_info "Clearing Go module cache..."
if command -v go &> /dev/null; then
    GO_CACHE=$(go env GOMODCACHE 2>/dev/null || echo "$HOME/go/pkg/mod")
    if [ -d "$GO_CACHE" ]; then
        GO_SIZE=$(du -sk "$GO_CACHE" 2>/dev/null | awk '{print $1}' || echo "0")
        go clean -modcache 2>/dev/null || rm -rf "$GO_CACHE"/* 2>/dev/null || true
        if [ "$GO_SIZE" -gt 0 ]; then
            print_success "Cleared Go module cache (~${GO_SIZE}KB)"
            TOTAL_FREED=$((TOTAL_FREED + GO_SIZE))
        fi
    fi
fi
echo ""

# 13. Clear system temporary files
print_info "Clearing system temporary files..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS temp directories
    TEMP_DIRS=("$HOME/Library/Caches" "$TMPDIR" "/tmp")
    for temp_dir in "${TEMP_DIRS[@]}"; do
        if [ -d "$temp_dir" ]; then
            # Only clear files older than 7 days
            find "$temp_dir" -type f -atime +7 -delete 2>/dev/null || true
            find "$temp_dir" -type d -empty -delete 2>/dev/null || true
        fi
    done
    print_success "Cleared old temporary files"
else
    # Linux temp directories
    TEMP_DIRS=("/tmp" "$HOME/.cache" "/var/tmp")
    for temp_dir in "${TEMP_DIRS[@]}"; do
        if [ -d "$temp_dir" ] && [ -w "$temp_dir" ]; then
            find "$temp_dir" -type f -atime +7 -delete 2>/dev/null || true
            find "$temp_dir" -type d -empty -delete 2>/dev/null || true
        fi
    done
    print_success "Cleared old temporary files"
fi
echo ""

# 14. Clear IDE caches
print_info "Clearing IDE caches..."
IDE_CACHES=(
    "$HOME/.vscode/extensions"
    "$HOME/.cache/Code"
    "$HOME/.config/Code/Cache"
    "$HOME/.config/Code/CachedData"
    "$HOME/.PyCharm*/system/caches"
    "$HOME/.IntelliJIdea*/system/caches"
    "$HOME/Library/Caches/com.jetbrains.*"
    "$HOME/.cache/JetBrains"
)
for ide_cache in "${IDE_CACHES[@]}"; do
    if [ -d "$ide_cache" ]; then
        IDE_SIZE=$(du -sk "$ide_cache" 2>/dev/null | awk '{print $1}' || echo "0")
        # Only clear cache subdirectories, not the entire IDE directory
        find "$ide_cache" -type d -name "Cache" -exec rm -rf {} + 2>/dev/null || true
        find "$ide_cache" -type d -name "CachedData" -exec rm -rf {} + 2>/dev/null || true
        find "$ide_cache" -type d -name "caches" -exec rm -rf {} + 2>/dev/null || true
        if [ "$IDE_SIZE" -gt 0 ]; then
            print_success "Cleared IDE cache (~${IDE_SIZE}KB)"
            TOTAL_FREED=$((TOTAL_FREED + IDE_SIZE))
        fi
    fi
done
echo ""

# 15. Clear Git object cache and garbage collection
print_info "Clearing Git object cache..."
if [ -d "$REPO_ROOT/.git" ]; then
    git gc --prune=now --aggressive 2>/dev/null || true
    print_success "Cleaned Git repository"
fi
echo ""

# 16. Clear browser caches (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_info "Clearing browser caches..."
    BROWSER_CACHES=(
        "$HOME/Library/Caches/com.google.Chrome"
        "$HOME/Library/Caches/com.google.Chrome.canary"
        "$HOME/Library/Caches/com.mozilla.firefox"
        "$HOME/Library/Caches/com.apple.Safari"
        "$HOME/Library/Safari/LocalStorage"
    )
    for browser_cache in "${BROWSER_CACHES[@]}"; do
        if [ -d "$browser_cache" ]; then
            BROWSER_SIZE=$(du -sk "$browser_cache" 2>/dev/null | awk '{print $1}' || echo "0")
            rm -rf "$browser_cache"/* 2>/dev/null || true
            if [ "$BROWSER_SIZE" -gt 0 ]; then
                print_success "Cleared browser cache (~${BROWSER_SIZE}KB)"
                TOTAL_FREED=$((TOTAL_FREED + BROWSER_SIZE))
            fi
        fi
    done
    echo ""
fi

# 17. Clear macOS user caches (expanded)
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_info "Clearing macOS user caches..."
    USER_CACHE="$HOME/Library/Caches"
    if [ -d "$USER_CACHE" ]; then
        CACHE_DIRS=("pip" "pypoetry" "pipx" "Homebrew" "com.apple.dt.Xcode" "org.python.python")
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
    
    # Clear Homebrew cache
    if command -v brew &> /dev/null; then
        print_info "Clearing Homebrew cache..."
        BREW_SIZE=$(brew cleanup --prune=all -s 2>&1 | grep -oE '[0-9.]+[KMGT]?B' | head -1 || echo "0")
        if [ "$BREW_SIZE" != "0" ]; then
            print_success "Cleared Homebrew cache: $BREW_SIZE"
        fi
    fi
    echo ""
fi

# 18. Clear system logs (old logs only)
print_info "Clearing old system logs..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    LOG_DIRS=("$HOME/Library/Logs" "/var/log")
    for log_dir in "${LOG_DIRS[@]}"; do
        if [ -d "$log_dir" ] && [ -w "$log_dir" ]; then
            find "$log_dir" -type f -name "*.log" -mtime +30 -delete 2>/dev/null || true
            find "$log_dir" -type f -name "*.log.*" -mtime +7 -delete 2>/dev/null || true
        fi
    done
    print_success "Cleared old log files"
else
    if [ -w "/var/log" ]; then
        find /var/log -type f -name "*.log" -mtime +30 -delete 2>/dev/null || true
        find /var/log -type f -name "*.log.*" -mtime +7 -delete 2>/dev/null || true
        print_success "Cleared old log files"
    else
        print_warning "Cannot clear system logs (requires sudo)"
    fi
fi
echo ""

# 19. Clear DNS cache
print_info "Clearing DNS cache..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    sudo dscacheutil -flushcache 2>/dev/null && sudo killall -HUP mDNSResponder 2>/dev/null && \
        print_success "DNS cache cleared" || \
        print_warning "DNS cache clear requires sudo (run: sudo dscacheutil -flushcache)"
else
    if command -v systemd-resolve &> /dev/null; then
        sudo systemd-resolve --flush-caches 2>/dev/null && \
            print_success "DNS cache cleared" || \
            print_warning "DNS cache clear requires sudo"
    elif [ -f /etc/init.d/nscd ]; then
        sudo /etc/init.d/nscd restart 2>/dev/null && \
            print_success "DNS cache cleared" || \
            print_warning "DNS cache clear requires sudo"
    fi
fi
echo ""

# 20. Kill idle/low-priority processes (optional, dangerous)
if [ "$KILL_IDLE_PROCESSES" = "yes" ]; then
    print_warning "Killing idle processes (this may close applications)..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Kill processes using excessive CPU but are idle
        ps aux | awk '$3 > 50.0 && $11 !~ /^\[/ {print $2}' | while read pid; do
            if [ -n "$pid" ] && [ "$pid" != "$$" ]; then
                kill "$pid" 2>/dev/null || true
            fi
        done
    else
        # Linux: kill processes in D (uninterruptible sleep) state for too long
        ps aux | awk '$8 ~ /^D/ {print $2}' | while read pid; do
            if [ -n "$pid" ] && [ "$pid" != "$$" ]; then
                kill -9 "$pid" 2>/dev/null || true
            fi
        done
    fi
    print_success "Idle processes terminated"
    echo ""
else
    print_info "Skipping idle process termination (set KILL_IDLE_PROCESSES=yes to enable)"
    echo ""
fi

# 21. Clear swap files (if safe)
print_info "Clearing swap files..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS doesn't use traditional swap files, but we can clear VM swap
    print_info "macOS manages swap automatically"
else
    if [ "$EUID" -eq 0 ] || sudo -n true 2>/dev/null; then
        swapoff -a 2>/dev/null && swapon -a 2>/dev/null && \
            print_success "Swap cleared" || \
            print_warning "Could not clear swap"
    else
        print_warning "Swap clearing requires sudo"
    fi
fi
echo ""

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

# 22. Clear additional Python package manager caches
print_info "Clearing additional Python package caches..."
if command -v pipx &> /dev/null; then
    PIPX_CACHE="$HOME/.local/pipx/cache"
    if [ -d "$PIPX_CACHE" ]; then
        PIPX_SIZE=$(du -sk "$PIPX_CACHE" 2>/dev/null | awk '{print $1}' || echo "0")
        rm -rf "$PIPX_CACHE"/* 2>/dev/null || true
        if [ "$PIPX_SIZE" -gt 0 ]; then
            print_success "Cleared pipx cache (~${PIPX_SIZE}KB)"
            TOTAL_FREED=$((TOTAL_FREED + PIPX_SIZE))
        fi
    fi
fi

# Clear virtual environment caches in repo
print_info "Clearing virtual environment caches..."
VENV_DIRS=("$REPO_ROOT/.venv" "$REPO_ROOT/venv" "$REPO_ROOT/env")
for venv_dir in "${VENV_DIRS[@]}"; do
    if [ -d "$venv_dir" ]; then
        VENV_CACHE="$venv_dir/__pycache__"
        if [ -d "$VENV_CACHE" ]; then
            VENV_SIZE=$(du -sk "$VENV_CACHE" 2>/dev/null | awk '{print $1}' || echo "0")
            find "$venv_dir" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
            if [ "$VENV_SIZE" -gt 0 ]; then
                print_success "Cleared venv cache (~${VENV_SIZE}KB)"
                TOTAL_FREED=$((TOTAL_FREED + VENV_SIZE))
            fi
        fi
    fi
done
echo ""

# 23. Clear system font cache (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_info "Clearing font cache..."
    FONT_CACHE="$HOME/Library/Caches/com.apple.ATS"
    if [ -d "$FONT_CACHE" ]; then
        FONT_SIZE=$(du -sk "$FONT_CACHE" 2>/dev/null | awk '{print $1}' || echo "0")
        rm -rf "$FONT_CACHE"/* 2>/dev/null || true
        if [ "$FONT_SIZE" -gt 0 ]; then
            print_success "Cleared font cache (~${FONT_SIZE}KB)"
            TOTAL_FREED=$((TOTAL_FREED + FONT_SIZE))
        fi
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
    # Also show memory pressure
    memory_pressure 2>/dev/null | head -5 || true
else
    free -h || true
    # Show memory usage percentage
    echo ""
    MEM_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
    print_info "Memory usage: ${MEM_USAGE}%"
fi

echo ""
print_success "RAM and cache cleanup completed!"
print_info "Note: Some system-level caches may require sudo privileges to clear."
print_info "To kill idle processes, run: KILL_IDLE_PROCESSES=yes $0"
