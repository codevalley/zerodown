"""
Utility functions for the static site generator.
"""

import os
import shutil
import sys


def clean_output_dir(config):
    """Removes and recreates the output directory."""
    print(f"Cleaning directory: {config.OUTPUT_DIR}")
    try:
        if os.path.exists(config.OUTPUT_DIR):
            shutil.rmtree(config.OUTPUT_DIR)
        os.makedirs(config.OUTPUT_DIR)
    except OSError as e:
        print(f"Error cleaning output directory: {e}")
        sys.exit(1)


def copy_static_assets(config):
    """Copies static files (images, fonts, etc.) to the output directory."""
    print(f"Copying static assets from {config.STATIC_DIR} to {config.OUTPUT_DIR}")
    if os.path.exists(config.STATIC_DIR) and os.path.isdir(config.STATIC_DIR):
        try:
            shutil.copytree(config.STATIC_DIR, config.OUTPUT_DIR, dirs_exist_ok=True)
        except OSError as e:
            print(f"Error copying static assets: {e}")
    else:
        print(f"Static directory '{config.STATIC_DIR}' not found or not a directory, skipping.")


def copy_styles(config):
    """Copies the selected theme CSS file as main.css."""
    styles_output_dir = os.path.join(config.OUTPUT_DIR, 'styles')
    selected_theme_file = getattr(config, 'THEME_CSS_FILE', 'main.css')
    source_css_path = os.path.join(config.STYLES_DIR, selected_theme_file)
    target_css_path = os.path.join(styles_output_dir, 'main.css')

    print(f"Applying theme: Copying '{source_css_path}' to '{target_css_path}'")

    if os.path.isfile(source_css_path):
        try:
            os.makedirs(styles_output_dir, exist_ok=True)
            shutil.copy2(source_css_path, target_css_path)
        except OSError as e:
             print(f"Error copying theme CSS: {e}")
    else:
        print(f"Styles theme file '{source_css_path}' not found, skipping CSS copy.")
        
    # Copy any additional CSS files that should always be included
    additional_css_files = getattr(config, 'ADDITIONAL_CSS_FILES', [])
    for css_file in additional_css_files:
        additional_source = os.path.join(config.STYLES_DIR, css_file)
        additional_target = os.path.join(styles_output_dir, css_file)
        if os.path.isfile(additional_source):
            try:
                shutil.copy2(additional_source, additional_target)
                print(f"Copied additional CSS: {css_file}")
            except OSError as e:
                print(f"Error copying additional CSS file {css_file}: {e}")
        else:
            print(f"Additional CSS file '{additional_source}' not found, skipping.")


def write_output_file(output_path, content):
    """Writes content to an output file with proper error handling."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except OSError as e:
        print(f"Error writing file {output_path}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error writing file {output_path}: {e}")
        return False
