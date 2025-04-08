"""
YAML configuration handler for Zerodown.
"""

import os
import yaml
from pathlib import Path
from types import SimpleNamespace


def load_yaml_config(config_path):
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        A SimpleNamespace object with configuration attributes
    """
    # Read the YAML file
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    # Create a config object
    config = SimpleNamespace()
    
    # Set basic site information
    config.SITE_NAME = config_data.get('site_name', 'Zerodown Site')
    config.SITE_DESCRIPTION = config_data.get('site_description', '')
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
    
    # Set navigation items
    config.NAV_ITEMS = config_data.get('nav_items', [])

    # Set additional CSS files
    config.ADDITIONAL_CSS_FILES = config_data.get('additional_css_files', [])

    # Add uppercase versions for compatibility with utils.copy_styles and templates expecting uppercase
    for key in ['SITE_NAME', 'SITE_DESCRIPTION', 'BASE_URL', 
                'CONTENT_DIR', 'TEMPLATE_DIR', 'STYLES_DIR', 
                'STATIC_DIR', 'OUTPUT_DIR', 'THEME_CSS_FILE', 
                'SECTIONS', 'NAV_ITEMS', 'ADDITIONAL_CSS_FILES']:
        lower_key = key.lower()
        if hasattr(config, lower_key):
            setattr(config, key, getattr(config, lower_key))

    return config


def create_default_yaml_config(config_path):
    """
    Create a default YAML configuration file.
    
    Args:
        config_path: Path where to create the configuration file
    """
    default_config = {
        'site_name': 'My Zerodown Site',
        'site_description': 'A site built with Zerodown',
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
    os.makedirs(os.path.dirname(os.path.abspath(config_path)), exist_ok=True)
    
    # Write the YAML file
    with open(config_path, 'w') as f:
        yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created default configuration at: {config_path}")
