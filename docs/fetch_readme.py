"""
@Author: Conghao Wong
@Date: 2024-12-04 09:44:45
@LastEditors: Conghao Wong
@LastEditTime: 2026-01-29 20:42:49
@Github: https://cocoon2wong.github.io
@Copyright 2024 Conghao Wong, All Rights Reserved.
"""

import shutil
from pathlib import Path

SOURCE_FILE = Path('./guidelines.md')
BACKUP_FILE = SOURCE_FILE.with_suffix('.md.backup')

README_SOURCE = Path('../README.md')

START_LINE = '## Getting Started'


if __name__ == '__main__':
    # ------
    # Backup
    # ------
    shutil.copy(SOURCE_FILE, BACKUP_FILE)

    # -----------
    # Read README
    # -----------
    with open(README_SOURCE, 'r') as f:
        new_lines = f.readlines()

    # ------------------
    # Find start section
    # ------------------
    start_index = None
    for i, line in enumerate(new_lines):
        if line.startswith(START_LINE):
            start_index = i
            break

    if start_index is None:
        raise RuntimeError(f'Cannot find section "{START_LINE}" in README.md')

    # --------------
    # Append content
    # --------------
    with open(SOURCE_FILE, 'a+', encoding='utf-8') as f:
        f.writelines(new_lines[start_index:])
