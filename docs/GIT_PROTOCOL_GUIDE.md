# Git Protocol & Workflow Best Practices

## Current Setup

- **Repository**: `https://github.com/Exios66/JJB_Gallery.git`
- **Protocol**: HTTPS
- **Branches**: `main`, `gh-pages` (currently on `gh-pages`)
- **User**: Jack J Burleson // Lucius Morningstar

## Recommended Protocol: SSH (for automation) or HTTPS (for simplicity)

### Option 1: SSH (Recommended for automation & GitHub Codespaces)

**Best for**: Automated workflows, GitHub CLI integration, no password prompts

**Setup**:

```bash
# 1. Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "exios4@protonmail.com"

# 2. Start SSH agent
eval "$(ssh-agent -s)"

# 3. Add key to SSH agent
ssh-add ~/.ssh/id_ed25519

# 4. Copy public key to clipboard
pbcopy < ~/.ssh/id_ed25519.pub  # macOS
# or: cat ~/.ssh/id_ed25519.pub

# 5. Add to GitHub:
#    - Go to: https://github.com/settings/keys
#    - Click "New SSH key"
#    - Paste your public key

# 6. Test connection
ssh -T git@github.com

# 7. Update remote URL
git remote set-url origin git@github.com:Exios66/JJB_Gallery.git
```

**Benefits**:

- ✅ No password prompts
- ✅ Works seamlessly with GitHub CLI (`gh`)
- ✅ Better for automation scripts
- ✅ Works well with GitHub Codespaces
- ✅ More secure for CI/CD

### Option 2: HTTPS with Personal Access Token (Current + Secure)

**Best for**: Simple setup, works everywhere, no SSH keys needed

**Current Status**: You're already using HTTPS!

**To secure it**:

```bash
# Use GitHub CLI for authentication (recommended)
gh auth login

# Or use Personal Access Token:
# 1. Go to: https://github.com/settings/tokens
# 2. Generate new token (classic) with 'repo' scope
# 3. Use token as password when prompted
```

**Benefits**:

- ✅ Already configured
- ✅ Works behind firewalls/proxies
- ✅ Simple setup
- ✅ Works with GitHub Codespaces

## Recommended Workflow

### Branch Strategy (Git Flow)

For your project with `main` and `gh-pages` branches:

```text
main (production)          ←─ Stable releases
  │
  ├─ gh-pages (deployment) ←─ GitHub Pages site
  │
  └─ feature/*             ←─ Feature branches (optional)
```

### Workflow Protocol

#### 1. Daily Development

```bash
# Start from main
git checkout main
git pull origin main

# Create feature branch (if needed)
git checkout -b feature/your-feature-name

# Work on your changes
# ... make changes ...

# Commit frequently with clear messages
git add .
git commit -m "feat: add cloud sandbox auto-launch script"
```

#### 2. Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```text
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting, missing semicolons, etc.
refactor: code refactoring
test: adding tests
chore: maintenance tasks
```

**Examples**:

```bash
git commit -m "feat: add cloud sandbox setup script"
git commit -m "fix: resolve import errors in crewai agents"
git commit -m "docs: update README with cloud sandbox instructions"
git commit -m "chore: update requirements.txt with crewai packages"
```

#### 3. Pushing Changes

```bash
# For main branch
git checkout main
git pull origin main  # Always pull first!
git push origin main

# For gh-pages branch (your current branch)
git checkout gh-pages
git pull origin gh-pages
git push origin gh-pages
```

#### 4. Syncing Branches

```bash
# Update gh-pages from main (when ready to deploy)
git checkout gh-pages
git merge main
git push origin gh-pages

# Or rebase (cleaner history)
git checkout gh-pages
git rebase main
git push origin gh-pages
```

## Best Practices for Your Setup

### 1. Pre-push Checklist

Before pushing:

```bash
# 1. Check status
git status

# 2. Review changes
git diff

# 3. Ensure working directory is clean
# (no uncommitted changes unless intentional)

# 4. Pull latest changes
git pull origin <branch-name>

# 5. Run tests/linting (if applicable)
# ./scripts/free_ram.sh  # Example

# 6. Push
git push origin <branch-name>
```

### 2. Integration with Cloud Sandbox

When working with GitHub Codespaces:

```bash
# 1. Work locally
git add .
git commit -m "feat: add new feature"

# 2. Push to GitHub
git push origin main

# 3. Codespace automatically syncs
# (or manually pull in Codespace)
```

### 3. Branch Protection Rules

Consider setting up on GitHub:

- Require pull requests for `main`
- Require status checks
- Require review (if working with team)

### 4. Handling Disk Space Constraints

```bash
# Use sparse checkout for large repos
git sparse-checkout init --cone
git sparse-checkout set 'projects/CrewAI'

# Clean up old branches locally
git branch -d old-branch

# Prune remote tracking branches
git remote prune origin
```

## Git Configuration Recommendations

### Essential Config

```bash
# Set default branch name
git config --global init.defaultBranch main

# Set default pull behavior
git config --global pull.rebase false  # or 'true' if you prefer rebase

# Set editor (if not already set)
git config --global core.editor "code --wait"  # VS Code
# or: git config --global core.editor "nano"

# Enable helpful aliases

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
```

### Credential Management

**For HTTPS**:

```bash
# macOS: Use keychain
git config --global credential.helper osxkeychain

# Cache credentials (1 hour)
git config --global credential.helper 'cache --timeout=3600'
```

**For SSH**: No credential helper needed (uses SSH keys)

## Recommended Protocol Choice

**For your situation**: **SSH** is recommended because:

1. ✅ You're using GitHub Codespaces (works seamlessly)
2. ✅ You're using GitHub CLI (`gh`) - SSH integrates better
3. ✅ No password prompts during automation
4. ✅ Better for your cloud sandbox scripts
5. ✅ More secure for automated workflows

**If you prefer simplicity**: **HTTPS + GitHub CLI** is also fine:

```bash
gh auth login
# This handles HTTPS authentication automatically
```

## Quick Migration to SSH

If you want to switch to SSH (recommended):

```bash
# 1. Setup SSH (see above)
# 2. Update remote
git remote set-url origin git@github.com:Exios66/JJB_Gallery.git

# 3. Verify
git remote -v

# 4. Test
git fetch origin
```

## Troubleshooting

### Authentication Issues (HTTPS)

```bash
# Re-authenticate with GitHub CLI
gh auth login

# Or use token
git remote set-url origin https://YOUR_TOKEN@github.com/Exios66/JJB_Gallery.git
```

### SSH Connection Issues

```bash
# Test SSH
ssh -T git@github.com

# Check SSH agent
ssh-add -l

# Add key to agent
ssh-add ~/.ssh/id_ed25519
```

### Large File Issues

```bash
# Use Git LFS for large files
git lfs install
git lfs track "*.ipynb"
git add .gitattributes
```

## Summary

**Recommended Protocol**: **SSH** for your use case

- Better automation support
- Works with GitHub CLI/Codespaces
- No password prompts
- More secure

**Alternative**: **HTTPS + GitHub CLI** if you prefer simplicity

- Already configured
- `gh auth login` handles authentication
- Works well with your current setup

Both work great! Choose based on your preference for automation vs simplicity.

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
