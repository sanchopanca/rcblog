import re

import CommonMark


def md_to_html(md: str) -> str:
    parser = CommonMark.Parser()
    ast = parser.parse(md)
    return CommonMark.HtmlRenderer().render(ast)


def difference_of_dictionaries(a: dict, b: dict):
    """
    Calculates a \ b like if a and b were sets.
    For example,
    difference_of_dictionaries({'a': 'A', 'b': 'B'}, {'a': 'A'}) is {'b': 'B'}
    :param b: a dictionary
    :param a: a dictionary
    """
    a_tuple = tuple((key, value) for (key, value) in a.items())
    b_tuple = tuple((key, value) for (key, value) in b.items())
    c_set = set(a_tuple) - set(b_tuple)
    c = {}
    for key, value in c_set:
        c[key] = value
    return c


# http://stackoverflow.com/a/1007615/4246963
def urlify(s):
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)
    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s
