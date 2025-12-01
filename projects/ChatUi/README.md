# ChatUI - Modern Chat Interface

A modern, SvelteKit-based chat interface for interacting with open-source and proprietary language models. This project provides a beautiful, responsive chat UI similar to HuggingChat, with support for multiple LLM providers.

## 🚀 Features

- **Modern UI**: Beautiful, responsive chat interface built with SvelteKit
- **Multiple Model Support**: Works with OpenAI, Anthropic, HuggingFace, and local models
- **MongoDB Integration**: Persistent chat history storage
- **Web Search**: Optional web search integration for enhanced responses
- **Customizable**: Easy theming and configuration

## 📋 Prerequisites

- Node.js 18+ and npm 9+
- MongoDB (local or Atlas instance)
- (Optional) API keys for LLM providers

## 🛠️ Installation

### Quick Setup

1. **Run the setup script:**
   ```bash
   cd projects/ChatUi
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Or manually:**
   ```bash
   npm install
   cp .env.example .env.local  # Edit with your configuration
   ```

### MongoDB Setup

**Option 1: Docker (Recommended)**
```bash
docker run -d -p 27017:27017 --name mongo-chatui mongo:latest
```

**Option 2: MongoDB Atlas**
- Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Create a free cluster
- Get your connection string

## ⚙️ Configuration

Create a `.env.local` file with the following:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017

# Hugging Face Token (optional, for remote models)
HF_TOKEN=your_huggingface_token

# Optional: Web Search API Keys
SERPER_API_KEY=your_serper_key
# OR
YDC_API_KEY=your_you_com_key

# Optional: OpenAI API Key
OPENAI_API_KEY=your_openai_key

# App Configuration
PUBLIC_APP_NAME=ChatUI
PUBLIC_APP_COLOR=blue
PUBLIC_APP_DESCRIPTION="Chat interface for open source models"
```

## 🚀 Usage

### Development Mode

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Production Build

```bash
npm run build
npm run preview
```

## 📚 Model Configuration

Configure models in `.env.local` using the `MODELS` variable:

```env
MODELS=`[
  {
    "name": "mistralai/Mistral-7B-Instruct-v0.2",
    "displayName": "Mistral 7B",
    "description": "Mistral 7B is a new Apache 2.0 model",
    "parameters": {
      "temperature": 0.7,
      "max_new_tokens": 1024
    }
  }
]`
```

### Supported Model Providers

- **HuggingFace**: Direct integration with HuggingFace models
- **OpenAI**: GPT-3.5, GPT-4, and other OpenAI models
- **Anthropic**: Claude models
- **Local Models**: Via llama.cpp, Ollama, or TGI servers

## 🔍 Web Search

Enable web search by adding one of these API keys:

- `SERPER_API_KEY` - [Serper.dev](https://serper.dev) (free tier available)
- `YDC_API_KEY` - [You.com](https://you.com)
- `SERPAPI_KEY` - [SerpAPI](https://serpapi.com)

## 🎨 Customization

### Theming

Customize the app appearance:

```env
PUBLIC_APP_NAME=MyChatApp
PUBLIC_APP_COLOR=purple
PUBLIC_APP_ASSETS=chatui
```

### Colors

Use any [Tailwind color](https://tailwindcss.com/docs/customizing-colors) for `PUBLIC_APP_COLOR`.

## 📦 Project Structure

```
ChatUi/
├── src/              # Source code
├── static/           # Static assets
├── package.json      # Dependencies
├── setup.sh          # Setup script
└── README.md         # This file
```

## 🧪 Testing

```bash
npm run test          # Run all tests
npm run test:unit     # Unit tests
npm run test:integration  # Integration tests
```

## 📖 Documentation

For detailed documentation, see:
- [HuggingFace ChatUI Docs](https://huggingface.co/docs/chat-ui)
- [SvelteKit Docs](https://kit.svelte.dev/docs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of the JJB Gallery portfolio. See the main repository LICENSE file.

## 🔗 Related Projects

- [CrewAI Multi-Agent System](../Crewai/README.md)
- [RAG Model](../RAG_Model/README.md)
- [Terminal Agents](../terminal_agents/README.md)
