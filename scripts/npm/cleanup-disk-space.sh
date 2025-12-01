#!/bin/bash
# Disk Space Cleanup Script for NPM and Development
# Cleans up npm cache, node_modules, and temporary files to free disk space
# Now includes external drive cleanup options

set -e

echo "🧹 Starting Disk Space Cleanup..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# External drive base path
EXTERNAL_BASE="${EXTERNAL_DRIVE_BASE:-/Volumes/SEALED/DSHB/GALLERY}"

# Function to get directory size
get_size() {
    if [ -d "$1" ]; then
        du -sh "$1" 2>/dev/null | cut -f1
    else
        echo "0"
    fi
}

# Function to clean directory
clean_dir() {
    local dir=$1
    local name=$2
    
    if [ -d "$dir" ]; then
        local size=$(get_size "$dir")
        echo -e "${YELLOW}Cleaning ${name}...${NC} (Size: ${size})"
        rm -rf "$dir"
        echo -e "${GREEN}✓ Cleaned ${name}${NC}"
    else
        echo -e "${YELLOW}⚠ ${name} not found, skipping${NC}"
    fi
}

# Ask user which cleanup to perform
echo -e "${BLUE}Select cleanup option:${NC}"
echo "  1) Local only (default)"
echo "  2) External drive only"
echo "  3) Both local and external"
read -p "Enter choice [1-3]: " choice
choice=${choice:-1}

# 1. Clean NPM cache
if [ "$choice" = "1" ] || [ "$choice" = "3" ]; then
    echo ""
    echo "📦 Cleaning Local NPM cache..."
    if command -v npm &> /dev/null; then
        npm cache clean --force 2>/dev/null || true
        echo -e "${GREEN}✓ Local NPM cache cleaned${NC}"
    else
        echo -e "${YELLOW}⚠ npm not found${NC}"
    fi
fi

if [ "$choice" = "2" ] || [ "$choice" = "3" ]; then
    if [ -d "$EXTERNAL_BASE/.npm-cache" ]; then
        echo ""
        echo "📦 Cleaning External NPM cache..."
        clean_dir "$EXTERNAL_BASE/.npm-cache" "External NPM cache"
    fi
fi

# 2. Clean node_modules in root
if [ "$choice" = "1" ] || [ "$choice" = "3" ]; then
    clean_dir "node_modules" "Root node_modules"
fi

# 3. Clean node_modules in workspaces
if [ -d "projects/ChatUi" ]; then
    clean_dir "projects/ChatUi/node_modules" "ChatUi node_modules"
fi

# 4. Clean build artifacts
clean_dir "dist" "Dist directory"
clean_dir "build" "Build directory"
clean_dir ".cache" "Cache directory"

# 5. Clean Python cache (if exists)
if [ "$choice" = "1" ] || [ "$choice" = "3" ]; then
    clean_dir "__pycache__" "Python cache"
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
fi

# 6. Clean temporary files
echo ""
echo "🗑️  Cleaning temporary files..."
find . -type f -name "*.tmp" -delete 2>/dev/null || true
find . -type f -name "*.temp" -delete 2>/dev/null || true
find . -type f -name ".DS_Store" -delete 2>/dev/null || true

# 7. Clean pip cache (if exists)
if [ "$choice" = "1" ] || [ "$choice" = "3" ]; then
    if command -v pip &> /dev/null; then
        echo "🐍 Cleaning local pip cache..."
        pip cache purge 2>/dev/null || true
        echo -e "${GREEN}✓ Local pip cache cleaned${NC}"
    fi
fi

if [ "$choice" = "2" ] || [ "$choice" = "3" ]; then
    if [ -d "$EXTERNAL_BASE/.pip-cache" ]; then
        echo "🐍 Cleaning external pip cache..."
        clean_dir "$EXTERNAL_BASE/.pip-cache" "External pip cache"
    fi
fi

# 8. Clean npm temporary directories
if [ "$choice" = "1" ] || [ "$choice" = "3" ]; then
    if [ -d "$HOME/.npm/_cacache" ]; then
        echo "📦 Cleaning npm cache directory..."
        rm -rf "$HOME/.npm/_cacache/tmp" 2>/dev/null || true
        echo -e "${GREEN}✓ NPM cache tmp cleaned${NC}"
    fi
fi

if [ "$choice" = "2" ] || [ "$choice" = "3" ]; then
    if [ -d "$EXTERNAL_BASE/.npm-tmp" ]; then
        echo "📦 Cleaning external npm tmp..."
        rm -rf "$EXTERNAL_BASE/.npm-tmp"/* 2>/dev/null || true
        echo -e "${GREEN}✓ External npm tmp cleaned${NC}"
    fi
fi

# 9. Show disk space
echo ""
echo "💾 Current Disk Space:"
if command -v df &> /dev/null; then
    echo "   Local Drive:"
    df -h "$HOME" 2>/dev/null | tail -1 | awk '{print "     Available: " $4 " / Total: " $2 " (" $5 " used)"}' || true
    
    if [ -d "$EXTERNAL_BASE" ]; then
        echo "   External Drive:"
        df -h "$EXTERNAL_BASE" 2>/dev/null | tail -1 | awk '{print "     Available: " $4 " / Total: " $2 " (" $5 " used)"}' || true
    fi
fi

echo ""
echo -e "${GREEN}✅ Cleanup completed!${NC}"
echo ""
echo "💡 To reinstall dependencies:"
echo "   npm install"
echo "   pip install -r requirements-minimal.txt"
echo ""
