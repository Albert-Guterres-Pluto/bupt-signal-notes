#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检测 pptx 中隐藏的幻灯片, 并建立 slide序号 -> PDF物理页 映射。

自动发现 _tools/_extract/ 下所有已提取的课件，逐个生成 pagemap.json。
若 show="0" 的幻灯片 LibreOffice 不导出, 则物理页 = 非隐藏幻灯片顺序号。
"""
import os, re, sys, json, zipfile, glob
from lxml import etree

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXTRACT = os.path.join(HERE, "_extract")


def safe_parse(raw):
    try:
        return etree.fromstring(raw)
    except etree.XMLSyntaxError:
        txt = raw.decode("utf-8", "replace")
        txt = re.sub(r'\s([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*"([^"]*)"',
                     lambda m: '' if len(m.group(2)) > 100000 else m.group(0), txt)
        return etree.fromstring(txt.encode("utf-8"))


total = 0
for d in sorted(glob.glob(os.path.join(EXTRACT, "*"))):
    mf = os.path.join(d, "manifest.json")
    if not os.path.exists(mf):
        continue
    man = json.load(open(mf, encoding="utf-8"))
    src = os.path.join(ROOT, man["source"])
    if not os.path.exists(src):
        print(f"跳过（课件已不在）: {man['source']}")
        continue
    z = zipfile.ZipFile(src)
    names = set(z.namelist())
    slide_names = sorted((n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                         key=lambda n: int(re.findall(r"\d+", os.path.basename(n))[0]))
    hidden = []
    for i, sn in enumerate(slide_names, 1):
        root = safe_parse(z.read(sn))
        if root.get("show") == "0":
            hidden.append(i)
    m = {"pdf": None, "slide_to_page": {}, "hidden": hidden}
    page = 0
    for i in range(1, len(slide_names) + 1):
        if i in hidden:
            m["slide_to_page"][str(i)] = None
        else:
            page += 1
            m["slide_to_page"][str(i)] = page
    with open(os.path.join(d, "pagemap.json"), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
    total += 1
    print(f"{man['source']}: 总 {len(slide_names)} 页, 隐藏 {hidden if hidden else '无'} "
          f"→ 导出 {page} 页")
    for h in hidden:
        print(f"    slide {h} 隐藏（不导出）")
print(f"\n共处理 {total} 份课件")
