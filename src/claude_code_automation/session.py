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
        """Start a Claude Code interactive session"""
        if not self._check_claude_available():
            self.logger.error("claude command not found")
            return False
        
        try:
            # Change to session directory
            os.chdir(self.session_dir)
            self.logger.info(f"Starting Claude Code session in {self.session_dir}")
            
            # Start claude in interactive mode with a simple initial message
            # This will open a new terminal window with Claude Code running
            if os.name == 'posix':  # macOS/Linux
                # Use osascript on macOS to open new terminal with claude
                if os.uname().sysname == 'Darwin':  # macOS
                    script = f'''
                    tell application "Terminal"
                        do script "cd {self.session_dir} && claude"
                        activate
                    end tell
                    '''
                    process = subprocess.run(['osascript', '-e', script], 
                                          capture_output=True, text=True)
                else:  # Linux
                    # Try common terminal emulators
                    terminals = ['gnome-terminal', 'xterm', 'konsole', 'terminator']
                    for term in terminals:
                        try:
                            subprocess.Popen([term, '-e', f'cd {self.session_dir} && claude'])
                            break
                        except FileNotFoundError:
                            continue
            
            # Mark session as started
            self.create_session_marker()
            self.logger.info("Claude Code interactive session started")
            return True
            
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
            self.logger.info(f"Created session marker: {marker_file}")
        except IOError as e:
            self.logger.warning(f"Failed to create session marker: {e}")
    
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