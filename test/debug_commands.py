#!/usr/bin/env python3
"""Debug CLI commands and structure"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.simple_cli import main, handle_schedule, handle_list

print("Simple CLI functions available:")
print(f"main: {main}")
print(f"handle_schedule: {handle_schedule}")
print(f"handle_list: {handle_list}")

# Test help
sys.argv = ['debug_commands', 'help']
print("\n--- Testing help command ---")
main()