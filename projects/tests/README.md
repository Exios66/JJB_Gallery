# Test Suite for JJB Gallery Projects

Comprehensive test suite for all projects in the JJB Gallery repository.

## 📋 Overview

This directory contains unit tests, integration tests, and end-to-end tests for all projects:

- **CrewAI** - Multi-agent swarm system
- **ChatUI** - Modern chat interface
- **iOS Chatbot** - iOS-inspired chatbot
- **LiteLLM** - LLM proxy server
- **Psychometrics** - NASA TLX assessment tool
- **RAG Model** - Retrieval-Augmented Generation
- **Terminal Agents** - Terminal-based AI agent

## 🛠️ Installation

### Install Test Dependencies

```bash
cd projects/tests
pip install -r requirements.txt
```

### Install Project Dependencies

You may also need to install dependencies for individual projects:

```bash
# Install all project dependencies
cd ../Crewai && pip install -r requirements.txt
cd ../ios_chatbot && pip install -r requirements.txt
cd ../litellm && pip install -r requirements.txt
cd ../Psychometrics && pip install -r requirements.txt
cd ../RAG_Model && pip install -r requirements.txt
cd ../terminal_agents && pip install -r requirements.txt
```

## 🚀 Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
# Test CrewAI
pytest test_crewai.py

# Test iOS Chatbot
pytest test_ios_chatbot.py

# Test LiteLLM
pytest test_litellm.py

# Test Psychometrics
pytest test_psychometrics.py

# Test RAG Model
pytest test_rag_model.py

# Test Terminal Agents
pytest test_terminal_agents.py

# Integration tests
pytest test_integration.py
```

### Run Tests with Coverage

```bash
pytest --cov=.. --cov-report=html --cov-report=term
```

### Run Tests in Parallel

```bash
pytest -n auto  # Uses all available CPUs
pytest -n 4     # Uses 4 workers
```

### Run Specific Test Categories

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Skip tests requiring API keys
pytest -m "not requires_api"
```

## 📊 Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Shared fixtures and configuration
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Test dependencies
├── README.md               # This file
├── test_crewai.py          # CrewAI tests
├── test_ios_chatbot.py     # iOS Chatbot tests
├── test_litellm.py         # LiteLLM tests
├── test_psychometrics.py   # Psychometrics tests
├── test_rag_model.py       # RAG Model tests
├── test_terminal_agents.py # Terminal Agents tests
└── test_integration.py     # Integration tests
```

## 🧪 Test Categories

### Unit Tests

Test individual components and functions in isolation:

- Configuration validation
- Data structure validation
- Function logic
- Error handling

### Integration Tests

Test interactions between components:

- API endpoints
- Database operations
- External service integration
- Workflow execution

### End-to-End Tests

Test complete user workflows:

- Full application flows
- User interactions
- System integration

## 🔧 Configuration

### Environment Variables

Some tests may require environment variables. Create a `.env.test` file:

```env
OPENAI_API_KEY=test_key
ANTHROPIC_API_KEY=test_key
GOOGLE_API_KEY=test_key
OLLAMA_BASE_URL=http://localhost:11434
```

### Pytest Configuration

Configuration is in `pytest.ini`. Key settings:

- **Test discovery**: `test_*.py` files
- **Output**: Verbose with short tracebacks
- **Markers**: For categorizing tests
- **Coverage**: Optional coverage reporting

## 📝 Writing Tests

### Test Naming

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test

```python
def test_example_function():
    """Test example function."""
    result = example_function(input_data)
    assert result == expected_output
```

### Using Fixtures

```python
def test_with_fixture(mock_openai_client):
    """Test using a fixture."""
    response = mock_openai_client.chat.completions.create(...)
    assert response is not None
```

### Marking Tests

```python
@pytest.mark.slow
def test_slow_operation():
    """This test is slow."""
    pass

@pytest.mark.requires_api
def test_api_call():
    """This test requires an API key."""
    pass
```

## 🐛 Troubleshooting

### Import Errors

If you get import errors:

1. Ensure all project dependencies are installed
2. Check that project paths are correct
3. Verify Python path includes project directories

### API Key Errors

Tests that require API keys are marked with `@pytest.mark.requires_api`. 

- Skip these tests: `pytest -m "not requires_api"`
- Or provide test API keys in environment variables

### Mock Issues

If mocks aren't working:

1. Check that you're patching the correct import path
2. Ensure mocks are set up before the code runs
3. Verify mock return values match expected types

## 📈 Coverage

Generate coverage reports:

```bash
# Terminal report
pytest --cov=.. --cov-report=term

# HTML report
pytest --cov=.. --cov-report=html
# Open htmlcov/index.html in browser
```

## 🔄 Continuous Integration

Tests can be run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    cd projects/tests
    pip install -r requirements.txt
    pytest --cov=.. --cov-report=xml
```

## 📚 Best Practices

1. **Isolate Tests**: Each test should be independent
2. **Use Fixtures**: Share common setup code
3. **Mock External Services**: Don't make real API calls in unit tests
4. **Test Edge Cases**: Include boundary conditions
5. **Clear Assertions**: Make test failures easy to understand
6. **Document Tests**: Explain what each test validates

## 🤝 Contributing

When adding new tests:

1. Follow the existing test structure
2. Use appropriate fixtures from `conftest.py`
3. Mark tests appropriately (unit, integration, slow, etc.)
4. Update this README if adding new test categories
5. Ensure tests pass before submitting PR

## 📄 License

This test suite is part of the JJB Gallery portfolio. See the main repository LICENSE file.

