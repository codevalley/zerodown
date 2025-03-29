"""
Command-line interface for Zerodown.
"""

import os
import sys
import argparse
import shutil
from pathlib import Path

from zerodown import __version__
from zerodown.config import load_config, create_default_config
from zerodown.builder import build_site


def main():
    """Main entry point for the Zerodown CLI."""
    parser = argparse.ArgumentParser(
        description="Zerodown - Zero effort markdown website generator"
    )
    
    # Add version argument
    parser.add_argument(
        '--version', action='version', 
        version=f'Zerodown {__version__}'
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # 'init' command
    init_parser = subparsers.add_parser('init', help='Initialize a new Zerodown site')
    init_parser.add_argument('path', help='Path where to create the new site')
    init_parser.add_argument(
        '--template', choices=['basic', 'blog', 'portfolio'], default='basic',
        help='Template to use for the new site (default: basic)'
    )
    
    # 'build' command
    build_parser = subparsers.add_parser('build', help='Build the site')
    build_parser.add_argument(
        'path', nargs='?', default='.',
        help='Path to the site directory (default: current directory)'
    )
    build_parser.add_argument(
        '--config', default='config.py',
        help='Path to the configuration file (default: config.py)'
    )
    
    # 'serve' command
    serve_parser = subparsers.add_parser('serve', help='Serve the site locally')
    serve_parser.add_argument(
        'path', nargs='?', default='.',
        help='Path to the site directory (default: current directory)'
    )
    serve_parser.add_argument(
        '--port', type=int, default=8000,
        help='Port to serve on (default: 8000)'
    )
    serve_parser.add_argument(
        '--config', default='config.py',
        help='Path to the configuration file (default: config.py)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'init':
        init_site(args.path, args.template)
    elif args.command == 'build':
        # Change to the specified directory
        original_dir = os.getcwd()
        os.chdir(args.path)
        
        try:
            config_path = args.config
            if not os.path.isabs(config_path):
                config_path = os.path.join(os.getcwd(), config_path)
                
            config = load_config(config_path)
            build_site(config)
        finally:
            # Change back to the original directory
            os.chdir(original_dir)
    elif args.command == 'serve':
        serve_site(args.port, args.config, args.path)
    else:
        parser.print_help()
        sys.exit(0)


def init_site(path, template):
    """
    Initialize a new Zerodown site.
    
    Args:
        path: Path where to create the new site
        template: Template to use (basic, blog, portfolio)
    """
    # Get the package directory
    package_dir = Path(__file__).parent
    examples_dir = package_dir.parent / 'examples'
    
    # Check if the template exists
    template_dir = examples_dir / template
    if not template_dir.exists():
        print(f"ERROR: Template '{template}' not found")
        sys.exit(1)
    
    # Create the target directory if it doesn't exist
    target_dir = Path(path)
    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"ERROR: Directory '{path}' already exists and is not empty")
        sys.exit(1)
    
    target_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Copy template files
        for item in template_dir.glob('**/*'):
            if item.is_file():
                relative_path = item.relative_to(template_dir)
                target_path = target_dir / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_path)
        
        # Create default config if it doesn't exist
        config_path = target_dir / 'config.py'
        if not config_path.exists():
            create_default_config(str(config_path))
        
        print(f"Initialized new Zerodown site at: {path}")
        print("To build the site, run: zerodown build")
    except Exception as e:
        print(f"ERROR: Failed to initialize site: {e}")
        sys.exit(1)


def serve_site(port, config_path, site_path='.'):
    """
    Serve the site locally.
    
    Args:
        port: Port to serve on
        config_path: Path to the configuration file
        site_path: Path to the site directory
    """
    # Change to the specified directory
    original_dir = os.getcwd()
    os.chdir(site_path)
    
    try:
        # First build the site
        config_path_abs = config_path
        if not os.path.isabs(config_path_abs):
            config_path_abs = os.path.join(os.getcwd(), config_path)
            
        config = load_config(config_path_abs)
        build_site(config)
        
        # Then serve it
        import http.server
        import socketserver
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=config.OUTPUT_DIR, **kwargs)
        
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"Serving at http://localhost:{port}")
            print("Press Ctrl+C to stop")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"ERROR: Failed to start server: {e}")
        sys.exit(1)
    finally:
        # Change back to the original directory
        os.chdir(original_dir)


if __name__ == "__main__":
    main()
