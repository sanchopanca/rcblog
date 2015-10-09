import CommonMark


def md_to_html(md: str) -> str:
    parser = CommonMark.DocParser()
    ast = parser.parse(md)
    return CommonMark.HTMLRenderer().render(ast)
