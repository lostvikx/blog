# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "beautifulsoup4",
#     "pyaml",
# ]
# ///

import os
import sys
import subprocess
import shutil
import yaml
from bs4 import BeautifulSoup


def convert_markdown_to_html(markdown_file: str) -> str:
    print(f"Markdown Path: {markdown_file}")
    base_dir: str = os.path.dirname(markdown_file)
    html_filename: str = os.path.basename(base_dir)
    html_path: str = os.path.join("posts", f"{html_filename}.html")

    try:
        subprocess.run(["pandoc", markdown_file, "-o", html_path, "--template=template.html"], check=True)
        print("Success: Markdown to HTML conversion complete.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    return html_path


def check_valid_post_dir(blog_post_dir: str) -> bool:
    files_in_dir: list[str] = os.listdir(blog_post_dir)
    return ("assets" in files_in_dir) and (len(files_in_dir) == 2)


def get_markdown_file(blog_post_dir: str) -> str | None:
    for file in os.listdir(blog_post_dir):
        if file.endswith(".md"):
            return os.path.join(blog_post_dir, file)
    return None


def copy_asset_files(blog_post_dir: str) -> None:
    assets_dir: str = os.path.join(blog_post_dir, "assets")
    destination_asset_dir: str = os.path.join("posts", "assets")

    for asset in os.listdir(assets_dir):
        src_path: str = os.path.join(assets_dir, asset)
        dst_path: str = os.path.join(destination_asset_dir, asset)

        if os.path.isfile(src_path):
            # Image files get compressed.
            if asset.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                webp_path = os.path.splitext(dst_path)[0] + ".webp"
                try:
                    subprocess.run(["convert", src_path, "-quality", "80", "-strip", webp_path], check=True)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                shutil.copy(src_path, dst_path)


def extract_md_metadata(markdown_file: str) -> dict:
    metadata_lines: list[str] = []
    with open(markdown_file, "r", encoding="utf-8") as file:
        first_line: str = file.readline()
        if first_line.strip() != "---":
            print("Info: No metadata found associated with the markdown file.")
            return {}

        for line in file:
            if line.strip() == "---":
                break
            metadata_lines.append(line.strip() + "\n")

    md_metadata: dict[str, str] = yaml.safe_load("".join(metadata_lines)) if metadata_lines else {}
    return md_metadata


def add_post_to_index(meta_data: dict) -> None:
    with open("index.html", "r", encoding="utf-8") as html:
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")

    # Update Featured Post
    featured = soup.find(id="featured-post")
    featured.h2.string = meta_data["title"] if len(meta_data["title"]) < 55 else meta_data["title"][:51] + "..."

    featured.find("p", attrs={"id": "description"}).string = meta_data["description"] if len(meta_data["description"]) < 125 else meta_data["description"][:121] + "..."

    featured.em.string = meta_data["date"]
    featured.img["src"] = os.path.join("posts", meta_data["thumbnail"])
    featured.a["href"] = meta_data["path"]

    # Insert in Recent Posts
    recent = soup.find(id="recent-posts")
    recent_posts: list[str] = recent.find_all("a")
    post_exists: bool = False
    for post in recent_posts:
        if post["href"] == meta_data["path"]:
            print("Post already exists.")
            post_exists = True
            break

    if not post_exists:
        new_post = soup.new_tag("a", attrs={"href": meta_data["path"]})
        div = soup.new_tag("div")
        new_post.insert(0, div)
        new_post_title = meta_data["title"] if len(meta_data["title"]) < 70 else meta_data["title"][:66] + "..."
        title = soup.new_tag("div", string=new_post_title)
        date = soup.new_tag("div", string=meta_data["date"])
        div.insert(0, title)
        title.insert_after(date)
        recent.insert(0, new_post)

    with open("index.html", "w", encoding="utf-8") as html:
        html.write(str(soup))


def main() -> None:
    blog_post_dir: str = sys.argv[1]
    if not os.path.isdir(blog_post_dir):
        print(f"Error: {blog_post_dir} is not a valid directory.")
        sys.exit(1)
    
    blog_post_dir: str = os.path.abspath(blog_post_dir)
    is_valid_dir: bool = check_valid_post_dir(blog_post_dir)
    
    if not is_valid_dir:
        print(f"Error: Make sure the blog post directory has only two items article.md and assets/")
        sys.exit(1)

    markdown_file: str = get_markdown_file(blog_post_dir)
    if markdown_file is None:
        print("Error: Markdown file not found.")
        sys.exit(1)

    html_path: str = convert_markdown_to_html(markdown_file)
    print(f"HTML: {html_path}")
    copy_asset_files(blog_post_dir)

    md_metadata: dict = extract_md_metadata(markdown_file)
    md_metadata["path"] = html_path

    add_post_to_index(md_metadata)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run script.py <path/to/blog-post-directory>")
        sys.exit(1)
    
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
