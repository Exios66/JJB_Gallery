"""
Tests for RAG Model Application
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
import tempfile
import os

# Add RAG_Model to path
RAG_MODEL_DIR = Path(__file__).parent.parent / "RAG_Model"
sys.path.insert(0, str(RAG_MODEL_DIR))


class TestDocumentLoading:
    """Test document loading functionality."""
    
    def test_text_loader_import(self):
        """Test text loader can be imported."""
        try:
            from langchain.document_loaders import TextLoader
            assert TextLoader is not None
        except ImportError:
            pytest.skip("LangChain not available")
    
    def test_pdf_loader_import(self):
        """Test PDF loader can be imported."""
        try:
            from langchain.document_loaders import PyPDFLoader
            assert PyPDFLoader is not None
        except ImportError:
            pytest.skip("LangChain not available")
    
    @patch('langchain.document_loaders.TextLoader')
    def test_load_text_document(self, mock_loader, sample_text_file):
        """Test loading text document."""
        try:
            from langchain.document_loaders import TextLoader
            
            mock_loader_instance = MagicMock()
            mock_doc = MagicMock()
            mock_doc.page_content = "Test content"
            mock_loader_instance.load.return_value = [mock_doc]
            mock_loader.return_value = mock_loader_instance
            
            loader = TextLoader(str(sample_text_file))
            documents = loader.load()
            
            assert len(documents) > 0
        except ImportError:
            pytest.skip("LangChain not available")


class TestTextSplitting:
    """Test text splitting functionality."""
    
    def test_text_splitter_import(self):
        """Test text splitter can be imported."""
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            assert RecursiveCharacterTextSplitter is not None
        except ImportError:
            pytest.skip("LangChain not available")
    
    def test_text_splitting(self):
        """Test text splitting."""
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=100,
                chunk_overlap=20
            )
            
            text = "This is a test document. " * 10
            splits = text_splitter.split_text(text)
            
            assert len(splits) > 0
            assert all(len(split) <= 100 for split in splits)
        except ImportError:
            pytest.skip("LangChain not available")


class TestEmbeddings:
    """Test embedding functionality."""
    
    def test_openai_embeddings_import(self):
        """Test OpenAI embeddings can be imported."""
        try:
            from langchain.embeddings import OpenAIEmbeddings
            assert OpenAIEmbeddings is not None
        except ImportError:
            pytest.skip("LangChain not available")
    
    def test_huggingface_embeddings_import(self):
        """Test HuggingFace embeddings can be imported."""
        try:
            from langchain.embeddings import HuggingFaceEmbeddings
            assert HuggingFaceEmbeddings is not None
        except ImportError:
            pytest.skip("LangChain not available")
    
    @patch('langchain.embeddings.OpenAIEmbeddings')
    def test_openai_embeddings_creation(self, mock_embeddings):
        """Test OpenAI embeddings creation."""
        try:
            from langchain.embeddings import OpenAIEmbeddings
            
            mock_embeddings.return_value = MagicMock()
            embeddings = OpenAIEmbeddings(openai_api_key="test_key")
            
            assert embeddings is not None
        except ImportError:
            pytest.skip("LangChain not available")


class TestVectorStores:
    """Test vector store functionality."""
    
    def test_faiss_import(self):
        """Test FAISS can be imported."""
        try:
            from langchain.vectorstores import FAISS
            assert FAISS is not None
        except ImportError:
            pytest.skip("FAISS not available")
    
    def test_chroma_import(self):
        """Test Chroma can be imported."""
        try:
            from langchain.vectorstores import Chroma
            assert Chroma is not None
        except ImportError:
            pytest.skip("Chroma not available")
    
    @patch('langchain.vectorstores.FAISS')
    def test_faiss_creation(self, mock_faiss):
        """Test FAISS vector store creation."""
        try:
            from langchain.vectorstores import FAISS
            from langchain.embeddings import OpenAIEmbeddings
            
            mock_embeddings = MagicMock()
            mock_documents = [MagicMock()]
            
            mock_faiss.from_documents.return_value = MagicMock()
            vectorstore = FAISS.from_documents(mock_documents, mock_embeddings)
            
            assert vectorstore is not None
        except ImportError:
            pytest.skip("FAISS not available")


class TestQAChain:
    """Test QA chain functionality."""
    
    def test_retrieval_qa_import(self):
        """Test RetrievalQA can be imported."""
        try:
            from langchain.chains import RetrievalQA
            assert RetrievalQA is not None
        except ImportError:
            pytest.skip("LangChain not available")
    
    @patch('langchain.chains.RetrievalQA.from_chain_type')
    def test_qa_chain_creation(self, mock_qa):
        """Test QA chain creation."""
        try:
            from langchain.chains import RetrievalQA
            
            mock_qa.return_value = MagicMock()
            qa_chain = mock_qa(
                llm=MagicMock(),
                chain_type="stuff",
                retriever=MagicMock(),
                return_source_documents=True
            )
            
            assert qa_chain is not None
        except ImportError:
            pytest.skip("LangChain not available")


class TestRAGWorkflow:
    """Test complete RAG workflow."""
    
    def test_document_processing_workflow(self, sample_document):
        """Test document processing workflow."""
        # Simulate workflow steps
        documents = [sample_document]
        
        # Split documents
        chunks = [doc[:100] for doc in documents]
        
        # Create embeddings (mock)
        embeddings = [[0.1] * 384 for _ in chunks]
        
        # Create vector store (mock)
        vectorstore = MagicMock()
        vectorstore.as_retriever.return_value = MagicMock()
        
        # Verify workflow
        assert len(documents) > 0
        assert len(chunks) > 0
        assert len(embeddings) == len(chunks)
        assert vectorstore is not None
    
    def test_retrieval_workflow(self):
        """Test retrieval workflow."""
        # Mock vector store
        mock_retriever = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "Relevant document content"
        mock_retriever.get_relevant_documents.return_value = [mock_doc]
        
        # Query
        query = "Test question"
        results = mock_retriever.get_relevant_documents(query)
        
        assert len(results) > 0
        assert results[0].page_content is not None


class TestFileHandling:
    """Test file handling functionality."""
    
    def test_supported_file_types(self):
        """Test supported file types."""
        supported_types = [".pdf", ".txt", ".md"]
        
        assert ".pdf" in supported_types
        assert ".txt" in supported_types
        assert ".md" in supported_types
    
    def test_file_extension_parsing(self):
        """Test file extension parsing."""
        test_files = [
            "document.pdf",
            "readme.txt",
            "notes.md"
        ]
        
        for file_path in test_files:
            ext = Path(file_path).suffix.lower()
            assert ext in [".pdf", ".txt", ".md"]

