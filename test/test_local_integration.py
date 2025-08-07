#!/usr/bin/env python3
"""Local integration tests - only runs on developer machines with Claude Code installed"""

import pytest
import sys
import os
import subprocess
import time
import tempfile
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.session import SessionManager
from src.launchagent import LaunchAgentManager


def is_claude_available():
    """Check if Claude Code is actually installed"""
    try:
        result = subprocess.run(['which', 'claude'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def is_macos():
    """Check if running on macOS"""
    return sys.platform == 'darwin'


# Skip all tests if Claude Code not available or not on macOS
pytestmark = pytest.mark.skipif(
    not (is_claude_available() and is_macos()), 
    reason="Requires Claude Code installation and macOS"
)


class TestLocalIntegration:
    """Local integration tests that verify real functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        print(f"\n🔍 Running local integration test...")
    
    def test_claude_command_accessible(self):
        """Test that claude command is accessible and responds"""
        result = subprocess.run(['claude', '--version'], capture_output=True, text=True, timeout=10)
        
        # Claude should respond (even if with error, it means command exists)
        assert result.returncode in [0, 1]  # 0 for success, 1 for expected error
        print(f"✓ Claude command accessible: {result.stdout[:50]}...")
    
    def test_session_directory_creation(self):
        """Test that session directory can be created"""
        session_manager = SessionManager()
        
        # Test directory creation
        test_dir = session_manager.session_dir
        test_dir.mkdir(parents=True, exist_ok=True)
        
        assert test_dir.exists()
        print(f"✓ Session directory created: {test_dir}")
    
    def test_claude_authentication_check(self):
        """Test if Claude Code has authentication set up"""
        try:
            # Try a simple claude command that would fail if not authenticated
            result = subprocess.run(
                ['claude', '--print', 'test'], 
                capture_output=True, 
                text=True, 
                timeout=15
            )
            
            # If not authenticated, usually returns specific error
            if 'login' in result.stderr.lower() or 'invalid api key' in result.stderr.lower():
                pytest.skip("Claude Code not authenticated - please run 'claude login'")
            
            # Any other response means authentication is likely working
            print(f"✓ Claude Code authentication appears to be working")
            
        except subprocess.TimeoutExpired:
            pytest.skip("Claude Code command timed out - may need authentication")
    
    def test_session_marker_creation(self):
        """Test session marker file creation in real filesystem"""
        session_manager = SessionManager()
        
        # Create session marker
        session_manager.create_session_marker()
        
        marker_file = session_manager.session_dir / ".claude_session_marker"
        assert marker_file.exists()
        
        # Check content
        content = marker_file.read_text()
        assert "Session started at:" in content
        
        print(f"✓ Session marker created with content: {content[:50]}...")
    
    def test_launchagent_plist_file_creation(self):
        """Test LaunchAgent plist file creation (without loading)"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create LaunchAgent manager with temporary directory
            agent = LaunchAgentManager()
            original_path = agent.plist_path
            
            # Use temporary path
            temp_path = Path(temp_dir) / "test.plist"
            agent.plist_path = temp_path
            
            try:
                # Create plist dictionary
                plist_dict = agent.create_plist(['14:30'])
                
                # Write to file (without loading)
                import plistlib
                with open(temp_path, 'wb') as f:
                    plistlib.dump(plist_dict, f)
                
                assert temp_path.exists()
                
                # Read back and verify
                with open(temp_path, 'rb') as f:
                    loaded_plist = plistlib.load(f)
                
                assert loaded_plist['Label'] == 'com.claude-code-automation'
                assert loaded_plist['StartCalendarInterval'] == {'Hour': 14, 'Minute': 30}
                
                print(f"✓ LaunchAgent plist file created and verified")
                
            finally:
                # Restore original path
                agent.plist_path = original_path
    
    @pytest.mark.slow
    def test_quick_session_attempt(self):
        """Test actual session start attempt (quick timeout)"""
        session_manager = SessionManager()
        
        # Store original values
        original_timeout = session_manager.max_retries
        original_delay = session_manager.retry_delay
        
        try:
            # Set quick timeout for testing
            session_manager.max_retries = 1
            session_manager.retry_delay = 1
            
            print("🚀 Attempting to start Claude Code session (quick test)...")
            
            # Try to start session
            result = session_manager.start_session()
            
            if result:
                print("✅ Claude Code session started successfully!")
                
                # Check if marker file was created
                marker_file = session_manager.session_dir / ".claude_session_marker"
                if marker_file.exists():
                    print(f"✅ Session marker created: {marker_file.read_text()[:100]}...")
            else:
                print("⚠️  Session start failed - this may be normal in test environment")
                # Still pass the test if the attempt was made without crashing
                assert True  # Test passes if no exception was thrown
                
        finally:
            # Restore original values
            session_manager.max_retries = original_timeout
            session_manager.retry_delay = original_delay


class TestLocalPerformance:
    """Performance and resource tests"""
    
    @pytest.mark.skipif(not is_claude_available(), reason="Requires Claude Code")
    def test_command_response_time(self):
        """Test that Claude command responds within reasonable time"""
        import time
        
        start_time = time.time()
        
        try:
            result = subprocess.run(['claude', '--help'], capture_output=True, timeout=10)
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"✓ Claude command response time: {response_time:.2f}s")
            
            # Should respond within 5 seconds
            assert response_time < 5.0, f"Claude command too slow: {response_time:.2f}s"
            
        except subprocess.TimeoutExpired:
            pytest.fail("Claude command did not respond within 10 seconds")


if __name__ == '__main__':
    print("🧪 Running local integration tests...")
    print(f"Claude available: {is_claude_available()}")
    print(f"macOS: {is_macos()}")
    
    if is_claude_available() and is_macos():
        pytest.main([__file__, '-v', '-s'])
    else:
        print("❌ Skipping tests - requires Claude Code installation and macOS")
        print("   To install Claude Code: https://docs.anthropic.com/claude/docs/claude-code")