import os
import sys
import shutil
import subprocess
import yaml
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
    if not Path(html_path).is_file():
        print(f"Generating: {html_path}")
        try:
            subprocess.run(["pandoc", file_path, "-o", html_path, "--template=template.html"], check=True)
            subprocess.run(["js-beautify", "-rq", html_path], check=True)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


def generate_posts(posts_dir: str) -> Path:
    Path(os.path.join("site", "posts", "assets")).mkdir(parents=True, exist_ok=True)
    posts = sorted(Path(posts_dir).glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    recent_post = None
    for file in posts:
        if recent_post is None:
            recent_post = file
        file_path: str = os.path.join(posts_dir, file)
        convert_html(file_path)
    print("Most Recent:", recent_post)
    return recent_post


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
    return md_metadata


def main() -> None:
    posts_dir: str = os.path.abspath("posts")
    print("posts/ directory:", posts_dir)

    print("Generating HTML files...")
    recent_post: Path = generate_posts(posts_dir)
    print("Generation Complete!")

    print("Copying static files...")
    public_dir: str = os.path.abspath("public")
    copy_asset_files(posts_dir)
    copy_site_static_files(public_dir)
    print("Copying Complete!")

    metadata: dict = extract_metadata(recent_post)
    print(metadata)

    # TODO: Add recent post metadata to featured post section in index.html

    # TODO: Add all posts in the recent posts section.


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
