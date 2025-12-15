# RAG Model Application

A complete Retrieval-Augmented Generation (RAG) system implementation with vector database, embeddings, and intelligent document retrieval.

## Overview

This project implements a full RAG pipeline that:

- Ingests and processes documents
- Creates embeddings using transformer models
- Stores embeddings in a vector database (FAISS)
- Retrieves relevant documents for queries
- Generates answers using retrieved context

## Features

- **Document Processing**: Supports TXT, MD, and JSON files
- **Vector Database**: Uses FAISS for efficient similarity search
- **Embeddings**: Sentence transformers for high-quality embeddings
- **Retrieval**: Semantic search with configurable top-k retrieval
- **Generation**: Integration with Ollama for local LLM inference
- **Interactive CLI**: Command-line interface for querying

## Installation

### Prerequisites

- Python 3.8+
- Ollama (for LLM generation) - [Install Ollama](https://ollama.ai)

### Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. (Optional) Install and start Ollama for LLM generation:

```bash
# Install Ollama from https://ollama.ai
# Then pull a model:
ollama pull llama3.1:8b
```

## Usage

### Basic Usage

Run the interactive query interface:

```bash
python main.py
```

The system will:

1. Create sample documents if none exist
2. Build or load the vector store
3. Start an interactive query session

### Programmatic Usage

```python
from rag_system import RAGSystem

# Initialize RAG system
rag = RAGSystem(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    vector_store_path="vector_store",
    llm_model="llama3.1:8b"
)

# Load or create vector store
documents = rag.load_documents(["doc1.txt", "doc2.txt"])
rag.create_vector_store(documents, save=True)

# Query the system
result = rag.query("What is RAG?", k=5)
print(result['answer'])
```

### Adding Your Own Documents

1. Place documents in the `documents/` directory (or any directory)
2. Update the code to load your documents:

```python
file_paths = [
    "documents/my_doc1.txt",
    "documents/my_doc2.md",
    "documents/data.json"
]
documents = rag.load_documents(file_paths)
rag.create_vector_store(documents, save=True)
```

## Configuration

Set environment variables to customize behavior:

```bash
export RAG_EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
export RAG_LLM_MODEL="llama3.1:8b"
export RAG_CHUNK_SIZE=1000
export RAG_CHUNK_OVERLAP=200
export RAG_DEFAULT_K=5
export RAG_VECTOR_STORE_PATH="vector_store"
```

## 🏭 Production Deployment

### Deployment Strategy

For production, we recommend wrapping the RAG system in a REST API (using FastAPI) and deploying it as a containerized service.

### Docker Deployment

1. **Dockerfile**:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Run Container**:

```bash
docker run -d -p 8000:8000 -v ./vector_store:/app/vector_store rag-service:latest
```

### Vector Database Scaling

1. **FAISS on GPU**: For large-scale datasets (>1M vectors), use `faiss-gpu` for significantly faster indexing and search.
2. **IVF Indexing**: Use Inverted File (IVF) indexing to speed up search by clustering vectors.
3. **External Vector DB**: For distributed scaling, consider migrating from local FAISS files to managed services like Qdrant, Pinecone, or Weaviate.

### Caching Strategies

- **Embedding Cache**: Cache embeddings for frequently ingested documents to avoid re-computation.
- **Query Cache**: Cache results for identical queries using Redis to reduce LLM latency.

### Performance Optimization

1. **Quantization**: Use quantized embedding models (int8) to reduce memory usage and increase speed with minimal accuracy loss.
2. **Batch Processing**: Process document ingestion in batches to utilize vectorization efficiencies.
3. **Asynchronous Ingestion**: Offload document processing to a background worker (Celery/RQ) to keep the API responsive.

## Architecture

```
┌─────────────┐
│  Documents  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Text Split  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Embeddings  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Vector Store │
│   (FAISS)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Retrieval  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Generation  │
│   (LLM)     │
└─────────────┘
```

## Components

### `rag_system.py`

Core RAG implementation with:

- Document loading and processing
- Embedding generation
- Vector store management
- Retrieval and generation

### `main.py`

Command-line interface and demo application

## Vector Database

The system uses FAISS (Facebook AI Similarity Search) for efficient vector storage and retrieval. FAISS supports:

- Fast similarity search
- Scalable to millions of vectors
- CPU and GPU support
- Various indexing methods

## Embedding Models

Default: `sentence-transformers/all-MiniLM-L6-v2`

You can use any sentence transformer model:

- `all-MiniLM-L6-v2` (default, fast, 384 dims)
- `all-mpnet-base-v2` (better quality, 768 dims)
- `all-MiniLM-L12-v2` (larger, 384 dims)

## LLM Integration

The system integrates with Ollama for local LLM inference. Supported models:

- `llama3.1:8b` (default)
- `mistral:7b`
- `codellama:13b`
- Any Ollama-compatible model

## Performance Tips

1. **Chunk Size**: Adjust based on your documents (500-2000 tokens)
2. **Overlap**: Use 10-20% overlap for better context
3. **Top-K**: Start with k=5, adjust based on results
4. **Embedding Model**: Larger models = better quality but slower
5. **Vector Store**: Use GPU FAISS for large datasets

## Troubleshooting

### Import Errors

```bash
pip install langchain faiss-cpu sentence-transformers
```

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags
```

### Memory Issues

- Reduce chunk size
- Use smaller embedding model
- Process documents in batches

## License

See main repository LICENSE file.

## References

- [RAG Paper](https://arxiv.org/abs/2005.11401)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [Ollama](https://ollama.ai)

## Related Projects

- [CrewAI](../CrewAI/README.md) - Multi-Agent System
- [Terminal Agents](../terminal_agents/README.md) - AI Coding Assistant
- [LiteLLM](../litellm/README.md) - Unified LLM API

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
