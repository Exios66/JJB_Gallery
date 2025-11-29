# Auto-Launch GitHub Codespace

Automatically create and launch a GitHub Codespace in the free tier with one command.

## Prerequisites

1. **Install GitHub CLI**:
   ```bash
   # macOS
   brew install gh
   
   # Linux - see https://cli.github.com/manual/installation
   # Windows
   winget install GitHub.cli
   ```

2. **Authenticate**:
   ```bash
   gh auth login
   ```
   Follow the prompts to authenticate with GitHub.

3. **Push Repository**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

## Usage

Simply run:
```bash
./scripts/launch_codespace.sh
```

## What Happens

1. ✅ Checks for GitHub CLI installation
2. ✅ Verifies you're authenticated
3. ✅ Detects your GitHub repository
4. ✅ Checks for existing Codespaces (reuses if found)
5. ✅ Creates new Codespace if needed (free tier)
6. ✅ Waits for Codespace to be ready
7. ✅ Opens in VS Code (if installed) or web browser
8. ✅ All packages from `requirements.txt` auto-install

## Free Tier Details

- **Included**: 60 hours/month for personal accounts
- **Machine**: 2 cores, 4GB RAM (default)
- **Storage**: 15GB per Codespace
- **Auto-suspend**: After 30 minutes of inactivity

## Features

- **Smart reuse**: Uses existing Codespace if available
- **Multiple options**: Opens in VS Code or browser
- **Status checking**: Waits for Codespace to be ready
- **Error handling**: Clear error messages and suggestions
- **Cost tracking**: Uses free tier by default

## Troubleshooting

### "GitHub CLI not installed"
Install GitHub CLI (see Prerequisites above).

### "Not authenticated"
Run `gh auth login` and follow the prompts.

### "Repository not found"
Ensure your repository is pushed to GitHub:
```bash
git push -u origin main
```

### "Could not create Codespace"
- Check your Codespace quota: `gh api user/codespaces`
- Verify repository exists: `gh repo view OWNER/REPO`
- Try creating manually from GitHub web interface

### Codespace won't open
- Check Codespace status: `gh codespace list`
- Open manually: `gh codespace view --web`
- Or go to: https://github.com/codespaces

## Advanced Usage

### List all Codespaces
```bash
gh codespace list
```

### View specific Codespace
```bash
gh codespace view --codespace CODESPACE_NAME
```

### Stop a Codespace
```bash
gh codespace stop --codespace CODESPACE_NAME
```

### Delete a Codespace
```bash
gh codespace delete --codespace CODESPACE_NAME
```

### SSH into Codespace
```bash
gh codespace ssh --codespace CODESPACE_NAME
```

## Integration with VS Code

If you have VS Code installed, the script will automatically:
1. Open the Codespace in VS Code Desktop
2. Install the GitHub Codespaces extension if needed
3. Connect to your cloud development environment

## Cost Management

- Free tier: 60 hours/month included
- Monitor usage: `gh api user/codespaces`
- Auto-suspend: Codespaces pause after 30 min inactivity
- Delete unused: Remove old Codespaces to save quota

## Next Steps

Once your Codespace is running:
1. All packages are already installed
2. Navigate to your project: `cd projects/Crewai`
3. Run your code: `python main.py`
4. Start developing!

