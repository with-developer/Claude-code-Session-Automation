#!/bin/sh
# Wrapper script for running claude-code-automation from cron
# Uses /bin/sh for maximum compatibility

# Detect user's default shell and load appropriate config
if [ -n "$SHELL" ]; then
    case "$SHELL" in
        */zsh)
            [ -f "$HOME/.zshrc" ] && . "$HOME/.zshrc"
            ;;
        */bash)
            [ -f "$HOME/.bashrc" ] && . "$HOME/.bashrc"
            [ -f "$HOME/.bash_profile" ] && . "$HOME/.bash_profile"
            ;;
        */fish)
            # Fish has different syntax, skip for now
            ;;
    esac
fi

# Ensure HOME and USER are set
[ -z "$HOME" ] && export HOME="$(eval echo ~$(whoami))"
[ -z "$USER" ] && export USER="$(whoami)"

# Try to find node in common locations
for dir in /usr/local/bin /opt/homebrew/bin "$HOME/.local/bin"; do
    [ -d "$dir" ] && export PATH="$dir:$PATH"
done

# Check for NVM
if [ -z "$NVM_DIR" ]; then
    [ -d "$HOME/.nvm" ] && export NVM_DIR="$HOME/.nvm"
fi

# Add NVM paths if available
if [ -d "$NVM_DIR/versions/node" ]; then
    for version in "$NVM_DIR/versions/node"/*; do
        [ -d "$version/bin" ] && export PATH="$version/bin:$PATH"
    done
fi

# Run the actual command
exec "$@"