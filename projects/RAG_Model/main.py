#!/usr/bin/env python3
"""
RAG Model Application - Main Entry Point
Demonstrates Retrieval-Augmented Generation with vector database.
"""

import os
import sys
from pathlib import Path
from rag_system import RAGSystem


def create_sample_documents():
    """Create sample documents for demonstration."""
    docs_dir = Path("sample_documents")
    docs_dir.mkdir(exist_ok=True)
    
    sample_docs = {
        "ai_overview.txt": """
Artificial Intelligence (AI) is a branch of computer science that aims to create 
intelligent machines capable of performing tasks that typically require human intelligence.
These tasks include learning, reasoning, problem-solving, perception, and language understanding.

Machine Learning is a subset of AI that enables systems to learn and improve from 
experience without being explicitly programmed. Deep Learning, in turn, is a subset 
of machine learning that uses neural networks with multiple layers to analyze 
various factors of data.

Natural Language Processing (NLP) is another important area of AI that focuses on 
the interaction between computers and human language. NLP enables machines to 
understand, interpret, and generate human language in a valuable way.
""",
        "rag_explanation.txt": """
Retrieval-Augmented Generation (RAG) is a technique that combines the power of 
information retrieval with language generation. RAG systems first retrieve relevant 
documents from a knowledge base, then use those documents as context for generating 
accurate and informed responses.

The RAG process typically involves:
1. Document ingestion and preprocessing
2. Creating embeddings for documents
3. Storing embeddings in a vector database
4. Retrieving relevant documents for a query
5. Using retrieved documents as context for generation

RAG addresses the limitation of LLMs by providing them with access to external 
knowledge sources, making responses more accurate and up-to-date.
""",
        "vector_databases.txt": """
Vector databases are specialized databases designed to store and query high-dimensional 
vectors efficiently. They are essential for RAG systems because they enable fast 
similarity search over embeddings.

Popular vector databases include:
- FAISS (Facebook AI Similarity Search) - Open source, efficient
- Pinecone - Managed service, scalable
- Weaviate - Open source, graph-like structure
- Chroma - Open source, easy to use
- Qdrant - Open source, production-ready

Vector databases use approximate nearest neighbor (ANN) algorithms to find similar 
vectors quickly, even with millions of documents. They support operations like 
similarity search, filtering, and hybrid search combining vector and metadata queries.
"""
    }
    
    for filename, content in sample_docs.items():
        filepath = docs_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"Created {len(sample_docs)} sample documents in {docs_dir}/")
    return [str(docs_dir / f) for f in sample_docs.keys()]


def main():
    """Main entry point."""
    print("=" * 60)
    print("RAG Model Application")
    print("=" * 60)
    print()
    
    # Initialize RAG system
    print("Initializing RAG system...")
    rag = RAGSystem(
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        vector_store_path="vector_store",
        llm_model="llama3.1:8b"
    )
    print("✅ RAG system initialized\n")
    
    # Check if vector store exists
    vector_store_path = Path("vector_store")
    if vector_store_path.exists() and any(vector_store_path.iterdir()):
        print("Loading existing vector store...")
        try:
            rag.load_vector_store()
            print("✅ Vector store loaded\n")
        except Exception as e:
            print(f"⚠️  Error loading vector store: {e}")
            print("Creating new vector store...")
            file_paths = create_sample_documents()
            rag.create_vector_store(
                rag.load_documents(file_paths),
                save=True
            )
    else:
        print("Creating new vector store from sample documents...")
        file_paths = create_sample_documents()
        documents = rag.load_documents(file_paths)
        rag.create_vector_store(documents, save=True)
        print("✅ Vector store created\n")
    
    # Interactive query loop
    print("=" * 60)
    print("RAG Query Interface")
    print("=" * 60)
    print("Enter queries to search the knowledge base.")
    print("Type 'exit' or 'quit' to exit.\n")
    
    while True:
        try:
            query = input("Query: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break
            
            if not query:
                continue
            
            print("\n🔍 Searching...")
            result = rag.query(query, k=3)
            
            print("\n" + "=" * 60)
            print("Answer:")
            print("=" * 60)
            print(result['answer'])
            print()
            
            print(f"Retrieved {result['num_retrieved']} relevant documents")
            print("\nRetrieved Documents:")
            for i, doc in enumerate(result['retrieved_documents'], 1):
                print(f"\n[{i}] (Score: {doc['score']:.4f})")
                print(f"{doc['content'][:200]}...")
            print("\n" + "=" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()

