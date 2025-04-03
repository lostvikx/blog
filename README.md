# Blog

* A static blog site to share my weird thoughts with the world.
* Contact [vikram.s.negi@proton.me](mailto:vikram.s.negi@proton.me) if you have any issues related to my content.

## Install

JS Beautify:

```bash
npm -g install js-beautify
```

uv Package Manager:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Usage

```bash
uv run generate.py 
```

## Test Server

```bash
cd site/ && python -m http.server
```

## Markdown Metadata

Make sure all your blog posts (markdown files) have this metadata:

```yaml
---
title: "Title of the Blog Post"
author: "Vikram S. Negi"
date: "Mar 24, 2025"
description: "A short summary of the blog post."
thumbnail: "assets/thumbnail.webp"
---
```

## Generate Site 

Script generates a directory `site/` these things:

1. HTML files with the same name as the markdown file.
2. Directories `posts/*.html` and `posts/assets`.

This is our directory to serve. `site/` will contain all static files.

## TODO

- [x] Let python access the markdown metadata
- [x] Add post title and date to index.html
- [x] Image compression
- [x] index.html page
- [ ] About Me page 
- [x] Create `site/` directory
