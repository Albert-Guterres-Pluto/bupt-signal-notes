#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提取 pptx 中的 OMML 公式 (真正的数学标记, 可转 LaTeX)。

用法: python _tools/formulas.py
输出: _tools/_extract/<deck>/formulas.md   每页公式的 LaTeX
      _tools/_extract/<deck>/formulas.json
说明: MathType (Equation.DSMT4) 公式对象不含 OMML, 只能靠截图; 脚本会统计并提示。
"""
import os, re, sys, json, zipfile, glob, posixpath
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lxml import etree
from omml import formulas

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def safe_parse(raw):
    try:
        return etree.fromstring(raw)
    except etree.XMLSyntaxError:
        txt = raw.decode("utf-8", "replace")
        txt = re.sub(r'\s([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*"([^"]*)"',
                     lambda m: '' if len(m.group(2)) > 100000 else m.group(0), txt)
        return etree.fromstring(txt.encode("utf-8"))


def slide_sort_key(n):
    return int(re.findall(r"\d+", posixpath.basename(n))[0])


def run(pptx, outdir):
    z = zipfile.ZipFile(pptx)
    names = set(z.namelist())
    slides = sorted((n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=slide_sort_key)
    out = {}
    n_mt = 0
    for i, sn in enumerate(slides, 1):
        raw = z.read(sn)
        root = safe_parse(raw)
        fs = formulas(root)
        txt = raw.decode("utf-8", "replace")
        mt = len(re.findall(r'progId="Equation\.(?:DSMT4|3)"', txt))
        n_mt += mt
        if fs or mt:
            out[i] = dict(formulas=fs, mathtype=mt)
    with open(os.path.join(outdir, "formulas.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    n_f = sum(len(v["formulas"]) for v in out.values())
    lines = [f"# 公式提取: {os.path.basename(pptx)}", "",
             f"可转 LaTeX 的 OMML 公式: {n_f} 个, 分布 {sum(1 for v in out.values() if v['formulas'])} 页",
             f"MathType 公式对象: {n_mt} 个 (不含 OMML, 只能看截图)", ""]
    for i in sorted(out):
        v = out[i]
        lines.append(f"## SLIDE {i}" + (f"  [MathType ×{v['mathtype']}]" if v["mathtype"] else ""))
        for f in v["formulas"]:
            lines.append(f"- `{f}`")
        lines.append("")
    with open(os.path.join(outdir, "formulas.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return n_f, n_mt, len(slides)


if __name__ == "__main__":
    for d in sorted(glob.glob(os.path.join(HERE, "_extract", "*"))):
        mf = os.path.join(d, "manifest.json")
        if not os.path.exists(mf):
            continue
        man = json.load(open(mf, encoding="utf-8"))
        pptx = os.path.join(ROOT, man["source"])
        if not os.path.exists(pptx):
            print("skip (课件不存在):", man["source"])
            continue
        n_f, n_mt, n_s = run(pptx, d)
        print(f"{man['source']}: OMML公式 {n_f} 个 | MathType对象 {n_mt} 个 | 共 {n_s} 页")
