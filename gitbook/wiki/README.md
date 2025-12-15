# JJB Gallery Wiki

This directory contains the complete wiki documentation for the JJB Gallery repository.

## Wiki Structure

### Main Pages
- **Home.md** - Main landing page and navigation
- **Installation-Guide.md** - Complete installation instructions
- **Quick-Start.md** - Quick start guide for all projects
- **Project-Overview.md** - Overview of all projects
- **Configuration-Guide.md** - Environment variables and configuration
- **Troubleshooting.md** - Common issues and solutions

### Project Documentation
- **RAG-Model.md** - RAG system documentation
- **Psychometrics.md** - NASA TLX assessment tool
- **ChatUi.md** - SvelteKit chat interface
- **iOS-Chatbot.md** - iOS-inspired chatbot
- **LiteLLM-Integration.md** - LiteLLM proxy and integration
- **CrewAI-Multi-Agent-System.md** - Multi-agent framework
- **Terminal-Agents.md** - Terminal coding agents

### Developer Documentation
- **Architecture-Overview.md** - System architecture
- **API-Reference.md** - Complete API documentation
- **Development-Setup.md** - Development environment setup
- **Testing-Guide.md** - Testing strategies and examples
- **Contributing-Guidelines.md** - Contribution guidelines

### Navigation
- **_Sidebar.md** - Sidebar navigation configuration

## Pushing to GitHub

See [PUSH_INSTRUCTIONS.md](PUSH_INSTRUCTIONS.md) for detailed instructions.

### Quick Push

```bash
cd wiki
git remote add origin https://github.com/Exios66/JJB_Gallery.wiki.git
git push -u origin main
```

## Wiki Statistics

- **Total Pages**: 19
- **Total Content**: ~5,000+ lines
- **Projects Documented**: 7
- **Coverage**: Complete

## Maintenance

### Updating Wiki

1. Edit markdown files in this directory
2. Commit changes: `git add . && git commit -m "Update: description"`
3. Push to GitHub: `git push origin main`

### Adding New Pages

1. Create new `.md` file
2. Add link to `_Sidebar.md`
3. Add link to `Home.md` if needed
4. Commit and push

## Notes

- All pages use GitHub Flavored Markdown
- Images should be stored in repository and referenced
- Links use relative paths within wiki
- Code blocks should specify language for syntax highlighting

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>

