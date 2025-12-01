# LiteLLM Integration

A comprehensive integration of LiteLLM for unified LLM API access. Includes a proxy server, usage examples, and configuration templates.

## Overview

LiteLLM is a library that provides a unified interface for calling various LLM APIs (OpenAI, Anthropic, Google, Ollama, etc.) using the OpenAI format. This project includes:

- **Proxy Server**: FastAPI-based proxy server for LLM requests
- **Usage Examples**: Comprehensive examples for different providers
- **Configuration**: YAML configuration for model management

## Features

- ✅ **Unified API**: Call any LLM provider using OpenAI-compatible format
- ✅ **Multiple Providers**: Support for 100+ LLM providers
- ✅ **Proxy Server**: HTTP proxy for centralized LLM access
- ✅ **Streaming Support**: Real-time streaming responses
- ✅ **Async Support**: Asynchronous API calls
- ✅ **Easy Configuration**: YAML-based configuration

## Installation

### Basic Installation

```bash
cd projects/litellm
pip install -r requirements.txt
```

### With Proxy Extras

```bash
pip install 'litellm[proxy]'
```

## Quick Start

### 1. Basic Usage

```python
from litellm import completion

response = completion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

### 2. Run Proxy Server

```bash
python proxy_server.py
# Server runs on http://localhost:8000
```

### 3. Use Proxy Server

```python
import openai

client = openai.OpenAI(
    api_key="anything",
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Usage Examples

### OpenAI

```python
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "your-key"

response = completion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Anthropic Claude

```python
os.environ["ANTHROPIC_API_KEY"] = "your-key"

response = completion(
    model="claude-3-sonnet-20240229",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Ollama (Local)

```python
# Make sure Ollama is running: ollama serve
# Pull a model: ollama pull llama3.1:8b

response = completion(
    model="ollama/llama3.1:8b",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Streaming

```python
response = completion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Count to 10"}],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Async

```python
from litellm import acompletion
import asyncio

async def main():
    response = await acompletion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

## Proxy Server

### Starting the Server

```bash
python proxy_server.py
```

Or with custom port:

```bash
PORT=8080 python proxy_server.py
```

### API Endpoints

#### POST `/v1/chat/completions`

OpenAI-compatible chat completions endpoint.

**Request:**
```json
{
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": "Hello!"}],
  "temperature": 0.7,
  "stream": false
}
```

#### GET `/models`

List available models.

#### GET `/health`

Health check endpoint.

### Using the Proxy

#### Python

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

#### cURL

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Configuration

### Environment Variables

Set API keys as environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
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

## Supported Providers

LiteLLM supports 100+ LLM providers. Common ones include:

- **OpenAI**: GPT-3.5, GPT-4, GPT-4 Turbo
- **Anthropic**: Claude 3 (Sonnet, Opus, Haiku)
- **Google**: Gemini Pro, PaLM
- **Ollama**: Local models (Llama, Mistral, etc.)
- **Azure OpenAI**: Azure-hosted OpenAI models
- **Hugging Face**: Transformers models
- **Cohere**: Command models
- **Together AI**: Various open models

See [LiteLLM Documentation](https://docs.litellm.ai/docs/providers) for full list.

## Advanced Features

### Router (Load Balancing)

```python
from litellm import Router

router = Router(
    model_list=[
        {"model_name": "gpt-3.5-turbo", "litellm_params": {"model": "openai/gpt-3.5-turbo"}},
        {"model_name": "claude-3-sonnet", "litellm_params": {"model": "anthropic/claude-3-sonnet-20240229"}},
    ]
)

response = router.completion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Fallbacks

```python
response = completion(
    model=["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"],  # Try in order
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Troubleshooting

### Import Errors

```bash
pip install litellm
```

### API Key Issues

Ensure API keys are set:

```bash
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
```

### Ollama Connection

Check if Ollama is running:

```bash
curl http://localhost:11434/api/tags
```

Start Ollama:

```bash
ollama serve
```

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- [Supported Providers](https://docs.litellm.ai/docs/providers)
- [Proxy Documentation](https://docs.litellm.ai/docs/simple_proxy)

## Related Documentation

- [Installation Guide](Installation-Guide)
- [Configuration Guide](Configuration-Guide)
- [API Reference](API-Reference)

