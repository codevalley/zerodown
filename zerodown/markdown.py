"""
Markdown processing for the Zerodown static site generator.
"""

import os
import re
import datetime
import frontmatter
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from zerodown.shortcodes import process_shortcodes


class AssetProcessor(Treeprocessor):
    """
    A Markdown treeprocessor that adjusts image and link paths to work correctly
    in the generated site.
    """
    def __init__(self, md, item_path, output_path, base_url):
        super().__init__(md)
        self.item_path = item_path  # Path to the markdown file being processed
        self.output_path = output_path  # Path where the HTML will be output
        self.base_url = base_url  # Base URL of the site
        
    def run(self, root):
        """
        Process all image and anchor elements to adjust their paths.
        """
        # Process images
        for img in root.findall('.//img'):
            if 'src' in img.attrib:
                img.attrib['src'] = self._adjust_asset_path(img.attrib['src'])
        
        # Process links
        for a in root.findall('.//a'):
            if 'href' in a.attrib:
                a.attrib['href'] = self._adjust_link_path(a.attrib['href'])
        
        return root
    
    def _adjust_asset_path(self, src):
        """
        Adjust the path of an asset (like an image) to work in the final site.
        """
        # Skip URLs that are already absolute
        if src.startswith(('http://', 'https://', '/')):
            return src
            
        # Handle relative paths
        item_dir = os.path.dirname(self.item_path)
        asset_abs_path = os.path.normpath(os.path.join(item_dir, src))
        
        # Determine the path relative to the content directory
        content_dir = os.path.dirname(os.path.dirname(item_dir))
        if asset_abs_path.startswith(content_dir):
            rel_path = os.path.relpath(asset_abs_path, content_dir)
            # Convert to URL path with forward slashes
            url_path = '/assets/' + rel_path.replace('\\', '/')
            return url_path
        
        # If we can't determine a proper path, return the original
        return src
    
    def _adjust_link_path(self, href):
        """
        Adjust the path of a link to work in the final site.
        """
        # Skip URLs that are already absolute or anchors
        if href.startswith(('http://', 'https://', '/', '#', 'mailto:')):
            return href
            
        # Handle relative paths to Markdown files
        item_dir = os.path.dirname(self.item_path)
        link_abs_path = os.path.normpath(os.path.join(item_dir, href))
        
        # If it's a Markdown file, convert to the corresponding HTML path
        if link_abs_path.endswith('.md'):
            # Determine the path relative to the content directory
            content_dir = os.path.dirname(os.path.dirname(item_dir))
            if link_abs_path.startswith(content_dir):
                rel_path = os.path.relpath(link_abs_path, content_dir)
                # Remove .md extension and add .html
                base_path = os.path.splitext(rel_path)[0]
                url_path = '/' + base_path.replace('\\', '/') + '.html'
                return url_path
        
        # If it's another type of file, treat it as an asset
        return self._adjust_asset_path(href)


class AssetExtension(Extension):
    """
    Markdown extension that adjusts image and link paths.
    """
    def __init__(self, item_path, output_path, base_url):
        super().__init__()
        self.item_path = item_path
        self.output_path = output_path
        self.base_url = base_url
        
    def extendMarkdown(self, md):
        md.treeprocessors.register(
            AssetProcessor(md, self.item_path, self.output_path, self.base_url),
            'asset_processor',
            175  # Priority: after 'inline' (150) but before 'prettify' (200)
        )


def parse_markdown_file(filepath, output_path=None, base_url=None, context=None):
    """
    Parses a Markdown file, extracting front matter and converting content.
    Also processes links and assets to work correctly in the final site.
    
    Args:
        filepath: Path to the Markdown file
        output_path: Path where the HTML will be output (for link adjustment)
        base_url: Base URL of the site (for link adjustment)
        context: Context dictionary for shortcode processing
        
    Returns:
        dict: Dictionary with metadata, HTML content, filepath, and slug
    """
    try:
        post = frontmatter.load(filepath)
        
        # Get the content
        content = post.content
        
        # Convert Markdown to HTML with asset processing and shortcode processing
        html_content = convert_markdown_to_html(content, filepath, output_path, base_url, context)
        
        # Ensure date is a Python date object if present
        if 'date' in post.metadata and not isinstance(post.metadata['date'], datetime.date):
           try:
               # Handle both date and datetime strings
               date_str = str(post.metadata['date'])
               if ' ' in date_str:  # Likely datetime
                    parsed_date = datetime.datetime.strptime(date_str.split(' ')[0], '%Y-%m-%d').date()
               else:  # Likely date only
                    parsed_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
               post.metadata['date'] = parsed_date
           except (ValueError, TypeError):
               print(f"Warning: Could not parse date '{post.metadata.get('date')}' in {filepath}. Expected YYYY-MM-DD.")
               post.metadata['date'] = None

        return {
            "metadata": post.metadata,
            "content_html": html_content,
            "filepath": filepath,
            "slug": os.path.splitext(os.path.basename(filepath))[0]  # Use filename (without ext) as slug
        }
    except Exception as e:
        print(f"Error parsing Markdown file {filepath}: {e}")
        return None


