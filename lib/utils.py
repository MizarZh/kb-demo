from stdlib_list import stdlib_list
import os
from pathlib import PurePath

def gen_dire_tree(path: str):
    directory_dict = {}
    for root, _, files in os.walk(path):
        P_root = PurePath(root)
        directory_dict[P_root.as_posix()] = files
    return directory_dict

def gen_stdlib_list(version: str):
    return stdlib_list(version)

def to_posix_path(path: str):
    return PurePath(path).as_posix()