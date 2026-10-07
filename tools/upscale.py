#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 110dpi 渲染 PNG 放大 1.7x (Lanczos) 并转 JPEG, 提升笔记内嵌图清晰度并控制体积。"""
import os, sys, glob
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
SCALE = 1.7
QUALITY = 92

for d in sorted(glob.glob(os.path.join(ASSETS, "slides*"))):
    srcs = sorted(glob.glob(os.path.join(d, "page-*.png")))
    tot_in = tot_out = 0
    for s in srcs:
        tot_in += os.path.getsize(s)
        im = Image.open(s).convert("RGB")
        w, h = im.size
        im2 = im.resize((int(w * SCALE), int(h * SCALE)), Image.LANCZOS)
        out = s[:-4] + ".jpg"
        im2.save(out, "JPEG", quality=QUALITY, optimize=True, subsampling=0)
        tot_out += os.path.getsize(out)
        os.remove(s)
    print(f"{os.path.basename(d)}: {len(srcs)} imgs  {tot_in/1048576:.1f} MB -> {tot_out/1048576:.1f} MB "
          f"(avg {tot_out/max(len(srcs),1)/1024:.0f} KB/img, {int(w*SCALE)}x{int(h*SCALE)})")
