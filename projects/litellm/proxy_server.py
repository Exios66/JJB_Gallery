"""
LiteLLM Proxy Server
A unified proxy server for multiple LLM providers using LiteLLM.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import litellm
from litellm import completion, acompletion
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LiteLLM Proxy Server",
    description="Unified proxy for multiple LLM providers",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    model: str = Field(..., description="Model identifier")
    messages: list[ChatMessage] = Field(..., description="List of chat messages")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    stream: Optional[bool] = Field(False, description="Whether to stream responses")

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[Dict[str, Any]]
    usage: Optional[Dict[str, int]] = None

# Configuration
class Config:
    """Configuration management for LiteLLM proxy."""
    
    @staticmethod
    def load_environment():
        """Load environment variables for LLM providers."""
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            litellm.openai_key = os.getenv("OPENAI_API_KEY")
            logger.info("✅ OpenAI API key configured")
        
        # Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            litellm.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            logger.info("✅ Anthropic API key configured")
        
        # Google
        if os.getenv("GOOGLE_API_KEY"):
            litellm.google_key = os.getenv("GOOGLE_API_KEY")
            logger.info("✅ Google API key configured")
        
        # Azure OpenAI
        if os.getenv("AZURE_OPENAI_API_KEY"):
            litellm.azure_key = os.getenv("AZURE_OPENAI_API_KEY")
            litellm.azure_api_base = os.getenv("AZURE_OPENAI_API_BASE", "")
            litellm.azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
            logger.info("✅ Azure OpenAI configured")
        
        # Cohere
        if os.getenv("COHERE_API_KEY"):
            litellm.cohere_key = os.getenv("COHERE_API_KEY")
            logger.info("✅ Cohere API key configured")
        
        # HuggingFace
        if os.getenv("HUGGINGFACE_API_KEY"):
            litellm.huggingface_key = os.getenv("HUGGINGFACE_API_KEY")
            logger.info("✅ HuggingFace API key configured")
        
        # Set default settings
        litellm.set_verbose = os.getenv("LITELLM_VERBOSE", "false").lower() == "true"
        litellm.drop_params = True

# Load configuration on startup
Config.load_environment()

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "LiteLLM Proxy Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/v1/chat/completions",
            "health": "/health",
            "models": "/v1/models"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "litellm-proxy"}

@app.get("/v1/models")
async def list_models():
    """List available models."""
    models = [
        {
            "id": "gpt-3.5-turbo",
            "object": "model",
            "created": 1677610602,
            "owned_by": "openai"
        },
        {
            "id": "gpt-4",
            "object": "model",
            "created": 1677610602,
            "owned_by": "openai"
        },
        {
            "id": "claude-3-opus-20240229",
            "object": "model",
            "created": 1677610602,
            "owned_by": "anthropic"
        },
        {
            "id": "claude-3-sonnet-20240229",
            "object": "model",
            "created": 1677610602,
            "owned_by": "anthropic"
        },
        {
            "id": "gemini-pro",
            "object": "model",
            "created": 1677610602,
            "owned_by": "google"
        }
    ]
    return {"object": "list", "data": models}

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """Chat completions endpoint compatible with OpenAI API."""
    try:
        # Convert messages to LiteLLM format
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Prepare parameters
        params = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
        }
        
        if request.max_tokens:
            params["max_tokens"] = request.max_tokens
        
        # Call LiteLLM
        if request.stream:
            # Streaming response
            def generate():
                response = completion(**params, stream=True)
                for chunk in response:
                    yield f"data: {chunk.model_dump_json()}\n\n"
                yield "data: [DONE]\n\n"
            
            from fastapi.responses import StreamingResponse
            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            # Non-streaming response
            response = completion(**params)
            
            # Format response to match OpenAI API format
            return {
                "id": f"chatcmpl-{response.id if hasattr(response, 'id') else 'default'}",
                "object": "chat.completion",
                "created": int(response.created) if hasattr(response, 'created') else 0,
                "model": request.model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response.choices[0].message.content
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if hasattr(response, 'usage') else 0,
                    "completion_tokens": response.usage.completion_tokens if hasattr(response, 'usage') else 0,
                    "total_tokens": response.usage.total_tokens if hasattr(response, 'usage') else 0
                } if hasattr(response, 'usage') else None
            }
    
    except Exception as e:
        logger.error(f"Error in chat completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": {"message": str(exc), "type": "internal_error"}}
    )

def main():
    """Main entry point for the proxy server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="LiteLLM Proxy Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Starting LiteLLM Proxy Server on {args.host}:{args.port}")
    
    uvicorn.run(
        "proxy_server:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()

