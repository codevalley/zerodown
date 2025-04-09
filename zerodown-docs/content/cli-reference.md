---
title: "CLI Reference"
description: "Complete documentation for Zerodown's command line interface and interactive shell."
---

# CLI Reference

Zerodown provides a simple but powerful command-line interface (CLI) to handle all aspects of site generation, from initialization to building and serving your site.

## Basic Commands

### Initialize a New Site

```bash
python zd_cli.py init <site_directory> [--template <template_name>]
```

Creates a new Zerodown site with the necessary directory structure and configuration files.

Options:
- `<site_directory>`: The directory where your new site will be created
- `--template <template_name>`: (Optional) The starter template to use (defaults to "basic")

Example:
```bash
python zd_cli.py init my-blog --template blog
```

### Build a Site

```bash
python zd_cli.py build <site_directory>
```

Builds a static site from your Markdown content.

Options:
- `<site_directory>`: The directory containing your Zerodown site
- `--output <directory>`: (Optional) Override the output directory
- `--clean`: (Optional) Clean the output directory before building

Example:
```bash
python zd_cli.py build my-blog --clean
```

### Serve a Site

```bash
python zd_cli.py serve <site_directory> [--port <port_number>]
```

Launches a local development server for previewing your site.

Options:
- `<site_directory>`: The directory containing your Zerodown site
- `--port <port_number>`: (Optional) The port to serve the site on (default: 8000)

Example:
```bash
python zd_cli.py serve my-blog --port 8080
```

## Interactive Shell

Zerodown also provides an interactive shell for more direct management of your site:

```bash
python zd_cli.py shell <site_directory>
```

In the interactive shell, you can use the following commands:

### Shell Commands

- `build`: Build the site
- `serve [port]`: Start the development server
- `watch`: Watch for file changes and rebuild automatically
- `config show`: Display current configuration
- `config set <key> <value>`: Modify a configuration value
- `exit` or `quit`: Exit the shell

Example shell session:
```
$ python zd_cli.py shell my-blog
Zerodown Interactive Shell
Type 'help' for a list of commands

zd> watch
Watching for changes... Press Ctrl+C to stop

[file changed] content/posts/my-first-post.md
Rebuilding site...
Site built successfully!

zd> config show
site_name: My Blog
site_description: A blog built with Zerodown
...

zd> exit
```

## Environment Variables

Zerodown respects the following environment variables:

- `ZERODOWN_CONFIG_PATH`: Path to a global config file
- `ZERODOWN_TEMPLATE_DIR`: Directory containing custom templates
- `ZERODOWN_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

## Additional Resources

- [Configuration Reference](/configuration.html): Detailed documentation of configuration options
- [Project Structure](/content-structure.html): Learn about the expected file structure
