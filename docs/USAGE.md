# Usage Guide

Complete guide to using Claude Code Session Automation.

## Overview

Claude Code Session Automation helps you bypass rate limits by automatically starting sessions at scheduled times. Each session runs for 5 hours, so proper scheduling ensures continuous availability.

## Basic Commands

### Schedule Sessions

```bash
# Schedule single session
claude-code-automation schedule 14:30

# Schedule multiple sessions (recommended)
claude-code-automation schedule 06:00 12:00 18:00

# Using HHMM format
claude-code-automation schedule 0600 1200 1800
```

### Manage Schedules

```bash
# View current schedules
claude-code-automation list

# Clear all schedules
claude-code-automation clear

# Check service status
claude-code-automation status
```

### Manual Operations

```bash
# Start session immediately
claude-code-automation start

# Get help
claude-code-automation help
```

## Advanced Usage

### Optimal Scheduling Strategy

For 24/7 coverage with 5-hour sessions:

```bash
# Option 1: 4 sessions per day (20 hours coverage)
claude-code-automation schedule 06:00 12:00 18:00 00:00

# Option 2: 5 sessions per day (full coverage + overlap)
claude-code-automation schedule 05:00 10:00 15:00 20:00 01:00
```

### Time Format Support

Both formats are supported:

```bash
# HH:MM format (24-hour)
claude-code-automation schedule 09:30 14:45 21:15

# HHMM format (no colon)
claude-code-automation schedule 0930 1445 2115
```

### Session Monitoring

```bash
# Check if sessions are running
claude-code-automation status

# View LaunchAgent status
launchctl list | grep claude-code-automation

# Check logs
tail -f ~/.config/claude-code-automation/logs/claude-code-automation.log
```

## Common Workflows

### Daily Development Schedule

```bash
# Start session when you begin work
claude-code-automation schedule 09:00

# Lunch break session
claude-code-automation schedule 13:00

# Evening session
claude-code-automation schedule 18:00
```

### Weekend Coverage

```bash
# Minimal weekend coverage
claude-code-automation schedule 10:00 16:00 22:00
```

### High-Usage Schedule

```bash
# Maximum coverage (every 4.5 hours)
claude-code-automation schedule 00:00 05:00 10:00 15:00 20:00
```

## Integration Tips

### Shell Aliases

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
alias cca='claude-code-automation'
alias cca-list='claude-code-automation list'
alias cca-start='claude-code-automation start'
```

### Quick Setup Script

```bash
#!/bin/bash
# quick-setup.sh
echo "Setting up Claude Code automation..."
claude-code-automation clear
claude-code-automation schedule 08:00 14:00 20:00
claude-code-automation list
echo "Setup complete!"
```

## Best Practices

1. **Test First**: Always test with a single schedule before setting multiple times
2. **Monitor Logs**: Check logs regularly for any issues
3. **Overlap Planning**: Consider 30-minute overlaps for critical times
4. **System Time**: Ensure your system clock is accurate
5. **Backup Plans**: Keep manual start option available

## Troubleshooting Quick Reference

```bash
# Service not running?
claude-code-automation status

# Logs showing errors?
tail -20 ~/.config/claude-code-automation/logs/claude-code-automation.log

# Reset everything
claude-code-automation clear
launchctl unload ~/Library/LaunchAgents/com.claude-code-automation.plist
```