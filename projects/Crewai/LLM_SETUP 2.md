# Multi-Provider LLM Configuration Guide

This system now supports multiple LLM providers with automatic detection and prioritization of free/open-source options to reduce costs.

## 🎯 Quick Start (Recommended - FREE)

### Option 1: Ollama (Local, Free, No API Costs)

**Install Ollama:**
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai
```

**Download a model:**
```bash
ollama pull llama3.1:8b        # Good general purpose (8GB)
ollama pull mistral:7b         # Fast and efficient (4GB)
ollama pull codellama:13b      # Great for code tasks (7GB)
ollama pull phi3:mini          # Very small, runs on most hardware (2GB)
```

**Start Ollama (usually runs automatically):**
```bash
ollama serve
```

**That's it!** The system will automatically detect Ollama and use it.

### Option 2: Set Environment Variables (Optional)

```bash
export OLLAMA_MODEL=llama3.1:8b
export OLLAMA_BASE_URL=http://localhost:11434
```

## 💰 Paid Provider Options

### OpenAI

```bash
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL_NAME=gpt-4o-mini  # Affordable option
```

**Models:** `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`, `gpt-4o-mini` (recommended for cost)

### Anthropic Claude

```bash
export ANTHROPIC_API_KEY=your_key_here
export ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Models:** `claude-3-5-sonnet-20241022`, `claude-3-opus`, `claude-3-haiku`

### Google Gemini (Free Tier Available)

```bash
export GOOGLE_API_KEY=your_key_here
export GOOGLE_MODEL=gemini-pro
```

**Get API Key:** https://ai.google.dev

### Azure OpenAI

```bash
export AZURE_OPENAI_API_KEY=your_key_here
export AZURE_OPENAI_ENDPOINT=your_endpoint
export AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment
export AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

## 🔧 How It Works

### Automatic Provider Detection

The system automatically detects available providers in this priority order:

1. **Ollama** (free, local) ← **HIGHEST PRIORITY**
2. OpenAI
3. Anthropic
4. Google
5. Azure

### Manual Provider Selection

To force a specific provider:

```bash
export LLM_PROVIDER=ollama
export LLM_PROVIDER=openai
export LLM_PROVIDER=anthropic
export LLM_PROVIDER=google
export LLM_PROVIDER=azure
```

## 📋 Setup Commands

### Check Status

```bash
python main.py --setup
```

Shows:
- Available providers
- Configured status
- Auto-detected provider

### View Setup Instructions

```bash
python main.py --setup-llm
```

Displays detailed setup instructions for all providers.

## 🔍 Troubleshooting

### "No LLM provider detected"

1. **For Ollama:**
   - Check if Ollama is running: `ollama list`
   - Start Ollama: `ollama serve`
   - Verify connection: `curl http://localhost:11434/api/tags`

2. **For other providers:**
   - Verify API keys are set: `echo $OPENAI_API_KEY`
   - Check environment variables are exported

### "Error importing native provider"

This means no LLM provider is configured. Follow the Quick Start guide above.

### Ollama Connection Issues

- Ensure Ollama is running
- Check firewall settings
- Try: `export OLLAMA_BASE_URL=http://localhost:11434`

## 💡 Cost Optimization Tips

1. **Use Ollama for development/testing** - Completely free
2. **Use `gpt-4o-mini` instead of `gpt-4`** - 10x cheaper
3. **Use local models for non-critical tasks** - No API costs
4. **Google Gemini has a generous free tier** - Good for experimentation

## 📦 Required Packages

Most providers work out of the box with CrewAI. Optional packages for direct LLM access:

```bash
# For Ollama direct access (optional, CrewAI uses OpenAI-compatible endpoint)
pip install langchain-community

# For OpenAI
pip install langchain-openai

# For Anthropic
pip install langchain-anthropic

# For Google
pip install langchain-google-genai
```

## 🚀 Example Usage

Once configured, the system works automatically:

```python
from crews import MLCrew

# Automatically uses detected provider
crew = MLCrew()
result = crew.kickoff(inputs={"topic": "Random Forest Classification"})
```

The LLM provider is automatically configured when you import the modules!

## 📚 Additional Resources

- **Ollama:** https://ollama.ai
- **OpenAI:** https://platform.openai.com
- **Anthropic:** https://console.anthropic.com
- **Google AI Studio:** https://ai.google.dev

