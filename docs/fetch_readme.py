"""
@Author: Conghao Wong
@Date: 2024-12-04 09:44:45
@LastEditors: Conghao Wong
@LastEditTime: 2026-09-28 15:15:00
@Github: https://cocoon2wong.github.io
@Copyright 2026 Conghao Wong, All Rights Reserved.
"""

from pathlib import Path
import re
import shutil

SOURCE_FILE = Path('__pages/guidelines.md')
BACKUP_FILE = Path('__pages/guidelines.md.backup')

README_SOURCE = Path('../README.md')

START_LINE = '## Getting Started'


if __name__ == '__main__':
    # Ensure destination directory exists
    SOURCE_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Backup old file if it exists
    if SOURCE_FILE.exists():
        shutil.copy(SOURCE_FILE, BACKUP_FILE)

    # Read README from repo root
    with open(README_SOURCE, 'r', encoding='utf-8') as f:
        new_lines = f.readlines()

    # Find start section
    start_index = None
    for i, line in enumerate(new_lines):
        if line.startswith(START_LINE):
            start_index = i
            break

    if start_index is None:
        raise RuntimeError(f'Cannot find section "{START_LINE}" in README.md')

    # Append content
    with open(SOURCE_FILE, 'a+', encoding='utf-8') as f:
        f.writelines(new_lines[start_index:])

    # Anti-crawler: replace email @xxx.com with [at-mark}xxx.com
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(
        r'(?<=[a-zA-Z0-9_.+-])@([a-zA-Z0-9.-]+\.com)\b',
        r'[at-mark}\1',
        content,
    )

    with open(SOURCE_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
