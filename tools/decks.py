# -*- coding: utf-8 -*-
r"""课件清单: 自动从 _extract/ 的 manifest 发现, 供各校验/构建脚本共用。

新增课件后不需要改任何脚本——只要跑过 extract.py + hidden.py 即可。
"""
import os, re, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXTRACT = os.path.join(HERE, "_extract")

# 课件 -> 图片子目录 / 笔记目录 的命名映射（按课件文件名关键字推断）
# 目录编号 = 课程讲授编号（2.2 节 → 02-2，2.3 节 → 02-3），与课件文件名严格对应。
_DECK_ALIASES = [
    (r"01_", "slides01", "01-信号分析与处理概述"),
    (r"2\.1节", "slides21", "02-1-连续时间信号分析"),
    (r"2\.2节", "slides22", "02-2-连续时间信号的频域分析"),
    (r"2\.3节", "slides23", "02-3-连续时间信号的复频域分析"),
    (r"第3章", "slides3", "03-连续时间系统的分析"),
    (r"第4章", "slides4", "04-滤波与滤波器"),
]


def decks():
    """返回 [{source, images, notes, slides, hidden, extract_dir}]，按课件顺序。

    工作区：从 _extract/ 的各 manifest 自动发现。
    仓库：没有 _extract，回退到 deck-meta.json（由 export_deck_meta.py 生成）。
    """
    out = []
    for d in sorted(glob.glob(os.path.join(EXTRACT, "*"))):
        mf = os.path.join(d, "manifest.json")
        if not os.path.exists(mf):
            continue
        man = json.load(open(mf, encoding="utf-8"))
        src = man["source"]
        images = notes = None
        for pat, img, note in _DECK_ALIASES:
            if re.search(pat, src):
                images, notes = img, note
                break
        if images is None:
            base = os.path.splitext(os.path.basename(d))[0]
            images = "slides_" + re.sub(r"[^0-9A-Za-z]", "", base)[:12]
            notes = base
        hidden = []
        pm = os.path.join(d, "pagemap.json")
        if os.path.exists(pm):
            p = json.load(open(pm, encoding="utf-8"))
            hidden = sorted(int(k) for k, v in p["slide_to_page"].items() if v is None)
        out.append(dict(name=os.path.basename(d), source=src, images=images, notes=notes,
                        slides=man["slides"], hidden=hidden, extract_dir=d))
    if out:
        return out
    # ---- 仓库模式：用 deck-meta.json ----
    meta_p = os.path.join(HERE, "deck-meta.json")
    if os.path.exists(meta_p):
        for d in json.load(open(meta_p, encoding="utf-8"))["decks"]:
            out.append(dict(name=d["dir"], source=d["source"], images=d["images"],
                            notes=d["dir"], slides=d["slides"],
                            hidden=d.get("hidden", []),
                            extract_dir=os.path.join(EXTRACT, d["dir"])))
    return out


if __name__ == "__main__":
    for x in decks():
        print(f"{x['notes']:38} {x['images']:12} {x['slides']:>4} 页  隐藏 {x['hidden'] or '无'}")
