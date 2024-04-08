import os
import re
import shutil

from src import block_markdown


def copy_dir(src, dst, force=False):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory {src} does not exist")

    if os.path.exists(dst) and force:
        os.rmdir(dst)

    if not os.path.exists(dst):
        os.mkdir(dst)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_dir(s, d)
        else:
            if os.path.exists(d) and force:
                os.remove(d)
            shutil.copy(s, d)


def extract_title(markdown) -> str:
    for line in markdown.split("\n"):
        if line.strip().startswith("# "):
            return line[2:]
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    with open(template_path, "r") as f:
        template = f.read()
    with open(from_path, "r") as f:
        content = f.read()

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        doc_title = extract_title(content)
        html_content = block_markdown.markdown_to_html_node(content).to_html()
        html_str = template.replace("{{ Title }}", doc_title).replace("{{ Content }}", html_content)
        f.write(html_str)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, item)
        dst = os.path.join(dest_dir_path, item)
        if os.path.isdir(src):
            generate_pages_recursive(src, template_path, dst)
        else:
            if item.endswith(".md"):
                generate_page(src, template_path, dst.replace(".md", ".html"))


def main(_: list[str]) -> int:
    copy_dir("../static", "../public")
    generate_pages_recursive("../content", "../template.html", "../public")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))