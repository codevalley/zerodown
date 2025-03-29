"""
Template handling for the Zerodown static site generator.
"""

import os
import sys
import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


def setup_jinja_env(config):
    """
    Sets up the Jinja2 templating environment.
    
    Args:
        config: Configuration module with TEMPLATE_DIR defined
        
    Returns:
        Environment: Configured Jinja2 environment
    """
    print(f"Setting up Jinja2 environment for templates in: {config.TEMPLATE_DIR}")
    try:
        env = Environment(
            loader=FileSystemLoader(config.TEMPLATE_DIR),
            autoescape=select_autoescape(['html', 'xml'])
        )
        # Add globals after initialization
        env.globals['config'] = config
        env.globals['now'] = datetime.datetime.now  # Example utility function
        return env
    except Exception as e:
         print(f"Error setting up Jinja2 environment: {e}")
         sys.exit(1)


def render_template(env, template_name, context):
    """
    Renders a Jinja2 template with the given context.
    
    Args:
        env: Jinja2 environment
        template_name: Name of the template to render
        context: Dictionary of variables to pass to the template
        
    Returns:
        str: Rendered HTML content
    """
    try:
        template = env.get_template(template_name)
        return template.render(context)
    except Exception as e:
        print(f"Error rendering template {template_name} with context keys {list(context.keys())}: {e}")
        # In production, might return a generic error page HTML
        return f"<h1>Error rendering template</h1><p>{e}</p>"


def process_includes(config, jinja_env):
    """
    Process Markdown includes for global template context.
    
    Args:
        config: Configuration module with CONTENT_DIR defined
        jinja_env: Jinja2 environment to update with globals
        
    Returns:
        dict: Global context with processed includes
    """
    # Importing here to avoid circular imports
    from zerodown.markdown import parse_markdown_content
    
    global_context = {}  # Dictionary to hold data for all templates
    includes_dir = os.path.join(config.CONTENT_DIR, '_includes')
    
    if os.path.isdir(includes_dir):
        print(f"Processing includes from {includes_dir}")
        for include_file in os.listdir(includes_dir):
            if include_file.endswith('.md') and not include_file.startswith('.'):
                include_path = os.path.join(includes_dir, include_file)
                if os.path.isfile(include_path):
                    try:
                        # Read the file content
                        with open(include_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Parse the content
                        parsed = parse_markdown_content(content, include_path)
                        if parsed:
                            # Add metadata to context with include_ prefix
                            for key, value in parsed['metadata'].items():
                                meta_key = f"include_{os.path.splitext(include_file)[0]}_{key}"
                                global_context[meta_key] = value
                                
                            # Add HTML content
                            context_key = os.path.splitext(include_file)[0] + '_html'
                            global_context[context_key] = parsed['content_html']
                            print(f"Loaded include: {include_file} as {context_key}")
                    except Exception as e:
                        print(f"Error parsing include file {include_path}: {e}")
    else:
        print(f"Includes directory '{includes_dir}' not found, skipping includes.")
    
    # Add includes to Jinja globals
    jinja_env.globals.update(global_context)
    
    return global_context
