"""
Configuration for the Zerodown blog example.
"""

import os

# Site information
SITE_NAME = "My Zerodown Blog"
SITE_DESCRIPTION = "A simple blog built with Zerodown"
BASE_URL = "/"  # Use "/" for local development, or your domain for production

# Directory paths
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
STYLES_DIR = os.path.join(os.path.dirname(__file__), "styles")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "_site")

# Theme settings
THEME_CSS_FILE = "blog.css"  # The CSS file to use from the styles directory

# Content sections
SECTIONS = {
    "posts": {
        "title": "Blog Posts",
        "template": "post.html",
        "list_template": "post_list.html",
        "sort_by": "date",
        "reverse_sort": True  # Newest first
    }
}

# Navigation items
NAV_ITEMS = [
    {"title": "Home", "url": "/"},
    {"title": "Blog", "url": "/posts/"},
    {"title": "About", "url": "/about.html"}
]
