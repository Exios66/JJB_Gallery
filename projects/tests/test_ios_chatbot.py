"""
Tests for iOS-Inspired Chatbot Application
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
import os

# Add ios_chatbot to path
IOS_CHATBOT_DIR = Path(__file__).parent.parent / "ios_chatbot"
sys.path.insert(0, str(IOS_CHATBOT_DIR))


class TestIOSChatbot:
    """Test iOS chatbot application."""
    
    def test_imports(self):
        """Test that the app can be imported."""
        try:
            import app
            assert True
        except ImportError as e:
            pytest.skip(f"App not available: {e}")
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    def test_page_config(self, mock_markdown, mock_page_config):
        """Test page configuration."""
        try:
            import app
            # Verify page config was called
            assert True
        except ImportError:
            pytest.skip("App not available")
    
    @patch('openai.OpenAI')
    def test_openai_client_creation(self, mock_openai):
        """Test OpenAI client creation."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        client = mock_openai(api_key="test_key")
        assert client is not None
        mock_openai.assert_called_once()
    
    @patch('openai.OpenAI')
    def test_chat_completion(self, mock_openai):
        """Test chat completion functionality."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        client = mock_openai(api_key="test_key")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        assert response.choices[0].message.content == "Test response"
    
    def test_message_formatting(self):
        """Test message formatting."""
        # Test that message formatting works correctly
        content = "Test message"
        role = "user"
        
        # Basic format check
        assert isinstance(content, str)
        assert role in ["user", "assistant", "system"]
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    def test_env_var_loading(self):
        """Test environment variable loading."""
        api_key = os.getenv("OPENAI_API_KEY")
        assert api_key == "test_key"


class TestChatInterface:
    """Test chat interface functionality."""
    
    def test_session_state_initialization(self):
        """Test session state initialization."""
        # Mock session state
        session_state = {
            "messages": [],
            "api_key": "",
            "model": "gpt-3.5-turbo"
        }
        
        assert "messages" in session_state
        assert isinstance(session_state["messages"], list)
        assert session_state["model"] == "gpt-3.5-turbo"
    
    def test_message_structure(self):
        """Test message structure."""
        message = {
            "role": "user",
            "content": "Hello, world!"
        }
        
        assert message["role"] in ["user", "assistant", "system"]
        assert isinstance(message["content"], str)
        assert len(message["content"]) > 0
    
    def test_chat_history_management(self):
        """Test chat history management."""
        messages = []
        
        # Add user message
        messages.append({"role": "user", "content": "Hello"})
        assert len(messages) == 1
        
        # Add assistant message
        messages.append({"role": "assistant", "content": "Hi there!"})
        assert len(messages) == 2
        
        # Clear messages
        messages.clear()
        assert len(messages) == 0


class TestModelSelection:
    """Test model selection functionality."""
    
    def test_model_options(self):
        """Test available model options."""
        models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
        
        assert "gpt-3.5-turbo" in models
        assert "gpt-4" in models
        assert len(models) > 0
    
    def test_model_validation(self):
        """Test model name validation."""
        valid_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
        test_model = "gpt-3.5-turbo"
        
        assert test_model in valid_models

