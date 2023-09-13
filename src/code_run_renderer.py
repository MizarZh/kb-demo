import html
from mistletoe.block_token import BlockToken, BlockCode
from mistletoe.html_renderer import HtmlRenderer

class CodeRunningRenderer(HtmlRenderer):
    def __init__(self):
        super().__init__(BlockCode)

    def render_block_code(self, token: BlockCode) -> str:
        template = '<pre><{elem}{attr}>{inner}</{elem}></pre>'
        elem = 'code'
        attr = ''
        if token.language == 'python-run':
            elem = 'py-script'
        elif token.language:
            attr = ' class="{}"'.format('language-{}'.format(html.escape(token.language)))
        else:
            attr = ''
        inner = self.escape_html_text(token.content)
        return template.format(elem=elem, attr=attr, inner=inner)
