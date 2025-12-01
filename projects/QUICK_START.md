# Quick Start Guide

This guide will help you quickly set up and test all projects in this repository.

## Prerequisites

- Python 3.8+ with pip
- Node.js 18+ with npm (for ChatUi)
- Git

## Step 1: Install Dependencies

### Option A: Automated Setup (Recommended)

```bash
cd projects
chmod +x setup_all.sh
./setup_all.sh
```

### Option B: Manual Setup

Install dependencies for each project:

```bash
# RAG_Model
cd RAG_Model && pip install -r requirements.txt && cd ..

# Psychometrics
cd Psychometrics && pip install -r requirements.txt && cd ..

# ChatUi
cd ChatUi && npm install && cd ..

# ios_chatbot
cd ios_chatbot && pip install -r requirements.txt && cd ..

# litellm
cd litellm && pip install -r requirements.txt && cd ..
```

## Step 2: Set Up Environment Variables

### Copy Environment Templates

```bash
# RAG_Model
cp RAG_Model/.env.example RAG_Model/.env

# Psychometrics
cp Psychometrics/.env.example Psychometrics/.env

# ios_chatbot
cp ios_chatbot/.env.example ios_chatbot/.env

# litellm
cp litellm/.env.example litellm/.env
```

### Configure API Keys

Edit each `.env` file and add your API keys:

#### For RAG_Model:
- Optional: `OPENAI_API_KEY` if using OpenAI
- Optional: `HF_TOKEN` for Hugging Face models

#### For ios_chatbot:
- Choose one: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or use Ollama (local)

#### For litellm:
- Add keys for providers you want to use: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.

## Step 3: Test Projects

### Run Automated Tests

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
```

#### Psychometrics

```bash
cd Psychometrics
python main.py
```

#### ChatUi

```bash
cd ChatUi
npm run dev
# Open http://localhost:5173
```

#### ios_chatbot

```bash
cd ios_chatbot
python app.py
# Open http://localhost:5000
```

#### litellm

```bash
cd litellm
# Test examples
python examples.py

# Or start proxy server
python proxy_server.py
# Server runs on http://localhost:8000
```

## Step 4: Optional Setup

### Install Ollama (for Local LLMs)

If you want to use local models with Ollama:

```bash
# Install Ollama from https://ollama.ai
# Then pull a model:
ollama pull llama3.1:8b
```

### Set Up MongoDB (for ChatUi)

If you want persistent chat history:

```bash
# Using Docker
docker run -d -p 27017:27017 --name mongo-chatui mongo:latest

# Or use MongoDB Atlas (free tier available)
```

## Project-Specific Quick Starts

### RAG_Model

1. Add documents to `sample_documents/` or `documents/`
2. Run: `python main.py`
3. The system will create vector store and start interactive chat

### Psychometrics

1. Run: `python main.py`
2. Follow prompts to complete NASA TLX assessment
3. Results are saved and can be exported to JSON

### ChatUi

1. Set `VITE_API_BASE_URL` in `.env.local` (or use default)
2. Run: `npm run dev`
3. Connect to your LLM backend (see README for integration)

### ios_chatbot

1. Set API keys in `.env`
2. Run: `python app.py`
3. Open browser to `http://localhost:5000`
4. Start chatting!

### litellm

1. Set API keys in `.env`
2. Start proxy: `python proxy_server.py`
3. Use with any OpenAI-compatible client:

```python
import openai
client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="anything"
)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Troubleshooting

### Import Errors

If you see import errors, make sure dependencies are installed:

```bash
pip install -r requirements.txt
```

### Port Already in Use

Change the port in the project's configuration or `.env` file.

### API Key Issues

- Verify API keys are set correctly in `.env` files
- Check that API keys are valid and have credits/quota
- For Ollama, ensure it's running: `ollama serve`

### Node.js Issues (ChatUi)

```bash
# Clear cache and reinstall
cd ChatUi
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

- Read individual project READMEs for detailed documentation
- Customize configurations for your use case
- Integrate with your existing systems
- Contribute improvements!

## Getting Help

- Check project-specific README files
- Review error messages for specific issues
- Ensure all prerequisites are installed
- Verify environment variables are set correctly

