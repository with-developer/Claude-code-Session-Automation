# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Claude Code Session Automation
- Unified CLI interface for session scheduling
- LaunchAgent integration for macOS
- Support for both HH:MM and HHMM time formats
- Automatic keychain authentication
- Comprehensive logging and error handling

### Features
- `claude-code-automation schedule` - Schedule sessions at specific times
- `claude-code-automation list` - View current schedule
- `claude-code-automation clear` - Remove all schedules
- `claude-code-automation start` - Manually start a session
- `claude-code-automation status` - Check service status
- `claude-code-automation help` - Show usage information

### Technical
- Clean project structure with `src/` organization
- Zero external dependencies (uses only Python stdlib)
- Comprehensive test suite
- Homebrew formula for easy installation
- Full documentation and examples

## [0.1.0] - 2024-XX-XX

### Added
- Initial project structure
- Core session management functionality
- LaunchAgent scheduling system
- CLI interface implementation