"""Cron schedule management for Claude Code sessions"""

import re
import subprocess
from typing import List
from crontab import CronTab
from croniter import croniter
from datetime import datetime
from .config import ConfigManager
from .logger import get_logger


class ScheduleManager:
    """Manages cron schedules for Claude Code sessions"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.logger = get_logger()
        self.cron = CronTab(user=True)
        self.script_comment = "claude-code-automation"
    
    def _validate_time_format(self, time_str: str) -> bool:
        """Validate time format (HH:MM)"""
        pattern = r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$'
        return bool(re.match(pattern, time_str))
    
    def _time_to_cron(self, time_str: str) -> str:
        """Convert HH:MM to cron format"""
        if not self._validate_time_format(time_str):
            raise ValueError(f"Invalid time format: {time_str}. Use HH:MM format.")
        
        hour, minute = time_str.split(':')
        return f"{minute} {hour} * * *"
    
    def _get_script_path(self) -> str:
        """Get the path to the automation script"""
        try:
            result = subprocess.run(['which', 'claude-code-automation'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "claude-code-automation"
    
    def add_schedule(self, time_str: str):
        """Add a new schedule"""
        if not self._validate_time_format(time_str):
            raise ValueError(f"Invalid time format: {time_str}. Use HH:MM format.")
        
        cron_time = self._time_to_cron(time_str)
        script_path = self._get_script_path()
        # Use wrapper script for better environment handling
        import os
        wrapper_path = os.path.join(os.path.dirname(__file__), 'wrapper.sh')
        command = f"{wrapper_path} {script_path} start"
        
        # Check if schedule already exists
        existing_jobs = list(self.cron.find_comment(self.script_comment))
        for job in existing_jobs:
            if str(job) == f"{cron_time} {command}":
                self.logger.info(f"Schedule for {time_str} already exists")
                return
        
        # Add new job
        job = self.cron.new(command=command, comment=self.script_comment)
        job.setall(cron_time)
        
        if job.is_valid():
            self.cron.write()
            self.config.add_schedule(time_str)
            self.logger.info(f"Added schedule for {time_str}")
        else:
            raise RuntimeError(f"Invalid cron job: {cron_time} {command}")
    
    def remove_schedule(self, time_str: str):
        """Remove a schedule"""
        if not self._validate_time_format(time_str):
            raise ValueError(f"Invalid time format: {time_str}")
        
        cron_time = self._time_to_cron(time_str)
        script_path = self._get_script_path()
        command = f"{script_path} start"
        
        # Find and remove matching jobs
        jobs_to_remove = []
        for job in self.cron.find_comment(self.script_comment):
            if str(job) == f"{cron_time} {command}":
                jobs_to_remove.append(job)
        
        for job in jobs_to_remove:
            self.cron.remove(job)
        
        if jobs_to_remove:
            self.cron.write()
            self.config.remove_schedule(time_str)
            self.logger.info(f"Removed schedule for {time_str}")
    
    def list_schedules(self) -> List[str]:
        """List all scheduled times"""
        return self.config.get_schedules()
    
    def clear_schedules(self) -> int:
        """Clear all schedules"""
        # Remove all cron jobs with our comment
        jobs_to_remove = list(self.cron.find_comment(self.script_comment))
        for job in jobs_to_remove:
            self.cron.remove(job)
        
        if jobs_to_remove:
            self.cron.write()
        
        count = self.config.clear_schedules()
        self.logger.info(f"Cleared {count} schedules")
        return count
    
    def get_next_run_time(self, time_str: str) -> datetime:
        """Get the next run time for a given schedule"""
        if not self._validate_time_format(time_str):
            raise ValueError(f"Invalid time format: {time_str}")
        
        cron_time = self._time_to_cron(time_str)
        cron = croniter(cron_time, datetime.now())
        return cron.get_next(datetime)