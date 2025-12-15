# Projects Overview

This directory contains multiple AI and ML projects, each with its own implementation and documentation.

## Available Projects

### 🤖 [RAG_Model](./RAG_Model/)
Retrieval-Augmented Generation system with vector database, embeddings, and intelligent document retrieval.

**Quick Start:**
```bash
cd RAG_Model
pip install -r requirements.txt
python main.py
```

### 📊 [Psychometrics](./Psychometrics/)
NASA Task Load Index (TLX) assessment tool for measuring workload and cognitive demand.

**Quick Start:**
```bash
cd Psychometrics
pip install -r requirements.txt
python main.py
```

### 💬 [ChatUi](./ChatUi/)
Modern SvelteKit chat interface for interacting with LLM models.

**Quick Start:**
```bash
cd ChatUi
npm install
npm run dev
```

### 📱 [ios_chatbot](./ios_chatbot/)
iOS-inspired chatbot with Flask backend and beautiful gradient UI.

**Quick Start:**
```bash
cd ios_chatbot
pip install -r requirements.txt
python app.py
```

### 🔌 [litellm](./litellm/)
LiteLLM integration with proxy server for unified LLM API access.

**Quick Start:**
```bash
cd litellm
pip install -r requirements.txt
python proxy_server.py
```

### 🤝 [CrewAI](./Crewai/)
Multi-agent system using CrewAI for complex workflows and task automation.

**Quick Start:**
```bash
cd Crewai
pip install -r requirements.txt
python main.py --setup
```

### ⌨️ [terminal_agents](./terminal_agents/)
AI coding agents for the terminal, similar to OpenCode.

## Setup

### Quick Setup (All Projects)

```bash
# Install all dependencies
chmod +x setup_all.sh
./setup_all.sh
```

### Individual Setup

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed instructions.

## Testing

### Test All Projects

```bash
chmod +x test_all.sh
./test_all.sh
```

### Test Individual Projects

See each project's README for specific testing instructions.

## Documentation

- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Complete setup instructions
- **[QUICK_START.md](./QUICK_START.md)** - Quick start guide
- Each project has its own README with detailed documentation

## Requirements

- Python 3.8+
- Node.js 18+ (for ChatUi)
- pip and npm

## Optional Dependencies

- Ollama (for local LLM models)
- MongoDB (for ChatUi chat history)
- API Keys (OpenAI, Anthropic, etc.)

## Project Status

| Project | Status | Dependencies | API Keys Required |
|---------|--------|--------------|-------------------|
| RAG_Model | ✅ Complete | Python | Optional |
| Psychometrics | ✅ Complete | Python | No |
| ChatUi | ✅ Complete | Node.js | Optional |
| ios_chatbot | ✅ Complete | Python | Optional |
| litellm | ✅ Complete | Python | Optional |
| CrewAI | ✅ Complete | Python | Yes |
| terminal_agents | ✅ Complete | Python | Yes |

## Getting Started

1. **Read [SETUP_GUIDE.md](./SETUP_GUIDE.md)** for detailed setup instructions
2. **Choose a project** that interests you
3. **Follow the project's README** for specific instructions
4. **Set up environment variables** as needed
5. **Test the project** to ensure it works

## Contributing

Each project is self-contained. To contribute:

1. Read the project's README
2. Follow the project's coding standards
3. Test your changes
4. Update documentation as needed

## Support

For issues or questions:

1. Check the project's README
2. Review [SETUP_GUIDE.md](./SETUP_GUIDE.md)
3. Check the main repository documentation

## License

See the main repository LICENSE file.

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>

