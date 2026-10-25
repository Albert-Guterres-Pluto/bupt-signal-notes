#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""用 PowerPoint(COM) 重导出全部课件渲染图，替换 assets/。

为什么：LibreOffice 导出 PDF 时会把 MathType 公式 / Visio 对象的多个内部单元
全部画出来（叠印），这类页在 01/2.1/2.2/2.3/第3章/第4章 都有。PowerPoint 自身导出
是真正的最终态，干净且更快。

流程（每份课件）:
  1) 调 ppt_export.ps1 把全部幻灯片导出成 page-<slide>.png
  2) 按 pagemap.json 把 slide 号映射成"导出页号"（跳过隐藏页）
  3) 写进 assets/slidesNN/page-<page>.png，再交给 upscale.py 转 jpg 并压缩

用法: python _tools\reexport_all.py [deck关键字...]
"""
import os, sys, json, glob, shutil, subprocess

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from decks import decks as discover

PS = os.path.join(HERE, "ppt_export.ps1")
TMP = os.path.join(HERE, "_ppt_out")


def run_deck(d):
    src = os.path.join(ROOT, d["source"])
    if not os.path.exists(src):
        print(f"  跳过（无课件）: {d['source']}")
        return False
    pm = json.load(open(os.path.join(d["extract_dir"], "pagemap.json"), encoding="utf-8"))["slide_to_page"]
    out_raw = os.path.join(TMP, d["images"])
    shutil.rmtree(out_raw, ignore_errors=True)
    os.makedirs(out_raw)
    r = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", PS,
                        "-Pptx", src, "-OutDir", out_raw],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(f"  ❌ 导出失败: {r.stderr[-400:]}")
        return False
    got = len(glob.glob(os.path.join(out_raw, "*.png")))
    # 按 pagemap 重命名到最终 assets 目录
    dest = os.path.join(ROOT, "assets", d["images"])
    tmp_dest = dest + "_new"
    shutil.rmtree(tmp_dest, ignore_errors=True)
    os.makedirs(tmp_dest)
    n = 0
    hidden = []
    for slide, page in pm.items():
        f = os.path.join(out_raw, f"page-{int(slide):04d}.png")
        if not os.path.exists(f):
            continue
        if page is None:
            hidden.append(int(slide))
            continue
        shutil.copy2(f, os.path.join(tmp_dest, f"page-{int(page):04d}.png"))
        n += 1
    shutil.rmtree(dest, ignore_errors=True)
    os.rename(tmp_dest, dest)
    print(f"  ✅ {d['images']}: 导出 {got} 张 → 入库 {n} 张（跳过隐藏页 {hidden or '无'}）")
    return True


def main():
    keys = sys.argv[1:]
    for d in discover():
        if keys and not any(k in d["images"] or k in d["source"] for k in keys):
            continue
        print(f"=== {d['source']} ===")
        run_deck(d)
    # 统一转 jpg + 压缩
    print("\n=== PNG→JPG 压缩 ===")
    subprocess.run([sys.executable, os.path.join(HERE, "upscale.py")],
                   cwd=ROOT)


if __name__ == "__main__":
    main()
