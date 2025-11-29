# Cloud Sandbox Quick Start

## Fastest Setup: GitHub Codespaces (Auto-launch)

### Option 1: Automatic Launch (Recommended)

1. **Install GitHub CLI** (if not installed):
   ```bash
   # macOS
   brew install gh
   gh auth login
   ```

2. **Push to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Add cloud sandbox configuration"
   git push
   ```

3. **Auto-launch Codespace**:
   ```bash
   ./scripts/launch_codespace.sh
   ```

4. **Done!** Codespace opens automatically with all packages installed!

### Option 2: Manual Launch

1. Push to GitHub
2. Go to your GitHub repository
3. Click "Code" → "Codespaces" → "Create codespace on main"
4. Wait ~2-3 minutes for setup

Both methods use the free tier (60 hours/month).

## Alternative: Docker (Local)

If you want to test locally without using disk space:

```bash
# Build and start container
docker-compose -f docker-compose.cloud.yml up -d

# Enter container shell
docker-compose -f docker-compose.cloud.yml exec sandbox bash

# Run your code
python projects/Crewai/main.py
```

## Test Your Setup

Once your cloud sandbox is running, test with:

```bash
# Test imports
python -c "import crewai; print('✅ CrewAI imported successfully!')"

# Test project
cd projects/Crewai
python main.py --help
```

## Cost Comparison

| Option | Cost | Disk Usage |
|--------|------|------------|
| GitHub Codespaces | Free (60hrs/mo) | 0 MB local |
| Docker | Free | ~500 MB (image) |
| Remote SSH | Free (if you have server) | 0 MB local |
| Replit | Free tier available | 0 MB local |

## Need Help?

See `.cloud_sandbox/README.md` for detailed instructions.

