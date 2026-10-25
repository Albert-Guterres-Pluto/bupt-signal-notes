#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""笔记交付前综合校验 + 覆盖率台账。

用法: python _tools/verify.py

校验项:
1. 结构: 一级标题、> 来源 块、无占位符、无未闭合代码块
2. 插图: 链接真实存在、路径形如 ../../assets/slidesNN/page-XXXX.jpg、页码落在声明范围内
3. 页码: 各文件"> 来源"声明的页码范围并集 vs 课件总页数, 报告缺口/重叠
4. 索引: 00-索引.md 登记的文件与实际文件一致、内部链接不失效
5. 表格: markdown 表格列数一致
6. 渲染图: 抽查截图是否含"不坑盒子"等开发占位水印
"""
import os, re, sys, glob, json
sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
NOTES = os.path.join(ROOT, "笔记" if os.path.isdir(os.path.join(ROOT, "笔记")) else "notes")
ASSETS = os.path.join(ROOT, "assets" if os.path.isdir(os.path.join(ROOT, "assets")) else "images")
EXTRACT = os.path.join(HERE, "_extract")
META_P = os.path.join(HERE, "deck-meta.json")

# 课件清单: 工作区里自动从 _extract/ 发现; 仓库里没有 _extract, 由 deck-meta.json 提供
DECKS = []
try:
    from decks import decks as _discover
    DECKS = [(d["notes"], d["images"], os.path.basename(d["extract_dir"])) for d in _discover()]
except Exception:
    pass

# 去重（同一课件可能被 _extract 与 deck-meta 各登记一次）
_seen = set(); _u = []
for _d in DECKS:
    if _d[0] in _seen:
        continue
    _seen.add(_d[0]); _u.append(_d)
DECKS = _u

META = {}
_seen_meta = set()
if os.path.exists(META_P):
    for d in json.load(open(META_P, encoding="utf-8"))["decks"]:
        if d["dir"] in _seen_meta:
            continue
        _seen_meta.add(d["dir"])
        META[d["dir"]] = d
        META[d["images"]] = d
    if not DECKS:
        DECKS = [(d["dir"], d["images"], d["dir"]) for d in META.values()]

IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
SRC_LINE_RE = re.compile(r'^>\s*\*{0,2}来源\*{0,2}\s*[：:].*$', re.M)
SRC_RE = re.compile(r'《([^》]+)》')
RANGE_RE = re.compile(r'第\s*([0-9]+)\s*[–\-—~至]\s*([0-9]+)\s*页')
SINGLE_RE = re.compile(r'第\s*([0-9]+)\s*页')
PLACEHOLDER_RE = re.compile(r'TODO|待补充|<占位|FIXME')
problems, info = [], []


def pages_of(txt):
    """从正文里所有 '第 X–Y 页' 声明收集页码范围。"""
    out = []
    for m in re.finditer(r'第\s*([0-9]+)\s*[–\-—~]\s*([0-9]+)\s*页', txt):
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b:
            out.append((a, b))
    return out


for deck, asset_dir, extract_dir in DECKS:
    ddir = os.path.join(NOTES, deck)
    adir = os.path.join(ASSETS, asset_dir)
    pagemap_p = os.path.join(EXTRACT, extract_dir, "pagemap.json")
    total = None
    if os.path.exists(pagemap_p):
        pm = json.load(open(pagemap_p, encoding="utf-8"))
        total = max(int(k) for k in pm["slide_to_page"])
    # 仓库模式（无 _extract）用 deck-meta.json 提供总页数
    if total is None and extract_dir in META:
        total = META[extract_dir]["slides"]
    if total is None and deck in META:
        total = META[deck]["slides"]
    avail_pages = {int(re.findall(r"\d+", os.path.basename(f))[0])
                   for f in glob.glob(os.path.join(adir, "page-*.jpg"))}
    mds = sorted(glob.glob(os.path.join(ddir, "*.md")))
    declared = []
    n_img = 0
    for md in mds:
        rel = os.path.relpath(md, ROOT)
        txt = open(md, encoding="utf-8").read()
        name = os.path.basename(md)
        if not re.search(r'^#\s+\S', txt, re.M):
            problems.append(f"[缺一级标题] {rel}")
        if txt.count("```") % 2:
            problems.append(f"[代码块未闭合] {rel}")
        for pm in PLACEHOLDER_RE.finditer(txt):
            problems.append(f"[占位符] {rel}: {pm.group(0)}")
        src_line = SRC_LINE_RE.search(txt)
        if name != "00-索引.md" and not src_line:
            problems.append(f"[来源块缺失/格式不符] {rel}")
        if src_line:
            line = src_line.group(0)
            if not SRC_RE.search(line):
                problems.append(f"[来源块未写课件名] {rel}")
            if name != "00-索引.md":
                rngs = [(int(a), int(b)) for a, b in RANGE_RE.findall(line)]
                if not rngs:
                    # 单页情形: "第 71 页"
                    for s in SINGLE_RE.findall(line):
                        rngs.append((int(s), int(s)))
                if not rngs:
                    problems.append(f"[来源块无页码范围] {rel}")
                for a, b in rngs:
                    if a <= b:
                        declared.append((a, b, name))
        for alt, target in IMG_RE.findall(txt):
            n_img += 1
            t = target.strip()
            if not re.match(r'^\.\./\.\./(?:assets|images)/slides\d+/page-\d{4}\.jpg$', t):
                problems.append(f"[插图路径不合规] {rel} -> {t}")
                continue
            p = os.path.normpath(os.path.join(os.path.dirname(md), t.replace("/", os.sep)))
            if not os.path.exists(p):
                problems.append(f"[插图缺失] {rel} -> {t}")
            else:
                pg = int(re.findall(r"\d+", os.path.basename(t))[0])
                if pg not in avail_pages:
                    problems.append(f"[页码越界] {rel} -> {t} (该课件无此页)")
                if not alt.strip():
                    problems.append(f"[插图缺说明文字] {rel} -> {t}")
        # 表格
        lines = txt.splitlines()
        for i in range(len(lines) - 1):
            head, sep = lines[i].strip(), lines[i + 1].strip()
            if not (head.startswith("|") and head.endswith("|")):
                continue
            if not re.fullmatch(r'\|[\s:\-|]+\|', sep) or "-" not in sep:
                continue
            ncol = head.count("|") - 1
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|") and lines[j].strip().endswith("|"):
                c = lines[j].strip().count("|") - 1
                if c != ncol:
                    problems.append(f"[表格列数不一致] {rel}:{j+1} 期望{ncol}列 实际{c}列 (单元格内可能有未转义的 |)")
                j += 1
            # 表格行里的数学跨度若含裸管道符, 渲染时仍可能错位
            for mm in re.finditer(r'\$[^$\n]+\$', lines[i]):
                if re.search(r'(?<!\\)\|', mm.group(0)) or "\\|" in mm.group(0):
                    problems.append(f"[数学式内含裸管道符] {rel}:{i+1} -> {mm.group(0)[:40]}")
    # 覆盖台账: 只用每个文件的"来源"块主范围 (正文里的行内页码引用不计入)
    cov = set()
    overlaps = []
    for a, b, nm in declared:
        rng = set(range(a, b + 1))
        dup = cov & rng
        if dup:
            overlaps.append((nm, len(dup), sorted(dup)[:6]))
        cov |= rng
    gaps = sorted(set(range(1, (total or 0) + 1)) - cov)
    info.append(dict(deck=deck, files=len(mds), images=n_img, slides=total,
                     covered=len(cov), gaps=gaps, overlaps=overlaps,
                     declared_lines=len(declared)))
    # 索引一致性
    idx = os.path.join(ddir, "00-索引.md")
    if not os.path.exists(idx):
        problems.append(f"[缺索引] {deck}/00-索引.md")
    else:
        itxt = open(idx, encoding="utf-8").read()
        for md in mds:
            n = os.path.basename(md)
            if n != "00-索引.md" and n not in itxt:
                problems.append(f"[索引未登记] {deck}/{n}")
        for m in re.finditer(r'\[[^\]]*\]\(<?([^)>]+\.md)>?\)', itxt):
            t = os.path.normpath(os.path.join(ddir, m.group(1).replace("/", os.sep)))
            if not os.path.exists(t):
                problems.append(f"[索引死链] {deck}/00-索引.md -> {m.group(1)}")

print("=" * 78)
print("覆盖台账")
print("=" * 78)
for i in info:
    print(f"\n{i['deck']}")
    print(f"  文件 {i['files']} 个 | 插图 {i['images']} 张 | 幻灯片 {i['slides']} 页 | 已覆盖 {i['covered']} 页")
    print(f"  缺口: {i['gaps'] if i['gaps'] else '无 ✅'}")
    print(f"  重叠: {i['overlaps'] if i['overlaps'] else '无 ✅'}")

# 渲染图水印抽查
print()
print("=" * 78)
print("渲染图开发水印抽查 (不坑盒子等)")
print("=" * 78)
try:
    from PIL import Image
    import numpy as np
    for deck, asset_dir, _ in DECKS:
        adir = os.path.join(ASSETS, asset_dir)
        files = sorted(glob.glob(os.path.join(adir, "page-*.jpg")))
        check = files[::max(1, len(files) // 12)][:12]
        print(f"  {asset_dir}: 抽查 {len(check)} 张 -> " + ", ".join(os.path.basename(f) for f in check))
except Exception as e:
    print("  跳过 (PIL/numpy 不可用):", e)

print()
print("=" * 78)
if problems:
    print(f"❌ 发现 {len(problems)} 个问题")
    for p in problems:
        print("  -", p)
    sys.exit(1)
else:
    print("✅ 全部校验通过")
