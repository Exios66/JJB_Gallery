# Architecture Overview

High-level architecture and design patterns used across projects in the JJB Gallery repository.

## System Architecture

### Overall Structure

```bash
JJB_Gallery/
├── projects/           # Individual project implementations
├── docs/              # Documentation
├── scripts/           # Utility scripts
├── notebooks/         # Jupyter notebooks
└── Quarto/            # Quarto documents
```

## Project Architectures

### RAG Model

**Architecture**: Pipeline-based

```bash
Documents → Text Splitter → Embeddings → Vector Store (FAISS)
                                              ↓
                                         Query → Retrieval
                                              ↓
                                         Context + Query → LLM → Answer
```

**Components**:

- **Document Loader**: Handles multiple file formats
- **Text Splitter**: Chunks documents for processing
- **Embedding Model**: Creates vector representations
- **Vector Store**: FAISS for similarity search
- **Retrieval**: Semantic search over embeddings
- **Generation**: LLM for answer generation

### Psychometrics

**Architecture**: Assessment Pipeline

```bash
User Input → Rating Collection → Pairwise Comparisons → Score Calculation
                                                              ↓
                                                         Statistics & Export
```

**Components**:

- **TLXRating**: Individual dimension ratings
- **TLXPairwiseComparison**: Weight calculation
- **TLXResult**: Complete assessment result
- **NASATLX**: Main assessment system

### ChatUi

**Architecture**: Client-Server (SvelteKit)

```bash
Frontend (SvelteKit) → API Routes → LLM Backend
         ↓
    MongoDB (History)
```

**Components**:

- **Frontend**: SvelteKit components
- **API Routes**: Server-side endpoints
- **Database**: MongoDB for chat history
- **LLM Integration**: Multiple provider support

### iOS Chatbot

**Architecture**: Traditional Web App

```bash
Browser → Flask Server → ChatBot → LLM Provider
              ↓
        In-Memory Storage (conversations)
```

**Components**:

- **Frontend**: HTML/CSS/JavaScript
- **Backend**: Flask application
- **API**: RESTful endpoints
- **Storage**: In-memory (can be extended to database)

### LiteLLM

**Architecture**: Proxy Server

```bash
Client → LiteLLM Proxy → Provider Router → LLM Providers
                              ↓
                         Response Aggregation
```

**Components**:

- **Proxy Server**: FastAPI application
- **Router**: Provider selection and routing
- **Adapters**: Provider-specific adapters
- **Configuration**: YAML-based config

### CrewAI

**Architecture**: Multi-Agent System

```bash
User Request → Crew Selection → Agent Swarm → Task Execution
                                      ↓
                                 Tool Execution
                                      ↓
                                 Result Aggregation
```

**Components**:

- **Agents**: Specialized AI agents
- **Crews**: Agent swarms
- **Tasks**: Workflow definitions
- **Tools**: Domain-specific tools
- **LLM Backend**: Multiple provider support

## Design Patterns

### 1. Factory Pattern

Used in:

- **RAG Model**: Embedding model selection
- **CrewAI**: Agent and crew creation
- **LiteLLM**: Provider initialization

### 2. Strategy Pattern

Used in:

- **LiteLLM**: Provider selection
- **CrewAI**: LLM provider switching
- **RAG Model**: Embedding model selection

### 3. Repository Pattern

Used in:

- **RAG Model**: Vector store abstraction
- **ChatUi**: MongoDB data access
- **Psychometrics**: Result storage

### 4. Adapter Pattern

Used in:

- **LiteLLM**: Provider API adaptation
- **RAG Model**: LLM provider integration
- **ChatUi**: Multiple backend support

## Data Flow Patterns

### Request-Response

Most projects use synchronous request-response:

```bash
Client → Server → LLM → Response → Client
```

### Streaming

Projects supporting streaming:

```bash
Client → Server → LLM (stream) → Chunks → Client
```

### Async Processing

Projects using async:

```bash
Client → Server → Async Task → Background Processing → Response
```

## Integration Patterns

### Direct Integration

Projects directly calling LLM APIs:

- iOS Chatbot
- Terminal Agents
- CrewAI

### Proxy Integration

Projects using proxy layer:

- ChatUi (can use LiteLLM proxy)
- LiteLLM (proxy server)

### Abstraction Layer

Projects with abstraction:

- LiteLLM (unified API)
- RAG Model (provider-agnostic)

## Technology Choices

### Why Python?

- Rich ML/AI ecosystem
- Easy LLM integration
- Rapid prototyping
- Extensive libraries

### Why SvelteKit?

- Modern framework
- Server-side rendering
- Type safety
- Great developer experience

### Why Flask?

- Simple and lightweight
- Easy to understand
- Quick development
- Flexible

### Why FastAPI?

- Modern async support
- Automatic documentation
- Type validation
- High performance

## Scalability Considerations

### Horizontal Scaling

- **Stateless Services**: ChatUi, iOS Chatbot, LiteLLM proxy
- **Load Balancing**: Multiple instances
- **Database**: Shared MongoDB/PostgreSQL

### Vertical Scaling

- **Vector Stores**: FAISS with GPU support
- **LLM Inference**: Local models with GPU
- **Caching**: Redis for frequent queries

### Optimization Strategies

1. **Caching**: Response caching for common queries
2. **Batching**: Batch processing for multiple requests
3. **Async**: Async processing for I/O operations
4. **Connection Pooling**: Database connection pooling

## Security Considerations

### API Key Management

- Environment variables (never in code)
- Secret management services
- Key rotation policies

### Input Validation

- Pydantic models for validation
- Sanitization of user inputs
- Rate limiting

### Data Privacy

- No logging of sensitive data
- Encrypted storage
- GDPR compliance considerations

## Monitoring & Observability

### Logging

- Structured logging
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Centralized logging

### Metrics

- Request counts
- Response times
- Error rates
- Resource usage

### Tracing

- Request tracing
- Distributed tracing
- Performance profiling

## Related Documentation

- [Project Overview](Project-Overview)
- [API Reference](API-Reference)
- [Development Setup](Development-Setup)
