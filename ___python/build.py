from __future__ import annotations
import shutil
import os

from tocify import tocify
from Utils import SOURCE_DIR, TARGET_DIR

if os.path.exists(TARGET_DIR):
    shutil.rmtree(TARGET_DIR)
shutil.copytree(SOURCE_DIR, TARGET_DIR)
tocify()