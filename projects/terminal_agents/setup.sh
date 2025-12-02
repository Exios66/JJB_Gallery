#!/bin/bash
# Setup script for Terminal Agents

set -e

echo "🚀 Setting up Terminal Agents..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Make agent.py executable
chmod +x agent.py

# Create config directory
mkdir -p ~/.terminal_agents

# Create example config file if it doesn't exist
if [ ! -f ~/.terminal_agents/config.yaml ]; then
    echo "📝 Creating example config file..."
    cat > ~/.terminal_agents/config.yaml << 'EOF'
# Terminal Agents Configuration
# Uncomment and configure the providers you want to use

# Provider selection (auto-detect if not set)
# provider: ollama  # Options: ollama, openai, anthropic, google, azure

# Ollama (Free, Local)
ollama_base_url: http://localhost:11434
ollama_model: llama3.1:8b

# OpenAI
# openai_api_key: your_key_here
# openai_model: gpt-4o-mini

# Anthropic
# anthropic_api_key: your_key_here
# anthropic_model: claude-3-5-sonnet-20241022

# Google
# google_api_key: your_key_here
# google_model: gemini-pro

# Azure OpenAI
# azure_openai_api_key: your_key_here
# azure_openai_endpoint: https://your-endpoint.openai.azure.com
# azure_openai_deployment: your-deployment-name
EOF
    echo "✓ Config file created at ~/.terminal_agents/config.yaml"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your API keys in ~/.terminal_agents/config.yaml"
echo "   Or set environment variables:"
echo "   export OPENAI_API_KEY=your_key"
echo "   export ANTHROPIC_API_KEY=your_key"
echo ""
echo "2. For free local models, install Ollama:"
echo "   curl -fsSL https://ollama.ai/install.sh | sh"
echo "   ollama pull llama3.1:8b"
echo ""
echo "3. Run the agent:"
echo "   source venv/bin/activate"
echo "   python agent.py interactive"
echo "   # or"
echo "   ./agent.py interactive"
echo ""

