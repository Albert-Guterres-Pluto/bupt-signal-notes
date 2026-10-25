#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""把渲染出来的 PNG 幻灯片转成 JPEG 并缩到长边 1600px（供笔记引用 / 控制仓库体积）。

渲染器输出的是 PNG，但笔记统一引用 .jpg —— 本脚本补上这一步。
幂等：已有同名 jpg 的跳过；转换成功后删除源 png（除非 --keep-png）。

用法:
  python _tools\upscale.py                 # 处理 assets/ 与 _tools/ 下所有 slides* 目录
  python _tools\upscale.py assets\slides3  # 只处理指定目录
  python _tools\upscale.py --keep-png      # 保留 png
"""
import os, sys, glob, io
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAXW = 1600
QUALITY = 84

args = [a for a in sys.argv[1:] if not a.startswith("--")]
KEEP_PNG = "--keep-png" in sys.argv

if args:
    targets = [os.path.abspath(a) for a in args]
else:
    targets = sorted(glob.glob(os.path.join(ROOT, "assets", "slides*"))) + \
              sorted(glob.glob(os.path.join(HERE, "slides*")))

total_in = total_out = grand = 0
for d in dict.fromkeys(targets):
    if not os.path.isdir(d):
        continue
    pngs = sorted(glob.glob(os.path.join(d, "*.png")))
    if not pngs:
        continue
    before = after = made = skipped = 0
    for f in pngs:
        jpg = f[:-4] + ".jpg"
        before += os.path.getsize(f)
        if os.path.exists(jpg):
            skipped += 1
            after += os.path.getsize(jpg)
        else:
            im = Image.open(f).convert("RGB")
            w, h = im.size
            if w > MAXW:
                im = im.resize((MAXW, round(h * MAXW / w)), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=QUALITY, optimize=True, subsampling=0)
            with open(jpg, "wb") as fh:
                fh.write(buf.getvalue())
            after += len(buf.getvalue())
            made += 1
        if not KEEP_PNG:
            os.remove(f)
    grand += made
    total_in += before
    total_out += after
    print(f"{os.path.relpath(d, ROOT):26} png {len(pngs):>4} → 新转 {made:>4} (已存在 {skipped:>3})  "
          f"{before/1048576:6.1f} MB → {after/1048576:6.1f} MB")

print(f"\n共转换 {grand} 张  {total_in/1048576:.1f} MB → {total_out/1048576:.1f} MB")
