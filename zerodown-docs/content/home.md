---
title: "Zerodown: Static site generation for Markdown lovers"
description: "Zero effort, maximum markdown power! Lightning-fast static site generator for blogs, portfolios, and documentation."
---
# Write in markdown, and publish with a _single command_. 

Zerodown is a lightning-fast, zero-configuration static site generator that transforms your Markdown content into beautiful, fast-loading websites. 

[Get Started](getting-started.html) | [View Features](markdown-features.html)

---

## Key Features

*   **📝 Content-focused**: Write in Markdown, focus on your content.
*   **🧩 Modular Architecture**: Clean separation for easy maintenance.
*   **🔗 Smart Asset Handling**: Links & images just work.
*   **🎨 Theme Support**: Easily switch CSS themes.
*   **⚡ Fast Builds**: Efficient processing.
*   **🔌 Zero Configuration**: Works out of the box.

---

## Quick Start

Get your site running in minutes:

```bash
# 1. Initialize a new site (creates directory, config, basic structure)
# Replace 'my-new-site' with your desired directory name
python zd_cli.py init my-new-site --template basic

# 2. Navigate into your site directory
cd my-new-site

# 3. Add your content
# Create Markdown files (.md) inside the 'content/' directory
# For example: content/about.md, content/posts/my-first-post.md

# 4. Build your static site (output goes to '_site/' by default)
python ../zd_cli.py build .

# 5. Preview your site locally
python ../zd_cli.py serve .
# Then open http://localhost:8000 in your browser!
``` 