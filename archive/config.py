# config.py
SITE_NAME = "Your Name"
SITE_AUTHOR = "Your Name"
SITE_DESCRIPTION = "Thoughts and creations"
# Base URL for production (important for absolute links, feeds, etc.)
# For local development, relative paths often work fine.
BASE_URL = "http://localhost:8000" # Or your final domain "https://yourwebsite.com"

CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
STATIC_DIR = "static"
STYLES_DIR = "styles"
OUTPUT_DIR = "public"

# Define the sections of your site based on folders in 'content/'
# Key: Matches the folder name in 'content/'
# Value: Dictionary with configuration for that section
SECTIONS = {
    "notes": {
        "title": "Notes",             # Human-readable title
        "template": "page.html",      # Template for individual items
        "list_template": "list.html", # Template for the section index
        "sort_by": "date",            # Sort items by 'date' field in front matter
        "reverse_sort": True,         # Show newest items first
    },
    # Add other sections like 'projects', 'art' here following the same pattern
    # "projects": { ... }
}

# Optional: Define specific templates for top-level files if needed
# Example: Use 'page.html' for any .md file directly in 'content/'
# TOP_LEVEL_TEMPLATE = "page.html"