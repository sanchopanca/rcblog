import os.path
from pathlib import Path

import CommonMark


def md_to_html(md: str) -> str:
    parser = CommonMark.DocParser()
    ast = parser.parse(md)
    return CommonMark.HTMLRenderer().render(ast)


def get_posts_list() -> list:
    post_directory = get_repository_path()
    html_files = [path.name for path in post_directory.iterdir() if path.is_file() and path.suffix == '.html']
    # print(html_files)
    return html_files


def get_repository_path() -> Path:
    cur_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    return cur_dir / 'posts_repository'