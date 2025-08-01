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
    
    def _check_claude_code_available(self) -> bool:
        """Check if claude-code command is available"""
        try:
            result = subprocess.run(['which', 'claude-code'], 
                                  capture_output=True, text=True, check=True)
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False
    
    def _start_claude_code_session(self) -> bool:
        """Start a Claude Code session in the session directory"""
        if not self._check_claude_code_available():
            self.logger.error("claude-code command not found")
            return False
        
        try:
            # Change to session directory
            os.chdir(self.session_dir)
            self.logger.info(f"Starting Claude Code session in {self.session_dir}")
            
            # Start claude-code with a simple greeting to initiate the session
            process = subprocess.Popen(
                ['claude-code'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.session_dir
            )
            
            # Send initial message to start the session
            initial_message = "Hello! Starting automated session."
            stdout, stderr = process.communicate(input=initial_message, timeout=30)
            
            if process.returncode == 0:
                self.logger.info("Claude Code session started successfully")
                return True
            else:
                self.logger.error(f"Claude Code session failed: {stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Claude Code session startup timed out")
            process.kill()
            return False
        except Exception as e:
            self.logger.error(f"Error starting Claude Code session: {e}")
            return False
    
    def start_session(self) -> bool:
        """Start a Claude Code session with retry logic"""
        for attempt in range(1, self.max_retries + 1):
            self.logger.info(f"Attempting to start session (attempt {attempt}/{self.max_retries})")
            
            if self._start_claude_code_session():
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
            self.logger.info(f"Created session marker: {marker_file}")
        except IOError as e:
            self.logger.warning(f"Failed to create session marker: {e}")
    
    def check_session_health(self) -> bool:
        """Check if Claude Code session is still active"""
        try:
            # Simple check to see if claude-code process is running
            result = subprocess.run(['pgrep', '-f', 'claude-code'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.warning(f"Failed to check session health: {e}")
            return False