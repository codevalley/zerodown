"""
Configuration for the Zerodown portfolio example.
"""

import os

# Site information
SITE_NAME = "My Portfolio"
SITE_DESCRIPTION = "A showcase of my work and skills"
BASE_URL = "/"  # Use "/" for local development, or your domain for production

# Directory paths
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
STYLES_DIR = os.path.join(os.path.dirname(__file__), "styles")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "_site")

# Theme settings
THEME_CSS_FILE = "portfolio-minimal.css"  # The CSS file to use from the styles directory

# Content sections
SECTIONS = {
    "projects": {
        "title": "My Projects",
        "template": "project.html",
        "list_template": "project_list.html",
        "sort_by": "order",  # Custom sort order
        "reverse_sort": False  # Important first
    }
}

# Navigation items
NAV_ITEMS = [
    {"title": "Home", "url": "/"},
    {"title": "Projects", "url": "/projects/"},
    {"title": "About", "url": "/about.html"},
    {"title": "Contact", "url": "/contact.html"}
]

# Shortcodes module
SHORTCODES_MODULE = "shortcodes"
