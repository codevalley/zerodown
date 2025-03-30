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
   python run_zerodown.py
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
   - 🧩 Add global elements in `content/_includes/` (header, footer, homepage)
   - 🖼️ Store images and other assets in `content/assets/`

4. **Customize templates**:
   - 🖌️ Edit HTML templates in the `templates/` directory
   - 🎨 Create or modify CSS themes in the `styles/` directory

5. **Build your site**:
   ```bash
   # If you installed the package
   zerodown build /path/to/your/site
   
   # Or using the run script
   python run_zerodown.py build /path/to/your/site
   ```

6. **Preview locally**:
   ```bash
   # If you installed the package
   zerodown serve /path/to/your/site
   
   # Or using the run script
   python run_zerodown.py serve /path/to/your/site
   ```
   Then visit `http://localhost:8000` in your browser. ✨

## 📂 Content Structure

```
content/
├── _includes/         # Global content elements
│   ├── header.md      # Site header with navigation
│   ├── footer.md      # Site footer
│   └── home.md        # Homepage content
├── assets/            # Images and other files
│   └── ...
├── notes/             # Example section
│   ├── first-note.md
│   └── ...
└── about.md           # Top-level page
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
site_name: My Website
site_description: A beautiful static site

# Content sections
sections:
  posts:
    title: Blog Posts
    template: post.html
    sort_by: date
    reverse_sort: true
```

#### Python Configuration

Python configuration offers more flexibility for advanced users:

```python
# config.py
SITE_NAME = "My Website"
SITE_DESCRIPTION = "A beautiful static site"

# Content sections
SECTIONS = {
    "posts": {
        "title": "Blog Posts",
        "template": "post.html",
        "sort_by": "date",
        "reverse_sort": True
    }
}
```

> 💡 **Note**: When both `config.yaml` and `config.py` exist, the YAML configuration takes precedence.

### 📚 Adding New Sections

1. Add a new section to your configuration file:

   **In YAML (config.yaml):**
   ```yaml
   sections:
     projects:
       title: Projects
       sort_by: date
       reverse_sort: true
   ```

   **Or in Python (config.py):**
   ```python
   "projects": {
       "title": "Projects",
       "sort_by": "date",
       "reverse": True
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
