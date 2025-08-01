"""Configuration management for Claude Code Automation"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


class ConfigManager:
    """Manages configuration storage and retrieval"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "claude-code-automation"
        self.config_file = self.config_dir / "config.json"
        self.session_dir = self.config_dir / "session"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create configuration and session directories if they don't exist"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_file.exists():
            return {"schedules": []}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise RuntimeError(f"Failed to load config: {e}")
    
    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save config: {e}")
    
    def get_schedules(self) -> List[str]:
        """Get list of scheduled times"""
        config = self.load_config()
        return config.get("schedules", [])
    
    def add_schedule(self, time_str: str):
        """Add a schedule time"""
        config = self.load_config()
        if "schedules" not in config:
            config["schedules"] = []
        
        if time_str not in config["schedules"]:
            config["schedules"].append(time_str)
            self.save_config(config)
    
    def remove_schedule(self, time_str: str):
        """Remove a schedule time"""
        config = self.load_config()
        if "schedules" in config and time_str in config["schedules"]:
            config["schedules"].remove(time_str)
            self.save_config(config)
    
    def clear_schedules(self) -> int:
        """Clear all schedules and return count of cleared items"""
        config = self.load_config()
        count = len(config.get("schedules", []))
        config["schedules"] = []
        self.save_config(config)
        return count
    
    @property
    def session_directory(self) -> Path:
        """Get the session directory path"""
        return self.session_dir