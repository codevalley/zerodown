#!/usr/bin/env python3
"""
Simple script to run Zerodown without installing it.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to import zerodown
sys.path.insert(0, str(Path(__file__).parent))

from zerodown.config import load_config
from zerodown.builder import build_site
from zerodown.cli import main as cli_main

if __name__ == "__main__":
    # Always use the CLI for consistent behavior
    cli_main()
