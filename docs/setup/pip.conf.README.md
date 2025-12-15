# Pip Configuration File

This `pip.conf` file configures pip to use the external USB drive for package caching.

## Installation

### Option 1: User-level Configuration (Recommended)

Copy to your pip config directory:

```bash
# macOS/Linux
mkdir -p ~/.pip
cp pip.conf ~/.pip/pip.conf

# Or create symlink
ln -s $(pwd)/pip.conf ~/.pip/pip.conf
```

### Option 2: Project-level Configuration

Pip will also read `pip.conf` from the project root if it exists.

### Option 3: Environment Variable

Alternatively, set the environment variable:

```bash
export PIP_CACHE_DIR=/Volumes/SEALED/DSHB/GALLERY/.pip-cache
```

## Verification

Check that pip is using the external cache:

```bash
pip cache dir
# Should show: /Volumes/SEALED/DSHB/GALLERY/.pip-cache
```

## Notes

- The external drive must be mounted before using pip
- If the drive is not mounted, pip will use default cache location
- Run `npm run verify:storage` to check all configurations

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>

