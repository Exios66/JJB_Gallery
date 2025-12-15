# Project Overview

Comprehensive overview of all projects in the JJB Gallery repository.

## Project Categories

### AI & Machine Learning

#### RAG Model
**Location**: `projects/RAG_Model/`

A complete Retrieval-Augmented Generation system with:
- Vector database (FAISS)
- Document embeddings
- Semantic search
- LLM integration

**Use Cases**: Document Q&A, knowledge bases, research assistants

**Tech Stack**: Python, LangChain, FAISS, Sentence Transformers

#### Psychometrics
**Location**: `projects/Psychometrics/`

NASA Task Load Index (TLX) assessment tool for:
- Workload measurement
- Cognitive load assessment
- User experience research

**Use Cases**: UX research, human factors engineering, training evaluation

**Tech Stack**: Python (standard library)

### Chat Interfaces

#### ChatUi
**Location**: `projects/ChatUi/`

Modern SvelteKit chat interface for:
- LLM interactions
- Multiple model support
- Real-time streaming
- Message history

**Use Cases**: Chat applications, AI assistants, customer support

**Tech Stack**: SvelteKit, TypeScript, MongoDB

#### iOS Chatbot
**Location**: `projects/ios_chatbot/`

iOS-inspired chatbot with:
- Beautiful gradient UI
- Flask backend
- RESTful API
- Easy LLM integration

**Use Cases**: Chat applications, mobile web apps, demos

**Tech Stack**: Flask, JavaScript, HTML/CSS

### LLM Integration

#### LiteLLM Integration
**Location**: `projects/litellm/`

Unified LLM API access with:
- Proxy server
- Multiple provider support
- OpenAI-compatible API
- Configuration management

**Use Cases**: LLM abstraction layer, multi-provider support, API gateway

**Tech Stack**: Python, FastAPI, LiteLLM

#### CrewAI Multi-Agent System
**Location**: `projects/Crewai/`

Multi-agent framework with:
- Specialized agent swarms
- Domain-specific tools
- Web and CLI interfaces
- Multiple LLM providers

**Use Cases**: Complex workflows, research automation, code generation

**Tech Stack**: Python, CrewAI, Streamlit

#### Terminal Agents
**Location**: `projects/terminal_agents/`

AI coding agents for terminal with:
- Code analysis
- Code generation
- Interactive chat
- Rich terminal UI

**Use Cases**: Code assistance, debugging, learning

**Tech Stack**: Python, OpenAI API

## Project Comparison

| Project | Type | API Keys | Complexity | Best For |
|---------|------|----------|------------|----------|
| RAG Model | ML/AI | Optional | Medium | Document Q&A |
| Psychometrics | Assessment | None | Low | UX Research |
| ChatUi | Web App | Optional | Medium | Chat Apps |
| iOS Chatbot | Web App | Optional | Low | Simple Chat |
| LiteLLM | Integration | Required | Medium | LLM Abstraction |
| CrewAI | Framework | Required | High | Complex Workflows |
| Terminal Agents | CLI Tool | Required | Low | Code Assistance |

## Technology Stack Summary

### Languages
- **Python**: Most projects
- **JavaScript/TypeScript**: ChatUi
- **HTML/CSS**: iOS Chatbot

### Frameworks
- **Flask**: iOS Chatbot
- **SvelteKit**: ChatUi
- **FastAPI**: LiteLLM proxy
- **Streamlit**: CrewAI web interface

### ML/AI Libraries
- **LangChain**: RAG Model
- **LiteLLM**: LiteLLM Integration
- **CrewAI**: CrewAI System
- **Sentence Transformers**: RAG Model

### Databases
- **FAISS**: RAG Model (vector database)
- **MongoDB**: ChatUi (chat history)

## Getting Started Recommendations

### For Beginners

1. **Psychometrics** - Simplest, no API keys needed
2. **iOS Chatbot** - Simple web app, easy to understand
3. **RAG Model** - Good introduction to ML concepts

### For Intermediate Users

1. **ChatUi** - Modern web development
2. **LiteLLM** - API integration patterns
3. **Terminal Agents** - CLI tool development

### For Advanced Users

1. **CrewAI** - Complex multi-agent systems
2. **RAG Model** - Advanced ML/AI concepts
3. **Full Stack Integration** - Combine multiple projects

## Project Dependencies

### Common Dependencies

Most Python projects share:
- `pydantic` - Data validation
- `python-dotenv` - Environment variables
- `requests` - HTTP clients

### Project-Specific

- **RAG Model**: langchain, faiss-cpu, sentence-transformers
- **ChatUi**: @sveltejs/kit, mongodb, openai
- **CrewAI**: crewai, crewai-tools, streamlit
- **LiteLLM**: litellm, fastapi, uvicorn

## Integration Possibilities

### Combine Projects

1. **ChatUi + LiteLLM**: Use LiteLLM proxy with ChatUi
2. **iOS Chatbot + RAG Model**: Add RAG capabilities to chatbot
3. **CrewAI + RAG Model**: Use RAG for research agents
4. **Terminal Agents + LiteLLM**: Unified LLM access

### Use Cases

- **Research Assistant**: RAG Model + CrewAI
- **Customer Support**: ChatUi + LiteLLM
- **Code Helper**: Terminal Agents + CrewAI
- **UX Testing**: Psychometrics + ChatUi

## Project Status

All projects are:
- ✅ **Complete**: Fully implemented
- ✅ **Documented**: Comprehensive READMEs
- ✅ **Tested**: Basic functionality verified
- ✅ **Maintained**: Active development

## Next Steps

1. **Choose a Project**: Based on your interests and skill level
2. **Read Documentation**: Check project-specific READMEs
3. **Install Dependencies**: Follow installation guides
4. **Run Examples**: Test with provided examples
5. **Customize**: Adapt to your needs

## Related Documentation

- [Installation Guide](Installation-Guide.md)
- [Quick Start](Quick-Start.md)
- [Configuration Guide](Configuration-Guide.md)
- Individual project pages

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>

