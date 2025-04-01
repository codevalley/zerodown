<div align="center">

# ⚡ Zerodown ⚡

*Zero effort, maximum markdown power!*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

</div>

## 🚀 What is Zerodown?

Zerodown is a lightning-fast, zero-configuration static site generator that transforms your Markdown content into beautiful, fast-loading websites. Perfect for personal blogs, portfolios, and documentation sites—without the headache!

## ✨ Features

- 📝 **Content-focused**: Write in Markdown, focus on your content
- 🧩 **Modular architecture**: Clean separation of concerns for easy maintenance
- 🔗 **Smart asset handling**: Links and images work correctly in both your editor and the final site
- 🎨 **Theme support**: Easily switch between different CSS themes
- ⚡ **Fast builds**: Efficient processing for quick development cycles
- 🗄️ **No database required**: Everything is stored as files
- 🔌 **Zero configuration**: Works out of the box with sensible defaults
- 🖥️ **Beautiful CLI**: Rich, colorful terminal output with progress tracking
- 🔄 **Interactive Shell**: Command-line shell for streamlined workflow

## 🚀 Getting Started

### Prerequisites

- 🐍 Python 3.7 or higher
- 📦 Pip for installing dependencies

### Installation

You can install Zerodown in two ways:

#### Option 1: Install from source

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/zerodown.git
   cd zerodown
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

#### Option 2: Quick start without installing

If you just want to try Zerodown without installing it:

1. Clone the repository as above
2. Run the included script:
   ```bash
   python zd_cli.py
   ```

> 💡 **Pro tip**: Use a virtual environment to keep your dependencies isolated!

### 🏗️ Creating Your Site

#### Using the CLI (Recommended)

1. **Initialize a new site** with one of the example templates:
   ```bash
   # For a blog (creates config.yaml by default)
   zerodown init my-blog --template blog
   
   # For a portfolio
   zerodown init my-portfolio --template portfolio
   
   # For a minimal site
   zerodown init my-site --template basic
   
   # If you prefer Python configuration
   zerodown init my-site --template basic --config-format py
   ```

2. **Configure your site**:
   Edit `config.yaml` (or `config.py` if you chose Python format) in your project directory to set your site title, description, and other settings.

#### Manual Setup

1. **Copy an example template**:
   ```bash
   # For a blog
   cp -r examples/blog my-blog
   
   # For a portfolio
   cp -r examples/portfolio my-portfolio
   
   # For a minimal site
   cp -r examples/basic my-site
   ```

2. **Configure your site**:
   Edit `config.yaml` (or `config.py`) in your project directory to set your site title, description, and other settings.

3. **Add content**:
   - 📄 Place Markdown files in the `content/` directory
   - 📂 Organize content into sections (e.g., `content/notes/`, `content/projects/`)
   - 🧩 Add reusable content fragments in `content/_includes/` (e.g., `bio.md`, `contact-info.md`)
   - 🖼️ Store images and other assets in `content/assets/`
   - 🏠 Create `content/home.md` for your homepage content with shortcodes

4. **Customize templates**:
   - 🖌️ Edit HTML templates in the `templates/` directory
   - 🎨 Create or modify CSS themes in the `styles/` directory

5. **Build your site**:
   ```bash
   # If you installed the package
   zerodown build /path/to/your/site
   
   # Or using the CLI script
   python zd_cli.py build /path/to/your/site
   ```

6. **Preview locally**:
   ```bash
   # If you installed the package
   zerodown serve /path/to/your/site
   
   # Or using the CLI script
   python zd_cli.py serve /path/to/your/site
   ```
   Then visit `http://localhost:8000` in your browser. ✨

## 📂 Content Structure

