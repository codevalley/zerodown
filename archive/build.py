# build.py
import os
import shutil
import datetime
import frontmatter  # Handles YAML front matter
import markdown     # Converts Markdown to HTML
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Import configuration
import config

# --- Helper Functions ---

def clean_output_dir():
    """Removes and recreates the output directory."""
    print(f"Cleaning directory: {config.OUTPUT_DIR}")
    if os.path.exists(config.OUTPUT_DIR):
        shutil.rmtree(config.OUTPUT_DIR)
    os.makedirs(config.OUTPUT_DIR)

def copy_static_assets():
    """Copies static files (images, fonts, etc.) to the output directory."""
    print(f"Copying static assets from {config.STATIC_DIR} to {config.OUTPUT_DIR}")
    if os.path.exists(config.STATIC_DIR):
        shutil.copytree(config.STATIC_DIR, config.OUTPUT_DIR, dirs_exist_ok=True)
    else:
        print("Static directory not found, skipping.")

def copy_styles():
    """Copies CSS files to the output directory."""
    styles_output_dir = os.path.join(config.OUTPUT_DIR, 'styles')
    print(f"Copying styles from {config.STYLES_DIR} to {styles_output_dir}")
    if os.path.exists(config.STYLES_DIR):
        shutil.copytree(config.STYLES_DIR, styles_output_dir, dirs_exist_ok=True)
    else:
        print("Styles directory not found, skipping.")

def setup_jinja_env():
    """Sets up the Jinja2 templating environment."""
    print(f"Setting up Jinja2 environment for templates in: {config.TEMPLATE_DIR}")
    env = Environment(
        loader=FileSystemLoader(config.TEMPLATE_DIR),
        autoescape=select_autoescape(['html', 'xml']),
        # Enable access to config and functions in templates
        globals={
            'config': config,
            'now': datetime.datetime.now # Example utility function
        }
    )
    return env

def parse_markdown_file(filepath):
    """Parses a Markdown file, extracting front matter and converting content."""
    try:
        post = frontmatter.load(filepath)
        html_content = markdown.markdown(
            post.content,
            extensions=[
                'fenced_code', # Support ```code``` blocks
                'codehilite',  # Add syntax highlighting classes (requires CSS)
                'tables',      # Support Markdown tables
                'toc'          # Table of contents (optional)
            ]
        )
        # Ensure date is a Python date object if present
        if 'date' in post.metadata and not isinstance(post.metadata['date'], datetime.date):
           try:
               post.metadata['date'] = datetime.datetime.strptime(str(post.metadata['date']), '%Y-%m-%d').date()
           except ValueError:
               print(f"Warning: Could not parse date '{post.metadata['date']}' in {filepath}. Expected YYYY-MM-DD.")
               # Decide how to handle invalid dates (e.g., set to None, use file mod time)
               post.metadata['date'] = None # Or keep the original string / raise error

        return {
            "metadata": post.metadata,
            "content_html": html_content,
            "filepath": filepath,
            "slug": os.path.splitext(os.path.basename(filepath))[0] # Use filename (without ext) as slug
        }
    except Exception as e:
        print(f"Error parsing Markdown file {filepath}: {e}")
        return None

def render_template(env, template_name, context):
    """Renders a Jinja2 template with the given context."""
    try:
        template = env.get_template(template_name)
        return template.render(context)
    except Exception as e:
        print(f"Error rendering template {template_name}: {e}")
        return f"Error rendering template: {e}" # Return error message in output

