#!/usr/bin/env python3
"""
LiteLLM Proxy Server
A simple proxy server using LiteLLM to unify LLM API calls.
"""

import os
import sys
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

try:
    from litellm import completion, acompletion
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    print("Warning: litellm not available. Install with: pip install litellm")


app = FastAPI(title="LiteLLM Proxy Server")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list
    usage: Optional[dict] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "LiteLLM Proxy Server",
        "status": "running",
        "litellm_available": LITELLM_AVAILABLE
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "litellm_available": LITELLM_AVAILABLE}


@app.get("/models")
async def list_models():
    """List available models."""
    # Return common models - customize based on your setup
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
            "id": "claude-3-sonnet-20240229",
            "object": "model",
            "created": 1677610602,
            "owned_by": "anthropic"
        },
        {
            "id": "llama3.1:8b",
            "object": "model",
            "created": 1677610602,
            "owned_by": "ollama"
        }
    ]
    return {"data": models, "object": "list"}


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """
    Chat completions endpoint compatible with OpenAI API.
    """
    if not LITELLM_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="LiteLLM not available. Install with: pip install litellm"
        )
    
    try:
        # Convert messages to dict format
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Prepare parameters
        params = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
        }
        
        if request.max_tokens:
            params["max_tokens"] = request.max_tokens
        
        # Handle streaming
        if request.stream:
            async def generate():
                try:
                    response = await acompletion(**params, stream=True)
                    async for chunk in response:
                        yield f"data: {chunk.model_dump_json()}\n\n"
                    yield "data: [DONE]\n\n"
                except Exception as e:
                    yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
            
            return StreamingResponse(generate(), media_type="text/event-stream")
        
        # Non-streaming response
        response = completion(**params)
        
        # Format response in OpenAI-compatible format
        return {
            "id": f"chatcmpl-{hash(str(response))}",
            "object": "chat.completion",
            "created": 1677610602,
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
                "prompt_tokens": 0,  # LiteLLM doesn't always provide this
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/completions")
async def completions(request: dict):
    """
    Legacy completions endpoint (for non-chat models).
    """
    if not LITELLM_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="LiteLLM not available"
        )
    
    try:
        response = completion(
            model=request.get("model", "gpt-3.5-turbo"),
            prompt=request.get("prompt", ""),
            temperature=request.get("temperature", 0.7),
            max_tokens=request.get("max_tokens")
        )
        
        return {
            "id": f"cmpl-{hash(str(response))}",
            "object": "text_completion",
            "created": 1677610602,
            "model": request.get("model"),
            "choices": [{
                "text": response.choices[0].text,
                "index": 0,
                "finish_reason": "stop"
            }]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting LiteLLM Proxy Server on {host}:{port}")
    print(f"LiteLLM Available: {LITELLM_AVAILABLE}")
    
    if not LITELLM_AVAILABLE:
        print("\n⚠️  Warning: LiteLLM not installed!")
        print("Install with: pip install litellm")
        print("Or install with proxy extras: pip install 'litellm[proxy]'")
    
    uvicorn.run(app, host=host, port=port)

