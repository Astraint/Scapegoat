from __future__ import annotations
import os, fnmatch, subprocess

from typing import Union, List, Tuple

import re

TAB = "    "
SOURCE_DIR : str = "../source/"
TARGET_DIR : str = "../__build/"

def find(pattern : str, start_dir : str) -> Union[str, None]:
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                return os.path.relpath(os.path.join(root, file), start_dir)
    return None

def find_all(pattern : str, start_dir : str) -> List[str]:
    results : List[str] = []
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                results.append(os.path.relpath(os.path.join(root, file), start_dir))
    return results

def relpath(file_A : str, file_B : str) -> str:
    file_B : str = "/".join(file_B.split("/")[:-1])
    return os.path.relpath(file_A, file_B)

def count_lstrip(line : str, char : str) -> Tuple[str, int]:
    count = 0
    for c in line: 
        if c == char: count += 1
        else: break
    return (line.lstrip(char), count)
            

def markdownify(s : str) -> str:
    # Remove special characters, punctuation, and spaces
    cleaned_name = re.sub(r'[^\w\s-]', '', s)
    
    # Replace spaces with dashes and convert to lowercase
    reference = cleaned_name.replace(' ', '-').lower()
    
    return reference

def run(command : str) -> Tuple[str, str]:
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return process.communicate()