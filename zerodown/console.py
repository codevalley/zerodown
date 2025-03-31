"""
Rich console interface for Zerodown.

This module provides styled, colorful terminal output for Zerodown using the rich library.
"""

import sys
import time
from typing import Optional, List, Dict, Any, Union

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.tree import Tree
from rich.live import Live
from rich.align import Align
from rich.text import Text

# Create console instance
console = Console()

# Create a separate error console that writes to stderr
error_console = Console(stderr=True, style="bold red")

class ZerodownConsole:
    """Handles rich console output for Zerodown."""
    
    def __init__(self):
        self.console = console
        self.error_console = error_console
        self._progress = None
        self._live = None
        self._task_ids = {}
        
    def header(self, title: str):
        """Display a styled header."""
        self.console.print()
        self.console.print(Panel(
            Align.center(f"[bold blue]{title}[/]"),
            border_style="blue",
            expand=False
        ))
        
    def subheader(self, text: str):
        """Display a styled subheader."""
        self.console.print(f"\n[bold cyan]{text}[/]")
        
    def print(self, message: str, style: str = None):
        """Print a message with optional styling."""
        if style:
            self.console.print(f"[{style}]{message}[/]")
        else:
            self.console.print(message)
            
    def info(self, message: str):
        """Display an info message."""
        self.console.print(f"[cyan]ℹ[/] {message}")
        
    def success(self, message: str):
        """Display a success message."""
        self.console.print(f"[green]✓[/] {message}")
        
    def warning(self, message: str):
        """Display a warning message."""
        self.console.print(f"[yellow]⚠[/] {message}")
        
    def error(self, message: str):
        """Display an error message."""
        self.error_console.print(f"[bold red]✗ ERROR:[/] {message}")
        
    def start_progress(self, description: str = "Building site"):
        """Start a progress display."""
        if self._progress is not None:
            self._progress.stop()
            
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[cyan]{task.fields[status]}"),
            TimeElapsedColumn(),
            console=self.console,
            expand=True
        )
        
        self._live = Live(self._progress, console=self.console, refresh_per_second=10)
        self._live.start()
        
        # Create a main task
        self._task_ids["main"] = self._progress.add_task(description, total=None, status="Starting...")
        return self._task_ids["main"]
        
    def update_progress(self, task_id, status: str, advance: float = 0):
        """Update a progress task."""
        if self._progress:
            self._progress.update(task_id, advance=advance, status=status)
            
    def add_subtask(self, description: str, parent_id=None, total: float = 100):
        """Add a subtask to the progress."""
        if self._progress:
            task_id = self._progress.add_task(description, total=total, status="Waiting...")
            self._task_ids[description] = task_id
            return task_id
        return None
            
    def stop_progress(self):
        """Stop the progress display."""
        if self._live:
            self._live.stop()
            self._live = None
            self._progress = None
            self._task_ids = {}
            
    def display_summary(self, stats: Dict[str, Any]):
        """Display a summary table of build statistics."""
        table = Table(title="Build Summary", show_header=True, header_style="bold blue")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in stats.items():
            table.add_row(key, str(value))
            
        self.console.print(table)
        
    def display_file_tree(self, title: str, root_dir: str, files: List[str]):
        """Display a tree of files."""
        tree = Tree(f"[bold blue]{title}[/]")
        
        # Group files by directory
        dirs = {}
        for file in files:
            parts = file.split('/')
            if len(parts) > 1:
                dir_path = '/'.join(parts[:-1])
                filename = parts[-1]
                if dir_path not in dirs:
                    dirs[dir_path] = []
                dirs[dir_path].append(filename)
            else:
                if '.' not in dirs:
                    dirs['.'] = []
                dirs['.'].append(file)
                
        # Add to tree
        for dir_path, filenames in dirs.items():
            dir_node = tree.add(f"[bold cyan]{dir_path}[/]")
            for filename in filenames:
                dir_node.add(f"[green]{filename}[/]")
                
        self.console.print(tree)
        
    def display_code(self, code: str, language: str = "python"):
        """Display syntax-highlighted code."""
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        self.console.print(syntax)
        
    def display_markdown(self, md_text: str):
        """Display rendered markdown."""
        markdown = Markdown(md_text)
        self.console.print(markdown)
        
    def clear(self):
        """Clear the console."""
        self.console.clear()


# Create a global console instance
zconsole = ZerodownConsole()