```
your-site/
├── config.yaml        # Site configuration
├── content/           # All your Markdown content
│   ├── home.md        # Homepage content with shortcodes
│   ├── about.md       # Top-level pages
│   ├── _includes/     # Reusable content fragments
│   │   └── bio.md     # Can be included in other pages with {% include "bio.md" %}
│   ├── assets/        # Images and other files
│   │   └── ...
│   ├── posts/         # Content section (defined in config)
│   │   ├── post1.md   # Individual content items
│   │   └── post2.md
│   └── projects/      # Another content section (defined in config)
│       ├── project1.md # Individual content items
│       └── project2.md
├── templates/         # HTML templates
│   ├── base.html      # Base template with common elements
│   ├── index.html     # Homepage template
│   ├── post.html      # Template for individual posts
│   └── post_list.html # Template for section index pages
├── styles/            # CSS styles
│   └── main.css       # Main stylesheet
└── _site/             # Generated output (created by build)
    ├── index.html     # Generated homepage
    ├── about.html     # Generated top-level pages
    ├── posts/         # Generated section directories
    │   ├── index.html # Section index page
    │   ├── post1.html # Generated content pages
    │   └── post2.md.html
    ├── styles/        # Copied and processed styles
    └── assets/        # Copied assets
```

> 💡 **Tip**: The structure is flexible—organize your content in a way that makes sense for your project!

## 📝 Markdown Features

### 📋 Front Matter

Each Markdown file can include metadata at the top:

```markdown
---
title: "My First Post"
date: 2025-03-29
description: "This is my first post"
featured: true        # Can be used to mark featured content
image: "hero.jpg"     # Featured image for the content
---

# Content starts here
```

### 🔗 Links and Images

You can use standard Markdown syntax for links and images:

```markdown
[Link to another page](another-page.md)
![Image description](../assets/image.png)
```

Zerodown automatically adjusts paths to work correctly in the final site. No more broken links! 🎉

#### 📐 Image Dimensions

You can specify image dimensions directly in your Markdown using a special syntax in the alt text:

```markdown
![Image description {width=300 height=200}](../assets/image.png)
```

This will set the width to 300px and height to 200px in the generated HTML. You can specify either width, height, or both. If dimensions aren't specified, images will be responsively sized with sensible defaults:

- Images will be limited to the content width
- Aspect ratio will be maintained
- Images will be centered in the content area

### 🧩 Shortcodes

Shortcodes allow you to include dynamic content directly in your Markdown files:

```markdown
## Latest Posts
[latest_posts count="3" section="posts"]

## Explore Sections
[section_list]

## Featured Content
[featured_items count="2"]
```

#### Available Shortcodes

- **`[latest_posts]`**: Displays the latest posts from a section
  - `count`: Number of posts to display (default: 3)
  - `section`: Section key to get posts from (default: "posts")

- **`[section_list]`**: Lists all sections or items in a section
  - `section`: Optional section key to list items from

- **`[featured_items]`**: Displays content items marked as featured in their frontmatter
  - `count`: Number of items to display (default: 3)
  - `section`: Optional section key to limit featured items to a specific section

## 🔄 Interactive Shell

Zerodown includes an interactive shell for a more streamlined workflow. This allows you to enter commands directly without having to type the full command each time.

### Starting the Shell

To start the interactive shell, simply run the CLI script without any arguments:

```bash
python zd_cli.py
```

You'll see a welcome message and a prompt where you can enter commands:

```
Zerodown v0.1.0 Interactive Shell

Welcome to Zerodown v0.1.0 interactive shell!
Type 'help' or '?' to list commands.

zerodown> 
```

### Available Commands

The shell supports all the same commands as the regular CLI, plus some additional navigation commands:

- **`build`**: Build your site
  ```
  zerodown> build examples/blog
  zerodown> build --verbose
  ```

- **`init`**: Initialize a new site
  ```
  zerodown> init my-new-site --template blog
  ```

- **`serve`**: Start a local development server
  ```
  zerodown> serve --port 8080
  ```

- **`cd`**: Change directory
  ```
  zerodown> cd examples/blog
  ```

- **`pwd`**: Show current directory
  ```
  zerodown> pwd
  ```

- **`ls`**: List files in current or specified directory
  ```
  zerodown> ls content
  ```

