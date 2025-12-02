#!/bin/bash
# Verify External Storage Configuration
# Checks that all package managers are using external drive

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

EXTERNAL_BASE="/Volumes/SEALED/DSHB/GALLERY"

echo -e "${BLUE}🔍 Verifying External Storage Configuration...${NC}\n"

# Check if external drive is mounted
if [ ! -d "$EXTERNAL_BASE" ]; then
    echo -e "${RED}❌ External drive not mounted at: $EXTERNAL_BASE${NC}"
    echo -e "${YELLOW}   Please mount the USB drive and run setup-external-storage.sh${NC}"
    exit 1
fi

echo -e "${GREEN}✓ External drive mounted${NC}\n"

# Check NPM configuration
echo "📦 NPM Configuration:"
if command -v npm &> /dev/null; then
    NPM_CACHE=$(npm config get cache 2>/dev/null || echo "not set")
    if [[ "$NPM_CACHE" == *"$EXTERNAL_BASE"* ]]; then
        echo -e "   ${GREEN}✓ Cache: $NPM_CACHE${NC}"
    else
        echo -e "   ${RED}❌ Cache: $NPM_CACHE (not on external drive)${NC}"
    fi
    
    # Check .npmrc file
    if grep -q "$EXTERNAL_BASE" .npmrc 2>/dev/null; then
        echo -e "   ${GREEN}✓ .npmrc configured${NC}"
    else
        echo -e "   ${YELLOW}⚠ .npmrc may not be configured${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠ npm not installed${NC}"
fi

# Check Pip configuration
echo ""
echo "🐍 Pip Configuration:"
if command -v pip &> /dev/null; then
    PIP_CACHE=$(pip cache dir 2>/dev/null || echo "not set")
    if [[ "$PIP_CACHE" == *"$EXTERNAL_BASE"* ]]; then
        echo -e "   ${GREEN}✓ Cache: $PIP_CACHE${NC}"
    else
        echo -e "   ${RED}❌ Cache: $PIP_CACHE (not on external drive)${NC}"
        echo -e "   ${YELLOW}   Run: pip config set global.cache-dir $EXTERNAL_BASE/.pip-cache${NC}"
    fi
    
    # Check pip.conf
    if [ -f "config/pip.conf" ] && grep -q "$EXTERNAL_BASE" config/pip.conf 2>/dev/null; then
        echo -e "   ${GREEN}✓ pip.conf configured${NC}"
    else
        echo -e "   ${YELLOW}⚠ pip.conf not found or not configured${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠ pip not installed${NC}"
fi

# Check Python virtual environments
echo ""
echo "🐍 Python Virtual Environments:"
if [ -n "$WORKON_HOME" ]; then
    if [[ "$WORKON_HOME" == *"$EXTERNAL_BASE"* ]]; then
        echo -e "   ${GREEN}✓ WORKON_HOME: $WORKON_HOME${NC}"
    else
        echo -e "   ${YELLOW}⚠ WORKON_HOME: $WORKON_HOME (not on external drive)${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠ WORKON_HOME not set${NC}"
fi

# Check environment variables
echo ""
echo "🔧 Environment Variables:"
if [ -n "$NPM_CONFIG_CACHE" ]; then
    if [[ "$NPM_CONFIG_CACHE" == *"$EXTERNAL_BASE"* ]]; then
        echo -e "   ${GREEN}✓ NPM_CONFIG_CACHE: $NPM_CONFIG_CACHE${NC}"
    else
        echo -e "   ${YELLOW}⚠ NPM_CONFIG_CACHE: $NPM_CONFIG_CACHE${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠ NPM_CONFIG_CACHE not set${NC}"
fi

if [ -n "$PIP_CACHE_DIR" ]; then
    if [[ "$PIP_CACHE_DIR" == *"$EXTERNAL_BASE"* ]]; then
        echo -e "   ${GREEN}✓ PIP_CACHE_DIR: $PIP_CACHE_DIR${NC}"
    else
        echo -e "   ${YELLOW}⚠ PIP_CACHE_DIR: $PIP_CACHE_DIR${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠ PIP_CACHE_DIR not set${NC}"
fi

# Check directory existence
echo ""
echo "📁 External Drive Directories:"
for dir in ".npm-cache" ".npm-tmp" ".pip-cache" ".python-venvs"; do
    if [ -d "$EXTERNAL_BASE/$dir" ]; then
        size=$(du -sh "$EXTERNAL_BASE/$dir" 2>/dev/null | cut -f1)
        echo -e "   ${GREEN}✓ $dir/ (${size})${NC}"
    else
        echo -e "   ${RED}❌ $dir/ (not found)${NC}"
    fi
done

# Check disk space
echo ""
echo "💾 Disk Space:"
echo "   External Drive:"
df -h "$EXTERNAL_BASE" 2>/dev/null | tail -1 | awk '{printf "     %s available / %s total (%s used)\n", $4, $2, $5}'
echo "   Local Drive:"
df -h "$HOME" 2>/dev/null | tail -1 | awk '{printf "     %s available / %s total (%s used)\n", $4, $2, $5}'

echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo "   If you see ❌ or ⚠️, run: npm run setup:external"
echo ""