def build_site():
    """Main function to build the entire static site."""
    start_time = datetime.datetime.now()
    print("Starting site build...")

    # 1. Setup
    clean_output_dir()
    copy_static_assets()
    copy_styles()
    jinja_env = setup_jinja_env()

    all_items = [] # To potentially collect items from all sections for homepage

    # 2. Process Sections defined in config.py
    for section_key, section_config in config.SECTIONS.items():
        print(f"\nProcessing section: {section_key} ({section_config.title})")
        section_content_dir = os.path.join(config.CONTENT_DIR, section_key)
        section_output_dir = os.path.join(config.OUTPUT_DIR, section_key)
        os.makedirs(section_output_dir, exist_ok=True)

        section_items = []

        if not os.path.isdir(section_content_dir):
            print(f"Warning: Content directory not found for section '{section_key}': {section_content_dir}")
            continue

        # Find and parse all markdown files in the section directory
        for filename in os.listdir(section_content_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(section_content_dir, filename)
                parsed_item = parse_markdown_file(filepath)
                if parsed_item:
                    # Add URL and section info
                    parsed_item["url"] = f"/{section_key}/{parsed_item['slug']}.html"
                    parsed_item["section_key"] = section_key
                    section_items.append(parsed_item)

        # Sort items if configured
        sort_key = section_config.get("sort_by")
        if sort_key:
            reverse_sort = section_config.get("reverse_sort", False)
            # Handle cases where the sort key might be missing in some items' metadata
            section_items.sort(
                key=lambda item: item['metadata'].get(sort_key) if item['metadata'].get(sort_key) is not None else (datetime.date.min if isinstance(sort_key, str) and 'date' in sort_key else 0),
                # Provide a default value for sorting if key is missing. Use date.min for dates, 0 otherwise.
                reverse=reverse_sort
            )
            print(f"Sorted {len(section_items)} items by '{sort_key}' (reverse={reverse_sort})")


        all_items.extend(section_items) # Add to global list

        # Build individual item pages
        item_template = section_config.get("template", "page.html") # Default to page.html
        print(f"Building {len(section_items)} individual pages using template '{item_template}'...")
        for item in section_items:
            output_path = os.path.join(section_output_dir, f"{item['slug']}.html")
            page_title = f"{item['metadata'].get('title', 'Untitled')} - {config.SITE_NAME}"
            context = {
                "item": item,
                "title": page_title,
                "description": item['metadata'].get('description', config.SITE_DESCRIPTION)
            }
            html_output = render_template(jinja_env, item_template, context)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_output)
            # print(f"  Built: {output_path}") # Uncomment for verbose output

        # Build section list page (index.html for the section)
        list_template = section_config.get("list_template", "list.html") # Default to list.html
        list_output_path = os.path.join(section_output_dir, "index.html")
        list_title = f"{section_config.get('title', section_key.capitalize())} - {config.SITE_NAME}"
        print(f"Building section list page '{list_output_path}' using template '{list_template}'...")
        context = {
            "items": section_items,
            "section": section_config,
            "title": list_title
        }
        html_output = render_template(jinja_env, list_template, context)
        with open(list_output_path, "w", encoding="utf-8") as f:
            f.write(html_output)

    # 3. Build Top-Level Pages (e.g., main index.html)
    print("\nBuilding top-level pages...")
    index_output_path = os.path.join(config.OUTPUT_DIR, "index.html")
    context = {
        "title": config.SITE_NAME, # Homepage title
        "description": config.SITE_DESCRIPTION,
        "latest_items": all_items # Pass all items for potential use on homepage
    }
    html_output = render_template(jinja_env, "index.html", context)
    with open(index_output_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"Built homepage: {index_output_path}")

    # --- Add logic here to build other top-level pages if needed ---
    # Example: Build an about page from content/about.md
    # about_md_path = os.path.join(config.CONTENT_DIR, "about.md")
    # if os.path.exists(about_md_path):
    #    about_item = parse_markdown_file(about_md_path)
    #    if about_item:
    #        about_output_path = os.path.join(config.OUTPUT_DIR, "about.html")
    #        about_template = config.TOP_LEVEL_TEMPLATE # Or specific template like "page.html"
    #        context = {"item": about_item, "title": f"{about_item['metadata'].get('title', 'About')} - {config.SITE_NAME}"}
    #        html_output = render_template(jinja_env, about_template, context)
    #        with open(about_output_path, "w", encoding="utf-8") as f:
    #             f.write(html_output)
    #        print(f"Built About page: {about_output_path}")


    # 4. Finish
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"\nSite build complete in {duration.total_seconds():.2f} seconds.")
    print(f"Output generated in: {config.OUTPUT_DIR}")


# --- Main Execution ---
if __name__ == "__main__":
    build_site()