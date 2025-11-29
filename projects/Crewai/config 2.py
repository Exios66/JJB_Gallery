"""
Configuration module for CrewAI ML Agent Swarm.
Handles environment variables, API keys, and system configuration.
Supports multiple LLM providers with priority on free/open-source options.
"""

import os
from pathlib import Path
from typing import Dict, Optional, List, Tuple
import socket


class Config:
    """Configuration class for CrewAI system with multi-provider LLM support."""

    # ==================== Provider Selection ====================
    # Priority order: free/open-source first, then paid
    # Set LLM_PROVIDER to override auto-detection: "ollama", "openai", "anthropic", "google", "azure"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "").lower()  # Empty = auto-detect

    # ==================== Ollama (Free/Local) ====================
    # Ollama is prioritized as it's free and runs locally
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")  # Free, local model
    # Alternative free models: "mistral:7b", "codellama:13b", "phi3:mini", "qwen2.5:7b"

    # ==================== OpenAI (Paid) ====================
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "")  # For OpenAI-compatible APIs
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")  # More affordable default

    # ==================== Anthropic Claude (Paid) ====================
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

    # ==================== Google Gemini (Paid/Free tier) ====================
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-pro")

    # ==================== Azure OpenAI (Paid) ====================
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    # ==================== Other Tools ====================
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")  # Web search (free tier available)
    
    # ==================== System Configuration ====================
    VERBOSE: bool = os.getenv("VERBOSE", "true").lower() == "true"
    PROCESS_TYPE: str = os.getenv("PROCESS_TYPE", "sequential")

    # Output Configuration
    OUTPUTS_DIR: Path = Path(__file__).parent.parent.parent / "outputs"
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_output_path(cls, filename: str) -> str:
        """Get the full path for an output file.

        Args:
            filename: Name of the output file

        Returns:
            Full path to the output file
        """
        return str(cls.OUTPUTS_DIR / filename)

    @classmethod
    def _check_ollama_available(cls) -> bool:
        """Check if Ollama is running locally."""
        try:
            # Parse URL to get host and port
            url_parts = cls.OLLAMA_BASE_URL.replace("http://", "").replace("https://", "")
            if ":" in url_parts:
                host, port = url_parts.split(":")
                port = int(port)
            else:
                host = url_parts
                port = 11434
            
            # Try to connect to Ollama
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    @classmethod
    def get_available_providers(cls) -> List[Tuple[str, str, bool]]:
        """Get list of available LLM providers with their status.
        
        Returns:
            List of tuples: (provider_name, status_message, is_available)
        """
        providers = []
        
        # Check Ollama (free, local)
        ollama_available = cls._check_ollama_available()
        providers.append((
            "ollama",
            f"Ollama ({cls.OLLAMA_MODEL}) - FREE/LOCAL",
            ollama_available
        ))
        
        # Check OpenAI
        openai_available = bool(cls.OPENAI_API_KEY) or bool(cls.OPENAI_API_BASE)
        providers.append((
            "openai",
            f"OpenAI ({cls.OPENAI_MODEL_NAME})",
            openai_available
        ))
        
        # Check Anthropic
        anthropic_available = bool(cls.ANTHROPIC_API_KEY)
        providers.append((
            "anthropic",
            f"Anthropic Claude ({cls.ANTHROPIC_MODEL})",
            anthropic_available
        ))
        
        # Check Google
        google_available = bool(cls.GOOGLE_API_KEY)
        providers.append((
            "google",
            f"Google Gemini ({cls.GOOGLE_MODEL})",
            google_available
        ))
        
        # Check Azure OpenAI
        azure_available = bool(cls.AZURE_OPENAI_API_KEY) and bool(cls.AZURE_OPENAI_ENDPOINT)
        providers.append((
            "azure",
            f"Azure OpenAI ({cls.AZURE_OPENAI_DEPLOYMENT_NAME or 'default'})",
            azure_available
        ))
        
        return providers

    @classmethod
    def detect_best_provider(cls) -> Optional[str]:
        """Automatically detect the best available provider.
        Priority: Ollama (free) > OpenAI > Anthropic > Google > Azure
        
        Returns:
            Provider name or None if none available
        """
        # If provider is explicitly set, use it
        if cls.LLM_PROVIDER:
            return cls.LLM_PROVIDER
        
        # Check providers in priority order (free first)
        if cls._check_ollama_available():
            return "ollama"
        
        if cls.OPENAI_API_KEY or cls.OPENAI_API_BASE:
            return "openai"
        
        if cls.ANTHROPIC_API_KEY:
            return "anthropic"
        
        if cls.GOOGLE_API_KEY:
            return "google"
        
        if cls.AZURE_OPENAI_API_KEY and cls.AZURE_OPENAI_ENDPOINT:
            return "azure"
        
        return None

    @classmethod
    def validate_environment(cls) -> Dict[str, bool]:
        """Validate that required environment variables are set.

        Returns:
            Dictionary mapping configuration keys to their configured status
        """
        best_provider = cls.detect_best_provider()
        
        validation = {
            "LLM_PROVIDER": best_provider is not None,
            "OLLAMA": cls._check_ollama_available(),
            "OPENAI": bool(cls.OPENAI_API_KEY) or bool(cls.OPENAI_API_BASE),
            "ANTHROPIC": bool(cls.ANTHROPIC_API_KEY),
            "GOOGLE": bool(cls.GOOGLE_API_KEY),
            "AZURE": bool(cls.AZURE_OPENAI_API_KEY) and bool(cls.AZURE_OPENAI_ENDPOINT),
            "SERPER_API_KEY": bool(cls.SERPER_API_KEY),
        }
        
        # Add provider info
        validation["_DETECTED_PROVIDER"] = best_provider
        
        return validation


# Create a singleton config instance
config = Config()

