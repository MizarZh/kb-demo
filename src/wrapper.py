
def HTML_wrapper(html_raw: str):
    first = '''
<html>
  <head>
    <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
    <script defer src="https://pyscript.net/latest/pyscript.js"></script>
  </head>
  <body>
  <py-config type="toml">
    packages = ["numpy", "matplotlib"]
  </py-config>
  <div id="plot"></div>
'''
    second = '''
  </body>
</html>
'''
    return first + html_raw + second