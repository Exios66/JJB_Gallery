# Documentation Index

Welcome to the JJB Gallery documentation. This directory contains comprehensive documentation organized by category.

```bash
cd docs # pwd: Documents/docs
```

```bash
├── README.md                    # Main documentation index
├── ORGANIZATION.md              # Organization guide
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
├── development/                 # Development Guides
│   ├── GIT_PROTOCOL_GUIDE.md
│   └── REMOTE_PYTHON_PATHS.md
│
├── security/                    # Security Documentation
│   ├── SECURITY.md              # Security policy
│   └── PRODUCTION_HARDENING.md  # Production hardening (New)
│
├── monitoring/                  # Monitoring & Observability (New)
│   └── SETUP.md                 # Monitoring setup guide
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

## 📚 Documentation Structure

### [Setup & Configuration](./setup/)

Guides for setting up and configuring the repository and its dependencies.

- [Quick Start Guide](./QUICK_START.md) - Get started quickly
- [NPM Setup & Integration](./setup/NPM_SETUP.md) - NPM package configuration
- [Storage Configuration](./setup/STORAGE_CONFIGURATION.md) - External storage setup
- [External Storage Setup](./setup/EXTERNAL_STORAGE_SETUP.md) - Detailed storage setup
- [External Storage Complete](./setup/EXTERNAL_STORAGE_COMPLETE.md) - Complete storage guide
- [Pip Configuration](./setup/pip.conf.README.md) - Python pip configuration
- [Dependencies](./setup/dependencies.md) - Dependency management

### [Production Deployment](./deployment/)

Comprehensive guides for deploying applications to production environments.

- [Production Deployment Guide](./deployment/PRODUCTION_DEPLOYMENT.md) - Best practices and strategies
- [Docker Deployment](./deployment/DOCKER.md) - Containerization and deployment
- [Kubernetes Deployment](./deployment/KUBERNETES.md) - Orchestration and scaling

### [Architecture](./architecture/)

High-level system design and component interaction documentation.

- [Architecture Overview](./architecture/OVERVIEW.md) - System design and data flow

### [Monitoring & Observability](./monitoring/)

Guides for ensuring system health and performance.

- [Monitoring Setup](./monitoring/SETUP.md) - Logging, metrics, and alerting configuration

### [Development](./development/)

Development guides and technical documentation.

- [Git Protocol Guide](./development/GIT_PROTOCOL_GUIDE.md) - Git and GitHub setup
- [Remote Python Paths](./development/REMOTE_PYTHON_PATHS.md) - Remote Python environment configuration

### [Security](./security/)

Security policies and best practices.

- [Security Policy](./security/SECURITY.md) - Security reporting and policies
- [Production Hardening](./security/PRODUCTION_HARDENING.md) - Securing production deployments

### [Scripts](./scripts/)

Documentation for repository scripts and automation.

- [Scripts Overview](./scripts/scripts.md) - All repository scripts
- [NPM Scripts](./scripts/npm-README.md) - NPM-related scripts and tools

### [Projects](./projects/)

Project-specific documentation.

#### CrewAI

- [LLM Setup](./projects/crewai/LLM_SETUP.md) - LLM provider configuration
- [Test Instructions](./projects/crewai/TEST_INSTRUCTIONS.md) - Testing guide
- [Tools Summary](./projects/crewai/TOOLS_SUMMARY.md) - Available tools overview

## 🔍 Quick Links

### Getting Started

1. Read the [Quick Start Guide](./QUICK_START.md)
2. Configure [Storage](./setup/STORAGE_CONFIGURATION.md)
3. Set up [NPM](./setup/NPM_SETUP.md)

### Production Deployment

1. Review [Production Deployment Guide](./deployment/PRODUCTION_DEPLOYMENT.md)
2. Consult [Security Hardening](./security/PRODUCTION_HARDENING.md)
3. Set up [Monitoring](./monitoring/SETUP.md)

### Development

1. Review [Git Protocol Guide](./development/GIT_PROTOCOL_GUIDE.md)
2. Check [Remote Python Paths](./development/REMOTE_PYTHON_PATHS.md) if using remote environments

### Projects

- See individual project READMEs in `projects/` directory
- Check [CrewAI documentation](./projects/crewai/) for multi-agent system

## 📝 Contributing to Documentation

When adding new documentation:

1. Place files in the appropriate subdirectory
2. Update this README with links
3. Follow existing naming conventions
4. Include clear headings and examples

## 🔗 External Resources

- [Main Repository README](../README.md)
- [Changelog](../CHANGELOG.md)
- [License](../LICENSE)

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
