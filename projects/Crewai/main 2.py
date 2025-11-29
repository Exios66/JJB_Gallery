#!/usr/bin/env python3
"""
CrewAI ML Agent Swarm - Main Entry Point
Complete Random Forest ML analysis using specialized AI agents.
"""

import os
import sys
from pathlib import Path

# Add the crewai directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from crews import (
    MLCrew,
    ResearchCrew,
    ResearchAcademicCrew,
    ResearchContentCrew,
    BusinessIntelligenceCrew,
    DevCodeCrew,
    DocumentationCrew,
)
try:
    from config import config
    from llm_config import get_setup_instructions, get_llm_for_agent, configure_crewai_environment
except ImportError:
    # Fallback for when running as a module
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from config import config
    from llm_config import get_setup_instructions, get_llm_for_agent, configure_crewai_environment

# Configure LLM environment on import
configure_crewai_environment()


def setup_environment():
    """Setup and validate the environment for CrewAI."""
    print("🔧 Setting up CrewAI ML Agent Swarm...")
    print("=" * 60)

    # Check environment configuration using new multi-provider system
    env_status = config.validate_environment()

    print("\n📊 LLM Provider Status:")
    print("-" * 60)
    
    providers = config.get_available_providers()
    for provider_name, description, is_available in providers:
        status = "✅" if is_available else "❌"
        print(f"  {status} {description}")
    
    # Show detected provider
    detected_provider = env_status.get("_DETECTED_PROVIDER")
    if detected_provider:
        print(f"\n🎯 Auto-detected provider: {detected_provider.upper()}")
        if detected_provider == "ollama":
            print("   💰 Using FREE local model - no API costs!")
    else:
        print("\n❌ No LLM provider detected!")

    # Check if at least one provider is available
    has_llm_provider = env_status.get("LLM_PROVIDER", False)
    
    # Check web search (optional)
    has_search = env_status.get("SERPER_API_KEY", False)
    
    if not has_llm_provider:
        print("\n" + "=" * 60)
        print("⚠️  NO LLM PROVIDER CONFIGURED!")
        print("=" * 60)
        print(get_setup_instructions())
        print("\n💡 RECOMMENDATION: Use Ollama (FREE, local, no API costs)")
        print("   Quick start: https://ollama.ai → Install → ollama pull llama3.1:8b")
        return False
    else:
        # Try to initialize LLM to verify it works
        print("\n🔍 Verifying LLM connection...")
        llm = get_llm_for_agent()
        if llm:
            print("✅ LLM configured successfully!")
        else:
            print("⚠️  LLM configuration available but failed to initialize")
            print("   Check your provider settings and ensure required packages are installed")
    
    if not has_search:
        print("\n⚠️  SERPER_API_KEY not set - web search features will be limited")
        print("   (Optional) Get free API key: https://serper.dev")
    
    print("\n✅ Environment setup complete!")
    return True


def get_crew_class(crew_type: str):
    """Get the appropriate crew class based on type."""
    crew_classes = {
        "ml": MLCrew,
        "research": ResearchCrew,
        "research_academic": ResearchAcademicCrew,
        "research_content": ResearchContentCrew,
        "business_intelligence": BusinessIntelligenceCrew,
        "dev_code": DevCodeCrew,
        "documentation": DocumentationCrew,
    }
    return crew_classes.get(crew_type.lower(), MLCrew)


