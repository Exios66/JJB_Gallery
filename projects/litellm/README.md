# LiteLLM Proxy Server

A unified proxy server for multiple LLM providers using LiteLLM. This server provides a single OpenAI-compatible API endpoint that can route requests to various LLM providers including OpenAI, Anthropic, Google, Azure, Cohere, and HuggingFace.

## 🚀 Features

- **Unified API**: Single OpenAI-compatible endpoint for all providers
- **Multi-Provider Support**: OpenAI, Anthropic, Google, Azure, Cohere, HuggingFace
- **Automatic Routing**: Automatically routes to configured providers
- **Streaming Support**: Full streaming response support
- **Cost Tracking**: Built-in cost tracking and usage monitoring
- **FastAPI**: Modern, fast API built with FastAPI
- **Easy Configuration**: Simple environment variable configuration

## 📋 Prerequisites

- Python 3.8+
- API keys for desired LLM providers

## 🛠️ Installation

### Quick Setup

1. **Clone and navigate:**
   ```bash
   cd projects/litellm
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the server:**
   ```bash
   python proxy_server.py
   ```

   Or use the startup script:
   ```bash
   chmod +x run_server.sh
   ./run_server.sh
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with your API keys:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_api_key_here
AZURE_OPENAI_API_BASE=https://your-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Cohere Configuration
COHERE_API_KEY=your_cohere_api_key_here

# HuggingFace Configuration
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# LiteLLM Settings
LITELLM_VERBOSE=false
```

### Supported Providers

| Provider | Environment Variable | Status |
|----------|---------------------|--------|
| OpenAI | `OPENAI_API_KEY` | ✅ |
| Anthropic | `ANTHROPIC_API_KEY` | ✅ |
| Google | `GOOGLE_API_KEY` | ✅ |
| Azure OpenAI | `AZURE_OPENAI_API_KEY` | ✅ |
| Cohere | `COHERE_API_KEY` | ✅ |
| HuggingFace | `HUGGINGFACE_API_KEY` | ✅ |

## 🚀 Usage

### Starting the Server

```bash
# Basic usage
python proxy_server.py

# With custom host/port
python proxy_server.py --host 0.0.0.0 --port 8000

# With auto-reload (development)
python proxy_server.py --reload
```

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### List Models
```bash
curl http://localhost:8000/v1/models
```

#### Chat Completions
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### Python Client Example

```python
import openai

client = openai.OpenAI(
    api_key="anything",  # Can be any value
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### Streaming Example

```python
import openai

client = openai.OpenAI(
    api_key="anything",
    base_url="http://localhost:8000/v1"
)

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔧 Advanced Configuration

### Model Routing

LiteLLM automatically routes based on the model name:

- `gpt-*` → OpenAI
- `claude-*` → Anthropic
- `gemini-*` → Google
- `command-*` → Cohere

### Custom Model Mapping

You can configure custom model mappings in the code:

```python
# In proxy_server.py
litellm.model_alias_map = {
    "my-custom-model": "gpt-3.5-turbo"
}
```

## 🐛 Troubleshooting

### Connection Issues

- Verify API keys are correctly set
- Check network connectivity
- Ensure provider APIs are accessible

### Model Not Found

- Check model name spelling
- Verify provider supports the model
- Check API key permissions

### Rate Limiting

- Implement retry logic in your client
- Use multiple API keys for load balancing
- Monitor usage through LiteLLM's logging

## 📊 Monitoring

### Enable Verbose Logging

```env
LITELLM_VERBOSE=true
```

### Cost Tracking

LiteLLM automatically tracks costs. View logs for cost information.

## 🔒 Security

- Never commit `.env` files
- Use environment variables in production
- Implement authentication for production deployments
- Consider rate limiting for public APIs

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "proxy_server.py", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

- Use a reverse proxy (nginx, Caddy)
- Implement authentication
- Set up monitoring and logging
- Configure rate limiting
- Use environment variables for secrets

## 📦 Project Structure

```
litellm/
├── proxy_server.py     # Main FastAPI server
├── requirements.txt    # Python dependencies
├── .env.example       # Environment template
├── run_server.sh      # Startup script
└── README.md          # This file
```

## 🔗 Related Projects

- [CrewAI](../Crewai/README.md) - Multi-agent system using LiteLLM
- [ChatUI](../ChatUi/README.md) - Chat interface
- [RAG Model](../RAG_Model/README.md) - Document Q&A system

## 📄 License

This project is part of the JJB Gallery portfolio. See the main repository LICENSE file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
