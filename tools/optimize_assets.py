#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""优化 assets 下的幻灯片渲染图, 让 markdown 预览更快。

原图 2493x1402 / 平均 290 KB, 356 张共 ~103 MB; VSCode 预览加载几十张就明显卡顿甚至显示不出。
统一缩到长边 MAXW 并重新编码为 JPEG, 总体积约降到 1/2, 文字与公式仍清晰。
幂等: 已小于目标宽度的图片不会被再次放大, 只会重新编码一次。
"""
import os, sys, glob, io
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
MAXW = 1600
QUALITY = 84

before = after = 0
n = 0
for f in sorted(glob.glob(os.path.join(ASSETS, "**", "*.jpg"), recursive=True)):
    size0 = os.path.getsize(f)
    im = Image.open(f).convert("RGB")
    w, h = im.size
    if w > MAXW:
        im = im.resize((MAXW, round(h * MAXW / w)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=QUALITY, optimize=True, subsampling=0)
    data = buf.getvalue()
    if len(data) < size0:
        with open(f, "wb") as fh:
            fh.write(data)
        after += len(data)
    else:
        after += size0
    before += size0
    n += 1

print(f"处理 {n} 张: {before/1048576:.1f} MB -> {after/1048576:.1f} MB "
      f"(平均 {after/n/1024:.0f} KB/张, 长边 {MAXW}px)")