def run_analysis(crew_type: str = "ml"):
    """Run the complete analysis workflow for the specified crew type."""
    try:
        crew_class = get_crew_class(crew_type)
        crew_name = crew_class.__name__.replace("Crew", "").replace("ML", "ML ")

        print(f"\n🤖 Initializing {crew_name} Agent Swarm...")
        print("-" * 40)

        # Create and configure the crew
        crew = crew_class(process=config.PROCESS_TYPE)

        print("Agents initialized:")
        agent_names = list(crew.agents.keys())
        for i, name in enumerate(agent_names, 1):
            print(f"  {i}. {name.replace('_', ' ').title()}")

        print(f"\nTasks configured: {len(crew.tasks)}")
        for i, task in enumerate(crew.tasks, 1):
            agent_name = task.agent.role.split()[0].lower()  # Extract first word
            print(f"  {i}. {task.description[:50]}... ({agent_name})")

        print(f"\n🚀 Starting {crew_name} Analysis Workflow...")
        print("=" * 60)

        # Execute the workflow
        result = crew.kickoff()

        print("\n" + "=" * 60)
        print(f"🎉 {crew_name} Analysis Workflow Complete!")
        print("=" * 60)

        print("\n📄 Generated Reports:")
        outputs_dir = config.OUTPUTS_DIR
        if outputs_dir.exists():
            for file_path in outputs_dir.glob("*.md"):
                print(f"  • {file_path.name}")

        print("\n📊 Final Result:")
        print(result)

        return result

    except Exception as e:
        crew_name = get_crew_class(crew_type).__name__.replace("Crew", "").replace("ML", "ML ")
        print(f"\n❌ Error during {crew_name} analysis: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your API keys are correctly set")
        print("2. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("3. Verify network connectivity for API calls")
        print("4. Check the outputs/ directory for partial results")
        raise


def run_ml_analysis():
    """Run the ML analysis workflow (backward compatibility)."""
    return run_analysis("ml")


def show_status():
    """Show current configuration and status."""
    print("📊 CrewAI Multi-Agent Swarm System Status")
    print("=" * 50)

    # Check environment
    env_status = config.validate_environment()
    env_ready = env_status.get("LLM_PROVIDER", False)

    print(f"Environment Ready: {'✅' if env_ready else '❌'}")
    print(f"API Keys Configured: {sum(env_status.values())}/4")

    print("\nConfiguration:")
    print(f"  verbose: {config.VERBOSE}")
    print(f"  process_type: {config.PROCESS_TYPE}")
    print(f"  outputs_dir: {config.OUTPUTS_DIR}")

    print("\n🤖 Available Crew Types:")
    crews_info = [
        ("ml", "ML Analysis", "Random Forest evaluation"),
        ("research", "Research", "Trends & innovation"),
        ("research_academic", "Academic Research", "Scholarly analysis"),
        ("research_content", "Content Research", "Content creation"),
        ("business_intelligence", "Business Intelligence", "Market analysis"),
        ("dev_code", "Dev & Code", "Software development"),
        ("documentation", "Documentation", "Technical writing"),
    ]

    for crew_type, name, desc in crews_info:
        try:
            crew_class = get_crew_class(crew_type)
            crew_status = crew_class.get_status()
            agent_count = crew_status.get('agents_available', 'Unknown')
            print(f"  {crew_type:<20} {name:<18} {desc:<25} ({agent_count} agents)")
        except:
            print(f"  {crew_type:<20} {name:<18} {desc:<25} (Status unavailable)")

    if not env_ready:
        print("\n⚠️  Run setup first: python main.py --setup")
        print("💡 Use --list-crews to see all available swarms")


def main():
    """Main entry point with command line argument handling."""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command in ["--help", "-h"]:
            print("CrewAI Multi-Agent Swarm System")
            print("Usage: python main.py [command] [crew_type]")
            print("")
            print("Commands:")
            print("  (no args)          Run ML analysis workflow")
            print("  --setup            Setup environment and validate configuration")
            print("  --setup-llm        Show LLM provider setup instructions")
            print("  --status           Show current status and configuration")
            print("  --list-crews       List all available crew types")
            print("  --run <crew_type>  Run specific crew workflow")
            print("  --help             Show this help message")
            print("")
            print("Available Crew Types:")
            print("  ml                    Machine Learning analysis")
            print("  research             General ML research")
            print("  research_academic    Academic research")
            print("  research_content     Content research")
            print("  business_intelligence Business intelligence")
            print("  dev_code             Development and coding")
            print("  documentation        Technical documentation")
            return

        elif command == "--setup":
            success = setup_environment()
            if success:
                print("\n🎯 Ready to run agent swarms!")
                print("Execute: python main.py --run ml")
            return

        elif command == "--setup-llm":
            print(get_setup_instructions())
            return

        elif command == "--status":
            show_status()
            return

        elif command == "--list-crews":
            print("🤖 Available Crew Types:")
            print("=" * 40)
            crews_info = [
                ("ml", "Machine Learning Analysis", "Complete Random Forest evaluation"),
                ("research", "Research Swarm", "ML trends and innovation"),
                ("research_academic", "Academic Research", "Scholarly literature review"),
                ("research_content", "Content Research", "Content creation and strategy"),
                ("business_intelligence", "Business Intelligence", "Market and business analysis"),
                ("dev_code", "Development & Code", "Software development workflows"),
                ("documentation", "Documentation", "Technical writing and docs"),
            ]
            for crew_type, name, desc in crews_info:
                print(f"  {crew_type:<20} {name:<25} {desc}")
            return

        elif command == "--run":
            if len(sys.argv) < 3:
                print("❌ Error: --run requires a crew type")
                print("Usage: python main.py --run <crew_type>")
                print("Run 'python main.py --list-crews' to see available types")
                return

            crew_type = sys.argv[2]
            available_crews = ["ml", "research", "research_academic", "research_content",
                             "business_intelligence", "dev_code", "documentation"]

            if crew_type not in available_crews:
                print(f"❌ Unknown crew type: {crew_type}")
                print("Run 'python main.py --list-crews' to see available types")
                return

            if not setup_environment():
                print("\n❌ Environment not properly configured.")
                print("Run: python main.py --setup")
                sys.exit(1)

            run_analysis(crew_type)
            return

        else:
            print(f"Unknown command: {command}")
            print("Use --help for available commands")
            return

    # Default behavior: run ML analysis
    if not setup_environment():
        print("\n❌ Environment not properly configured.")
        print("Run: python main.py --setup")
        sys.exit(1)

    run_ml_analysis()


if __name__ == "__main__":
    main()