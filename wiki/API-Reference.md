# API Reference

Complete API documentation for all projects with HTTP endpoints.

## RAG Model

### Python API

#### `RAGSystem`

```python
class RAGSystem:
    def __init__(
        self,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        vector_store_path: Optional[str] = None,
        llm_model: str = "llama3.1:8b",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    )
```

#### Methods

**`load_documents(file_paths: List[str]) -> List[str]`**

Load documents from file paths.

**`create_vector_store(documents: List[str], save: bool = True)`**

Create vector store from documents.

**`load_vector_store()`**

Load existing vector store.

**`retrieve(query: str, k: int = 5) -> List[Dict]`**

Retrieve relevant documents for a query.

**`generate(query: str, k: int = 5) -> str`**

Generate answer using RAG.

**`query(query: str, k: int = 5) -> Dict`**

Complete RAG query: retrieve and generate.

## Psychometrics

### Python API

#### `NASATLX`

```python
class NASATLX:
    def create_assessment(
        self,
        task_name: str,
        participant_id: Optional[str] = None
    ) -> TLXResult
    
    def add_rating(
        self,
        result: TLXResult,
        mental_demand: int,
        physical_demand: int,
        temporal_demand: int,
        performance: int,
        effort: int,
        frustration: int
    ) -> TLXResult
    
    def calculate_scores(self, result: TLXResult) -> TLXResult
    
    def get_statistics(self, task_name: Optional[str] = None) -> Dict
```

## ChatUi

### HTTP API

#### POST `/api/chat`

Send a chat message.

**Request:**

```json
{
  "message": "Hello, how are you?",
  "model": "gpt-3.5-turbo",
  "temperature": 0.7
}
```

**Response:**

```json
{
  "role": "assistant",
  "content": "I'm doing well, thank you!",
  "timestamp": "2024-01-15T10:30:00Z",
  "model": "gpt-3.5-turbo"
}
```

## iOS Chatbot

### HTTP API

#### POST `/api/chat`

Send a chat message.

**Request:**

```json
{
  "message": "Hello, how are you?",
  "conversation_id": "optional-conversation-id"
}
```

**Response:**

```json
{
  "conversation_id": "uuid-here",
  "response": {
    "role": "assistant",
    "content": "Hello! How can I help you?",
    "timestamp": "2024-01-15T10:30:00"
  },
  "message": {
    "role": "user",
    "content": "Hello, how are you?",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

#### GET `/api/conversations/<conversation_id>`

Get conversation history.

**Response:**

```json
{
  "conversation_id": "uuid-here",
  "messages": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-01-15T10:30:00"
    },
    {
      "role": "assistant",
      "content": "Hi there!",
      "timestamp": "2024-01-15T10:30:01"
    }
  ]
}
```

#### GET `/api/conversations`

List all conversations.

**Response:**

```json
{
  "conversations": [
    {
      "id": "uuid-1",
      "message_count": 5,
      "last_message": "2024-01-15T10:30:00"
    }
  ]
}
```

#### DELETE `/api/conversations/<conversation_id>`

Delete a conversation.

**Response:**

```json
{
  "success": true
}
```

#### GET `/api/health`

Health check.

**Response:**

```json
{
  "status": "healthy",
  "service": "ios-chatbot",
  "conversations": 10
}
```

## LiteLLM Proxy

### HTTP API

#### POST `/v1/chat/completions`

OpenAI-compatible chat completions.

**Request:**

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 100,
  "stream": false
}
```

**Response:**

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1677610602,
  "model": "gpt-3.5-turbo",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 8,
    "total_tokens": 18
  }
}
```

#### POST `/v1/completions`

Legacy completions endpoint.

**Request:**

```json
{
  "model": "gpt-3.5-turbo",
  "prompt": "Hello, world!",
  "temperature": 0.7,
  "max_tokens": 100
}
```

#### GET `/models`

List available models.

**Response:**

```json
{
  "data": [
    {
      "id": "gpt-3.5-turbo",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    }
  ],
  "object": "list"
}
```

#### GET `/health`

Health check.

**Response:**

```json
{
  "status": "healthy",
  "litellm_available": true
}
```

#### GET `/`

Root endpoint.

**Response:**

```json
{
  "service": "LiteLLM Proxy Server",
  "status": "running",
  "litellm_available": true
}
```

## CrewAI

### Python API

#### Command Line

```bash
# Setup
python main.py --setup

# Run swarm
python main.py --run <crew_type>

# Status
python main.py --status

# List crews
python main.py --list-crews
```

#### Programmatic

```python
from crews import MLCrew, ResearchCrew
from config import config

# Initialize crew
crew = MLCrew(process=config.PROCESS_TYPE)

# Execute
result = crew.kickoff()
```

### Web Interface

**Endpoint**: `http://localhost:8501` (Streamlit)

**Features**:

- Select swarm type
- Enter task description
- View progress
- Download results

## Terminal Agents

### Command Line API

```bash
# Interactive mode
python agent.py interactive

# Chat
python agent.py chat "message"

# Analyze
python agent.py analyze file.py

# Explain
python agent.py explain "code snippet"

# Generate
python agent.py generate "description"

# Fix
python agent.py fix file.py
```

## Error Responses

### Standard Error Format

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {}
}
```

### Common Error Codes

- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error
- `503`: Service Unavailable

## Rate Limiting

Some endpoints may have rate limiting:

- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`
- **Status**: `429 Too Many Requests`
- **Response**: `{"error": "Rate limit exceeded"}`

## Authentication

### API Keys

Most endpoints require API keys:

```bash
# Header
Authorization: Bearer <api_key>

# Or environment variable
export OPENAI_API_KEY=sk-...
```

### Master Keys (LiteLLM)

```bash
export LITELLM_MASTER_KEY=sk-1234
```

## Related Documentation

- [Project Overview](Project-Overview)
- [Configuration Guide](Configuration-Guide)
- [Architecture Overview](Architecture-Overview)
