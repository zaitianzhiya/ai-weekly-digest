#!/usr/bin/env python3
"""将 Obsidian 笔记从项目目录同步到 Z:\知识库\学习知识库\AI学习"""

import shutil
from pathlib import Path

# 源目录：项目中的 obsidian-notes
SRC = Path(__file__).resolve().parent.parent / "obsidian-notes"
# 目标目录：Z:\知识库\学习知识库\AI学习
DST = Path(r"Z:\知识库\学习知识库\AI学习\03 - 主流进化方向\AI每周发展摘要")

# 确保目标目录存在
DST.mkdir(parents=True, exist_ok=True)
print(f"目标目录: {DST}")

# 复制所有 .md 文件
copied = []
for f in sorted(SRC.glob("*.md")):
    dst_file = DST / f.name
    shutil.copy2(f, dst_file)
    copied.append(f.name)
    print(f"  ✓ {f.name}")

print(f"\n同步完成: {len(copied)} 个文件")
for name in copied:
    print(f"  → {name}")
