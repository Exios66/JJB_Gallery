# Scripts Documentation

Documentation for the repository automation scripts under `scripts/`.

## 📋 Available Documentation

- **[Scripts Overview](./scripts.md)** - What each script does, prerequisites, and usage examples
- **[NPM Scripts & Utilities](./npm-README.md)** - `scripts/npm/*` plus the root `package.json` shortcuts

## 🧭 Quick Navigation

- **Repository scripts directory**: `../../scripts/README.md`
- **Root npm shortcuts** (recommended entry points):
  - `npm run clean:resource-forks`
  - `npm run prevent:resource-forks`
  - `npm run setup:external`
  - `npm run verify:storage`
  - `npm run clean:disk`
  - `npm run test:apis`

## 🛠️ Script Categories (high level)

### Rendering (Quarto / GitHub Pages)

- **`render_gh_pages.sh`**: Render the full site defined by `_quarto.yml` (`--preview`, `--no-clean`)
- **`render_randomforest.sh`**: Render `Quarto/randomforest.qmd` and start a preview server (`HOST`, `PORT`)
- **`rerender_gh_pages.sh`**: Legacy one-off flow that renders `randomforest.qmd` and moves it to `index.html`
- **`fix_quarto_rendering.sh`**: Helper for Quarto kernel timeout / freeze workflows

### macOS resource fork hygiene (._* files)

- **`archive-macos-resource-forks.sh`**: Move `._*` files into `archives/macos-resource-forks/` (`--dry-run`, `--quiet`)
- **`cleanup-macos-resource-forks.sh`**: Wrapper for the archiver (kept for backwards compatibility)
- **`prevent-resource-forks.sh`**: Adds shell exports to reduce future `._*` creation (one-time setup)

### Storage & disk-space management

- **`setup-external-storage.sh`**: Configure caches to live on an external drive (also exposed as `npm run setup:external`)
- **`verify-external-storage.sh`**: Verify your storage/caching setup (also exposed as `npm run verify:storage`)
- **`free_ram.sh`**: Aggressive cache cleanup across tools; optional process termination via `KILL_IDLE_PROCESSES=yes`
- **`scripts/npm/cleanup-disk-space.sh`**: Node/npm-focused cleanup (also exposed as `npm run clean:disk`)

### Cloud & remote execution

- **`setup_cloud_sandbox.sh`**: Interactive setup for Codespaces/SSH/Docker sandbox execution
- **`use_cloud_sandbox.sh`**: Run Python in the configured sandbox (reads `.cloud_sandbox/config.env`)
- **`launch_codespace.sh`**: Create/open a GitHub Codespace via `gh`

### Git & SSH

- **`setup_git_ssh.sh`**: Interactive SSH key setup and optional remote conversion (HTTPS → SSH)

## 📚 Related Documentation

- [Setup Guides](../setup/) - Initial setup and external storage workflows
- [Development Guides](../development/) - Git protocol and remote environment guidance

