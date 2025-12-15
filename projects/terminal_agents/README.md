# Terminal Agents - Production-Ready AI Coding Assistant

A comprehensive terminal-based AI agent for code assistance, similar to OpenCode. Provides AI-powered code analysis, generation, explanation, and debugging directly from your terminal.

## 🚀 Features

- **Multi-Provider LLM Support**: OpenAI, Anthropic Claude, Ollama (free/local), Google, Azure
- **Code Analysis**: Analyze code files for issues, security vulnerabilities, and improvements
- **Code Explanation**: Get detailed explanations of code functionality
- **Code Generation**: Generate code from natural language descriptions
- **Code Fixing**: Fix bugs and improve code quality
- **Code Refactoring**: Refactor code for better maintainability
- **Interactive Chat**: Real-time chat interface with conversation history
- **Rich Terminal UI**: Beautiful terminal interface with colors, markdown, and syntax highlighting
- **File Operations**: Read, analyze, and work with code files
- **Configuration Management**: YAML config files and environment variables

## 📋 Prerequisites

- Python 3.8+
- At least one LLM provider configured:
  - **Ollama** (Recommended - Free, local): [Install Ollama](https://ollama.ai)
  - **OpenAI API Key**: [Get API Key](https://platform.openai.com/api-keys)
  - **Anthropic API Key**: [Get API Key](https://console.anthropic.com)
  - **Google API Key**: [Get API Key](https://makersuite.google.com/app/apikey)
  - **Azure OpenAI**: Configure Azure endpoint

## 🛠️ Installation

### Quick Setup

```bash
cd projects/terminal_agents
./setup.sh
```

### Manual Setup

1. **Navigate to the project:**

   ```bash
   cd projects/terminal_agents
   ```

2. **Create virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Make agent executable:**

   ```bash
   chmod +x agent.py
   ```

## ⚙️ Configuration

### Option 1: Environment Variables (Recommended)

```bash
# For OpenAI
export OPENAI_API_KEY=your_api_key_here

# For Anthropic
export ANTHROPIC_API_KEY=your_api_key_here

# For Ollama (default, no key needed if running locally)
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.1:8b
```

### Option 2: Config File

Create `~/.terminal_agents/config.yaml`:

```yaml
# Provider selection (auto-detect if not set)
provider: ollama  # Options: ollama, openai, anthropic, google, azure

# Ollama (Free, Local)
ollama_base_url: http://localhost:11434
ollama_model: llama3.1:8b

# OpenAI
openai_api_key: your_key_here
openai_model: gpt-4o-mini

# Anthropic
anthropic_api_key: your_key_here
anthropic_model: claude-3-5-sonnet-20241022
```

### Option 3: Command Line Arguments

```bash
python agent.py --api-key your_key --provider openai --model gpt-4 chat "Hello"
```

## 🚀 Usage

### Interactive Mode (Recommended)

Start an interactive chat session:

```bash
python agent.py interactive
# or
./agent.py interactive
```

**Interactive Commands:**

- `@analyze <file>` - Analyze code file
- `@explain <file>` - Explain code file
- `@generate <description>` - Generate code
- `@fix <file>` - Fix code issues
- `@refactor <file>` - Refactor code
- `clear` - Clear conversation history
- `save <file>` - Save conversation
- `help` - Show help
- `exit` - Exit interactive mode

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
# or
python agent.py explain app.py
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
# or
python agent.py fix buggy_code.py
```

#### Refactor Code

Refactor code for improvement:

```bash
python agent.py refactor app.py
```

### Help

View all available commands:

```bash
python agent.py help
```

## 🏭 Production Considerations

### CLI Distribution

To distribute this tool to a team:

1. **PyPI Package**: Package the agent as a Python package and publish to a private PyPI repository.

   ```bash
   python -m build
   twine upload dist/*
   ```

2. **Standalone Binary**: Use PyInstaller to create a single-file executable.

   ```bash
   pyinstaller --onefile agent.py
   ```

3. **Docker Image**: Distribute as a Docker image for consistent environments.

   ```bash
   docker run -it -v $(pwd):/app/code terminal-agent:latest
   ```

### Configuration Management

For team-wide configuration:

1. **Shared Config**: Distribute a standard `config.yaml` to `~/.terminal_agents/` via configuration management tools (Ansible, Chef).
2. **Environment Variables**: Enforce API keys via environment variables in CI/CD pipelines.

### Security Hardening

1. **API Key Storage**: Never commit `config.yaml` with API keys to version control. Use a secrets manager (e.g., `keyring` python package) for local storage.
2. **Input Sanitization**: The agent executes within the user's shell context. Ensure prompts do not contain malicious shell commands if piping input.
3. **Audit Logging**: Enable logging to a file to audit agent usage and generated code.

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
├── agent.py              # Main agent application
├── config.py            # Configuration management
├── llm_providers.py     # LLM provider implementations
├── requirements.txt      # Python dependencies
├── setup.sh             # Setup script
├── DESIGN.md            # Design documentation
└── README.md            # This file
```

## 🔧 Customization

### Changing the Default Model

Edit the default model in `config.py` or set environment variables:

```bash
export OLLAMA_MODEL=mistral:7b
export OPENAI_MODEL_NAME=gpt-4
```

### Adding New Commands

Add new command handlers in the `main()` function in `agent.py`.

### Custom Prompts

Modify prompt templates in the agent methods.

## 🎨 Terminal UI

The agent uses the `rich` library for beautiful terminal output:

- **Colors**: Syntax highlighting and colored output
- **Markdown**: Renders markdown in terminal
- **Panels**: Beautiful bordered panels for help text
- **Progress**: Progress indicators for long operations
- **Syntax Highlighting**: Code blocks with syntax highlighting

If `rich` is not available, the agent falls back to plain text output.

## 🔐 Security & Safety

- File write operations require explicit confirmation
- API keys are never logged or displayed
- Error messages are sanitized
- Safe file path handling

## 🐛 Troubleshooting

### "No LLM provider available"

**Solution**: Configure at least one provider:

- Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
- Or set API keys: `export OPENAI_API_KEY=your_key`

### "Module not found" errors

**Solution**: Install dependencies:

```bash
pip install -r requirements.txt
```

### Ollama connection errors

**Solution**: Ensure Ollama is running:

```bash
ollama serve
# In another terminal:
ollama pull llama3.1:8b
```

### Rich library not working

**Solution**: The agent will fall back to plain text. To fix:

```bash
pip install rich pygments
```

## 📚 Examples

### Example 1: Analyze Python File

```bash
python agent.py analyze my_script.py
```

### Example 2: Generate Code

```bash
python agent.py generate "A function to sort a list of dictionaries by a key"
```

### Example 3: Interactive Session

```bash
python agent.py interactive
> @analyze app.py
> @generate "A REST API with FastAPI"
> @fix buggy_function.py
> exit
```

### Example 4: With API Key

```bash
python agent.py --api-key your_key_here chat "Hello"
```

### Example 5: Pipe Code

```bash
cat code.py | python agent.py explain
```

## 🔗 Related Projects

- [CrewAI](../Crewai/README.md) - Multi-agent system
- [ChatUi](../ChatUi/README.md) - Web-based chat interface
- [OpenCode](https://opencode.ai) - Inspiration for this project

## 📝 License

See main repository LICENSE file.

## 🤝 Contributing

Contributions welcome! Please read the main repository contributing guidelines.

## 🙏 Acknowledgments

Inspired by [OpenCode](https://opencode.ai) and similar terminal-based AI coding assistants.

---

**Made with ❤️ for developers who love the terminal**

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
