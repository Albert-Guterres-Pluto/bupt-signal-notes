#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""校验笔记插图说明里的 "课件 slide N / 第 P 页" 是否与 pagemap 一致, 且 P 与文件名匹配。"""
import os, re, sys, glob, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXTRACT = os.path.join(HERE, "_extract")

DECKS = {
    "slides01": r"_信号分析与处理_01_20260915",
    "slides21": r"_信号分析与处理_2.1节-20260920",
    "slides22": r"_信号分析与处理_2.2节-20260920",
}
maps = {}
META_P = os.path.join(HERE, "deck-meta.json")
for k, d in DECKS.items():
    p = os.path.join(EXTRACT, d, "pagemap.json")
    if os.path.exists(p):
        maps[k] = json.load(open(p, encoding="utf-8"))["slide_to_page"]
if not maps and os.path.exists(META_P):
    # 仓库模式: 用轻量元数据代替 _extract
    for d in json.load(open(META_P, encoding="utf-8"))["decks"]:
        maps[d["images"]] = d["slide_to_page"]
NOTES_DIR = os.path.join(ROOT, "笔记" if os.path.isdir(os.path.join(ROOT, "笔记")) else "notes")

# 说明文字与链接可能在同一行不同位置: 先取每张图的 alt, 再取链接
ENTRY = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
SLIDE = re.compile(r'slide\s*([0-9]+)')
PAGE = re.compile(r'第\s*([0-9]+)\s*页')
FNAME = re.compile(r'page-(\d{4})\.jpg')

bad, checked, noanno = [], 0, 0
for md in sorted(glob.glob(os.path.join(NOTES_DIR, "**", "*.md"), recursive=True)):
    rel = os.path.relpath(md, ROOT)
    txt = open(md, encoding="utf-8").read()
    for m in ENTRY.finditer(txt):
        alt, link = m.group(1), m.group(2)
        fm = FNAME.search(link)
        if not fm:
            continue
        file_page = int(fm.group(1))
        deck = None
        for k in DECKS:
            if f"{k}/" in link.replace("\\", "/"):
                deck = k
        if deck is None:
            bad.append(f"[无法判定所属课件] {rel} -> {link}")
            continue
        sm = SLIDE.search(alt)
        pm = PAGE.search(alt)
        if sm and pm:
            slide, page = int(sm.group(1)), int(pm.group(1))
            expected = maps[deck].get(str(slide))
            checked += 1
            if expected is None:
                bad.append(f"[该 slide 为隐藏页却引用了插图] {rel}: slide {slide}")
            elif expected != page:
                bad.append(f"[页码标注不符] {rel}: slide {slide} 应={expected}, 文字写={page}")
            if page != file_page:
                bad.append(f"[文字页码与文件名不符] {rel}: 文字={page}, 文件={file_page}")
        elif sm and not pm:
            bad.append(f"[有 slide 号却无页码] {rel}: {alt[:60]}")
        else:
            noanno += 1
            # 无 slide 标注时, 至少人工可核对; 记录以便统计

print(f"校验带 'slide N / 第 P 页' 标注的插图: {checked} 张")
print(f"仅有说明、无页码标注的插图: {noanno} 张 (需人工阅读, 不参与自动校验)")
print()
if bad:
    print(f"❌ {len(bad)} 个问题:")
    for b in bad:
        print("  -", b)
    sys.exit(1)
print("✅ 全部插图的 slide↔page 标注与 pagemap 一致")
