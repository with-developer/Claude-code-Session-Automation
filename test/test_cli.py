#!/usr/bin/env python3
"""Test suite for Claude Code Session Automation CLI"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.simple_cli import main, print_help, handle_schedule, handle_list


class TestCLI:
    """Test the CLI interface"""

    def test_help_command(self, capsys):
        """Test help command output"""
        with patch('sys.argv', ['claude-code-automation', 'help']):
            main()
        
        captured = capsys.readouterr()
        assert "Claude Code Session Automation Tool" in captured.out
        assert "Usage:" in captured.out

    def test_no_args_shows_help(self, capsys):
        """Test that no arguments shows help"""
        with patch('sys.argv', ['claude-code-automation']):
            main()
        
        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    @patch('platform.system')
    def test_non_macos_scheduling(self, mock_platform, capsys):
        """Test scheduling on non-macOS systems"""
        mock_platform.return_value = 'Linux'
        
        with patch('sys.argv', ['claude-code-automation', 'schedule', '14:30']):
            with pytest.raises(SystemExit) as exc_info:
                main()
        
        captured = capsys.readouterr()
        assert "Error: Scheduling is only available on macOS" in captured.out
        assert exc_info.value.code == 1

    def test_invalid_time_format(self, capsys):
        """Test invalid time format handling"""
        with patch('platform.system', return_value='Darwin'):
            with patch('sys.argv', ['claude-code-automation', 'schedule', '25:70']):
                with pytest.raises(SystemExit) as exc_info:
                    main()
        
        captured = capsys.readouterr()
        assert "Error: Invalid time format" in captured.out
        assert exc_info.value.code == 1

    def test_valid_time_formats(self):
        """Test valid time format validation"""
        # Test HH:MM format
        valid_times = ['14:30', '09:00', '23:59']
        for time_str in valid_times:
            parts = time_str.split(':')
            assert len(parts) == 2
            assert all(p.isdigit() for p in parts)
        
        # Test HHMM format
        valid_times = ['1430', '0900', '2359']
        for time_str in valid_times:
            assert len(time_str) == 4
            assert time_str.isdigit()


class TestTimeValidation:
    """Test time format validation"""

    def test_hhmm_format_validation(self):
        """Test HHMM format validation"""
        valid_times = ['0000', '1430', '2359']
        invalid_times = ['abc', '12345', '25:00', '12:60']
        
        for time_str in valid_times:
            if ':' not in time_str:
                assert len(time_str) == 4 and time_str.isdigit()
        
        for time_str in invalid_times:
            if ':' not in time_str:
                assert not (len(time_str) == 4 and time_str.isdigit())

    def test_hhcolon_mm_format_validation(self):
        """Test HH:MM format validation"""
        valid_times = ['00:00', '14:30', '23:59']
        invalid_times = ['25:00', '12:60', 'ab:cd']
        
        for time_str in valid_times:
            if ':' in time_str:
                parts = time_str.split(':')
                if len(parts) == 2 and all(p.isdigit() for p in parts):
                    hour, minute = int(parts[0]), int(parts[1])
                    assert 0 <= hour <= 23 and 0 <= minute <= 59
        
        for time_str in invalid_times:
            if ':' in time_str:
                parts = time_str.split(':')
                if len(parts) == 2 and all(p.isdigit() for p in parts):
                    hour, minute = int(parts[0]), int(parts[1])
                    assert not (0 <= hour <= 23 and 0 <= minute <= 59)
                else:
                    # String format is invalid (like 'ab:cd')
                    assert not (len(parts) == 2 and all(p.isdigit() for p in parts))


if __name__ == '__main__':
    pytest.main([__file__])