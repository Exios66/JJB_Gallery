# Documentation Organization

This document describes how documentation files are organized in the `docs/` directory.

## 📁 Directory Structure

```
docs/
├── README.md                    # Main documentation index
├── ORGANIZATION.md              # This file
│
├── setup/                       # Setup & Configuration
│   ├── README.md
│   ├── QUICK_START.md
│   ├── NPM_SETUP.md
│   ├── STORAGE_CONFIGURATION.md
│   ├── EXTERNAL_STORAGE_SETUP.md
│   ├── EXTERNAL_STORAGE_COMPLETE.md
│   ├── pip.conf.README.md
│   └── dependencies.md
│
├── development/                 # Development Guides
│   ├── README.md
│   ├── GIT_PROTOCOL_GUIDE.md
│   └── REMOTE_PYTHON_PATHS.md
│
├── security/                    # Security Documentation
│   ├── README.md
│   └── SECURITY.md
│
├── scripts/                     # Script Documentation
│   ├── README.md
│   ├── scripts.md
│   └── npm-README.md
│
└── projects/                    # Project-Specific Docs
    ├── README.md
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

### Files Moved from Root
- `NPM_SETUP.md` → `docs/setup/NPM_SETUP.md`
- `QUICK_START.md` → `docs/setup/QUICK_START.md`
- `EXTERNAL_STORAGE_SETUP.md` → `docs/setup/EXTERNAL_STORAGE_SETUP.md`
- `EXTERNAL_STORAGE_COMPLETE.md` → `docs/setup/EXTERNAL_STORAGE_COMPLETE.md`
- `STORAGE_CONFIGURATION.md` → `docs/setup/STORAGE_CONFIGURATION.md`
- `pip.conf.README.md` → `docs/setup/pip.conf.README.md`
- `SECURITY.md` → `docs/security/SECURITY.md`

### Files Moved from `docs/`
- `docs/GIT_PROTOCOL_GUIDE.md` → `docs/development/GIT_PROTOCOL_GUIDE.md`
- `docs/REMOTE_PYTHON_PATHS.md` → `docs/development/REMOTE_PYTHON_PATHS.md`

### Files Copied from Other Locations
- `scripts/scripts.md` → `docs/scripts/scripts.md` (copied)
- `scripts/npm/README.md` → `docs/scripts/npm-README.md` (copied)
- `projects/Crewai/LLM_SETUP.md` → `docs/projects/crewai/LLM_SETUP.md` (copied)
- `projects/Crewai/TEST_INSTRUCTIONS.md` → `docs/projects/crewai/TEST_INSTRUCTIONS.md` (copied)
- `projects/Crewai/TOOLS_SUMMARY.md` → `docs/projects/crewai/TOOLS_SUMMARY.md` (copied)
- `Quickstart/docs/dependencies.md` → `docs/setup/dependencies.md` (copied)

## 📝 Files Kept at Root

These files remain at the repository root:
- `README.md` - Main repository README
- `CHANGELOG.md` - Changelog (standard location)
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

