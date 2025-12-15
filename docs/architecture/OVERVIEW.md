# System Architecture Overview

This document provides a high-level overview of the JJB Gallery system architecture.

## High-Level Design

The system is composed of loose coupled components communicating via REST APIs and WebSockets.

```mermaid
graph TD
    Client[Client Browser/Mobile] --> LB[Load Balancer]
    LB --> ChatUi[Chat UI (SvelteKit)]
    LB --> iOSChat[iOS Chatbot (Flask)]
    
    ChatUi --> LiteLLM[LiteLLM Proxy]
    iOSChat --> LiteLLM
    
    LiteLLM --> OpenAI[OpenAI API]
    LiteLLM --> Anthropic[Anthropic API]
    LiteLLM --> Ollama[Local Ollama]
    
    Client --> RAG[RAG Service]
    RAG --> VectorDB[(FAISS Vector DB)]
    RAG --> LiteLLM
    
    Client --> CrewAI[CrewAI Swarm]
    CrewAI --> LiteLLM
```

## Component Description

### 1. Frontend Interfaces

- **Chat UI**: A SvelteKit-based modern web interface. Handles real-time chat state and rendering.
- **iOS Chatbot**: A Flask-based mobile-responsive interface mimicking iOS design patterns.

### 2. Middleware / Orchestration

- **LiteLLM Proxy**: Centralized gateway for all LLM calls. Handles auth, logging, rate limiting, and provider abstraction.
- **CrewAI System**: Manages multi-agent workflows, delegating tasks to specific agent roles.

### 3. Backend Services

- **RAG Service**: Handles document ingestion, embedding generation, and semantic retrieval.
- **Terminal Agents**: Standalone CLI tools for developer assistance.

### 4. Data Layer

- **Vector Database**: FAISS (Facebook AI Similarity Search) for storing and retrieving high-dimensional embeddings.
- **File System**: Used for document storage, caching, and configuration.
- **External Storage**: Configured to offload large dependencies and model weights.

## Data Flow

1. **User Request**: User sends a prompt via Chat UI.
2. **Orchestration**: Chat UI sends request to LiteLLM Proxy.
3. **Inference**: LiteLLM routes request to appropriate provider (e.g., OpenAI).
4. **Response**: Provider returns token stream.
5. **Delivery**: LiteLLM streams tokens back to Chat UI via WebSocket/SSE.

## Security Architecture

- **Transport**: TLS/SSL for all external communication.
- **Authentication**: API Key validation at the Proxy level.
- **Isolation**: Components run in isolated Docker containers.

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
