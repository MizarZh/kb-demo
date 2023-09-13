from md_parser import get_markdown_document, render_html, render_ast, render_mpm

doc = get_markdown_document('../example/test.md')
# render_html(doc)
# render_ast(doc)
render_mpm(doc)