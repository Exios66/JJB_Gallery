"""
Configuration module for CrewAI ML Agent Swarm.
Handles environment variables, API keys, and system configuration.
"""

import os
from pathlib import Path
from typing import Dict


class Config:
    """Configuration class for CrewAI system."""

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "")
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4")
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")

    # System Configuration
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
    def validate_environment(cls) -> Dict[str, bool]:
        """Validate that required environment variables are set.

        Returns:
            Dictionary mapping configuration keys to their configured status
        """
        return {
            "OPENAI_API_KEY": bool(cls.OPENAI_API_KEY),
            "OPENAI_API_BASE": bool(cls.OPENAI_API_BASE) or bool(cls.OPENAI_API_KEY),
            "OPENAI_MODEL_NAME": bool(cls.OPENAI_MODEL_NAME),
            "SERPER_API_KEY": bool(cls.SERPER_API_KEY),
        }


# Create a singleton config instance
config = Config()

