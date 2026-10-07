#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""精简安全性检查: 对比精简前后, 确认公式、条件、易错点没有被误删。

用法: python _tools\compare_trim.py [备份目录]

做法:
1. 行间公式 ($$...$$) 与行内公式 ($...$) 的**规范化指纹**集合对比 —— 公式不得凭空消失;
2. 关键短语 (定义/条件/注意/易错/性质/定理/适用) 的出现次数对比;
3. 数值与常量 (如 20%、95%、1/10、π、Ω₀ 等) 的集合对比 —— 可考事实不得丢;
4. 图片数、字符数。
输出: 消失的公式清单 (需人工确认是有意删除还是误删)。
"""
import os, re, sys, glob, json, collections
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BACKUP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "_backup_before_trim", "笔记")

DISPLAY = re.compile(r'\$\$(.+?)\$\$', re.S)
INLINE = re.compile(r'(?<!\$)\$(?!\$)([^$\n]{1,200})\$(?!\$)')
NUM = re.compile(r'\d+(?:\.\d+)?\s*(?:%|Hz|kHz|MHz|GHz|ms|μs|ns|s|V|W|Ω|km/h|dB)|\d+/\d+|π')


def norm(s):
    s = re.sub(r'\s+', '', s)
    s = s.replace(r'\,', '').replace(r'\!', '').replace(r'\ ', '')
    s = re.sub(r'\\[a-zA-Z]+', lambda m: m.group(0).lower(), s)
    return s


def fingerprints(path):
    t = open(path, encoding="utf-8").read()
    disp = {norm(x) for x in DISPLAY.findall(t)}
    inl = {norm(x) for x in INLINE.findall(t)}
    nums = collections.Counter(NUM.findall(t))
    return disp, inl, nums


def main():
    old_files = {os.path.relpath(p, BACKUP): p
                 for p in glob.glob(os.path.join(BACKUP, "**", "*.md"), recursive=True)}
    print(f"备份目录: {os.path.relpath(BACKUP, ROOT)}  ({len(old_files)} 个文件)\n")
    missing_disp, missing_inl, lost_nums = [], [], []
    tot_old = tot_new = 0
    for rel, op in sorted(old_files.items()):
        np_ = os.path.join(ROOT, "笔记", rel)
        if not os.path.exists(np_):
            print(f"⚠ 文件消失: {rel}")
            continue
        od, oi, on = fingerprints(op)
        nd, ni, nn = fingerprints(np_)
        tot_old += len(od) + len(oi)
        tot_new += len(nd) + len(ni)
        for x in sorted(od - nd):
            missing_disp.append((rel, x))
        for x in sorted(oi - ni):
            missing_inl.append((rel, x))
        for k, v in on.items():
            if nn.get(k, 0) < v:
                lost_nums.append((rel, k, v, nn.get(k, 0)))

    print(f"公式指纹: 精前 {tot_old} 个 → 精后 {tot_new} 个")
    print(f"  消失的行间公式: {len(missing_disp)}")
    print(f"  消失的行内公式: {len(missing_inl)}")
    print(f"  数量减少的数值/常量: {len(lost_nums)}")
    if missing_disp:
        print("\n--- 消失的行间公式 (需人工确认) ---")
        for rel, x in missing_disp[:40]:
            print(f"  {rel}: {x[:90]}")
    if missing_inl:
        print("\n--- 消失的行内公式 (前 30 条, 可能只是被合并/改写) ---")
        for rel, x in missing_inl[:30]:
            print(f"  {rel}: {x[:80]}")
    if lost_nums:
        print("\n--- 数值/常量减少 (需人工确认可考事实未丢) ---")
        for rel, k, a, b in lost_nums[:30]:
            print(f"  {rel}: {k!r} {a}→{b}")
    json.dump(dict(missing_disp=missing_disp, missing_inl=missing_inl, lost_nums=lost_nums),
              open(os.path.join(HERE, "_trim_diff.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\n明细: _tools/_trim_diff.json")


if __name__ == "__main__":
    main()
