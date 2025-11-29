#!/usr/bin/env bash

# Use Cloud Sandbox Script
# Executes Python commands in remote/cloud environment

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$REPO_ROOT/.cloud_sandbox/config.env"

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

# Load configuration
if [ ! -f "$CONFIG_FILE" ]; then
    print_error "Cloud sandbox not configured. Run: ./scripts/setup_cloud_sandbox.sh"
    exit 1
fi

# Validate config file before sourcing
if grep -q "your-server.com\|example.com\|user@" "$CONFIG_FILE"; then
    print_error "Invalid configuration detected in .cloud_sandbox/config.env"
    print_error "The config file contains placeholder values."
    print_info "Please reconfigure: ./scripts/setup_cloud_sandbox.sh"
    print_info "Or remove the config file to start fresh: rm .cloud_sandbox/config.env"
    exit 1
fi

# Source config file safely
source "$CONFIG_FILE" 2>/dev/null || {
    print_error "Error loading configuration file"
    print_info "Please reconfigure: ./scripts/setup_cloud_sandbox.sh"
    exit 1
}

case "${SANDBOX_TYPE:-}" in
    github_codespaces)
        print_info "GitHub Codespaces detected"
        print_info "Execute commands directly in the Codespace terminal"
        print_info "All packages are already installed in the cloud environment"
        ;;
        
    ssh)
        if [ -z "${SSH_HOST:-}" ] || [ -z "${REMOTE_PYTHON:-}" ]; then
            print_error "SSH configuration incomplete. Check .cloud_sandbox/config.env"
            exit 1
        fi
        
        print_info "Connecting to remote server: $SSH_HOST"
        print_info "Using remote Python: $REMOTE_PYTHON"
        
        if [ $# -eq 0 ]; then
            print_info "Starting interactive SSH session..."
            ssh -t "$SSH_HOST" "cd ${REMOTE_WORKSPACE:-~} && $REMOTE_PYTHON"
        else
            print_info "Executing command remotely: $*"
            ssh "$SSH_HOST" "cd ${REMOTE_WORKSPACE:-~} && $REMOTE_PYTHON $*"
        fi
        ;;
        
    docker)
        print_info "Using Docker container..."
        
        if ! command -v docker &> /dev/null; then
            print_error "Docker not found. Please install Docker first."
            exit 1
        fi
        
        if [ $# -eq 0 ]; then
            print_info "Starting Docker container shell..."
            docker-compose -f "$REPO_ROOT/docker-compose.cloud.yml" exec sandbox bash
        else
            print_info "Executing command in Docker: $*"
            docker-compose -f "$REPO_ROOT/docker-compose.cloud.yml" exec sandbox python "$@"
        fi
        ;;
        
    manual)
        print_info "Manual cloud sandbox configuration"
        print_info "Please follow instructions in .cloud_sandbox/REPLIT_SETUP.md"
        ;;
        
    *)
        print_error "Unknown sandbox type: ${SANDBOX_TYPE:-none}"
        exit 1
        ;;
esac