- **`help`**: Show help for a command
  ```
  zerodown> help build
  ```

- **`exit`** or **`quit`**: Exit the shell

### Verbosity Control

All commands support the same verbosity flags as the regular CLI:

- **`-q`**: Quiet mode (errors only)
- **`-v`**: Normal verbosity (detailed information)
- **`-vv`**: Verbose mode (maximum detail)

> 💡 **Philosophy**: Shortcodes keep all content decisions in Markdown files while templates remain purely structural, maintaining a clean separation of concerns.

## 📟 How Zerodown Works

Zerodown follows a clean, modular approach to generate static sites from your Markdown content. Here's how it works:

```
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|  Configuration  +---->+  Content Files +---->+  Templates     |
|  (config.yaml) |     |  (Markdown)    |     |  (HTML/Jinja2) |
|                |     |                |     |                |
+-------+--------+     +--------+-------+     +-------+--------+
        |                       |                     |
        |                       |                     |
        v                       v                     v
+-------+---------------------------------------------+--------+
|                                                              |
|                      Build Process                           |
|                                                              |
|  1. Load configuration                                       |
|  2. Set up template environment                              |
|  3. Process includes and assets                              |
|  4. Process content sections                                 |
|     - Parse Markdown files (with shortcodes)                 |
|     - Build individual pages                                 |
|     - Build section index pages                              |
|  5. Build homepage and top-level pages                       |
|  6. Copy static assets and styles                            |
|                                                              |
+-------------------------------+------------------------------+
                                |
                                |
                                v
                    +-----------+-----------+
                    |                       |
                    |    Generated Site     |
                    |    (_site directory)  |
                    |                       |
                    +-----------------------+
```

### Build Process in Detail

1. **Configuration Loading**:
   - Load settings from `config.yaml` or `config.py`
   - Set up paths, site information, and section definitions

2. **Template Setup**:
   - Initialize Jinja2 environment with the template directory
   - Register custom filters and functions

3. **Content Processing**:
   - Process `_includes` directory for reusable content fragments
   - For each content section defined in the config:
     - Find all Markdown files in the section directory
     - Parse frontmatter metadata
     - Convert Markdown to HTML
     - Process shortcodes (like `[latest_posts]` or `[section_list]`)
     - Apply the appropriate template
     - Generate individual pages and section index pages

4. **Asset Handling**:
   - Copy static assets from `static/` to the output directory
   - Process and copy CSS from `styles/` to the output directory
   - Fix relative paths in links and image sources

5. **Output Generation**:
   - Write all processed files to the `_site/` directory
   - Maintain the directory structure for sections

### Philosophy

Zerodown follows these core principles:

1. **Content/Code Separation**: All content lives in Markdown files, all presentation logic in templates
2. **No Content Opinions in Templates**: Templates should be purely structural with no hardcoded content
3. **Dynamic Content via Shortcodes**: Use shortcodes in Markdown to include dynamic elements
4. **Simplicity First**: Sensible defaults that work out of the box
5. **Flexibility**: Easy to customize for different site types

## 🚀 Deployment

After building your site, the `_site/` directory contains all the files needed for your website. You can deploy these files to any static hosting service:

- 🌐 **GitHub Pages**: Push the `_site/` directory to a GitHub repository
- ⚡ **Netlify**: Connect your repository and set the publish directory to `_site/`
- 🔼 **Vercel**: Similar to Netlify, with automatic deployments
- ☁️ **Amazon S3**: Upload the `_site/` directory to an S3 bucket configured for static website hosting

> 💡 **Pro tip**: Set up a GitHub Action to automatically build and deploy your site whenever you push changes!

## 🛠️ Customization

### 📄 Configuration Options

Zerodown supports two configuration formats:

#### YAML Configuration (Recommended)

YAML configuration is simpler and more user-friendly, perfect for non-technical users:

