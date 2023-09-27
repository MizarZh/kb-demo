from mistletoe import Document
from mistletoe.block_token import BlockToken, BlockCode, CodeFence
from mistletoe.html_renderer import HtmlRenderer
from mistletoe.ast_renderer import AstRenderer
from lib.code_run_renderer import CodeRunningRenderer

def get_markdown_document(path: str):
    f = open(path)
    doc = Document(f.read())
    f.close()
    return doc

def render_html(doc: Document):
    renderer = HtmlRenderer()
    html = renderer.render(doc)
    print(html)


def render_ast(doc: Document):
    renderer = AstRenderer()
    html = renderer.render(doc)
    print(html)

def markdown2html(path: str):
    f = open(path)
    doc = Document(f.read())
    f.close()
    renderer = CodeRunningRenderer()
    return renderer.render(doc)
