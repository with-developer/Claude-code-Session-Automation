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


if __name__ == '__main__':
    pytest.main([__file__])