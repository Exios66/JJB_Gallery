# Remote Python Path Guide

## Common Python Paths by System

### Linux (Most Common)

```bash
/usr/bin/python3        # Default system Python 3
/usr/bin/python         # Python 2 or symlink to python3
/usr/local/bin/python3  # User-installed Python 3
```

### macOS

```bash
/usr/bin/python3        # System Python 3 (may not exist on newer macOS)
/usr/local/bin/python3  # Homebrew Python 3
/opt/homebrew/bin/python3  # Apple Silicon Homebrew
```

### Cloud Services

**AWS EC2 / Ubuntu:**

```bash
/usr/bin/python3
```

**DigitalOcean / Ubuntu:**

```bash
/usr/bin/python3
```

**Google Cloud Platform:**

```bash
/usr/bin/python3
```

**Azure:**

```bash
/usr/bin/python3
```

**Docker Containers:**

```bash
/usr/local/bin/python3  # Official Python images
/usr/bin/python3        # Some base images
```

## How to Find Python Path on Remote Server

### Method 1: SSH and Check

```bash
# SSH into your server
ssh user@your-server.com

# Check Python 3 location
which python3
# or
whereis python3

# Check Python version
python3 --version

# Exit
exit
```

### Method 2: One-liner Command

```bash
ssh user@your-server.com "which python3"
```

### Method 3: Check Multiple Locations

```bash
ssh user@your-server.com "ls -la /usr/bin/python3 /usr/local/bin/python3 2>/dev/null"
```

## Virtual Environments

If you're using a virtual environment on the remote server:

```bash
# Path to venv Python
/path/to/your/venv/bin/python3

# Example
/home/user/projects/myproject/.venv/bin/python3
```

## Recommended: Use Default

For most cases, **just press Enter** to use the default `/usr/bin/python3` - this works on:

- ✅ Most Linux distributions (Ubuntu, Debian, CentOS, etc.)
- ✅ Most cloud providers
- ✅ Docker containers (usually)

## If Default Doesn't Work

1. SSH into your server
2. Run: `which python3`
3. Use that path in the setup script

## Example Session

```bash
$ ./scripts/setup_cloud_sandbox.sh
# ... select option 2 (SSH) ...
Enter SSH host (e.g., user@example.com): user@myserver.com
Enter remote Python path (default: /usr/bin/python3): [Press Enter]
Enter remote workspace path: /home/user/projects/JJB_Gallery
```

Or if you know it's in a different location:

```bash
Enter remote Python path (default: /usr/bin/python3): /usr/local/bin/python3
```

## Testing the Path

After setup, test the connection:

```bash
./scripts/use_cloud_sandbox.sh python3 --version
```

This will show you if the Python path is correct.

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
