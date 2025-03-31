"""
Content handling for the Zerodown static site generator.
"""

import os
import datetime
import sys
from pathlib import Path
from zerodown.markdown import parse_markdown_file
from zerodown.templates import render_template
from zerodown.utils import write_output_file
from zerodown.console import zconsole


def process_section(config, jinja_env, section_key, section_config, all_items):
    """
    Process a single section of content.
    
    Args:
        config: Configuration module
        jinja_env: Jinja2 environment
        section_key: Key identifying the section
        section_config: Configuration for this section
        all_items: List to which processed items will be added
        
    Returns:
        list: Processed items for this section
    """
    if not isinstance(section_config, dict):
        zconsole.warning(f"Invalid configuration for section '{section_key}'. Skipping.")
        return []

    section_title = section_config.get('title', section_key.capitalize())  # Default title
    
    section_content_dir = os.path.join(config.CONTENT_DIR, section_key)
    section_output_dir = os.path.join(config.OUTPUT_DIR, section_key)

    if not os.path.isdir(section_content_dir):
        zconsole.warning(f"Content directory not found for section '{section_key}': {section_content_dir}. Skipping section.")
        return []  # Skip this section if content dir doesn't exist

    try:
        os.makedirs(section_output_dir, exist_ok=True)  # Ensure output dir exists
    except OSError as e:
        zconsole.error(f"Failed to create output directory '{section_output_dir}': {e}. Skipping section.")
        return []

    section_items = []

    # Find and parse all markdown files in the section directory
    try:
        filenames = os.listdir(section_content_dir)
    except OSError as e:
        zconsole.error(f"Error reading content directory '{section_content_dir}': {e}. Skipping section.")
        return []

    for filename in filenames:
        if filename.lower().endswith(".md") and not filename.startswith('.'):  # Ignore hidden files
            filepath = os.path.join(section_content_dir, filename)
            if os.path.isfile(filepath):  # Ensure it's a file
                # Determine the output path for this item
                output_filename = os.path.splitext(filename)[0] + '.html'
                output_path = os.path.join(section_output_dir, output_filename)
                
                # Create context for shortcode processing
                item_context = {
                    "config": config,
                    "section_key": section_key,
                    "section_config": section_config,
                    "latest_items": all_items  # Pass existing items for dynamic content
                }
                
                # Parse the markdown file with asset handling and shortcode processing
                parsed_item = parse_markdown_file(
                    filepath, 
                    output_path=output_path, 
                    base_url=config.BASE_URL,
                    context=item_context
                )
                
                if parsed_item:  # Check if parsing succeeded
                    # Add URL and section info
                    parsed_item["url"] = f"/{section_key}/{parsed_item['slug']}.html"
                    parsed_item["section_key"] = section_key
                    section_items.append(parsed_item)

    # Sort items if configured
    sort_items(section_items, section_config, section_key)
    zconsole.info(f"Sorted {len(section_items)} items by '{section_config.get('sort_by', 'date')}' (reverse={section_config.get('sort_reverse', True)})")

    # Build individual pages for each item
    zconsole.info(f"Building {len(section_items)} individual pages using template '{section_config.get('template', 'page.html')}'...")
    build_item_pages(config, jinja_env, section_items, section_config)

    # Build section list page
    list_template = section_config.get('list_template', 'list.html')
    index_path = f"{section_output_dir}/index.html"
    zconsole.info(f"Building section list page '{index_path}' using template '{list_template}'...")
    build_section_list(config, jinja_env, section_items, section_config, section_key, section_title)

    # Add items to the global list
    all_items.extend(section_items)
    
    return section_items


def sort_items(items, config, section_key):
    """
    Sort a list of content items based on configuration.
    
    Args:
        items: List of content items to sort
        config: Configuration for the section
        section_key: Key identifying the section
    """
    sort_key = config.get("sort_by")
    if not sort_key or not items:  # Only sort if key exists and items exist
        return
        
    reverse_sort = config.get("reverse_sort", False)

    # Handle cases where the sort key might be missing or have incompatible types
    def get_sort_value(item):
        value = item['metadata'].get(sort_key)
        if value is None:
            # Provide default fallback values for sorting if key is missing
            if isinstance(sort_key, str) and 'date' in sort_key:
                return datetime.date.min if reverse_sort else datetime.date.max
            else:
                return 0  # Or float('-inf') / float('inf') depending on desired behavior
        return value

    try:
        # Use a try-except block during sort in case of incompatible types comparison
        items.sort(key=get_sort_value, reverse=reverse_sort)
    except TypeError as e:
        zconsole.warning(f"Could not sort section '{section_key}' by '{sort_key}'. Check data types are comparable. Error: {e}")


