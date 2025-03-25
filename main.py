import os
import sys
import subprocess
import shutil
import yaml


def convert_markdown_to_html(markdown_file):
    print(f"Markdown Path: {markdown_file}")
    base_dir = os.path.dirname(markdown_file)
    html_filename = os.path.basename(base_dir)
    html_path = os.path.join("posts", f"{html_filename}.html")

    try:
        subprocess.run(["pandoc", markdown_file, "-o", html_path, "--template=template.html"], check=True)
        print("Success: Markdown to HTML conversion complete.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    return html_path


def check_valid_post_dir(blog_post_dir):
    files_in_dir = os.listdir(blog_post_dir)
    return ("assets" in files_in_dir) and (len(files_in_dir) == 2)


def get_markdown_file(blog_post_dir):
    for file in os.listdir(blog_post_dir):
        if file.endswith(".md"):
            return os.path.join(blog_post_dir, file)
    return None


def copy_asset_files(blog_post_dir):
    assets_dir = os.path.join(blog_post_dir, "assets")
    destination_asset_dir = "posts/assets"

    for asset in os.listdir(assets_dir):
        src_path = os.path.join(assets_dir, asset)
        dst_path = os.path.join(destination_asset_dir, asset)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)


def extract_md_metadata(markdown_file):
    metadata_lines = []
    with open(markdown_file, "r", encoding="utf-8") as file:
        first_line = file.readline()
        if first_line.strip() != "---":
            print("Info: No metadata found associated with the markdown file.")
            return {}

        for line in file:
            if line.strip() == "---":
                break
            metadata_lines.append(line.strip() + "\n")

    md_metadata = yaml.safe_load("".join(metadata_lines)) if metadata_lines else {}
    return md_metadata


def main():
    blog_post_dir = sys.argv[1]
    if not os.path.isdir(blog_post_dir):
        print(f"Error: {blog_post_dir} is not a valid directory.")
        sys.exit(1)
    
    blog_post_dir = os.path.abspath(blog_post_dir)
    is_valid_dir = check_valid_post_dir(blog_post_dir)
    
    if not is_valid_dir:
        print(f"Error: Make sure the blog post directory has only two items article.md and assets/")
        sys.exit(1)

    markdown_file = get_markdown_file(blog_post_dir)
    if markdown_file is None:
        print("Error: Markdown file not found.")
        sys.exit(1)

    html_path = convert_markdown_to_html(markdown_file)
    print(f"HTML: {html_path}")
    copy_asset_files(blog_post_dir)

    md_metadata = extract_md_metadata(markdown_file)
    print(md_metadata)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path/to/blog-post-directory>")
        sys.exit(1)
    
    main()