def parse_markdown_content(content, source_path=None, output_path=None, base_url=None):
    """
    Parses Markdown content from a string, extracting front matter and converting content.
    Also processes links and assets if source_path is provided.
    
    Args:
        content: Markdown content string
        source_path: Path to the source file (for link adjustment)
        output_path: Path where the HTML will be output (for link adjustment)
        base_url: Base URL of the site (for link adjustment)
        
    Returns:
        dict: Dictionary with metadata and HTML content
    """
    try:
        # Parse frontmatter
        if content.startswith('---'):
            post = frontmatter.loads(content)
            metadata = post.metadata
            content = post.content
        else:
            metadata = {}
        
        # Convert Markdown to HTML with asset processing
        html_content = convert_markdown_to_html(content, source_path, output_path, base_url)
        
        return {
            "metadata": metadata,
            "content_html": html_content
        }
    except Exception as e:
        print(f"Error parsing Markdown content: {e}")
        return None


def process_nav_content(content):
    """
    Pre-process navigation content before Markdown conversion.
    This function extracts the nav content, processes the Markdown list separately,
    and then reinserts it as proper HTML.
    
    Args:
        content: Markdown content string
        
    Returns:
        str: Processed content with navigation lists handled
    """
    # Find nav tags with Markdown lists inside
    nav_pattern = r'(<nav\s+class="[^"]+"\s*>)(.*?)(</nav>)'
    
    def nav_replacement(match):
        nav_open = match.group(1)
        nav_content = match.group(2)
        nav_close = match.group(3)
        
        # Process the nav content as Markdown to get a proper list
        if '*' in nav_content:  # Only process if it contains list items
            # Convert Markdown list to HTML
            list_html = markdown.markdown(nav_content)
            # Make sure we have a proper ul structure
            if '<ul>' not in list_html:
                list_html = f'<ul>{list_html}</ul>'
            return f'{nav_open}{list_html}{nav_close}'
        
        return match.group(0)  # Return unchanged if no list items
    
    # Process nav tags
    return re.sub(nav_pattern, nav_replacement, content, flags=re.DOTALL)


def convert_markdown_to_html(content, source_path=None, output_path=None, base_url=None, context=None):
    """
    Converts Markdown content to HTML with optional asset processing and shortcode processing.
    
    Args:
        content: Markdown content string
        source_path: Path to the source file (for link adjustment)
        output_path: Path where the HTML will be output (for link adjustment)
        base_url: Base URL of the site (for link adjustment)
        context: Context dictionary for shortcode processing
        
    Returns:
        str: HTML content
    """
    # Pre-process content to handle navigation lists
    content = process_nav_content(content)
    
    extensions = [
        'fenced_code',  # Support ```code``` blocks
        'codehilite',   # Add syntax highlighting classes
        'tables',       # Support Markdown tables
        'toc',          # Table of contents
        'nl2br',        # Convert newlines to <br>
        'extra'         # Includes many common extensions
    ]
    
    # Add asset processing if source_path is provided
    if source_path:
        asset_ext = AssetExtension(source_path, output_path, base_url)
        extensions.append(asset_ext)
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(content, extensions=extensions)
    
    # Process shortcodes if context is provided
    if context:
        html_content = process_shortcodes(html_content, context)
    
    return html_content


def copy_content_assets(config):
    """
    Copy assets from content directory to output directory.
    This ensures that images and other assets referenced in Markdown files
    are available in the built site.
    
    Args:
        config: Configuration module with CONTENT_DIR and OUTPUT_DIR defined
    """
    assets_dir = os.path.join(config.CONTENT_DIR, 'assets')
    output_assets_dir = os.path.join(config.OUTPUT_DIR, 'assets')
    
    # Skip if there's no assets directory
    if not os.path.isdir(assets_dir):
        return
    
    print(f"Copying content assets from {assets_dir} to {output_assets_dir}")
    try:
        os.makedirs(output_assets_dir, exist_ok=True)
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                # Skip hidden files
                if file.startswith('.'):
                    continue
                    
                # Get the relative path from the assets directory
                rel_path = os.path.relpath(os.path.join(root, file), assets_dir)
                src_path = os.path.join(assets_dir, rel_path)
                dst_path = os.path.join(output_assets_dir, rel_path)
                
                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy the file
                try:
                    import shutil
                    shutil.copy2(src_path, dst_path)
                except Exception as e:
                    print(f"Error copying asset {src_path}: {e}")
    except Exception as e:
        print(f"Error copying content assets: {e}")
