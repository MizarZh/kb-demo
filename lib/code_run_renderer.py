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
                        # if it's not relative, then we need to identify where it comes from
                        # from file, stdlib or PyPI
                        # considering adding more function to whl?
                        # if it's relative, leave it be, let the interpreter handle it
                        for x in node.names:
                            if x.name[0] != '.':
                                self.abs_import_recognize(x.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module[0] != '.':
                            self.abs_import_recognize(node.module)
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

    def abs_import_recognize(self, name: str):
        name_list = name.split('.')
        name_path = name.replace('.', '/')
        name_path_without_last = '/'.join(name_list[:-1])
        import_append_flag = True
        if name != '':
            # first layer
            if len(name_list) == 1:
                # first layer of lib
                if name in self.local_dire_tree and '__init__.py' in self.local_dire_tree[name]:
                    import_append_flag = False
                # first layer of file
                elif name + '.py' in self.local_dire_tree['.']:
                    import_append_flag = False
            # path referrs to a module with __init__.py
            if name_path in self.local_dire_tree:
                if '__init__.py' in self.local_dire_tree[name_path]:
                    import_append_flag = False
            # path referrs to a file
            elif name_path_without_last in self.local_dire_tree:
                if name_list[-1] + '.py' in self.local_dire_tree[name_path_without_last]:
                    import_append_flag = False
            # this path is not in the directory
            elif name_list[0] in self.stdlib_list:
                    import_append_flag = False
                # if module is in stdlib
            if import_append_flag:
                self.imports.append(name_list[0]) # get outermost package
