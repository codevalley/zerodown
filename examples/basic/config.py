# config.py
import datetime # Need this if using default sorting for dates

SITE_NAME = "Your Name"
SITE_AUTHOR = "Your Name"
SITE_DESCRIPTION = "Thoughts and creations"
BASE_URL = "http://localhost:8000" # Or your final domain "https://yourwebsite.com"

CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
STATIC_DIR = "static"
STYLES_DIR = "styles"
OUTPUT_DIR = "public"

# Theme configuration
THEME_CSS_FILE = "main.css"  # Change this to use a different theme file
# ADDITIONAL_CSS_FILES = ["syntax-highlighting.css"]  # Uncomment to include additional CSS files

# Define the sections of your site based on folders in 'content/'
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