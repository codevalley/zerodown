"""
Configuration handling for Zerodown static site generator.
"""

import os
import sys
from importlib.util import spec_from_file_location, module_from_spec


def load_config(config_path):
    """
    Load configuration from a Python file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        config: Configuration module
    """
    if not os.path.exists(config_path):
        print(f"ERROR: Configuration file not found: {config_path}")
        sys.exit(1)
        
    try:
        # Load the config file as a module
        spec = spec_from_file_location("config", config_path)
        config = module_from_spec(spec)
        spec.loader.exec_module(config)
        
        # Validate required configuration
        _validate_config(config)
        
        return config
    except Exception as e:
        print(f"ERROR: Failed to load configuration: {e}")
        sys.exit(1)


def _validate_config(config):
    """
    Validate that the configuration has all required attributes.
    
    Args:
        config: Configuration module to validate
    """
    required_attrs = [
        'SITE_NAME',
        'SITE_DESCRIPTION',
        'CONTENT_DIR',
        'TEMPLATE_DIR',
        'OUTPUT_DIR',
        'STATIC_DIR',
        'STYLES_DIR',
        'SECTIONS'
    ]
    
    missing = [attr for attr in required_attrs if not hasattr(config, attr)]
    
    if missing:
        print(f"ERROR: Missing required configuration attributes: {', '.join(missing)}")
        sys.exit(1)
        
    # Set default values for optional attributes
    if not hasattr(config, 'SITE_AUTHOR'):
        config.SITE_AUTHOR = config.SITE_NAME
        
    if not hasattr(config, 'THEME_CSS_FILE'):
        config.THEME_CSS_FILE = 'main.css'


def create_default_config(output_path):
    """
    Create a default configuration file.
    
    Args:
        output_path: Path where the configuration file will be written
    """
    default_config = '''"""
Zerodown site configuration
"""

import os

# Site metadata
SITE_NAME = "My Zerodown Site"
SITE_DESCRIPTION = "A site built with Zerodown"
SITE_AUTHOR = "Your Name"

# Directory paths (relative to this file)
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "public"
STATIC_DIR = "static"
STYLES_DIR = "styles"

# Theme selection
THEME_CSS_FILE = "main.css"  # File from STYLES_DIR to use as main.css

# Content sections
SECTIONS = {
    "notes": {
        "title": "Notes",
        "sort_by": "date",
        "reverse": True
    },
    # Add more sections as needed
}
'''
    
    try:
        with open(output_path, 'w') as f:
            f.write(default_config)
        print(f"Created default configuration at: {output_path}")
    except Exception as e:
        print(f"ERROR: Failed to create default configuration: {e}")
        sys.exit(1)
