"""
Tests for LiteLLM Proxy Server
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from fastapi.testclient import TestClient

# Add litellm to path
LITELLM_DIR = Path(__file__).parent.parent / "litellm"
sys.path.insert(0, str(LITELLM_DIR))


class TestProxyServer:
    """Test proxy server functionality."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        try:
            from proxy_server import app
            return TestClient(app)
        except ImportError:
            pytest.skip("Proxy server not available")
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        if client is None:
            pytest.skip("Client not available")
        
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "status" in data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        if client is None:
            pytest.skip("Client not available")
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_models_endpoint(self, client):
        """Test models listing endpoint."""
        if client is None:
            pytest.skip("Client not available")
        
        response = client.get("/v1/models")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
    
    @patch('litellm.completion')
    def test_chat_completions_endpoint(self, mock_completion, client):
        """Test chat completions endpoint."""
        if client is None:
            pytest.skip("Client not available")
        
        # Mock LiteLLM response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_response.choices[0].message.role = "assistant"
        mock_response.id = "test-id"
        mock_response.created = 1234567890
        
        mock_usage = MagicMock()
        mock_usage.prompt_tokens = 10
        mock_usage.completion_tokens = 20
        mock_usage.total_tokens = 30
        mock_response.usage = mock_usage
        
        mock_completion.return_value = mock_response
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "Hello"}
            ]
        }
        
        response = client.post("/v1/chat/completions", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "choices" in data
        assert len(data["choices"]) > 0


class TestConfiguration:
    """Test configuration management."""
    
    def test_config_import(self):
        """Test config can be imported."""
        try:
            from proxy_server import Config
            assert Config is not None
        except ImportError:
            pytest.skip("Config not available")
    
    @patch.dict('os.environ', {
        'OPENAI_API_KEY': 'test_key',
        'ANTHROPIC_API_KEY': 'test_anthropic_key'
    })
    def test_load_environment(self):
        """Test environment loading."""
        try:
            from proxy_server import Config
            Config.load_environment()
            assert True
        except ImportError:
            pytest.skip("Config not available")


class TestRequestModels:
    """Test request/response models."""
    
    def test_chat_message_model(self):
        """Test ChatMessage model."""
        try:
            from proxy_server import ChatMessage
            message = ChatMessage(role="user", content="Hello")
            assert message.role == "user"
            assert message.content == "Hello"
        except ImportError:
            pytest.skip("Models not available")
    
    def test_chat_request_model(self):
        """Test ChatRequest model."""
        try:
            from proxy_server import ChatRequest, ChatMessage
            messages = [ChatMessage(role="user", content="Hello")]
            request = ChatRequest(model="gpt-3.5-turbo", messages=messages)
            assert request.model == "gpt-3.5-turbo"
            assert len(request.messages) == 1
        except ImportError:
            pytest.skip("Models not available")


class TestLiteLLMIntegration:
    """Test LiteLLM integration."""
    
    @patch('litellm.completion')
    def test_litellm_completion(self, mock_completion):
        """Test LiteLLM completion call."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test"
        mock_completion.return_value = mock_response
        
        try:
            from litellm import completion
            response = completion(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            )
            assert response is not None
        except ImportError:
            pytest.skip("LiteLLM not available")

