# Cloud Sandbox Configuration

This directory contains configuration for remote Python environments to avoid local disk space usage.

## Quick Start

### Auto-launch Codespace (Fastest)

1. Install GitHub CLI: `brew install gh && gh auth login` (macOS)
2. Push repo to GitHub: `git push`
3. Auto-launch: `./scripts/setup_cloud_sandbox.sh`
   - Choose option 1 (GitHub Codespaces)
   - Then run: `./scripts/launch_codespace.sh`
4. Done! Codespace opens automatically with all packages installed.

### Manual Setup

Run the setup script:
```bash
./scripts/setup_cloud_sandbox.sh
```

## Available Options

### 1. GitHub Codespaces (Recommended)

**Best for**: Full development environment in the cloud

- ✅ Free tier: 60 hours/month for personal accounts
- ✅ Automatic package installation
- ✅ Full VS Code experience in browser
- ✅ Zero local disk usage
- ✅ Pre-configured with all dependencies

**Setup**:
1. Push repository to GitHub
2. Click "Code" → "Codespaces" → "Create codespace"
3. Wait for environment setup (packages install automatically)
4. Start coding!

### 2. Remote SSH Server

**Best for**: Using an existing remote server

**Requirements**:
- SSH access to a remote server
- Python 3.11+ installed on remote server

**Setup**:
```bash
./scripts/setup_cloud_sandbox.sh
# Choose option 2
# Enter SSH details
```

**Usage**:
```bash
./scripts/use_cloud_sandbox.sh python projects/Crewai/main.py
```

### 3. Docker Container

**Best for**: Local development without installing packages

**Requirements**:
- Docker installed locally
- ~500MB for Docker image (one-time)

**Setup**:
```bash
./scripts/setup_cloud_sandbox.sh
# Choose option 3
```

**Usage**:
```bash
docker-compose -f docker-compose.cloud.yml up -d
docker-compose -f docker-compose.cloud.yml exec sandbox bash
```

### 4. Replit/CodeSandbox

**Best for**: Quick browser-based development

**Instructions**: See `.cloud_sandbox/REPLIT_SETUP.md`

## Configuration Files

- `config.env` - Active cloud sandbox configuration
- `README.md` - This file

## Benefits

- 🚀 No local disk space for Python packages
- 🔄 Consistent environment across machines
- 📦 All dependencies pre-installed
- 🛠️ Easy to reset/recreate
- 💰 Cost-effective (many free tiers)

## Troubleshooting

### GitHub Codespaces
- Ensure repository is pushed to GitHub
- Check Codespace logs if packages fail to install
- Verify `requirements.txt` is correct

### SSH Remote
- Test SSH connection: `ssh user@host`
- Verify Python path on remote server
- Check remote workspace directory exists

### Docker
- Ensure Docker is running: `docker ps`
- Rebuild container: `docker-compose -f docker-compose.cloud.yml build --no-cache`

## Migration Guide

To switch from local to cloud sandbox:

1. Backup your work (git commit)
2. Run `./scripts/setup_cloud_sandbox.sh`
3. Select your preferred option
4. Use `./scripts/use_cloud_sandbox.sh` to execute Python commands

Your local code remains unchanged - only the Python execution environment changes!

