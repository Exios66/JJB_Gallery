# Scripts Documentation

Comprehensive documentation for all scripts and automation tools in the JJB Gallery repository.

## 📋 Table of Contents

- [Overview](#overview)
- [Rendering Scripts](#rendering-scripts)
- [System Management Scripts](#system-management-scripts)
- [Cloud & Remote Scripts](#cloud--remote-scripts)
- [Storage & Setup Scripts](#storage--setup-scripts)
- [Git & SSH Scripts](#git--ssh-scripts)
- [NPM Scripts](#npm-scripts)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)
- [Related Documentation](#related-documentation)

## Overview

The `scripts/` directory contains automation tools for rendering, system management, cloud development, storage configuration, and Git setup. All scripts are designed to be run from the repository root using `./scripts/script_name.sh`.

## Rendering Scripts

### `render_gh_pages.sh` - Main GitHub Pages Renderer

The primary script for rendering all GitHub Pages content. Renders all Quarto pages defined in `_quarto.yml` for the complete website.

#### What It Renders

This script renders all pages configured in `_quarto.yml`:

- ✅ `index.html` (Home page)
- ✅ `CHANGELOG.html`
- ✅ `SECURITY.html`
- ✅ `projects/CrewAI/README.html`
- ✅ `projects/terminal_agents/README.html`
- ✅ `projects/RAG_Model/README.html`
- ✅ `projects/Psychometrics/README.html`
- ✅ `projects/ChatUi/README.html`
- ✅ `projects/ios_chatbot/README.html`
- ✅ `projects/litellm/README.html`
- ✅ `Quarto/randomforest.html`

#### Usage

```bash
# Standard rendering (cleans build artifacts first)
./scripts/render_gh_pages.sh

# Render without cleaning (faster, but may have stale artifacts)
./scripts/render_gh_pages.sh --no-clean

# Render and start preview server
./scripts/render_gh_pages.sh --preview

# Combine options
./scripts/render_gh_pages.sh --no-clean --preview
```

#### Features

- **Comprehensive rendering**: Renders all website pages in one command
- **Automatic cleanup**: Removes old build artifacts before rendering
- **Python environment detection**: Automatically activates `.venv` or `venv` if available
- **Build organization**: Outputs organized in `_build/quarto/` directory
- **Verification**: Checks that all expected output files were created
- **Preview server**: Optional local preview with `--preview` flag
- **Colored output**: Easy-to-read status messages
- **Error handling**: Fails fast with clear error messages
- **Resource fork management**: Automatically archives macOS `._*` files

#### What It Does

1. ✅ Checks for Quarto installation
2. ✅ Activates Python virtual environment (if available)
3. ✅ Cleans old build artifacts (unless `--no-clean` is used)
4. ✅ Archives macOS resource fork files
5. ✅ Renders all pages defined in `_quarto.yml`
6. ✅ Verifies all expected output files exist
7. ✅ Optionally starts preview server (with `--preview`)

#### When to Use

- **Before deploying to GitHub Pages**: Run this to ensure all pages are up-to-date
- **After editing any Quarto/Markdown files**: Re-render to see changes
- **Local development**: Use with `--preview` to test changes locally
- **CI/CD pipelines**: Use in GitHub Actions for automated deployments

#### Build Output

- **HTML files**: Rendered in repository root (e.g., `index.html`, `CHANGELOG.html`)
- **Build artifacts**: Organized in `_build/quarto/` (gitignored)
- **Support files**: CSS, JS, and other assets in `_build/quarto/site_libs/`

#### Prerequisites

- Quarto CLI installed: <https://quarto.org/docs/get-started/>
- Python environment (optional, but recommended)
- All dependencies from `requirements/requirements.txt` installed

#### Example Workflow

```bash
# 1. Make changes to Quarto/Markdown files
# 2. Render all pages
./scripts/render_gh_pages.sh

# 3. Review changes locally (optional)
./scripts/render_gh_pages.sh --preview

# 4. Commit and push to gh-pages branch
git add .
git commit -m "Update website content"
git push origin gh-pages
```

---

### `render_randomforest.sh` - Render Random Forest Document

Renders the `Quarto/randomforest.qmd` file to HTML and PDF, then starts a preview server.

#### Usage

```bash
./scripts/render_randomforest.sh
```

#### Features

- Renders `Quarto/randomforest.qmd` to HTML and PDF
- Automatically activates Python virtual environment if available
- Starts preview server on port 4343 (configurable via `PORT` environment variable)
- Opens preview in default browser (macOS/Linux)
- Cleans up previous artifacts before rendering
- Archives macOS resource fork files

#### Configuration

```bash
# Change preview host (default: 127.0.0.1)
HOST=0.0.0.0 ./scripts/render_randomforest.sh

# Change preview port (default: 4343)
PORT=8080 ./scripts/render_randomforest.sh
```

#### Output

- `Quarto/randomforest.html` - Rendered HTML document
- `Quarto/randomforest.pdf` - Rendered PDF document
- `Quarto/randomforest_files/` - Support files directory

#### Preview Server

After rendering, the script automatically:

- Starts Quarto preview server on `http://127.0.0.1:4343`
- Opens the URL in your default browser
- Runs in background until you press Ctrl+C

---

### `rerender_gh_pages.sh` - Re-render for GitHub Pages

Legacy script that re-renders `Quarto/randomforest.qmd` and moves output to `index.html`. **Note**: This script is superseded by `render_gh_pages.sh` for most use cases.

#### How to Use

```bash
./scripts/rerender_gh_pages.sh
```

#### Details

1. ✅ Cleans up old `index.html` and Quarto cache/freeze directories
2. ✅ Activates the virtual environment (if available)
3. ✅ Renders the `Quarto/randomforest.qmd` file to HTML
4. ✅ Moves the output HTML to `index.html` in the repository root
5. ✅ Moves/updates the support files directory (`randomforest_files`) to the repository root

#### When Should You Use This Script?

Run this script when you make changes to `Quarto/randomforest.qmd` and want to update the public-facing page on GitHub Pages. However, `render_gh_pages.sh` is recommended for most use cases as it handles all pages.

---

### `fix_quarto_rendering.sh` - Fix Quarto Rendering Issues

Helps resolve kernel timeout errors when rendering Quarto documents with Python code chunks.

#### Usage

```bash
./scripts/fix_quarto_rendering.sh
```

#### What It Does

1. Pre-renders `randomforest.qmd` to create frozen outputs
2. Activates Python virtual environment if available
3. Attempts to render the document to generate cache

#### When Should You Use This Script?

Use this script in the following situations:

- You experience Python kernel timeout errors during Quarto rendering
- There are issues with code execution in Quarto documents
- You need to pre-generate frozen outputs to enable faster subsequent renders

#### Additional Solutions

If issues persist after running this script:

1. Update `_quarto.yml` execute section to use: `freeze: true`
2. Or temporarily comment out `Quarto/randomforest.qmd` from render list
3. Check Python environment and dependencies

---

## System Management Scripts

### `free_ram.sh` - Free System Resources

Enhanced tool that frees up unnecessary RAM, disk space, and compute resources by clearing extensive caches, temporary files, and idle processes.

#### Usage

```bash
# Standard cleanup (safe, recommended)
./scripts/free_ram.sh

# Aggressive cleanup including idle processes (use with caution)
KILL_IDLE_PROCESSES=yes ./scripts/free_ram.sh
```

#### What It Clears

**Python & Development Tools:**

- Python cache files: `__pycache__` directories, `.pyc`, `.pyo`, and `.py[cod]` files
- Jupyter/IPython checkpoints: `.ipynb_checkpoints` directories
- Quarto cache: Quarto freeze directories and user cache
- pip cache: Cached pip packages
- Conda cache: Conda package cache
- Poetry cache: Poetry package cache
- pipx cache: pipx package cache
- Virtual environment caches: Cache files in `.venv`, `venv`, and `env` directories

**Package Manager Caches:**

- npm cache: Node.js package manager cache
- yarn cache: Yarn package manager cache
- Homebrew cache (macOS): Homebrew package cache
- Cargo cache (Rust): Rust package manager cache
- Go module cache: Go language module cache

**System & Application Caches:**

- Docker cache: Docker images, containers, and volumes (unused)
- Browser caches: Chrome, Firefox, Safari caches (macOS)
- IDE caches: VS Code, PyCharm, IntelliJ IDEA caches
- System temporary files: Old temp files (7+ days)
- System logs: Old log files (30+ days)
- Font cache (macOS): System font cache
- DNS cache: System DNS resolver cache

**System Resources (Optional):**

- System page cache (Linux): Kernel page cache (requires sudo)
- Swap files: Clear and reset swap (Linux, requires sudo)

#### Features

- **Comprehensive cleanup**: Clears 20+ different cache types
- **Cross-platform support**: Works on macOS and Linux
- **Colored output**: Easy-to-read status messages
- **Memory reporting**: Shows before/after memory status
- **Safe by default**: Only clears caches, not user data
- **Smart cleanup**: Only removes old temporary files (7+ days)
- **Space tracking**: Reports total space freed
- **Permission-aware**: Skips operations requiring sudo if not available
- **Process management**: Optional idle process termination

#### Advanced Options

**Kill Idle Processes:**

```bash
KILL_IDLE_PROCESSES=yes ./scripts/free_ram.sh
```

**Warning**: This may close applications that appear idle but are actually working.

#### Notes

- **System-level operations** (page cache, swap, DNS) require sudo privileges
- The script will **skip** operations that require elevated privileges if not available
- **All cleanup operations are safe** and only remove cache/temporary files
- **User data is never deleted** - only caches and temporary files
- Old files are preserved (only files 7+ days old are removed from temp directories)
- Browser caches will be cleared - you may need to re-login to some websites
- IDE caches will be cleared - first launch after cleanup may be slower

#### What Gets Preserved

- Your source code and project files
- Git history and repository data
- Installed packages (only caches are cleared)
- User preferences and settings
- Active application data

---

### `archive-macos-resource-forks.sh` - Archive macOS Resource Fork Files

Moves macOS AppleDouble "dot-underscore" files (`._*`) into an archive directory to keep the repository clean while retaining artifacts for inspection.

#### How to Use

```bash
# Archive resource fork files
./scripts/archive-macos-resource-forks.sh

# Dry run (see what would be archived)
./scripts/archive-macos-resource-forks.sh --dry-run

# Quiet mode (minimal output)
./scripts/archive-macos-resource-forks.sh --quiet
```

#### What It Does

- Finds all `._*` files and directories in the repository
- Moves them to `archives/macos-resource-forks/<original-relative-path>`
- Preserves directory structure in archive
- Handles conflicts by appending timestamp and PID
- Excludes `.git/` and `archives/` directories from scanning

#### When to Use

- After copying files from macOS to non-HFS/APFS filesystems
- Before committing changes to avoid committing resource fork files
- When Quarto or other tools encounter issues with `._*` files
- Automatically called by rendering scripts

#### Archive Location

Files are archived to: `archives/macos-resource-forks/`

This directory is gitignored (except `archives/.gitkeep`).

---

### `cleanup-macos-resource-forks.sh` - Clean macOS Resource Forks (Legacy)

Legacy wrapper script that calls `archive-macos-resource-forks.sh`. Use `archive-macos-resource-forks.sh` directly for new usage.

#### Usage

```bash
./scripts/cleanup-macos-resource-forks.sh [--dry-run] [--quiet]
```

This script is a compatibility wrapper and forwards all arguments to `archive-macos-resource-forks.sh`.

---

### `prevent-resource-forks.sh` - Prevent Resource Fork Creation

One-time setup script that configures your shell environment to reduce `._*` file creation on macOS.

#### Usage

```bash
./scripts/prevent-resource-forks.sh
```

#### What It Does

1. Detects your shell (zsh or bash)
2. Adds environment variables to your shell rc file:
   - `export COPYFILE_DISABLE=1`
   - `export COPY_EXTENDED_ATTRIBUTES_DISABLE=1`
3. Provides instructions to apply changes

#### Configuration

The script modifies:

- `~/.zshrc` (for zsh)
- `~/.bashrc` or `~/.bash_profile` (for bash)

#### After Running

```bash
# Apply changes immediately
source ~/.zshrc  # or ~/.bashrc
```

#### Notes

- This only affects **new** operations
- Existing `._*` files are not removed (use `archive-macos-resource-forks.sh`)
- Changes take effect in new terminal sessions
- Can be safely run multiple times (checks for existing configuration)

---

## Cloud & Remote Scripts

### `setup_cloud_sandbox.sh` - Configure Cloud Development Environment

Configures remote Python environments to avoid local disk space usage. Particularly useful when working with large Python packages like CrewAI.

#### Usage

```bash
./scripts/setup_cloud_sandbox.sh
```

#### Available Options

**1. GitHub Codespaces (Recommended)**

- Free tier: 60 hours/month
- Automatic package installation
- Full VS Code in browser
- Zero local disk usage

**2. Remote SSH Server**

- Use existing remote server
- Execute Python remotely
- Requires SSH access

**3. Docker Container**

- Local containerized environment
- Minimal local disk usage
- Requires Docker installed

**4. Replit/CodeSandbox**

- Browser-based development
- Free tiers available
- Manual setup instructions

#### What It Creates

**For GitHub Codespaces:**

- `.devcontainer/devcontainer.json` - VS Code dev container configuration
- `.codespaces/README.md` - Setup instructions

**For SSH:**

- `.cloud_sandbox/config.env` - SSH configuration

**For Docker:**

- `Dockerfile.cloud` - Docker image definition
- `docker-compose.cloud.yml` - Docker Compose configuration
- `.cloud_sandbox/config.env` - Docker configuration

#### Benefits

- No local disk space for Python packages
- Consistent environment
- Easy to reset/recreate
- Cost-effective (many free options)

#### Next Steps

After setup, use `use_cloud_sandbox.sh` to execute commands in the cloud environment.

---

### `use_cloud_sandbox.sh` - Use Cloud Sandbox

Executes Python commands in the configured remote/cloud environment.

#### Usage

```bash
# Execute a Python script remotely
./scripts/use_cloud_sandbox.sh python projects/CrewAI/main.py

# Start interactive session (SSH/Docker)
./scripts/use_cloud_sandbox.sh
```

#### Prerequisites

- Cloud sandbox must be configured (run `setup_cloud_sandbox.sh` first)
- For SSH: valid SSH connection
- For Docker: Docker installed and running
- For Codespaces: Codespace already created

#### Supported Sandbox Types

**GitHub Codespaces:**

- Execute commands directly in the Codespace terminal
- All packages are already installed

**SSH:**

- Connects to remote server via SSH
- Executes Python commands remotely
- Uses configured `REMOTE_PYTHON` path

**Docker:**

- Executes commands in Docker container
- Uses `docker-compose.cloud.yml` configuration

**Manual:**

- Displays instructions from `.cloud_sandbox/REPLIT_SETUP.md`

#### Configuration

Configuration is stored in `.cloud_sandbox/config.env`:

- `SANDBOX_TYPE` - Type of sandbox (github_codespaces, ssh, docker, manual)
- `SSH_HOST` - SSH server address (for SSH type)
- `REMOTE_PYTHON` - Python path on remote server (for SSH type)
- `REMOTE_WORKSPACE` - Workspace path on remote server (for SSH type)

---

### `launch_codespace.sh` - Auto-launch GitHub Codespace

Automatically creates and launches a GitHub Codespace in the free tier. Provides instant cloud development environment without manual setup.

#### Usage

```bash
./scripts/launch_codespace.sh
```

#### Required Tools & Setup

- GitHub CLI (`gh`) installed
- Repository pushed to GitHub
- GitHub CLI authenticated (`gh auth login`)

#### What This Script Does

1. ✅ Checks for GitHub CLI installation
2. ✅ Verifies authentication
3. ✅ Finds or creates a Codespace
4. ✅ Waits for Codespace to be ready
5. ✅ Opens in VS Code (if installed) or web browser
6. ✅ Uses free tier machine (2 cores, 4GB RAM)

#### Features

- Automatic Codespace creation
- Reuses existing Codespace if available
- Opens in preferred editor (VS Code or browser)
- Uses free tier resources (60 hours/month)
- All packages auto-installed from `requirements/requirements.txt`

#### Installation

**macOS:**

```bash
brew install gh
gh auth login
```

**Linux:**

```bash
# See https://cli.github.com/manual/installation
```

**Windows:**

```bash
winget install GitHub.cli
gh auth login
```

#### Troubleshooting

If the script fails:

- Ensure repository is pushed: `git push -u origin main`
- Verify authentication: `gh auth status`
- Check Codespace quota: `gh api user/codespaces`
- Manually create: Go to GitHub → Code → Codespaces → Create codespace

---

## Storage & Setup Scripts

### `setup-external-storage.sh` - Configure External Storage

Configures npm, pip, and other package managers to use an external USB drive for caches and packages, saving local disk space.

#### Usage

```bash
./scripts/setup-external-storage.sh
```

#### What It Configures

**NPM:**

- Cache directory: `$EXTERNAL_BASE/.npm-cache`
- Temporary directory: `$EXTERNAL_BASE/.npm-tmp`
- Global packages: `$EXTERNAL_BASE/.npm-global`

**Pip:**

- Cache directory: `$EXTERNAL_BASE/.pip-cache`
- Installs `config/pip.conf` to `~/.pip/pip.conf`

**Python Virtual Environments:**

- Sets `WORKON_HOME` to `$EXTERNAL_BASE/.python-venvs`

**Quarto:**

- Cache directory: `$EXTERNAL_BASE/.quarto-cache`

#### External Drive Path

Default path: `/Volumes/SEALED/DSHB/GALLERY`

To use a different path, edit the script or set `EXTERNAL_BASE` environment variable.

#### What It Creates

1. **Directories on external drive:**
   - `.npm-cache/`
   - `.npm-tmp/`
   - `.npm-global/`
   - `.pip-cache/`
   - `.python-venvs/`
   - `.node-modules/`
   - `.quarto-cache/`

2. **Configuration files:**
   - `.env` file in repository root (if it doesn't exist)
   - Shell profile additions (`~/.zshrc` or `~/.bashrc`)

3. **Environment variables:**
   - `NPM_CONFIG_CACHE`
   - `TMPDIR`
   - `PIP_CACHE_DIR`
   - `WORKON_HOME`

#### After Setup

```bash
# Apply configuration
source ~/.zshrc  # or ~/.bashrc

# Or restart your terminal

# Verify configuration
./scripts/verify-external-storage.sh
```

#### Prerequisites

- External USB drive mounted
- Write permissions on external drive
- npm, pip, and python3 installed (optional, script skips if not found)

---

### `verify-external-storage.sh` - Verify Storage Configuration

Checks that all package managers are correctly configured to use the external drive.

#### Usage

```bash
./scripts/verify-external-storage.sh
```

#### What It Checks

1. **External Drive Mount:**
   - Verifies drive is mounted at expected path

2. **NPM Configuration:**
   - Cache location
   - `.npmrc` file configuration

3. **Pip Configuration:**
   - Cache directory location
   - `pip.conf` file presence

4. **Python Virtual Environments:**
   - `WORKON_HOME` environment variable

5. **Environment Variables:**
   - `NPM_CONFIG_CACHE`
   - `PIP_CACHE_DIR`

6. **Directory Existence:**
   - Checks all required directories exist on external drive
   - Reports sizes for each directory

7. **Disk Space:**
   - Shows available space on external drive
   - Shows available space on local drive

#### Output

The script provides color-coded output:

- ✅ Green: Configuration correct
- ⚠️ Yellow: Warning or missing configuration
- ❌ Red: Error or incorrect configuration

#### Troubleshooting

If verification fails:

1. Ensure external drive is mounted
2. Run `./scripts/setup-external-storage.sh` again
3. Check that shell profile was updated
4. Restart terminal or source shell config

---

## Git & SSH Scripts

### `setup_git_ssh.sh` - Configure Git SSH Keys

Configures SSH keys for GitHub and switches your repository to use SSH protocol. Eliminates password prompts and works better with automation tools.

#### Usage

```bash
./scripts/setup_git_ssh.sh
```

#### Why SSH?

- ✅ No password prompts during git operations
- ✅ Better integration with GitHub CLI and Codespaces
- ✅ More secure for automated workflows
- ✅ Required for some advanced GitHub features

#### What SSH Setup Does

1. ✅ Checks for existing SSH keys
2. ✅ Generates new SSH key if needed (Ed25519)
3. ✅ Starts SSH agent and adds key
4. ✅ Copies public key to clipboard
5. ✅ Guides you to add key to GitHub
6. ✅ Tests SSH connection
7. ✅ Updates git remote from HTTPS to SSH (optional)

#### After Setup

Once configured:

- All `git push/pull` operations use SSH
- No password prompts required
- Works seamlessly with `gh` CLI commands
- Better integration with GitHub Codespaces

#### Interactive Steps

The script will:

1. Ask for your GitHub email (if not in git config)
2. Check for existing SSH keys
3. Generate new key if needed
4. Display public key and copy to clipboard
5. Wait for you to add key to GitHub
6. Test SSH connection
7. Ask if you want to switch remote from HTTPS to SSH

#### Adding Key to GitHub

1. Go to: <https://github.com/settings/keys>
2. Click 'New SSH key'
3. Paste your public key (already in clipboard if on macOS)
4. Click 'Add SSH key'

#### Current Status

Your repository currently uses HTTPS protocol. To switch to SSH, run:

```bash
./scripts/setup_git_ssh.sh
```

For detailed Git protocol recommendations, see `docs/GIT_PROTOCOL_GUIDE.md`.

---

## NPM Scripts

The `scripts/npm/` directory contains NPM-related scripts and utilities. See the [NPM Scripts Documentation](../../scripts/npm/README.md) for detailed information.

### Quick Overview

**`scripts/npm/integrations.js`** - API client utilities for external services:

- GitHub API
- Hugging Face API
- OpenAI API
- Anthropic API
- Serper API (Web Search)
- MongoDB Helper

**`scripts/npm/examples.js`** - Example usage of all API clients

**`scripts/npm/cleanup-disk-space.sh`** - Disk space cleanup script that cleans:

- NPM cache
- node_modules directories
- Build artifacts
- Temporary files
- Python cache
- Pip cache

### Usage Examples

```bash
# Test API connections
node scripts/npm/integrations.js

# Run examples
node scripts/npm/examples.js

# Clean disk space
./scripts/npm/cleanup-disk-space.sh
```

### Environment Variables

Set these in your `.env` file:

```env
GITHUB_TOKEN=your_github_token
HF_TOKEN=your_huggingface_token
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
SERPER_API_KEY=your_serper_key
MONGODB_URL=mongodb://localhost:27017
```

For complete documentation, see: [scripts/npm/README.md](../../scripts/npm/README.md)

---

## Common Workflows

### Rendering Website for GitHub Pages

```bash
# 1. Make changes to Quarto/Markdown files
# 2. Render all pages
./scripts/render_gh_pages.sh

# 3. Preview locally (optional)
./scripts/render_gh_pages.sh --preview

# 4. Commit and push
git add .
git commit -m "Update website"
git push origin gh-pages
```

### Setting Up Cloud Development

```bash
# 1. Configure cloud sandbox
./scripts/setup_cloud_sandbox.sh
# Select option 1 (GitHub Codespaces)

# 2. Launch Codespace
./scripts/launch_codespace.sh

# 3. Or use SSH/Docker sandbox
./scripts/use_cloud_sandbox.sh python projects/CrewAI/main.py
```

### Freeing Up Disk Space

```bash
# 1. Free RAM and clear caches
./scripts/free_ram.sh

# 2. Clean npm/node_modules (if needed)
./scripts/npm/cleanup-disk-space.sh

# 3. Verify external storage is being used
./scripts/verify-external-storage.sh
```

### Setting Up External Storage

```bash
# 1. Mount external USB drive
# 2. Configure package managers
./scripts/setup-external-storage.sh

# 3. Verify configuration
./scripts/verify-external-storage.sh

# 4. Restart terminal or source config
source ~/.zshrc
```

### Initial Repository Setup

```bash
# 1. Set up Git SSH
./scripts/setup_git_ssh.sh

# 2. Configure external storage (optional)
./scripts/setup-external-storage.sh

# 3. Prevent macOS resource forks
./scripts/prevent-resource-forks.sh

# 4. Render website
./scripts/render_gh_pages.sh
```

---

## Troubleshooting

### Quarto Rendering Issues

**Problem**: Quarto not found

```bash
# macOS
brew install quarto

# Linux/Windows
# See: https://quarto.org/docs/get-started/installation/
```

**Problem**: Python kernel timeout

```bash
# Run fix script
./scripts/fix_quarto_rendering.sh

# Or update _quarto.yml to use freeze: true
```

**Problem**: Build artifacts in wrong location

- The script automatically moves old artifacts to `_build/quarto/`
- Check `.gitignore` to ensure `_build/` is ignored

**Problem**: macOS resource fork files (`._*`) causing issues

```bash
# Archive existing files
./scripts/archive-macos-resource-forks.sh

# Prevent future creation
./scripts/prevent-resource-forks.sh
```

### Cloud Sandbox Issues

**Problem**: SSH connection fails

- Verify SSH host and credentials
- Test connection manually: `ssh user@host`
- Check `.cloud_sandbox/config.env` for correct settings

**Problem**: Docker container won't start

- Ensure Docker is installed and running
- Check `docker-compose.cloud.yml` configuration
- Verify Docker has sufficient resources

**Problem**: Codespace creation fails

- Verify repository is pushed to GitHub
- Check GitHub CLI authentication: `gh auth status`
- Verify Codespace quota: `gh api user/codespaces`

### Storage Configuration Issues

**Problem**: External drive not found

- Verify drive is mounted
- Check mount path in script (default: `/Volumes/SEALED/DSHB/GALLERY`)
- Update `EXTERNAL_BASE` in script if using different path

**Problem**: Package managers not using external drive

- Run verification: `./scripts/verify-external-storage.sh`
- Re-run setup: `./scripts/setup-external-storage.sh`
- Ensure shell profile was updated and sourced

### Git SSH Issues

**Problem**: SSH key not working

- Verify key was added to GitHub: <https://github.com/settings/keys>
- Test connection: `ssh -T git@github.com`
- Check SSH agent: `ssh-add -l`

**Problem**: Remote still using HTTPS

- Run setup script again: `./scripts/setup_git_ssh.sh`
- Or manually update: `git remote set-url origin git@github.com:USER/REPO.git`

### System Resource Issues

**Problem**: Out of disk space

```bash
# Free up RAM and caches
./scripts/free_ram.sh

# Clean npm/node_modules
./scripts/npm/cleanup-disk-space.sh

# Set up external storage
./scripts/setup-external-storage.sh
```

**Problem**: Script requires sudo but fails

- Some operations (page cache, swap) require sudo
- Script will skip these if sudo is not available
- Run with sudo if needed: `sudo ./scripts/free_ram.sh` (use with caution)

---

## Related Documentation

- [Setup Guides](../setup/) - Initial setup and configuration
- [Development Guides](../development/) - Development workflows
- [Git Protocol Guide](../development/GIT_PROTOCOL_GUIDE.md) - Git and GitHub setup
- [External Storage Setup](../setup/EXTERNAL_STORAGE_SETUP.md) - Detailed storage configuration
- [NPM Scripts Documentation](../../scripts/npm/README.md) - Complete NPM scripts guide
- [Main Repository README](../../README.md) - Repository overview

---

## Quick Reference

| Script | Purpose | Location |
|--------|---------|----------|
| `render_gh_pages.sh` | Render all GitHub Pages | `./scripts/render_gh_pages.sh` |
| `render_randomforest.sh` | Render Quarto document | `./scripts/render_randomforest.sh` |
| `rerender_gh_pages.sh` | Legacy re-render script | `./scripts/rerender_gh_pages.sh` |
| `fix_quarto_rendering.sh` | Fix rendering issues | `./scripts/fix_quarto_rendering.sh` |
| `free_ram.sh` | Free system resources | `./scripts/free_ram.sh` |
| `archive-macos-resource-forks.sh` | Archive resource forks | `./scripts/archive-macos-resource-forks.sh` |
| `cleanup-macos-resource-forks.sh` | Legacy cleanup wrapper | `./scripts/cleanup-macos-resource-forks.sh` |
| `prevent-resource-forks.sh` | Prevent resource forks | `./scripts/prevent-resource-forks.sh` |
| `setup_cloud_sandbox.sh` | Configure cloud environment | `./scripts/setup_cloud_sandbox.sh` |
| `use_cloud_sandbox.sh` | Use cloud sandbox | `./scripts/use_cloud_sandbox.sh` |
| `launch_codespace.sh` | Launch GitHub Codespace | `./scripts/launch_codespace.sh` |
| `setup-external-storage.sh` | Configure external storage | `./scripts/setup-external-storage.sh` |
| `verify-external-storage.sh` | Verify storage config | `./scripts/verify-external-storage.sh` |
| `setup_git_ssh.sh` | Configure Git SSH | `./scripts/setup_git_ssh.sh` |

---

*Last updated: 2024*
