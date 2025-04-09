---
title: "Setting Up"
description: "Guide to configuring, theming, and deploying your Zerodown site."
---

# Setting Up Your Zerodown Site

This guide covers everything you need to set up and customize your Zerodown site, from configuration to deployment.

## Configuration

Zerodown uses a simple configuration file that controls how your site is built, which templates are used, and where files are stored.

### Configuration File

By default, Zerodown looks for a file named `config.yaml` in your site's root directory. Here's a typical configuration file with all available options:

```yaml
# Basic site information
site_name: "My Zerodown Site"
site_description: "A site built with Zerodown"
base_url: /                  # Base URL for production deployment

# Directory paths (relative to config file)
content_dir: content         # Where your markdown files live
template_dir: templates      # Where your HTML templates live
styles_dir: styles           # Where your CSS files live
output_dir: _site            # Where the generated site will be output

# Theme settings
theme_css_file: pico.min.css # Main CSS theme file
additional_css_files:        # Additional CSS files to include
  - custom.css
  - syntax.css

# Navigation items (rendered in the header)
nav_items:
  - title: Home
    url: /
  - title: About
    url: /about.html
  - title: Blog
    url: /blog/

# Content sections (optional)
sections:
  blog:
    title: Blog
    template: blog_post.html    # Template for individual posts
    list_template: blog_list.html # Template for the list page
    sort_by: date               # Sort by which front matter field
    sort_reverse: true          # Newest first

# Markdown processing options
markdown_extensions:          # Extensions for Python-Markdown
  - codehilite
  - fenced_code
  - toc
  - admonition

# Advanced options
permalink_style: /:title.html # How URLs are generated
date_format: "%B %d, %Y"      # Date format for templates
timezone: UTC                 # Timezone for date handling
```

### Configuration Options

#### Basic Information

- `site_name`: The name of your site (used in templates and metadata)
- `site_description`: A brief description of your site (used in metadata)
- `base_url`: The base URL where your site will be deployed (e.g., "/" or "/blog/")

#### Directory Paths

- `content_dir`: Directory containing your Markdown content files
- `template_dir`: Directory containing your HTML templates
- `styles_dir`: Directory containing your CSS files
- `output_dir`: Directory where the generated site will be output
- `assets_dir`: (Optional) Directory for static assets like images and downloads

#### Navigation

- `nav_items`: List of navigation items to display in your site's header
  - Each item needs a `title` and `url`
  - Optional `target: _blank` for external links

#### Content Sections

Sections allow you to organize content into categories with specific templates:

```yaml
sections:
  blog:
    title: Blog Posts
    template: blog_post.html
    list_template: blog_list.html
    sort_by: date
    sort_reverse: true
    path: blog/           # Custom path for this section
    index_page: true      # Generate an index page for this section
```

#### Markdown Processing

- `markdown_extensions`: List of Python-Markdown extensions to enable
- `markdown_extension_configs`: Configuration for specific extensions

#### Advanced Options

- `permalink_style`: Pattern for generating URLs
- `date_format`: Default date format for templates
- `timezone`: Timezone for date handling

### Python Configuration

Instead of YAML, you can also use a Python file (`config.py`) for more dynamic configuration:

```python
# config.py
import os
from datetime import datetime

# Basic site info
site_name = "My Zerodown Site"
site_description = "A site built with Zerodown"

# Dynamic configuration based on environment
if os.environ.get("PRODUCTION"):
    base_url = "https://mysite.com/"
else:
    base_url = "/"

# Dynamic navigation
nav_items = [
    {"title": "Home", "url": "/"},
    {"title": "About", "url": "/about.html"},
]

# Add blog section only if blog posts exist
if os.path.exists("content/blog"):
    nav_items.append({"title": "Blog", "url": "/blog/"})

# Dynamic copyright year
def copyright_year():
    return datetime.now().year
```

### Environment Variables

Configuration values can be overridden with environment variables prefixed with `ZERODOWN_`:

- `ZERODOWN_SITE_NAME`: Override site_name
- `ZERODOWN_OUTPUT_DIR`: Override output_dir
- `ZERODOWN_BASE_URL`: Override base_url

## Theming

Zerodown makes it easy to customize the appearance of your site using CSS.

### Default Theme: Pico.css

By default, Zerodown uses [Pico.css](https://picocss.com/), a minimal CSS framework that provides beautiful, semantic styling with minimal effort.

Pico.css follows these principles:
- **Semantic:** Works with standard HTML elements, no need for custom classes
- **Responsive:** Adapts to all screen sizes
- **Lightweight:** Minimal footprint at under 10KB
- **No JavaScript:** Pure CSS for maximum simplicity

### Customizing the Theme

To customize your site's appearance:

1. **Include Pico.css:** Make sure your `config.yaml` has:
   ```yaml
   theme_css_file: pico.min.css
   ```

2. **Create a custom CSS file:** Add your custom styles in `styles/custom.css` and reference it in `config.yaml`:
   ```yaml
   additional_css_files:
     - custom.css
   ```

3. **Use CSS variables:** Override Pico's CSS variables for easy customization:
   ```css
   /* Change the primary color */
   :root {
     --primary: #8e24aa;
     --primary-hover: #7b1fa2;
   }
   
   /* Customize fonts */
   :root {
     --font-family: 'Source Sans Pro', sans-serif;
     --font-size: 16px;
   }
   ```

### Light and Dark Modes

Pico.css supports both light and dark modes. To enable this:

1. Add `data-theme="light"` or `data-theme="dark"` to your HTML tag, or
2. Use `<meta name="color-scheme" content="light dark">` to respect system preferences

### Custom Layouts

For more advanced customization, you can:

1. Create custom templates in your `templates/` directory
2. Override blocks in the base template
3. Create section-specific templates

## Deployment

Once you've built your Zerodown site, you can deploy it to various hosting platforms.

### Building for Production

Before deploying, build your site with production settings:

```bash
# Set the base URL for production (if different)
export ZERODOWN_BASE_URL="https://mysite.com/"

# Build the site
python zd_cli.py build my-site --clean
```

Your built site will be in the `_site` directory (or whatever you've set as `output_dir`).

### Deployment Options

#### GitHub Pages

To deploy to GitHub Pages:

1. Build your site with `base_url` set to your GitHub Pages URL:
   ```yaml
   base_url: /your-repo-name/
   ```

2. Push the contents of your `_site` directory to the `gh-pages` branch:
   ```bash
   cd _site
   git init
   git add .
   git commit -m "Deploy to GitHub Pages"
   git remote add origin https://github.com/username/your-repo-name.git
   git push -f origin master:gh-pages
   ```

#### Netlify

To deploy to Netlify:

1. Connect your GitHub repository to Netlify
2. Set the build command: `python zd_cli.py build .`
3. Set the publish directory: `_site`

#### Vercel

To deploy to Vercel:

1. Create a `vercel.json` file:
   ```json
   {
     "builds": [
       { "src": "_site/**", "use": "@vercel/static" }
     ],
     "routes": [
       { "src": "/(.*)", "dest": "_site/$1" }
     ]
   }
   ```

2. Connect your GitHub repository to Vercel

#### Simple Hosting

For simpler hosting solutions (shared hosting, VPS):

1. Upload the contents of the `_site` directory to your web server.
2. Ensure your server is configured to serve the static files correctly.

### Custom Domains

If you're using a custom domain:

1. Update the `base_url` in your configuration:
   ```yaml
   base_url: https://mysite.com/
   ```

2. Set up DNS records pointing to your hosting provider
3. Configure SSL certificates for HTTPS (Let's Encrypt is a free option)
