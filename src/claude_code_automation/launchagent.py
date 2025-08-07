"""LaunchAgent management for macOS"""

import os
import subprocess
import plistlib
from pathlib import Path
from typing import List, Optional
from .logger import get_logger


class LaunchAgentManager:
    """Manages LaunchAgent for Claude Code automation on macOS"""
    
    def __init__(self):
        self.logger = get_logger()
        self.label = "com.claude-code-automation"
        self.plist_filename = f"{self.label}.plist"
        self.launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
        self.plist_path = self.launch_agents_dir / self.plist_filename
        
    def create_plist(self, schedule_times: List[str]) -> dict:
        """Create plist configuration"""
        # Convert HH:MM or HHMM to hour and minute integers
        intervals = []
        for time_str in schedule_times:
            if ':' in time_str:
                hour, minute = map(int, time_str.split(':'))
            else:
                # Handle HHMM format
                if len(time_str) == 4:
                    hour = int(time_str[:2])
                    minute = int(time_str[2:])
                else:
                    raise ValueError(f"Invalid time format: {time_str}")
            intervals.append({
                'Hour': hour,
                'Minute': minute
            })
        
        # Get claude-code-automation path
        try:
            result = subprocess.run(['which', 'claude-code-automation'], 
                                  capture_output=True, text=True, check=True)
            program_path = result.stdout.strip()
        except subprocess.CalledProcessError:
            # Fallback to expected Homebrew location
            program_path = "/usr/local/bin/claude-code-automation"
        
        plist_dict = {
            'Label': self.label,
            'ProgramArguments': [program_path, 'start'],
            'StartCalendarInterval': intervals if len(intervals) > 1 else intervals[0],
            'StandardOutPath': str(Path.home() / "Library/Logs/claude-code-automation.out.log"),
            'StandardErrorPath': str(Path.home() / "Library/Logs/claude-code-automation.err.log"),
            'EnvironmentVariables': {
                'PATH': '/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin'
            }
        }
        
        return plist_dict
    
    def install(self, schedule_times: List[str]) -> bool:
        """Install LaunchAgent with given schedule"""
        try:
            # Ensure LaunchAgents directory exists
            self.launch_agents_dir.mkdir(parents=True, exist_ok=True)
            
            # Create plist
            plist_dict = self.create_plist(schedule_times)
            
            # Write plist file
            with open(self.plist_path, 'wb') as f:
                plistlib.dump(plist_dict, f)
            
            # Load the agent
            self.load()
            
            self.logger.info(f"LaunchAgent installed at {self.plist_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to install LaunchAgent: {e}")
            return False
    
    def uninstall(self) -> bool:
        """Uninstall LaunchAgent"""
        try:
            # Unload first
            self.unload()
            
            # Remove plist file
            if self.plist_path.exists():
                self.plist_path.unlink()
            
            self.logger.info("LaunchAgent uninstalled")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to uninstall LaunchAgent: {e}")
            return False
    
    def load(self) -> bool:
        """Load LaunchAgent"""
        try:
            subprocess.run(['launchctl', 'load', str(self.plist_path)], 
                         check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def unload(self) -> bool:
        """Unload LaunchAgent"""
        try:
            subprocess.run(['launchctl', 'unload', str(self.plist_path)], 
                         check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def start(self) -> bool:
        """Start the service"""
        return self.load()
    
    def stop(self) -> bool:
        """Stop the service"""
        return self.unload()
    
    def status(self) -> str:
        """Get service status"""
        try:
            result = subprocess.run(['launchctl', 'list'], 
                                  capture_output=True, text=True, check=True)
            if self.label in result.stdout:
                # Parse the status
                for line in result.stdout.splitlines():
                    if self.label in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            pid = parts[0]
                            status = parts[1]
                            if pid != '-':
                                return f"✓ Service is running (PID: {pid})"
                            else:
                                return f"✗ Service is loaded but not running (status: {status})"
                return "✓ Service is loaded"
            else:
                if self.plist_path.exists():
                    return "✗ Service is not loaded (plist exists)"
                else:
                    return "✗ Service is not installed"
        except subprocess.CalledProcessError:
            return "✗ Unable to check service status"