#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""校验合并笔记: 插图链接、目录锚点、单章链接、代码块闭合。"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.join(ROOT, "信号分析与处理-完整笔记.md")

t = open(P, encoding="utf-8").read()
imgs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', t)
bad = [i for i in imgs if not os.path.exists(os.path.join(ROOT, i.replace("/", os.sep)))]
print(f"插图链接 {len(imgs)} 条, 失效 {len(bad)}")
for b in bad[:10]:
    print("   BAD", b)

anchors = set(re.findall(r'<a id="([^"]+)"></a>', t))
links = re.findall(r'\]\(#([^)]+)\)', t)
badl = [l for l in links if l not in anchors]
print(f"目录锚点 {len(links)} 条, 失效 {len(badl)}")
for b in badl[:10]:
    print("   BAD #" + b)

mds = re.findall(r'\]\((笔记/[^)]+\.md)\)', t)
badmd = [m for m in mds if not os.path.exists(os.path.join(ROOT, m.replace("/", os.sep)))]
print(f"指向单章文件的链接 {len(mds)} 条, 失效 {len(badmd)}")
for b in badmd[:5]:
    print("   BAD", b)

fences = t.count("```")
print(f"代码块围栏 {fences} 个 ({'闭合正常' if fences % 2 == 0 else '⚠ 未闭合'})")
print(f"字符数 {len(t)} | 行数 {t.count(chr(10)) + 1} | 体积 {os.path.getsize(P)/1048576:.2f} MB")
print("章节标题数:", len(re.findall(r'^## \d+\. ', t, re.M)))
print("篇标题数:", len(re.findall(r'^# 第[一二三]篇', t, re.M)))
