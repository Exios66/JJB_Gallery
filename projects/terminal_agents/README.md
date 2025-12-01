# Terminal Agents

A command-line AI agent interface for code assistance, similar to OpenCode. This tool provides AI-powered code analysis, generation, explanation, and debugging directly from your terminal.

## 🚀 Features

- **Code Analysis**: Analyze code files for issues and improvements
- **Code Explanation**: Get detailed explanations of code functionality
- **Code Generation**: Generate code from natural language descriptions
- **Code Fixing**: Fix bugs and improve code quality
- **Interactive Chat**: Real-time chat interface with AI agent
- **Rich Terminal UI**: Beautiful terminal interface with colors and formatting
- **Multiple Commands**: Various commands for different use cases

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key

## 🛠️ Installation

1. **Navigate to the project:**
   ```bash
   cd projects/terminal_agents
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key:**
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

   Or create a `.env` file:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## 🚀 Usage

### Interactive Mode

Start an interactive chat session:

```bash
python agent.py interactive
```

Or make it executable:

```bash
chmod +x agent.py
./agent.py interactive
```

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
python agent.py generate "A function to calculate factorial"
```

#### Fix Code

Fix code issues:

```bash
python agent.py fix "def broken_function(x): return x / 0"
```

### Help

View all available commands:

```bash
python agent.py help
```

## ⚙️ Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Command-Line Options

- `--model <model>`: LLM model to use (default: gpt-3.5-turbo)
- `--api-key <key>`: OpenAI API key (overrides environment variable)

### Example with Options

```bash
python agent.py --model gpt-4 chat "Explain machine learning"
```

## 🎯 Use Cases

### Code Review

```bash
python agent.py analyze src/main.py
```

### Learning New Code

```bash
python agent.py explain "$(cat complex_algorithm.py)"
```

### Quick Code Generation

```bash
python agent.py generate "A REST API endpoint for user authentication"
```

### Debugging

```bash
python agent.py fix "$(cat buggy_code.py)"
```

### General Questions

```bash
python agent.py chat "What is the difference between async and await in Python?"
```

## 📦 Project Structure

```
terminal_agents/
├── agent.py            # Main agent application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Customization

### Changing the Model

Edit the default model in `agent.py`:

```python
def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
    # Change default model here
```

### Adding New Commands

Add new command handlers in the `main()` function:

```python
elif command == "your_command":
    # Your command logic here
    response = agent.your_method(input_text)
    # Display response
```

### Custom Prompts

Modify prompt templates in the agent methods:

```python
def your_method(self, input_data: str) -> str:
    prompt = f"""Your custom prompt template here:
{input_data}
"""
    return self.chat(prompt)
```

## 🎨 Terminal UI

The agent uses the `rich` library for beautiful terminal output:

- **Colors**: Syntax highlighting and colored output
- **Markdown**: Renders markdown in terminal
- **Panels**: Beautiful bordered panels for help text
- **Progress**: Progress indicators for long operations

If `rich` is not available, the agent falls back to plain text output.

## 🐛 Troubleshooting

### API Key Not Found

```bash
export OPENAI_API_KEY=your_key_here
```

Or use the `--api-key` option:

```bash
python agent.py --api-key your_key_here chat "Hello"
```

### Import Errors

Install missing dependencies:

```bash
pip install -r requirements.txt
```

### Model Not Available

- Check your OpenAI API key has access to the model
- Verify the model name is correct
- Try a different model (e.g., `gpt-3.5-turbo`)

## 🚀 Advanced Usage

### Shell Integration

Add to your `.bashrc` or `.zshrc`:

```bash
alias ai="python /path/to/agent.py"
```

Then use:

```bash
ai chat "Hello"
ai analyze file.py
```

### Scripting

Use in scripts:

```bash
#!/bin/bash
RESPONSE=$(python agent.py generate "A function to sort a list")
echo "$RESPONSE"
```

### Piping

Pipe code to the agent:

```bash
cat code.py | python agent.py explain
```

## 📚 Examples

### Code Review Workflow

```bash
# Analyze all Python files in a directory
for file in *.py; do
    echo "Analyzing $file..."
    python agent.py analyze "$file"
done
```

### Learning Session

```bash
# Start interactive mode for learning
python agent.py interactive
# Then ask questions about code concepts
```

### Quick Fixes

```bash
# Fix a specific function
python agent.py fix "$(sed -n '10,20p' buggy_file.py)"
```

## 🔗 Related Projects

- [CrewAI](../Crewai/README.md) - Multi-agent system
- [ChatUI](../ChatUi/README.md) - Web chat interface
- [RAG Model](../RAG_Model/README.md) - Document Q&A

## 📄 License

This project is part of the JJB Gallery portfolio. See the main repository LICENSE file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue in the main repository.

## 🙏 Acknowledgments

Inspired by [OpenCode](https://opencode.ai) and similar terminal-based AI coding assistants.
