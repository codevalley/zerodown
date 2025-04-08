# Zerodown Documentation Site Plan

**Goal:** Create the official documentation website for the Zerodown project, built using Zerodown itself and styled with a clean, semantic look inspired by Pico.css.

**Guiding Principles:**
*   **Dogfooding:** Use Zerodown's features (Markdown, templates, shortcodes, CLI) extensively.
*   **Content First:** Leverage the existing `README.md` as the primary source material.
*   **Semantic HTML:** Rely on standard HTML tags styled by Pico.css, minimizing custom CSS.
*   **Maintainability:** Structure content logically for easy updates.

**Proposed Structure & Content:**

1.  **Project Directory:** Create a new directory, e.g., `zerodown-docs/`, alongside the main `zerodown/` source directory. This will keep the docs site separate from the core codebase.

2.  **Configuration (`zerodown-docs/config.yaml`):**
    *   `site_name`: "Zerodown Documentation"
    *   `site_description`: "Official documentation for the Zerodown static site generator."
    *   `content_dir`: `content`
    *   `template_dir`: `templates`
    *   `styles_dir`: `styles`
    *   `output_dir`: `_site` (or maybe `../docs_build` to output outside the source folder)
    *   `theme_css_file`: `pico.min.css` (or similar, assuming we download it)
    *   `nav_items`: Define the main navigation links (e.g., Home, Getting Started, Features, Configuration, CLI Reference, Contributing). These will be rendered in the header.
    *   `sections`: Potentially define a 'docs' section or rely solely on top-level pages initially.

3.  **Content (`zerodown-docs/content/`)**:
    *   **Source:** Adapt content heavily from the project's main `README.md`.
    *   `home.md`: Homepage content. **Plan:**
        *   **Headline:** "⚡ Zerodown ⚡"
        *   **Tagline:** "Zero effort, maximum markdown power!" (or similar)
        *   **Brief Intro Paragraph:** Adapted from "What is Zerodown?".
        *   **Call to Action Buttons:** Link to `getting-started.md` ("Get Started") and perhaps `markdown-features.md` ("View Features") or `cli-reference.md` ("CLI Guide"). These will require styling using Pico's button suggestions (potentially using role="button").
        *   **Key Features Section:** A concise list or grid highlighting the main benefits (Markdown focus, Fast builds, Zero config, etc.).
    *   `getting-started.md`: Installation, `init`, `build`, `serve`.
    *   `content-structure.md`: Explain the project directory layout.
    *   `markdown-features.md`: Front matter, links/images, shortcodes.
    *   `configuration.md`: `config.yaml`/`.py`, options, sections.
    *   `theming.md`: Using CSS themes, referencing Pico.css.
    *   `cli-reference.md`: CLI commands and interactive shell details.
    *   `deployment.md`: How to deploy the generated site.
    *   `contributing.md`: Contribution guidelines.
    *   `about.md`: Project philosophy, license.
    *   `_includes/`: (Optional) For reusable snippets if needed.
    *   `assets/`: For any images or diagrams used.

4.  **Templates (`zerodown-docs/templates/`)**:
    *   `base.html`:
        *   Basic HTML5 structure (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`).
        *   Link to `pico.min.css`.
        *   **Theme:** Set `data-theme="light"` or `data-theme="dark"` on `<html>` for Pico theme control, potentially adding a toggle later.
        *   Semantic structure: `<header>`, `<nav>`, `<main class="container">`, `<footer>`.
        *   **Header/Nav:** Include the site title (`{{ config.site_name }}`) and render the `nav_items` from `config.yaml` as a list of links within the `<nav>` element, styled appropriately by Pico.
        *   Define blocks for title, content, scripts.
    *   `page.html`:
        *   Extends `base.html`.
        *   Renders the main content (`{{ content | safe }}`) within the `<main>` block.
        *   Displays the page title (`{{ title }}`).
    *   `home.html`:
        *   Extends `base.html`.
        *   **Layout:** Designed to match the `home.md` plan. Use appropriate semantic HTML (`<section>`, `<h1>`, `<p>`, `<a>` possibly with `role="button"`, `<ul>`) that Pico.css will style. Might override the `content` block entirely to structure the intro, CTAs, and features sections specifically.
        *   Renders `home.md` content within its specific structure.

5.  **Styles (`zerodown-docs/styles/`)**:
    *   Download `pico.min.css` from [https://picocss.com/](https://picocss.com/) and place it here.
    *   (Optional) Add a minimal `custom.css` for minor overrides if absolutely necessary, and link it *after* Pico in `base.html`.

**Implementation Steps:**

1.  Create the `zerodown-docs/` directory structure (`content`, `templates`, `styles`).
2.  Download `pico.min.css` into `zerodown-docs/styles/`.
3.  Create the initial `zerodown-docs/config.yaml` with basic site info and paths.
4.  Implement `templates/base.html` linking Pico.css and setting up semantic blocks.
5.  Implement `templates/page.html` and `templates/home.html`.
6.  Populate `config.yaml` with initial `nav_items`.
7.  Copy/adapt content from `README.md` into the corresponding Markdown files within `zerodown-docs/content/`. Start with `home.md` and `getting-started.md`.
8.  Use the Zerodown CLI to build and serve the docs site:
    ```bash
    # Navigate to the main project root
    python zd_cli.py build zerodown-docs
    python zd_cli.py serve zerodown-docs
    ```
9.  Iterate: Add more content pages, refine templates, adjust configuration, and check the appearance in the browser, ensuring it leverages Pico's styling effectively. 