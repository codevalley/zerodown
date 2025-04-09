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


def fix_fenced_code_blocks(content):
    """
    Fix common issues with fenced code blocks in Markdown content.
    This is crucial for proper rendering of fenced code blocks.
    
    Args:
        content: Markdown content string
        
    Returns:
        str: Processed Markdown content
    """
    # Standardize line endings first to ensure consistent regex matching
    content = content.replace('\r\n', '\n')
    
    # The problem is often that fenced code blocks need to have:
    # 1. A blank line BEFORE the opening ```
    # 2. A proper newline after the language specifier
    # 3. A proper newline before the closing ```
    # 4. The closing ``` needs to be on its own line
    
    # First, ensure there's a blank line before code blocks if they come after a list item
    # This is important for proper rendering in CommonMark
    content = re.sub(r'(\n\s*\d+\.\s+.*?:)\s*\n\s*(```)', r'\1\n\n\2', content, flags=re.DOTALL)
    
    # Find all fenced code blocks and fix them one by one (non-greedy matching)
    # Using split and join to preserve the non-matching parts exactly as they are
    parts = re.split(r'(```\w*.*?```)', content, flags=re.DOTALL)
    
    for i in range(1, len(parts), 2):  # Process only the code block parts
        code_block = parts[i]
        
        # Fix opening fence to ensure language specifier is followed by a newline
        code_block = re.sub(r'```(\w*)\s*', r'```\1\n', code_block)
        
        # Fix closing fence to ensure it has its own line
        if '```' in code_block[3:]:  # Skip the opening ```
            open_part, close_part = code_block[:3], code_block[3:]
            last_line_pos = close_part.rfind('\n', 0, close_part.rfind('```'))
            
            if last_line_pos != -1:
                # Ensure the closing ``` is on its own line
                close_part_fixed = close_part[:last_line_pos+1] + close_part[last_line_pos+1:].replace('```', '\n```')
                code_block = open_part + close_part_fixed
        
        parts[i] = code_block
    
    # Rejoin all parts
    fixed_content = ''.join(parts)
    
    # Final cleanup to ensure proper spacing around lists and code blocks
    fixed_content = re.sub(r'(\n\s*\d+\.\s+.*?)\n(```)', r'\1\n\n\2', fixed_content)
    
    return fixed_content


