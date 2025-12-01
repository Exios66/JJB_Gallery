"""
Retrieval-Augmented Generation (RAG) Model Application
A complete RAG implementation with vector store and document retrieval.
"""

import streamlit as st
import os
from pathlib import Path
from typing import List, Dict, Optional
import tempfile
import pickle

# LangChain imports
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.vectorstores import FAISS, Chroma
    from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
    from langchain.llms import OpenAI
    from langchain.chains import RetrievalQA
    from langchain.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import PromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    st.error("⚠️ LangChain not installed. Please install: pip install langchain openai faiss-cpu chromadb")

# Page configuration
st.set_page_config(
    page_title="RAG Model",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .info-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "documents" not in st.session_state:
    st.session_state.documents = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def load_documents(file_paths: List[str]) -> List:
    """Load documents from file paths."""
    documents = []
    
    for file_path in file_paths:
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif file_ext in [".txt", ".md"]:
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            st.warning(f"Unsupported file type: {file_ext}")
            continue
        
        docs = loader.load()
        documents.extend(docs)
    
    return documents

def create_vectorstore(documents: List, embedding_model: str, vectorstore_type: str = "faiss"):
    """Create a vector store from documents."""
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    splits = text_splitter.split_documents(documents)
    
    # Create embeddings
    if embedding_model == "openai":
        embeddings = OpenAIEmbeddings(openai_api_key=st.session_state.openai_key)
    else:
        # Use HuggingFace embeddings
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    # Create vector store
    if vectorstore_type == "faiss":
        vectorstore = FAISS.from_documents(splits, embeddings)
    else:
        vectorstore = Chroma.from_documents(splits, embeddings)
    
    return vectorstore, splits

def create_qa_chain(vectorstore, llm_model: str = "gpt-3.5-turbo"):
    """Create a QA chain from vector store."""
    # Create LLM
    if llm_model.startswith("gpt"):
        llm = ChatOpenAI(
            model_name=llm_model,
            temperature=0,
            openai_api_key=st.session_state.openai_key
        )
    else:
        llm = OpenAI(
            model_name=llm_model,
            temperature=0,
            openai_api_key=st.session_state.openai_key
        )
    
    # Create prompt template
    prompt_template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )
    
    return qa_chain

def main():
    if not LANGCHAIN_AVAILABLE:
        st.error("Please install required packages: pip install langchain openai faiss-cpu chromadb sentence-transformers")
        return
    
    st.markdown('<div class="main-header"><h1>🔍 Retrieval-Augmented Generation (RAG) Model</h1></div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key
        openai_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.get("openai_key", os.getenv("OPENAI_API_KEY", "")),
            type="password"
        )
        st.session_state.openai_key = openai_key
        
        # Embedding model
        embedding_model = st.selectbox(
            "Embedding Model",
            ["openai", "huggingface"],
            help="OpenAI embeddings are more accurate but require API key. HuggingFace is free but slower."
        )
        
        # Vector store type
        vectorstore_type = st.selectbox(
            "Vector Store",
            ["faiss", "chroma"],
            help="FAISS is faster, Chroma is more feature-rich"
        )
        
        # LLM model
        llm_model = st.selectbox(
            "LLM Model",
            ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"],
            help="Model for generating answers"
        )
        
        # Document upload
        st.header("📄 Documents")
        uploaded_files = st.file_uploader(
            "Upload documents",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True
        )
        
        if st.button("Process Documents", type="primary"):
            if not uploaded_files:
                st.error("Please upload at least one document.")
                return
            
            if not openai_key and embedding_model == "openai":
                st.error("OpenAI API key required for OpenAI embeddings.")
                return
            
            with st.spinner("Processing documents..."):
                # Save uploaded files temporarily
                temp_files = []
                for uploaded_file in uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                        tmp.write(uploaded_file.read())
                        temp_files.append(tmp.name)
                
                # Load documents
                documents = load_documents(temp_files)
                st.session_state.documents = documents
                
                # Create vector store
                vectorstore, splits = create_vectorstore(
                    documents,
                    embedding_model,
                    vectorstore_type
                )
                st.session_state.vectorstore = vectorstore
                
                # Create QA chain
                if openai_key:
                    qa_chain = create_qa_chain(vectorstore, llm_model)
                    st.session_state.qa_chain = qa_chain
                
                st.success(f"✅ Processed {len(documents)} documents, {len(splits)} chunks created!")
                
                # Cleanup temp files
                for tmp_file in temp_files:
                    os.unlink(tmp_file)
        
        if st.button("Clear All"):
            st.session_state.vectorstore = None
            st.session_state.documents = []
            st.session_state.qa_chain = None
            st.session_state.chat_history = []
            st.rerun()
    
    # Main content area
    if st.session_state.vectorstore is None:
        st.info("""
        👋 Welcome to the RAG Model Application!
        
        **Getting Started:**
        1. Configure your settings in the sidebar
        2. Upload documents (PDF, TXT, or MD files)
        3. Click "Process Documents" to create the vector store
        4. Start asking questions!
        
        **What is RAG?**
        Retrieval-Augmented Generation combines document retrieval with language model generation.
        It allows you to ask questions about your documents and get accurate, context-aware answers.
        """)
    else:
        # Chat interface
        st.header("💬 Ask Questions")
        
        # Display chat history
        for i, (question, answer, sources) in enumerate(st.session_state.chat_history):
            with st.expander(f"Q: {question}", expanded=(i == len(st.session_state.chat_history) - 1)):
                st.write("**Answer:**")
                st.write(answer)
                if sources:
                    st.write("**Sources:**")
                    for j, source in enumerate(sources[:3], 1):
                        st.write(f"{j}. {source.page_content[:200]}...")
        
        # Question input
        question = st.text_input("Enter your question:", key="question_input")
        
        if st.button("Ask", type="primary") or question:
            if not question:
                st.warning("Please enter a question.")
                return
            
            if not st.session_state.qa_chain:
                st.error("QA chain not initialized. Please process documents with OpenAI API key.")
                return
            
            with st.spinner("Searching documents and generating answer..."):
                # Get answer
                result = st.session_state.qa_chain({"query": question})
                
                answer = result["result"]
                sources = result.get("source_documents", [])
                
                # Add to chat history
                st.session_state.chat_history.append((question, answer, sources))
                
                # Display answer
                st.success("Answer generated!")
                st.write("**Answer:**")
                st.write(answer)
                
                if sources:
                    st.write("**Relevant Sources:**")
                    for i, source in enumerate(sources[:3], 1):
                        with st.expander(f"Source {i}"):
                            st.write(source.page_content)
                            if hasattr(source, "metadata"):
                                st.caption(f"Source: {source.metadata.get('source', 'Unknown')}")
                
                st.rerun()
        
        # Document statistics
        with st.expander("📊 Document Statistics"):
            st.write(f"**Total Documents:** {len(st.session_state.documents)}")
            st.write(f"**Vector Store Type:** {vectorstore_type.upper()}")
            st.write(f"**Embedding Model:** {embedding_model}")
            st.write(f"**LLM Model:** {llm_model}")

if __name__ == "__main__":
    main()

