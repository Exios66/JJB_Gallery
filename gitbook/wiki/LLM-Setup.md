# LLM Setup Guide

Comprehensive guide for setting up Large Language Model (LLM) providers across all projects in the JJB Gallery repository.

## Overview

Many projects in this repository support multiple LLM providers with automatic detection and prioritization of free/open-source options to reduce costs. This guide covers setup for all supported providers.

## Quick Start (Recommended - FREE)

### Option 1: Ollama (Local, Free, No API Costs)

Ollama is the recommended option for local development and testing. It runs models locally with no API costs.

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

**That's it!** Projects will automatically detect Ollama and use it.

### Option 2: Set Environment Variables (Optional)

```bash
export OLLAMA_MODEL=llama3.1:8b
export OLLAMA_BASE_URL=http://localhost:11434
```

## Paid Provider Options

### OpenAI

```bash
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL_NAME=gpt-4o-mini  # Affordable option
```

**Models Available:**

- `gpt-4` - Most capable (expensive)
- `gpt-4-turbo` - Fast GPT-4 variant
- `gpt-4o-mini` - Affordable, recommended
- `gpt-3.5-turbo` - Fast and economical

**Get API Key:** <https://platform.openai.com/api-keys>

### Anthropic Claude

```bash
export ANTHROPIC_API_KEY=your_key_here
export ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Models Available:**

- `claude-3-5-sonnet-20241022` - Latest, most capable
- `claude-3-opus` - Most powerful
- `claude-3-haiku` - Fast and efficient

**Get API Key:** <https://console.anthropic.com/>

### Google Gemini (Free Tier Available)

```bash
export GOOGLE_API_KEY=your_key_here
export GOOGLE_MODEL=gemini-pro
```

**Models Available:**

- `gemini-pro` - General purpose
- `gemini-pro-vision` - Multimodal

**Get API Key:** <https://ai.google.dev>

### Azure OpenAI

```bash
export AZURE_OPENAI_API_KEY=your_key_here
export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
export AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
export AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**Setup:** Requires Azure OpenAI resource setup in Azure Portal

## How Automatic Detection Works

Most projects automatically detect available providers in this priority order:

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

## Project-Specific Setup

### CrewAI Multi-Agent System

The CrewAI system has comprehensive LLM setup support:

```bash
cd projects/Crewai
python main.py --setup        # Check status
python main.py --setup-llm    # View detailed instructions
```

For detailed CrewAI-specific setup, see [CrewAI Multi-Agent System](CrewAI-Multi-Agent-System.md).

### RAG Model

RAG Model supports Ollama for local generation:

```bash
# Set in .env or environment
RAG_LLM_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```

See [RAG Model](RAG-Model.md) for complete configuration.

### iOS Chatbot

Supports multiple providers via environment variables:

```bash
# .env file
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...
# OR
OLLAMA_URL=http://localhost:11434
```

See [iOS Chatbot](iOS-Chatbot.md) for details.

### LiteLLM Integration

LiteLLM provides unified access to all providers:

```bash
# Set provider-specific keys
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=...

# Use via proxy or directly
python proxy_server.py
```

See [LiteLLM Integration](LiteLLM-Integration.md) for comprehensive documentation.

### Terminal Agents

Currently supports OpenAI:

```bash
export OPENAI_API_KEY=your_api_key_here
```

See [Terminal Agents](Terminal-Agents.md) for usage.

## Setup Verification

### Check Ollama

```bash
# List available models
ollama list

# Test connection
curl http://localhost:11434/api/tags
```

### Check API Keys

```bash
# Verify keys are set
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
echo $GOOGLE_API_KEY
```

### Test Provider Connection

**OpenAI:**

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

**Anthropic:**

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

## Troubleshooting

### "No LLM provider detected"

1. **For Ollama:**
   - Check if Ollama is running: `ollama list`
   - Start Ollama: `ollama serve`
   - Verify connection: `curl http://localhost:11434/api/tags`

2. **For other providers:**
   - Verify API keys are set: `echo $OPENAI_API_KEY`
   - Check environment variables are exported
   - Restart your terminal/session after setting variables

### "Error importing native provider"

This means no LLM provider is configured. Follow the Quick Start guide above to set up at least one provider.

### Ollama Connection Issues

- Ensure Ollama is running: `ollama serve`
- Check firewall settings
- Try explicit URL: `export OLLAMA_BASE_URL=http://localhost:11434`
- Verify port 11434 is not blocked

### API Key Not Working

1. Verify key is valid and has credits/quota
2. Check for extra spaces or quotes in the key
3. Ensure key hasn't expired
4. Verify key has required permissions

## Cost Optimization Tips

1. **Use Ollama for development/testing** - Completely free, runs locally
2. **Use `gpt-4o-mini` instead of `gpt-4`** - 10x cheaper with good performance
3. **Use local models for non-critical tasks** - No API costs
4. **Google Gemini has a generous free tier** - Good for experimentation
5. **Monitor API usage** - Set up billing alerts for paid providers

## Required Packages

### For Ollama

No Python packages needed - just install the Ollama application. However, some projects may require:

```bash
pip install langchain-community
```

### For OpenAI

```bash
pip install langchain-openai
# or
pip install openai
```

### For Anthropic

```bash
pip install langchain-anthropic
# or
pip install anthropic
```

### For Google

```bash
pip install langchain-google-genai
```

### For Azure OpenAI

```bash
pip install langchain-openai  # Same as OpenAI
```

## Environment File Setup

Create a `.env` file in your project directory:

```bash
# .env file example
# Ollama (Free)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# OpenAI (Paid)
OPENAI_API_KEY=sk-...
OPENAI_MODEL_NAME=gpt-4o-mini

# Anthropic (Paid)
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Google (Free tier available)
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-pro
```

**Important:** Add `.env` to `.gitignore` to avoid committing secrets!

## Best Practices

1. **Use local models for development** - Ollama is free and fast for local work
2. **Use cloud providers for production** - When you need consistent, high-quality responses
3. **Set up environment variables** - Never hardcode API keys in source code
4. **Use `.env` files** - Keep secrets out of version control
5. **Monitor costs** - Set up billing alerts for paid providers
6. **Test with free options first** - Verify functionality before committing to paid plans

## Additional Resources

- **Ollama:** <https://ollama.ai>
- **OpenAI:** <https://platform.openai.com>
- **Anthropic:** <https://console.anthropic.com>
- **Google AI Studio:** <https://ai.google.dev>
- **Azure OpenAI:** <https://azure.microsoft.com/en-us/products/ai-services/openai-service>

## Related Documentation

- [Configuration Guide](Configuration-Guide.md) - Detailed configuration for all projects
- [CrewAI Multi-Agent System](CrewAI-Multi-Agent-System.md) - CrewAI-specific LLM setup
- [Installation Guide](Installation-Guide.md) - Project installation instructions
- [Troubleshooting](Troubleshooting.md) - Common issues and solutions

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
