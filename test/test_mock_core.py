#!/usr/bin/env python3
"""Core Mock tests for essential functionality"""

import pytest
import sys
import subprocess
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.launchagent import LaunchAgentManager
from src.session import SessionManager
from src.simple_cli import main


class TestLaunchAgentCore:
    """Test core LaunchAgent functionality with mocks"""
    
    def setup_method(self):
        """Setup test environment"""
        self.manager = LaunchAgentManager()
    
    def test_create_plist_basic(self):
        """Test basic plist creation"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                stdout='/usr/local/bin/claude-code-automation',
                returncode=0
            )
            
            plist = self.manager.create_plist(['14:30'])
            
            assert plist['Label'] == 'com.claude-code-automation'
            assert plist['StartCalendarInterval'] == {'Hour': 14, 'Minute': 30}
    
    def test_create_plist_multiple_times(self):
        """Test plist creation with multiple times"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                stdout='/usr/local/bin/claude-code-automation',
                returncode=0
            )
            
            plist = self.manager.create_plist(['09:00', '18:30'])
            
            expected = [
                {'Hour': 9, 'Minute': 0},
                {'Hour': 18, 'Minute': 30}
            ]
            assert plist['StartCalendarInterval'] == expected


class TestSessionCore:
    """Test core Session functionality with mocks"""
    
    def setup_method(self):
        """Setup test environment"""
        with patch('src.config.ConfigManager'):
            with patch('src.logger.get_logger'):
                self.manager = SessionManager()
    
    @patch('subprocess.run')
    def test_check_claude_available_found(self, mock_run):
        """Test Claude availability check when found"""
        mock_run.return_value = MagicMock(
            stdout='/usr/local/bin/claude\n',
            returncode=0
        )
        
        result = self.manager._check_claude_available()
        
        assert result is True
        assert self.manager.claude_path == '/usr/local/bin/claude'
    
    @patch('subprocess.run')
    def test_check_claude_available_not_found(self, mock_run):
        """Test Claude availability check when not found"""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'which')
        
        with patch('os.path.exists', return_value=False):
            result = self.manager._check_claude_available()
        
        assert result is False
        assert self.manager.claude_path == 'claude'  # fallback
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('time.strftime', return_value='2024-01-01 14:30:00')
    def test_create_session_marker(self, mock_time, mock_file):
        """Test session marker creation"""
        self.manager.session_dir = Path('/tmp/test')
        
        self.manager.create_session_marker()
        
        mock_file.assert_called()
        # Verify marker content
        written_calls = mock_file().write.call_args_list
        content = ''.join(call[0][0] for call in written_calls)
        assert 'Session started at: 2024-01-01 14:30:00' in content


