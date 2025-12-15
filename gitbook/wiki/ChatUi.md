# ChatUi

A modern, open-source chat interface for interacting with LLM models. Built with SvelteKit, this application provides a clean and intuitive interface for chat-based AI interactions.

## Overview

ChatUi is a SvelteKit application that provides a web-based interface for chatting with various LLM models. It supports multiple backends including OpenAI, Ollama, Hugging Face, and custom API endpoints.

## Features

- ✅ **Modern UI**: Clean, responsive chat interface
- ✅ **Multiple Model Support**: Connect to various LLM providers
- ✅ **Real-time Streaming**: Support for streaming responses
- ✅ **Message History**: Persistent chat history (with MongoDB)
- ✅ **Customizable**: Easy to customize and extend
- ✅ **TypeScript Support**: Type-safe development

## Installation

```bash
cd projects/ChatUi
npm install
```

## Quick Start

### Development

```bash
npm run dev
# Opens at http://localhost:5173
```

### Production Build

```bash
npm run build
npm run preview
```

## Configuration

### Environment Variables

Create `.env.local`:

```env
VITE_API_BASE_URL=http://localhost:3000
MONGODB_URL=mongodb://localhost:27017/chatui
HF_TOKEN=your_huggingface_token
OPENAI_API_KEY=your_openai_key
OLLAMA_BASE_URL=http://localhost:11434
```

### Connecting to LLM Backends

#### OpenAI

```javascript
// src/routes/api/chat/+server.js
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

export async function POST({ request }) {
  const { message } = await request.json();
  
  const completion = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: message }]
  });
  
  return json({
    role: 'assistant',
    content: completion.choices[0].message.content
  });
}
```

#### Ollama

```javascript
export async function POST({ request }) {
  const { message, model = 'llama3.1:8b' } = await request.json();
  
  const response = await fetch(`${process.env.OLLAMA_BASE_URL}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model,
      prompt: message,
      stream: false
    })
  });
  
  const data = await response.json();
  return json({
    role: 'assistant',
    content: data.response
  });
}
```

## Project Structure

```
ChatUi/
├── src/
│   ├── components/        # Svelte components
│   │   └── ChatInterface.svelte
│   ├── lib/               # Utilities and libraries
│   │   └── api.js         # API client
│   ├── routes/           # SvelteKit routes
│   │   ├── api/          # API endpoints
│   │   │   └── chat/     # Chat API
│   │   └── +page.svelte  # Main page
│   └── app.html          # HTML template
├── static/               # Static assets
├── package.json
├── svelte.config.js
└── vite.config.js
```

## Components

### ChatInterface

The main chat component that handles:
- Message display
- User input
- Message sending
- Loading states
- Typing indicators

### API Client

Located in `src/lib/api.js`, provides:
- `sendMessage()`: Send a message and get response
- `streamMessage()`: Stream responses in real-time
- `getModels()`: Fetch available models

## API Endpoints

### POST `/api/chat`

Send a chat message and get a response.

**Request:**
```json
{
  "message": "Hello, how are you?",
  "model": "gpt-3.5-turbo",
  "temperature": 0.7
}
```

**Response:**
```json
{
  "role": "assistant",
  "content": "I'm doing well, thank you!",
  "timestamp": "2024-01-15T10:30:00Z",
  "model": "gpt-3.5-turbo"
}
```

## Customization

### Styling

Modify styles in component `<style>` blocks or create a global stylesheet in `src/app.css`.

### Adding Features

1. **New Components**: Add to `src/components/`
2. **API Routes**: Add to `src/routes/api/`
3. **Utilities**: Add to `src/lib/`

## Deployment

### Vercel

```bash
npm install -g vercel
vercel
```

### Netlify

```bash
npm install -g netlify-cli
netlify deploy
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["node", "build"]
```

## Troubleshooting

### Port Already in Use

Change the port in `vite.config.js`:

```javascript
server: {
  port: 5174
}
```

### MongoDB Connection Issues

Ensure MongoDB is running:

```bash
docker run -d -p 27017:27017 --name mongo mongo:latest
```

### API Errors

Check browser console and server logs for detailed error messages. Ensure your API keys are correctly set in `.env.local`.

## Related Documentation

- [Installation Guide](Installation-Guide.md)
- [Configuration Guide](Configuration-Guide.md)
- [API Reference](API-Reference.md)

