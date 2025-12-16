# iOS Chatbot

A beautiful, iOS-style chatbot interface built with Flask and vanilla JavaScript. Features a modern, gradient-based design inspired by iOS Messages.

## Overview

This project provides a clean, iOS-inspired chat interface with a Flask backend. It's designed to be easily integrated with various LLM providers for intelligent conversations.

## Features

- ✅ **iOS-Style UI**: Beautiful gradient design inspired by iOS Messages
- ✅ **Responsive Design**: Works on desktop and mobile devices
- ✅ **Real-time Chat**: Instant message sending and receiving
- ✅ **Conversation Management**: Track multiple conversations
- ✅ **RESTful API**: Clean API for integration
- ✅ **Easy LLM Integration**: Simple interface for connecting LLM backends

## Installation

```bash
cd projects/ios_chatbot
pip install -r requirements.txt
```

**Dependencies:**

- Flask
- flask-cors
- python-dotenv

## Quick Start

### Basic Usage

```bash
python app.py
# Open http://localhost:5000
```

### With Environment Variables

```bash
# Create .env file
cat > .env << EOF
FLASK_ENV=development
PORT=5000
SECRET_KEY=your-secret-key
OPENAI_API_KEY=sk-...
EOF

python app.py
```

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

### GET `/api/conversations`

List all conversations.

### DELETE `/api/conversations/<conversation_id>`

Delete a conversation.

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
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content
```

### Ollama

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

### Anthropic Claude

```python
import anthropic

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

class ChatBot:
    def respond(self, message: str, conversation_id: str) -> str:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": message}]
        )
        return response.content[0].text
```

## Customization

### Styling

Modify `static/style.css` to customize:

- Colors and gradients
- Font sizes and families
- Spacing and layout
- Animations

### Backend Logic

Modify `app.py` to:

- Add conversation persistence (database)
- Implement user authentication
- Add message history
- Integrate with external services

## Project Structure

```bash
ios_chatbot/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # iOS-inspired styles
│   └── app.js            # Frontend JavaScript
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```

## Deployment

### Local Development

```bash
export FLASK_ENV=development
python app.py
```

### Production

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `PORT` | Server port | `5000` |
| `SECRET_KEY` | Flask secret key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `OLLAMA_URL` | Ollama server URL | `http://localhost:11434` |

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

## Related Documentation

- [Installation Guide](Installation-Guide)
- [Configuration Guide](Configuration-Guide)
- [API Reference](API-Reference)
