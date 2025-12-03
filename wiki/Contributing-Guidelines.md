# Contributing Guidelines

Thank you for your interest in contributing to the JJB Gallery repository!

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Error messages or screenshots

### Suggesting Features

1. **Check existing issues** for similar suggestions
2. **Create a feature request** with:
   - Clear description
   - Use case and motivation
   - Proposed implementation (if applicable)
   - Examples or mockups

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes**
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Ensure tests pass**: `pytest` or `npm test`
7. **Commit with clear messages**
8. **Push to your fork**: `git push origin feature/your-feature`
9. **Create a Pull Request**

## Code Standards

### Python

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable names

**Example**:

```python
def process_document(file_path: str) -> Dict[str, Any]:
    """
    Process a document and extract metadata.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        Dictionary containing document metadata
    """
    # Implementation
    pass
```

### JavaScript/TypeScript

- Follow ESLint rules
- Use TypeScript for type safety
- Write JSDoc comments
- Use async/await for async operations

**Example**:

```typescript
/**
 * Process a chat message and return response.
 * @param message - The user's message
 * @returns Promise resolving to assistant response
 */
async function processMessage(message: string): Promise<string> {
  // Implementation
}
```

## Testing

### Writing Tests

- Write tests for new features
- Aim for good coverage
- Test edge cases
- Use descriptive test names

**Python Example**:

```python
def test_rag_retrieval():
    """Test RAG document retrieval."""
    rag = RAGSystem()
    rag.load_vector_store()
    results = rag.retrieve("test query", k=5)
    assert len(results) <= 5
    assert all('content' in r for r in results)
```

### Running Tests

```bash
# Python
pytest

# Node.js
npm test
```

## Documentation

### Code Documentation

- Write clear docstrings
- Explain complex logic
- Include examples where helpful
- Update READMEs for user-facing changes

### README Updates

When adding features:

- Update project README
- Add usage examples
- Update installation if needed
- Document new configuration options

## Pull Request Process

### Before Submitting

1. **Ensure tests pass**
2. **Check code style** (Black, Prettier)
3. **Update documentation**
4. **Rebase on latest main** (if needed)

### PR Description

Include:

- **What**: What changes were made
- **Why**: Motivation for changes
- **How**: How to test the changes
- **Screenshots**: If UI changes

### Review Process

- Maintainers will review your PR
- Address feedback promptly
- Be open to suggestions
- Keep discussions constructive

## Project-Specific Guidelines

### RAG Model

- Maintain backward compatibility
- Add tests for new embedding models
- Document performance implications

### Psychometrics

- Follow scientific methodology
- Maintain assessment validity
- Document statistical methods

### Chat Interfaces

- Ensure responsive design
- Test on multiple browsers
- Consider accessibility

### LLM Integration

- Support multiple providers
- Handle errors gracefully
- Document rate limits

## Questions?

- **GitHub Issues**: For bugs and features
- **Discussions**: For questions and ideas
- **Email**: <jackburleson.dev@gmail.com>

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect different viewpoints

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be:

- Listed in CONTRIBUTORS.md
- Credited in release notes
- Appreciated in the community!

Thank you for contributing! 🎉

## Related Documentation

- [Development Setup](Development-Setup)
- [Testing Guide](Testing-Guide)
- [Architecture Overview](Architecture-Overview)
