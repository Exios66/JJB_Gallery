#!/usr/bin/env python3
"""
Terminal Agents - Production-Ready AI Coding Assistant
A comprehensive terminal-based AI agent for code assistance, similar to OpenCode.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

# Try to import rich for beautiful terminal UI
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Rich library not available. Install with: pip install rich")
    print("   Falling back to plain text output.\n")

# Try to import pygments for syntax highlighting
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
    from pygments.formatters import TerminalFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

# Import LLM providers
try:
    from openai import OpenAI as OpenAIClient
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from langchain_community.llms import Ollama
    from langchain.callbacks.manager import CallbackManager
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

from config import TerminalAgentConfig
from llm_providers import LLMProvider, get_llm_provider


class TerminalAgent:
    """Production-ready terminal-based AI agent for code assistance."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        config_path: Optional[str] = None
    ):
        """Initialize the terminal agent.
        
        Args:
            api_key: API key for LLM provider (overrides config)
            model: Model name to use (overrides config)
            provider: Provider name (overrides config)
            config_path: Path to config file
        """
        self.config = TerminalAgentConfig(config_path=config_path)
        
        # Override config with provided values
        if api_key:
            self.config.api_key = api_key
        if model:
            self.config.model = model
        if provider:
            self.config.provider = provider
        
        # Initialize console
        self.console = Console() if RICH_AVAILABLE else None
        
        # Initialize LLM provider
        self.llm: Optional[LLMProvider] = None
        self._initialize_llm()
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        
        # Working directory
        self.working_dir = Path.cwd()

    def _initialize_llm(self):
        """Initialize the LLM provider."""
        try:
            self.llm = get_llm_provider(
                provider=self.config.provider,
                api_key=self.config.api_key,
                model=self.config.model,
                config=self.config
            )
            if self.llm:
                if self.console:
                    self._print(f"[green]✓[/green] Using {self.llm.provider_name}: {self.llm.model_name}")
                else:
                    print(f"✓ Using {self.llm.provider_name}: {self.llm.model_name}")
            else:
                self._error("Failed to initialize LLM provider. Check your configuration.")
                self._print("\n[bold]Setup Instructions:[/bold]")
                self._print("1. Install Ollama (free, local): curl -fsSL https://ollama.ai/install.sh | sh")
                self._print("2. Or set API keys: export OPENAI_API_KEY=your_key")
                self._print("3. See README.md for more options")
        except ImportError as e:
            self._error(f"Missing dependency: {e}")
            self._print("\n[bold]Install missing dependencies:[/bold]")
            self._print("pip install -r requirements.txt")
        except Exception as e:
            self._error(f"Error initializing LLM: {e}")
            import traceback
            if self.config.verbose:
                self._print(f"\n[dim]{traceback.format_exc()}[/dim]")

    def _print(self, message: str, style: Optional[str] = None):
        """Print message with rich formatting if available."""
        if self.console:
            try:
                self.console.print(message, style=style)
            except Exception:
                # Fallback if rich fails
                import re
                clean = re.sub(r'\[.*?\]', '', message)
                print(clean)
        else:
            # Strip rich markup
            import re
            clean = re.sub(r'\[.*?\]', '', message)
            print(clean)

    def _error(self, message: str):
        """Print error message."""
        if self.console:
            self.console.print(f"[red]✗ Error:[/red] {message}")
        else:
            print(f"Error: {message}")

    def _success(self, message: str):
        """Print success message."""
        if self.console:
            self.console.print(f"[green]✓[/green] {message}")
        else:
            print(f"✓ {message}")

    def _code_block(self, code: str, language: str = "python"):
        """Display code block with syntax highlighting."""
        if self.console and PYGMENTS_AVAILABLE:
            syntax = Syntax(code, language, theme="monokai", line_numbers=True)
            self.console.print(syntax)
        elif self.console:
            self.console.print(Panel(code, title=f"[{language}]", border_style="blue"))
        else:
            print(f"\n```{language}\n{code}\n```")

    def chat(self, message: str, stream: bool = True) -> str:
        """Send a chat message to the agent.
        
        Args:
            message: User message
            stream: Whether to stream the response
            
        Returns:
            Agent response
        """
        if not self.llm:
            self._error("LLM provider not initialized")
            return ""
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        try:
            if stream and self.llm.supports_streaming:
                response = self._stream_chat(message)
            else:
                response = self.llm.chat(message, history=self.conversation_history)
            
            # Add response to history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
        except Exception as e:
            self._error(f"Chat error: {e}")
            return ""

    def _stream_chat(self, message: str) -> str:
        """Stream chat response."""
        if not self.console:
            # Fallback to non-streaming
            return self.llm.chat(message, history=self.conversation_history)
        
        full_response = ""
        with self.console.status("[bold blue]Thinking...", spinner="dots"):
            try:
                for chunk in self.llm.stream_chat(message, history=self.conversation_history):
                    if chunk:
                        full_response += chunk
                        self.console.print(chunk, end="")
                self.console.print()  # New line after streaming
            except Exception as e:
                self._error(f"Streaming error: {e}")
                # Fallback to non-streaming
                full_response = self.llm.chat(message, history=self.conversation_history)
        
        return full_response

    def analyze_code(self, code_or_file: str) -> str:
        """Analyze code for issues and improvements.
        
        Args:
            code_or_file: Code string or file path
            
        Returns:
            Analysis report
        """
        code = self._get_code(code_or_file)
        if not code:
            return ""
        
        prompt = f"""Analyze the following code and provide a comprehensive report including:
1. Code quality issues
2. Performance problems
3. Security vulnerabilities
4. Best practices violations
5. Refactoring opportunities
6. Suggestions for improvement

Code:
```python
{code}
```

Provide a detailed analysis:"""
        
        return self.chat(prompt, stream=False)

    def explain_code(self, code_or_file: str) -> str:
        """Explain code functionality in detail.
        
        Args:
            code_or_file: Code string or file path
            
        Returns:
            Explanation
        """
        code = self._get_code(code_or_file)
        if not code:
            return ""
        
        prompt = f"""Explain the following code in detail, including:
1. What the code does
2. How it works (step by step)
3. Key concepts and patterns used
4. Potential use cases
5. Any important considerations

Code:
```python
{code}
```

Provide a clear, educational explanation:"""
        
        return self.chat(prompt, stream=False)

    def generate_code(self, description: str, language: str = "python") -> str:
        """Generate code from a description.
        
        Args:
            description: Natural language description
            language: Programming language
            
        Returns:
            Generated code
        """
        prompt = f"""Generate {language} code based on the following description:
{description}

Requirements:
- Write clean, well-documented code
- Include type hints if applicable
- Add comments explaining key parts
- Follow best practices for {language}
- Include error handling where appropriate

Provide only the code with brief comments, no explanations outside the code:"""
        
        response = self.chat(prompt, stream=False)
        
        # Extract code block if present
        code = self._extract_code_block(response, language)
        return code if code else response

    def fix_code(self, code_or_file: str, issue: Optional[str] = None) -> str:
        """Fix bugs and issues in code.
        
        Args:
            code_or_file: Code string or file path
            issue: Specific issue to fix (optional)
            
        Returns:
            Fixed code
        """
        code = self._get_code(code_or_file)
        if not code:
            return ""
        
        issue_text = f"\nSpecific issue to fix: {issue}" if issue else ""
        
        prompt = f"""Fix the following code, addressing any bugs, errors, or issues.{issue_text}

Code:
```python
{code}
```

Provide the fixed code with explanations of what was changed:"""
        
        response = self.chat(prompt, stream=False)
        
        # Extract code block if present
        code = self._extract_code_block(response)
        return code if code else response

    def refactor_code(self, code_or_file: str, goal: Optional[str] = None) -> str:
        """Refactor code for better quality.
        
        Args:
            code_or_file: Code string or file path
            goal: Refactoring goal (e.g., "optimize performance", "improve readability")
            
        Returns:
            Refactored code
        """
        code = self._get_code(code_or_file)
        if not code:
            return ""
        
        goal_text = f"\nRefactoring goal: {goal}" if goal else ""
        
        prompt = f"""Refactor the following code to improve quality, maintainability, and follow best practices.{goal_text}

Code:
```python
{code}
```

Provide the refactored code with explanations of improvements:"""
        
        response = self.chat(prompt, stream=False)
        
        # Extract code block if present
        code = self._extract_code_block(response)
        return code if code else response

    def _get_code(self, code_or_file: str) -> Optional[str]:
        """Get code from string or file.
        
        Args:
            code_or_file: Code string or file path
            
        Returns:
            Code content or None if error
        """
        # Check if it's a file path
        file_path = Path(code_or_file)
        if file_path.exists() and file_path.is_file():
            try:
                return file_path.read_text()
            except Exception as e:
                self._error(f"Error reading file: {e}")
                return None
        else:
            # Assume it's code
            return code_or_file

    def _extract_code_block(self, text: str, language: str = "python") -> Optional[str]:
        """Extract code block from markdown response.
        
        Args:
            text: Response text
            language: Expected language
            
        Returns:
            Extracted code or None
        """
        import re
        # Look for code blocks
        pattern = rf'```(?:{language}|python)?\n(.*?)```'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def interactive_mode(self):
        """Start interactive chat mode."""
        if self.console:
            self.console.print(Panel.fit(
                "[bold cyan]Terminal Agents - AI Coding Assistant[/bold cyan]\n"
                "[dim]Type 'help' for commands, 'exit' to quit[/dim]",
                border_style="cyan"
            ))
        else:
            print("=" * 60)
            print("Terminal Agents - AI Coding Assistant")
            print("Type 'help' for commands, 'exit' to quit")
            print("=" * 60)
        
        self._print_status()
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    self._print("\n[cyan]Goodbye! 👋[/cyan]")
                    break
                
                if user_input.lower() == 'help':
                    self._show_interactive_help()
                    continue
                
                if user_input.lower() == 'clear':
                    self.conversation_history = []
                    self._success("Conversation history cleared")
                    continue
                
                if user_input.lower().startswith('save '):
                    filename = user_input[5:].strip()
                    self._save_conversation(filename)
                    continue
                
                # Check for command shortcuts
                if user_input.startswith('@'):
                    self._handle_command_shortcut(user_input)
                    continue
                
                # Regular chat
                self._print("\n🤖 Agent:")
                response = self.chat(user_input)
                
                if self.console:
                    self.console.print(Markdown(response))
                else:
                    print(response)
                    
            except KeyboardInterrupt:
                self._print("\n\n[cyan]Interrupted. Type 'exit' to quit.[/cyan]")
            except EOFError:
                self._print("\n[cyan]Goodbye! 👋[/cyan]")
                break
            except Exception as e:
                self._error(f"Error: {e}")

    def _print_status(self):
        """Print current status."""
        if not self.console:
            return
        
        table = Table(title="Status", show_header=False, box=None)
        table.add_row("Provider", f"[green]{self.llm.provider_name if self.llm else 'None'}[/green]")
        table.add_row("Model", f"[cyan]{self.llm.model_name if self.llm else 'None'}[/cyan]")
        table.add_row("Working Dir", f"[dim]{self.working_dir}[/dim]")
        self.console.print(table)

    def _show_interactive_help(self):
        """Show help for interactive mode."""
        help_text = """
[bold]Available Commands:[/bold]

  [cyan]@analyze <file>[/cyan]     - Analyze code file
  [cyan]@explain <file>[/cyan]    - Explain code file
  [cyan]@generate <desc>[/cyan]    - Generate code from description
  [cyan]@fix <file>[/cyan]         - Fix code issues
  [cyan]@refactor <file>[/cyan]   - Refactor code
  [cyan]clear[/cyan]               - Clear conversation history
  [cyan]save <file>[/cyan]         - Save conversation to file
  [cyan]help[/cyan]                - Show this help
  [cyan]exit[/cyan]                - Exit interactive mode

[bold]Examples:[/bold]
  @analyze app.py
  @generate "A function to calculate fibonacci"
  @fix buggy_code.py
        """
        if self.console:
            self.console.print(Panel(help_text, title="Help", border_style="blue"))
        else:
            print(help_text)

    def _handle_command_shortcut(self, command: str):
        """Handle command shortcuts in interactive mode."""
        parts = command[1:].split(' ', 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else None
        
        if cmd == 'analyze' and arg:
            self._print("\n🤖 Analyzing code...")
            result = self.analyze_code(arg)
            if self.console:
                self.console.print(Markdown(result))
            else:
                print(result)
        elif cmd == 'explain' and arg:
            self._print("\n🤖 Explaining code...")
            result = self.explain_code(arg)
            if self.console:
                self.console.print(Markdown(result))
            else:
                print(result)
        elif cmd == 'generate' and arg:
            self._print("\n🤖 Generating code...")
            result = self.generate_code(arg)
            self._code_block(result)
        elif cmd == 'fix' and arg:
            self._print("\n🤖 Fixing code...")
            result = self.fix_code(arg)
            self._code_block(result)
        elif cmd == 'refactor' and arg:
            self._print("\n🤖 Refactoring code...")
            result = self.refactor_code(arg)
            self._code_block(result)
        else:
            self._error("Invalid command. Type 'help' for available commands.")

    def _save_conversation(self, filename: str):
        """Save conversation history to file."""
        try:
            file_path = Path(filename)
            data = {
                "timestamp": datetime.now().isoformat(),
                "conversation": self.conversation_history
            }
            file_path.write_text(json.dumps(data, indent=2))
            self._success(f"Conversation saved to {filename}")
        except Exception as e:
            self._error(f"Error saving conversation: {e}")

    def show_help(self):
        """Show help message."""
        help_text = """
[bold cyan]Terminal Agents - AI Code Assistant[/bold cyan]

[bold]Usage:[/bold]
  python agent.py [command] [options]

[bold]Commands:[/bold]
  [cyan]chat <message>[/cyan]           Send a message to the agent
  [cyan]analyze <file>[/cyan]            Analyze code file for issues
  [cyan]explain <file|code>[/cyan]      Explain code functionality
  [cyan]generate <description>[/cyan]    Generate code from description
  [cyan]fix <file|code>[/cyan]          Fix bugs in code
  [cyan]refactor <file>[/cyan]          Refactor code for improvement
  [cyan]interactive[/cyan]               Start interactive chat mode
  [cyan]help[/cyan]                     Show this help message

[bold]Options:[/bold]
  [yellow]--api-key <key>[/yellow]       API key (overrides config)
  [yellow]--model <model>[/yellow]       Model name (overrides config)
  [yellow]--provider <name>[/yellow]     Provider name (overrides config)
  [yellow]--config <path>[/yellow]       Path to config file

[bold]Examples:[/bold]
  python agent.py chat "Explain Python decorators"
  python agent.py analyze app.py
  python agent.py generate "A function to calculate factorial"
  python agent.py interactive
        """
        if self.console:
            self.console.print(Panel(help_text, border_style="cyan"))
        else:
            print(help_text)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Terminal Agents - AI Coding Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("command", nargs="?", help="Command to execute")
    parser.add_argument("input", nargs="*", help="Input for the command")
    parser.add_argument("--api-key", help="API key for LLM provider")
    parser.add_argument("--model", help="Model name to use")
    parser.add_argument("--provider", help="LLM provider name")
    parser.add_argument("--config", help="Path to config file")
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = TerminalAgent(
        api_key=args.api_key,
        model=args.model,
        provider=args.provider,
        config_path=args.config
    )
    
    if not agent.llm:
        print("❌ Failed to initialize LLM provider.")
        print("   Please check your configuration and API keys.")
        sys.exit(1)
    
    # Handle commands
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
            agent._error("Please provide code or file path.")
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
        code = agent.generate_code(input_text)
        agent._code_block(code)
    
    elif command == "fix":
        if not input_text:
            agent._error("Please provide code or file path.")
            return
        code = agent.fix_code(input_text)
        agent._code_block(code)
    
    elif command == "refactor":
        if not input_text:
            agent._error("Please provide a file path.")
            return
        code = agent.refactor_code(input_text)
        agent._code_block(code)
    
    elif command == "interactive":
        agent.interactive_mode()
    
    else:
        agent._error(f"Unknown command: {command}")
        agent.show_help()


if __name__ == "__main__":
    main()

