# Wiki Push Instructions

Instructions for pushing the wiki to GitHub.

## Prerequisites

1. GitHub repository with wiki enabled
2. Git configured with your credentials
3. Access to push to the wiki repository

## Push to GitHub Wiki

### Option 1: Direct Push (Recommended)

```bash
cd wiki

# Add remote (if not already added)
git remote add origin https://github.com/Exios66/JJB_Gallery.wiki.git

# Push to GitHub
git push -u origin main
```

### Option 2: Using SSH

```bash
cd wiki

# Add remote with SSH
git remote set-url origin git@github.com:Exios66/JJB_Gallery.wiki.git

# Push to GitHub
git push -u origin main
```

### Option 3: Using GitHub CLI

```bash
cd wiki

# Push using gh CLI
gh repo sync Exios66/JJB_Gallery.wiki --source .
```

## Verify Push

1. Go to: https://github.com/Exios66/JJB_Gallery/wiki
2. Verify all pages are present
3. Check that links work correctly

## Updating the Wiki

After making changes:

```bash
cd wiki

# Add changes
git add .

# Commit
git commit -m "Update: description of changes"

# Push
git push origin main
```

## Troubleshooting

### Authentication Issues

```bash
# Use GitHub Personal Access Token
git remote set-url origin https://<token>@github.com/Exios66/JJB_Gallery.wiki.git

# Or configure SSH
ssh-keygen -t ed25519 -C "your_email@example.com"
# Add key to GitHub Settings > SSH and GPG keys
```

### Permission Issues

- Ensure you have write access to the repository
- Check repository settings allow wiki editing
- Verify you're pushing to the correct remote

### Wiki Not Enabled

If wiki is not enabled:
1. Go to repository Settings
2. Enable "Wikis" in Features section
3. Retry push

## Notes

- Wiki pages use Markdown format
- GitHub automatically renders Markdown
- `_Sidebar.md` controls the sidebar navigation
- `Home.md` is the main landing page

