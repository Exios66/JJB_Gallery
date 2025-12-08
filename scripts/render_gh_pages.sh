#!/usr/bin/env bash

################################################################################
# Render All GitHub Pages
#
# This script renders all Quarto pages defined in _quarto.yml for GitHub Pages.
# It handles:
# - Cleaning old build artifacts
# - Setting up Python environment
# - Rendering all website pages
# - Organizing output files
#
# Usage:
#   ./scripts/render_gh_pages.sh [--clean] [--preview]
#
# Options:
#   --clean    Clean all build artifacts before rendering (default: true)
#   --preview  Start preview server after rendering (default: false)
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
QUARTO_CONFIG="$REPO_ROOT/_quarto.yml"
BUILD_DIR="$REPO_ROOT/_build/quarto"

# Parse command line arguments
CLEAN_BUILD=true
START_PREVIEW=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN_BUILD=true
            shift
            ;;
        --no-clean)
            CLEAN_BUILD=false
            shift
            ;;
        --preview)
            START_PREVIEW=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}" >&2
            echo "Usage: $0 [--clean|--no-clean] [--preview]"
            exit 1
            ;;
    esac
done

################################################################################
# Helper Functions
################################################################################

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

check_quarto() {
    if ! command -v quarto &> /dev/null; then
        log_error "Quarto CLI is not installed or not in PATH."
        echo ""
        echo "Please install Quarto: https://quarto.org/docs/get-started/"
        echo ""
        echo "On macOS:"
        echo "  brew install quarto"
        echo ""
        echo "On Linux:"
        echo "  See: https://quarto.org/docs/get-started/installation/"
        exit 1
    fi
    
    QUARTO_VERSION=$(quarto --version 2>/dev/null || echo "unknown")
    log_info "Quarto version: $QUARTO_VERSION"
}

setup_python_env() {
    if [[ -d "$REPO_ROOT/.venv" ]]; then
        log_info "Activating virtual environment (.venv)..."
        # shellcheck disable=SC1091
        source "$REPO_ROOT/.venv/bin/activate"
        export QUARTO_PYTHON="$REPO_ROOT/.venv/bin/python"
        log_success "Python environment activated"
    elif [[ -d "$REPO_ROOT/venv" ]]; then
        log_info "Activating virtual environment (venv)..."
        # shellcheck disable=SC1091
        source "$REPO_ROOT/venv/bin/activate"
        export QUARTO_PYTHON="$REPO_ROOT/venv/bin/python"
        log_success "Python environment activated"
    else
        log_warning "No virtual environment found. Using system Python."
        if command -v python3 &> /dev/null; then
            export QUARTO_PYTHON=$(which python3)
        fi
    fi
}

clean_build_artifacts() {
    if [[ "$CLEAN_BUILD" == "true" ]]; then
        log_info "Cleaning build artifacts..."
        
        # Remove build directory
        if [[ -d "$BUILD_DIR" ]]; then
            rm -rf "$BUILD_DIR"
            log_success "Removed $BUILD_DIR"
        fi
        
        # Remove Quarto cache directories
        local cache_dirs=(
            "$REPO_ROOT/.quarto"
            "$REPO_ROOT/Quarto/_freeze"
            "$REPO_ROOT/Quarto/.quarto"
        )
        
        for dir in "${cache_dirs[@]}"; do
            if [[ -d "$dir" ]]; then
                rm -rf "$dir"
                log_success "Removed $dir"
            fi
        done
        
        # Remove old artifact directories (if they exist in root)
        # These are legacy artifacts from previous builds and should be in _build/quarto/
        local old_dirs=(
            "$REPO_ROOT/site_libs"
            "$REPO_ROOT/index_files"
            "$REPO_ROOT/randomforest_files"
        )
        
        for dir in "${old_dirs[@]}"; do
            if [[ -d "$dir" ]]; then
                rm -rf "$dir"
                log_info "Cleaned up legacy artifact: $(basename "$dir") (artifacts should be in _build/quarto/)"
            fi
        done
        
        log_success "Build artifacts cleaned"
    else
        log_info "Skipping clean (use --clean to force cleanup)"
    fi
}

render_quarto_site() {
    log_info "Rendering Quarto website..."
    log_info "Configuration: $QUARTO_CONFIG"
    
    cd "$REPO_ROOT"
    
    # Check if _quarto.yml exists
    if [[ ! -f "$QUARTO_CONFIG" ]]; then
        log_error "Quarto configuration not found: $QUARTO_CONFIG"
        exit 1
    fi
    
    # Render the website (this renders all pages in _quarto.yml)
    # Note: Quarto may exit with error code during post-processing (sitemap generation)
    # but the HTML files are still generated successfully
    if quarto render --to html 2>&1 | tee /tmp/quarto_render.log; then
        log_success "Quarto website rendered successfully"
    else
        # Check if files were actually generated despite the error
        local error_occurred=false
        if grep -q "Source and destination cannot be the same" /tmp/quarto_render.log 2>/dev/null; then
            log_warning "Sitemap generation error detected (known issue, files were still generated)"
            error_occurred=true
        fi
        
        # Verify that key files were generated
        if [[ -f "$REPO_ROOT/index.html" ]] && [[ -f "$REPO_ROOT/CHANGELOG.html" ]]; then
            if [[ "$error_occurred" == "true" ]]; then
                log_success "HTML files generated successfully (sitemap error is non-critical)"
            else
                log_error "Quarto rendering failed"
                exit 1
            fi
        else
            log_error "Quarto rendering failed and files were not generated"
            exit 1
        fi
    fi
}

