# Documentation Organization

This document describes how documentation files are organized in the `docs/` directory.

## 📁 Directory Structure

```
docs/
├── README.md                    # Main documentation index
├── ORGANIZATION.md              # This file
├── QUICK_START.md               # Quick start guide
│
├── setup/                       # Setup & Configuration
│   ├── NPM_SETUP.md
│   ├── STORAGE_CONFIGURATION.md
│   ├── EXTERNAL_STORAGE_SETUP.md
│   ├── EXTERNAL_STORAGE_COMPLETE.md
│   ├── pip.conf.README.md
│   └── dependencies.md
│
├── deployment/                  # Production Deployment (New)
│   ├── PRODUCTION_DEPLOYMENT.md # Main production guide
│   ├── DOCKER.md                # Docker deployment guide
│   └── KUBERNETES.md            # Kubernetes deployment guide
│
├── architecture/                # Architecture Documentation (New)
│   └── OVERVIEW.md              # System architecture overview
│
├── monitoring/                  # Monitoring & Observability (New)
│   └── SETUP.md                 # Monitoring setup guide
│
├── development/                 # Development Guides
│   ├── GIT_PROTOCOL_GUIDE.md
│   └── REMOTE_PYTHON_PATHS.md
│
├── security/                    # Security Documentation
│   ├── SECURITY.md              # Security policy
│   └── PRODUCTION_HARDENING.md  # Production hardening (New)
│
├── scripts/                     # Script Documentation
│   ├── scripts.md
│   └── npm-README.md
│
└── projects/                    # Project-Specific Docs
    └── crewai/
        ├── LLM_SETUP.md
        ├── TEST_INSTRUCTIONS.md
        └── TOOLS_SUMMARY.md
```

## 📋 File Organization Rules

### Setup & Configuration (`docs/setup/`)

Contains all setup guides, configuration instructions, and dependency management:

- Quick start guides
- Package manager setup (NPM, pip)
- Storage configuration
- Dependency documentation

### Production Deployment (`docs/deployment/`)

Documentation for deploying applications to production:

- Deployment strategies
- Docker and Kubernetes guides
- Production environment configuration

### Architecture (`docs/architecture/`)

High-level system design documentation:

- System overview
- Component interaction
- Data flow diagrams

### Monitoring (`docs/monitoring/`)

Observability and health check documentation:

- Logging setup
- Metrics collection
- Alerting configuration

### Development (`docs/development/`)

Technical documentation for developers:

- Git and GitHub setup
- Remote development configuration
- Development workflows

### Security (`docs/security/`)

Security-related documentation:

- Security policies
- Vulnerability reporting
- Security best practices
- Production hardening guides

### Scripts (`docs/scripts/`)

Documentation for repository scripts:

- Script overview and usage
- NPM scripts documentation
- Automation tools

### Projects (`docs/projects/`)

Project-specific documentation:

- Individual project guides
- Project setup instructions
- Project-specific tools and features

## 🔄 Migration Notes

### Files Moved from Root (2024-12-02 Reorganization)

- `NPM_SETUP.md` → `docs/setup/NPM_SETUP.md`
- `QUICK_START.md` → `docs/QUICK_START.md`
- `EXTERNAL_STORAGE_SETUP.md` → `docs/setup/EXTERNAL_STORAGE_SETUP.md`
- `EXTERNAL_STORAGE_COMPLETE.md` → `docs/setup/EXTERNAL_STORAGE_COMPLETE.md`
- `STORAGE_CONFIGURATION.md` → `docs/setup/STORAGE_CONFIGURATION.md`
- `pip.conf.README.md` → `docs/setup/pip.conf.README.md`
- `requirements.txt` → `requirements/requirements.txt`
- `requirements-minimal.txt` → `requirements/requirements-minimal.txt`
- `requirements-micro.txt` → `requirements/requirements-micro.txt`
- `pip.conf` → `config/pip.conf`
- `changelogger.prompt.yml` → `docs/changelogger.prompt.yml`
- `SECURITY.md` → Kept at root (standard location)

### Files Moved from `docs/`

- `docs/GIT_PROTOCOL_GUIDE.md` → `docs/development/GIT_PROTOCOL_GUIDE.md`
- `docs/REMOTE_PYTHON_PATHS.md` → `docs/development/REMOTE_PYTHON_PATHS.md`

## 📝 Files Kept at Root

These files remain at the repository root:

- `README.md` - Main repository README
- `CHANGELOG.md` - Changelog (standard location)
- `SECURITY.md` - Security policy (standard location)
- `LICENSE` - License file (standard location)
- `package.json` - NPM configuration (standard location)
- `_quarto.yml` - Quarto website configuration
- `index.qmd` - Quarto website source
- `index.html` - Generated website homepage
- `search.json` - Website search index
- `theme-switcher.html` - Website theme switcher
- Project READMEs in `projects/*/README.md` - Project-specific READMEs

## 🔗 Link Updates

When referencing documentation, use paths relative to the repository root:

- `docs/setup/QUICK_START.md` (not `QUICK_START.md`)
- `docs/security/SECURITY.md` (not `SECURITY.md`)
- `docs/development/GIT_PROTOCOL_GUIDE.md` (not `docs/GIT_PROTOCOL_GUIDE.md`)

## ✅ Benefits of This Organization

1. **Clear Categorization**: Easy to find documentation by topic
2. **Scalability**: Easy to add new documentation in appropriate categories
3. **Maintainability**: Related documentation grouped together
4. **Navigation**: README files in each directory provide quick navigation
5. **Consistency**: Standard structure across all documentation

## 📚 Adding New Documentation

When adding new documentation:

1. **Determine Category**: Choose the appropriate subdirectory
2. **Follow Naming**: Use descriptive, consistent naming
3. **Update READMEs**: Add links to relevant README files
4. **Update Index**: Update `docs/README.md` if adding new categories

## 🔍 Finding Documentation

- **Main Index**: Start at `docs/README.md`
- **Category READMEs**: Each subdirectory has a README with links
- **Search**: Use your editor's search to find specific topics
- **Project READMEs**: See individual project directories for project-specific docs

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
