# Complete Setup Guide

This guide provides step-by-step instructions for setting up and testing all projects.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Setup](#quick-setup)
3. [Individual Project Setup](#individual-project-setup)
4. [Environment Variables](#environment-variables)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required

- **Python 3.8+** with pip
- **Node.js 18+** with npm (for ChatUi project)
- **Git**

### Optional (for enhanced functionality)

- **Ollama** - For local LLM models ([Install](https://ollama.ai))
- **MongoDB** - For ChatUi chat history (Docker or Atlas)
- **API Keys** - OpenAI, Anthropic, etc. (depending on which projects you use)

## Quick Setup

### Automated Setup Script

```bash
cd projects
chmod +x setup_all.sh
./setup_all.sh
```

This will install all dependencies for all projects.

### Manual Setup

If you prefer to set up projects individually, see [Individual Project Setup](#individual-project-setup) below.

## Individual Project Setup

### 1. RAG_Model

```bash
cd projects/RAG_Model

# Install dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
RAG_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RAG_VECTOR_STORE_PATH=vector_store
RAG_LLM_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200
RAG_DEFAULT_K=5
EOF

# Test
python -c "from rag_system import RAGSystem; print('✓ RAG System ready')"

# Run
python main.py
```

### 2. Psychometrics

```bash
cd projects/Psychometrics

# Install dependencies
pip install -r requirements.txt

# Test
python -c "from nasa_tlx import NASATLX; print('✓ NASA TLX ready')"

# Run
python main.py
```

**Note:** Psychometrics doesn't require API keys - it's a standalone assessment tool.

### 3. ChatUi

```bash
cd projects/ChatUi

# Install dependencies
npm install

# Create environment file
cat > .env.local << EOF
VITE_API_BASE_URL=http://localhost:3000
MONGODB_URL=mongodb://localhost:27017/chatui
HF_TOKEN=
OPENAI_API_KEY=
OLLAMA_BASE_URL=http://localhost:11434
EOF

# Test
npm run check

# Run development server
npm run dev
# Opens at http://localhost:5173
```

### 4. ios_chatbot

```bash
cd projects/ios_chatbot

# Install dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
FLASK_ENV=development
PORT=5000
SECRET_KEY=dev-secret-key-change-in-production
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
OLLAMA_URL=http://localhost:11434
EOF

# Test
python -c "import app; print('✓ Flask app ready')"

# Run
python app.py
# Opens at http://localhost:5000
```

### 5. litellm

```bash
cd projects/litellm

# Install dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
PORT=8000
HOST=0.0.0.0
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
OLLAMA_BASE_URL=http://localhost:11434
EOF

# Test
python -c "from litellm import completion; print('✓ LiteLLM ready')"

# Run examples
python examples.py

# Or start proxy server
python proxy_server.py
# Server runs on http://localhost:8000
```

## Environment Variables

### RAG_Model

| Variable | Description | Default |
|----------|-------------|---------|
| `RAG_EMBEDDING_MODEL` | Embedding model name | `sentence-transformers/all-MiniLM-L6-v2` |
| `RAG_VECTOR_STORE_PATH` | Path for vector store | `vector_store` |
| `RAG_LLM_MODEL` | LLM model for generation | `llama3.1:8b` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `RAG_CHUNK_SIZE` | Text chunk size | `1000` |
| `RAG_CHUNK_OVERLAP` | Chunk overlap | `200` |
| `RAG_DEFAULT_K` | Default retrieval count | `5` |

### Psychometrics

No required environment variables. Optional for future features.

### ChatUi

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | API base URL | `http://localhost:3000` |
| `MONGODB_URL` | MongoDB connection string | - |
| `HF_TOKEN` | Hugging Face token | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |

### ios_chatbot

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `PORT` | Server port | `5000` |
| `SECRET_KEY` | Flask secret key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `OLLAMA_URL` | Ollama server URL | `http://localhost:11434` |

### litellm

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Proxy server port | `8000` |
| `HOST` | Server host | `0.0.0.0` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |

## Testing

### Run All Tests

```bash
cd projects
chmod +x test_all.sh
./test_all.sh
```

### Test Individual Projects

#### RAG_Model

```bash
cd RAG_Model
python main.py
# Type a query when prompted
```

#### Psychometrics

```bash
cd Psychometrics
python main.py
# Follow the interactive prompts
```

#### ChatUi

```bash
cd ChatUi
npm run dev
# Open http://localhost:5173 in browser
```

#### ios_chatbot

```bash
cd ios_chatbot
python app.py
# Open http://localhost:5000 in browser
```

#### litellm

```bash
cd litellm
python examples.py
# Or test proxy:
python proxy_server.py
# Then in another terminal:
curl http://localhost:8000/health
```

## Optional Setup

### Ollama (Local LLMs)

1. Install from [ollama.ai](https://ollama.ai)
2. Pull a model:
   ```bash
   ollama pull llama3.1:8b
   ollama pull mistral:7b
   ```
3. Start Ollama (usually runs automatically):
   ```bash
   ollama serve
   ```

### MongoDB (for ChatUi)

**Option 1: Docker**
```bash
docker run -d -p 27017:27017 --name mongo-chatui mongo:latest
```

**Option 2: MongoDB Atlas**
1. Sign up at [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Create a free cluster
3. Get connection string
4. Add to ChatUi `.env.local`:
   ```
   MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/chatui
   ```

## Troubleshooting

### Common Issues

#### Import Errors

**Problem:** `ModuleNotFoundError` or `ImportError`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
# Or for Node.js projects:
npm install
```

#### Port Already in Use

**Problem:** `Address already in use`

**Solution:**
- Change port in `.env` file
- Or kill the process using the port:
  ```bash
  # Find process
  lsof -i :5000
  # Kill it
  kill -9 <PID>
  ```

#### API Key Issues

**Problem:** API errors or authentication failures

**Solution:**
1. Verify API key is set: `echo $OPENAI_API_KEY`
2. Check key is valid (has credits/quota)
3. Ensure key is in `.env` file, not just environment
4. For Ollama, ensure it's running: `curl http://localhost:11434/api/tags`

#### Node.js Issues (ChatUi)

**Problem:** npm install fails or build errors

**Solution:**
```bash
cd ChatUi
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Ollama Connection Issues

**Problem:** Can't connect to Ollama

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve

# Verify model is available
ollama list
```

### Getting Help

1. Check project-specific README files
2. Review error messages carefully
3. Verify all prerequisites are installed
4. Ensure environment variables are set correctly
5. Check that required services (Ollama, MongoDB) are running

## Next Steps

After setup is complete:

1. **Read Project READMEs** - Each project has detailed documentation
2. **Customize Configurations** - Adjust settings for your use case
3. **Integrate with Your Systems** - Connect projects to your existing infrastructure
4. **Experiment** - Try different models and configurations
5. **Contribute** - Share improvements and feedback!

## Quick Reference

### Start All Services

```bash
# Terminal 1: Ollama (if using local models)
ollama serve

# Terminal 2: MongoDB (if using ChatUi)
docker start mongo-chatui

# Terminal 3: RAG_Model
cd projects/RAG_Model && python main.py

# Terminal 4: ios_chatbot
cd projects/ios_chatbot && python app.py

# Terminal 5: litellm proxy
cd projects/litellm && python proxy_server.py

# Terminal 6: ChatUi
cd projects/ChatUi && npm run dev
```

### Useful Commands

```bash
# Check Python version
python --version

# Check Node version
node --version

# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check if MongoDB is running
docker ps | grep mongo

# List installed Python packages
pip list

# List installed npm packages
npm list --depth=0
```

