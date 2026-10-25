#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""从工作区的 _tools/_extract/ 抽取轻量元数据, 供仓库内校验使用。

仓库里不放课件和提取中间产物（体积）, 但校验需要:
- 每份课件的幻灯片总数与"幻灯片序号 → 渲染图页码"映射（隐藏页信息）
- 每份课件打勾用的 DEKCS 定义

产出: tools/deck-meta.json
"""
import os, sys, json, glob
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
EXTRACT = os.path.join(HERE, "_extract")
OUT = os.path.abspath(os.path.join(ROOT, "..", "信号分析与处理-笔记", "tools", "deck-meta.json"))

# 课件清单直接复用 decks.py（自动发现，新增课件无需改这里）
from decks import decks as discover

meta = {"decks": []}
for d in discover():
    pm_p = os.path.join(d["extract_dir"], "pagemap.json")
    if not os.path.exists(pm_p):
        print("缺少 pagemap:", d["extract_dir"])
        continue
    pm = json.load(open(pm_p, encoding="utf-8"))
    slides = max(int(k) for k in pm["slide_to_page"])
    hidden = [int(k) for k, v in pm["slide_to_page"].items() if v is None]
    meta["decks"].append(dict(dir=d["notes"], images=d["images"], source=d["source"],
                              slides=slides, hidden=sorted(hidden),
                              slide_to_page=pm["slide_to_page"]))
    print(f"{d['notes']:32} {d['images']:10} {slides:>4} 页, 隐藏页 {sorted(hidden) if hidden else '无'}")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=1)
print("已写入:", OUT)
