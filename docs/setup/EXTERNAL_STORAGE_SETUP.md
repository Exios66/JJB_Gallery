# External USB Drive Storage Configuration

This repository is configured to store all storage-intensive files (npm cache, pip cache, node_modules, etc.) on an external USB drive to free up local disk space.

## 🎯 Quick Setup

### 1. Run the Setup Script

```bash
./scripts/setup-external-storage.sh
```

This script will:
- ✅ Create necessary directories on the external drive
- ✅ Configure npm to use external drive for cache
- ✅ Configure pip to use external drive for cache
- ✅ Set up Python virtual environments on external drive
- ✅ Add environment variables to your shell config
- ✅ Create `.env` file with paths

### 2. Reload Your Shell

```bash
# For zsh
source ~/.zshrc

# For bash
source ~/.bashrc
```

### 3. Verify Configuration

```bash
# Check npm cache location
npm config get cache

# Should show: /Volumes/SEALED/DSHB/GALLERY/.npm-cache

# Check pip cache location
pip cache dir

# Should show: /Volumes/SEALED/DSHB/GALLERY/.pip-cache
```

## 📁 Directory Structure on External Drive

```
/Volumes/SEALED/DSHB/GALLERY/
├── .npm-cache/          # NPM package cache
├── .npm-tmp/            # NPM temporary files
├── .npm-global/          # Global npm packages (optional)
├── .pip-cache/          # Pip package cache
├── .python-venvs/        # Python virtual environments
├── .node-modules/        # Shared node_modules (optional)
└── .quarto-cache/       # Quarto cache
```

## 🔧 Manual Configuration

If you prefer to configure manually:

### NPM Configuration

```bash
# Set npm cache location
npm config set cache /Volumes/SEALED/DSHB/GALLERY/.npm-cache --global

# Set temporary directory
export TMPDIR=/Volumes/SEALED/DSHB/GALLERY/.npm-tmp

# Verify
npm config get cache
```

The `.npmrc` file in the repository root is already configured with these paths.

### Pip Configuration

```bash
# Set pip cache location
pip config set global.cache-dir /Volumes/SEALED/DSHB/GALLERY/.pip-cache

# Or set environment variable
export PIP_CACHE_DIR=/Volumes/SEALED/DSHB/GALLERY/.pip-cache
```

### Python Virtual Environments

```bash
# Set virtual environment location
export WORKON_HOME=/Volumes/SEALED/DSHB/GALLERY/.python-venvs

# Create venv on external drive
python3 -m venv /Volumes/SEALED/DSHB/GALLERY/.python-venvs/jjb-gallery
```

## 📝 Environment Variables

Add these to your `.env` file or shell config:

```bash
# External Drive Base Path
EXTERNAL_DRIVE_BASE=/Volumes/SEALED/DSHB/GALLERY

# NPM Configuration
export NPM_CONFIG_CACHE="$EXTERNAL_DRIVE_BASE/.npm-cache"
export TMPDIR="$EXTERNAL_DRIVE_BASE/.npm-tmp"

# Pip Configuration
export PIP_CACHE_DIR="$EXTERNAL_DRIVE_BASE/.pip-cache"

# Python Virtual Environments
export WORKON_HOME="$EXTERNAL_DRIVE_BASE/.python-venvs"
```

## 🧹 Cleanup

### Clean External Drive Storage

```bash
# Clean external drive caches
npm run clean:disk

# Select option 2 (External drive only) or 3 (Both)
```

### Manual Cleanup

```bash
# Clean npm cache on external drive
rm -rf /Volumes/SEALED/DSHB/GALLERY/.npm-cache/*

# Clean pip cache on external drive
rm -rf /Volumes/SEALED/DSHB/GALLERY/.pip-cache/*

# Clean temporary files
rm -rf /Volumes/SEALED/DSHB/GALLERY/.npm-tmp/*
```

## ⚠️ Important Notes

### 1. External Drive Must Be Mounted

The external drive must be mounted before running npm/pip commands. If the drive is not mounted:

- npm/pip will fall back to default locations
- You may encounter errors
- Check mount status: `df -h | grep SEALED`

### 2. Performance Considerations

- External USB drives may be slower than internal storage
- For development, this is usually acceptable
- For production builds, consider using internal storage temporarily

### 3. Backup Considerations

- External drive storage is not automatically backed up
- Consider backing up important caches if needed
- node_modules can always be regenerated with `npm install`

### 4. Multiple Machines

If working on multiple machines:
- Each machine needs the external drive mounted
- Configuration is per-machine
- Consider using the same drive path on all machines

## 🔍 Verification

### Check Current Storage Locations

```bash
# NPM cache
echo "NPM Cache: $(npm config get cache)"

# Pip cache
echo "Pip Cache: $(pip cache dir)"

# Python venv location
echo "Python Venvs: ${WORKON_HOME:-Not set}"

# Temporary directory
echo "Temp Dir: ${TMPDIR:-Not set}"
```

### Check Disk Space

```bash
# External drive space
df -h /Volumes/SEALED/DSHB/GALLERY

# Local drive space
df -h ~
```

## 🐛 Troubleshooting

### Issue: "No space left on device" even after setup

**Solution:**
1. Verify external drive is mounted: `df -h | grep SEALED`
2. Check npm is using external cache: `npm config get cache`
3. Run cleanup: `npm run clean:disk`
4. Verify paths in `.npmrc` file

### Issue: npm/pip still using local cache

**Solution:**
1. Check environment variables: `echo $NPM_CONFIG_CACHE`
2. Reload shell config: `source ~/.zshrc` (or `~/.bashrc`)
3. Verify `.npmrc` file has correct paths
4. Run setup script again: `./scripts/setup-external-storage.sh`

### Issue: External drive not found

**Solution:**
1. Mount the USB drive
2. Update `EXTERNAL_BASE` in `scripts/setup-external-storage.sh` if path changed
3. Verify path: `ls /Volumes/SEALED/DSHB/GALLERY`

### Issue: Slow npm/pip operations

**Solution:**
- This is expected with USB drives
- Consider using USB 3.0+ for better performance
- For critical operations, temporarily use local storage

## 📊 Storage Savings

By moving storage to external drive, you can save significant local disk space:

- **npm cache**: Typically 500MB - 2GB
- **pip cache**: Typically 200MB - 1GB
- **node_modules**: Varies by project (can be 100MB - 5GB+)
- **Python venvs**: Typically 100MB - 500MB each

**Total potential savings: 1GB - 10GB+ on local drive**

## 🔄 Migration from Local to External

If you already have local caches:

```bash
# Move npm cache
mv ~/.npm /Volumes/SEALED/DSHB/GALLERY/.npm-cache

# Move pip cache (if exists)
if [ -d ~/.cache/pip ]; then
    mv ~/.cache/pip /Volumes/SEALED/DSHB/GALLERY/.pip-cache
fi
```

## 📚 Related Documentation

- [NPM Setup Guide](NPM_SETUP.md)
- [Python Requirements](requirements-minimal.txt)
- [Scripts Documentation](scripts/scripts.md)

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>

