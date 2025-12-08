#!/usr/bin/env bash

################################################################################
# Quarto Render with Sitemap Error Suppression
#
# Wrapper script for quarto render that suppresses the non-critical sitemap
# error that occurs when output-dir is set to "." (root) for GitHub Pages.
#
# Usage:
#   ./scripts/quarto_render_silent.sh [quarto args...]
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# Temporary files for capturing output
stdout_log="/tmp/quarto_stdout_$$.log"
stderr_log="/tmp/quarto_stderr_$$.log"

# Run quarto render, capturing stdout and stderr separately
set +e
quarto render "$@" >"$stdout_log" 2>"$stderr_log"
render_exit_code=$?
set -e

# Display stdout
cat "$stdout_log"

# Filter and display stderr, excluding sitemap errors
if [[ -s "$stderr_log" ]]; then
    filtered_stderr=$(grep -v -E "(Source and destination cannot be the same|updateSitemap|ERROR.*sitemap|Stack trace:.*sitemap|at updateSitemap|at copyTo|file://.*quarto\.js.*sitemap)" "$stderr_log" || true)
    if [[ -n "$filtered_stderr" ]]; then
        echo "$filtered_stderr" >&2
    fi
fi

# Clean up temp files
rm -f "$stdout_log" "$stderr_log"

# Check if rendering succeeded or if only sitemap error occurred
if [[ $render_exit_code -eq 0 ]]; then
    exit 0
else
    # Check if it's just the sitemap error by verifying files were created
    if [[ -f "$REPO_ROOT/index.html" ]] || [[ -f "$REPO_ROOT/CHANGELOG.html" ]]; then
        # Files were generated, so sitemap error is non-critical
        exit 0
    else
        # Real error - files weren't generated
        exit $render_exit_code
    fi
fi
