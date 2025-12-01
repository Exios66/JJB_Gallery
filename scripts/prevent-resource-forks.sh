#!/bin/bash
# Prevent macOS Resource Fork File Creation
# Configures environment to prevent ._* files from being created
# This is a one-time setup script

set -e

ZSHRC="$HOME/.zshrc"
ENV_VAR="COPYFILE_DISABLE=1"

echo "🔧 Configuring macOS to prevent resource fork file creation..."
echo ""

# Check if already configured
if grep -q "COPYFILE_DISABLE" "$ZSHRC" 2>/dev/null; then
    echo "✅ COPYFILE_DISABLE is already configured in $ZSHRC"
    echo ""
    echo "Current configuration:"
    grep "COPYFILE_DISABLE" "$ZSHRC" | head -3
    echo ""
    echo "💡 To apply changes, run: source $ZSHRC"
    exit 0
fi

# Add configuration
echo "Adding COPYFILE_DISABLE=1 to $ZSHRC..."
echo "" >> "$ZSHRC"
echo "# Prevent macOS resource fork files (._*)" >> "$ZSHRC"
echo "export COPYFILE_DISABLE=1" >> "$ZSHRC"

echo "✅ Configuration added to $ZSHRC"
echo ""
echo "📝 To apply immediately, run:"
echo "   source $ZSHRC"
echo ""
echo "Or restart your terminal."
echo ""
echo "💡 This prevents macOS from creating ._* files when copying/moving files."
echo "   Note: This only affects new operations. Existing ._* files won't be removed."
echo "   Use scripts/cleanup-macos-resource-forks.sh to remove existing files."
