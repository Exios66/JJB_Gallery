# Quick Start Guide

## 🚀 First Time Setup

### 1. Configure External Storage (IMPORTANT!)

**Before installing anything**, configure the external USB drive to store all caches and dependencies:

```bash
npm run setup:external
```

This will:

- Configure npm to use external drive for cache
- Configure pip to use external drive for cache
- Set up Python virtual environments on external drive
- Add environment variables to your shell

**Then reload your shell:**
```bash
source ~/.zshrc  # or ~/.bashrc
```

### 2. Verify Configuration

```bash
npm run verify:storage
```

### 3. Install Dependencies

```bash
# Python dependencies
pip install -r requirements/requirements-minimal.txt

# NPM dependencies
npm install
```

## 📦 Available Commands

### Storage Management
```bash
npm run setup:external    # Configure external storage
npm run verify:storage    # Verify configuration
npm run clean:disk        # Clean up disk space
```

### Development
```bash
npm run dev               # Start ChatUi dev server
npm run build             # Build ChatUi
npm run format            # Format code
```

### API Testing
```bash
npm run test:apis         # Test all API connections
npm run examples          # Run API client examples
```

## 🔧 Troubleshooting

### Disk Space Issues

If you get `ENOSPC: no space left on device`:

1. **Run cleanup:**
   ```bash
   npm run clean:disk
   ```

2. **Verify external storage:**
   ```bash
   npm run verify:storage
   ```

3. **Re-run setup if needed:**
   ```bash
   npm run setup:external
   ```

### External Drive Not Found

1. **Mount the USB drive**
2. **Verify path:**
   ```bash
   ls /Volumes/SEALED/DSHB/GALLERY
   ```
3. **Re-run setup:**
   ```bash
   npm run setup:external
   ```

## 📚 Documentation

- [NPM Setup](setup/NPM_SETUP.md) - Complete NPM configuration guide
- [External Storage Setup](setup/EXTERNAL_STORAGE_SETUP.md) - External drive configuration
- [API Integrations](../scripts/npm/README.md) - API client usage

