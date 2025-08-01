"""CLI interface for Claude Code Session Automation"""

import click
from .scheduler import ScheduleManager
from .session import SessionManager
from .config import ConfigManager
from .logger import setup_logger


@click.group()
@click.version_option()
def main():
    """Claude Code Session Automation Tool"""
    pass


@main.command()
@click.argument('times', nargs=-1, required=True)
def schedule(times):
    """Schedule Claude Code sessions at specified times (HH:MM format)"""
    setup_logger()
    config = ConfigManager()
    scheduler = ScheduleManager(config)
    
    for time_str in times:
        try:
            scheduler.add_schedule(time_str)
            click.echo(f"✓ Scheduled session at {time_str}")
        except ValueError as e:
            click.echo(f"✗ Error scheduling {time_str}: {e}", err=True)


@main.command()
@click.option('--dry-run', is_flag=True, help='Test mode - simulate session start without running claude-code')
def start(dry_run):
    """Manually start a Claude Code session"""
    setup_logger()
    session_manager = SessionManager()
    
    if dry_run:
        success = session_manager.test_session_start()
        if success:
            click.echo("✓ [DRY RUN] Claude Code session would start successfully")
        else:
            click.echo("✗ [DRY RUN] Claude Code session would fail", err=True)
    else:
        success = session_manager.start_session()
        if success:
            click.echo("✓ Claude Code session started successfully")
        else:
            click.echo("✗ Failed to start Claude Code session", err=True)
            exit(1)


@main.command()
def list():
    """List all scheduled sessions"""
    config = ConfigManager()
    scheduler = ScheduleManager(config)
    schedules = scheduler.list_schedules()
    
    if not schedules:
        click.echo("No scheduled sessions")
        return
    
    click.echo("Scheduled sessions:")
    for schedule in schedules:
        click.echo(f"  - {schedule}")


@main.command()
def clear():
    """Clear all scheduled sessions"""
    config = ConfigManager()
    scheduler = ScheduleManager(config)
    count = scheduler.clear_schedules()
    click.echo(f"✓ Cleared {count} scheduled session(s)")


if __name__ == "__main__":
    main()