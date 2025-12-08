# Quick Start Guide

## 🚀 First Time Setup (Development)

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

## 🏭 Production Quick Start

### 1. Docker Deployment (Recommended)

Deploy the entire stack using Docker Compose:

```bash
# 1. Create production env file
cp .env.example .env.production
# Edit .env.production with your API keys and production settings

# 2. Build and run containers
docker-compose -f docker-compose.prod.yml up -d --build
```

### 2. Production Environment Variables

Ensure these variables are set in your CI/CD or production environment:

| Variable | Description | Example |
|----------|-------------|---------|
| `NODE_ENV` | Environment mode | `production` |
| `OPENAI_API_KEY` | LLM Provider Key | `sk-...` |
| `DATABASE_URL` | Production DB Connection | `postgres://user:pass@host:5432/db` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

### 3. Production Readiness Checklist

- [ ] **Security**: API keys are rotated and secured
- [ ] **HTTPS**: TLS/SSL certificates are configured
- [ ] **Monitoring**: Health check endpoints are monitored
- [ ] **Backup**: Database backup schedule is active
- [ ] **Updates**: All dependencies are patched to latest secure versions

See [Production Deployment Guide](./deployment/PRODUCTION_DEPLOYMENT.md) for detailed instructions.

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
- [Production Deployment](deployment/PRODUCTION_DEPLOYMENT.md) - Production guide
