#!/usr/bin/env bash
# Setup script to install git hooks

set -e

echo "🔧 Setting up Git hooks for local integration testing..."

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy our pre-commit hook
cp .githooks/pre-commit .git/hooks/pre-commit

# Make it executable
chmod +x .git/hooks/pre-commit

echo "✅ Git hooks installed successfully!"
echo ""
echo "📋 What this does:"
echo "   • Runs local integration tests before each commit"
echo "   • Verifies Claude Code is accessible and working"
echo "   • Tests actual session management functions"
echo "   • Only runs on macOS with Claude Code installed"
echo ""
echo "🚀 Now every commit will automatically test real functionality!"
echo ""
echo "💡 To test the hook manually:"
echo "   .git/hooks/pre-commit"