def fix_html_code_blocks(html_content):
    """
    Fix any issues with rendered HTML code blocks.
    
    Args:
        html_content: HTML content string
        
    Returns:
        str: Processed HTML content
    """
    # Fix code blocks that have <br> tags inside them from nl2br extension
    # First pattern: <code>code<br>more code</code>
    html_content = re.sub(r'(<code.*?>)(.*?)</code>', 
                         lambda m: m.group(1) + m.group(2).replace('<br />', '\n') + '</code>',
                         html_content, flags=re.DOTALL)
    
    # Second pattern: Detect incorrectly formatted code blocks
    # This looks for text that should be a code block but is rendered as regular text with <br> tags
    pattern = r'<p>(```\w*)<br />(.*?)<br />(```)</p>'
    
    def code_block_fix(match):
        # Extract the parts of the malformed code block
        start = match.group(1)  # Opening fence with optional language
        code = match.group(2)   # Code content
        end = match.group(3)    # Closing fence
        
        # Extract language if present
        lang_match = re.match(r'```(\w+)', start)
        lang = lang_match.group(1) if lang_match else ''
        
        # Format as a proper code block
        # Replace all <br /> tags with newlines
        code = code.replace('<br />', '\n')
        
        # Return a properly formatted code block
        return f'<div class="codehilite"><pre><code class="language-{lang}">{code}</code></pre></div>'
    
    # Apply the fix
    html_content = re.sub(pattern, code_block_fix, html_content, flags=re.DOTALL)
    
    # Third pattern: Fix list items followed by code blocks that got merged
    # For example: <li>Item text:<br />```bash<br />code<br />```</li>
    pattern_list_code = r'<li>(.*?):<br\s*/?>\s*(```\w*)<br\s*/?>(.*?)<br\s*/?>\s*(```)\s*</li>'
    
    def list_code_fix(match):
        # Extract the parts
        item_text = match.group(1)
        fence_open = match.group(2)
        code = match.group(3)
        fence_close = match.group(4)
        
        # Extract language if present
        lang_match = re.match(r'```(\w+)', fence_open)
        lang = lang_match.group(1) if lang_match else ''
        
        # Format properly - close the list item, then add the code block
        code = code.replace('<br />', '\n')
        
        return f'<li>{item_text}:</li></ol><div class="codehilite"><pre><code class="language-{lang}">{code}</code></pre></div><ol>'
    
    # Apply the list item fix
    html_content = re.sub(pattern_list_code, list_code_fix, html_content, flags=re.DOTALL)
    
    # Fourth pattern: Fix ordered list items that got split by a code block
    # First check if we have two consecutive ol tags with only the closing tag between them
    html_content = re.sub(r'</ol>\s*<ol>', '', html_content)
    
    # Fifth pattern: Handle any code blocks that show up as inline code with backticks
    # For example: <p>`bash<br />code<br />`</p>
    inline_code_pattern = r'<p><code>(\w+)<br\s*/?>(.*?)<br\s*/?></code></p>'
    
    def inline_code_fix(match):
        lang = match.group(1)
        code = match.group(2)
        code = code.replace('<br />', '\n')
        
        return f'<div class="codehilite"><pre><code class="language-{lang}">{code}</code></pre></div>'
    
    # Apply the inline code fix
    html_content = re.sub(inline_code_pattern, inline_code_fix, html_content, flags=re.DOTALL)
    
    return html_content


def convert_markdown_to_html(content, source_path=None, output_path=None, base_url=None, context=None):
    """
    Converts Markdown content to HTML with optional asset processing and shortcode processing.
    Special attention is given to properly rendering fenced code blocks.
    
    Args:
        content: Markdown content string
        source_path: Path to the source file (for link adjustment)
        output_path: Path where the HTML will be output (for link adjustment)
        base_url: Base URL of the site (for link adjustment)
        context: Context dictionary for shortcode processing
        
    Returns:
        str: HTML content
    """
    # Pre-process content to fix any fenced code block issues
    # This is critical for proper rendering of code blocks
    content = fix_fenced_code_blocks(content)
    
    # Process shortcodes if context is provided
    if context:
        content = process_shortcodes(content, context)

    # Configure extension settings for optimal code block handling
    extension_configs = {
        'codehilite': {
            'css_class': 'codehilite',
            'linenums': False,
            'guess_lang': True,
            'use_pygments': True
        },
        'fenced_code': {
            'lang_prefix': 'language-'  # Standard prefix for code language
        },
        'markdown.extensions.tables': {},
        'markdown.extensions.toc': {'permalink': False}
    }
    
    # Order matters! Process code blocks before nl2br to avoid breaking them
    extensions = [
        'markdown.extensions.fenced_code',  # Support ```code``` blocks (must come first)
        'markdown.extensions.codehilite',   # Add syntax highlighting classes
        'markdown.extensions.tables',       # Support Markdown tables
        'markdown.extensions.toc',          # Table of contents
        'markdown.extensions.sane_lists',   # Better list handling
        'markdown.extensions.nl2br',        # Convert newlines to <br>
        'markdown.extensions.extra'         # Includes many common extensions
    ]
    
    # Add asset processing if source_path is provided
    if source_path:
        asset_ext = AssetExtension(source_path, output_path, base_url)
        extensions.append(asset_ext)
    
    # Convert Markdown to HTML with proper handling of fenced code blocks
    html_content = markdown.markdown(
        content, 
        extensions=extensions, 
        extension_configs=extension_configs,
        output_format='html5'  # Ensures modern HTML5 output
    )
    
    # Post-process to fix any remaining issues with code blocks
    html_content = fix_html_code_blocks(html_content)
    
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