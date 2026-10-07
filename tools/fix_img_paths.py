#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""统一笔记中的插图相对路径。

笔记位于 笔记/<deck>/xxx.md, 图片位于 根目录/assets/slidesNN/,
因此正确相对路径是 ../../assets/slidesNN/page-XXXX.jpg。
本脚本把任何 ../assets/ 归一化为 ../../assets/ (幂等, 可重复运行)。
"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NOTES = os.path.join(ROOT, "笔记")

BAD = re.compile(r'(?<!\.\./)\.\./assets/')
total_files = total_fixes = 0
for md in sorted(glob.glob(os.path.join(NOTES, "**", "*.md"), recursive=True)):
    txt = open(md, encoding="utf-8").read()
    new, n = BAD.subn(r'../../assets/', txt)
    if n:
        open(md, "w", encoding="utf-8").write(new)
        total_files += 1
        total_fixes += n
        print(f"fixed {n:>3} links  {os.path.relpath(md, ROOT)}")
print(f"\n共修复 {total_fixes} 条链接, 涉及 {total_files} 个文件")

# 复验
bad = []
for md in sorted(glob.glob(os.path.join(NOTES, "**", "*.md"), recursive=True)):
    txt = open(md, encoding="utf-8").read()
    for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', txt):
        t = m.group(1).strip()
        if t.startswith(("http://", "https://")):
            continue
        p = os.path.normpath(os.path.join(os.path.dirname(md), t.replace("/", os.sep)))
        if not os.path.exists(p):
            bad.append(f"{os.path.relpath(md, ROOT)} -> {t}")
if bad:
    print(f"\n❌ 仍有 {len(bad)} 条链接无效:")
    for b in bad:
        print("  -", b)
else:
    print("\n✅ 所有插图链接均指向真实文件")
