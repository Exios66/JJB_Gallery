# Testing Guide

Comprehensive guide to testing all projects in the JJB Gallery repository.

## Overview

This guide covers testing strategies, test execution, and best practices for all projects.

## Testing Philosophy

- **Unit Tests**: Test individual components
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Manual Testing**: User acceptance testing

## RAG Model

### Unit Tests

```python
# tests/test_rag_system.py
import pytest
from rag_system import RAGSystem

def test_rag_initialization():
    """Test RAG system initialization."""
    rag = RAGSystem()
    assert rag.embedding_model_name is not None
    assert rag.vector_store_path is not None

def test_document_loading():
    """Test document loading."""
    rag = RAGSystem()
    docs = rag.load_documents(["test.txt"])
    assert len(docs) > 0

def test_retrieval():
    """Test document retrieval."""
    rag = RAGSystem()
    rag.load_vector_store()
    results = rag.retrieve("test query", k=5)
    assert len(results) <= 5
```

### Integration Tests

```python
def test_full_rag_pipeline():
    """Test complete RAG pipeline."""
    rag = RAGSystem()
    documents = ["Document 1", "Document 2"]
    rag.create_vector_store(documents)
    result = rag.query("test query")
    assert 'answer' in result
    assert 'retrieved_documents' in result
```

### Running Tests

```bash
cd projects/RAG_Model
pytest tests/
pytest --cov=rag_system tests/
```

## Psychometrics

### Unit Tests

```python
# tests/test_nasa_tlx.py
import pytest
from nasa_tlx import NASATLX, TLXRating

def test_tlx_rating_validation():
    """Test TLX rating validation."""
    rating = TLXRating(
        mental_demand=15,
        physical_demand=3,
        temporal_demand=12,
        performance=5,
        effort=14,
        frustration=8
    )
    assert rating.validate()

def test_raw_tlx_calculation():
    """Test raw TLX score calculation."""
    tlx = NASATLX()
    result = tlx.create_assessment("Test Task")
    tlx.add_rating(result, 15, 3, 12, 5, 14, 8)
    tlx.calculate_scores(result)
    assert result.raw_tlx_score is not None
    assert 1 <= result.raw_tlx_score <= 20
```

### Running Tests

```bash
cd projects/Psychometrics
pytest tests/
```

## ChatUi

### Unit Tests

```javascript
// tests/ChatInterface.test.js
import { render } from '@testing-library/svelte';
import ChatInterface from '../src/components/ChatInterface.svelte';

test('renders chat interface', () => {
  const { container } = render(ChatInterface);
  expect(container).toBeTruthy();
});

test('handles message input', () => {
  // Test message input handling
});
```

### Integration Tests

```javascript
test('sends message and receives response', async () => {
  // Test API integration
});
```

### Running Tests

```bash
cd projects/ChatUi
npm test
npm run test:coverage
```

## iOS Chatbot

### Unit Tests

```python
# tests/test_app.py
import pytest
from app import app, chatbot

def test_health_endpoint():
    """Test health check endpoint."""
    client = app.test_client()
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_chat_endpoint():
    """Test chat endpoint."""
    client = app.test_client()
    response = client.post('/api/chat', json={
        'message': 'Hello'
    })
    assert response.status_code == 200
    assert 'response' in response.json
```

### Running Tests

```bash
cd projects/ios_chatbot
pytest tests/
```

## LiteLLM

### Unit Tests

```python
# tests/test_proxy.py
import pytest
from proxy_server import app

def test_health_endpoint():
    """Test health check."""
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200

def test_chat_completions():
    """Test chat completions endpoint."""
    client = app.test_client()
    response = client.post('/v1/chat/completions', json={
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Hello'}]
    })
    assert response.status_code in [200, 503]  # 503 if LiteLLM not available
```

### Running Tests

```bash
cd projects/litellm
pytest tests/
```

## CrewAI

### Unit Tests

```python
# tests/test_crews.py
import pytest
from crews import MLCrew

def test_ml_crew_initialization():
    """Test ML crew initialization."""
    crew = MLCrew()
    assert crew.agents is not None
    assert len(crew.agents) > 0
```

### Running Tests

```bash
cd projects/Crewai
python run_tests.py
```

## Test Coverage

### Python Projects

```bash
# Install coverage
pip install pytest-cov

# Run with coverage
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

### Node.js Projects

```bash
# Run with coverage
npm run test:coverage

# View report
open coverage/index.html
```

## Continuous Integration

### GitHub Actions

Example workflow (`.github/workflows/test.yml`):

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
```

## Manual Testing

### Test Checklist

For each project:

- [ ] Installation works
- [ ] Basic functionality works
- [ ] Error handling works
- [ ] Documentation is accurate
- [ ] Examples run successfully

### User Acceptance Testing

- Test with real use cases
- Verify user experience
- Check performance
- Validate outputs

## Best Practices

### 1. Write Tests First (TDD)

- Write tests before implementation
- Ensure tests fail initially
- Implement to make tests pass
- Refactor while keeping tests green

### 2. Test Edge Cases

- Empty inputs
- Invalid inputs
- Boundary conditions
- Error conditions

### 3. Keep Tests Independent

- Each test should be independent
- Don't rely on test execution order
- Clean up after tests

### 4. Use Descriptive Names

```python
# Good
def test_rag_retrieves_top_5_documents():
    pass

# Bad
def test_rag():
    pass
```

### 5. Mock External Dependencies

```python
from unittest.mock import patch

@patch('openai.ChatCompletion.create')
def test_with_mock(mock_openai):
    mock_openai.return_value = {'choices': [{'message': {'content': 'test'}}]}
    # Test code
```

## Related Documentation

- [Development Setup](Development-Setup.md)
- [Contributing Guidelines](Contributing-Guidelines.md)
- [Architecture Overview](Architecture-Overview.md)

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>

