#!/usr/bin/env python3
"""
Terminal-Based AI Agent
A command-line interface for AI agents similar to OpenCode.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, List, Dict
import json

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.prompt import Prompt
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

class TerminalAgent:
    """Terminal-based AI agent for code assistance."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """Initialize the terminal agent."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.console = Console() if RICH_AVAILABLE else None
        
        if not self.api_key:
            self._error("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
            sys.exit(1)
        
        if not OPENAI_AVAILABLE:
            self._error("OpenAI library not installed. Install with: pip install openai")
            sys.exit(1)
        
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history = []
    
    def _print(self, message: str, style: str = ""):
        """Print message with optional styling."""
        if self.console:
            self.console.print(message, style=style)
        else:
            print(message)
    
    def _error(self, message: str):
        """Print error message."""
        if self.console:
            self.console.print(f"[red]Error:[/red] {message}")
        else:
            print(f"Error: {message}")
    
    def _success(self, message: str):
        """Print success message."""
        if self.console:
            self.console.print(f"[green]✓[/green] {message}")
        else:
            print(f"✓ {message}")
    
    def _info(self, message: str):
        """Print info message."""
        if self.console:
            self.console.print(f"[blue]ℹ[/blue] {message}")
        else:
            print(f"ℹ {message}")
    
    def chat(self, message: str) -> str:
        """Send a message to the agent and get response."""
        self.conversation_history.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
        except Exception as e:
            self._error(f"Failed to get response: {str(e)}")
            return ""
    
    def analyze_code(self, file_path: str) -> str:
        """Analyze a code file."""
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            prompt = f"""Analyze the following code file and provide:
1. A brief description of what the code does
2. Potential issues or improvements
3. Code quality assessment

Code:
```python
{code}
```
"""
            return self.chat(prompt)
        except FileNotFoundError:
            self._error(f"File not found: {file_path}")
            return ""
        except Exception as e:
            self._error(f"Error reading file: {str(e)}")
            return ""
    
    def explain_code(self, code: str) -> str:
        """Explain a piece of code."""
        prompt = f"""Explain the following code in detail:

```python
{code}
```

Provide:
1. What the code does
2. How it works
3. Key concepts used
"""
        return self.chat(prompt)
    
    def generate_code(self, description: str, language: str = "python") -> str:
        """Generate code from a description."""
        prompt = f"""Generate {language} code for the following task:

{description}

Provide:
1. Complete, working code
2. Brief comments explaining key parts
3. Usage example if applicable
"""
        return self.chat(prompt)
    
    def fix_code(self, code: str, error: Optional[str] = None) -> str:
        """Fix code issues."""
        prompt = f"""Fix the following code:
```python
{code}
```

{f'Error message: {error}' if error else ''}

Provide:
1. Fixed code
2. Explanation of what was wrong
3. What was changed
"""
        return self.chat(prompt)
    
    def interactive_mode(self):
        """Start interactive chat mode."""
        self._print("\n[bold cyan]Terminal Agent - Interactive Mode[/bold cyan]")
        self._print("Type 'exit' or 'quit' to end the session\n")
        
        while True:
            try:
                user_input = Prompt.ask("[bold green]You[/bold green]") if RICH_AVAILABLE else input("You: ")
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    self._info("Goodbye!")
                    break
                
                if not user_input.strip():
                    continue
                
                self._print("\n[bold blue]Agent[/bold blue]")
                response = self.chat(user_input)
                
                if self.console:
                    self.console.print(Markdown(response))
                else:
                    print(response)
                print()
                
            except KeyboardInterrupt:
                self._info("\nInterrupted. Goodbye!")
                break
            except Exception as e:
                self._error(f"Error: {str(e)}")
    
    def show_help(self):
        """Show help information."""
        help_text = """
[bold]Terminal Agent - AI Code Assistant[/bold]

[bold]Usage:[/bold]
  python agent.py [command] [options]

[bold]Commands:[/bold]
  chat <message>        Send a message to the agent
  analyze <file>        Analyze a code file
  explain <code>        Explain a piece of code
  generate <desc>       Generate code from description
  fix <code>            Fix code issues
  interactive           Start interactive chat mode
  help                  Show this help message

[bold]Options:[/bold]
  --model <model>       LLM model to use (default: gpt-3.5-turbo)
  --api-key <key>       OpenAI API key (or set OPENAI_API_KEY env var)

[bold]Examples:[/bold]
  python agent.py chat "Explain Python decorators"
  python agent.py analyze app.py
  python agent.py generate "A function to calculate fibonacci numbers"
  python agent.py interactive
"""
        if self.console:
            self.console.print(Panel(help_text, title="Help", border_style="blue"))
        else:
            print(help_text)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Terminal-based AI agent")
    parser.add_argument("command", nargs="?", help="Command to execute")
    parser.add_argument("input", nargs="*", help="Input for the command")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="LLM model to use")
    parser.add_argument("--api-key", help="OpenAI API key")
    
    args = parser.parse_args()
    
    agent = TerminalAgent(api_key=args.api_key, model=args.model)
    
    if not args.command or args.command == "help":
        agent.show_help()
        return
    
    command = args.command.lower()
    input_text = " ".join(args.input) if args.input else ""
    
    if command == "chat":
        if not input_text:
            agent._error("Please provide a message.")
            return
        response = agent.chat(input_text)
        if agent.console:
            agent.console.print(Markdown(response))
        else:
            print(response)
    
    elif command == "analyze":
        if not input_text:
            agent._error("Please provide a file path.")
            return
        response = agent.analyze_code(input_text)
        if agent.console:
            agent.console.print(Markdown(response))
        else:
            print(response)
    
    elif command == "explain":
        if not input_text:
            agent._error("Please provide code to explain.")
            return
        response = agent.explain_code(input_text)
        if agent.console:
            agent.console.print(Markdown(response))
        else:
            print(response)
    
    elif command == "generate":
        if not input_text:
            agent._error("Please provide a description.")
            return
        response = agent.generate_code(input_text)
        if agent.console:
            agent.console.print(Markdown(response))
        else:
            print(response)
    
    elif command == "fix":
        if not input_text:
            agent._error("Please provide code to fix.")
            return
        response = agent.fix_code(input_text)
        if agent.console:
            agent.console.print(Markdown(response))
        else:
            print(response)
    
    elif command == "interactive":
        agent.interactive_mode()
    
    else:
        agent._error(f"Unknown command: {command}")
        agent.show_help()

if __name__ == "__main__":
    main()

