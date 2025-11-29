# SCRIPTS

## 1. render_randomforest.sh

Run the render_randomforest.sh script to render the randomforest.qmd file to a html and pdf file. This script will also start a preview server on the default port 4343.

Run the script:

```bash
./scripts/render_randomforest.sh
```

Open the preview server in your browser:

```bash
open http://localhost:4343
```

## 2. free_ram.sh

The free_ram.sh script is an **enhanced** tool that frees up unnecessary RAM, disk space, and compute resources by clearing extensive caches, temporary files, and idle processes. This script is particularly useful when working with large Jupyter notebooks, Python projects, or when your system is running low on resources.

### What it clears

#### Python & Development Tools
- **Python cache files**: `__pycache__` directories, `.pyc`, `.pyo`, and `.py[cod]` files
- **Jupyter/IPython checkpoints**: `.ipynb_checkpoints` directories
- **Quarto cache**: Quarto freeze directories and user cache
- **pip cache**: Cached pip packages
- **Conda cache**: Conda package cache
- **Poetry cache**: Poetry package cache
- **pipx cache**: pipx package cache
- **Virtual environment caches**: Cache files in `.venv`, `venv`, and `env` directories

#### Package Manager Caches
- **npm cache**: Node.js package manager cache
- **yarn cache**: Yarn package manager cache
- **Homebrew cache** (macOS): Homebrew package cache
- **Cargo cache** (Rust): Rust package manager cache
- **Go module cache**: Go language module cache

#### System & Application Caches
- **Docker cache**: Docker images, containers, and volumes (unused)
- **Browser caches**: Chrome, Firefox, Safari caches (macOS)
- **IDE caches**: VS Code, PyCharm, IntelliJ IDEA caches
- **System temporary files**: Old temp files (7+ days)
- **System logs**: Old log files (30+ days)
- **Font cache** (macOS): System font cache
- **DNS cache**: System DNS resolver cache

#### System Resources (Optional)
- **System page cache** (Linux): Kernel page cache (requires sudo)
- **Swap files**: Clear and reset swap (Linux, requires sudo)
- **Idle processes**: Kill high CPU/low priority processes (optional, dangerous)

### Usage

```bash
# Standard cleanup (safe, recommended)
./scripts/free_ram.sh

# Aggressive cleanup including idle processes (use with caution)
KILL_IDLE_PROCESSES=yes ./scripts/free_ram.sh
```

### Features

- **Comprehensive cleanup**: Clears 20+ different cache types
- **Cross-platform support**: Works on macOS and Linux
- **Colored output**: Easy-to-read status messages
- **Memory reporting**: Shows before/after memory status
- **Safe by default**: Only clears caches, not user data
- **Smart cleanup**: Only removes old temporary files (7+ days)
- **Space tracking**: Reports total space freed
- **Permission-aware**: Skips operations requiring sudo if not available
- **Process management**: Optional idle process termination

### Advanced Options

#### Kill Idle Processes

To terminate idle or high-CPU processes (use with extreme caution):

```bash
KILL_IDLE_PROCESSES=yes ./scripts/free_ram.sh
```

**Warning**: This may close applications that appear idle but are actually working.

### Notes

- **System-level operations** (page cache, swap, DNS) require sudo privileges
- The script will **skip** operations that require elevated privileges if not available
- **All cleanup operations are safe** and only remove cache/temporary files
- **User data is never deleted** - only caches and temporary files
- Old files are preserved (only files 7+ days old are removed from temp directories)
- Browser caches will be cleared - you may need to re-login to some websites
- IDE caches will be cleared - first launch after cleanup may be slower

### What Gets Preserved

- Your source code and project files
- Git history and repository data
- Installed packages (only caches are cleared)
- User preferences and settings
- Active application data

## 7. Rerender for GitHub Pages (rerender_gh_pages.sh)

The rerender_gh_pages.sh script is designed to properly purge old artifacts and re-render the Quarto document for deployment to GitHub Pages. It ensures that the `index.html` in the root directory is correctly generated and that all resource files are in place.

### Usage

```bash
./scripts/rerender_gh_pages.sh
```

### What it does

1. ✅ Cleans up old `index.html` and Quarto cache/freeze directories.
2. ✅ Activates the virtual environment (if available) to ensure correct dependencies.
3. ✅ Renders the `Quarto/randomforest.qmd` file to HTML.
4. ✅ Moves the output HTML to `index.html` in the repository root.
5. ✅ Moves/updates the support files directory (`randomforest_files`) to the repository root.

### When to use

Run this script whenever you make changes to the Quarto document (`Quarto/randomforest.qmd`) and want to update the public-facing page on GitHub Pages.

