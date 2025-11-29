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
