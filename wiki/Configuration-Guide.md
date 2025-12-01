# Configuration Guide

Complete guide to configuring all projects in the JJB Gallery repository.

## Overview

This guide covers environment variables, configuration files, and settings for all projects.

## RAG Model

### Environment Variables

Create `.env` in `projects/RAG_Model/`:

```bash
# Embedding Model Configuration
RAG_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
# Alternatives:
# RAG_EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
# RAG_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L12-v2

# Vector Store Configuration
RAG_VECTOR_STORE_PATH=vector_store

# LLM Configuration (for generation)
RAG_LLM_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434

# Text Chunking Configuration
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200

# Retrieval Configuration
RAG_DEFAULT_K=5

# Optional: OpenAI API Key (if using OpenAI for generation)
# OPENAI_API_KEY=sk-...

# Optional: Hugging Face Token (for gated models)
# HF_TOKEN=hf_...
```

### Configuration File

Use `config.py` for programmatic configuration:

```python
from config import config

print(config.EMBEDDING_MODEL)
print(config.CHUNK_SIZE)
```

## Psychometrics

### Environment Variables

No required environment variables. Optional for future features:

```bash
# Optional: For future LLM integration
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# Data Storage (optional - for future database integration)
# DATABASE_URL=sqlite:///psychometrics.db
```

## ChatUi

### Environment Variables

Create `.env.local` in `projects/ChatUi/`:

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:3000

# MongoDB Configuration (for chat history)
MONGODB_URL=mongodb://localhost:27017/chatui

# Hugging Face Token (optional)
HF_TOKEN=

# OpenAI API Key (optional)
OPENAI_API_KEY=

# Ollama Configuration (optional)
OLLAMA_BASE_URL=http://localhost:11434
```

### Model Configuration

Configure models in `.env.local`:

```env
MODELS=`[
  {
    "name": "gpt-3.5-turbo",
    "displayName": "GPT 3.5 Turbo",
    "endpoints": [{"type": "openai"}]
  }
]`
```

## iOS Chatbot

### Environment Variables

Create `.env` in `projects/ios_chatbot/`:

```bash
# Flask Configuration
FLASK_ENV=development
PORT=5000
SECRET_KEY=your-secret-key-change-in-production

# LLM Provider Configuration (choose one or more)

# OpenAI
# OPENAI_API_KEY=sk-...

# Anthropic Claude
# ANTHROPIC_API_KEY=sk-ant-...

# Ollama (local, no API key needed)
# OLLAMA_URL=http://localhost:11434

# Google Gemini
# GOOGLE_API_KEY=...

# Hugging Face
# HF_TOKEN=hf_...
```

## LiteLLM

### Environment Variables

Create `.env` in `projects/litellm/`:

```bash
# Master Key (optional, for key management)
# LITELLM_MASTER_KEY=sk-1234

# Provider API Keys (set the ones you want to use)

# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google
# GOOGLE_API_KEY=...

# Azure OpenAI
# AZURE_OPENAI_API_KEY=...
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment

# Ollama (local, no API key needed)
# OLLAMA_BASE_URL=http://localhost:11434

# Hugging Face
# HF_TOKEN=hf_...

# Cohere
# COHERE_API_KEY=...

# Database (optional, for usage tracking)
# DATABASE_URL=postgresql://user:password@localhost/litellm

# Proxy Server Configuration
PORT=8000
HOST=0.0.0.0
```

### Configuration File

Use `config.yaml` for advanced configuration:

```yaml
model_list:
  - model_name: gpt-3.5-turbo
    litellm_params:
      model: openai/gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY
```

Start proxy with config:

```bash
litellm --config config.yaml
```

## CrewAI

### Environment Variables

```bash
# LLM Provider (auto-detected if not set)
LLM_PROVIDER=ollama  # or openai, anthropic, google, azure

# Ollama (Free/Local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# OpenAI (Paid)
OPENAI_API_KEY=sk-...
OPENAI_MODEL_NAME=gpt-4o-mini

# Anthropic Claude (Paid)
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Google Gemini (Paid/Free tier)
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-pro

# Azure OpenAI (Paid)
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Other Tools
SERPER_API_KEY=...  # Web search (free tier available)

# System Configuration
VERBOSE=true
PROCESS_TYPE=sequential  # or hierarchical
```

## Terminal Agents

### Environment Variables

```bash
# OpenAI API Key
OPENAI_API_KEY=your_api_key_here
```

Or create `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

## Configuration Best Practices

### 1. Use Environment Files

Always use `.env` files instead of hardcoding values:

```bash
# Good
export OPENAI_API_KEY=sk-...

# Better
echo "OPENAI_API_KEY=sk-..." > .env
```

### 2. Never Commit Secrets

Add `.env` to `.gitignore`:

```gitignore
.env
.env.local
.env.*.local
```

### 3. Use Different Configs for Different Environments

```bash
.env.development
.env.production
.env.test
```

### 4. Validate Configuration

Most projects include validation:

```bash
# CrewAI
python main.py --status

# RAG Model
python -c "from config import config; print(config.validate())"
```

## Common Configuration Patterns

### Local Development

```bash
# Use Ollama for free local LLMs
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

### Production

```bash
# Use cloud providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Testing

```bash
# Use minimal configuration
FLASK_ENV=test
VERBOSE=false
```

## Troubleshooting Configuration

### Variables Not Loading

1. Check file location (should be in project root)
2. Check file name (`.env` or `.env.local`)
3. Restart application after changes
4. Check for typos in variable names

### API Keys Not Working

1. Verify keys are valid
2. Check key has required permissions
3. Ensure keys are set in correct environment
4. Check for extra spaces or quotes

### Port Conflicts

Change ports in configuration:

```bash
# iOS Chatbot
PORT=5001

# LiteLLM Proxy
PORT=8001

# ChatUi (in vite.config.js)
server: { port: 5174 }
```

## Related Documentation

- [Installation Guide](Installation-Guide)
- [Quick Start](Quick-Start)
- [Troubleshooting](Troubleshooting)

