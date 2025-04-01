#!/usr/bin/env python3
"""
Simple script to run Zerodown without installing it.

This script can be run in two modes:
1. Command mode: python run_zerodown.py [command] [options]
2. Interactive shell mode: python run_zerodown.py
"""

import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to import zerodown
sys.path.insert(0, str(Path(__file__).parent))

from zerodown.config import load_config
from zerodown.builder import build_site
from zerodown.cli import main as cli_main
from zerodown.shell import main as shell_main

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command mode - pass to CLI for consistent behavior
        cli_main()
    else:
        # Interactive shell mode
        shell_main()
