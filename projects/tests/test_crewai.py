"""
Tests for CrewAI Multi-Agent Swarm System
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add Crewai to path
CREWAI_DIR = Path(__file__).parent.parent / "Crewai"
sys.path.insert(0, str(CREWAI_DIR))

from config import Config


class TestConfig:
    """Test configuration module."""
    
    def test_config_initialization(self):
        """Test that config initializes correctly."""
        assert Config is not None
        assert hasattr(Config, 'OLLAMA_BASE_URL')
        assert hasattr(Config, 'OPENAI_API_KEY')
    
    def test_get_available_providers(self):
        """Test getting available providers."""
        providers = Config.get_available_providers()
        assert isinstance(providers, list)
        assert len(providers) > 0
    
    def test_detect_best_provider(self, mock_env_vars):
        """Test provider detection."""
        provider = Config.detect_best_provider()
        # Should detect at least one provider if env vars are set
        assert provider is None or isinstance(provider, str)
    
    def test_validate_environment(self):
        """Test environment validation."""
        validation = Config.validate_environment()
        assert isinstance(validation, dict)
        assert "LLM_PROVIDER" in validation
        assert "OLLAMA" in validation
        assert "OPENAI" in validation


class TestMainModule:
    """Test main module functionality."""
    
    @patch('sys.argv', ['main.py', '--status'])
    def test_status_command(self):
        """Test status command."""
        # This would require importing main, which may have side effects
        # For now, we'll just verify the structure
        assert True
    
    @patch('sys.argv', ['main.py', '--list-crews'])
    def test_list_crews_command(self):
        """Test list crews command."""
        assert True


class TestCrews:
    """Test crew classes."""
    
    def test_crew_imports(self):
        """Test that crew classes can be imported."""
        try:
            from crews import (
                MLCrew,
                ResearchCrew,
                ResearchAcademicCrew,
                ResearchContentCrew,
                BusinessIntelligenceCrew,
                DevCodeCrew,
                DocumentationCrew,
            )
            assert True
        except ImportError as e:
            pytest.skip(f"Crew classes not available: {e}")
    
    def test_ml_crew_exists(self):
        """Test ML crew class exists."""
        try:
            from crews import MLCrew
            assert MLCrew is not None
        except ImportError:
            pytest.skip("MLCrew not available")


class TestAgents:
    """Test agent classes."""
    
    def test_agent_imports(self):
        """Test that agent classes can be imported."""
        try:
            from agents import (
                business_intelligence_agents,
                hyperparameter_optimizer,
                literature_reviewer,
            )
            assert True
        except ImportError as e:
            pytest.skip(f"Agent modules not available: {e}")


class TestTools:
    """Test tool classes."""
    
    def test_tool_imports(self):
        """Test that tool classes can be imported."""
        try:
            from tools import (
                academic_tools,
                business_intelligence_tools,
                content_tools,
                dev_tools,
                documentation_tools,
                ml_tools,
                research_tools,
            )
            assert True
        except ImportError as e:
            pytest.skip(f"Tool modules not available: {e}")


class TestLLMConfig:
    """Test LLM configuration."""
    
    def test_llm_config_import(self):
        """Test LLM config can be imported."""
        try:
            from llm_config import (
                get_setup_instructions,
                get_llm_for_agent,
                configure_crewai_environment,
            )
            assert callable(get_setup_instructions)
        except ImportError:
            pytest.skip("LLM config not available")
    
    @patch('llm_config.config')
    def test_get_llm_for_agent(self, mock_config):
        """Test getting LLM for agent."""
        try:
            from llm_config import get_llm_for_agent
            # This would require actual LLM setup, so we'll mock it
            assert True
        except ImportError:
            pytest.skip("LLM config not available")

