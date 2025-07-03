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

from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path


def copy_site_static_files(public_dir) -> None:
    for src_path in Path(public_dir).iterdir():
        dst_path = Path("site") / src_path.name
        if (src_path.is_file()) and (not dst_path.is_file()):
            shutil.copy(src_path, dst_path)

    return None


def copy_assets(assets_dir: Path, dest_dir: Path) -> None:

    for asset in assets_dir.iterdir():
        src_path = asset
        dst_path = dest_dir / asset.name
        
        if src_path.is_file():
            is_image_file: bool = asset.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
            if is_image_file:
                try:
                    print(f"Compressing: {str(asset)}")
                    subprocess.run(["convert", str(src_path), "-quality", "80", "-strip", str(dst_path)], check=True)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                shutil.copy(src_path, dst_path)
        else:
            print("Copying a directory:", asset)
            dir_name: str = asset.name
            dest_d: Path = Path(os.path.join("site", "posts", "assets", dir_name))
            dest_d.mkdir()
            copy_assets(asset, dest_d)

    return None


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
        metadata["file"] = str(file)
        posts_metadata.append(metadata)

    posts_metadata = sorted(posts_metadata, 
                            key=lambda meta: datetime.strptime(meta.get("date"), "%b %d, %Y"), 
                            reverse=True)
    for post_meta in posts_metadata:
        if most_recent_post is None:
            most_recent_post = post_meta
            add_featured_post(post_meta)
        
        convert_html(post_meta.get("file"))
    
    add_posts_entries(posts_metadata[1:])


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

    featured.h2.string = metadata.get("title")
    featured.find("p", attrs={"id": "description"}).string = metadata.get("description")

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
    # print(posts_metadata[0])

    for metadata in posts_metadata:
        new_post = soup.new_tag("a", attrs={"href": metadata["path"]})
        div = soup.new_tag("div")

        fig = soup.new_tag("figure")
        img_src = os.path.join("posts", metadata.get("thumbnail"))
        img = soup.new_tag("img", attrs={"src": img_src, "alt": "Post Thumbnail", "loading": "lazy"})
        fig.append(img)

        info = soup.new_tag("div", attrs={"class": "details"})

        title_string = None
        if len(metadata.get("title")) <= 50:
            title_string = metadata.get("title")
        else:
            title_string = metadata.get("title")[:47] + "..."

        description_string = None
        if len(metadata.get("description")) <= 90:
            description_string = metadata.get("description")
        else:
            description_string = metadata.get("description")[:87] + "..."

        title = soup.new_tag("h3", string=title_string)
        description = soup.new_tag("div", string=description_string, attrs={"class": "description"})

        date = soup.new_tag("div")
        em = soup.new_tag("em", string=metadata["date"])
        date.append(em)

        info.append(date)
        info.append(title)
        info.append(description)

        div.append(fig)
        div.append(info)

        new_post.append(div)
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
    assets_dir = Path(os.path.join(posts_dir, "assets"))
    dest_dir = Path(os.path.join("site", "posts", "assets"))
    copy_assets(assets_dir, dest_dir)
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
