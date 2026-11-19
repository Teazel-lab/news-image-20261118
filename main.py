#!/usr/bin/env python3
# Copies entry.png beside this script to /output/entry.png for the make.fun grader.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")

os.makedirs(DEST_DIR, exist_ok=True)
shutil.copy2(SRC, DEST)
print(DEST)
