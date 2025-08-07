#!/usr/bin/env python3
"""Simple CLI interface for Claude Code Session Automation"""

import sys
import platform
from src.session import SessionManager
from src.logger import setup_logger
from src.launchagent import LaunchAgentManager


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'schedule':
        handle_schedule(sys.argv[2:])
    elif command == 'list':
        handle_list()
    elif command == 'clear':
        handle_clear()
    elif command == 'start':
        handle_start()
    elif command == 'status':
        handle_status()
    elif command in ['-h', '--help', 'help']:
        print_help()
    else:
        print(f"Error: Unknown command '{command}'")
        print_help()
        sys.exit(1)


def print_help():
    """Print help message"""
    print("Claude Code Session Automation Tool")
    print()
    print("Usage:")
    print("  claude-code-automation schedule <time1> [time2] ...  Schedule sessions (HH:MM or HHMM)")
    print("  claude-code-automation list                          List scheduled sessions")
    print("  claude-code-automation clear                         Clear all scheduled sessions")
    print("  claude-code-automation start                         Manually start a session")
    print("  claude-code-automation status                        Show current status")
    print("  claude-code-automation help                          Show this help")
    print()
    print("Examples:")
    print("  claude-code-automation schedule 14:30 16:00         Schedule at 2:30 PM and 4:00 PM")
    print("  claude-code-automation schedule 1430 1600           Schedule at 2:30 PM and 4:00 PM")


def handle_schedule(times):
    """Handle schedule command"""
    if not times:
        print("Error: No times specified")
        print("Usage: claude-code-automation schedule <time1> [time2] ...")
        sys.exit(1)
    
    if platform.system() != 'Darwin':
        print("Error: Scheduling is only available on macOS")
        sys.exit(1)
    
    setup_logger()
    agent = LaunchAgentManager()
    
    # Validate time formats
    for time_str in times:
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) != 2 or not all(p.isdigit() for p in parts):
                print(f"Error: Invalid time format '{time_str}'. Use HH:MM or HHMM")
                sys.exit(1)
            hour, minute = int(parts[0]), int(parts[1])
            if not (0 <= hour <= 23) or not (0 <= minute <= 59):
                print(f"Error: Invalid time format '{time_str}'. Use HH:MM or HHMM")
                sys.exit(1)
        elif len(time_str) == 4 and time_str.isdigit():
            hour, minute = int(time_str[:2]), int(time_str[2:])
            if not (0 <= hour <= 23) or not (0 <= minute <= 59):
                print(f"Error: Invalid time format '{time_str}'. Use HH:MM or HHMM")
                sys.exit(1)
        else:
            print(f"Error: Invalid time format '{time_str}'. Use HH:MM or HHMM")
            sys.exit(1)
    
    # Install LaunchAgent
    if agent.install(times):
        print(f"✓ Scheduled sessions at: {', '.join(times)}")
        print("Use 'claude-code-automation list' to view current schedule")
    else:
        print("✗ Failed to schedule sessions")
        sys.exit(1)


def handle_list():
    """Handle list command"""
    if platform.system() != 'Darwin':
        print("Error: This command is only available on macOS")
        sys.exit(1)
    
    agent = LaunchAgentManager()
    status = agent.status()
    
    # Check if plist exists
    if not agent.plist_path.exists():
        print("No sessions scheduled")
        return
    
    # Read plist to get schedule
    try:
        import plistlib
        with open(agent.plist_path, 'rb') as f:
            plist = plistlib.load(f)
        
        intervals = plist.get('StartCalendarInterval', [])
        if not isinstance(intervals, list):
            intervals = [intervals]
        
        print("Scheduled sessions:")
        for interval in intervals:
            hour = interval.get('Hour', 0)
            minute = interval.get('Minute', 0)
            print(f"  - {hour:02d}:{minute:02d}")
        
        print(f"\nService status: {status}")
    except Exception as e:
        print(f"Error reading schedule: {e}")
        sys.exit(1)


def handle_clear():
    """Handle clear command"""
    if platform.system() != 'Darwin':
        print("Error: This command is only available on macOS")
        sys.exit(1)
    
    agent = LaunchAgentManager()
    if agent.uninstall():
        print("✓ Cleared all scheduled sessions")
    else:
        print("✗ Failed to clear sessions")
        sys.exit(1)


def handle_start():
    """Handle start command"""
    setup_logger()
    session_manager = SessionManager()
    
    success = session_manager.start_session()
    if success:
        print("✓ Claude Code session started successfully")
    else:
        print("✗ Failed to start Claude Code session")
        sys.exit(1)


def handle_status():
    """Handle status command"""
    if platform.system() != 'Darwin':
        print("Error: This command is only available on macOS")
        sys.exit(1)
    
    # Show LaunchAgent status
    agent = LaunchAgentManager()
    print(f"Service: {agent.status()}")
    
    # Show current session status
    import os
    from pathlib import Path
    marker_file = Path.home() / ".config/claude-code-automation/session/.claude_session_marker"
    
    if marker_file.exists():
        with open(marker_file, 'r') as f:
            content = f.read()
        print(f"\nCurrent session:")
        print(content)
    else:
        print("\nNo active session")


if __name__ == '__main__':
    main()