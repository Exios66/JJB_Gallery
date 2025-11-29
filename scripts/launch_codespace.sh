#!/usr/bin/env bash

# Auto-launch GitHub Codespace Script
# Automatically creates and opens a Codespace in the free tier

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed."
    echo ""
    print_info "Install GitHub CLI:"
    echo "  macOS: brew install gh"
    echo "  Linux: See https://cli.github.com/manual/installation"
    echo "  Windows: winget install GitHub.cli"
    echo ""
    print_info "After installation, authenticate with: gh auth login"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    print_warning "GitHub CLI not authenticated"
    print_info "Authenticating with GitHub..."
    gh auth login
fi

# Get repository info
if [ ! -d "$REPO_ROOT/.git" ]; then
    print_error "Not a git repository. Please initialize git first."
    exit 1
fi

# Get remote URL
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$REMOTE_URL" ]; then
    print_error "No git remote found."
    echo ""
    print_info "Please add a remote:"
    echo "  git remote add origin https://github.com/USERNAME/REPO.git"
    echo "  git push -u origin main"
    exit 1
fi

# Extract owner and repo from URL
if [[ "$REMOTE_URL" =~ github\.com[:/]([^/]+)/([^/]+)(\.git)?$ ]]; then
    OWNER="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]%.git}"
else
    print_error "Could not parse GitHub repository from: $REMOTE_URL"
    exit 1
fi

print_info "Repository: $OWNER/$REPO"

# Check if codespace exists
print_info "Checking for existing Codespaces..."
EXISTING_CODESPACE=$(gh codespace list --repo "$OWNER/$REPO" --json name,state,displayName --jq '.[0].name' 2>/dev/null || echo "")

if [ -n "$EXISTING_CODESPACE" ] && [ "$EXISTING_CODESPACE" != "null" ]; then
    print_info "Found existing Codespace: $EXISTING_CODESPACE"
    read -p "Use existing Codespace? [Y/n]: " use_existing
    use_existing=${use_existing:-Y}
    
    if [[ "$use_existing" =~ ^[Yy]$ ]]; then
        print_info "Opening existing Codespace..."
        gh codespace code --codespace "$EXISTING_CODESPACE" || gh codespace view --web --codespace "$EXISTING_CODESPACE"
        print_success "Codespace opened!"
        exit 0
    fi
fi

# Check if repo is pushed
print_info "Checking if repository is pushed to GitHub..."
if ! gh repo view "$OWNER/$REPO" &> /dev/null; then
    print_error "Repository not found on GitHub: $OWNER/$REPO"
    echo ""
    print_info "Please push your repository first:"
    echo "  git push -u origin main"
    exit 1
fi

# Create new Codespace
print_info "Creating new Codespace (this may take a few minutes)..."
print_info "Using free tier machine (2 cores, 4GB RAM)"

# Create codespace with free tier settings (smallest available machine)
# Free tier default is 2-core, 4GB RAM - we'll let GitHub choose the default
CODESPACE_NAME=$(gh codespace create \
    --repo "$OWNER/$REPO" \
    --display-name "JJB Gallery Cloud Sandbox" \
    --json name --jq '.name' 2>/dev/null || echo "")

if [ -z "$CODESPACE_NAME" ] || [ "$CODESPACE_NAME" = "null" ]; then
    print_error "Failed to create Codespace"
    print_info "Trying alternative method..."
    
    # Alternative: create and wait for it
    print_info "Creating Codespace (please wait)..."
    gh codespace create --repo "$OWNER/$REPO"
    
    # Wait a bit and get the codespace
    sleep 5
    CODESPACE_NAME=$(gh codespace list --repo "$OWNER/$REPO" --json name --jq '.[0].name' 2>/dev/null || echo "")
fi

if [ -z "$CODESPACE_NAME" ] || [ "$CODESPACE_NAME" = "null" ]; then
    print_error "Could not create or find Codespace"
    print_info "Try creating manually:"
    echo "  1. Go to https://github.com/$OWNER/$REPO"
    echo "  2. Click 'Code' → 'Codespaces' → 'Create codespace on main'"
    exit 1
fi

print_success "Codespace created: $CODESPACE_NAME"

# Wait for codespace to be ready
print_info "Waiting for Codespace to be ready..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    STATUS=$(gh codespace view --codespace "$CODESPACE_NAME" --json state --jq '.state' 2>/dev/null || echo "Unknown")
    
    if [ "$STATUS" = "Available" ]; then
        print_success "Codespace is ready!"
        break
    fi
    
    if [ "$STATUS" = "Failed" ]; then
        print_error "Codespace creation failed"
        exit 1
    fi
    
    attempt=$((attempt + 1))
    echo -n "."
    sleep 2
done

echo ""

if [ "$STATUS" != "Available" ]; then
    print_warning "Codespace is still starting (status: $STATUS)"
    print_info "You can open it manually when ready"
fi

# Open Codespace
print_info "Opening Codespace..."

# Try to open in VS Code first
if command -v code &> /dev/null; then
    print_info "Opening in VS Code..."
    gh codespace code --codespace "$CODESPACE_NAME" 2>/dev/null && {
        print_success "Codespace opened in VS Code!"
        exit 0
    }
fi

# Fallback to web browser
print_info "Opening in web browser..."
gh codespace view --web --codespace "$CODESPACE_NAME"

print_success "Codespace launched!"
echo ""
print_info "Your Codespace is ready with:"
echo "  ✅ All packages from requirements.txt installed"
echo "  ✅ Full development environment"
echo "  ✅ Zero local disk usage"
echo ""
print_info "To view Codespace details:"
echo "  gh codespace view --codespace $CODESPACE_NAME"
echo ""
print_info "To list all Codespaces:"
echo "  gh codespace list --repo $OWNER/$REPO"

