# LiteLLM Integration

A comprehensive integration of LiteLLM for unified LLM API access. Includes a proxy server, usage examples, and configuration templates.

## Overview

LiteLLM is a library that provides a unified interface for calling various LLM APIs (OpenAI, Anthropic, Google, Ollama, etc.) using the OpenAI format. This project includes:

- **Proxy Server**: FastAPI-based proxy server for LLM requests
- **Usage Examples**: Comprehensive examples for different providers
- **Configuration**: YAML configuration for model management

## Features

- **Unified API**: Call any LLM provider using OpenAI-compatible format
- **Multiple Providers**: Support for OpenAI, Anthropic, Google, Ollama, and more
- **Proxy Server**: HTTP proxy for centralized LLM access
- **Streaming Support**: Real-time streaming responses
- **Async Support**: Asynchronous API calls
- **Easy Configuration**: YAML-based configuration

## Installation

### Basic Installation

```bash
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
```

The server will start on `http://localhost:8000`.

## 🏭 Production Deployment

### Deployment Strategy

For high-throughput environments, deploy the LiteLLM Proxy as a scalable microservice.

### Docker Deployment

1. **Dockerfile**:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN pip install 'litellm[proxy]'
COPY config.yaml .
CMD ["litellm", "--config", "config.yaml", "--port", "8000", "--host", "0.0.0.0"]
```

2. **Run Container**:

```bash
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  -v $(pwd)/config.yaml:/app/config.yaml \
  litellm-proxy:latest
```

### Scaling & Load Balancing

- **Horizontal Scaling**: Run multiple instances behind a load balancer (Nginx, AWS ALB). LiteLLM Proxy is stateless.
- **Internal Load Balancing**: Configure LiteLLM's `Router` to balance traffic across multiple API keys or deployments (e.g., multiple Azure deployments).

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4-east
      api_base: https://east-us.api.cognitive.microsoft.com/
      api_key: env/AZURE_KEY_1
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4-west
      api_base: https://west-us.api.cognitive.microsoft.com/
      api_key: env/AZURE_KEY_2
```

### Cost Monitoring & Control

- **Budgeting**: Set monthly budgets per user or key in `config.yaml`.
- **Database**: Connect a PostgreSQL database to track spend and usage logs.

```bash
# Set DATABASE_URL environment variable
export DATABASE_URL="postgresql://user:pass@db:5432/litellm"
```

### Observability

- **Logging**: Configure callbacks for LangFuse, Helicone, or custom logging.
- **Metrics**: Expose Prometheus metrics at `/metrics` to monitor latency, error rates, and request volume.

### Production Readiness Checklist

- [ ] **Rate Limiting**: Configured per user/key to prevent abuse.
- [ ] **Failover**: Configured fallbacks (e.g., Azure -> OpenAI) for high availability.
- [ ] **Caching**: Redis caching enabled for frequent queries.
- [ ] **Security**: API Master Key configured for admin endpoints.

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

### API Key Issues
Ensure API keys are set:
```bash
echo $OPENAI_API_KEY
```

### Ollama Connection
Check if Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

## License

See main repository LICENSE file.

## Related Projects

- [RAG Model](../RAG_Model/README.md) - Retrieval-Augmented Generation
- [ChatUi](../ChatUi/README.md) - Modern Chat Interface
- [iOS Chatbot](../ios_chatbot/README.md) - Flask-based Chatbot
- [CrewAI](../CrewAI/README.md) - Multi-Agent System

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
