import html
from mistletoe.block_token import BlockToken, BlockCode
from mistletoe.html_renderer import HtmlRenderer
from mistletoe import block_token
import ast


class CodeRunningRenderer(HtmlRenderer):
    def __init__(self):
        super().__init__(BlockCode)
        self.imports = []
        self.files = []

    def render_block_code(self, token: BlockCode) -> str:
        template = '<pre><{elem}{attr}>{inner}</{elem}></pre>'
        elem = 'code'
        attr = ''
        inner = self.escape_html_text(token.content)
        code_block_parameter = token.language.split('-')
        # Display code block
        if len(code_block_parameter) == 0:
            if token.language:
                attr = ' class="{}"'.format(
                    'language-{}'.format(html.escape(token.language)))
            else:
                attr = ''
        # Frontend running code
        elif 'frontend' in code_block_parameter:
            if 'python' in code_block_parameter:
                elem = 'py-script'
                inner_ast_tree = ast.parse(inner)
                for node in ast.walk(inner_ast_tree):
                    if isinstance(node, ast.Import):
                        for x in node.names:
                            # .split('.')[0] is to get out the name of the outermost package
                            self.imports.append(x.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                            self.imports.append(node.module.split('.')[0])
                print(self.imports)
        # Backend running code, default running mode
        # 'backend' in code_block_parameter
        else:
            pass
        return template.format(elem=elem, attr=attr, inner=inner)

    def render_document(self, token: block_token.Document) -> str:
        self.footnotes.update(token.footnotes)
        inner = '\n'.join([self.render(child) for child in token.children])
        doc = '{}\n'.format(inner) if inner else ''
        return self.wrapper(doc)

    def wrapper(self, doc: str) -> str:
        first = '''
    <html>
    <head>
        <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
        <script defer src="https://pyscript.net/latest/pyscript.js"></script>
    </head>
    <body>
    <py-config type="toml">
        packages = {}
        [[fetch]]
        files = ['test.py']
        from = './static/'
    </py-config>
    <div id="plot"></div>
    '''.format(self.imports)
        second = '''
    </body>
    </html>
    '''
        return first + doc + second