```yaml
# config.yaml
# Site information
site_name: My Website
site_description: A beautiful static site
base_url: /  # Use "/" for local development, or your domain for production

# Directory paths
content_dir: content
template_dir: templates
styles_dir: styles
static_dir: static
output_dir: _site

# Theme settings
theme_css_file: main.css  # The CSS file to use from the styles directory

# Content sections
sections:
  posts:
    title: Blog Posts
    template: post.html         # Template for individual posts
    list_template: post_list.html  # Template for the section index page
    sort_by: date               # Sort items by this metadata field
    reverse_sort: true          # Sort in reverse order (newest first)

# Navigation items
nav_items:
  - title: Home
    url: /
  - title: Blog
    url: /posts/
  - title: About
    url: /about.html
```

#### Python Configuration

Python configuration offers more flexibility for advanced users:

```python
# config.py
# Site information
SITE_NAME = "My Website"
SITE_DESCRIPTION = "A beautiful static site"
BASE_URL = "/"  # Use "/" for local development, or your domain for production

# Directory paths
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
STYLES_DIR = "styles"
STATIC_DIR = "static"
OUTPUT_DIR = "_site"

# Theme settings
THEME_CSS_FILE = "main.css"  # The CSS file to use from the styles directory

# Content sections
SECTIONS = {
    "posts": {
        "title": "Blog Posts",
        "template": "post.html",
        "list_template": "post_list.html",
        "sort_by": "date",
        "reverse_sort": True
    }
}

# Navigation items
NAV_ITEMS = [
    {"title": "Home", "url": "/"},
    {"title": "Blog", "url": "/posts/"},
    {"title": "About", "url": "/about.html"}
]
```

> 💡 **Note**: When both `config.yaml` and `config.py` exist, the YAML configuration takes precedence.

### 📚 Adding New Sections

1. Add a new section to your configuration file:

   **In YAML (config.yaml):**
   ```yaml
   sections:
     projects:
       title: Projects
       template: project.html      # Template for individual items
       list_template: project_list.html  # Template for section index
       sort_by: date
       reverse_sort: true
   ```

   **Or in Python (config.py):**
   ```python
   "projects": {
       "title": "Projects",
       "template": "project.html",
       "list_template": "project_list.html",
       "sort_by": "date",
       "reverse_sort": True
   }
   ```

2. Create the corresponding directory in `content/`:
   ```bash
   mkdir -p content/projects
   ```

3. Add Markdown files to the new section. That's it! 🎉

### 🎨 Creating a New Theme

1. Add a new CSS file in the `styles/` directory:
   ```bash
   cp styles/main.css styles/my-theme.css
   ```

2. Edit the CSS file to customize the appearance.

3. Update your configuration to use your new theme:

   **In YAML (config.yaml):**
   ```yaml
   theme_css_file: my-theme.css
   ```

   **Or in Python (config.py):**
   ```python
   THEME_CSS_FILE = "my-theme.css"
   ```

> 💅 **Style tip**: Check out CSS frameworks like [Water.css](https://watercss.kognise.dev/) or [Pico.css](https://picocss.com/) for quick, beautiful styling!

## 🏗️ Architecture

Zerodown is organized into modular components:

```
zerodown/
├── zerodown/           # Core package (the framework)
│   ├── __init__.py     # Package initialization
│   ├── builder.py      # Main build orchestration
│   ├── cli.py          # Command-line interface
│   ├── config.py       # Configuration handling
│   ├── content.py      # Content processing
│   ├── markdown.py     # Markdown handling with link/asset processing
│   ├── templates.py    # Template handling
│   └── utils.py        # Utility functions
├── examples/           # Example sites
│   ├── basic/          # Minimal example
│   ├── blog/           # Blog template
│   └── portfolio/      # Portfolio template
├── setup.py            # Package installation
└── run_zerodown.py     # Script to run without installing
```

This modular architecture ensures a clean separation between the framework and your content, making it easy to upgrade Zerodown without affecting your site.
  - `utils.py`: Utility functions

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

<div align="center">

### Built with ❤️ for Markdown lovers everywhere

*Zerodown: Because life's too short for complicated static site generators*

</div>
