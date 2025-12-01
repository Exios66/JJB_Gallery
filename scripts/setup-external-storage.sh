#!/bin/bash
# Setup External USB Drive Storage Configuration
# Configures npm, pip, and other package managers to use external drive

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# External drive base path
EXTERNAL_BASE="/Volumes/SEALED/DSHB/GALLERY"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${BLUE}🔧 Setting up external USB drive storage...${NC}\n"

# Check if external drive is mounted
if [ ! -d "$EXTERNAL_BASE" ]; then
    echo -e "${YELLOW}⚠️  External drive not found at: $EXTERNAL_BASE${NC}"
    echo -e "${YELLOW}   Please mount the USB drive and update EXTERNAL_BASE in this script${NC}"
    exit 1
fi

echo -e "${GREEN}✓ External drive found at: $EXTERNAL_BASE${NC}\n"

# Create directories on external drive
echo "📁 Creating directories on external drive..."
mkdir -p "$EXTERNAL_BASE/.npm-cache"
mkdir -p "$EXTERNAL_BASE/.npm-tmp"
mkdir -p "$EXTERNAL_BASE/.npm-global"
mkdir -p "$EXTERNAL_BASE/.pip-cache"
mkdir -p "$EXTERNAL_BASE/.python-venvs"
mkdir -p "$EXTERNAL_BASE/.node-modules"
mkdir -p "$EXTERNAL_BASE/.quarto-cache"

echo -e "${GREEN}✓ Directories created${NC}\n"

# Configure NPM
echo "📦 Configuring NPM..."
if command -v npm &> /dev/null; then
    # Set npm cache location
    npm config set cache "$EXTERNAL_BASE/.npm-cache" --global
    
    # Set npm tmp location
    export TMPDIR="$EXTERNAL_BASE/.npm-tmp"
    
    # Verify configuration
    echo "   Cache location: $(npm config get cache)"
    echo -e "${GREEN}✓ NPM configured${NC}\n"
else
    echo -e "${YELLOW}⚠️  npm not found, skipping${NC}\n"
fi

# Configure Pip
echo "🐍 Configuring Pip..."
if command -v pip &> /dev/null; then
    # Try to set via pip config command
    pip config set global.cache-dir "$EXTERNAL_BASE/.pip-cache" 2>/dev/null || true
    
    # Also install pip.conf to user directory
    if [ -f "$REPO_ROOT/pip.conf" ]; then
        PIP_CONFIG_DIR="$HOME/.pip"
        mkdir -p "$PIP_CONFIG_DIR"
        if [ ! -f "$PIP_CONFIG_DIR/pip.conf" ]; then
            cp "$REPO_ROOT/pip.conf" "$PIP_CONFIG_DIR/pip.conf"
            echo "   Installed pip.conf to $PIP_CONFIG_DIR"
        else
            echo "   pip.conf already exists in $PIP_CONFIG_DIR"
        fi
    fi
    
    # Set environment variable as fallback
    export PIP_CACHE_DIR="$EXTERNAL_BASE/.pip-cache"
    
    # Verify
    PIP_CACHE=$(pip cache dir 2>/dev/null || echo "not set")
    echo "   Cache location: $PIP_CACHE"
    echo -e "${GREEN}✓ Pip configured${NC}\n"
else
    echo -e "${YELLOW}⚠️  pip not found, skipping${NC}\n"
fi

# Configure Python virtual environments
echo "🐍 Configuring Python virtual environments..."
if command -v python3 &> /dev/null; then
    export WORKON_HOME="$EXTERNAL_BASE/.python-venvs"
    echo "   Virtual environments will be stored at: $WORKON_HOME"
    echo -e "${GREEN}✓ Python venv configured${NC}\n"
else
    echo -e "${YELLOW}⚠️  python3 not found, skipping${NC}\n"
fi

# Create .env file with external drive paths
echo "📝 Creating .env file..."
if [ ! -f "$REPO_ROOT/.env" ]; then
    cat > "$REPO_ROOT/.env" << EOF
# External Drive Configuration
EXTERNAL_DRIVE_BASE=$EXTERNAL_BASE
NPM_CACHE_DIR=$EXTERNAL_BASE/.npm-cache
NPM_TMP_DIR=$EXTERNAL_BASE/.npm-tmp
PIP_CACHE_DIR=$EXTERNAL_BASE/.pip-cache
PYTHON_VENV_DIR=$EXTERNAL_BASE/.python-venvs
NODE_MODULES_DIR=$EXTERNAL_BASE/.node-modules

# Export for current session
export NPM_CONFIG_CACHE="$EXTERNAL_BASE/.npm-cache"
export TMPDIR="$EXTERNAL_BASE/.npm-tmp"
export PIP_CACHE_DIR="$EXTERNAL_BASE/.pip-cache"
export WORKON_HOME="$EXTERNAL_BASE/.python-venvs"
EOF
    echo -e "${GREEN}✓ .env file created${NC}\n"
else
    echo -e "${YELLOW}⚠️  .env file already exists, skipping${NC}\n"
fi

# Create shell profile additions
echo "📝 Creating shell profile configuration..."
SHELL_CONFIG=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_CONFIG="$HOME/.bash_profile"
fi

if [ -n "$SHELL_CONFIG" ]; then
    if ! grep -q "JJB_Gallery External Storage" "$SHELL_CONFIG" 2>/dev/null; then
        cat >> "$SHELL_CONFIG" << EOF

# JJB_Gallery External Storage Configuration
export NPM_CONFIG_CACHE="$EXTERNAL_BASE/.npm-cache"
export TMPDIR="$EXTERNAL_BASE/.npm-tmp"
export PIP_CACHE_DIR="$EXTERNAL_BASE/.pip-cache"
export WORKON_HOME="$EXTERNAL_BASE/.python-venvs"
EOF
        echo -e "${GREEN}✓ Added to $SHELL_CONFIG${NC}\n"
        echo -e "${YELLOW}💡 Run: source $SHELL_CONFIG${NC}\n"
    else
        echo -e "${YELLOW}⚠️  Configuration already in $SHELL_CONFIG${NC}\n"
    fi
fi

# Show disk space
echo "💾 Disk Space Information:"
echo "   External Drive:"
df -h "$EXTERNAL_BASE" | tail -1 | awk '{print "     Available: " $4 " / Total: " $2 " (" $5 " used)"}'
echo "   Local Drive:"
df -h "$HOME" | tail -1 | awk '{print "     Available: " $4 " / Total: " $2 " (" $5 " used)"}'

echo ""
echo -e "${GREEN}✅ External storage setup complete!${NC}\n"
echo -e "${BLUE}📋 Next steps:${NC}"
echo "   1. Source your shell config: source $SHELL_CONFIG"
echo "   2. Or restart your terminal"
echo "   3. Run: npm install"
echo "   4. Run: pip install -r requirements-minimal.txt"
echo ""

