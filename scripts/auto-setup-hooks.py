#!/usr/bin/env python3
"""Automatically setup Git hooks when project is cloned/installed"""

import os
import sys
import shutil
from pathlib import Path


def is_git_repo():
    """Check if we're in a git repository"""
    return Path('.git').exists()


def setup_git_hooks():
    """Setup Git hooks automatically"""
    if not is_git_repo():
        print("ℹ️  Not in a git repository, skipping Git hooks setup")
        return False
    
    hooks_dir = Path('.git/hooks')
    hooks_dir.mkdir(exist_ok=True)
    
    source_hook = Path('.githooks/pre-commit')
    target_hook = hooks_dir / 'pre-commit'
    
    if not source_hook.exists():
        print("⚠️  Source pre-commit hook not found, skipping setup")
        return False
    
    # Check if hook is already installed
    if target_hook.exists():
        print("✓ Git pre-commit hook already installed")
        return True
    
    try:
        shutil.copy2(source_hook, target_hook)
        target_hook.chmod(0o755)
        print("✅ Git pre-commit hook installed successfully!")
        print("   → Will run local integration tests before each commit")
        return True
    except Exception as e:
        print(f"⚠️  Failed to install Git hook: {e}")
        return False


def main():
    """Main setup function"""
    print("🔧 Auto-setup: Installing development tools...")
    
    # Only auto-install in development environments
    if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
        print("ℹ️  Skipping Git hooks in CI environment")
        return
    
    if '--skip-hooks' in sys.argv:
        print("ℹ️  Skipping Git hooks setup (--skip-hooks flag)")
        return
    
    setup_git_hooks()
    
    print("\n💡 Development environment setup complete!")
    print("   To run local integration tests manually:")
    print("   python -m pytest test/test_local_integration.py -v")


if __name__ == '__main__':
    main()