# Quick Start Guide

Get up and running with JJB Gallery projects in minutes.

## 🚀 Fastest Path to Running Projects

### 1. Clone Repository

```bash
git clone https://github.com/Exios66/JJB_Gallery.git
cd JJB_Gallery
```

### 2. Install Dependencies

```bash
cd projects
chmod +x setup_all.sh
./setup_all.sh
```

### 3. Run a Project

Choose any project to start:

#### RAG Model (No API keys needed for basic use)

```bash
cd RAG_Model
python main.py
```

#### Psychometrics (No API keys needed)

```bash
cd Psychometrics
python main.py
```

#### iOS Chatbot (Basic mode - no API keys)

```bash
cd ios_chatbot
python app.py
# Open http://localhost:5000
```

## 📋 Project Quick Starts

### RAG Model

**What it does**: Retrieval-Augmented Generation with vector database

```bash
cd projects/RAG_Model
pip install -r requirements.txt
python main.py
```

**First run**: Creates sample documents and vector store automatically.

### Psychometrics

**What it does**: NASA Task Load Index assessment tool

```bash
cd projects/Psychometrics
pip install -r requirements.txt
python main.py
```

**Usage**: Follow interactive prompts to complete assessment.

### ChatUi

**What it does**: Modern SvelteKit chat interface

```bash
cd projects/ChatUi
npm install
npm run dev
# Open http://localhost:5173
```

**Setup**: Configure API endpoint in `.env.local`

### iOS Chatbot

**What it does**: iOS-inspired chatbot with Flask

```bash
cd projects/ios_chatbot
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

**Setup**: Add API keys to `.env` for LLM integration

### LiteLLM

**What it does**: Unified LLM API proxy server

```bash
cd projects/litellm
pip install -r requirements.txt

# Run examples
python examples.py

# Or start proxy
python proxy_server.py
# Server: http://localhost:8000
```

**Setup**: Add API keys to `.env` for providers you want to use

### CrewAI

**What it does**: Multi-agent system for complex workflows

```bash
cd projects/Crewai
pip install -r requirements.txt
python main.py --setup
python main.py --run ml
```

**Setup**: Configure LLM provider (Ollama recommended for free local use)

## 🔑 API Keys (Optional)

Most projects work without API keys, but you can enhance them:

### For OpenAI

```bash
export OPENAI_API_KEY=sk-...
```

### For Anthropic

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### For Local Models (Ollama)

```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.1:8b
# No API key needed!
```

## ✅ Verify Installation

```bash
cd projects
chmod +x test_all.sh
./test_all.sh
```

## 🎯 Next Steps

1. **Read Project READMEs** - Detailed documentation for each project
2. **Try Examples** - Each project includes example code
3. **Customize** - Adjust configurations for your needs
4. **Integrate** - Connect projects to your systems

## 📚 More Information

- [Installation Guide](Installation-Guide.md) - Detailed setup instructions
- [Configuration Guide](Configuration-Guide.md) - Environment variables and settings
- [Project Overview](Project-Overview.md) - Detailed project descriptions
- [Troubleshooting](Troubleshooting.md) - Common issues and solutions

## 💡 Tips

- **Start Simple**: Begin with projects that don't require API keys (RAG Model, Psychometrics)
- **Use Ollama**: Free local LLMs - no API costs!
- **Read READMEs**: Each project has comprehensive documentation
- **Check Examples**: Look for `examples.py` or example code in project directories

## 🆘 Need Help?

- Check [Troubleshooting](Troubleshooting.md) guide
- Review project-specific README files
- Check GitHub Issues
- Contact: jackburleson.dev@gmail.com

