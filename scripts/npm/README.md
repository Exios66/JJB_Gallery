# NPM Scripts & Utilities

This directory contains NPM-related scripts and utilities for the JJB Gallery repository.

## Files

### `integrations.js`
API client utilities for external services:
- GitHub API
- Hugging Face API
- OpenAI API
- Anthropic API
- Serper API (Web Search)
- MongoDB Helper

**Usage:**
```javascript
import { GitHubClient, OpenAIClient } from './scripts/npm/integrations.js';

const github = new GitHubClient(process.env.GITHUB_TOKEN);
const repo = await github.getRepository('Exios66', 'JJB_Gallery');
```

### `examples.js`
Example usage of all API clients. Run to see how each client works:

```bash
node scripts/npm/examples.js
```

### `cleanup-disk-space.sh`
Disk space cleanup script. Cleans:
- NPM cache
- node_modules directories
- Build artifacts
- Temporary files
- Python cache
- Pip cache

**Usage:**
```bash
./scripts/npm/cleanup-disk-space.sh
```

## Quick Start

### 1. Test API Connections
```bash
node scripts/npm/integrations.js
```

### 2. Run Examples
```bash
node scripts/npm/examples.js
```

### 3. Clean Disk Space (if needed)
```bash
./scripts/npm/cleanup-disk-space.sh
```

## Environment Variables

Set these in your `.env` file:

```env
GITHUB_TOKEN=your_github_token
HF_TOKEN=your_huggingface_token
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
SERPER_API_KEY=your_serper_key
MONGODB_URL=mongodb://localhost:27017
```

## Integration with Projects

### CrewAI Project
- **Type**: Python
- **NPM Integration**: Uses API clients via Node.js scripts
- **Example**: Can call API clients from Python subprocess

### ChatUi Project
- **Type**: SvelteKit (Node.js)
- **NPM Integration**: Direct import in SvelteKit code
- **Example**: 
  ```javascript
  import { testAllConnections } from '../../scripts/npm/integrations.js';
  ```

### Terminal Agents
- **Type**: NPM package (opencode-ai)
- **NPM Integration**: Separate package, not in workspace
- **Installation**: `npm i -g opencode-ai@latest`

## Troubleshooting

### Disk Space Issues
If you encounter `ENOSPC: no space left on device`:

1. Run cleanup script:
   ```bash
   ./scripts/npm/cleanup-disk-space.sh
   ```

2. Clean npm cache manually:
   ```bash
   npm cache clean --force
   rm -rf ~/.npm/_cacache/tmp
   ```

3. Free up system space:
   ```bash
   # Check disk usage
   df -h
   
   # Clean system caches (macOS)
   sudo rm -rf /private/var/folders/*/T/pip-*
   ```

### Module Import Issues
If you get import errors:

1. Ensure you're using ES modules:
   ```json
   { "type": "module" }
   ```

2. Use full file extensions:
   ```javascript
   import { ... } from './integrations.js'; // ✅
   import { ... } from './integrations';    // ❌
   ```

3. Check Node.js version:
   ```bash
   node --version  # Should be >= 18
   ```

## API Client Examples

### GitHub Client
```javascript
import { GitHubClient } from './scripts/npm/integrations.js';

const github = new GitHubClient(process.env.GITHUB_TOKEN);

// Get repository info
const repo = await github.getRepository('Exios66', 'JJB_Gallery');

// Get statistics
const stats = await github.getStats('Exios66', 'JJB_Gallery');

// Create issue
const issue = await github.createIssue(
  'Exios66',
  'JJB_Gallery',
  'Test Issue',
  'This is a test issue'
);
```

### OpenAI Client
```javascript
import { OpenAIClient } from './scripts/npm/integrations.js';

const openai = new OpenAIClient(process.env.OPENAI_API_KEY);

const response = await openai.chatCompletion([
  { role: 'user', content: 'Hello!' }
], 'gpt-3.5-turbo');

console.log(response.choices[0].message.content);
```

### Serper Web Search
```javascript
import { SerperClient } from './scripts/npm/integrations.js';

const serper = new SerperClient(process.env.SERPER_API_KEY);

const results = await serper.search('machine learning', { num: 5 });
console.log(results.organic);
```

## Testing All Connections

```javascript
import { testAllConnections } from './scripts/npm/integrations.js';

const status = await testAllConnections();
console.log(status);
// {
//   github: { status: 'connected', error: null },
//   openai: { status: 'ready', error: null },
//   ...
// }
```

