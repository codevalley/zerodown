"""
Script to preprocess home.md and replace shortcodes with HTML before Zerodown processes it.
"""

import os
import json
import re
import sys
from pathlib import Path

def parse_shortcode_attributes(attrs_string):
    """Parse attributes from a shortcode string."""
    attrs = {}
    if not attrs_string:
        return attrs
    
    # Match key="value" patterns
    pattern = r'(\w+)=["\']([^"\']+)["\']'
    matches = re.findall(pattern, attrs_string)
    
    for key, value in matches:
        attrs[key] = value
    
    return attrs

def featured_projects_shortcode(count=3):
    """Render featured projects shortcode."""
    count = int(count)
    
    # Load latest items
    content_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'content'
    latest_items_file = content_dir / '_includes' / 'latest_items.json'
    
    if not latest_items_file.exists():
        return "<p>Error: latest_items.json not found. Run latest_items.py first.</p>"
    
    with open(latest_items_file, 'r') as f:
        all_items = json.load(f)
    
    # Filter to featured projects
    featured_items = []
    for item in all_items:
        if item.get('section_key') == 'projects' and item.get('metadata', {}).get('featured'):
            featured_items.append(item)
    
    # Sort and limit
    featured_items.sort(key=lambda p: int(p.get("metadata", {}).get("order", 999)))
    featured_items = featured_items[:count]
    
    if not featured_items:
        return "<p>No featured projects found.</p>"
    
    # Generate HTML
    html = '<div class="featured-projects">\n'
    html += '<h2>Featured Projects</h2>\n'
    html += '<div class="project-grid">\n'
    
    for project in featured_items:
        metadata = project.get('metadata', {})
        html += f'<div class="project-card">\n'
        
        # Skip images entirely - as per user request
        
        html += f'<div class="project-card-content">\n'
        html += f'<h3><a href="{project["url"]}">{metadata.get("title", "Project")}</a></h3>\n'
        
        if 'summary' in metadata:
            html += f'<p>{metadata["summary"]}</p>\n'
        
        if 'tags' in metadata and isinstance(metadata['tags'], list):
            html += f'<div class="tags">\n'
            for tag in metadata['tags'][:3]:
                html += f'<span class="tag">{tag}</span>\n'
            html += f'</div>\n'
        
        html += f'<a href="{project["url"]}" class="read-more">View Project →</a>\n'
        html += f'</div>\n'
        html += f'</div>\n'
    
    html += '</div>\n'
    html += '</div>\n'
    
    return html

def section_list_shortcode(section=None):
    """Render section list shortcode."""
    if not section:
        return "<p>Error: Section parameter is required.</p>"
    
    # Load latest items
    content_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'content'
    latest_items_file = content_dir / '_includes' / 'latest_items.json'
    
    if not latest_items_file.exists():
        return "<p>Error: latest_items.json not found. Run latest_items.py first.</p>"
    
    with open(latest_items_file, 'r') as f:
        all_items = json.load(f)
    
    # Filter by section
    section_items = []
    for item in all_items:
        if item.get('section_key') == section:
            section_items.append(item)
    
    if not section_items:
        return f"<p>No items found in section '{section}'.</p>"
    
    # Sort by order
    section_items.sort(key=lambda p: int(p.get("metadata", {}).get("order", 999)))
    
    # Generate HTML
    html = '<div class="section-list">\n'
    html += '<div class="project-grid">\n'
    
    for item in section_items:
        metadata = item.get('metadata', {})
        html += f'<div class="project-card">\n'
        
        # Skip images entirely - as per user request
        
        html += f'<div class="project-card-content">\n'
        html += f'<h3><a href="{item["url"]}">{metadata.get("title", "Item")}</a></h3>\n'
        
        if 'summary' in metadata:
            html += f'<p>{metadata["summary"]}</p>\n'
        
        if 'tags' in metadata and isinstance(metadata['tags'], list):
            html += f'<div class="tags">\n'
            for tag in metadata['tags'][:3]:
                html += f'<span class="tag">{tag}</span>\n'
            html += f'</div>\n'
        
        html += f'<a href="{item["url"]}" class="read-more">View Details →</a>\n'
        html += f'</div>\n'
        html += f'</div>\n'
    
    html += '</div>\n'
    html += '</div>\n'
    
    return html

def process_shortcodes(content):
    """Process shortcodes in content."""
    # Match shortcodes like [shortcode_name param="value"]
    pattern = r'\[(\w+)(?:\s+([^\]]+))?\]'
    
    def replace_shortcode(match):
        shortcode_name = match.group(1)
        params_str = match.group(2) or ""
        params = parse_shortcode_attributes(params_str)
        
        if shortcode_name == 'featured_projects':
            return featured_projects_shortcode(**params)
        elif shortcode_name == 'section_list':
            return section_list_shortcode(**params)
        else:
            return match.group(0)  # Keep original for unknown shortcodes
    
    return re.sub(pattern, replace_shortcode, content)

def preprocess_home_md():
    """Preprocess home.md and replace shortcodes with HTML."""
    portfolio_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    home_md_path = portfolio_dir / 'content' / 'home.md'
    
    if not home_md_path.exists():
        print(f"Error: home.md not found at {home_md_path}")
        return False
    
    with open(home_md_path, 'r') as f:
        content = f.read()
    
    # Check if the file has frontmatter
    has_frontmatter = content.startswith('---')
    
    if has_frontmatter:
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            # Process shortcodes in the body
            processed_body = process_shortcodes(body)
            processed_content = f"---{frontmatter}---{processed_body}"
        else:
            # Invalid frontmatter format
            processed_content = process_shortcodes(content)
    else:
        # No frontmatter
        processed_content = process_shortcodes(content)
    
    # Write back to home.md
    with open(home_md_path, 'w') as f:
        f.write(processed_content)
    
    print(f"Preprocessed {home_md_path} and replaced shortcodes with HTML")
    return True

if __name__ == "__main__":
    preprocess_home_md() 