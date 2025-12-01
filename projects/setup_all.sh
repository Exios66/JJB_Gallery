#!/bin/bash
# Setup script for all projects
# Installs dependencies and sets up environment for each project

set -e

echo "=========================================="
echo "Setting up all projects"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to setup a project
setup_project() {
    local project_name=$1
    local project_path=$2
    
    echo -e "${BLUE}Setting up ${project_name}...${NC}"
    cd "$project_path"
    
    if [ -f "requirements.txt" ]; then
        echo "  Installing Python dependencies..."
        pip install -r requirements.txt
    fi
    
    if [ -f "package.json" ]; then
        echo "  Installing Node.js dependencies..."
        npm install
    fi
    
    echo -e "${GREEN}✓ ${project_name} setup complete${NC}"
    echo ""
    cd - > /dev/null
}

# Setup each project
echo -e "${YELLOW}1. RAG_Model${NC}"
setup_project "RAG_Model" "RAG_Model"

echo -e "${YELLOW}2. Psychometrics${NC}"
setup_project "Psychometrics" "Psychometrics"

echo -e "${YELLOW}3. ChatUi${NC}"
setup_project "ChatUi" "ChatUi"

echo -e "${YELLOW}4. ios_chatbot${NC}"
setup_project "ios_chatbot" "ios_chatbot"

echo -e "${YELLOW}5. litellm${NC}"
setup_project "litellm" "litellm"

echo -e "${YELLOW}6. CrewAI${NC}"
if [ -f "Crewai/requirements.txt" ]; then
    setup_project "CrewAI" "Crewai"
else
    echo "  No requirements.txt found, skipping..."
fi

echo ""
echo -e "${GREEN}=========================================="
echo "All projects setup complete!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Copy .env.example files to .env in each project"
echo "2. Set your API keys in the .env files"
echo "3. Test each project individually"
echo ""

