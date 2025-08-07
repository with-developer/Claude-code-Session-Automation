#!/usr/bin/env python3

import sys
sys.path.insert(0, 'src')
from claude_code_automation.new_cli import cli

print("CLI object:", cli)
print("Commands:", cli.commands)
print("Available commands:", list(cli.commands.keys()))

# Try to manually invoke schedule
schedule_cmd = cli.commands.get('schedule')
print("Schedule command:", schedule_cmd)

if schedule_cmd:
    print("Schedule callback:", schedule_cmd.callback)
    print("Schedule params:", schedule_cmd.params)