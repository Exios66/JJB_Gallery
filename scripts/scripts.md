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

The free_ram.sh script frees up unnecessary RAM by clearing various caches and temporary files that accumulate during development. This script is particularly useful when working with large Jupyter notebooks, Python projects, or Quarto documents that generate cached files.

### What it clears

- **Python cache files**: `__pycache__` directories, `.pyc`, and `.pyo` files
- **Jupyter/IPython checkpoints**: `.ipynb_checkpoints` directories
- **Quarto cache**: Quarto freeze directories and user cache
- **pip cache**: Cached pip packages
- **Python bytecode**: Additional bytecode files

### Usage

```bash
./scripts/free_ram.sh
```

### Features

- Cross-platform support (macOS and Linux)
- Colored output for better readability
- Memory usage reporting before and after cleanup
- Safe cleanup (doesn't require sudo on macOS for basic operations)
- Summary of total space freed

### Notes

- On Linux, system page cache clearing requires sudo privileges
- The script will skip operations that require elevated privileges if not available
- All cleanup operations are safe and only remove cache/temporary files

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

### Usage

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

### Usage

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

### Usage

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

### Features

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
