#!/usr/bin/env python3
"""
LaunchAgent setup script for Claude Code Automation
Usage: python setup-launchagent.py [time1] [time2] ...
Example: 
  python setup-launchagent.py 09:00 14:00 19:00
  python setup-launchagent.py 0900 1400 1900
"""

import sys
import os
sys.path.insert(0, 'src')

from claude_code_automation.launchagent import LaunchAgentManager

def main():
    if len(sys.argv) < 2:
        # Default schedule: every 5 hours
        schedule_times = ["05:00", "10:00", "15:00", "20:00"]
        print(f"No times specified. Using default schedule: {', '.join(schedule_times)}")
    else:
        schedule_times = sys.argv[1:]
        # Validate time format
        for time_str in schedule_times:
            if ':' in time_str:
                if len(time_str.split(':')) != 2:
                    print(f"Error: Invalid time format '{time_str}'. Use HH:MM or HHMM format.")
                    sys.exit(1)
            elif len(time_str) != 4 or not time_str.isdigit():
                print(f"Error: Invalid time format '{time_str}'. Use HH:MM or HHMM format.")
                sys.exit(1)
    
    print(f"Setting up LaunchAgent with schedule: {', '.join(schedule_times)}")
    
    agent = LaunchAgentManager()
    if agent.install(schedule_times):
        print("✓ LaunchAgent installed successfully")
        print("\nTo manage the service:")
        print("  Check status: launchctl list | grep claude-code-automation")
        print("  View logs: tail -f ~/Library/Logs/claude-code-automation.out.log")
        print("  Uninstall: launchctl unload ~/Library/LaunchAgents/com.claude-code-automation.plist")
    else:
        print("✗ Failed to install LaunchAgent")
        sys.exit(1)

if __name__ == "__main__":
    main()