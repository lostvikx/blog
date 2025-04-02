#!/bin/bash

# Description: Creates a directory for writing a blog post.
# Usage: ./create_post.sh <post-dirname>
# Example: ./create_post.sh ai-slop

# Creates the post/assets directories.
post_dir="${1:-'post'}"
mkdir -p "$post_dir/assets"
cd "$post_dir"

# Creates the article.md file.
cat << EOF > "article.md"
---
title: "Title Goes Here"
author: "Vikram S. Negi"
date: "$(date +'%b %d, %Y')"
description: "Add a description for the article."
thumbnail: "assets/image_720p.webp"
---
EOF

echo "Start writing in '$post_dir/article.md'."
echo "Note: All post assets go in '$post_dir/assets'."
