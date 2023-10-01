import html
from mistletoe.block_token import BlockToken, BlockCode
from mistletoe.html_renderer import HtmlRenderer
from mistletoe import block_token
import ast
from .config import pyscript_local_root, pyscript_from, python_version, pyscript_path
from .utils import gen_dire_tree, gen_stdlib_list, to_posix_path
import os

class CodeRunningRenderer(HtmlRenderer):
    def __init__(self):
        super().__init__(BlockCode)
        self.imports = []
        self.local_dire_tree = gen_dire_tree(pyscript_local_root)
        self.stdlib_list = gen_stdlib_list(python_version)

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
                            self.abs_import_recognize(x.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        # if it's not relative, then it's same case as before
                        # if it's relative, leave it be, let the interpreter handle it
                        if node.module[0] != '.':
                            self.abs_import_recognize(node.module.split('.')[0])
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
        fetch_block = []
        for folder in self.local_dire_tree:
            fetch_block.append(
                '''
            [[fetch]]
            from = "{path}"
            files = {files}
            to_folder = "{to}"
            '''.format(path=to_posix_path(os.path.join(pyscript_path, folder)), files=self.local_dire_tree[folder], to=folder)
            )
        fetch_block = '\n\n'.join(fetch_block)
        return '''
            <html>
            <head>
                <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
                <script defer src="https://pyscript.net/latest/pyscript.js"></script>
            </head>
            <body>
            <py-config type="toml">
                packages = {packages}

                {fetch}
            </py-config>
            <div id="plot"></div>
            {doc}
            </body>
            </html>
            '''.format(packages=self.imports, fetch = fetch_block, doc = doc)

    def abs_import_recognize(self, name):
        # .split('.')[0] is to get out the name of the outermost package
        # pkg_name not null, not in the local directory of the same level
        # and not in stdlib, can be added to imports
        print(self.local_dire_tree)
        if name != ''  \
                and name not in self.local_dire_tree[to_posix_path(pyscript_local_root)] \
                and name not in self.stdlib_list:
            self.imports.append(name)
