from stdlib_list import stdlib_list
import os
from pathlib import PurePath

def gen_dire_tree(path: str):
    current_cwd = os.getcwd()
    directory_dict = {}
    os.chdir(path)
    for root, _, files in os.walk('.'):
        P_root = PurePath(root)
        directory_dict[P_root.as_posix()] = files
    os.chdir(current_cwd)
    return directory_dict

def gen_stdlib_list(version: str):
    return stdlib_list(version)

def to_posix_path(path: str):
    return PurePath(path).as_posix()