"""
Configuration for RAG Model Application
"""

import os
from pathlib import Path


class RAGConfig:
    """Configuration class for RAG system."""
    
    # Embedding model configuration
    EMBEDDING_MODEL: str = os.getenv(
        "RAG_EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Vector store configuration
    VECTOR_STORE_PATH: str = os.getenv(
        "RAG_VECTOR_STORE_PATH",
        "vector_store"
    )
    
    # LLM configuration
    LLM_MODEL: str = os.getenv("RAG_LLM_MODEL", "llama3.1:8b")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Text chunking configuration
    CHUNK_SIZE: int = int(os.getenv("RAG_CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("RAG_CHUNK_OVERLAP", "200"))
    
    # Retrieval configuration
    DEFAULT_K: int = int(os.getenv("RAG_DEFAULT_K", "5"))
    
    # Document paths
    DOCUMENTS_DIR: Path = Path(__file__).parent / "documents"
    SAMPLE_DOCUMENTS_DIR: Path = Path(__file__).parent / "sample_documents"
    
    @classmethod
    def validate(cls) -> dict:
        """Validate configuration."""
        return {
            "embedding_model": cls.EMBEDDING_MODEL,
            "vector_store_path": cls.VECTOR_STORE_PATH,
            "llm_model": cls.LLM_MODEL,
            "chunk_size": cls.CHUNK_SIZE,
            "chunk_overlap": cls.CHUNK_OVERLAP,
        }


# Create singleton instance
config = RAGConfig()

