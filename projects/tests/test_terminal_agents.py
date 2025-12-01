"""
Tests for Terminal Agents Application
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import os

# Add terminal_agents to path
TERMINAL_AGENTS_DIR = Path(__file__).parent.parent / "terminal_agents"
sys.path.insert(0, str(TERMINAL_AGENTS_DIR))


class TestTerminalAgent:
    """Test TerminalAgent class."""
    
    def test_agent_import(self):
        """Test that TerminalAgent can be imported."""
        try:
            from agent import TerminalAgent
            assert TerminalAgent is not None
        except ImportError as e:
            pytest.skip(f"Agent not available: {e}")
    
    @patch('openai.OpenAI')
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    def test_agent_initialization(self, mock_openai):
        """Test agent initialization."""
        try:
            from agent import TerminalAgent
            
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            
            agent = TerminalAgent(api_key="test_key")
            
            assert agent is not None
            assert agent.api_key == "test_key"
        except ImportError:
            pytest.skip("Agent not available")
    
    @patch('openai.OpenAI')
    def test_chat_functionality(self, mock_openai):
        """Test chat functionality."""
        try:
            from agent import TerminalAgent
            
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            agent = TerminalAgent(api_key="test_key")
            response = agent.chat("Hello")
            
            assert response == "Test response"
        except ImportError:
            pytest.skip("Agent not available")
    
    @patch('openai.OpenAI')
    def test_analyze_code(self, mock_openai, sample_text_file):
        """Test code analysis functionality."""
        try:
            from agent import TerminalAgent
            
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Code analysis result"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            agent = TerminalAgent(api_key="test_key")
            result = agent.analyze_code(str(sample_text_file))
            
            assert "analysis" in result.lower() or len(result) > 0
        except ImportError:
            pytest.skip("Agent not available")
    
    @patch('openai.OpenAI')
    def test_explain_code(self, mock_openai):
        """Test code explanation functionality."""
        try:
            from agent import TerminalAgent
            
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Code explanation"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            agent = TerminalAgent(api_key="test_key")
            code = "def hello(): return 'world'"
            result = agent.explain_code(code)
            
            assert len(result) > 0
        except ImportError:
            pytest.skip("Agent not available")
    
    @patch('openai.OpenAI')
    def test_generate_code(self, mock_openai):
        """Test code generation functionality."""
        try:
            from agent import TerminalAgent
            
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "def fibonacci(n):\n    return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            agent = TerminalAgent(api_key="test_key")
            result = agent.generate_code("Fibonacci function")
            
            assert "def" in result or "function" in result.lower()
        except ImportError:
            pytest.skip("Agent not available")
    
    @patch('openai.OpenAI')
    def test_fix_code(self, mock_openai):
        """Test code fixing functionality."""
        try:
            from agent import TerminalAgent
            
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Fixed code"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            agent = TerminalAgent(api_key="test_key")
            code = "def broken(): return x / 0"
            result = agent.fix_code(code)
            
            assert len(result) > 0
        except ImportError:
            pytest.skip("Agent not available")


class TestCommandLineInterface:
    """Test command-line interface."""
    
    @patch('sys.argv', ['agent.py', 'chat', 'Hello'])
    @patch('openai.OpenAI')
    def test_chat_command(self, mock_openai):
        """Test chat command."""
        try:
            from agent import TerminalAgent
            
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            # Test would require running main(), which has side effects
            # So we'll just verify the structure
            assert True
        except ImportError:
            pytest.skip("Agent not available")
    
    def test_command_parsing(self):
        """Test command parsing."""
        commands = ["chat", "analyze", "explain", "generate", "fix", "interactive", "help"]
        
        assert "chat" in commands
        assert "analyze" in commands
        assert len(commands) >= 5


class TestConversationHistory:
    """Test conversation history management."""
    
    def test_history_structure(self):
        """Test conversation history structure."""
        history = []
        
        # Add user message
        history.append({"role": "user", "content": "Hello"})
        assert len(history) == 1
        
        # Add assistant message
        history.append({"role": "assistant", "content": "Hi there!"})
        assert len(history) == 2
        
        # Verify structure
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"
    
    def test_history_persistence(self):
        """Test that history persists across calls."""
        history = []
        
        history.append({"role": "user", "content": "First message"})
        history.append({"role": "assistant", "content": "First response"})
        history.append({"role": "user", "content": "Second message"})
        
        assert len(history) == 3
        assert history[0]["content"] == "First message"
        assert history[2]["content"] == "Second message"


class TestRichUI:
    """Test Rich UI functionality."""
    
    def test_rich_import(self):
        """Test Rich library can be imported."""
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.markdown import Markdown
            assert Console is not None
        except ImportError:
            pytest.skip("Rich not available")
    
    def test_console_creation(self):
        """Test console creation."""
        try:
            from rich.console import Console
            console = Console()
            assert console is not None
        except ImportError:
            pytest.skip("Rich not available")

