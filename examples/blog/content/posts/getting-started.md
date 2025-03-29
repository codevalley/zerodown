---
title: Getting Started with Zerodown
date: 2023-01-15
author: Zerodown Team
tags: [tutorial, markdown, zerodown]
---

# Getting Started with Zerodown

Welcome to Zerodown, the zero-effort Markdown website generator! This post will guide you through the basics of setting up and using Zerodown for your own projects.

## What is Zerodown?

Zerodown is a simple static site generator that converts Markdown files into a beautiful website. It's designed to be easy to use, with minimal configuration required. Perfect for:

- Personal blogs
- Project documentation
- Portfolio websites
- Simple business sites

## Installation

Installing Zerodown is straightforward:

```bash
# Clone the repository
git clone https://github.com/yourusername/zerodown.git

# Navigate to the directory
cd zerodown

# Install dependencies
pip install -r requirements.txt

# Install the package (optional)
pip install -e .
```

## Creating Your First Site

To create a new site, you can use one of the example templates:

1. Copy an example directory (like `examples/blog`) to your desired location
2. Modify the `config.py` file to match your site details
3. Add your content to the `content` directory
4. Run the build command:

```bash
python -m zerodown build /path/to/your/site
```

## Writing Content

All content in Zerodown is written in Markdown with YAML frontmatter. Here's an example:

```markdown
---
title: My First Post
date: 2023-01-15
author: Your Name
tags: [example, first-post]
---

# My First Post

This is my first post using Zerodown!

## Subheading

You can use all standard Markdown features.

- Lists
- **Bold text**
- *Italic text*
- [Links](https://example.com)
- ![Images](path/to/image.jpg)
```

## Next Steps

Now that you have the basics down, try:

- Customizing the CSS to match your brand
- Adding new sections to your site
- Creating custom templates
- Deploying your site to GitHub Pages or Netlify

Happy building with Zerodown!
