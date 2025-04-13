"""
Script to generate latest_items.json for shortcode processing.
This is a workaround for the portfolio example to ensure shortcodes work.
"""

import os
import json
import glob
from pathlib import Path

def main():
    print("Generating latest_items.json for shortcode processing...")
    
    # Get content directory
    content_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    projects_dir = content_dir / 'projects'
    
    if not projects_dir.exists():
        print(f"Error: Projects directory not found at {projects_dir}")
        return
    
    # Collect all project items
    latest_items = []
    
    for md_file in projects_dir.glob('*.md'):
        with open(md_file, 'r') as f:
            content = f.read()
        
        # Parse frontmatter
        metadata = {}
        if content.startswith('---'):
            _, frontmatter, content = content.split('---', 2)
            for line in frontmatter.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    
                    # Parse boolean values
                    if value.strip().lower() == 'true':
                        metadata[key.strip()] = True
                    elif value.strip().lower() == 'false':
                        metadata[key.strip()] = False
                    else:
                        metadata[key.strip()] = value.strip()
        
        # Build item object
        item = {
            "url": f"/projects/{md_file.stem}.html",
            "slug": md_file.stem,
            "section_key": "projects",
            "metadata": metadata,
            "content_html": f"<h1>{metadata.get('title', 'Project')}</h1>",
        }
        
        latest_items.append(item)
    
    # Sort items by order if available
    latest_items.sort(key=lambda p: int(p.get("metadata", {}).get("order", 999)))
    
    # Write to JSON file
    output_file = content_dir / '_includes' / 'latest_items.json'
    with open(output_file, 'w') as f:
        json.dump(latest_items, f, indent=2)
    
    print(f"Generated {output_file} with {len(latest_items)} items")

if __name__ == "__main__":
    main() 