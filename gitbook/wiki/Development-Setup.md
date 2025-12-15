# Development Setup

Guide for setting up a development environment for contributing to JJB Gallery projects.

## Prerequisites

### Required Tools

- **Git**: Version control
- **Python 3.8+**: For Python projects
- **Node.js 18+**: For ChatUi
- **Code Editor**: VS Code, PyCharm, or similar

### Recommended Tools

- **Docker**: For containerized services
- **Postman/Insomnia**: API testing
- **GitHub CLI**: For GitHub operations

## Development Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/Exios66/JJB_Gallery.git
cd JJB_Gallery
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Node.js Environment (for ChatUi)

```bash
cd projects/ChatUi
npm install
```

### 4. Install Development Dependencies

```bash
# Python development tools
pip install black isort pytest pytest-cov mypy

# Pre-commit hooks
pip install pre-commit
pre-commit install
```

## Project Structure

### Python Projects

```
project_name/
├── src/              # Source code
├── tests/            # Test files
├── docs/             # Documentation
├── requirements.txt  # Dependencies
├── setup.py          # Package setup
└── README.md         # Documentation
```

### Node.js Projects

```
project_name/
├── src/              # Source code
├── tests/            # Test files
├── public/           # Static assets
├── package.json      # Dependencies
└── README.md         # Documentation
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code
- Add tests
- Update documentation

### 3. Test Changes

```bash
# Run tests
pytest

# Check code style
black --check .
isort --check .

# Type checking
mypy .
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add new feature"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
# Create PR on GitHub
```

## Code Style

### Python

- **Formatter**: Black
- **Import Sorting**: isort
- **Type Hints**: mypy
- **Linting**: flake8 or pylint

**Configuration**:

```bash
# .black
line-length = 88
target-version = ['py38']

# .isort.cfg
[settings]
profile = black
```

### JavaScript/TypeScript

- **Formatter**: Prettier
- **Linting**: ESLint
- **Type Checking**: TypeScript

**Configuration**:

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2
}
```

## Testing

### Python Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_specific.py
```

### Node.js Tests

```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## Documentation

### Docstrings

**Python**:

```python
def function(param: str) -> str:
    """
    Function description.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
    """
    pass
```

### README Updates

- Update project READMEs when adding features
- Include usage examples
- Update installation instructions if needed

## Pre-commit Hooks

### Setup

```bash
pre-commit install
```

### Hooks

- **Black**: Format Python code
- **isort**: Sort imports
- **flake8**: Lint Python code
- **Prettier**: Format JavaScript/TypeScript

## Debugging

### Python

```python
# Use debugger
import pdb; pdb.set_trace()

# Or use IDE debugger
# VS Code: F5
# PyCharm: Shift+F9
```

### Node.js

```javascript
// Use debugger
debugger;

// Or use Node inspector
node --inspect app.js
```

## IDE Setup

### VS Code

**Extensions**:

- Python
- Pylance
- Black Formatter
- ESLint
- Prettier

**Settings** (`.vscode/settings.json`):

```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "editor.formatOnSave": true
}
```

### PyCharm

- Configure Python interpreter (virtual environment)
- Enable Black formatter
- Set up code inspections

## Git Workflow

### Branch Naming

- `feature/`: New features
- `fix/`: Bug fixes
- `docs/`: Documentation
- `refactor/`: Code refactoring
- `test/`: Test additions

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: fix bug
docs: update documentation
refactor: refactor code
test: add tests
chore: maintenance tasks
```

## CI/CD

### GitHub Actions

Projects may include GitHub Actions workflows:

- **Tests**: Run on PR
- **Linting**: Check code style
- **Build**: Build artifacts
- **Deploy**: Deploy on merge

## Related Documentation

- [Contributing Guidelines](Contributing-Guidelines.md)
- [Testing Guide](Testing-Guide.md)
- [Installation Guide](Installation-Guide.md)

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
