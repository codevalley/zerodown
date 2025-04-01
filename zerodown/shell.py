"""
Interactive shell for Zerodown.

This module provides an interactive command-line interface for Zerodown,
allowing users to enter commands directly in a shell-like environment.
"""

import os
import sys
import cmd
import shlex
import argparse
from pathlib import Path

from zerodown import __version__
from zerodown.config import load_config, create_default_config
from zerodown.builder import build_site
from zerodown.console import zconsole, ZerodownConsole
from zerodown.cli import init_site, serve_site


class ZerodownShell(cmd.Cmd):
    """Interactive shell for Zerodown."""
    
    intro = f"\nWelcome to Zerodown v{__version__} interactive shell!\n" \
            "Type 'help' or '?' to list commands.\n"
    prompt = "zerodown> "
    
    def __init__(self):
        super().__init__()
        self.current_dir = os.getcwd()
        
    def do_init(self, arg):
        """
        Initialize a new Zerodown site.
        
        Usage: init PATH [--template TEMPLATE] [--config-format FORMAT] [-v] [-q]
        
        Arguments:
          PATH                  Path where to create the new site
          
        Options:
          --template TEMPLATE   Template to use (basic, blog, portfolio)
          --config-format FORMAT Format for config file (yaml, py)
          -v, --verbose         Increase output verbosity
          -q, --quiet           Suppress all output except errors
        """
        parser = argparse.ArgumentParser(prog="init", description="Initialize a new Zerodown site")
        parser.add_argument('path', help='Path where to create the new site')
        parser.add_argument(
            '--template', choices=['basic', 'blog', 'portfolio'], default='basic',
            help='Template to use for the new site (default: basic)'
        )
        parser.add_argument(
            '--config-format', choices=['yaml', 'py'], default='yaml',
            help='Format for the configuration file (default: yaml)'
        )
        parser.add_argument(
            '-v', '--verbose', action='count', default=0,
            help='Increase output verbosity (can be used multiple times)'
        )
        parser.add_argument(
            '-q', '--quiet', action='store_true',
            help='Suppress all output except errors'
        )
        
        try:
            args = parser.parse_args(shlex.split(arg))
            self._set_verbosity(args)
            init_site(args.path, args.template, args.config_format)
        except SystemExit:
            # Catch the SystemExit to prevent the shell from exiting
            pass
    
    def do_build(self, arg):
        """
        Build the site.
        
        Usage: build [PATH] [--config CONFIG] [-v] [-q]
        
        Arguments:
          PATH                  Path to the site directory (default: current directory)
          
        Options:
          --config CONFIG       Path to the configuration file (default: config.py)
          -v, --verbose         Increase output verbosity
          -q, --quiet           Suppress all output except errors
        """
        parser = argparse.ArgumentParser(prog="build", description="Build the site")
        parser.add_argument(
            'path', nargs='?', default='.',
            help='Path to the site directory (default: current directory)'
        )
        parser.add_argument(
            '--config', default='config.py',
            help='Path to the configuration file (default: config.py)'
        )
        parser.add_argument(
            '-v', '--verbose', action='count', default=0,
            help='Increase output verbosity (can be used multiple times)'
        )
        parser.add_argument(
            '-q', '--quiet', action='store_true',
            help='Suppress all output except errors'
        )
        
        try:
            args = parser.parse_args(shlex.split(arg))
            self._set_verbosity(args)
            
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
        except SystemExit:
            # Catch the SystemExit to prevent the shell from exiting
            pass
    
    def do_serve(self, arg):
        """
        Serve the site locally.
        
        Usage: serve [PATH] [--port PORT] [--config CONFIG] [-v] [-q]
        
        Arguments:
          PATH                  Path to the site directory (default: current directory)
          
        Options:
          --port PORT           Port to serve on (default: 8000)
          --config CONFIG       Path to the configuration file (default: config.py)
          -v, --verbose         Increase output verbosity
          -q, --quiet           Suppress all output except errors
        """
        parser = argparse.ArgumentParser(prog="serve", description="Serve the site locally")
        parser.add_argument(
            'path', nargs='?', default='.',
            help='Path to the site directory (default: current directory)'
        )
        parser.add_argument(
            '--port', type=int, default=8000,
            help='Port to serve on (default: 8000)'
        )
        parser.add_argument(
            '--config', default='config.py',
            help='Path to the configuration file (default: config.py)'
        )
        parser.add_argument(
            '-v', '--verbose', action='count', default=0,
            help='Increase output verbosity (can be used multiple times)'
        )
        parser.add_argument(
            '-q', '--quiet', action='store_true',
            help='Suppress all output except errors'
        )
        
        try:
            args = parser.parse_args(shlex.split(arg))
            self._set_verbosity(args)
            serve_site(args.port, args.config, args.path)
        except SystemExit:
            # Catch the SystemExit to prevent the shell from exiting
            pass
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nServer stopped")
    
    def do_cd(self, arg):
        """
        Change the current working directory.
        
        Usage: cd [PATH]
        
        Arguments:
          PATH                  Directory to change to (default: home directory)
        """
        if not arg:
            # Default to home directory if no path is provided
            arg = str(Path.home())
        
        try:
            os.chdir(os.path.expanduser(arg))
            self.current_dir = os.getcwd()
            print(f"Changed directory to: {self.current_dir}")
        except FileNotFoundError:
            print(f"Directory not found: {arg}")
        except PermissionError:
            print(f"Permission denied: {arg}")
    
    def do_pwd(self, arg):
        """
        Print the current working directory.
        
        Usage: pwd
        """
        print(self.current_dir)
    
    def do_ls(self, arg):
        """
        List directory contents.
        
        Usage: ls [PATH]
        
        Arguments:
          PATH                  Directory to list (default: current directory)
        """
        path = arg or '.'
        try:
            for item in os.listdir(path):
                if os.path.isdir(os.path.join(path, item)):
                    print(f"[DIR] {item}")
                else:
                    print(f"      {item}")
        except FileNotFoundError:
            print(f"Directory not found: {path}")
        except PermissionError:
            print(f"Permission denied: {path}")
    
    def do_exit(self, arg):
        """
        Exit the Zerodown shell.
        
        Usage: exit
        """
        print("Goodbye!")
        return True
    
    def do_quit(self, arg):
        """
        Exit the Zerodown shell.
        
        Usage: quit
        """
        return self.do_exit(arg)
    
    def do_version(self, arg):
        """
        Display the Zerodown version.
        
        Usage: version
        """
        print(f"Zerodown v{__version__}")
    
    def emptyline(self):
        """Do nothing on empty line."""
        pass
    
    def default(self, line):
        """Handle unknown commands."""
        print(f"Unknown command: {line}")
        print("Type 'help' or '?' to list available commands.")
    
    def _set_verbosity(self, args):
        """Set the verbosity level based on arguments."""
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


def main():
    """Start the interactive shell."""
    # Display a welcome header
    zconsole.header(f"Zerodown v{__version__} Interactive Shell")
    
    # Start the shell
    ZerodownShell().cmdloop()


if __name__ == "__main__":
    main()
