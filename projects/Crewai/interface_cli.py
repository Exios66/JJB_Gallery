"""
CrewAI Terminal CLI Interface.
Interactive command-line interface for Agent Swarms.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from main import get_crew_class
from router import MetaRouter
from config import config

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 60)
    print("🤖 CrewAI Swarm CLI Chat")
    print("Interact with specialized AI agent swarms.")
    print("=" * 60)

def get_user_choice(options):
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("\nSelect an option: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a number.")

def main():
    clear_screen()
    print_header()

    # Configuration Phase
    print("\n⚙️  Configuration")
    print("-" * 20)
    
    print("\n1. Routing Mode:")
    routing_mode = get_user_choice(["Manual Selection", "Meta-Agent Router"])
    
    target_crew = None
    if routing_mode == "Manual Selection":
        print("\nSelect Swarm:")
        crew_options = [
            "ml", "research", "research_academic", "research_content",
            "business_intelligence", "dev_code", "documentation"
        ]
        target_crew = get_user_choice(crew_options)

    print("\n2. Input Mode:")
    input_mode = get_user_choice(["Dynamic (Chat)", "Static (Default Workflow)"])

    print("\n✅ Setup Complete! Starting Chat Session...")
    print("Type 'exit' or 'quit' to end the session.\n")

    # Chat Loop
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye! 👋")
                break
            
            if not user_input:
                continue

            print("\n🤖 Assistant: Processing...")

            # Determine Crew (if Meta-Agent)
            current_crew = target_crew
            if routing_mode == "Meta-Agent Router":
                print("   🔄 Routing request...")
                current_crew = MetaRouter.route_query(user_input)
                print(f"   ✅ Routed to: {current_crew}")

            # Prepare Inputs
            inputs = {"topic": user_input} if input_mode == "Dynamic (Chat)" else None
            
            # Execute
            crew_class = get_crew_class(current_crew)
            crew = crew_class()
            
            print(f"   🚀 Starting {current_crew} workflow...")
            result = crew.kickoff(inputs=inputs)
            
            print("\n" + "=" * 40)
            print(f"🏁 Result from {current_crew}:")
            print(str(result))
            print("=" * 40)

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()

