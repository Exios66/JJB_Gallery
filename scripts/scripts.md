# SCRIPTS

## 1. render_randomforest.sh

Run the render_randomforest.sh script to render the randomforest.qmd file to a html and pdf file. This script will also start a preview server on the default port 4343.

Run the script:

```bash
./scripts/render_randomforest.sh
```

Open the preview server in your browser:

```bash
open http://localhost:4343
```

## 2. free_ram.sh

The free_ram.sh script frees up unnecessary RAM by clearing various caches and temporary files that accumulate during development. This script is particularly useful when working with large Jupyter notebooks, Python projects, or Quarto documents that generate cached files.

### What it clears

- **Python cache files**: `__pycache__` directories, `.pyc`, and `.pyo` files
- **Jupyter/IPython checkpoints**: `.ipynb_checkpoints` directories
- **Quarto cache**: Quarto freeze directories and user cache
- **pip cache**: Cached pip packages
- **Python bytecode**: Additional bytecode files

### Usage

```bash
./scripts/free_ram.sh
```

### Features

- Cross-platform support (macOS and Linux)
- Colored output for better readability
- Memory usage reporting before and after cleanup
- Safe cleanup (doesn't require sudo on macOS for basic operations)
- Summary of total space freed

### Notes

- On Linux, system page cache clearing requires sudo privileges
- The script will skip operations that require elevated privileges if not available
- All cleanup operations are safe and only remove cache/temporary files

## Virtual Environment Management

Activate the Python virtual environment:

```bash
source .venv/bin/activate
```

Deactivate the Python virtual environment:

```bash
deactivate
```

## Manual System Cache Clearing (Linux)

Clear cached memory to help preserve system memory and RAM (requires sudo privileges):

```bash
sudo sync; sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

Note: This functionality is included in the `free_ram.sh` script on Linux systems when run with appropriate privileges.
