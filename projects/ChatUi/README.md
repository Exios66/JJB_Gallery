# Chat UI

A modern, open-source chat interface for interacting with LLM models. Built with SvelteKit, this application provides a clean and intuitive interface for chat-based AI interactions.

## Overview

Chat UI is a SvelteKit application that provides a web-based interface for chatting with various LLM models. It supports multiple backends including OpenAI, Ollama, Hugging Face, and custom API endpoints.

## Features

- **Modern UI**: Clean, responsive chat interface
- **Multiple Model Support**: Connect to various LLM providers
- **Real-time Streaming**: Support for streaming responses
- **Message History**: Persistent chat history (with MongoDB)
- **Customizable**: Easy to customize and extend
- **TypeScript Support**: Type-safe development

## Installation

### Prerequisites

- Node.js 18+ and npm 9+
- MongoDB (for chat history, optional)

### Setup

1. Install dependencies:

```bash
npm install
```

2. Copy environment variables:

```bash
cp .env.example .env.local
```

3. Create a `.env.local` file and configure your environment variables:

```env
VITE_API_BASE_URL=http://localhost:3000
MONGODB_URL=mongodb://localhost:27017/chatui
HF_TOKEN=your_huggingface_token
OPENAI_API_KEY=your_openai_key
OLLAMA_BASE_URL=http://localhost:11434
```

4. Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

## Usage

### Development

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

## 🏭 Production Deployment

### 1. Docker Deployment (Recommended)

Build and run the Docker container:

```bash
# Build
docker build -t chatui:latest .

# Run
docker run -d \
  -p 3000:3000 \
  --env-file .env.production \
  --name chatui \
  chatui:latest
```

### 2. Vercel Deployment

ChatUi is optimized for Vercel deployment:

1. Install Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel`
3. Set environment variables in the Vercel dashboard.

### 3. Node.js Hosting (PM2)

For VPS deployment (DigitalOcean, EC2):

```bash
npm run build
pm2 start build/index.js --name "chatui"
```

### WebSocket Scaling

To scale WebSocket connections across multiple instances:

1. **Redis Adapter**: Use Redis to broadcast events between instances.
2. **Sticky Sessions**: Configure your load balancer (Nginx/HAProxy) to use IP-hash or sticky sessions to ensure a client stays connected to the same server.

### CDN Configuration

Serve static assets (`_app/immutable/`) via a CDN (Cloudflare/CloudFront) by configuring `svelte.config.js`:

```javascript
kit: {
  paths: {
    assets: 'https://cdn.yourdomain.com'
  }
}
```

### Performance Optimization

- **Tree Shaking**: Enabled by default in Vite build.
- **Image Optimization**: Use `@sveltejs/enhanced-img`.
- **Lazy Loading**: Code-split routes are automatically lazy-loaded.

### Monitoring

- **Error Tracking**: Integrate Sentry in `hooks.server.js`.
- **Performance**: Monitor Core Web Vitals using Vercel Analytics or Google Analytics.
- **Server Metrics**: Monitor CPU/RAM usage of the Node.js process.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Base URL for API | `http://localhost:3000` |
| `MONGODB_URL` | MongoDB connection string | - |
| `HF_TOKEN` | Hugging Face API token | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `ORIGIN` | Allowed origin for CORS | `http://localhost:3000` |

## Connecting to LLM Backends

### OpenAI

Set your OpenAI API key in `.env.local`:

```env
OPENAI_API_KEY=sk-...
```

### Ollama

Set Ollama base URL:

```env
OLLAMA_BASE_URL=http://localhost:11434
```

### Hugging Face

Set your Hugging Face token:

```env
HF_TOKEN=hf_...
```

## Project Structure

```bash
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
├── vite.config.js
└── README.md
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

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to Netlify

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

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Base URL for API | `http://localhost:3000` |
| `MONGODB_URL` | MongoDB connection string | - |
| `HF_TOKEN` | Hugging Face API token | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |

## Troubleshooting

### Port Already in Use

Change the port in `vite.config.js`:

```javascript
server: {
  port: 5174  // Use different port
}
```

### MongoDB Connection Issues

Ensure MongoDB is running:

```bash
# Using Docker
docker run -d -p 27017:27017 --name mongo mongo:latest

# Or check if already running
docker ps | grep mongo
```

### API Errors

Check browser console and server logs for detailed error messages. Ensure your API keys are correctly set in `.env.local`.

## Related Projects

- [iOS Chatbot](../ios_chatbot/README.md) - Flask-based Chatbot
- [LiteLLM](../litellm/README.md) - Unified LLM API
- [RAG Model](../RAG_Model/README.md) - Retrieval-Augmented Generation
- [CrewAI](../CrewAI/README.md) - Multi-Agent System

## Additional Resources

- 📚 [Project Wiki](https://github.com/Exios66/JJB_Gallery/wiki) - Comprehensive documentation
- 📖 [ChatUi Wiki Page](https://github.com/Exios66/JJB_Gallery/wiki/ChatUi) - Detailed project documentation
- 🔧 [Development Setup](https://github.com/Exios66/JJB_Gallery/wiki/Development-Setup) - Development environment setup
- 🐛 [Troubleshooting](https://github.com/Exios66/JJB_Gallery/wiki/Troubleshooting) - Common issues and solutions

## Contributing

Contributions welcome! Please see the main repository [Contributing Guidelines](https://github.com/Exios66/JJB_Gallery/wiki/Contributing-Guidelines).

For issues, questions, or suggestions, please use the [GitHub Issues](https://github.com/Exios66/JJB_Gallery/issues) page.

## License

See main repository LICENSE file.

## References

- [SvelteKit Documentation](https://kit.svelte.dev/)
- [Svelte Documentation](https://svelte.dev/)
- [Chat UI by Hugging Face](https://github.com/huggingface/chat-ui)

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
