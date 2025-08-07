#!/bin/bash
# Wrapper script for running claude-code-automation from cron

# Load user environment
source ~/.zshrc || source ~/.bashrc || true

# Ensure proper PATH
export PATH="/Users/weakness/.nvm/versions/node/v20.19.4/bin:$PATH"

# Set HOME and USER
export HOME="/Users/weakness"
export USER="weakness"

# Use osascript to run in user context with keychain access
osascript -e "do shell script \"$@\""