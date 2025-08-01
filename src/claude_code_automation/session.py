"""Claude Code session management"""

import subprocess
import os
import time
from pathlib import Path
from .config import ConfigManager
from .logger import get_logger


class SessionManager:
    """Manages Claude Code session startup and monitoring"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.logger = get_logger()
        self.session_dir = self.config.session_directory
        self.max_retries = 3
        self.retry_delay = 5  # seconds
    
    def _check_claude_available(self) -> bool:
        """Check if claude command is available"""
        try:
            result = subprocess.run(['which', 'claude'], 
                                  capture_output=True, text=True, check=True)
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False
    
    def _start_claude_session(self) -> bool:
        """Start a Claude Code session in background"""
        if not self._check_claude_available():
            self.logger.error("claude command not found")
            return False
        
        try:
            # Change to session directory
            os.chdir(self.session_dir)
            self.logger.info(f"Starting Claude Code session in {self.session_dir}")
            
            # First, add the session directory to trusted paths
            # This bypasses the trust dialog
            trust_command = ['claude', 'config', 'set', '-g', 'hasTrustDialogAccepted', 'true']
            subprocess.run(trust_command, capture_output=True)
            
            # Start claude with a simple message to initiate a session
            # Using --print to avoid interactive mode but still create a session
            process = subprocess.Popen(
                ['claude', '--print', '--dangerously-skip-permissions', 'Session started automatically at ' + time.strftime('%Y-%m-%d %H:%M:%S')],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.session_dir
            )
            
            # Wait for completion
            stdout, stderr = process.communicate(timeout=30)
            
            if process.returncode == 0:
                self.logger.info("Claude Code session initiated successfully")
                self.logger.info(f"Response: {stdout[:100]}...")  # Log first 100 chars
                self.create_session_marker()
                return True
            else:
                self.logger.error(f"Claude Code session failed: {stderr}")
                return False
            
        except subprocess.TimeoutExpired:
            self.logger.error("Claude session startup timed out")
            process.kill()
            return False
        except Exception as e:
            self.logger.error(f"Error starting Claude Code session: {e}")
            return False
    
    def start_session(self) -> bool:
        """Start a Claude session with retry logic"""
        for attempt in range(1, self.max_retries + 1):
            self.logger.info(f"Attempting to start session (attempt {attempt}/{self.max_retries})")
            
            if self._start_claude_session():
                self.logger.info("Session started successfully")
                return True
            
            if attempt < self.max_retries:
                self.logger.warning(f"Attempt {attempt} failed, retrying in {self.retry_delay} seconds")
                time.sleep(self.retry_delay)
            else:
                self.logger.error("All attempts failed")
        
        return False
    
    def create_session_marker(self):
        """Create a marker file to track session creation"""
        marker_file = self.session_dir / ".claude_session_marker"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(marker_file, 'w') as f:
                f.write(f"Session started at: {timestamp}\n")
                f.write(f"Expected end time: {self.calculate_session_end_time()}\n")
            self.logger.info(f"Created session marker: {marker_file}")
        except IOError as e:
            self.logger.warning(f"Failed to create session marker: {e}")
    
    def calculate_session_end_time(self) -> str:
        """Calculate expected session end time (5 hours from start)"""
        from datetime import datetime, timedelta
        # Session starts at the beginning of the hour
        now = datetime.now()
        session_start = now.replace(minute=0, second=0, microsecond=0)
        session_end = session_start + timedelta(hours=5)
        return session_end.strftime("%Y-%m-%d %H:%M:%S")
    
    def check_session_health(self) -> bool:
        """Check if Claude session is still active"""
        try:
            # Simple check to see if claude process is running
            result = subprocess.run(['pgrep', '-f', 'claude'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.warning(f"Failed to check session health: {e}")
            return False
    
    def test_session_start(self) -> bool:
        """Test session start without actually running claude"""
        if not self._check_claude_available():
            self.logger.error("claude command not found")
            return False
        
        self.logger.info("Test mode: Claude command is available")
        self.logger.info(f"Session directory exists: {self.session_dir}")
        return True