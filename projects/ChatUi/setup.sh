#!/bin/bash
# ChatUI Setup Script
# Sets up the ChatUI project with necessary dependencies and configuration

set -e

echo "🚀 Setting up ChatUI..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Create .env.local if it doesn't exist
if [ ! -f .env.local ]; then
    echo "📝 Creating .env.local template..."
    cat > .env.local << EOF
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017

# Hugging Face Token (optional, for remote models)
HF_TOKEN=

# Optional: Web Search API Keys
# SERPER_API_KEY=
# YDC_API_KEY=

# Optional: OpenAI API Key
# OPENAI_API_KEY=

# App Configuration
PUBLIC_APP_NAME=ChatUI
PUBLIC_APP_COLOR=blue
PUBLIC_APP_DESCRIPTION="Chat interface for open source models"
EOF
    echo "✅ Created .env.local template. Please update with your configuration."
else
    echo "✅ .env.local already exists."
fi

# Check if MongoDB is running (optional check)
if command -v docker &> /dev/null; then
    echo "💡 Tip: You can run MongoDB with Docker:"
    echo "   docker run -d -p 27017:27017 --name mongo-chatui mongo:latest"
fi

echo ""
echo "✅ ChatUI setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env.local with your configuration"
echo "2. Start MongoDB (if not already running)"
echo "3. Run 'npm run dev' to start the development server"
echo "4. Open http://localhost:5173 in your browser"

