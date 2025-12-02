# NPM Setup & Integration Guide

This document outlines all NPM packages, configurations, and integrations for the JJB Gallery repository.

## 📦 Package Structure

### Root Package (`package.json`)
- **Purpose**: Main repository configuration with workspace support
- **Workspaces**: `projects/ChatUi`
- **Key Features**:
  - Commit linting with conventional commits
  - Code formatting with Prettier
  - Husky git hooks
  - GitHub API integration
  - External API clients

### ChatUi Package (`projects/ChatUi/package.json`)
- **Purpose**: SvelteKit chat interface application
- **Key Dependencies**:
  - SvelteKit framework
  - MongoDB for chat history
  - Hugging Face Transformers.js
  - OpenAI SDK
  - TypeScript support

## 🚀 Quick Start

### 0. Setup External Storage (Recommended)

**IMPORTANT**: Before installing dependencies, configure external USB drive storage to avoid disk space issues:

```bash
# Run the setup script
npm run setup:external
# or
./scripts/setup-external-storage.sh

# Reload your shell
source ~/.zshrc  # or ~/.bashrc
```

See [EXTERNAL_STORAGE_SETUP.md](EXTERNAL_STORAGE_SETUP.md) for complete details.

### 1. Install Dependencies

```bash
# Install root dependencies
npm install

# Install all workspace dependencies
npm install --workspaces
```

### 2. Setup Git Hooks

```bash
# Husky will auto-install on npm install
# Or manually:
npx husky install
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# GitHub
GITHUB_TOKEN=your_github_token

# Hugging Face
HF_TOKEN=your_huggingface_token

# OpenAI
OPENAI_API_KEY=your_openai_key

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_key

# Serper (Web Search)
SERPER_API_KEY=your_serper_key

# MongoDB (for ChatUi)
MONGODB_URL=mongodb://localhost:27017
```

## 📋 Available Scripts

### Root Level

```bash
npm run prepare          # Setup Husky git hooks
npm run lint:commits     # Lint commit messages
npm run format           # Format all code with Prettier
npm run format:check     # Check code formatting
npm run build            # Build ChatUi workspace
npm run dev              # Start ChatUi dev server
npm run clean            # Clean all build artifacts
npm run clean:disk       # Clean disk space (npm cache, node_modules, etc.)
npm run test:apis        # Test all API connections
npm run examples         # Run API client examples
```

### ChatUi Workspace

```bash
npm run dev --workspace=projects/ChatUi    # Start dev server
npm run build --workspace=projects/ChatUi  # Build for production
npm run preview --workspace=projects/ChatUi # Preview production build
npm run test --workspace=projects/ChatUi   # Run tests
```

## 🔧 Configuration Files

### `.commitlintrc.json`
- Enforces conventional commit format
- Scopes: `crewai`, `chatui`, `litellm`, `quarto`, `jupyter`, etc.
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

### `.prettierrc.json`
- Code formatting rules
- 100 character line width
- 2 space indentation
- LF line endings

### `.npmrc`
- Auto-install peer dependencies
- Package lock enabled
- Moderate audit level

### `.nvmrc` / `.node-version`
- Node.js version: 20
- Ensures consistent Node version across environments

## 🔌 External API Integrations

All API clients are available in `scripts/npm/integrations.js`. See `scripts/npm/README.md` for detailed usage.

### GitHub API
- **Client**: `GitHubClient` (custom axios client)
- **Usage**: Repository management, releases, issues, statistics
- **Environment**: `GITHUB_TOKEN`
- **Example**: See `scripts/npm/examples.js`

### Hugging Face API
- **Client**: `HuggingFaceClient` (custom axios client)
- **Usage**: Model inference, embeddings, model information
- **Environment**: `HF_TOKEN`
- **Example**: See `scripts/npm/examples.js`

### OpenAI API
- **Client**: `OpenAIClient` (custom axios client)
- **Usage**: Chat completions, embeddings
- **Environment**: `OPENAI_API_KEY`
- **Example**: See `scripts/npm/examples.js`

### Anthropic API
- **Client**: `AnthropicClient` (custom axios client)
- **Usage**: Claude model completions, streaming
- **Environment**: `ANTHROPIC_API_KEY`
- **Example**: See `scripts/npm/examples.js`

