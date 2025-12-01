# RAG Model Application

A complete Retrieval-Augmented Generation (RAG) implementation with vector store and document retrieval. This application allows you to ask questions about your documents and get accurate, context-aware answers using advanced language models.

## 🚀 Features

- **Document Processing**: Support for PDF, TXT, and Markdown files
- **Vector Store**: FAISS and Chroma vector store options
- **Multiple Embeddings**: OpenAI and HuggingFace embedding models
- **Question Answering**: Ask questions about your documents
- **Source Citation**: View source documents for each answer
- **Chat History**: Track conversation history
- **Interactive UI**: Beautiful Streamlit interface

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key (for OpenAI embeddings and LLM)
- (Optional) HuggingFace models for free embeddings

## 🛠️ Installation

1. **Navigate to the project:**
   ```bash
   cd projects/RAG_Model
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: For FAISS, you may need:
   ```bash
   pip install faiss-cpu  # CPU version
   # OR
   pip install faiss-gpu  # GPU version (requires CUDA)
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (optional):

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Or set the API key directly in the Streamlit app's sidebar.

## 🚀 Usage

### Start the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using RAG

1. **Configure Settings**:
   - Enter your OpenAI API key in the sidebar
   - Choose embedding model (OpenAI or HuggingFace)
   - Select vector store type (FAISS or Chroma)
   - Choose LLM model (GPT-3.5-turbo, GPT-4, etc.)

2. **Upload Documents**:
   - Click "Upload documents" in the sidebar
   - Select PDF, TXT, or MD files
   - Click "Process Documents"

3. **Ask Questions**:
   - Type your question in the input field
   - Click "Ask" or press Enter
   - View the answer with source citations

## 🔍 How RAG Works

1. **Document Loading**: Documents are loaded and split into chunks
2. **Embedding**: Each chunk is converted to a vector embedding
3. **Vector Store**: Embeddings are stored in a vector database
4. **Retrieval**: When you ask a question, relevant chunks are retrieved
5. **Generation**: The LLM generates an answer using retrieved context

## 📚 Supported File Types

- **PDF**: `.pdf` files
- **Text**: `.txt` files
- **Markdown**: `.md` files

## 🎯 Embedding Models

### OpenAI Embeddings

- **Pros**: High quality, fast
- **Cons**: Requires API key, costs money
- **Best for**: Production applications

### HuggingFace Embeddings

- **Pros**: Free, runs locally
- **Cons**: Slower, requires more memory
- **Best for**: Development, privacy-sensitive applications

**Recommended Models**:
- `sentence-transformers/all-MiniLM-L6-v2` (default)
- `sentence-transformers/all-mpnet-base-v2` (better quality)

## 🗄️ Vector Stores

### FAISS

- **Pros**: Fast, efficient, Facebook-developed
- **Cons**: Less feature-rich
- **Best for**: Large-scale applications

### Chroma

- **Pros**: Feature-rich, easy to use
- **Cons**: Slightly slower
- **Best for**: Development, smaller applications

## 🔧 Advanced Configuration

### Chunk Size and Overlap

Modify in `app.py`:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Size of each chunk
    chunk_overlap=200,    # Overlap between chunks
    length_function=len
)
```

### Retrieval Parameters

Adjust the number of retrieved documents:

```python
retriever=vectorstore.as_retriever(search_kwargs={"k": 3})  # Retrieve top 3 chunks
```

### Custom Prompts

Modify the prompt template in `create_qa_chain()`:

```python
prompt_template = """Your custom prompt here...
Context: {context}
Question: {question}
Answer:"""
```

## 📊 Performance Tips

1. **Chunk Size**: Larger chunks = more context, but slower processing
2. **Retrieval Count**: More chunks = better answers, but slower generation
3. **Embedding Model**: OpenAI is faster but costs money
4. **Vector Store**: FAISS is faster for large document sets

## 🐛 Troubleshooting

### Import Errors

If you get import errors:

```bash
pip install --upgrade langchain openai faiss-cpu chromadb sentence-transformers
```

### Memory Issues

- Use smaller chunk sizes
- Use FAISS instead of Chroma
- Process fewer documents at once

### API Key Issues

- Verify your OpenAI API key is correct
- Check you have sufficient credits
- Ensure the key has proper permissions

### Slow Processing

- Use OpenAI embeddings (faster)
- Reduce chunk size
- Use FAISS vector store
- Process documents in batches

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add `OPENAI_API_KEY` as a secret
4. Deploy!

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📦 Project Structure

```
RAG_Model/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔗 Related Projects

- [CrewAI](../Crewai/README.md) - Multi-agent system
- [ChatUI](../ChatUi/README.md) - Chat interface
- [LiteLLM](../litellm/README.md) - LLM proxy server

## 📚 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Chroma Documentation](https://www.trychroma.com/)
- [RAG Paper](https://arxiv.org/abs/2005.11401)

## 📄 License

This project is part of the JJB Gallery portfolio. See the main repository LICENSE file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue in the main repository.
