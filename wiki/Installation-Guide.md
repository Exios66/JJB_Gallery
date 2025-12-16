# Installation Guide

Complete guide for installing and setting up all projects in the JJB Gallery repository.

## Prerequisites

### Required Software

- **Python 3.8+** with pip
- **Node.js 18+** with npm (for ChatUi project)
- **Git** for cloning the repository

### Optional Software

- **Ollama** - For local LLM models ([Download](https://ollama.ai))
- **MongoDB** - For ChatUi chat history (Docker or Atlas)
- **Docker** - For containerized services

## Quick Installation

### Automated Setup

```bash
# Clone the repository
git clone https://github.com/Exios66/JJB_Gallery.git
cd JJB_Gallery/projects

# Run automated setup script
chmod +x setup_all.sh
./setup_all.sh
```

This script will:

- Install all Python dependencies
- Install Node.js dependencies for ChatUi
- Verify installations

### Manual Installation

#### 1. Python Projects

```bash
# RAG Model
cd projects/RAG_Model
pip install -r requirements.txt

# Psychometrics
cd ../Psychometrics
pip install -r requirements.txt

# iOS Chatbot
cd ../ios_chatbot
pip install -r requirements.txt

# LiteLLM
cd ../litellm
pip install -r requirements.txt

# CrewAI
cd ../Crewai
pip install -r requirements.txt
```

#### 2. Node.js Projects

```bash
# ChatUi
cd projects/ChatUi
npm install
```

## Project-Specific Installation

### RAG Model

```bash
cd projects/RAG_Model
pip install -r requirements.txt

# Verify installation
python -c "from rag_system import RAGSystem; print('✓ RAG System installed')"
```

**Dependencies:**

- langchain
- faiss-cpu (or faiss-gpu for GPU support)
- sentence-transformers
- numpy
- torch

### Psychometrics

```bash
cd projects/Psychometrics
pip install -r requirements.txt

# Verify installation
python -c "from nasa_tlx import NASATLX; print('✓ NASA TLX installed')"
```

**Dependencies:**

- Standard library only (numpy, pandas optional for advanced analysis)

### ChatUi

```bash
cd projects/ChatUi
npm install

# Verify installation
npm run check
```

**Dependencies:**

- @sveltejs/kit
- @huggingface/inference
- mongodb
- openai

### iOS Chatbot

```bash
cd projects/ios_chatbot
pip install -r requirements.txt

# Verify installation
python -c "import app; print('✓ Flask app installed')"
```

**Dependencies:**

- Flask
- flask-cors
- python-dotenv

### LiteLLM

```bash
cd projects/litellm
pip install -r requirements.txt

# Verify installation
python -c "from litellm import completion; print('✓ LiteLLM installed')"
```

**Dependencies:**

- litellm
- fastapi
- uvicorn
- pydantic

### CrewAI

```bash
cd projects/Crewai
pip install -r requirements.txt

# Verify installation
python main.py --status
```

**Dependencies:**

- crewai
- crewai-tools
- streamlit
- pydantic

## Optional Dependencies

### Ollama (Local LLMs)

```bash
# Install Ollama from https://ollama.ai
# Then pull models:
ollama pull llama3.1:8b
ollama pull mistral:7b
```

### MongoDB (for ChatUi)

#### Option 1: Docker

```bash
docker run -d -p 27017:27017 --name mongo-chatui mongo:latest
```

#### Option 2: MongoDB Atlas

1. Sign up at [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Create a free cluster
3. Get connection string

## Environment Setup

### Create Environment Files

Each project may require environment variables. See [Configuration Guide](Configuration-Guide) for details.

**Quick setup:**

```bash
# RAG Model
cd projects/RAG_Model
cp .env.example .env  # Edit with your settings

# iOS Chatbot
cd ../ios_chatbot
cp .env.example .env  # Add API keys

# LiteLLM
cd ../litellm
cp .env.example .env  # Add API keys
```

## Verification

### Test All Installations

```bash
cd projects
chmod +x test_all.sh
./test_all.sh
```

### Individual Project Tests

```bash
# RAG Model
cd RAG_Model && python -c "from rag_system import RAGSystem; print('OK')"

# Psychometrics
cd ../Psychometrics && python -c "from nasa_tlx import NASATLX; print('OK')"

# ChatUi
cd ../ChatUi && npm run check

# iOS Chatbot
cd ../ios_chatbot && python -c "import app; print('OK')"

# LiteLLM
cd ../litellm && python -c "from litellm import completion; print('OK')"
```

## Troubleshooting

### Common Issues

#### Python Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Node.js Issues

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Port Conflicts

If ports are already in use:

- Change port in `.env` files
- Or kill existing processes:

  ```bash
  lsof -i :5000  # Find process
  kill -9 <PID>   # Kill process
  ```

## Next Steps

After installation:

1. **Configure Environment Variables** - See [Configuration Guide](Configuration-Guide)
2. **Read Project READMEs** - Each project has detailed documentation
3. **Run Examples** - Test each project with provided examples
4. **Set Up API Keys** - Add keys for cloud LLM providers (if needed)

## Additional Resources

- [Quick Start Guide](Quick-Start)
- [Configuration Guide](Configuration-Guide)
- [Troubleshooting](Troubleshooting)
- [Development Setup](Development-Setup)
