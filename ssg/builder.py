"""
Main builder module for the static site generator.
"""

import os
import sys
import datetime
import time

from ssg.utils import clean_output_dir, copy_static_assets, copy_styles
from ssg.templates import setup_jinja_env, process_includes
from ssg.content import process_section, build_homepage, process_top_level_pages
from ssg.markdown import copy_content_assets


def build_site(config):
    """
    Main function to build the entire static site.
    """
    start_time = datetime.datetime.now()
    print("Starting site build...")

    # 1. Setup
    clean_output_dir(config)  # Exits on error
    copy_static_assets(config)  # Continues on error
    copy_styles(config)  # Continues on error
    jinja_env = setup_jinja_env(config)  # Exits on error
    
    # 2. Process includes for global template context
    process_includes(config, jinja_env)
    
    # 3. Copy assets from content directory
    copy_content_assets(config)

    # 4. Process all sections
    all_items = []  # To collect items from all sections for homepage
    
    if not hasattr(config, 'SECTIONS') or not isinstance(config.SECTIONS, dict):
        print("ERROR: 'SECTIONS' dictionary not found or invalid in config.py")
        sys.exit(1)

    for section_key, section_config in config.SECTIONS.items():
        process_section(config, jinja_env, section_key, section_config, all_items)

    # 5. Build top-level pages
    build_homepage(config, jinja_env, all_items)
    process_top_level_pages(config, jinja_env)

    # 6. Finish and report
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"\nSite build complete in {duration.total_seconds():.2f} seconds.")
    print(f"Output generated in: {config.OUTPUT_DIR}")
    
    return True
