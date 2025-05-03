# Blog

* A static blog site to share my weird thoughts with the world.
* Contact [vikram.s.negi@proton.me](mailto:vikram.s.negi@proton.me) if you have any issues related to my content.

## Install

Pandoc:

```bash
sudo apt install pandoc
```

ImageMagick:

```bash
sudo apt install imagemagick
```

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

Make sure all your blog posts (`.md` files) have this metadata:

```yaml
---
title: "Title Goes Here"
author: "Vikram S. Negi"
date: "$(date +'%b %d, %Y')"
description: "Add a description for the article."
thumbnail: "assets/image_720p.webp"
---
```

Note: Use the `create_post.sh` script to create a new blog post.

## Generate Site 

Script generates a directory `site/` these things:

1. HTML files with the same name as the markdown file.
2. Directories `posts/*.html` and `posts/assets`.

* `site/` will contain all static files.
* Please refer the Cloudflare Pages [docs](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/).

## TODO

- [x] Let python access the markdown metadata
- [x] Add post title and date to index.html
- [x] Image compression
- [x] index.html page
- [x] Add a create_post.sh script
- [ ] ABOUT page 
- [x] Create `site/` directory
- [ ] LINKS page
