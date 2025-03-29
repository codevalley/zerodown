#!/usr/bin/env python3
"""
Static Site Generator - Main Build Script

This script builds a static website from Markdown content files.
It has been refactored to use a modular approach with proper
handling of links and assets.
"""

import os
import sys
import datetime

# Import the builder module
try:
    from ssg.builder import build_site
except ImportError:
    print("ERROR: Could not import the ssg module. Make sure it's in your Python path.")
    sys.exit(1)

# Import configuration
try:
    import config
except ImportError:
    print("ERROR: config.py not found. Ensure it exists in the same directory.")
    sys.exit(1)


def main():
    """Main entry point for the build script."""
    # Build the site
    success = build_site(config)
    
    if not success:
        print("ERROR: Site build failed.")
        sys.exit(1)
    
    # Optionally add post-build actions here
    # For example: deploy to a server, run tests, etc.


if __name__ == "__main__":
    main()
