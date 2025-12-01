#!/usr/bin/env bash

# Cloud Sandbox Setup Script
# Configures remote Python environments to avoid local disk usage

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_DIR="$REPO_ROOT/.cloud_sandbox"
CONFIG_FILE="$CONFIG_DIR/config.env"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Create config directory
mkdir -p "$CONFIG_DIR"

# Interactive setup
print_info "Cloud Sandbox Setup"
echo "This will configure a remote Python environment to avoid local disk usage."
echo ""

echo "Select your cloud sandbox option:"
echo "1) GitHub Codespaces (Recommended - Free tier available)"
echo "2) Remote SSH Server"
echo "3) Docker Remote Container"
echo "4) Replit/CodeSandbox (Manual setup)"
echo "5) View current configuration"
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        print_info "Setting up GitHub Codespaces configuration..."
        
        # Create .devcontainer configuration
        mkdir -p "$REPO_ROOT/.devcontainer"
        
        cat > "$REPO_ROOT/.devcontainer/devcontainer.json" << 'EOF'
{
  "name": "JJB Gallery Cloud Sandbox",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-toolsai.jupyter"
      ]
    }
  },
  "postCreateCommand": "pip install --upgrade pip && pip install -r requirements.txt",
  "remoteUser": "vscode",
  "mounts": [
    "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"
  ]
}
EOF
        
        # Create .codespaces directory with instructions
        mkdir -p "$REPO_ROOT/.codespaces"
        cat > "$REPO_ROOT/.codespaces/README.md" << 'EOF'
# GitHub Codespaces Setup

## Quick Start

1. Push this repository to GitHub
2. Go to your repository on GitHub
3. Click "Code" -> "Codespaces" -> "Create codespace on main"
4. Wait for the environment to build (includes all dependencies)
5. All packages are installed in the cloud - no local disk usage!

## Benefits

- ✅ Free tier: 60 hours/month for personal accounts
- ✅ Pre-installed packages (from requirements.txt)
- ✅ Full VS Code experience in browser
- ✅ Automatic environment setup
- ✅ No local disk space required

## Usage

Once the codespace is running:
```bash
cd projects/CrewAI
python main.py
```

## Cost

- Free tier: 60 hours/month for personal accounts
- After free tier: ~$0.18/hour for 2-core machine
EOF
        
        echo "GITHUB_CODESPACES=true" > "$CONFIG_FILE"
        echo "SANDBOX_TYPE=github_codespaces" >> "$CONFIG_FILE"
        
        print_success "GitHub Codespaces configuration created!"
        print_info "Next steps:"
        echo "  1. Push repository to GitHub"
        echo "  2. Auto-launch Codespace: ./scripts/launch_codespace.sh"
        echo "     OR manually create from GitHub web interface"
        echo "  3. All dependencies will install automatically in the cloud"
        ;;
        
    2)
        print_info "Setting up Remote SSH Server configuration..."
        
        read -p "Enter SSH host (e.g., user@example.com): " ssh_host
        ssh_host=${ssh_host:-}
        
        if [ -z "$ssh_host" ] || [[ "$ssh_host" == *"example.com"* ]] || [[ "$ssh_host" == *"your-server"* ]]; then
            print_error "Invalid SSH host. Please provide a real SSH host."
            exit 1
        fi
        
        read -p "Enter remote Python path (default: /usr/bin/python3): " remote_python
        remote_python=${remote_python:-/usr/bin/python3}
        
        # Validate Python path doesn't contain commands
        if [[ "$remote_python" == *"ssh"* ]] || [[ "$remote_python" == *"which"* ]]; then
            print_error "Python path should be a file path, not a command."
            print_info "If you need to find the Python path, run on the server: which python3"
            exit 1
        fi
        
        read -p "Enter remote workspace path: " remote_workspace
        remote_workspace=${remote_workspace:-}
        
        if [ -z "$remote_workspace" ] || [[ "$remote_workspace" == *"ssh"* ]] || [[ "$remote_workspace" == *"which"* ]]; then
            print_error "Remote workspace should be a directory path, not a command."
            exit 1
        fi
        
        # Write config with validation
        {
            echo "SSH_HOST=$ssh_host"
            echo "REMOTE_PYTHON=$remote_python"
            echo "REMOTE_WORKSPACE=$remote_workspace"
            echo "SANDBOX_TYPE=ssh"
        } > "$CONFIG_FILE"
        
        print_success "SSH configuration saved!"
        print_info "To use remote Python:"
        echo "  ./scripts/use_cloud_sandbox.sh"
        
        # Test SSH connection
        read -p "Test SSH connection now? [Y/n]: " test_ssh
        test_ssh=${test_ssh:-Y}
        if [[ "$test_ssh" =~ ^[Yy]$ ]]; then
            print_info "Testing SSH connection..."
            if ssh -o ConnectTimeout=5 "$ssh_host" "echo 'SSH connection successful'" 2>/dev/null; then
                print_success "SSH connection works!"
            else
                print_warning "Could not connect via SSH. Please verify your SSH host and credentials."
            fi
        fi
        
        print_success "SSH configuration saved!"
        print_info "To use remote Python:"
        echo "  ./scripts/use_cloud_sandbox.sh"
        ;;
        
    3)
        print_info "Setting up Docker Remote Container configuration..."
        
        read -p "Enter Docker host (leave empty for local): " docker_host
        docker_host=${docker_host:-localhost}
        
        echo "DOCKER_HOST=$docker_host" > "$CONFIG_FILE"
        echo "SANDBOX_TYPE=docker" >> "$CONFIG_FILE"
        
        # Create Dockerfile
        cat > "$REPO_ROOT/Dockerfile.cloud" << 'EOF'
FROM python:3.11-slim

WORKDIR /workspace

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

CMD ["/bin/bash"]
EOF
        
        cat > "$REPO_ROOT/docker-compose.cloud.yml" << 'EOF'
version: '3.8'

services:
  sandbox:
    build:
      context: .
      dockerfile: Dockerfile.cloud
    volumes:
      - .:/workspace
    working_dir: /workspace
    tty: true
    stdin_open: true
EOF
        
        print_success "Docker configuration created!"
        print_info "To start cloud sandbox:"
        echo "  docker-compose -f docker-compose.cloud.yml up -d"
        echo "  docker-compose -f docker-compose.cloud.yml exec sandbox bash"
        ;;
        
    4)
        print_info "Manual cloud setup instructions..."
        
        cat > "$CONFIG_DIR/REPLIT_SETUP.md" << 'EOF'
# Replit/CodeSandbox Setup

## Replit Setup

1. Go to https://replit.com
2. Create a new Python Repl
3. Upload your project files
4. Run: `pip install -r requirements.txt`
5. All packages stored in cloud

## CodeSandbox Setup

1. Go to https://codesandbox.io
2. Create new Python sandbox
3. Upload project files
4. Run: `pip install -r requirements.txt`
5. Packages installed in cloud environment

## Benefits

- ✅ Free tiers available
- ✅ Zero local disk usage
- ✅ Browser-based development
- ✅ Pre-configured environments
EOF
        
        echo "SANDBOX_TYPE=manual" > "$CONFIG_FILE"
        print_success "Manual setup guide created at .cloud_sandbox/REPLIT_SETUP.md"
        ;;
        
    5)
        if [ -f "$CONFIG_FILE" ]; then
            print_info "Current configuration:"
            cat "$CONFIG_FILE"
        else
            print_warning "No configuration found. Run setup first."
        fi
        ;;
        
    *)
        print_warning "Invalid choice"
        exit 1
        ;;
esac

print_success "Cloud sandbox setup complete!"

