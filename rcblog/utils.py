import re

import CommonMark

from rcblog import data


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


# based on
# https://siongui.github.io/2012/10/11/python-parse-accept-language-in-http-request-header/
def parse_accept_language(accept_language):
    languages = accept_language.split(",")
    locales = {}

    for language in languages:
        if language.split(";")[0] == language:
            # no q => q = 1
            locales[language.strip()] = 1.0
        else:
            locale = language.split(";")[0].strip()
            if '-' in locale:  # I don't care about difference between en-US and en-GB
                locale = locale.split('-')[0].lower()
            q = language.split(";")[1].split("=")[1]
            if locale in locales:
                if locales[locale] < float(q):
                    continue
            locales[locale] = float(q)

    iso_639_1 = sorted(locales, key=lambda l: locales[l], reverse=True)
    iso_639_3 = []
    for language in iso_639_1:
        if language in data.ISO_639_1_TO_ISO_639_3:
            iso_639_3.append(data.ISO_639_1_TO_ISO_639_3[language])
    return iso_639_3

if __name__ == '__main__':
    print(parse_accept_language(accept_language='da, en-gb;q=0.8, en;q=0.7'))
