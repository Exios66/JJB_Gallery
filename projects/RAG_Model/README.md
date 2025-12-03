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

Or use the config module:

```python
from config import config

print(config.EMBEDDING_MODEL)
print(config.CHUNK_SIZE)
```

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
│  Retrieval   │
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

### `config.py`

Configuration management

## Supported File Formats

- **TXT**: Plain text files
- **MD**: Markdown files
- **JSON**: JSON data files

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

# Start Ollama if needed
ollama serve
```

### Memory Issues

- Reduce chunk size
- Use smaller embedding model
- Process documents in batches

## Examples

### Example 1: Simple Query

```python
rag = RAGSystem()
rag.load_vector_store()
result = rag.query("What is machine learning?")
print(result['answer'])
```

### Example 2: Custom Configuration

```python
rag = RAGSystem(
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    chunk_size=1500,
    chunk_overlap=300
)
```

### Example 3: Batch Processing

```python
# Process multiple document sets
for doc_set in document_sets:
    documents = rag.load_documents(doc_set)
    rag.create_vector_store(documents, save=False)
    # Process queries
```

## License

See main repository LICENSE file.

## References

- [RAG Paper](https://arxiv.org/abs/2005.11401)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [Ollama](https://ollama.ai)

## Related Projects

This project is part of the [JJB Gallery](https://github.com/Exios66/JJB_Gallery) portfolio. Related projects include:

- [Ruckus](../ruckus/README.md) - LLM Fine-tuning Framework
- [CrewAI](../CrewAI/README.md) - Multi-Agent System
- [Terminal Agents](../terminal_agents/README.md) - AI Coding Assistant
- [LiteLLM](../litellm/README.md) - Unified LLM API

## Additional Resources

- 📚 [Project Wiki](https://github.com/Exios66/JJB_Gallery/wiki) - Comprehensive documentation
- 📖 [RAG Model Wiki Page](https://github.com/Exios66/JJB_Gallery/wiki/RAG-Model) - Detailed project documentation
- 🔧 [Configuration Guide](https://github.com/Exios66/JJB_Gallery/wiki/Configuration-Guide) - Setup and configuration
- 🐛 [Troubleshooting](https://github.com/Exios66/JJB_Gallery/wiki/Troubleshooting) - Common issues and solutions

## Contributing

Contributions welcome! Please see the main repository [Contributing Guidelines](https://github.com/Exios66/JJB_Gallery/wiki/Contributing-Guidelines).

For issues, questions, or suggestions, please use the [GitHub Issues](https://github.com/Exios66/JJB_Gallery/issues) page.
