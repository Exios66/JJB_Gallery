# NPM Scripts & Utilities

This repository includes Node.js utilities under `scripts/npm/` plus a set of root npm shortcuts in `package.json`.

## ✅ Requirements

- **Node.js**: `>= 18` (see `package.json` engines)
- **npm**: `>= 9`

## 🚀 Root npm shortcuts (from `package.json`)

These are the recommended entry points because they’re stable and discoverable:

- **Resource fork hygiene**
  - `npm run clean:resource-forks` → `bash scripts/cleanup-macos-resource-forks.sh`
  - `npm run prevent:resource-forks` → `bash scripts/prevent-resource-forks.sh`
- **External storage**
  - `npm run setup:external` → `bash scripts/setup-external-storage.sh`
  - `npm run verify:storage` → `bash scripts/verify-external-storage.sh`
- **Disk cleanup**
  - `npm run clean:disk` → `bash scripts/npm/cleanup-disk-space.sh`
- **API connectivity**
  - `npm run test:apis` → `node scripts/npm/integrations.js`
  - `npm run examples` → `node scripts/npm/examples.js`

## 📁 `scripts/npm/` contents

### `cleanup-disk-space.sh`

**Purpose**
- Frees disk space by cleaning common Node/npm and project build artifacts.

**Usage**

```bash
./scripts/npm/cleanup-disk-space.sh
```

### `integrations.js`

**Purpose**
- Provides API client helpers (e.g. GitHub, OpenAI, Anthropic, Serper, Hugging Face).

**Usage**

```bash
node scripts/npm/integrations.js
```

**Environment variables**

Set these via a local `.env` file or your shell environment:

```env
GITHUB_TOKEN=...
HF_TOKEN=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
SERPER_API_KEY=...
MONGODB_URL=mongodb://localhost:27017
```

**Security note**
- Never commit `.env` files or API keys. Use environment variables and secret managers where possible.

### `examples.js`

**Purpose**
- Demonstrates example usage of the API clients.

**Usage**

```bash
node scripts/npm/examples.js
```

## 🔧 Importing these utilities in code

`scripts/npm/*.js` uses ES Modules. Import with full file extensions:

```javascript
import { GitHubClient } from "./scripts/npm/integrations.js";
```

