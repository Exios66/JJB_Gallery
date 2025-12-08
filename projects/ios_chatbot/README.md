# iOS-Inspired Chatbot

A beautiful, iOS-style chatbot interface built with Flask and vanilla JavaScript. Features a modern, gradient-based design inspired by iOS Messages.

## Overview

This project provides a clean, iOS-inspired chat interface with a Flask backend. It's designed to be easily integrated with various LLM providers for intelligent conversations.

## Features

- **iOS-Style UI**: Beautiful gradient design inspired by iOS Messages
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Chat**: Instant message sending and receiving
- **Conversation Management**: Track multiple conversations
- **RESTful API**: Clean API for integration
- **Easy LLM Integration**: Simple interface for connecting LLM backends

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. (Optional) Set environment variables:

```bash
export FLASK_ENV=development
export PORT=5000
export SECRET_KEY=your-secret-key-here
```

3. Run the application:

```bash
python app.py
```

The application will be available at `http://localhost:5000`.

## Usage

### Basic Usage

1. Start the server:

```bash
python app.py
```

2. Open your browser to `http://localhost:5000`

3. Start chatting!

## 🏭 Production Deployment

### Deployment Strategy

For production, do NOT use the built-in Flask server. Instead, use a WSGI server like Gunicorn behind a reverse proxy (Nginx).

### Docker Deployment

1. **Dockerfile**:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
```

2. **Run Container**:

```bash
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=prod-secret-key \
  ios-chatbot:latest
```

### WSGI Configuration

We recommend **Gunicorn** for production.

**Configuration (`gunicorn_config.py`):**

```python
workers = 4
bind = "0.0.0.0:5000"
accesslog = "-"
errorlog = "-"
loglevel = "info"
timeout = 120
```

Run with config: `gunicorn -c gunicorn_config.py app:app`

### Database Setup

For production, replace in-memory or SQLite storage with **PostgreSQL**.

1. Install driver: `pip install psycopg2-binary`
2. Configure `SQLALCHEMY_DATABASE_URI` in `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/db')
```

### WebSocket Scaling

If using Flask-SocketIO:

1. Use **Redis** as a message queue to sync state across multiple Gunicorn workers.
2. Enable sticky sessions in your load balancer (Nginx/HAProxy) to ensure client connection persistence.

### Security Headers

In production, ensure Nginx or your application sets security headers:

- `Strict-Transport-Security` (HSTS)
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`

### Monitoring

- **Application Logs**: Stream logs to stdout for Docker logging drivers.
- **Uptime Monitoring**: Check `/api/health` endpoint.
- **Performance**: Use New Relic or Datadog APM agents for Python.

## API Endpoints

### POST `/api/chat`

Send a chat message and get a response.

**Request:**

```json
{
  "message": "Hello, how are you?",
  "conversation_id": "optional-conversation-id"
}
```

**Response:**

```json
{
  "conversation_id": "uuid-here",
  "response": {
    "role": "assistant",
    "content": "Hello! How can I help you?",
    "timestamp": "2024-01-15T10:30:00"
  },
  "message": {
    "role": "user",
    "content": "Hello, how are you?",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

### GET `/api/conversations/<conversation_id>`

Get conversation history.

### GET `/api/health`

Health check endpoint.

## Integrating LLM Providers

### OpenAI

Update `app.py`:

```python
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

class ChatBot:
    def respond(self, message: str, conversation_id: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
```

### Ollama

Update `app.py`:

```python
import requests

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')

class ChatBot:
    def respond(self, message: str, conversation_id: str) -> str:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": message,
                "stream": False
            }
        )
        return response.json()['response']
```

## Troubleshooting

### Port Already in Use

Change the port:

```bash
export PORT=5001
python app.py
```

### CORS Issues

CORS is enabled by default. If you need to restrict origins, update `app.py`:

```python
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

## License

See main repository LICENSE file.

## Related Projects

- [ChatUi](../ChatUi/README.md) - Modern SvelteKit Chat Interface
- [LiteLLM](../litellm/README.md) - Unified LLM API
- [RAG Model](../RAG_Model/README.md) - Retrieval-Augmented Generation
- [CrewAI](../CrewAI/README.md) - Multi-Agent System

## Contributing

Contributions welcome! Please see the main repository [Contributing Guidelines](https://github.com/Exios66/JJB_Gallery/wiki/Contributing-Guidelines).

For issues, questions, or suggestions, please use the [GitHub Issues](https://github.com/Exios66/JJB_Gallery/issues) page.