verify_outputs() {
    log_info "Verifying rendered outputs..."
    
    local expected_files=(
        "index.html"
        "CHANGELOG.html"
        "SECURITY.html"
        "projects/CrewAI/README.html"
        "projects/terminal_agents/README.html"
        "projects/RAG_Model/README.html"
        "projects/Psychometrics/README.html"
        "projects/ChatUi/README.html"
        "projects/ios_chatbot/README.html"
        "projects/litellm/README.html"
        "Quarto/randomforest.html"
    )
    
    local missing_files=()
    
    for file in "${expected_files[@]}"; do
        local full_path="$REPO_ROOT/$file"
        if [[ -f "$full_path" ]]; then
            log_success "Found: $file"
        else
            missing_files+=("$file")
            log_warning "Missing: $file"
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        log_warning "Some expected files are missing:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
    else
        log_success "All expected output files found"
    fi
    
    # Verify embed-resources configuration
    if grep -q "embed-resources: true" "$QUARTO_CONFIG" 2>/dev/null; then
        log_info "embed-resources: true is enabled - resources should be embedded in HTML"
        log_info "Checking if HTML files are self-contained..."
        
        local html_files=("index.html" "CHANGELOG.html" "SECURITY.html")
        local embedded_count=0
        
        for html_file in "${html_files[@]}"; do
            local full_path="$REPO_ROOT/$html_file"
            if [[ -f "$full_path" ]]; then
                # Check if file contains embedded styles/scripts (indicator of embed-resources)
                if grep -q "<style>" "$full_path" 2>/dev/null || grep -q "<script>" "$full_path" 2>/dev/null; then
                    embedded_count=$((embedded_count + 1))
                fi
            fi
        done
        
        if [[ $embedded_count -gt 0 ]]; then
            log_success "Resources appear to be embedded in HTML files"
        else
            log_warning "Resources may not be embedded - verify embed-resources: true is working"
        fi
    else
        log_info "embed-resources: false - checking for site_libs directory"
        if [[ -d "$REPO_ROOT/site_libs" ]]; then
            log_success "site_libs directory found"
            local lib_count=$(find "$REPO_ROOT/site_libs" -type f ! -name "._*" | wc -l | tr -d ' ')
            log_info "Found $lib_count files in site_libs"
        else
            log_warning "site_libs directory not found"
        fi
    fi
    
    # Check for build directory
    if [[ -d "$BUILD_DIR" ]]; then
        log_success "Build artifacts in: $BUILD_DIR"
    else
        log_info "Build directory not found (expected if embed-resources: true)"
    fi
    
    # Verify additional files
    local additional_files=("404.html" "robots.txt" "favicon.svg")
    for file in "${additional_files[@]}"; do
        local full_path="$REPO_ROOT/$file"
        if [[ -f "$full_path" ]]; then
            log_success "Found: $file"
        else
            log_warning "Missing: $file"
        fi
    done
}

start_preview() {
    if [[ "$START_PREVIEW" == "true" ]]; then
        log_info "Starting Quarto preview server..."
        log_info "Preview will be available at: http://localhost:4200"
        log_info "Press Ctrl+C to stop the preview server"
        echo ""
        
        cd "$REPO_ROOT"
        quarto preview --no-browser --port 4200
    fi
}

print_summary() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_success "GitHub Pages rendering complete!"
    echo ""
    echo "Rendered pages:"
    echo "  • index.html (Home)"
    echo "  • CHANGELOG.html"
    echo "  • SECURITY.html"
    echo "  • projects/CrewAI/README.html"
    echo "  • projects/terminal_agents/README.html"
    echo "  • Quarto/randomforest.html"
    echo ""
    echo "Build artifacts: $BUILD_DIR"
    echo ""
    echo "Next steps:"
    echo "  1. Review the rendered HTML files"
    echo "  2. Commit and push to gh-pages branch for deployment"
    echo "  3. Or run with --preview to start a local preview server"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

################################################################################
# Main Execution
################################################################################

main() {
    echo ""
    log_info "Starting GitHub Pages rendering process..."
    echo ""
    
    # Pre-flight checks
    check_quarto
    setup_python_env
    
    # Build process
    clean_build_artifacts
    render_quarto_site
    verify_outputs
    
    # Summary
    print_summary
    
    # Optional preview
    if [[ "$START_PREVIEW" == "true" ]]; then
        start_preview
    fi
}

# Run main function
main "$@"
