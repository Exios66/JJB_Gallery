# Scripts Overview

This repository includes a set of maintenance and automation scripts under `scripts/`.

## ✅ Conventions

- **Run from repo root** (recommended):

```bash
bash scripts/<script>.sh
```

- Many scripts are executable; when they are, you can also run:

```bash
./scripts/<script>.sh
```

- Some scripts are **interactive** (they will prompt for input) and are not intended for CI.

## 🧰 Inventory

| Script | Category | What it does |
|---|---|---|
| `scripts/render_gh_pages.sh` | Rendering | Render the full Quarto website defined in `_quarto.yml` (optionally preview) |
| `scripts/render_randomforest.sh` | Rendering | Render `Quarto/randomforest.qmd` and launch a local preview server |
| `scripts/rerender_gh_pages.sh` | Rendering (legacy) | Re-render `randomforest.qmd` and move output to `index.html` |
| `scripts/fix_quarto_rendering.sh` | Rendering | Helper for Quarto kernel timeout / freeze workflows |
| `scripts/free_ram.sh` | System | Clear caches/temp files across many tools; optional “kill idle processes” mode |
| `scripts/archive-macos-resource-forks.sh` | Hygiene | Archive `._*` AppleDouble files into `archives/macos-resource-forks/` |
| `scripts/cleanup-macos-resource-forks.sh` | Hygiene | Wrapper for the archiver (kept for compatibility) |
| `scripts/prevent-resource-forks.sh` | Hygiene | Add shell exports to reduce future `._*` creation (one-time setup) |
| `scripts/setup-external-storage.sh` | Storage | Configure npm/pip caches (and env vars) to use an external drive |
| `scripts/verify-external-storage.sh` | Storage | Verify npm/pip/env vars point at the external drive |
| `scripts/setup_cloud_sandbox.sh` | Cloud | Interactive setup for Codespaces / SSH / Docker / manual sandbox |
| `scripts/use_cloud_sandbox.sh` | Cloud | Execute Python in the configured sandbox (`.cloud_sandbox/config.env`) |
| `scripts/launch_codespace.sh` | Cloud | Create/open a GitHub Codespace via `gh` |
| `scripts/setup_git_ssh.sh` | Git/SSH | Interactive SSH key setup and optional remote conversion (HTTPS → SSH) |

For Node-related utilities, see **[NPM Scripts & Utilities](./npm-README.md)**.

## 🧱 Rendering scripts

### `render_gh_pages.sh` (main site render)

**Purpose**
- Renders the full Quarto site defined by `_quarto.yml`.
- Handles cleanup of legacy artifacts and Quarto caches.
- Archives any macOS AppleDouble files (`._*`) via `scripts/archive-macos-resource-forks.sh`.

**Prerequisites**
- Quarto CLI installed (`quarto --version`).
- Python is optional; if `.venv/` or `venv/` exists it will be activated and `QUARTO_PYTHON` will be set.

**Usage**

```bash
# Default: clean build artifacts, render site
./scripts/render_gh_pages.sh

# Skip cleaning (faster; can leave stale artifacts)
./scripts/render_gh_pages.sh --no-clean

# Render and start a local preview server (port 4200)
./scripts/render_gh_pages.sh --preview
```

**Outputs**
- Writes rendered HTML files into the repo tree (e.g. `index.html`, `CHANGELOG.html`, `SECURITY.html`, `projects/*/README.html`).
- Uses `_build/quarto/` for build artifacts when applicable.

**Notes**
- `--preview` runs `quarto preview` and will keep running until you stop it (Ctrl+C).

### `render_randomforest.sh` (single document render + preview)

**Purpose**
- Purges prior outputs for `Quarto/randomforest.qmd`.
- Renders the document (HTML/PDF if configured by Quarto).
- Starts a preview server and opens a browser (when supported).

**Usage**

```bash
./scripts/render_randomforest.sh
```

**Environment variables**
- **`HOST`**: Preview host (default `127.0.0.1`)
- **`PORT`**: Preview port (default `4343`)

```bash
HOST=0.0.0.0 PORT=4343 ./scripts/render_randomforest.sh
```

**Notes**
- This script starts a background preview process and then waits for it; stop it with Ctrl+C.
- If `.venv/` exists, it will be activated and `QUARTO_PYTHON` will be set.

### `rerender_gh_pages.sh` (legacy flow)

**Purpose**
- Re-renders `Quarto/randomforest.qmd` and then **moves** the output to the repo root as `index.html`.

**Usage**

