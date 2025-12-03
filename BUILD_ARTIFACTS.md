# Build Artifacts Organization

## Expected Directory Structure

After rendering, Quarto creates the following structure:

```
JJB_Gallery/
├── index.html              # Rendered HTML files (in root for GitHub Pages)
├── CHANGELOG.html
├── projects/*/README.html  # Project documentation pages
├── _build/                 # Build artifacts directory (gitignored)
│   └── quarto/
│       ├── site_libs/      # Quarto CSS/JS assets
│       ├── index_files/    # HTML dependencies
│       └── *.html          # Additional artifacts
└── Quarto/
    └── randomforest.html   # Rendered Quarto documents
```

## Build Artifacts Location

- **HTML files**: In repository root (for GitHub Pages compatibility)
- **Support files**: In `_build/quarto/` directory (automatically organized by Quarto)
- **Legacy artifacts**: Automatically cleaned from root directory

## Cleanup Process

The `render_gh_pages.sh` script automatically cleans up:

1. **Old build directories**: `_build/quarto/` (for fresh builds)
2. **Quarto cache**: `.quarto/` directories
3. **Legacy artifacts**: Old `site_libs/`, `index_files/`, etc. from root

### Legacy Artifact Cleanup

If you see messages like:
```
⚠ Removed old directory: /path/to/site_libs (should be in _build/quarto/)
```

This is **expected behavior**. The script is:
- ✅ Removing old artifact directories from the root
- ✅ Ensuring a clean build environment
- ✅ Organizing artifacts properly in `_build/quarto/`

## GitHub Pages Configuration

For GitHub Pages to work correctly:
- HTML files must be in the repository root
- Support files can be in `_build/` (gitignored) or embedded
- The `output-dir: .` setting ensures HTML files are in root

## Configuration

The current Quarto configuration (`_quarto.yml`) uses:
- `output-dir: .` - Outputs HTML to root (required for GitHub Pages)
- `embed-resources: false` - Keeps resources separate (better for caching)

This means:
- HTML files → Root directory (for GitHub Pages)
- CSS/JS/resources → `_build/quarto/` or embedded in HTML

## Notes

- The `_build/` directory is automatically gitignored
- Legacy artifacts in root are cleaned automatically
- No manual cleanup needed - the script handles everything

