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
        content: HTML content to process
        context: Context dictionary with site data
        
    Returns:
        str: Processed content with shortcodes replaced
    """
    # Match shortcodes like [shortcode_name param1="value1" param2="value2"]
    pattern = r'\[(\w+)(?:\s+([^\]]+))?\]'
    
    def replace_shortcode(match):
        shortcode_name = match.group(1)
        params_str = match.group(2) or ""
        
        # Parse parameters
        params = {}
        if params_str:
            param_pattern = r'(\w+)=["\']([^"\']+)["\']'
            for param_match in re.finditer(param_pattern, params_str):
                params[param_match.group(1)] = param_match.group(2)
        
        # Execute the shortcode
        if shortcode_name in SHORTCODE_REGISTRY:
            return SHORTCODE_REGISTRY[shortcode_name](context, **params)
        else:
            return f"[Unknown shortcode: {shortcode_name}]"
    
    return re.sub(pattern, replace_shortcode, content)

# Define built-in shortcodes

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
    posts = []
    
    if "latest_items" in context:
        for item in context["latest_items"]:
            if item.get("section_key") == section:
                posts.append(item)
        
        posts = sorted(posts, key=lambda x: x.get("metadata", {}).get("date", ""), reverse=True)[:count]
    
    if not posts:
        return "<p>No posts found.</p>"
    
    # Render the posts
    template_str = """
    <div class="latest-posts">
        {% for post in posts %}
        <div class="post-item">
            <h3><a href="{{ post.url }}">{{ post.metadata.title }}</a></h3>
            {% if post.metadata.date %}
            <span class="date">{{ post.metadata.date.strftime('%B %d, %Y') }}</span>
            {% endif %}
            <div class="excerpt">
                {% if post.metadata.excerpt %}
                    {{ post.metadata.excerpt }}
                {% else %}
                    {{ post.content_html | striptags | truncate(100) | safe }}
                {% endif %}
            </div>
            <a href="{{ post.url }}" class="read-more">Read More</a>
        </div>
        {% endfor %}
    </div>
    """
    template = Template(template_str)
    return template.render(posts=posts)

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
