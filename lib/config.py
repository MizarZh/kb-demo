import os
from .utils import to_posix_path

pyscript_domain = 'http://127.0.0.1:8000/'
pyscript_path = 'static'
pyscript_from = to_posix_path(os.path.join(pyscript_domain, pyscript_path))

pyscript_local_root = './example'

python_version = '3.9'