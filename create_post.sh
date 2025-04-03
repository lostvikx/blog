#!/bin/bash

# Description: Creates a directory for writing a blog post.
# Usage: ./create_post.sh <markdown-file-name.md>
# Example: ./create_post.sh new-post.md

# Creates the post/assets directories.
cd "posts/"

# Creates the new-post.md file.
cat << EOF > "${$1:-'new-post.md'}"
---
title: "Title Goes Here"
author: "Vikram S. Negi"
date: "$(date +'%b %d, %Y')"
description: "Add a description for the article."
thumbnail: "assets/image_720p.webp"
---
EOF

echo "Start writing in '$(pwd)/new-post.md'."
echo "Note: All post assets go in '$(pwd)/assets'."
