# Terminal Agents

AI coding agents for the terminal, providing AI-powered code analysis, generation, explanation, and debugging directly from your terminal.

## Overview

Terminal Agents provides a command-line interface for interacting with AI coding assistants. Similar to OpenCode, it offers code analysis, generation, explanation, and debugging capabilities.

## Features

- ✅ **Code Analysis**: Analyze code files for issues and improvements
- ✅ **Code Explanation**: Get detailed explanations of code functionality
- ✅ **Code Generation**: Generate code from natural language descriptions
- ✅ **Code Fixing**: Fix bugs and improve code quality
- ✅ **Interactive Chat**: Real-time chat interface with AI agent
- ✅ **Rich Terminal UI**: Beautiful terminal interface with colors and formatting

## Installation

```bash
cd projects/terminal_agents
pip install -r requirements.txt
```

## Quick Start

### Interactive Mode

```bash
python agent.py interactive
```

Or make it executable:

```bash
chmod +x agent.py
./agent.py interactive
```

## Usage

### Command-Line Commands

#### Chat

Send a message to the agent:

```bash
python agent.py chat "Explain Python decorators"
```

#### Analyze Code

Analyze a code file:

```bash
python agent.py analyze app.py
```

#### Explain Code

Explain a piece of code:

```bash
python agent.py explain "def fibonacci(n): return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)"
```

#### Generate Code

Generate code from a description:

```bash
python agent.py generate "Create a function to calculate factorial"
```

#### Fix Code

Fix bugs in a code file:

```bash
python agent.py fix buggy_code.py
```

## Configuration

### Environment Variables

```bash
export OPENAI_API_KEY=your_api_key_here
```

Or create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

## Features

### Code Analysis

The agent can analyze code for:
- Code quality issues
- Performance problems
- Security vulnerabilities
- Best practices violations
- Refactoring opportunities

### Code Explanation

Get detailed explanations of:
- Function behavior
- Algorithm logic
- Design patterns
- Complex code structures

### Code Generation

Generate code for:
- Functions and classes
- Complete applications
- Test cases
- Documentation

### Interactive Chat

Engage in real-time conversation about:
- Code questions
- Programming concepts
- Debugging help
- Architecture decisions

## Project Structure

```
terminal_agents/
├── agent.py            # Main agent script
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## Advanced Usage

### Custom Prompts

Modify agent prompts in `agent.py` to customize behavior.

### Integration

Integrate with your workflow:

```bash
# In your scripts
python agent.py analyze $1 > analysis.txt
```

## Troubleshooting

### API Key Issues

Ensure your OpenAI API key is set:

```bash
echo $OPENAI_API_KEY
```

### Import Errors

```bash
pip install -r requirements.txt
```

## Related Documentation

- [Installation Guide](Installation-Guide.md)
- [Configuration Guide](Configuration-Guide.md)
- [Quick Start](Quick-Start.md)

