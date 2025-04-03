# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "beautifulsoup4",
#     "pyyaml",
# ]
# ///

import os
import sys
import shutil
import subprocess
import yaml
from bs4 import BeautifulSoup
from pathlib import Path


def copy_site_static_files(public_dir):
    for src_path in Path(public_dir).iterdir():
        dst_path = Path("site") / src_path.name
        if (src_path.is_file()) and (not dst_path.is_file()):
            shutil.copy(src_path, dst_path)


def copy_asset_files(posts_dir: str):
    assets_dir = os.path.join(posts_dir, "assets")
    dest_dir = os.path.join("site", "posts", "assets")

    for asset in Path(assets_dir).iterdir():
        src_path = asset
        dst_path = Path(dest_dir) / asset.name
        
        if (src_path.is_file()) and (not dst_path.is_file()):
            is_image_file: bool = asset.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
            if is_image_file:
                try:
                    print(f"Compressing: {str(asset)}")
                    subprocess.run(["convert", str(src_path), "-quality", "80", "-strip", str(dst_path)], check=True)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                shutil.copy(src_path, dst_path)


def convert_html(file_path: str) -> None:
    md_file: str = os.path.basename(file_path)
    html_path: str = os.path.join("site", "posts", f"{os.path.splitext(md_file)[0]}.html")

    # Don't re-generate an HTML file.
    if not Path(html_path).is_file():
        print(f"Generating: {html_path}")
        try:
            subprocess.run(["pandoc", file_path, "-o", html_path, "--template=template.html"], check=True)
            subprocess.run(["js-beautify", "-rq", html_path], check=True)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


def generate_posts(posts_dir: str) -> None:
    posts: list[Path] = sorted(Path(posts_dir).glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)

    # TODO: Save posts metadata to a file.
    posts_metadata: list[dict] = []
    most_recent_post = None

    for file in posts:
        metadata: dict = extract_metadata(file)
        posts_metadata.append(metadata)
        if most_recent_post is None:
            most_recent_post = file
            add_featured_post(metadata)

        file_path: str = os.path.join(posts_dir, str(file))
        convert_html(file_path)
    
    add_posts_entries(posts_metadata)


def extract_metadata(post: Path) -> dict:
    metadata_lines: list[str] = []
    with open(str(post), "r", encoding="utf-8") as file:
        first_line: str = file.readline()
        if first_line.strip() != "---":
            print("Info: No metadata found associated with the markdown file.")
            return {}

        for line in file:
            if line.strip() == "---":
                break
            metadata_lines.append(line.strip() + "\n")

    md_metadata: dict[str, str] = yaml.safe_load("".join(metadata_lines)) if metadata_lines else {}
    md_metadata["path"] = os.path.join("posts", post.stem + ".html")
    return md_metadata


def add_featured_post(metadata: dict) -> None:
    index_file: Path = Path(os.path.join("site", "index.html"))
    with open(str(index_file), "r", encoding="utf-8") as html:
        soup = BeautifulSoup(html, "html.parser")

    featured = soup.find(id="featured-post")
    featured.h2.string = metadata["title"] if len(metadata["title"]) < 55 else metadata["title"][:51] + "..."

    featured.find("p", attrs={"id": "description"}).string = metadata["description"] if len(metadata["description"]) < 125 else metadata["description"][:121] + "..."

    featured.em.string = metadata["date"]
    featured.img["src"] = os.path.join("posts", metadata["thumbnail"])
    featured.a["href"] = metadata["path"]

    with open(index_file, "w", encoding="utf-8") as html:
        html.write(str(soup))
    
    try:
        subprocess.run(["js-beautify", "-rq", index_file], check=True)
    except Exception as e:
        print(f"Error: {e}")


def add_posts_entries(posts_metadata: list[dict]) -> None:
    index_file: Path = Path(os.path.join("site", "index.html"))
    with open(str(index_file), "r", encoding="utf-8") as html:
        soup = BeautifulSoup(html, "html.parser")

    recent = soup.find(id="recent-posts")
    posts_metadata.reverse()

    for metadata in posts_metadata:
        new_post = soup.new_tag("a", attrs={"href": metadata["path"]})
        div = soup.new_tag("div")
        new_post.insert(0, div)
        new_post_title = metadata["title"] if len(metadata["title"]) < 70 else metadata["title"][:66] + "..."
        title = soup.new_tag("div", string=new_post_title)
        date = soup.new_tag("div", string=metadata["date"])
        div.insert(0, title)
        title.insert_after(date)
        recent.insert(0, new_post)
    
    with open(index_file, "w", encoding="utf-8") as html:
        html.write(str(soup))

    try:
        subprocess.run(["js-beautify", "-rq", index_file], check=True)
    except Exception as e:
        print(f"Error: {e}")


def main() -> None:
    site = Path(os.path.abspath("site"))
    if site.exists() and site.is_dir():
        print("Deleting site/ directory.")
        shutil.rmtree(site)

    posts_dir: str = os.path.abspath("posts")
    print("Posts:", posts_dir)
    public_dir: str = os.path.abspath("public")

    # Note: mkdir -p site/posts/assets
    Path(os.path.join("site", "posts", "assets")).mkdir(parents=True, exist_ok=True)

    print("Copying static files...")
    copy_asset_files(posts_dir)
    copy_site_static_files(public_dir)
    print("Copying Complete!")

    print("Generating HTML files...")
    generate_posts(posts_dir)
    print("Generation Complete!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
