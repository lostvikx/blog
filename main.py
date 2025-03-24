import os
import sys
import subprocess

def convert_markdown_to_html(markdown_file):
    md_file = os.path.abspath(markdown_file)
    print(f"Path: {md_file}")
    try:
        subprocess.run(["pandoc", md_file, "-o", "temp/post.html", "--template=template.html"], check=True)
        print("Success: Markdown to HTML conversion complete.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    markdown_file = sys.argv[1]
    convert_markdown_to_html(markdown_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <markdown_file_path>")
        sys.exit(1)
    
    main()
