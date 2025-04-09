---
title: "Getting Started"
description: "Install Zerodown and create your first site."
---

# Getting Started

Welcome to Zerodown! This guide will walk you through installing Zerodown and creating your first static site.

## Prerequisites

Before you begin, ensure you have the following installed:

*   🐍 **Python 3.7** or higher
*   📦 **Pip** (Python's package installer, usually included with Python)

We recommend using a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html) to manage dependencies for your project.

## Installation

You can install Zerodown directly from source using pip.

1.  **Clone the repository** (replace `yourusername/zerodown.git` with the actual repository URL if needed):
```bash
    git clone https://github.com/yourusername/zerodown.git
    cd zerodown
```

2.  **Install the package** in editable mode (`-e`) along with its dependencies:
```bash
    # Make sure you are in the 'zerodown' directory cloned above
    pip install -e .
```
    This makes the `zerodown` command available in your environment.

## Creating Your Site

The easiest way to start is using the `init` command.

1.  **Initialize a new site**:
    Choose a template (`basic`, `blog`, `portfolio`). This command creates a new directory with the template files and a default `config.yaml`.
    
```bash
    # Create a site named 'my-awesome-site' using the basic template
    zerodown init my-awesome-site --template basic

    # Or create a blog
    # zerodown init my-blog --template blog
```

2.  **Navigate to your site directory**:
```bash
    cd my-awesome-site
```

3.  **Add Content**:
    Place your Markdown files (`.md`) inside the `content/` directory. You can create subdirectories for organization (e.g., `content/posts/`, `content/projects/`). See the [Content Structure](content-structure.html) page for more details.

## Building Your Site

Once you have added content, build the static HTML files:

```bash
# Run from within your site directory ('my-awesome-site')
zerodown build
```

Or, if you haven't installed Zerodown globally, run from the main Zerodown source directory:
```bash
# Run from the main Zerodown project directory
python zd_cli.py build path/to/my-awesome-site
```

This generates the final site in the `_site/` directory (or the directory specified by `output_dir` in your config).

## Previewing Locally

To see your site before deploying, use the `serve` command:

```bash
# Run from within your site directory ('my-awesome-site')
zerodown serve
```

Or, from the main Zerodown source directory:
```bash
# Run from the main Zerodown project directory
python zd_cli.py serve path/to/my-awesome-site
```

This starts a local web server (usually at `http://localhost:8000`). Open that address in your browser. The server automatically rebuilds the site when it detects changes to your content or templates.
