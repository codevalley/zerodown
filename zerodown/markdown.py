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
        Also handles image dimensions specified in Markdown.
        """
        # Process images
        for img in root.findall('.//img'):
            if 'src' in img.attrib:
                # Check for dimensions in the alt text (format: alt {width=300 height=200})
                if 'alt' in img.attrib:
                    alt_text = img.attrib['alt']
                    # Look for dimension specifications
                    dimensions_match = re.search(r'\{\s*(?:width=(\d+))?\s*(?:height=(\d+))?\s*\}', alt_text)
                    if dimensions_match:
                        # Extract dimensions
                        width, height = dimensions_match.groups()
                        # Remove the dimensions from alt text
                        clean_alt = re.sub(r'\{\s*(?:width=\d+)?\s*(?:height=\d+)?\s*\}', '', alt_text).strip()
                        img.attrib['alt'] = clean_alt
                        
                        # Set width and height attributes if specified
                        if width:
                            img.attrib['width'] = width
                        if height:
                            img.attrib['height'] = height
                
                # Adjust the image path
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
            # Ensure we handle cases where item_path might be directly in content_dir
            try:
                content_dir = config.CONTENT_DIR # Assuming config is accessible or find root differently
            except NameError:
                 # Fallback logic if config isn't directly available
                 # This part might need refinement depending on context access
                 parts = Path(self.item_path).parts
                 try:
                     content_index = parts.index('content')
                     content_dir = os.path.join(*parts[:content_index+1])
                 except ValueError:
                     content_dir = os.path.dirname(self.item_path) # Best guess

            if link_abs_path.startswith(content_dir):
                rel_path = os.path.relpath(link_abs_path, content_dir)
                # Remove .md extension and add .html
                base_path = os.path.splitext(rel_path)[0]
                url_path = '/' + base_path.replace('\\', '/') + '.html'
                # Ensure leading slash is present
                if not url_path.startswith('/'):
                    url_path = '/' + url_path
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
        from zerodown.console import zconsole
        zconsole.error("Error parsing Markdown file", f"{filepath}: {e}")
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
        from zerodown.console import zconsole
        zconsole.error("Error parsing Markdown content", str(e))
        return None


def convert_markdown_to_html(content, source_path=None, output_path=None, base_url=None, context=None):
    """
    Converts Markdown content to HTML using standard extensions.
    Shortcodes are processed AFTER HTML generation.
    
    Args:
        content: Markdown content string
        source_path: Path to the source file (for link adjustment)
        output_path: Path where the HTML will be output (for link adjustment)
        base_url: Base URL of the site (for link adjustment)
        context: Context dictionary for shortcode processing (passed through)
        
    Returns:
        str: HTML content
    """
    # DO NOT pre-process code blocks - let the markdown processor handle them directly
    # This prevents issues with nesting and content being treated as code blocks
    
    # Standard and reliable set of extensions
    extensions = [
        'markdown.extensions.extra',        # Includes abbr, attr_list, def_list, fenced_code, footnotes, tables, smarty
        'markdown.extensions.codehilite',   # Syntax highlighting
        'markdown.extensions.toc',          # Table of contents
        'markdown.extensions.sane_lists',   # Improved list handling
        # 'markdown.extensions.nl2br',      # Often causes issues, leave out unless needed
    ]
    extension_configs = {
        'markdown.extensions.codehilite': {
            'css_class': 'codehilite',
            'linenums': False,
            'guess_lang': True
        },
        'markdown.extensions.toc': {
            'permalink': False  # Disable permalink symbols that add the ¶ character
        }
    }

    # Add asset processing if source_path is provided
    if source_path:
        asset_ext = AssetExtension(source_path, output_path, base_url)
        extensions.append(asset_ext)

    # Convert Markdown to HTML
    html_content = markdown.markdown(
        content,
        extensions=extensions,
        extension_configs=extension_configs,
        output_format='html5'
    )

    # Process shortcodes AFTER HTML generation if context is provided
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
    
    from zerodown.console import zconsole
    zconsole.info("Copying content assets", f"from {assets_dir} to {output_assets_dir}")
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
                    from zerodown.console import zconsole
                    zconsole.error("Error copying asset", f"{src_path}: {e}")
    except Exception as e:
        from zerodown.console import zconsole
        zconsole.error("Error copying content assets", str(e))