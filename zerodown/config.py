"""
Configuration handling for Zerodown static site generator.
"""

import os
import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import yaml
from types import SimpleNamespace


def load_config(config_path):
    """
    Load configuration from a file.
    
    Supports both Python (.py) and YAML (.yaml, .yml) configuration files.
    YAML files take precedence over Python files when both exist.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        config: Configuration module or object
    """
    # Check if the provided path exists
    file_exists = os.path.exists(config_path)
    
    # Get the directory and base name
    base_dir = os.path.dirname(config_path)
    base_name = os.path.splitext(os.path.basename(config_path))[0]
    
    # Check for YAML versions first (they take precedence)
    yaml_path = os.path.join(base_dir, f"{base_name}.yaml")
    yml_path = os.path.join(base_dir, f"{base_name}.yml")
    py_path = os.path.join(base_dir, f"{base_name}.py")
    
    # Determine which config file to use (in order of preference)
    if os.path.exists(yaml_path):
        config_path = yaml_path
        print(f"Using YAML configuration: {yaml_path}")
    elif os.path.exists(yml_path):
        config_path = yml_path
        print(f"Using YAML configuration: {yml_path}")
    elif os.path.exists(py_path):
        config_path = py_path
        print(f"Using Python configuration: {py_path}")
    elif file_exists:
        # Use the original path if it exists
        print(f"Using configuration: {config_path}")
    else:
        # No config file found
        print(f"ERROR: Configuration file not found: {config_path}")
        print(f"Tried: {yaml_path}, {yml_path}, {py_path}")
        sys.exit(1)
    
    try:
        # Determine the file type
        ext = os.path.splitext(config_path)[1].lower()
        
        if ext in ('.yaml', '.yml'):
            # Load YAML configuration
            config = _load_yaml_config(config_path)
        else:
            # Load Python configuration
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


def _load_yaml_config(config_path):
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        config: Configuration object
    """
    # Read the YAML file
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    # Create a config object
    config = SimpleNamespace()
    
    # Set basic site information
    config.SITE_NAME = config_data.get('site_name', 'Zerodown Site')
    config.SITE_DESCRIPTION = config_data.get('site_description', '')
    config.SITE_AUTHOR = config_data.get('site_author', config.SITE_NAME)
    config.BASE_URL = config_data.get('base_url', '/')
    
    # Determine paths based on the config file location
    base_dir = os.path.dirname(os.path.abspath(config_path))
    
    # Set directory paths
    config.CONTENT_DIR = os.path.join(base_dir, config_data.get('content_dir', 'content'))
    config.TEMPLATE_DIR = os.path.join(base_dir, config_data.get('template_dir', 'templates'))
    config.STYLES_DIR = os.path.join(base_dir, config_data.get('styles_dir', 'styles'))
    config.STATIC_DIR = os.path.join(base_dir, config_data.get('static_dir', 'static'))
    config.OUTPUT_DIR = os.path.join(base_dir, config_data.get('output_dir', '_site'))
    
    # Set theme settings
    config.THEME_CSS_FILE = config_data.get('theme_css_file', 'main.css')
    
    # Set sections
    config.SECTIONS = config_data.get('sections', {})
    
    return config


def create_default_config(output_path):
    """
    Create a default configuration file.
    
    Args:
        output_path: Path where the configuration file will be written
    """
    # Determine the file type based on extension
    ext = os.path.splitext(output_path)[1].lower()
    
    try:
        if ext in ('.yaml', '.yml'):
            # Create YAML configuration
            _create_default_yaml_config(output_path)
        else:
            # Create Python configuration
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
            with open(output_path, 'w') as f:
                f.write(default_config)
                
        print(f"Created default configuration at: {output_path}")
    except Exception as e:
        print(f"ERROR: Failed to create default configuration: {e}")
        sys.exit(1)


def _create_default_yaml_config(output_path):
    """
    Create a default YAML configuration file.
    
    Args:
        output_path: Path where to create the configuration file
    """
    default_config = {
        'site_name': 'My Zerodown Site',
        'site_description': 'A site built with Zerodown',
        'site_author': 'Your Name',
        'base_url': '/',
        
        'content_dir': 'content',
        'template_dir': 'templates',
        'styles_dir': 'styles',
        'static_dir': 'static',
        'output_dir': '_site',
        
        'theme_css_file': 'main.css',
        
        'sections': {
            'posts': {
                'title': 'Blog Posts',
                'template': 'post.html',
                'list_template': 'post_list.html',
                'sort_by': 'date',
                'reverse_sort': True
            }
        }
    }
    
    # Create parent directories if they don't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Write the YAML file
    with open(output_path, 'w') as f:
        yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)
