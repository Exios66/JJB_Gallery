"""
LLM Provider System for Terminal Agents.
Supports multiple LLM providers with a unified interface.
"""

import os
from typing import Optional, List, Dict, Any, Iterator
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Base class for LLM providers."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize provider with configuration."""
        self.config = config
        self.provider_name = "Unknown"
        self.model_name = "Unknown"
        self.supports_streaming = False
    
    @abstractmethod
    def chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        """Send a chat message and get response.
        
        Args:
            message: User message
            history: Conversation history
            
        Returns:
            Response text
        """
        pass
    
    @abstractmethod
    def stream_chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> Iterator[str]:
        """Stream chat response.
        
        Args:
            message: User message
            history: Conversation history
            
        Yields:
            Response chunks
        """
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI provider."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=config.get("api_key"),
                base_url=config.get("api_base") or None
            )
            self.provider_name = "OpenAI"
            self.model_name = config.get("model", "gpt-4o-mini")
            self.supports_streaming = True
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI: {e}")
    
    def chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        """Send chat message."""
        messages = []
        
        # Add history if provided
        if history:
            messages.extend(history[:-1])  # All but last user message
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")
    
    def stream_chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> Iterator[str]:
        """Stream chat response."""
        messages = []
        
        if history:
            messages.extend(history[:-1])
        
        messages.append({"role": "user", "content": message})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise Exception(f"OpenAI streaming error: {e}")


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=config.get("api_key"))
            self.provider_name = "Anthropic"
            self.model_name = config.get("model", "claude-3-5-sonnet-20241022")
            self.supports_streaming = True
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")
        except Exception as e:
            raise Exception(f"Failed to initialize Anthropic: {e}")
    
    def chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        """Send chat message."""
        # Anthropic uses different message format
        system_message = ""
        messages = []
        
        if history:
            # Convert history to Anthropic format
            for msg in history[:-1]:
                if msg["role"] == "assistant":
                    messages.append({"role": "assistant", "content": msg["content"]})
                elif msg["role"] == "user":
                    messages.append({"role": "user", "content": msg["content"]})
        
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=4096,
                system=system_message,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {e}")
    
    def stream_chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> Iterator[str]:
        """Stream chat response."""
        system_message = ""
        messages = []
        
        if history:
            for msg in history[:-1]:
                if msg["role"] == "assistant":
                    messages.append({"role": "assistant", "content": msg["content"]})
                elif msg["role"] == "user":
                    messages.append({"role": "user", "content": msg["content"]})
        
        messages.append({"role": "user", "content": message})
        
        try:
            with self.client.messages.stream(
                model=self.model_name,
                max_tokens=4096,
                system=system_message,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            raise Exception(f"Anthropic streaming error: {e}")


class OllamaProvider(LLMProvider):
    """Ollama provider (free, local)."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        try:
            from langchain_community.llms import Ollama
            self.llm = Ollama(
                model=config.get("model", "llama3.1:8b"),
                base_url=config.get("base_url", "http://localhost:11434"),
                temperature=0.7
            )
            self.provider_name = "Ollama"
            self.model_name = config.get("model", "llama3.1:8b")
            self.supports_streaming = True
        except ImportError:
            raise ImportError("langchain-community not installed. Install with: pip install langchain-community")
        except Exception as e:
            raise Exception(f"Failed to initialize Ollama: {e}")
    
    def chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        """Send chat message."""
        # Build prompt from history
        prompt = self._build_prompt(message, history)
        try:
            response = self.llm.invoke(prompt)
            return str(response)
        except Exception as e:
            raise Exception(f"Ollama error: {e}")
    
    def stream_chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> Iterator[str]:
        """Stream chat response."""
        prompt = self._build_prompt(message, history)
        try:
            for chunk in self.llm.stream(prompt):
                yield str(chunk)
        except Exception as e:
            raise Exception(f"Ollama streaming error: {e}")
    
    def _build_prompt(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        """Build prompt from message and history."""
        if not history:
            return message
        
        # Simple prompt building for Ollama
        prompt_parts = []
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            prompt_parts.append(f"{role}: {msg['content']}")
        
        prompt_parts.append(f"User: {message}")
        prompt_parts.append("Assistant:")
        
        return "\n\n".join(prompt_parts)


def get_llm_provider(
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    config: Any = None
) -> Optional[LLMProvider]:
    """Get initialized LLM provider.
    
    Args:
        provider: Provider name (auto-detect if None)
        api_key: API key (overrides config)
        model: Model name (overrides config)
        config: TerminalAgentConfig instance
        
    Returns:
        Initialized LLMProvider or None
    """
    if not config:
        from config import TerminalAgentConfig
        config = TerminalAgentConfig()
    
    # Determine provider
    if not provider:
        provider = config.detect_best_provider()
    
    if not provider:
        print("❌ No LLM provider available. Please configure at least one provider.")
        return None
    
    # Get provider configuration
    provider_config = config.get_provider_config(provider)
    
    # Override with provided values
    if api_key:
        provider_config["api_key"] = api_key
    if model:
        provider_config["model"] = model
    
    # Initialize provider
    try:
        if provider == "openai":
            return OpenAIProvider(provider_config)
        elif provider == "anthropic":
            return AnthropicProvider(provider_config)
        elif provider == "ollama":
            return OllamaProvider(provider_config)
        else:
            print(f"❌ Unknown provider: {provider}")
            return None
    except Exception as e:
        print(f"❌ Failed to initialize {provider}: {e}")
        return None

