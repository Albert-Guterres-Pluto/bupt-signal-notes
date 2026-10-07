#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检测 pptx 中隐藏的幻灯片, 并建立 slide序号 -> PDF物理页 映射。

若 show="0" 的幻灯片 LibreOffice 不导出, 则物理页 = 非隐藏幻灯片顺序号。
"""
import os, re, sys, json, zipfile, glob
from lxml import etree
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"

decks = [
    ("01.pdf", r"_extract\_信号分析与处理_01_20260915"),
    ("2.1.pdf", r"_extract\_信号分析与处理_2.1节-20260920"),
    ("2.2fix.pdf", r"_extract\_信号分析与处理_2.2节-20260920"),
]
for pdf, ext in decks:
    d = os.path.join(HERE, ext)
    man = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
    src = os.path.join(WORK, man["source"])
    z = zipfile.ZipFile(src)
    names = set(z.namelist())
    slide_names = sorted((n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                         key=lambda n: int(re.findall(r"\d+", os.path.basename(n))[0]))
    hidden = []
    for i, sn in enumerate(slide_names, 1):
        raw = z.read(sn)
        try:
            root = etree.fromstring(raw)
        except etree.XMLSyntaxError:
            txt = raw.decode("utf-8", "replace")
            txt = re.sub(r'\s([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*"([^"]*)"',
                         lambda mm: '' if len(mm.group(2)) > 100000 else mm.group(0), txt)
            root = etree.fromstring(txt.encode("utf-8"))
        if root.get("show") == "0":
            hidden.append(i)
    z.close()
    m = {"pdf": pdf, "slide_to_page": {}, "hidden": hidden}
    page = 0
    for i in range(1, len(slide_names) + 1):
        if i in hidden:
            m["slide_to_page"][str(i)] = None
        else:
            page += 1
            m["slide_to_page"][str(i)] = page
    with open(os.path.join(d, "pagemap.json"), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
    print(f"{man['source']}: total={len(slide_names)} hidden={hidden} -> 末页物理页号={page}")
    if hidden:
        for h in hidden:
            print(f"    slide {h} 隐藏 (不导出)")
