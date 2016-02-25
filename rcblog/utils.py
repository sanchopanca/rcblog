import os.path
from pathlib import Path

import CommonMark


def md_to_html(md: str) -> str:
    parser = CommonMark.Parser()
    ast = parser.parse(md)
    return CommonMark.HtmlRenderer().render(ast)


def get_posts_list() -> list:
    post_directory = get_repository_path()
    html_files = [path.name for path in post_directory.iterdir() if path.is_file() and path.suffix == '.html']
    # print(html_files)
    return html_files


def get_repository_path() -> Path:
    cur_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    return cur_dir / 'posts_repository'


def complement_of_lists_of_dictionaries(a: dict, b: dict):
    a_tuple = tuple((key, value) for (key, value) in a.items())
    b_tuple = tuple((key, value) for (key, value) in b.items())
    c_set = set(a_tuple) - set(b_tuple)
    c = {}
    for key, value in c_set:
        c[key] = value
    return c


if __name__ == '__main__':
    print(complement_of_lists_of_dictionaries({'a': 'A', 'b': 'B'}, {'a': 'A'}))

