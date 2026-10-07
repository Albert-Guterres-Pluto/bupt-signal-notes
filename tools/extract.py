#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从 pptx 提取结构化文本 (绕过 python-pptx 在畸形 XML 属性上的崩溃)。

输出: _extract/<deck>/slides.md   每页文本 + 表格 + 备注, 按阅读位置排序
      _extract/<deck>/media/      页面引用的媒体文件 (png/jpg/emf/wmf/svg...)
      _extract/<deck>/manifest.json
"""
import os, re, sys, json, zipfile, hashlib, shutil, posixpath
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
OUT_ROOT = os.path.join(HERE, "_extract")

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rels": "http://schemas.openxmlformats.org/package/2006/relationships",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
}
A = "{%s}" % NS["a"]
P = "{%s}" % NS["p"]
R = "{%s}" % NS["r"]
RELS = "{%s}" % NS["rels"]


def safe_parse(data):
    """解析 xml; 对超大/畸形属性做删除后重试。返回 (root, heavy_attrs_removed)"""
    try:
        return etree.fromstring(data), False
    except etree.XMLSyntaxError:
        txt = data.decode("utf-8", "replace")
        # 删除长度 > 100000 的属性值 (通常是误塞入的 HTML/ink 数据)
        def repl(m):
            return '' if len(m.group(2)) > 100000 else m.group(0)
        txt2 = re.sub(r'\s([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*"([^"]*)"', repl, txt)
        return etree.fromstring(txt2.encode("utf-8")), True


def xml_text(el):
    """按文档顺序拼接所有 a:t (跳过 a:descr 等属性)。"""
    parts = [t.text or "" for t in el.iter(A + "t")]
    return "".join(parts)


def para_lines(el):
    """返回该 txBody 的段落列表 (保留换行结构)。"""
    out = []
    for para in el.iter(A + "p"):
        s = "".join(t.text or "" for t in para.iter(A + "t"))
        out.append(s)
    # 去掉首尾空段
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def table_md(tbl):
    rows = []
    for tr in tbl.findall(A + "tr"):
        cells = []
        for tc in tr.findall(A + "tc"):
            cells.append(" ".join(para_lines(tc)).replace("|", "\\|").strip())
        rows.append(cells)
    if not rows:
        return ""
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * ncol]
    for r in rows[1:]:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def shape_tree_entries(spTree, srel):
    """遍历 spTree (含组合), 产出 dict 列表。"""
    out = []

    def walk(node, gx=0, gy=0, depth=0):
        for child in node:
            tag = etree.QName(child).localname
            if tag == "grpSp":
                xfrm = child.find(".//" + A + "xfrm")
                off = xfrm.find(A + "off") if xfrm is not None else None
                ox = int(off.get("x", 0)) if off is not None else 0
                oy = int(off.get("y", 0)) if off is not None else 0
                walk(child, gx + ox, gy + oy, depth + 1)
                continue
            if tag not in ("sp", "pic", "graphicFrame", "cxnSp", "contentPart"):
                continue
            xfrm = child.find(".//" + A + "xfrm")
            off = xfrm.find(A + "off") if xfrm is not None else None
            ext = xfrm.find(A + "ext") if xfrm is not None else None
            try:
                x = int(off.get("x", 0)) + gx if off is not None else 0
                y = int(off.get("y", 0)) + gy if off is not None else 0
                cx = int(ext.get("cx", 0)) if ext is not None else 0
                cy = int(ext.get("cy", 0)) if ext is not None else 0
            except Exception:
                x = y = cx = cy = 0

            nv = child.find(".//" + P + "cNvPr")
            if nv is None:
                nv = child.find(".//" + P + "nvPr")
            name = nv.get("name", "") if nv is not None else ""
            descr = nv.get("descr", "") if nv is not None else ""
            if len(descr) > 300:
                descr = descr[:120] + " ...[已截断]" + descr[-60:]

            kind = tag
            media = None
            blip = child.find(".//" + A + "blip")
            if blip is not None:
                rid = blip.get(R + "embed") or blip.get(R + "link")
                if rid:
                    media = srel.get(rid)
                    kind = "pic"
            olevb = child.find(".//" + P + "oleObj")
            if olevb is not None:
                kind = "ole"
            tbl = child.find(".//" + A + "tbl")
            if tbl is not None:
                kind = "table"

            tx = child.find(".//" + P + "txBody")
            if tx is None:
                tx = child.find(".//" + A + "txBody")
            lines = para_lines(tx) if tx is not None else []
            txt = "\n".join(lines).strip()

            # 检测公式 (OMML)
            omml = child.findall(".//{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath")
            is_math = bool(omml)
            if is_math and not txt:
                txt = " ".join("".join(t.text or "" for t in m.iter(A + "t")) for m in omml).strip()

            if not txt and kind not in ("pic", "ole") and tbl is None and not is_math:
                continue
            if kind in ("table",):
                out.append(dict(kind="table", x=x, y=y, cx=cx, cy=cy, depth=depth,
                                name=name, md=table_md(tbl) if tbl is not None else ""))
                continue
            out.append(dict(kind=("math" if is_math and txt else kind), x=x, y=y, cx=cx, cy=cy,
                            depth=depth, name=name, descr=descr, text=txt, media=media))

    walk(spTree)
    return out


def extract(pptx_path, outdir):
    os.makedirs(outdir, exist_ok=True)
    mediadir = os.path.join(outdir, "media")
    os.makedirs(mediadir, exist_ok=True)

    z = zipfile.ZipFile(pptx_path)
    names = set(z.namelist())

    # 全局 rels: part -> {rid: target}
    def rels_for(part):
        d, base = posixpath.split(part)
        rp = posixpath.join(d, "_rels", base + ".rels")
        if rp not in names:
            return {}
        root = etree.fromstring(z.read(rp))
        m = {}
        for rel in root.findall(RELS + "Relationship"):
            t = rel.get("Target")
            if rel.get("TargetMode") != "External":
                t = posixpath.normpath(posixpath.join(d, t))
            m[rel.get("Id")] = t
        return m

    slide_names = sorted(
        (n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)),
        key=lambda n: int(re.findall(r"\d+", posixpath.basename(n))[0]),
    )

    # 媒体去重落地
    hash_map = {}
    media_index = {}

    def dump_media(part):
        if part in media_index:
            return media_index[part]
        data = z.read(part)
        h = hashlib.sha1(data).hexdigest()[:12]
        ext = os.path.splitext(part)[1].lower()
        fname = h + ext
        if h not in hash_map:
            hash_map[h] = fname
            with open(os.path.join(mediadir, fname), "wb") as f:
                f.write(data)
        media_index[part] = hash_map[h]
        return hash_map[h]

    slides = []
    warnings = []
    for idx, sn in enumerate(slide_names, 1):
        data = z.read(sn)
        root, heavy = safe_parse(data)
        if heavy:
            warnings.append(f"slide {idx}: 畸形超长属性已剥离 (不影响文字提取)")
        srel = rels_for(sn)
        spTree = root.find(".//" + P + "cSld/" + P + "spTree")
        if spTree is None:
            spTree = root.find(".//" + P + "spTree")
        entries = shape_tree_entries(spTree, srel) if spTree is not None else []
        # 落地媒体
        for e in entries:
            if e.get("media") and e["media"] in names:
                e["file"] = dump_media(e["media"])
            elif e.get("media"):
                e["file"] = None
        entries.sort(key=lambda e: (e["y"] // 100000, e["x"]))

        # 备注
        notes = ""
        nrel = rels_for(sn)
        for rel in root.findall(".//" + P + "hlinkClick"):
            pass
        # 找 notesSlide 关系: 从 slide rels 查
        note_part = None
        for rid, tgt in srel.items():
            if tgt and "notesSlide" in tgt:
                note_part = tgt
        if note_part and note_part in names:
            nroot, _ = safe_parse(z.read(note_part))
            keep = []
            for sp in nroot.iter(P + "sp"):
                ph = sp.find(".//" + P + "ph")
                typ = ph.get("type") if ph is not None else None
                tx = sp.find(".//" + P + "txBody")
                if tx is None:
                    continue
                lines = para_lines(tx)
                txt = " ".join(lines).strip()
                if not txt:
                    continue
                if typ in ("sldNum", "slideNumber"):
                    continue
                keep.append((typ, txt))
            notes = "\n".join(t for _, t in keep if t)

        slides.append(dict(index=idx, part=sn, entries=entries, notes=notes))

    # 写 markdown
    lines = []
    lines.append(f"# 提取文本: {os.path.basename(pptx_path)}")
    lines.append(f"\n幻灯片总数: {len(slides)}\n")
    for s in slides:
        lines.append("\n" + "=" * 90)
        lines.append(f"## SLIDE {s['index']}  ({s['part']})")
        lines.append("=" * 90)
        for e in s["entries"]:
            k = e["kind"]
            if k == "table":
                lines.append(f"\n[TABLE] {e.get('name','')}")
                lines.append(e["md"])
            elif k == "pic":
                lines.append(f"\n[IMAGE] file={e.get('file')} size={e['cx']//9525}x{e['cy']//9525}pt name={e.get('name','')}")
                if e.get("descr"):
                    lines.append(f"        alt: {e['descr']}")
            elif k == "ole":
                lines.append(f"\n[OLE/嵌入对象] {e.get('name','')} {e.get('text','')[:200]}")
            elif k == "math":
                lines.append(f"\n[公式] {e['text']}")
            else:
                lines.append(f"\n[TEXT] {e['text']}")
        if s["notes"]:
            lines.append(f"\n[备注/NOTES] {s['notes']}")

    with open(os.path.join(outdir, "slides.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # 每页单独文件, 方便并行阅读
    per = os.path.join(outdir, "slides")
    os.makedirs(per, exist_ok=True)
    for s in slides:
        pl = [f"# SLIDE {s['index']}"]
        for e in s["entries"]:
            k = e["kind"]
            if k == "table":
                pl.append("[TABLE]\n" + e["md"])
            elif k == "pic":
                pl.append(f"[IMAGE] file={e.get('file')} size={e['cx']//9525}x{e['cy']//9525}pt")
                if e.get("descr"):
                    pl.append(f"        alt: {e['descr']}")
            elif k == "ole":
                pl.append(f"[OLE] {e.get('name','')} {e.get('text','')[:200]}")
            elif k == "math":
                pl.append(f"[公式] {e['text']}")
            else:
                pl.append(e["text"])
        if s["notes"]:
            pl.append("[备注] " + s["notes"])
        with open(os.path.join(per, f"slide_{s['index']:03d}.md"), "w", encoding="utf-8") as f:
            f.write("\n\n".join(pl) + "\n")

    manifest = dict(source=os.path.basename(pptx_path), slides=len(slides),
                    media_files=len(set(hash_map.values())),
                    warnings=warnings,
                    per_slide_stats=[dict(index=s["index"], blocks=len(s["entries"]),
                                          has_notes=bool(s["notes"]),
                                          chars=sum(len(e.get("text", "")) for e in s["entries"]))
                                     for s in slides])
    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    return manifest


if __name__ == "__main__":
    decks = sys.argv[1:] or [f for f in sorted(os.listdir(WORK)) if f.lower().endswith(".pptx")]
    for fn in decks:
        if not fn.lower().endswith(".pptx"):
            continue
        base = os.path.splitext(fn)[0]
        safe = re.sub(r'[\\/:*?"<>|《》]', "_", base)
        outdir = os.path.join(OUT_ROOT, safe)
        m = extract(os.path.join(WORK, fn), outdir)
        print(f"{fn}: slides={m['slides']} media={m['media_files']} dir={safe}")
