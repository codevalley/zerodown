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
from zerodown.console import zconsole, ZerodownConsole


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
    init_parser.add_argument(
        '--config-format', choices=['yaml', 'py'], default='yaml',
        help='Format for the configuration file (default: yaml)'
    )
    
    # Add verbosity control to init command
    init_parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='Increase output verbosity (can be used multiple times)'
    )
    init_parser.add_argument(
        '-q', '--quiet', action='store_true',
        help='Suppress all output except errors'
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
    
    # Add verbosity control to build command
    build_parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='Increase output verbosity (can be used multiple times)'
    )
    build_parser.add_argument(
        '-q', '--quiet', action='store_true',
        help='Suppress all output except errors'
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
    
    # Add verbosity control to serve command
    serve_parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='Increase output verbosity (can be used multiple times)'
    )
    serve_parser.add_argument(
        '-q', '--quiet', action='store_true',
        help='Suppress all output except errors'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set verbosity level based on arguments
    if args.quiet:
        verbosity = ZerodownConsole.QUIET
    else:
        # Map the verbosity count to our levels
        verbosity_map = {
            0: ZerodownConsole.MINIMAL,  # Default
            1: ZerodownConsole.NORMAL,   # -v
            2: ZerodownConsole.VERBOSE   # -vv
        }
        # Get the verbosity level, capped at VERBOSE
        verbosity = verbosity_map.get(min(args.verbose, 2), ZerodownConsole.VERBOSE)
    
    # Update the global console instance with the selected verbosity
    zconsole.verbosity = verbosity
    
    # Show header based on verbosity
    if verbosity >= ZerodownConsole.MINIMAL:
        zconsole.header(f"Zerodown v{__version__}")
    
    # Handle commands
    if args.command == 'init':
        init_site(args.path, args.template, args.config_format)
    elif args.command == 'build':
        # Get absolute paths before changing directory
        site_path = os.path.abspath(args.path)
        config_path = args.config
        if not os.path.isabs(config_path):
            config_path = os.path.join(site_path, config_path)
        
        # Change to the specified directory
        original_dir = os.getcwd()
        os.chdir(site_path)
        
        try:
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


def init_site(path, template, config_format='yaml'):
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
        zconsole.error(f"Template '{template}' not found")
        sys.exit(1)
    
    # Create the target directory if it doesn't exist
    target_dir = Path(path)
    if target_dir.exists() and any(target_dir.iterdir()):
        zconsole.error(f"Directory '{path}' already exists and is not empty")
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
        if config_format == 'yaml':
            config_path = target_dir / 'config.yaml'
        else:
            config_path = target_dir / 'config.py'
            
        if not config_path.exists():
            create_default_config(str(config_path))
        
        zconsole.success(f"Initialized new Zerodown site at: {path}")
        zconsole.info("To build the site, run: zerodown build")
    except Exception as e:
        zconsole.error(f"Failed to initialize site: {e}")
        sys.exit(1)


def serve_site(port, config_path, site_path='.'):
    """
    Serve the site locally.
    
    Args:
        port: Port to serve on
        config_path: Path to the configuration file
        site_path: Path to the site directory
    """
    # Get absolute paths before changing directory
    site_path_abs = os.path.abspath(site_path)
    config_path_abs = config_path
    if not os.path.isabs(config_path_abs):
        config_path_abs = os.path.join(site_path_abs, config_path)
    
    # Change to the specified directory
    original_dir = os.getcwd()
    os.chdir(site_path_abs)
    
    try:
        # First build the site
        config = load_config(config_path_abs)
        build_site(config)
        
        # Then serve it
        import http.server
        import socketserver
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=config.OUTPUT_DIR, **kwargs)
        
        with socketserver.TCPServer(("", port), Handler) as httpd:
            zconsole.success(f"Serving at http://localhost:{port}")
            zconsole.info("Press Ctrl+C to stop")
            httpd.serve_forever()
    except KeyboardInterrupt:
        zconsole.info("\nServer stopped")
    except Exception as e:
        zconsole.error(f"Failed to start server: {e}")
        sys.exit(1)
    finally:
        # Change back to the original directory
        os.chdir(original_dir)


if __name__ == "__main__":
    main()
