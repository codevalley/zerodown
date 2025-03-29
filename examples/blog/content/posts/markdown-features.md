---
title: Markdown Features in Zerodown
date: 2023-01-20
author: Zerodown Team
tags: [markdown, features, tutorial]
---

# Markdown Features in Zerodown

Zerodown supports all standard Markdown features plus some additional enhancements. This post showcases the various Markdown elements you can use in your content.

## Basic Formatting

Markdown makes it easy to format your text:

**Bold text** is created with double asterisks.

*Italic text* uses single asterisks.

***Bold and italic*** combines both.

~~Strikethrough~~ uses double tildes.

## Lists

### Unordered Lists

* Item 1
* Item 2
  * Nested item 2.1
  * Nested item 2.2
* Item 3

### Ordered Lists

1. First item
2. Second item
3. Third item
   1. Nested item 3.1
   2. Nested item 3.2

## Links and Images

### Links

[External link to Google](https://www.google.com)

[Link to another page](/about.html)

### Images

![Sample image](https://via.placeholder.com/600x400)

## Blockquotes

> This is a blockquote.
> 
> It can span multiple lines.
>
> > And can be nested.

## Code

### Inline Code

Use the `print()` function to output text.

### Code Blocks

```python
def hello_world():
    print("Hello, Zerodown!")
    
hello_world()
```

## Tables

| Name     | Age | Occupation    |
|----------|-----|---------------|
| John     | 32  | Developer     |
| Sarah    | 28  | Designer      |
| Michael  | 45  | Project Manager |

## Horizontal Rules

Three hyphens create a horizontal rule:

---

## Task Lists

- [x] Create a Zerodown site
- [x] Write documentation
- [ ] Deploy to production

## Footnotes

Here's a sentence with a footnote[^1].

[^1]: This is the footnote content.

## Headings

# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

## Special Features in Zerodown

### Asset Handling

In Zerodown, you can link to assets using relative paths, and they'll be automatically adjusted in the final site:

![Local image](../assets/sample.jpg)

### Navigation

Navigation in Zerodown can be written in Markdown and will be properly converted to HTML:

```markdown
<nav class="main-nav">
* [Home](/)
* [Blog](/posts/)
* [About](/about.html)
</nav>
```

### Frontmatter

The YAML frontmatter at the top of each Markdown file provides metadata:

```yaml
---
title: My Post Title
date: 2023-01-20
author: Your Name
tags: [tag1, tag2]
---
```

This metadata is available in templates and can be used for sorting, filtering, and displaying information about your content.

## Conclusion

With Zerodown's Markdown support, you can create rich, well-formatted content without needing to write HTML. Focus on your writing, and let Zerodown handle the presentation!
