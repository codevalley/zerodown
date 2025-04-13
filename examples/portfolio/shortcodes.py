"""
Custom shortcodes for the portfolio example.
"""

import jinja2
from pathlib import Path
import os
import re

def parse_shortcode_attributes(attrs_string):
    """Parse attributes from a shortcode string."""
    attrs = {}
    if not attrs_string:
        return attrs
    
    # Match key="value" patterns
    pattern = r'(\w+)="([^"]*)"'
    matches = re.findall(pattern, attrs_string)
    
    for key, value in matches:
        attrs[key] = value
    
    return attrs

def featured_projects_shortcode(content, attrs_string, site_config, page_context):
    """Render featured projects shortcode."""
    attrs = parse_shortcode_attributes(attrs_string)
    count = int(attrs.get('count', 3))
    
    # Get the project section from config
    project_section = site_config.get('sections', {}).get('projects', {})
    if not project_section:
        return "<p>Error: Projects section not found in config</p>"
    
    # Get content directory
    content_dir = site_config.get('content_dir', 'content')
    if not isinstance(content_dir, str):
        content_dir = site_config.get('CONTENT_DIR', 'content')
    
    # Get projects directory
    projects_dir = Path(content_dir) / 'projects'
    if not projects_dir.exists():
        return "<p>Error: Projects directory not found</p>"
    
    # Collect project files
    projects = []
    for md_file in projects_dir.glob('*.md'):
        with open(md_file, 'r') as f:
            content = f.read()
        
        # Extract frontmatter
        metadata = {}
        if content.startswith('---'):
            _, frontmatter, content = content.split('---', 2)
            for line in frontmatter.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        # Only include featured projects
        if metadata.get('featured', 'false').lower() == 'true':
            metadata['url'] = f"/projects/{md_file.stem}.html"
            projects.append(metadata)
    
    # Sort projects by order if available
    projects.sort(key=lambda p: int(p.get('order', 999)))
    
    # Limit to count
    projects = projects[:count]
    
    # Render HTML
    html = '<div class="featured-projects">\n'
    html += '<h2>Featured Projects</h2>\n'
    html += '<div class="project-grid">\n'
    
    for project in projects:
        html += f'<div class="project-card">\n'
        if 'image' in project:
            html += f'<div class="project-card-image">\n'
            html += f'<a href="{project["url"]}">\n'
            html += f'<img src="{project["image"]}" alt="{project.get("title", "Project")}">\n'
            html += f'</a>\n'
            html += f'</div>\n'
        
        html += f'<div class="project-card-content">\n'
        html += f'<h3><a href="{project["url"]}">{project.get("title", "Project")}</a></h3>\n'
        
        if 'summary' in project:
            html += f'<p>{project["summary"]}</p>\n'
        
        html += f'<a href="{project["url"]}" class="read-more">View Project →</a>\n'
        html += f'</div>\n'
        html += f'</div>\n'
    
    html += '</div>\n'
    html += '</div>\n'
    
    return html

def section_list_shortcode(content, attrs_string, site_config, page_context):
    """Render section list shortcode."""
    attrs = parse_shortcode_attributes(attrs_string)
    section_name = attrs.get('section')
    
    if not section_name:
        return "<p>Error: Section name not specified</p>"
    
    # Get the section from config
    section = site_config.get('sections', {}).get(section_name, {})
    if not section:
        section = site_config.get('SECTIONS', {}).get(section_name, {})
    
    if not section:
        return f"<p>Error: Section '{section_name}' not found in config</p>"
    
    # Get content directory
    content_dir = site_config.get('content_dir', 'content')
    if not isinstance(content_dir, str):
        content_dir = site_config.get('CONTENT_DIR', 'content')
    
    # Get section directory
    section_dir = Path(content_dir) / section_name
    if not section_dir.exists():
        return f"<p>Error: Section directory '{section_name}' not found</p>"
    
    # Collect section files
    items = []
    for md_file in section_dir.glob('*.md'):
        with open(md_file, 'r') as f:
            content = f.read()
        
        # Extract frontmatter
        metadata = {}
        if content.startswith('---'):
            _, frontmatter, content = content.split('---', 2)
            for line in frontmatter.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        metadata['url'] = f"/{section_name}/{md_file.stem}.html"
        items.append(metadata)
    
    # Sort items
    sort_by = section.get('sort_by', 'title')
    reverse_sort = section.get('reverse_sort', False)
    
    def get_sort_key(item):
        key = item.get(sort_by)
        if sort_by == 'order' and key:
            return int(key)
        return key or ''
    
    items.sort(key=get_sort_key, reverse=reverse_sort)
    
    # Render HTML
    html = '<div class="section-list">\n'
    html += '<div class="project-grid">\n'
    
    for item in items:
        html += f'<div class="project-card">\n'
        if 'image' in item:
            html += f'<div class="project-card-image">\n'
            html += f'<a href="{item["url"]}">\n'
            html += f'<img src="{item["image"]}" alt="{item.get("title", "Item")}">\n'
            html += f'</a>\n'
            html += f'</div>\n'
        
        html += f'<div class="project-card-content">\n'
        html += f'<h3><a href="{item["url"]}">{item.get("title", "Item")}</a></h3>\n'
        
        if 'summary' in item:
            html += f'<p>{item["summary"]}</p>\n'
        
        html += f'<a href="{item["url"]}" class="read-more">View Details →</a>\n'
        html += f'</div>\n'
        html += f'</div>\n'
    
    html += '</div>\n'
    html += '</div>\n'
    
    return html

# Register shortcodes
SHORTCODES = {
    'featured_projects': featured_projects_shortcode,
    'section_list': section_list_shortcode
} 