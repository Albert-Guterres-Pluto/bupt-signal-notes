#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""把工作区整理成一个可共享的 git 仓库骨架。

产出: ..\信号分析与处理-笔记\   （工作区同级目录, 不污染已校验的原始工作区）
- notes/      单章笔记 + 索引（相对路径不变: ../../images/slidesNN/...）
- images/     只复制被笔记实际引用的图（约 18 MB, 而不是全部 47 MB）
- tools/      校验脚本（零依赖，同学 clone 后可直接跑）
- docs/       撰写规范
- .github/workflows/check.yml   push/PR 自动校验
- .gitignore / README.md / CONTRIBUTING.md / LICENSE
"""
import os, re, sys, glob, shutil, filecmp
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEST = os.path.abspath(os.path.join(ROOT, "..", "信号分析与处理-笔记"))

IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')


def copy_tree(src, dst, exts=None):
    n = 0
    for p in glob.glob(os.path.join(src, "**", "*"), recursive=True):
        if os.path.isfile(p):
            if exts and os.path.splitext(p)[1].lower() not in exts:
                continue
            rel = os.path.relpath(p, src)
            d = os.path.join(dst, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(p, d)
            n += 1
    return n


def main():
    if os.path.exists(DEST):
        print(f"目标已存在, 先删除: {DEST}")
        shutil.rmtree(DEST)
    os.makedirs(DEST)

    # ---------- 1. notes/ ----------
    n_notes = copy_tree(os.path.join(ROOT, "笔记"), os.path.join(DEST, "notes"), exts={".md"})
    # 抱佛脚版是子目录, 保持结构 notes/00-抱佛脚版/
    print(f"notes/  : {n_notes} 个 md")

    # ---------- 2. images/ 只保留被引用的图 ----------
    used = set()
    for md in glob.glob(os.path.join(DEST, "notes", "**", "*.md"), recursive=True):
        for m in IMG_RE.finditer(open(md, encoding="utf-8").read()):
            link = m.group(1).replace("\\", "/")
            parts = link.split("/")
            for i, seg in enumerate(parts):
                if seg == "assets":
                    used.add("/".join(parts[i + 1:]))
                    break
    n_img = 0
    for rel in sorted(used):
        src = os.path.join(ROOT, "assets", rel.replace("/", os.sep))
        if not os.path.exists(src):
            print(f"  ⚠ 笔记引用了不存在的图: {rel}")
            continue
        dst = os.path.join(DEST, "images", rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        n_img += 1
    print(f"images/ : {n_img} 张被引用的图")

    # ---------- 3. tools/ ----------
    KEEP = ["verify.py", "fix_img_paths.py", "fix_table_pipes.py", "verify_captions.py",
            "verify_combined.py", "scan_text.py", "make_combined.py", "make_cram.py",
            "extract.py", "omml.py", "formulas.py", "hidden.py", "upscale.py",
            "optimize_assets.py", "measure.py", "compare_trim.py", "audit_lost_formulas.py",
            "orphans.py", "audit_images.py"]
    os.makedirs(os.path.join(DEST, "tools"), exist_ok=True)
    n_tools = 0
    for f in KEEP:
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(DEST, "tools", f))
            n_tools += 1
    # 规范文档
    os.makedirs(os.path.join(DEST, "tools", "docs"), exist_ok=True)
    for f in ["笔记撰写规范.md", "精简规范.md"]:
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(DEST, "tools", "docs", f))
    print(f"tools/  : {n_tools} 个脚本")

    print(f"\n骨架已建: {DEST}")
    return DEST


if __name__ == "__main__":
    main()
