"""
Configuration module for Terminal Agents.
Handles environment variables, API keys, and system configuration.
Supports multiple LLM providers with priority on free/open-source options.
"""

import os
import socket
from pathlib import Path
from typing import Optional, Dict, Any
import yaml


class TerminalAgentConfig:
    """Configuration class for Terminal Agents with multi-provider LLM support."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to YAML config file (optional)
        """
        # Load config file if provided
        config_data = {}
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        # Helper to get value from config file or environment
        def get_config(key: str, env_key: str, default: Any = "") -> str:
            return str(config_data.get(key, os.getenv(env_key, default)))
        
        # ==================== Provider Selection ====================
        # Priority order: free/open-source first, then paid
        # Set LLM_PROVIDER to override auto-detection: "ollama", "openai", "anthropic", "google", "azure"
        self.provider: str = get_config("provider", "LLM_PROVIDER", "").lower()
        
        # ==================== Ollama (Free/Local) ====================
        self.ollama_base_url: str = get_config("ollama_base_url", "OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model: str = get_config("ollama_model", "OLLAMA_MODEL", "llama3.1:8b")
        
        # ==================== OpenAI (Paid) ====================
        self.openai_api_key: str = get_config("openai_api_key", "OPENAI_API_KEY", "")
        self.openai_api_base: str = get_config("openai_api_base", "OPENAI_API_BASE", "")
        self.openai_model: str = get_config("openai_model", "OPENAI_MODEL_NAME", "gpt-4o-mini")
        
        # ==================== Anthropic Claude (Paid) ====================
        self.anthropic_api_key: str = get_config("anthropic_api_key", "ANTHROPIC_API_KEY", "")
        self.anthropic_model: str = get_config("anthropic_model", "ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        
        # ==================== Google Gemini (Paid/Free tier) ====================
        self.google_api_key: str = get_config("google_api_key", "GOOGLE_API_KEY", "")
        self.google_model: str = get_config("google_model", "GOOGLE_MODEL", "gemini-pro")
        
        # ==================== Azure OpenAI (Paid) ====================
        self.azure_openai_api_key: str = get_config("azure_openai_api_key", "AZURE_OPENAI_API_KEY", "")
        self.azure_openai_endpoint: str = get_config("azure_openai_endpoint", "AZURE_OPENAI_ENDPOINT", "")
        self.azure_openai_deployment: str = get_config("azure_openai_deployment", "AZURE_OPENAI_DEPLOYMENT_NAME", "")
        self.azure_openai_api_version: str = get_config("azure_openai_api_version", "AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        # ==================== General Settings ====================
        self.api_key: Optional[str] = get_config("api_key", "TERMINAL_AGENTS_API_KEY", "")
        self.model: Optional[str] = get_config("model", "TERMINAL_AGENTS_MODEL", "")
        
        # Output settings
        self.verbose: bool = os.getenv("VERBOSE", "true").lower() == "true"
        
        # Config directory
        self.config_dir = Path.home() / ".terminal_agents"
        self.config_dir.mkdir(exist_ok=True)
        
        # History file
        self.history_file = self.config_dir / "history.json"

    def detect_best_provider(self) -> Optional[str]:
        """Auto-detect the best available LLM provider.
        
        Returns:
            Provider name or None
        """
        # If provider is explicitly set, use it
        if self.provider:
            return self.provider
        
        # Priority order: free first, then paid
        # 1. Check Ollama (free, local)
        if self._check_ollama_available():
            return "ollama"
        
        # 2. Check OpenAI
        if self.openai_api_key:
            return "openai"
        
        # 3. Check Anthropic
        if self.anthropic_api_key:
            return "anthropic"
        
        # 4. Check Google
        if self.google_api_key:
            return "google"
        
        # 5. Check Azure
        if self.azure_openai_api_key and self.azure_openai_endpoint:
            return "azure"
        
        return None

    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running locally."""
        try:
            url_parts = self.ollama_base_url.replace("http://", "").replace("https://", "")
            if ":" in url_parts:
                host, port = url_parts.split(":")
                port = int(port)
            else:
                host = url_parts
                port = 11434
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get configuration for a specific provider.
        
        Args:
            provider: Provider name
            
        Returns:
            Configuration dictionary
        """
        configs = {
            "ollama": {
                "base_url": self.ollama_base_url,
                "model": self.ollama_model,
            },
            "openai": {
                "api_key": self.openai_api_key or self.api_key,
                "api_base": self.openai_api_base,
                "model": self.openai_model or self.model,
            },
            "anthropic": {
                "api_key": self.anthropic_api_key or self.api_key,
                "model": self.anthropic_model or self.model,
            },
            "google": {
                "api_key": self.google_api_key or self.api_key,
                "model": self.google_model or self.model,
            },
            "azure": {
                "api_key": self.azure_openai_api_key or self.api_key,
                "endpoint": self.azure_openai_endpoint,
                "deployment": self.azure_openai_deployment,
                "api_version": self.azure_openai_api_version,
            },
        }
        return configs.get(provider, {})

