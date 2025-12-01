"""
RAG (Retrieval-Augmented Generation) System
Implements a complete RAG pipeline with vector database, embeddings, and retrieval.
"""

import os
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import pickle
from datetime import datetime

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.llms import Ollama
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: langchain not available. Install with: pip install langchain faiss-cpu sentence-transformers")

try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class RAGSystem:
    """
    A complete RAG system that handles document ingestion, embedding, 
    vector storage, and retrieval-augmented generation.
    """
    
    def __init__(
        self,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        vector_store_path: Optional[str] = None,
        llm_model: str = "llama3.1:8b",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize the RAG system.
        
        Args:
            embedding_model: Model name for embeddings
            vector_store_path: Path to save/load vector store
            llm_model: LLM model name (for Ollama)
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.embedding_model_name = embedding_model
        self.vector_store_path = vector_store_path or "vector_store"
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize components
        self.text_splitter = None
        self.embeddings = None
        self.vector_store = None
        self.qa_chain = None
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize text splitter and embeddings."""
        if LANGCHAIN_AVAILABLE:
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
            )
            
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model_name
            )
        elif SENTENCE_TRANSFORMERS_AVAILABLE:
            print("Using sentence-transformers directly (langchain not available)")
            self.embeddings_model = SentenceTransformer(self.embedding_model_name)
        else:
            raise ImportError(
                "Neither langchain nor sentence-transformers available. "
                "Install at least one: pip install sentence-transformers"
            )
    
    def load_documents(self, file_paths: List[str]) -> List[str]:
        """
        Load documents from file paths.
        
        Args:
            file_paths: List of file paths to load
            
        Returns:
            List of document texts
        """
        documents = []
        for file_path in file_paths:
            path = Path(file_path)
            if not path.exists():
                print(f"Warning: File not found: {file_path}")
                continue
            
            try:
                if path.suffix == '.txt':
                    with open(path, 'r', encoding='utf-8') as f:
                        documents.append(f.read())
                elif path.suffix == '.md':
                    with open(path, 'r', encoding='utf-8') as f:
                        documents.append(f.read())
                elif path.suffix == '.json':
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        documents.append(json.dumps(data, indent=2))
                else:
                    print(f"Warning: Unsupported file type: {path.suffix}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        return documents
    
    def create_vector_store(self, documents: List[str], save: bool = True):
        """
        Create vector store from documents.
        
        Args:
            documents: List of document texts
            save: Whether to save the vector store
        """
        if not documents:
            raise ValueError("No documents provided")
        
        if LANGCHAIN_AVAILABLE:
            # Split documents
            texts = self.text_splitter.create_documents(documents)
            
            # Create vector store
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
            
            if save:
                self.vector_store.save_local(self.vector_store_path)
                print(f"Vector store saved to {self.vector_store_path}")
        else:
            # Fallback: simple chunking and embedding
            chunks = []
            for doc in documents:
                for i in range(0, len(doc), self.chunk_size - self.chunk_overlap):
                    chunk = doc[i:i + self.chunk_size]
                    chunks.append(chunk)
            
            # Create embeddings
            embeddings = self.embeddings_model.encode(chunks)
            
            # Store in simple format
            store_data = {
                'chunks': chunks,
                'embeddings': embeddings.tolist(),
                'model': self.embedding_model_name,
                'created_at': datetime.now().isoformat()
            }
            
            os.makedirs(self.vector_store_path, exist_ok=True)
            with open(f"{self.vector_store_path}/store.pkl", 'wb') as f:
                pickle.dump(store_data, f)
            
            self.vector_store = store_data
            print(f"Vector store saved to {self.vector_store_path}/store.pkl")
    
    def load_vector_store(self):
        """Load existing vector store."""
        if LANGCHAIN_AVAILABLE:
            if os.path.exists(self.vector_store_path):
                self.vector_store = FAISS.load_local(
                    self.vector_store_path,
                    self.embeddings
                )
                print(f"Vector store loaded from {self.vector_store_path}")
            else:
                raise FileNotFoundError(
                    f"Vector store not found at {self.vector_store_path}"
                )
        else:
            store_path = f"{self.vector_store_path}/store.pkl"
            if os.path.exists(store_path):
                with open(store_path, 'rb') as f:
                    self.vector_store = pickle.load(f)
                print(f"Vector store loaded from {store_path}")
            else:
                raise FileNotFoundError(f"Vector store not found at {store_path}")
    
    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Query string
            k: Number of documents to retrieve
            
        Returns:
            List of relevant document chunks with metadata
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Load or create one first.")
        
        if LANGCHAIN_AVAILABLE:
            docs = self.vector_store.similarity_search_with_score(query, k=k)
            return [
                {
                    'content': doc.page_content,
                    'score': float(score),
                    'metadata': doc.metadata
                }
                for doc, score in docs
            ]
        else:
            # Simple cosine similarity search
            query_embedding = self.embeddings_model.encode([query])[0]
            embeddings = np.array(self.vector_store['embeddings'])
            
            # Calculate cosine similarity
            scores = np.dot(embeddings, query_embedding) / (
                np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            
            # Get top k
            top_indices = np.argsort(scores)[::-1][:k]
            
            return [
                {
                    'content': self.vector_store['chunks'][idx],
                    'score': float(scores[idx]),
                    'metadata': {'index': int(idx)}
                }
                for idx in top_indices
            ]
    
    def generate(self, query: str, k: int = 5) -> str:
        """
        Generate answer using RAG.
        
        Args:
            query: Query string
            k: Number of documents to retrieve
            
        Returns:
            Generated answer
        """
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(query, k=k)
        
        # Build context
        context = "\n\n".join([
            f"[Document {i+1}]: {doc['content']}"
            for i, doc in enumerate(retrieved_docs)
        ])
        
        # Create prompt
        prompt = f"""Based on the following context, answer the question.
If the answer is not in the context, say so.

Context:
{context}

Question: {query}

Answer:"""
        
        # Generate answer (simplified - in production, use proper LLM)
        if LANGCHAIN_AVAILABLE:
            try:
                llm = Ollama(model=self.llm_model)
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=self.vector_store.as_retriever(search_kwargs={"k": k}),
                    return_source_documents=True
                )
                result = qa_chain({"query": query})
                return result['result']
            except Exception as e:
                print(f"Error with LLM: {e}")
                return f"Retrieved context:\n\n{context}\n\nQuestion: {query}\n\n(LLM generation failed - showing retrieved context only)"
        else:
            return f"Retrieved context:\n\n{context}\n\nQuestion: {query}\n\n(Install langchain and Ollama for full generation)"
    
    def query(self, query: str, k: int = 5) -> Dict:
        """
        Complete RAG query: retrieve and generate.
        
        Args:
            query: Query string
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with answer and retrieved documents
        """
        retrieved_docs = self.retrieve(query, k=k)
        answer = self.generate(query, k=k)
        
        return {
            'query': query,
            'answer': answer,
            'retrieved_documents': retrieved_docs,
            'num_retrieved': len(retrieved_docs)
        }

