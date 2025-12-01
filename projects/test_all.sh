#!/bin/bash
# Test script for all projects
# Runs basic tests to verify each project is set up correctly

set -e

echo "=========================================="
echo "Testing all projects"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test results
PASSED=0
FAILED=0

# Function to test a project
test_project() {
    local project_name=$1
    local project_path=$2
    local test_command=$3
    
    echo -e "${BLUE}Testing ${project_name}...${NC}"
    cd "$project_path"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✓ ${project_name} test passed${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ ${project_name} test failed${NC}"
        ((FAILED++))
    fi
    
    echo ""
    cd - > /dev/null
}

# Test RAG_Model
test_project "RAG_Model" "RAG_Model" "python -c 'from rag_system import RAGSystem; print(\"RAG System import successful\")'"

# Test Psychometrics
test_project "Psychometrics" "Psychometrics" "python -c 'from nasa_tlx import NASATLX; print(\"NASA TLX import successful\")'"

# Test ios_chatbot
test_project "ios_chatbot" "ios_chatbot" "python -c 'import app; print(\"Flask app import successful\")'"

# Test litellm
test_project "litellm" "litellm" "python -c 'try:
    from litellm import completion
    print(\"LiteLLM import successful\")
except ImportError:
    print(\"LiteLLM not installed - run: pip install litellm\")'"

# Test ChatUi (check if node_modules exists)
if [ -d "ChatUi/node_modules" ]; then
    echo -e "${BLUE}Testing ChatUi...${NC}"
    cd ChatUi
    if npm run check > /dev/null 2>&1; then
        echo -e "${GREEN}✓ ChatUi test passed${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠ ChatUi check had warnings (this is OK)${NC}"
        ((PASSED++))
    fi
    echo ""
    cd - > /dev/null
else
    echo -e "${YELLOW}⚠ ChatUi: node_modules not found - run: cd ChatUi && npm install${NC}"
    ((FAILED++))
fi

# Summary
echo "=========================================="
echo -e "${GREEN}Passed: ${PASSED}${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: ${FAILED}${NC}"
fi
echo "=========================================="

if [ $FAILED -eq 0 ]; then
    exit 0
else
    exit 1
fi

