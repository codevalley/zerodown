---
title: "Working with Links and Assets"
date: 2025-03-29
description: "A demonstration of how links and assets work in our static site generator"
---

# Working with Links and Assets

This page demonstrates how our static site generator handles various types of links and assets.

## Images

### Relative Image Path
Here's an image using a relative path:

![Sample Image](../assets/sample-image.png)

### Absolute Image Path
Here's an image using an absolute path (from content root):

![Another Sample](/assets/sample-image.png)

### External Image
Here's an external image:

![External Image](https://via.placeholder.com/300x150)

## Links

### Internal Link to Another Note
Here's a link to [our first note](first-note.md)

### Link to a Section
Here's a link to the [notes section](/notes/)

### External Link
Here's an external link to [Google](https://www.google.com)

## Testing Asset Paths in Different Contexts

When writing content, you want to be able to:

1. Preview the Markdown in your editor with working links
2. Have all links work correctly in the final built site

Our asset processor automatically adjusts paths to make this possible!