## Virtual Environment Management

Activate the Python virtual environment:

```bash
source .venv/bin/activate
```

Deactivate the Python virtual environment:

```bash
deactivate
```

## Manual System Cache Clearing (Linux)

Clear cached memory to help preserve system memory and RAM (requires sudo privileges):

```bash
sudo sync; sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

Note: This functionality is included in the `free_ram.sh` script on Linux systems when run with appropriate privileges.

## 3. Cloud Sandbox Setup (setup_cloud_sandbox.sh)

The setup_cloud_sandbox.sh script configures remote Python environments to avoid local disk space usage. This is particularly useful when you have limited disk space but need to work with large Python packages like CrewAI.

### Cloud Sandbox Setup Usage

```bash
./scripts/setup_cloud_sandbox.sh
```

### Available Options

1. **GitHub Codespaces** (Recommended)
   - Free tier: 60 hours/month
   - Automatic package installation
   - Full VS Code in browser
   - Zero local disk usage

2. **Remote SSH Server**
   - Use existing remote server
   - Execute Python remotely

3. **Docker Container**
   - Local containerized environment
   - Minimal local disk usage

4. **Replit/CodeSandbox**
   - Browser-based development
   - Free tiers available

### Benefits

- No local disk space for Python packages
- Consistent environment
- Easy to reset/recreate
- Cost-effective (many free options)

## 4. Use Cloud Sandbox (use_cloud_sandbox.sh)

After setting up a cloud sandbox, use this script to execute Python commands in the remote environment.

### Use Cloud Sandbox Usage

```bash
# Execute a Python script remotely
./scripts/use_cloud_sandbox.sh python projects/Crewai/main.py

# Start interactive session (SSH/Docker)
./scripts/use_cloud_sandbox.sh
```

### Prerequisites

- Cloud sandbox must be configured (run `setup_cloud_sandbox.sh` first)
- For SSH: valid SSH connection
- For Docker: Docker installed and running
- For Codespaces: Codespace already created

For detailed instructions, see `.cloud_sandbox/README.md`.

## 6. Git SSH Setup (setup_git_ssh.sh)

The setup_git_ssh.sh script configures SSH keys for GitHub and switches your repository to use SSH protocol. This eliminates password prompts and works better with automation tools.

### Why SSH?

- ✅ No password prompts during git operations
- ✅ Better integration with GitHub CLI and Codespaces
- ✅ More secure for automated workflows
- ✅ Required for some advanced GitHub features

### Git SSH Setup Usage

```bash
./scripts/setup_git_ssh.sh
```

### What it does

1. ✅ Checks for existing SSH keys
2. ✅ Generates new SSH key if needed (Ed25519)
3. ✅ Starts SSH agent and adds key
4. ✅ Copies public key to clipboard
5. ✅ Guides you to add key to GitHub
6. ✅ Tests SSH connection
7. ✅ Updates git remote from HTTPS to SSH (optional)

### After Setup

Once configured:

- All `git push/pull` operations use SSH
- No password prompts required
- Works seamlessly with `gh` CLI commands
- Better integration with GitHub Codespaces

### Current Status

Your repository currently uses HTTPS protocol. To switch to SSH, run:

```bash
./scripts/setup_git_ssh.sh
```

For detailed Git protocol recommendations, see `docs/GIT_PROTOCOL_GUIDE.md`.

## 5. Auto-launch Codespace (launch_codespace.sh)

The launch_codespace.sh script automatically creates and launches a GitHub Codespace in the free tier. This provides instant cloud development environment without manual setup.

### Required Tools & Setup

- GitHub CLI (`gh`) installed
- Repository pushed to GitHub
- GitHub CLI authenticated (`gh auth login`)

### How to Use

```bash
./scripts/launch_codespace.sh
```

### What this script does

1. ✅ Checks for GitHub CLI installation
2. ✅ Verifies authentication
3. ✅ Finds or creates a Codespace
4. ✅ Waits for Codespace to be ready
5. ✅ Opens in VS Code (if installed) or web browser
6. ✅ Uses free tier machine (2 cores, 4GB RAM)

### Launch Codespace Features

- Automatic Codespace creation
- Reuses existing Codespace if available
- Opens in preferred editor (VS Code or browser)
- Uses free tier resources (60 hours/month)
- All packages auto-installed from requirements.txt

### Installation

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

### Troubleshooting

If the script fails:

- Ensure repository is pushed: `git push -u origin main`
- Verify authentication: `gh auth status`
- Check Codespace quota: `gh api user/codespaces`
- Manually create: Go to GitHub → Code → Codespaces → Create codespace