def build_item_pages(config, jinja_env, items, section_config):
    """
    Build individual HTML pages for each content item.
    
    Args:
        config: Configuration module
        jinja_env: Jinja2 environment
        items: List of content items
        section_config: Configuration for this section
    """
    if not items:
        return
        
    item_template = section_config.get("template", "page.html")  # Default to page.html
    
    for item in items:
        output_path = os.path.join(config.OUTPUT_DIR, item["section_key"], f"{item['slug']}.html")
        page_title = f"{item['metadata'].get('title', 'Untitled')} - {config.SITE_NAME}"
        
        context = {
            "item": item,
            "title": page_title,
            "description": item['metadata'].get('description', config.SITE_DESCRIPTION)
        }
        
        html_output = render_template(jinja_env, item_template, context)
        write_output_file(output_path, html_output)


def build_section_list(config, jinja_env, items, section_config, section_key, section_title):
    """
    Build a list page for a section.
    
    Args:
        config: Configuration module
        jinja_env: Jinja2 environment
        items: List of content items
        section_config: Configuration for this section
        section_key: Key identifying the section
        section_title: Title for the section
    """
    list_template = section_config.get("list_template", "list.html")  # Default to list.html
    list_output_path = os.path.join(config.OUTPUT_DIR, section_key, "index.html")
    list_title = f"{section_title} - {config.SITE_NAME}"  # Use defined section title
    
    # Logging is now handled in the process_section function
    
    context = {
        "items": items,
        "section": section_config,
        "section_key": section_key,
        "title": list_title
    }
    
    html_output = render_template(jinja_env, list_template, context)
    write_output_file(list_output_path, html_output)


def build_homepage(config, jinja_env, all_items):
    """
    Build the main homepage.
    
    Args:
        config: Configuration module
        jinja_env: Jinja2 environment
        all_items: List of all content items
    """
    zconsole.subheader("Building top-level pages")
    
    index_output_path = os.path.join(config.OUTPUT_DIR, "index.html")
    context = {
        "title": config.SITE_NAME,
        "description": config.SITE_DESCRIPTION,
        "latest_items": all_items,  # Pass all items for potential use on homepage
        "config": config  # Pass the entire config object for shortcodes
    }
    
    # Look for a home.md file in the content directory (preferred approach)
    home_md_path = os.path.join(config.CONTENT_DIR, "home.md")
    if os.path.isfile(home_md_path):
        # Parse the home.md file with context for shortcodes
        home_content = parse_markdown_file(
            home_md_path,
            output_path=index_output_path,
            base_url=config.BASE_URL,
            context=context  # Pass context for shortcode processing
        )
        if home_content:
            # Add the parsed home content to the context
            context["home_content"] = home_content
            
            # For backward compatibility, also provide home_html
            if "home_html" not in context and "content_html" in home_content:
                context["home_html"] = home_content["content_html"]
    
    html_output = render_template(jinja_env, "index.html", context)
    success = write_output_file(index_output_path, html_output)
    
    if success:
        zconsole.success(f"Built homepage: {index_output_path}")


def process_top_level_pages(config, jinja_env):
    """
    Process any standalone pages at the top level of the content directory.
    
    Args:
        config: Configuration module
        jinja_env: Jinja2 environment
    """
    # This is a placeholder for future functionality
    # Example: Build an about page from content/about.md if it exists
    about_md_path = os.path.join(config.CONTENT_DIR, "about.md")
    if os.path.exists(about_md_path) and os.path.isfile(about_md_path):
        # Determine the output path
        about_output_path = os.path.join(config.OUTPUT_DIR, "about.html")
        
        # Create context for the page
        context = {
            "title": "About",
            "config": config
        }
        
        # Parse the markdown file with asset handling and shortcode processing
        about_item = parse_markdown_file(
            about_md_path, 
            output_path=about_output_path, 
            base_url=config.BASE_URL,
            context=context  # Pass context for shortcode processing
        )
        
        if about_item:
            # Decide on template
            about_template = getattr(config, 'TOP_LEVEL_TEMPLATE', 'page.html')
            
            # Create context
            context = {
                "item": about_item, 
                "title": f"{about_item['metadata'].get('title', 'About')} - {config.SITE_NAME}"
            }
            
            # Render and write
            html_output = render_template(jinja_env, about_template, context)
            success = write_output_file(about_output_path, html_output)
            
            if success:
                zconsole.success(f"Built page: {about_output_path}")