```bash
./scripts/rerender_gh_pages.sh
```

**When to use**
- Prefer `render_gh_pages.sh` for the normal website build.
- Use this only if you intentionally want `randomforest.qmd` to become the root `index.html`.

### `fix_quarto_rendering.sh`

**Purpose**
- Helps with Quarto rendering failures caused by kernel startup timeouts by pre-rendering and/or moving toward `freeze` workflows.

**Usage**

```bash
./scripts/fix_quarto_rendering.sh
```

## 🧹 System cleanup

### `free_ram.sh`

**Purpose**
- Clears caches and temporary files across Python tooling, Node tooling, Quarto, Docker, and more.

**Usage**

```bash
# Safe/default mode
./scripts/free_ram.sh

# Optional (dangerous): attempt to terminate “idle” processes
KILL_IDLE_PROCESSES=yes ./scripts/free_ram.sh
```

**Notes**
- Some operations require **sudo** (Linux page cache drop, swap reset, DNS cache).
- Review before using on production machines; this is intended for developer workstations.

## 🍎 macOS “dot-underscore” resource fork files (._*)

macOS may create AppleDouble `._*` files when copying to non-Apple filesystems. These are noise in git repos and can confuse tooling.

### `archive-macos-resource-forks.sh` (primary)

**Purpose**
- Moves any `._*` files/directories (excluding `.git/` and `archives/`) into:
  - `archives/macos-resource-forks/<original-relative-path>`

**Usage**

```bash
# Archive (move) any existing ._* files
./scripts/archive-macos-resource-forks.sh

# Preview what would happen
./scripts/archive-macos-resource-forks.sh --dry-run

# Reduce output
./scripts/archive-macos-resource-forks.sh --quiet
```

### `cleanup-macos-resource-forks.sh`

Compatibility wrapper that forwards args to `archive-macos-resource-forks.sh`.

### `prevent-resource-forks.sh`

**Purpose**
- Adds shell exports to your `~/.zshrc` or `~/.bashrc`:
  - `COPYFILE_DISABLE=1`
  - `COPY_EXTENDED_ATTRIBUTES_DISABLE=1`

**Usage**

```bash
./scripts/prevent-resource-forks.sh
```

## 💾 External storage scripts

### `setup-external-storage.sh`

**Purpose**
- Creates cache directories on an external drive and points tools at them.
- Writes a `.env` file (only if it doesn’t exist) and appends exports to your shell rc file.

**Usage**

```bash
./scripts/setup-external-storage.sh
```

**Important**
- The external drive mount path is currently hard-coded in the script as `EXTERNAL_BASE` (default: `/Volumes/SEALED/DSHB/GALLERY`). If your drive mounts elsewhere, update the script accordingly.

**Related npm shortcut**
- `npm run setup:external`

### `verify-external-storage.sh`

**Purpose**
- Verifies that npm and pip caches, plus relevant env vars, point to the external drive.

**Usage**

```bash
./scripts/verify-external-storage.sh
```

**Related npm shortcut**
- `npm run verify:storage`

## ☁️ Cloud sandbox scripts

### `setup_cloud_sandbox.sh` (interactive)

**Purpose**
- Guides you through choosing a sandbox approach and writes configuration under `.cloud_sandbox/`.

**Usage**

```bash
./scripts/setup_cloud_sandbox.sh
```

**What it may create**
- `.cloud_sandbox/config.env`
- `.devcontainer/devcontainer.json` (Codespaces)
- `.codespaces/README.md` (Codespaces)
- `Dockerfile.cloud` and `docker-compose.cloud.yml` (Docker option)

### `use_cloud_sandbox.sh`

**Purpose**
- Executes Python via the configured sandbox type (SSH/Docker/manual guidance).

**Usage**

```bash
# Interactive session (SSH) or container shell (Docker)
./scripts/use_cloud_sandbox.sh

# Run a Python file remotely (SSH) or in-container (Docker)
./scripts/use_cloud_sandbox.sh path/to/script.py
```

### `launch_codespace.sh` (interactive)

**Purpose**
- Uses the GitHub CLI (`gh`) to create or open a Codespace for the current repo.

**Usage**

```bash
./scripts/launch_codespace.sh
```

## 🔐 Git & SSH script

### `setup_git_ssh.sh` (interactive)

**Purpose**
- Generates (or reuses) an SSH key, helps you add it to GitHub, tests connectivity, and can optionally update `origin` from HTTPS to SSH.

**Usage**

```bash
./scripts/setup_git_ssh.sh
```