class TestCLICore:
    """Test core CLI functionality with mocks"""
    
    def test_schedule_basic_success(self, capsys):
        """Test basic schedule command success"""
        
        with patch('platform.system', return_value='Darwin'):
            with patch('src.simple_cli.LaunchAgentManager') as MockManager:
                with patch('src.logger.setup_logger'):
                    mock_manager = MockManager.return_value
                    mock_manager.install.return_value = True
                    
                    with patch('sys.argv', ['claude-code-automation', 'schedule', '14:30']):
                        main()
                    
                    mock_manager.install.assert_called_once_with(['14:30'])
        
        captured = capsys.readouterr()
        assert "✓ Scheduled sessions at: 14:30" in captured.out
    
    def test_schedule_non_macos_error(self, capsys):
        """Test schedule command on non-macOS"""
        
        with patch('platform.system', return_value='Linux'):
            with patch('sys.argv', ['claude-code-automation', 'schedule', '14:30']):
                with pytest.raises(SystemExit) as exc_info:
                    main()
            
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Error: Scheduling is only available on macOS" in captured.out
    
    def test_start_session_success(self, capsys):
        """Test manual session start success"""
        
        with patch('src.simple_cli.SessionManager') as MockSessionManager:
            with patch('src.logger.setup_logger'):
                mock_session = MockSessionManager.return_value
                mock_session.start_session.return_value = True
                
                with patch('sys.argv', ['claude-code-automation', 'start']):
                    main()
                
                mock_session.start_session.assert_called_once()
        
        captured = capsys.readouterr()
        assert "✓ Claude Code session started successfully" in captured.out
    
    def test_logs_app_success(self, capsys, tmp_path):
        """Test logs command for app logs"""
        
        # Create a temporary log file
        log_dir = tmp_path / ".config/claude-code-automation/logs"
        log_dir.mkdir(parents=True)
        log_file = log_dir / "claude-code-automation.log"
        log_file.write_text("2025-08-07 16:50:05 - INFO - Test log entry 1\n2025-08-07 16:51:05 - INFO - Test log entry 2\n")
        
        with patch('pathlib.Path.home', return_value=tmp_path):
            with patch('subprocess.run') as mock_run:
                mock_run.return_value.stdout = "2025-08-07 16:50:05 - INFO - Test log entry 1\n2025-08-07 16:51:05 - INFO - Test log entry 2"
                mock_run.return_value.returncode = 0
                
                with patch('sys.argv', ['claude-code-automation', 'logs', 'app', '50']):
                    main()
                
                mock_run.assert_called_once_with(
                    ['tail', '-n', '50', str(log_file)],
                    capture_output=True,
                    text=True,
                    check=True
                )
        
        captured = capsys.readouterr()
        assert "📋 Application logs (last 50 lines)" in captured.out
        assert "Test log entry" in captured.out
    
    def test_logs_launch_success(self, capsys, tmp_path):
        """Test logs command for LaunchAgent logs"""
        
        # Create a temporary log file
        log_dir = tmp_path / "Library/Logs"
        log_dir.mkdir(parents=True)
        log_file = log_dir / "claude-code-automation.out.log"
        log_file.write_text("✓ Claude Code session started successfully\n")
        
        with patch('pathlib.Path.home', return_value=tmp_path):
            with patch('subprocess.run') as mock_run:
                mock_run.return_value.stdout = "✓ Claude Code session started successfully"
                mock_run.return_value.returncode = 0
                
                with patch('sys.argv', ['claude-code-automation', 'logs', 'launch']):
                    main()
                
                mock_run.assert_called_once_with(
                    ['tail', '-n', '50', str(log_file)],
                    capture_output=True,
                    text=True,
                    check=True
                )
        
        captured = capsys.readouterr()
        assert "📋 LaunchAgent output logs (last 50 lines)" in captured.out
        assert "Claude Code session started successfully" in captured.out
    
    def test_logs_missing_file(self, capsys, tmp_path):
        """Test logs command when log file doesn't exist"""
        
        with patch('pathlib.Path.home', return_value=tmp_path):
            with patch('sys.argv', ['claude-code-automation', 'logs', 'app']):
                main()
        
        captured = capsys.readouterr()
        assert "⚠️  Log file not found:" in captured.out
        assert "No logs have been created yet" in captured.out
    
    def test_logs_invalid_type(self, capsys):
        """Test logs command with invalid log type"""
        
        with patch('sys.argv', ['claude-code-automation', 'logs', 'invalid']):
            with pytest.raises(SystemExit) as exc_info:
                main()
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Invalid log type 'invalid'" in captured.out
        assert "Valid types: app, launch, error" in captured.out
    
    def test_logs_invalid_line_count(self, capsys):
        """Test logs command with invalid line count"""
        
        with patch('sys.argv', ['claude-code-automation', 'logs', 'app', 'not_a_number']):
            with pytest.raises(SystemExit) as exc_info:
                main()
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Invalid line count 'not_a_number'" in captured.out
    
    def test_logs_empty_file(self, capsys, tmp_path):
        """Test logs command with empty log file"""
        
        # Create empty log file
        log_dir = tmp_path / ".config/claude-code-automation/logs"
        log_dir.mkdir(parents=True)
        log_file = log_dir / "claude-code-automation.log"
        log_file.write_text("")
        
        with patch('pathlib.Path.home', return_value=tmp_path):
            with patch('subprocess.run') as mock_run:
                mock_run.return_value.stdout = ""
                mock_run.return_value.returncode = 0
                
                with patch('sys.argv', ['claude-code-automation', 'logs', 'app']):
                    main()
        
        captured = capsys.readouterr()
        assert "📝 Log file is empty" in captured.out


if __name__ == '__main__':
    pytest.main([__file__])