### Serper API
- **Client**: `SerperClient` (custom axios client)
- **Usage**: Web search functionality, search suggestions
- **Environment**: `SERPER_API_KEY`
- **Example**: See `scripts/npm/examples.js`

### MongoDB
- **Client**: `MongoDBHelper` (connection validator)
- **Usage**: Chat history storage (ChatUi), connection validation
- **Environment**: `MONGODB_URL`
- **Note**: Actual MongoDB operations handled by `mongodb` driver in ChatUi

### Testing All Connections
```bash
# Test all API connections at once
npm run test:apis

# Or use the function directly
import { testAllConnections } from './scripts/npm/integrations.js';
const status = await testAllConnections();
```

## 📁 Project Integrations

### CrewAI Project
- **Type**: Python-based
- **NPM Integration**: None (Python dependencies in `requirements.txt`)
- **External APIs**: OpenAI, Anthropic, Google, Azure (via Python)

### ChatUi Project
- **Type**: SvelteKit (Node.js)
- **NPM Integration**: Full workspace package
- **External APIs**: Hugging Face, OpenAI, Anthropic, MongoDB

### LiteLLM Project
- **Type**: Python-based
- **NPM Integration**: None (Python dependencies)
- **External APIs**: Multiple LLM providers (via Python)

### Quarto Documents
- **Type**: Markdown/Quarto
- **NPM Integration**: None (rendered via Quarto CLI)
- **External APIs**: None

## 🛠️ Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes**

3. **Format code**
   ```bash
   npm run format
   ```

4. **Commit with conventional format**
   ```bash
   git commit -m "feat(scope): your commit message"
   ```
   - Husky will automatically lint your commit message
   - Lint-staged will format staged files

5. **Push and create PR**

### Commit Message Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Examples:**
- `feat(chatui): add dark mode toggle`
- `fix(crewai): resolve API timeout issue`
- `docs(root): update installation guide`
- `chore(deps): update npm packages`

## 🔒 Security

### Audit Dependencies
```bash
npm audit
npm audit fix
```

### Update Dependencies
```bash
npm outdated
npm update
```

## 📊 CI/CD Integration

### GitHub Actions
- **Workflow**: `.github/workflows/npm-deps.yml`
- **Triggers**: Changes to `package.json` files
- **Actions**:
  - Install dependencies
  - Security audit
  - Check for outdated packages
  - Verify package-lock.json

## 🐛 Troubleshooting

### Disk Space Issues (ENOSPC Error)

If you encounter `ENOSPC: no space left on device`:

1. **Run the cleanup script:**
   ```bash
   npm run clean:disk
   # or
   ./scripts/npm/cleanup-disk-space.sh
   ```

2. **Clean npm cache manually:**
   ```bash
   npm cache clean --force
   rm -rf ~/.npm/_cacache/tmp
   ```

3. **Free up system space:**
   ```bash
   # Check disk usage
   df -h
   
   # Clean system caches (macOS)
   sudo rm -rf /private/var/folders/*/T/pip-*
   sudo rm -rf /private/var/folders/*/T/npm-*
   ```

4. **After cleanup, reinstall:**
   ```bash
   npm install
   ```

### Node Version Issues
```bash
# Use nvm to switch to correct version
nvm use

# Or install Node 20
nvm install 20
nvm use 20
```

### Husky Hooks Not Working
```bash
# Reinstall Husky
rm -rf .husky
npm run prepare
```

### Workspace Issues
```bash
# Clean and reinstall
npm run clean
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues
```bash
# Test all API connections
npm run test:apis

# Run examples to see usage
npm run examples
```

## 📚 Additional Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Commitlint](https://commitlint.js.org/)
- [Husky](https://typicode.github.io/husky/)
- [Prettier](https://prettier.io/)
- [SvelteKit](https://kit.svelte.dev/)
- [NPM Workspaces](https://docs.npmjs.com/cli/v9/using-npm/workspaces)

## 🔄 Integration with Python Projects

While most projects use Python, NPM is used for:
1. **Frontend Development** (ChatUi)
2. **Git Hooks & Linting** (Root)
3. **CI/CD Automation** (GitHub Actions)
4. **API Client Utilities** (Scripts)

Python dependencies are managed separately in `requirements.txt` and `requirements-minimal.txt`.

