# Blog

A static blog site to share my thoughts with the world. Contact [vikram.s.negi@proton.me](mailto:vikram.s.negi@proton.me) if you have any issues with my content.

## Markdown Metadata

Make sure all your blog posts (markdown files) have this metadata. This helps provide structure to the document.

```yaml
---
title: "Title of the Blog Post"
author: "Vikram S. Negi"
date: "Mar 24, 2025"
description: "A short summary of the blog post."
---
```

## Create a Post

Simply create a directory with two things:

1. A markdown file with any name.
2. A directory for assets named `assets/`.

Note: The name of the directory should be in lowercase and hypen separated. As it will be used as the HTML filename.

## TODO

- [*] Input a blog-post directory `["article.md", "assets/*"]`
- [ ] Let python access the markdown metadata (post title and date)
- [ ] Add post title and date to index.html
- [ ] Image compression
- [ ] index.html page
