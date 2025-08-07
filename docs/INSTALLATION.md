# Installation Guide

This guide provides detailed instructions for installing Claude Code Session Automation.

## Prerequisites

- macOS (required for LaunchAgent functionality)
- Python 3.8 or higher
- Claude Code CLI tool installed and authenticated

### Verify Claude Code Installation

```bash
# Check if Claude Code is installed
which claude

# Verify authentication
claude login --help
```

## Installation Methods

### Method 1: Development Installation (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/with-developer/claude-code-automation.git
cd claude-code-automation

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install in development mode
pip install -e .

# 4. Verify installation
claude-code-automation help
```

### Method 2: Homebrew (Future)

```bash
# Add custom tap (when released)
brew tap with-developer/claude-code-automation

# Install
brew install claude-code-automation
```

## First Time Setup

After installation, test the basic functionality:

```bash
# Test CLI
claude-code-automation help

# Schedule a test session (optional)
claude-code-automation schedule 15:30

# Check the schedule
claude-code-automation list

# Clean up test
claude-code-automation clear
```

## Troubleshooting

### Permission Issues

If you encounter permission errors:

```bash
# Ensure proper directory permissions
mkdir -p ~/.config/claude-code-automation
chmod 755 ~/.config/claude-code-automation
```

### Claude Code Not Found

```bash
# Install Claude Code if not available
# Follow official Claude Code installation instructions
```

### Python Version Issues

```bash
# Check Python version
python3 --version

# Use specific Python version if needed
python3.11 -m venv venv
```

## Next Steps

After successful installation:

1. Read the [Usage Guide](USAGE.md)
2. Configure your first schedule
3. Check the [Troubleshooting Guide](TROUBLESHOOTING.md) if needed