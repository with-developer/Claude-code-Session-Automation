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
    elif command == 'logs':
        handle_logs(sys.argv[2:] if len(sys.argv) > 2 else [])
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
    print("  claude-code-automation logs [type] [lines]           Show logs (app, launch, error)")
    print("  claude-code-automation help                          Show this help")
    print()
    print("Examples:")
    print("  claude-code-automation schedule 14:30 16:00         Schedule at 2:30 PM and 4:00 PM")
    print("  claude-code-automation schedule 1430 1600           Schedule at 2:30 PM and 4:00 PM")
    print("  claude-code-automation logs app 50                  Show last 50 lines of app logs")
    print("  claude-code-automation logs launch                  Show LaunchAgent output logs")
    print("  claude-code-automation logs error                   Show LaunchAgent error logs")


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


def handle_logs(args):
    """Handle logs command"""
    import os
    import subprocess
    from pathlib import Path
    
    # Default values
    log_type = 'app'  # app, launch, error
    lines = 50
    
    # Parse arguments
    if len(args) >= 1:
        log_type = args[0].lower()
    if len(args) >= 2:
        try:
            lines = int(args[1])
        except ValueError:
            print(f"Error: Invalid line count '{args[1]}'")
            sys.exit(1)
    
    # Validate log type
    if log_type not in ['app', 'launch', 'error']:
        print(f"Error: Invalid log type '{log_type}'")
        print("Valid types: app, launch, error")
        sys.exit(1)
    
    # Determine log file path
    if log_type == 'app':
        log_path = Path.home() / ".config/claude-code-automation/logs/claude-code-automation.log"
        log_name = "Application logs"
    elif log_type == 'launch':
        log_path = Path.home() / "Library/Logs/claude-code-automation.out.log"
        log_name = "LaunchAgent output logs"
    else:  # error
        log_path = Path.home() / "Library/Logs/claude-code-automation.err.log"
        log_name = "LaunchAgent error logs"
    
    print(f"📋 {log_name} (last {lines} lines)")
    print("=" * 60)
    
    # Check if log file exists
    if not log_path.exists():
        print(f"⚠️  Log file not found: {log_path}")
        print("   No logs have been created yet or the service hasn't run.")
        return
    
    # Show logs using tail
    try:
        result = subprocess.run(
            ['tail', '-n', str(lines), str(log_path)],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            print(result.stdout)
        else:
            print("📝 Log file is empty")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to read log file: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ 'tail' command not found")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print(f"💡 To follow logs in real-time: tail -f {log_path}")


if __name__ == '__main__':
    main()