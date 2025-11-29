#!/usr/bin/env python3
"""
CrewAI Swarm Test Runner.
Executes verification tests for specific swarms or the entire system.
"""

import sys
import argparse
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from llm_config import configure_crewai_environment

def setup_environment():
    """Ensure environment is configured for testing."""
    print("🔧 Configuring test environment...")
    configure_crewai_environment()
    # Disable verbose mode for cleaner test output unless requested
    config.VERBOSE = False

def test_tool_imports():
    """Verify all tools can be imported."""
    print("\n📦 Verifying Tool Imports...")
    try:
        from tools import (
            DatasetAnalyzerTool, ModelEvaluatorTool,
            DataGatheringTool, CitationManagerTool,
            MarketAnalyzerTool, FinancialModelingTool,
            CodeExecutorTool, FileManagerTool,
            DocumentStructureTool, MarkdownFormatterTool,
            SEOAnalyzerTool, ContentAnalyzerTool,
            PaperAnalyzerTool, CitationNetworkTool
        )
        print("✅ All tool modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Tool import failed: {e}")
        return False

def test_crew_instantiation(crew_name):
    """Test if a specific crew can be instantiated with its tools."""
    print(f"\n🤖 Testing instantiation of {crew_name}...")
    try:
        from main import get_crew_class
        crew_class = get_crew_class(crew_name)
        crew_instance = crew_class()
        
        # Check agents
        print(f"   - Agents created: {len(crew_instance.agents)}")
        
        # Check tools for first agent
        first_agent = list(crew_instance.agents.values())[0]
        tools_count = len(first_agent.tools) if hasattr(first_agent, 'tools') and first_agent.tools else 0
        print(f"   - First agent tools: {tools_count}")
        
        if tools_count == 0:
             print("   ⚠️  Warning: First agent has no tools (check LLM config or optional tools)")
        
        print(f"✅ {crew_name} verified")
        return True
    except Exception as e:
        print(f"❌ {crew_name} failed: {e}")
        # Print more detail if it's an LLM error
        if "OPENAI_API_KEY" in str(e):
            print("   ℹ️  Error likely due to missing API Key. This is expected if no keys are set.")
        return False

def test_dev_tools_functionality():
    """Test actual functionality of Dev Tools."""
    print("\n🛠️  Testing Dev Tools Functionality...")
    try:
        from tools.dev_tools import CodeExecutorTool
        executor = CodeExecutorTool()
        
        # Test print capture
        code = "print('Hello from test')"
        result = executor._run(python_code=code)
        if "Hello from test" in result:
            print("✅ CodeExecutor captured stdout")
        else:
            print(f"❌ CodeExecutor failed to capture stdout: {result}")
            return False
            
        # Test variable return
        code = "x = 10 + 5"
        result = executor._run(python_code=code)
        if "15" in result:
             print("✅ CodeExecutor returned variables")
        else:
             print(f"❌ CodeExecutor failed to return variables: {result}")
             return False
             
        return True
    except Exception as e:
        print(f"❌ Dev tool test failed: {e}")
        return False

def test_ml_tools_functionality():
    """Test actual functionality of ML Tools."""
    print("\n🧪 Testing ML Tools Functionality...")
    import os  # Import os here to ensure it's available in the except block
    try:
        from tools.ml_tools import DatasetAnalyzerTool
        import pandas as pd
        
        # Create dummy csv
        dummy_path = "test_data.csv"
        df = pd.DataFrame({'A': [1, 2, 3], 'B': ['x', 'y', 'z']})
        df.to_csv(dummy_path, index=False)
        
        analyzer = DatasetAnalyzerTool()
        result = analyzer._run(dataset_path=dummy_path)
        
        # Clean up
        if os.path.exists(dummy_path):
            os.remove(dummy_path)
            
        if "dataset_shape" in result and "(3, 2)" in result:
            print("✅ DatasetAnalyzer read CSV correctly")
        else:
            print(f"❌ DatasetAnalyzer failed to read CSV: {result}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ ML tool test failed: {e}")
        # Clean up
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run CrewAI Verification Tests")
    parser.add_argument("--crew", type=str, help="Specific crew to test (ml, research, etc.)")
    parser.add_argument("--all", action="store_true", help="Test all crews")
    parser.add_argument("--tools", action="store_true", help="Test tool functionality")
    
    args = parser.parse_args()
    
    setup_environment()
    
    success = True
    
    # Always test imports
    if not test_tool_imports():
        success = False
        
    # Test specific functional checks
    if args.tools or args.all:
        if not test_dev_tools_functionality():
            success = False
        if not test_ml_tools_functionality():
            success = False

    # Test Crews
    crews_to_test = []
    if args.crew:
        crews_to_test.append(args.crew)
    elif args.all:
        crews_to_test = [
            "ml", "research", "research_academic", "research_content",
            "business_intelligence", "dev_code", "documentation"
        ]
    
    for crew in crews_to_test:
        if not test_crew_instantiation(crew):
            success = False
            
    if not args.crew and not args.all and not args.tools:
        parser.print_help()
        
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

