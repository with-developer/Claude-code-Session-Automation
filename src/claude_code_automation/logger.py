"""Logging configuration for Claude Code Automation"""

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = "claude-code-automation", level: int = logging.INFO) -> logging.Logger:
    """Set up the logger with file and console handlers"""
    
    # Create logs directory
    log_dir = Path.home() / ".config" / "claude-code-automation" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    log_file = log_dir / "claude-code-automation.log"
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1024*1024, backupCount=5  # 1MB per file, keep 5 backups
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Console handler (only for errors and warnings)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = "claude-code-automation") -> logging.Logger:
    """Get the configured logger"""
    return logging.getLogger(name)