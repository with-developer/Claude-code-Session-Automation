"""CLI interface for Claude Code Session Automation"""

import click
from .session import SessionManager
from .logger import setup_logger


@click.group()
@click.version_option()
def main():
    """Claude Code Session Automation Tool"""
    pass


@main.command()
@click.argument('times', nargs=-1, required=True)
def schedule(times):
    """[Deprecated] Use 'setup' command instead for macOS LaunchAgent"""
    click.echo("Warning: 'schedule' command is deprecated. Use 'setup' command instead.")
    click.echo("Example: claude-code-automation setup -t 09:00 -t 14:00")


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
    """[Deprecated] Use 'service status' command instead"""
    click.echo("Warning: 'list' command is deprecated.")
    click.echo("Use: claude-code-automation service status")


@main.command()
def clear():
    """[Deprecated] Use 'service uninstall' command instead"""
    click.echo("Warning: 'clear' command is deprecated.")
    click.echo("Use: claude-code-automation service uninstall")


@main.command()
@click.option('--times', '-t', multiple=True, help='Schedule times in HH:MM format')
@click.option('--interval', '-i', type=int, help='Run every N hours')
def setup(times, interval):
    """Setup LaunchAgent with schedules (macOS only)"""
    import platform
    if platform.system() != 'Darwin':
        click.echo("Error: LaunchAgent is only available on macOS", err=True)
        return
    
    # Generate schedule times
    schedule_times = []
    if interval:
        # Generate times based on interval
        for hour in range(0, 24, interval):
            schedule_times.append(f"{hour:02d}:00")
    elif times:
        schedule_times = list(times)
    else:
        # Default schedule: every 5 hours starting at 5 AM
        schedule_times = ["05:00", "10:00", "15:00", "20:00"]
    
    # Create LaunchAgent
    from .launchagent import LaunchAgentManager
    agent = LaunchAgentManager()
    if agent.install(schedule_times):
        click.echo(f"✓ LaunchAgent installed with schedule: {', '.join(schedule_times)}")
        click.echo("\nTo manage the service:")
        click.echo("  Status:  claude-code-automation service status")
        click.echo("  Stop:    claude-code-automation service stop")
        click.echo("  Start:   claude-code-automation service start")
    else:
        click.echo("✗ Failed to install LaunchAgent", err=True)


@main.group()
def service():
    """Manage LaunchAgent service (macOS only)"""
    pass


@service.command('start')
def service_start():
    """Start the LaunchAgent service"""
    from .launchagent import LaunchAgentManager
    agent = LaunchAgentManager()
    if agent.start():
        click.echo("✓ Service started")
    else:
        click.echo("✗ Failed to start service", err=True)


@service.command('stop')
def service_stop():
    """Stop the LaunchAgent service"""
    from .launchagent import LaunchAgentManager
    agent = LaunchAgentManager()
    if agent.stop():
        click.echo("✓ Service stopped")
    else:
        click.echo("✗ Failed to stop service", err=True)


@service.command('status')
def service_status():
    """Check LaunchAgent service status"""
    from .launchagent import LaunchAgentManager
    agent = LaunchAgentManager()
    status = agent.status()
    click.echo(status)


@service.command('uninstall')
def service_uninstall():
    """Uninstall the LaunchAgent service"""
    from .launchagent import LaunchAgentManager
    agent = LaunchAgentManager()
    if agent.uninstall():
        click.echo("✓ Service uninstalled")
    else:
        click.echo("✗ Failed to uninstall service", err=True)


if __name__ == "__main__":
    main()