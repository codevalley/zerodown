"""
Shortcode processing for the Zerodown static site generator.

This module provides a way to include dynamic content in Markdown files
through shortcodes like [latest_posts], [section_list], etc.
"""

import re
import os
from jinja2 import Template

# Registry of available shortcodes
SHORTCODE_REGISTRY = {}

def register_shortcode(name):
    """
    Decorator to register a shortcode handler function.
    
    Args:
        name: Name of the shortcode
        
    Returns:
        Function decorator
    """
    def decorator(func):
        SHORTCODE_REGISTRY[name] = func
        return func
    return decorator

def process_shortcodes(content, context):
    """
    Process all shortcodes in the content.
    
    Args:
        content: Content to process (Markdown or HTML)
        context: Context dictionary with site data
        
    Returns:
        str: Processed content with shortcodes replaced
    """
    # Match shortcodes like [shortcode_name param1="value1" param2="value2"]
    # More specific pattern to avoid matching common markdown
    pattern = r'(?<!\s)\[(\w+)(?:\s+([^\]]+))?\](?!\()'
    
    def replace_shortcode(match):
        shortcode_name = match.group(1)
        params_str = match.group(2) or ""
        
        # Check if this is part of a markdown link pattern like [text](url)
        # Look ahead to see if the match is followed by a parenthesis, which would indicate a markdown link
        match_end_pos = match.end()
        if match_end_pos < len(content) and match_end_pos + 1 <= len(content):
            next_char = content[match_end_pos:match_end_pos+1]
            if next_char == '(':
                # This is part of a markdown link, not a shortcode
                return match.group(0)
        
        # Skip if it looks like a standard Markdown reference-style link
        if re.match(r'^[\w\-\.]+$', shortcode_name) and not params_str:
            # This is probably a reference-style Markdown link
            return match.group(0)
        
        # Avoid processing if there are spaces around the shortcode name
        # This helps prevent false positives in documentation
        if " " in match.group(0).strip()[1:-1]:
            return match.group(0)
        
        # Parse parameters
        params = {}
        if params_str:
            # Match param="value" or param='value' patterns
            param_pattern = r'(\w+)=["\']([^"\']+)["\']'
            for param_match in re.finditer(param_pattern, params_str):
                params[param_match.group(1)] = param_match.group(2)
        
        # Execute the shortcode
        if shortcode_name in SHORTCODE_REGISTRY:
            try:
                return SHORTCODE_REGISTRY[shortcode_name](context, **params)
            except Exception as e:
                from zerodown.console import zconsole
                zconsole.error(f"Error processing shortcode: {shortcode_name}", str(e))
                return f"<p>Error in shortcode [{shortcode_name}]: {str(e)}</p>"
        else:
            # Only treat as a shortcode if it has parameters or looks like one
            if params or params_str:
                return f"<p>Unknown shortcode: [{shortcode_name}]</p>"
            return match.group(0)  # Return the original text for false positives
    
    return re.sub(pattern, replace_shortcode, content)

# Define built-in shortcodes

@register_shortcode("featured_items")
def featured_items_shortcode(context, count="3", section=None):
    """
    Display featured items.
    
    Args:
        context: Context dictionary with site data
        count: Number of items to display
        section: Optional section to filter items by
        
    Returns:
        str: HTML for the featured items
    """
    count = int(count)
    items = []
    
    if "latest_items" in context:
        for item in context["latest_items"]:
            # Filter by section if provided
            if section and item.get("section_key") != section:
                continue
                
            # Check if item is featured
            if item.get("metadata", {}).get("featured"):
                items.append(item)
        
        items = items[:count]
    
    if not items:
        return "<p>No featured items found. Mark items as featured by adding <code>featured: true</code> to their frontmatter.</p>"
    
    template_str = """
    <div class="featured-items">
        <ul>
            {% for item in items %}
            <li>
                <a href="{{ item.url }}">{{ item.metadata.title }}</a>
                {% if item.metadata.description %}
                <p>{{ item.metadata.description }}</p>
                {% endif %}
            </li>
            {% endfor %}
        </ul>
    </div>
    """
    template = Template(template_str)
    return template.render(items=items)

