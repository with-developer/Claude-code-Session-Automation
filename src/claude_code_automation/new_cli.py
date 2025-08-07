#!/usr/bin/env python3
"""CLI interface for Claude Code Session Automation"""

import click
import platform
from .session import SessionManager
from .logger import setup_logger
from .launchagent import LaunchAgentManager


@click.group()
@click.version_option()
def cli():
    """Claude Code Session Automation Tool"""
    pass


@cli.command()
@click.argument('times', nargs=-1, required=True)
def schedule(times):
    """Schedule Claude Code sessions at specified times (HH:MM or HHMM format)"""
    if platform.system() != 'Darwin':
        click.echo("Error: Scheduling is only available on macOS", err=True)
        return
    
    setup_logger()
    agent = LaunchAgentManager()
    
    # Convert times to list
    schedule_times = list(times)
    
    # Validate time formats
    for time_str in schedule_times:
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) != 2 or not all(p.isdigit() for p in parts):
                click.echo(f"Error: Invalid time format '{time_str}'. Use HH:MM or HHMM", err=True)
                return
        elif not (len(time_str) == 4 and time_str.isdigit()):
            click.echo(f"Error: Invalid time format '{time_str}'. Use HH:MM or HHMM", err=True)
            return
    
    # Install LaunchAgent
    if agent.install(schedule_times):
        click.echo(f"✓ Scheduled sessions at: {', '.join(schedule_times)}")
        click.echo("Use 'claude-code-automation list' to view current schedule")
    else:
        click.echo("✗ Failed to schedule sessions", err=True)


@cli.command()
def list():
    """List scheduled sessions"""
    if platform.system() != 'Darwin':
        click.echo("Error: This command is only available on macOS", err=True)
        return
    
    agent = LaunchAgentManager()
    status = agent.status()
    
    # Check if plist exists
    if not agent.plist_path.exists():
        click.echo("No sessions scheduled")
        return
    
    # Read plist to get schedule
    try:
        import plistlib
        with open(agent.plist_path, 'rb') as f:
            plist = plistlib.load(f)
        
        intervals = plist.get('StartCalendarInterval', [])
        if not isinstance(intervals, list):
            intervals = [intervals]
        
        click.echo("Scheduled sessions:")
        for interval in intervals:
            hour = interval.get('Hour', 0)
            minute = interval.get('Minute', 0)
            click.echo(f"  - {hour:02d}:{minute:02d}")
        
        click.echo(f"\nService status: {status}")
    except Exception as e:
        click.echo(f"Error reading schedule: {e}", err=True)


if __name__ == '__main__':
    cli()