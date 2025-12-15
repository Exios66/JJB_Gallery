# Troubleshooting Guide

Common issues and solutions for all projects in the JJB Gallery repository.

## General Issues

### Import Errors

**Problem**: `ModuleNotFoundError` or `ImportError`

**Solutions**:

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

### Port Already in Use

**Problem**: `Address already in use` or `Port XXXX is already in use`

**Solutions**:

```bash
# Find process using port
lsof -i :5000  # Replace 5000 with your port

# Kill process
kill -9 <PID>

# Or change port in configuration
# iOS Chatbot: PORT=5001 in .env
# LiteLLM: PORT=8001 in .env
# ChatUi: Change in vite.config.js
```

### API Key Issues

**Problem**: API errors, authentication failures, or "Invalid API key"

**Solutions**:

1. **Verify API key is set**:
   ```bash
   echo $OPENAI_API_KEY
   echo $ANTHROPIC_API_KEY
   ```

2. **Check key is in .env file**:
   ```bash
   cat .env | grep API_KEY
   ```

3. **Ensure key is valid**:
   - Check key has credits/quota
   - Verify key hasn't expired
   - Check key has required permissions

4. **Remove extra spaces or quotes**:
   ```bash
   # Bad
   OPENAI_API_KEY="sk-... "
   
   # Good
   OPENAI_API_KEY=sk-...
   ```

## Project-Specific Issues

### RAG Model

#### Import Errors

```bash
# Install missing dependencies
pip install langchain faiss-cpu sentence-transformers

# For GPU support
pip install faiss-gpu
```

#### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Verify model is available
ollama list
```

#### Memory Issues

- Reduce chunk size: `RAG_CHUNK_SIZE=500`
- Use smaller embedding model: `RAG_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2`
- Process documents in batches

### Psychometrics

#### No Issues Expected

Psychometrics uses only standard library. If you see errors:

```bash
# Verify Python installation
python --version

# Check file permissions
chmod +x main.py
```

### ChatUi

#### Node.js Issues

```bash
# Clear cache and reinstall
cd ChatUi
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Check Node version
node --version  # Should be 18+
```

#### MongoDB Connection

```bash
# Check if MongoDB is running
docker ps | grep mongo

# Start MongoDB
docker run -d -p 27017:27017 --name mongo-chatui mongo:latest

# Or check connection string in .env.local
```

#### Build Errors

```bash
# Update dependencies
npm update

# Clear build cache
rm -rf .svelte-kit
npm run build
```

### iOS Chatbot

#### Flask Errors

```bash
# Install Flask
pip install flask flask-cors python-dotenv

# Check Flask version
python -c "import flask; print(flask.__version__)"
```

#### CORS Issues

Update `app.py`:

```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

#### Template Not Found

Ensure `templates/` directory exists:

```bash
mkdir -p templates static
```

### LiteLLM

#### Import Errors

```bash
# Install LiteLLM
pip install litellm

# Or with proxy extras
pip install 'litellm[proxy]'
```

#### Provider Connection Issues

```bash
# Test OpenAI
python -c "from litellm import completion; completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'test'}])"

# Test Ollama
curl http://localhost:11434/api/tags
```

#### Proxy Server Not Starting

```bash
# Check port
lsof -i :8000

# Change port
PORT=8001 python proxy_server.py
```

### CrewAI

#### LLM Provider Not Detected

```bash
# Check status
python main.py --status

# Get setup instructions
python main.py --setup-llm

# Verify provider
# For Ollama:
curl http://localhost:11434/api/tags

# For OpenAI:
echo $OPENAI_API_KEY
```

#### Agent Errors

```bash
# Check verbose mode
export VERBOSE=true
python main.py --run ml

# Verify tools are available
python -c "from tools import ml_tools; print('OK')"
```

### Terminal Agents

#### API Key Not Found

```bash
# Set API key
export OPENAI_API_KEY=sk-...

# Or create .env file
echo "OPENAI_API_KEY=sk-..." > .env
```

#### Command Not Found

```bash
# Make executable
chmod +x agent.py

# Or use Python directly
python agent.py interactive
```

## Environment-Specific Issues

### macOS

#### Permission Errors

```bash
# Fix permissions
chmod +x setup_all.sh
chmod +x test_all.sh
```

#### Homebrew Issues

```bash
# Update Homebrew
brew update

# Reinstall Python
brew reinstall python@3.11
```

### Linux

#### Missing System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pip nodejs npm

# Fedora
sudo dnf install python3-pip nodejs npm
```

#### Permission Errors

```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
```

### Windows

#### Path Issues

```bash
# Use full paths
python C:\path\to\project\main.py

# Or add to PATH
set PATH=%PATH%;C:\Python311;C:\Python311\Scripts
```

#### Line Ending Issues

```bash
# Convert line endings
dos2unix setup_all.sh
```

## Performance Issues

### Slow Responses

1. **Use local models** (Ollama) instead of cloud APIs
2. **Reduce chunk sizes** in RAG Model
3. **Use smaller models** for faster inference
4. **Enable caching** where available

### Memory Issues

1. **Use virtual environments** to isolate dependencies
2. **Process data in batches**
3. **Use smaller models**
4. **Close unused applications**

### Network Issues

1. **Check internet connection**
2. **Verify API endpoints are accessible**
3. **Check firewall settings**
4. **Use local models** (Ollama) to avoid network

## Getting Help

### Before Asking for Help

1. **Check error messages** carefully
2. **Review project READMEs**
3. **Search existing issues** on GitHub
4. **Check documentation**

### When Asking for Help

Include:
- Project name and version
- Error message (full traceback)
- Steps to reproduce
- Environment details (OS, Python version, etc.)
- Configuration (sanitized, no API keys)

### Resources

- [Installation Guide](Installation-Guide.md)
- [Configuration Guide](Configuration-Guide.md)
- [Quick Start](Quick-Start.md)
- Project-specific READMEs
- GitHub Issues

## Prevention Tips

1. **Use virtual environments** for Python projects
2. **Keep dependencies updated**
3. **Use version control** (Git)
4. **Test in isolated environments**
5. **Document your setup**
6. **Backup configurations**

## Related Documentation

- [Installation Guide](Installation-Guide.md)
- [Configuration Guide](Configuration-Guide.md)
- [Quick Start](Quick-Start.md)

