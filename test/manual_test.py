#!/usr/bin/env python3

# Bypass the entry point and import directly
import sys
sys.path.insert(0, 'src')
from claude_code_automation.new_cli import cli

# Manually set argv and test
sys.argv = ['manual_test', 'schedule', '14:30']
cli()