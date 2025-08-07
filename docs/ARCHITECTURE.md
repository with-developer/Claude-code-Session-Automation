# Architecture Overview

This document explains the technical architecture of Claude Code Session Automation.

## System Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│                     │    │                     │    │                     │
│   CLI Interface     │    │   LaunchAgent       │    │   Claude Code       │
│   (simple_cli.py)   │    │   (macOS Service)   │    │   (External Tool)   │
│                     │    │                     │    │                     │
└─────────┬───────────┘    └─────────┬───────────┘    └─────────┬───────────┘
          │                          │                          │
          │ Commands                 │ Scheduled                │ Session
          │                          │ Execution                │ Management
          │                          │                          │
          ▼                          ▼                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        Session Management Layer                            │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │  LaunchAgent    │  │  Session        │  │  Config         │            │
│  │  Manager        │  │  Manager        │  │  Manager        │            │
│  │                 │  │                 │  │                 │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        File System & Storage                               │
│                                                                             │
│  ~/.config/claude-code-automation/                                         │
│  ├── session/           # Claude Code session directory                    │
│  ├── logs/              # Application logs                                 │
│  └── config.json        # Configuration file                              │
│                                                                             │
│  ~/Library/LaunchAgents/                                                   │
│  └── com.claude-code-automation.plist  # macOS LaunchAgent config         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. CLI Interface (`src/simple_cli.py`)

- **Purpose**: User-facing command-line interface
- **Responsibilities**:
  - Parse user commands and arguments
  - Validate input (time formats, platform compatibility)
  - Coordinate with other components
  - Display results and errors

**Key Functions**:
```python
def main()                    # Entry point, command routing
def handle_schedule(times)    # Schedule management
def handle_list()            # Display current schedules
def handle_clear()           # Remove all schedules
```

### 2. LaunchAgent Manager (`src/launchagent.py`)

- **Purpose**: macOS LaunchAgent integration
- **Responsibilities**:
  - Create and manage LaunchAgent plist files
  - Install/uninstall system services
  - Monitor service status
  - Handle service lifecycle

**Key Methods**:
```python
def install(schedule_times)   # Create and load LaunchAgent
def uninstall()              # Remove LaunchAgent
def status()                 # Check service status
```

### 3. Session Manager (`src/session.py`)

- **Purpose**: Claude Code session management
- **Responsibilities**:
  - Start Claude Code sessions
  - Manage session directories
  - Handle authentication
  - Monitor session health

**Key Methods**:
```python
def start_session()          # Launch new Claude Code session
def check_session_status()   # Monitor existing sessions
```

### 4. Configuration Manager (`src/config.py`)

- **Purpose**: Application configuration
- **Responsibilities**:
  - Store application settings
  - Manage file paths
  - Handle configuration persistence

## Data Flow

### 1. Schedule Creation Flow

```
User Command → CLI Parser → Time Validation → LaunchAgent Creation → System Integration
```

1. User runs `claude-code-automation schedule 14:30`
2. CLI parses command and validates time format
3. LaunchAgentManager creates plist configuration
4. macOS LaunchAgent service is loaded
5. Confirmation returned to user

### 2. Scheduled Execution Flow

```
macOS LaunchAgent → Session Manager → Claude Code → Session Creation
```

1. macOS triggers LaunchAgent at scheduled time
2. SessionManager.start_session() is called
3. New Claude Code session is started in dedicated directory
4. Session status is logged

## Security Considerations

### Authentication
- Uses macOS Keychain for Claude Code authentication
- No credentials stored in application files
- LaunchAgent runs in user session context

### File Permissions
- Application files stored in user directory (`~/.config/`)
- LaunchAgent plist has user-only permissions
- Log files protected by standard Unix permissions

### Process Isolation
- Each Claude Code session runs in isolated directory
- No shared state between sessions
- Clean environment for each execution

## Error Handling

### Failure Points and Recovery

1. **LaunchAgent Creation Failure**
   - Validation: Check plist syntax
   - Recovery: Recreate with corrected parameters

2. **Session Start Failure**
   - Detection: Exit code monitoring
   - Recovery: Retry mechanism with exponential backoff

3. **Authentication Failure**
   - Detection: Claude Code error messages
   - Recovery: User notification for re-authentication

## Scalability and Performance

### Resource Usage
- **Memory**: Minimal (< 10MB per session)
- **CPU**: Low impact (occasional scheduled tasks)
- **Disk**: Small (logs and config files < 1MB)

### Limits
- **Concurrent Sessions**: 1 per schedule (by design)
- **Schedule Count**: Unlimited (practical limit ~20)
- **Log Retention**: Configurable (default: 7 days)

## Future Architecture Considerations

### Potential Enhancements
1. **GUI Interface**: Native macOS menu bar app
2. **Multi-Platform**: Windows Task Scheduler support
3. **Remote Management**: Web interface for multiple machines
4. **Advanced Scheduling**: Cron-like expressions
5. **Session Analytics**: Usage tracking and optimization