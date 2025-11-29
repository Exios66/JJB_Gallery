#!/usr/bin/env bash

# Git SSH Setup Script
# Configures SSH keys for GitHub and updates remote URL

set -euo pipefail

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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Get email from git config
GIT_EMAIL=$(git config user.email 2>/dev/null || echo "")
if [ -z "$GIT_EMAIL" ]; then
    read -p "Enter your GitHub email: " GIT_EMAIL
fi

SSH_KEY_NAME="id_ed25519"
SSH_KEY_PATH="$HOME/.ssh/$SSH_KEY_NAME"
SSH_PUB_KEY_PATH="$SSH_KEY_PATH.pub"

print_info "Setting up SSH for GitHub..."

# Check if SSH key already exists
if [ -f "$SSH_KEY_PATH" ]; then
    print_warning "SSH key already exists: $SSH_KEY_PATH"
    read -p "Generate new key? [y/N]: " generate_new
    if [[ ! "$generate_new" =~ ^[Yy]$ ]]; then
        print_info "Using existing key"
    else
        # Backup existing key
        BACKUP_PATH="${SSH_KEY_PATH}.backup.$(date +%s)"
        print_info "Backing up existing key to $BACKUP_PATH"
        mv "$SSH_KEY_PATH" "$BACKUP_PATH"
        mv "${SSH_KEY_PATH}.pub" "${BACKUP_PATH}.pub" 2>/dev/null || true
    fi
fi

# Generate SSH key if needed
if [ ! -f "$SSH_KEY_PATH" ]; then
    print_info "Generating new SSH key..."
    ssh-keygen -t ed25519 -C "$GIT_EMAIL" -f "$SSH_KEY_PATH" -N ""
    print_success "SSH key generated"
else
    print_success "Using existing SSH key"
fi

# Start SSH agent
print_info "Starting SSH agent..."
eval "$(ssh-agent -s)" > /dev/null

# Add key to SSH agent
if [ -f "$SSH_KEY_PATH" ]; then
    ssh-add "$SSH_KEY_PATH" 2>/dev/null || {
        print_warning "Could not add key to SSH agent (may already be added)"
    }
fi

# Display public key
print_info "Your public SSH key:"
echo ""
cat "$SSH_PUB_KEY_PATH"
echo ""

# Copy to clipboard (macOS)
if command -v pbcopy &> /dev/null; then
    pbcopy < "$SSH_PUB_KEY_PATH"
    print_success "Public key copied to clipboard!"
elif command -v xclip &> /dev/null; then
    xclip -selection clipboard < "$SSH_PUB_KEY_PATH"
    print_success "Public key copied to clipboard!"
else
    print_info "Please copy the public key above manually"
fi

print_info "Next steps:"
echo "  1. Go to: https://github.com/settings/keys"
echo "  2. Click 'New SSH key'"
echo "  3. Paste your public key (already in clipboard if on macOS)"
echo "  4. Click 'Add SSH key'"
echo ""
read -p "Press Enter when you've added the key to GitHub..."

# Test SSH connection
print_info "Testing SSH connection to GitHub..."
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    print_success "SSH connection successful!"
else
    print_warning "SSH connection test returned unexpected result"
    print_info "This is normal if you see 'Hi USERNAME! You've successfully authenticated'"
    ssh -T git@github.com || true
fi

# Update git remote to use SSH
cd "$REPO_ROOT"

if [ -d ".git" ]; then
    CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
    
    if [[ "$CURRENT_REMOTE" == *"github.com"* ]] && [[ "$CURRENT_REMOTE" != *"git@"* ]]; then
        # Extract owner and repo from HTTPS URL
        if [[ "$CURRENT_REMOTE" =~ github\.com[:/]([^/]+)/([^/]+)(\.git)?$ ]]; then
            OWNER="${BASH_REMATCH[1]}"
            REPO="${BASH_REMATCH[2]%.git}"
            SSH_URL="git@github.com:$OWNER/$REPO.git"
            
            print_info "Updating remote URL to SSH..."
            read -p "Change remote from HTTPS to SSH? [Y/n]: " change_remote
            change_remote=${change_remote:-Y}
            
            if [[ "$change_remote" =~ ^[Yy]$ ]]; then
                git remote set-url origin "$SSH_URL"
                print_success "Remote URL updated to: $SSH_URL"
                
                # Verify
                print_info "Verifying remote..."
                git remote -v
                
                # Test fetch
                print_info "Testing connection..."
                if git fetch origin --dry-run &>/dev/null; then
                    print_success "Git remote working with SSH!"
                else
                    print_warning "Could not test fetch (this may be normal)"
                fi
            fi
        fi
    elif [[ "$CURRENT_REMOTE" == *"git@"* ]]; then
        print_info "Remote is already using SSH: $CURRENT_REMOTE"
    else
        print_warning "Could not detect GitHub remote URL"
    fi
else
    print_warning "Not a git repository, skipping remote update"
fi

echo ""
print_success "SSH setup complete!"
print_info "You can now use Git without password prompts"
print_info "For GitHub CLI, ensure you're authenticated: gh auth login"

