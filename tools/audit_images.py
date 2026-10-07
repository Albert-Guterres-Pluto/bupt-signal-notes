#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""盘点笔记里的插图: 按 课件页 统计其"信息形态", 为精简提供依据。

分类依据 (尽量用客观信号, 不靠猜):
- name        : 图名/alt 里出现"演示"等字样
- slide_kind  : 该页在提取文本里的形态 (课堂演示 / 交互 / 纯文字 / 含公式 / 含表格)
- html_video  : 该页是否内嵌 HTML/video 等动态内容 (提取文本里含 <html / <video)
- ink         : 该页渲染图的"非背景墨迹占比" (纯文字页墨迹很低, 图多的页较高)
"""
import os, re, sys, glob, json
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXTRACT = os.path.join(HERE, "_extract")

DECKS = [
    ("01-信号分析与处理概述", "slides01", r"_信号分析与处理_01_20260915"),
    ("02-1-连续时间信号分析", "slides21", r"_信号分析与处理_2.1节-20260920"),
    ("02-2-连续时间信号的频域分析", "slides22", r"_信号分析与处理_2.2节-20260920"),
]
ENTRY = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
FNAME = re.compile(r'page-(\d{4})\.jpg')


def ink_ratio(path):
    """非背景像素占比: 幻灯片底色近白, 文字与图形算墨迹。"""
    im = Image.open(path).convert("L").resize((320, 180))
    a = np.asarray(im, dtype=np.int16)
    return float((a < 230).mean())


report = {}
for deck, asset, ext in DECKS:
    ddir = os.path.join(ROOT, "笔记", deck)
    adir = os.path.join(ROOT, "assets", asset)
    slides_dir = os.path.join(EXTRACT, ext, "slides")
    rows = []
    for md in sorted(glob.glob(os.path.join(ddir, "*.md"))):
        txt = open(md, encoding="utf-8").read()
        for m in ENTRY.finditer(txt):
            alt, link = m.group(1), m.group(2)
            fm = FNAME.search(link)
            if not fm:
                continue
            page = int(fm.group(1))
            sp = os.path.join(slides_dir, f"slide_{page:03d}.md")
            raw = open(sp, encoding="utf-8").read() if os.path.exists(sp) else ""
            kind = []
            if "课堂演示" in raw or "演示" in alt:
                kind.append("演示")
            if "<html" in raw.lower() or "<video" in raw.lower():
                kind.append("H5")
            if "[公式]" in raw or "OLE" in raw:
                kind.append("公式")
            if "[TABLE]" in raw:
                kind.append("表格")
            n_text = len(re.findall(r'\[TEXT\]', raw))
            if n_text >= 1 and not kind:
                kind.append("文字")
            img = os.path.join(adir, f"page-{page:04d}.jpg")
            ink = ink_ratio(img) if os.path.exists(img) else -1
            rows.append(dict(file=os.path.basename(md), page=page, alt=alt,
                             kinds=",".join(kind), ink=round(ink, 3),
                             ntext=n_text, has_img="[IMAGE]" in raw))
    report[deck] = rows

print(f"{'篇':34} {'插图':>4} {'含演示':>6} {'含H5':>5} {'公式页':>6} {'表格页':>6} {'纯文字页':>7} {'均墨迹':>7}")
tot = 0
for deck, rows in report.items():
    n = len(rows)
    tot += n
    def c(k):
        return sum(1 for r in rows if k in r["kinds"])
    inks = [r["ink"] for r in rows if r["ink"] >= 0]
    print(f"{deck:34} {n:>4} {c('演示'):>6} {c('H5'):>5} {c('公式'):>6} {c('表格'):>6} "
          f"{sum(1 for r in rows if r['kinds']=='文字'):>7} {np.mean(inks):>7.3f}")
print(f"{'合计':34} {tot:>4}")

print("\n--- 墨迹最少的 25 张 (空白/纯文字嫌疑, 优先删) ---")
allrows = [(r, d) for d, rows in report.items() for r in rows]
for r, d in sorted(allrows, key=lambda x: x[0]["ink"])[:25]:
    print(f"  {r['ink']:.3f}  {d[:12]:12} {r['file'][:26]:28} p{r['page']:<4} [{r['kinds']:8}] {r['alt'][:46]}")

json.dump(report, open(os.path.join(HERE, "image_audit.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n明细已写入 _tools/image_audit.json")