@register_shortcode("latest_posts")
def latest_posts_shortcode(context, count="3", section="posts"):
    """
    Display the latest posts from a section.
    
    Args:
        context: Context dictionary with site data
        count: Number of posts to display
        section: Section key to get posts from
        
    Returns:
        str: HTML for the latest posts
    """
    count = int(count)
    items = []
    
    if "latest_items" in context:
        for item in context["latest_items"]:
            if item.get("section_key") == section:
                items.append(item)
        
        items = items[:count]  # Limit to requested count
    
    if not items:
        return "<p>No posts found.</p>"
    
    template_str = """
    <div class="latest-posts">
        <ul>
            {% for item in items %}
            <li>
                <a href="{{ item.url }}">{{ item.metadata.title }}</a>
                {% if item.metadata.date %}
                <time datetime="{{ item.metadata.date }}">
                    {{ item.metadata.date.strftime('%B %d, %Y') }}
                </time>
                {% endif %}
                {% if item.metadata.description %}
                <p>{{ item.metadata.description }}</p>
                {% endif %}
            </li>
            {% endfor %}
        </ul>
    </div>
    """
    template = Template(template_str)
    return template.render(items=items)

@register_shortcode("section_list")
def section_list_shortcode(context, section=None):
    """
    Display a list of all sections or items in a section.
    
    Args:
        context: Context dictionary with site data
        section: Optional section key to list items from
        
    Returns:
        str: HTML for the section list
    """
    if section:
        # List items from a specific section
        items = []
        if "latest_items" in context:
            for item in context["latest_items"]:
                if item.get("section_key") == section:
                    items.append(item)
        
        if not items:
            return f"<p>No items found in section '{section}'.</p>"
        
        template_str = """
        <div class="section-list">
            <ul>
                {% for item in items %}
                <li><a href="{{ item.url }}">{{ item.metadata.title }}</a></li>
                {% endfor %}
            </ul>
        </div>
        """
        template = Template(template_str)
        return template.render(items=items)
    else:
        # List all sections
        sections = {}
        config = context.get("config", {})
        
        # Check for lowercase 'sections' from YAML config
        if hasattr(config, "sections") and config.sections:
            sections = config.sections
        # Also check for uppercase 'SECTIONS' for backward compatibility
        elif hasattr(config, "SECTIONS") and config.SECTIONS:
            sections = config.SECTIONS
        
        if not sections:
            return "<p>No sections found.</p>"
        
        template_str = """
        <div class="section-list">
            <ul>
                {% for section_key, section_config in sections.items() %}
                <li><a href="/{{ section_key }}/">{{ section_config.title }}</a></li>
                {% endfor %}
            </ul>
        </div>
        """
        template = Template(template_str)
        return template.render(sections=sections)

@register_shortcode("featured_projects")
def featured_projects_shortcode(context, count="3"):
    """
    Display featured projects.
    
    Args:
        context: Context dictionary with site data
        count: Number of projects to display
        
    Returns:
        str: HTML for the featured projects
    """
    count = int(count)
    projects = []
    
    if "latest_items" in context:
        for item in context["latest_items"]:
            if item.get("section_key") == "projects" and item.get("metadata", {}).get("featured"):
                projects.append(item)
        
        projects = projects[:count]
    
    if not projects:
        return "<p>No featured projects found. Mark projects as featured by adding <code>featured: true</code> to their frontmatter.</p>"
    
    template_str = """
    <div class="featured-projects">
        <div class="project-grid">
            {% for project in projects %}
            <div class="project-card">
                {% if project.metadata.image %}
                <div class="project-card-image">
                    <img src="{{ project.metadata.image }}" alt="{{ project.metadata.title }}" style="max-width: 100%; height: auto; max-height: 100px; width: auto;">
                </div>
                {% endif %}
                <div class="project-card-content">
                    <h3 class="project-card-title">
                        <a href="{{ project.url }}">{{ project.metadata.title }}</a>
                    </h3>
                    <div class="project-card-description">
                        {% if project.metadata.summary %}
                            {{ project.metadata.summary }}
                        {% else %}
                            {{ project.content_html | striptags | truncate(100) | safe }}
                        {% endif %}
                    </div>
                    <a href="{{ project.url }}" class="read-more">View Project</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    """
    template = Template(template_str)
    return template.render(projects=projects)