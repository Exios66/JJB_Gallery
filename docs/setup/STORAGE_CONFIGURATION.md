# Storage Configuration Summary

This repository is configured to use an **external USB drive** for all storage-intensive operations to prevent local disk space issues.

## 📍 External Drive Location

**Base Path:** `/Volumes/SEALED/DSHB/GALLERY`

**Available Space:** 110GB (as of setup)

## 🗂️ Directory Structure

All storage-intensive files are stored on the external drive:

```
/Volumes/SEALED/DSHB/GALLERY/
├── .npm-cache/          # NPM package cache (saves ~500MB-2GB local space)
├── .npm-tmp/            # NPM temporary files
├── .npm-global/         # Global npm packages (optional)
├── .pip-cache/          # Pip package cache (saves ~200MB-1GB local space)
├── .python-venvs/       # Python virtual environments (saves ~100MB-500MB each)
├── .node-modules/       # Shared node_modules (optional)
└── .quarto-cache/       # Quarto document cache
```

## ⚙️ Configuration Files

### NPM Configuration
- **File:** `.npmrc`
- **Cache Location:** `/Volumes/SEALED/DSHB/GALLERY/.npm-cache`
- **Temp Location:** `/Volumes/SEALED/DSHB/GALLERY/.npm-tmp`

### Pip Configuration
- **File:** `pip.conf` (copy to `~/.pip/pip.conf`)
- **Cache Location:** `/Volumes/SEALED/DSHB/GALLERY/.pip-cache`

### Environment Variables
- **File:** `.env` (created by setup script)
- **Shell Config:** Added to `~/.zshrc` or `~/.bashrc`

## 🚀 Setup Commands

```bash
# 1. Run setup (one-time)
npm run setup:external

# 2. Reload shell
source ~/.zshrc  # or ~/.bashrc

# 3. Verify configuration
npm run verify:storage

# 4. Install dependencies
npm install
pip install -r requirements-minimal.txt
```

## ✅ Verification

After setup, verify everything is configured:

```bash
# Check npm cache
npm config get cache
# Should show: /Volumes/SEALED/DSHB/GALLERY/.npm-cache

# Check pip cache
pip cache dir
# Should show: /Volumes/SEALED/DSHB/GALLERY/.pip-cache

# Check environment variables
echo $NPM_CONFIG_CACHE
echo $PIP_CACHE_DIR
```

## 📊 Storage Savings

By using external storage, you save significant local disk space:

| Component | Typical Size | Saved on Local Drive |
|-----------|--------------|---------------------|
| npm cache | 500MB - 2GB | ✅ Yes |
| pip cache | 200MB - 1GB | ✅ Yes |
| node_modules | 100MB - 5GB+ | ✅ Yes (if moved) |
| Python venvs | 100MB - 500MB each | ✅ Yes |
| **Total** | **1GB - 10GB+** | **✅ Significant savings** |

## 🔄 Migration

If you already have local caches, you can migrate them:

```bash
# Migrate npm cache (if exists)
if [ -d "$HOME/.npm" ]; then
    mv "$HOME/.npm" "/Volumes/SEALED/DSHB/GALLERY/.npm-cache"
fi

# Migrate pip cache (if exists)
if [ -d "$HOME/.cache/pip" ]; then
    mv "$HOME/.cache/pip" "/Volumes/SEALED/DSHB/GALLERY/.pip-cache"
fi
```

## ⚠️ Important Notes

1. **External drive must be mounted** before running npm/pip commands
2. **Performance**: USB drives may be slower than internal storage (acceptable for development)
3. **Backup**: External drive storage is not automatically backed up
4. **Portability**: Configuration is per-machine; each machine needs the drive mounted

## 🐛 Troubleshooting

See [EXTERNAL_STORAGE_SETUP.md](EXTERNAL_STORAGE_SETUP.md) for detailed troubleshooting.

Quick fixes:
- **Not using external drive?** → Run `npm run setup:external`
- **Drive not mounted?** → Mount USB drive first
- **Still getting ENOSPC?** → Run `npm run clean:disk`

## 📚 Related Documentation

- [EXTERNAL_STORAGE_SETUP.md](EXTERNAL_STORAGE_SETUP.md) - Complete setup guide
- [NPM_SETUP.md](NPM_SETUP.md) - NPM configuration details
- [QUICK_START.md](QUICK_START.md) - Quick start guide

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>

