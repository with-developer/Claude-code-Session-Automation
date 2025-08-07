#!/usr/bin/env python3
"""Manual test for CLI functionality"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.simple_cli import main

# Manually set argv and test
sys.argv = ['manual_test', 'schedule', '14:30']
main()