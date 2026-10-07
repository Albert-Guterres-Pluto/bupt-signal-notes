#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""统计 assets 下有多少渲染图被笔记实际引用, 以及被删图后变成"孤儿"的图片。

用法: python _tools\orphans.py [--list]
"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

used = set()
for md in glob.glob(os.path.join(ROOT, "笔记", "**", "*.md"), recursive=True):
    t = open(md, encoding="utf-8").read()
    for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', t):
        link = m.group(1).replace("\\", "/")
        # 笔记里是 ../../assets/slidesNN/page-XXXX.jpg, 归一化为 资产目录名/文件名
        parts = link.split("/")
        for i, seg in enumerate(parts):
            if seg == "assets" and i + 2 < len(parts) + 1:
                used.add("/".join(parts[i + 1:]))
                break

allimg = {}
for p in glob.glob(os.path.join(ROOT, "assets", "**", "*.jpg"), recursive=True):
    rel = os.path.relpath(p, os.path.join(ROOT, "assets")).replace("\\", "/")
    allimg[rel] = p

orphan = sorted(set(allimg) - used)
print(f"assets 图片总数: {len(allimg)}")
print(f"被笔记引用:     {len(set(allimg) & used)}")
print(f"未被引用(孤儿): {len(orphan)}")
if "--list" in sys.argv:
    for o in orphan:
        print("  ", o)
size = sum(os.path.getsize(allimg[o]) for o in orphan)
print(f"孤儿图片占用:   {size/1048576:.1f} MB")
