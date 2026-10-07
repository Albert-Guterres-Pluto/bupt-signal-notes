#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""统计各章正文字数与插图数, 用于精简前后对比。

用法:
  python _tools/measure.py save     # 把当前状态存为基线 (_tools/_baseline.json)
  python _tools/measure.py diff     # 与基线对比, 输出每章变化
"""
import os, re, sys, json, glob
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NOTES = os.path.join(ROOT, "笔记")
BASE = os.path.join(HERE, "_baseline.json")
IMG = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')


def scan():
    out = {}
    for md in sorted(glob.glob(os.path.join(NOTES, "**", "*.md"), recursive=True)):
        rel = os.path.relpath(md, ROOT)
        t = open(md, encoding="utf-8").read()
        # 正文字数: 去掉图片行与空白
        body = "\n".join(l for l in t.splitlines() if not l.strip().startswith("!["))
        chars = len(re.sub(r'\s', '', body))
        out[rel] = dict(chars=chars, imgs=len(IMG.findall(t)))
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "diff"
    cur = scan()
    if mode == "save":
        json.dump(cur, open(BASE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"已保存基线: {len(cur)} 个文件, 正文合计 {sum(v['chars'] for v in cur.values())} 字, "
              f"插图 {sum(v['imgs'] for v in cur.values())} 张")
        return
    base = json.load(open(BASE, encoding="utf-8"))
    print(f"{'文件':52} {'字数':>14} {'插图':>11}")
    print(f"{'':52} {'前→后':>14} {'前→后':>11}")
    print("-" * 82)
    tc0 = tc1 = ti0 = ti1 = 0
    for rel in sorted(set(base) | set(cur)):
        b = base.get(rel, dict(chars=0, imgs=0))
        c = cur.get(rel, dict(chars=0, imgs=0))
        tc0 += b["chars"]; tc1 += c["chars"]; ti0 += b["imgs"]; ti1 += c["imgs"]
        dc = c["chars"] - b["chars"]
        di = c["imgs"] - b["imgs"]
        flag = ""
        if b["chars"] and dc > 0:
            flag = "  ⚠字数反增"
        name = rel.replace("笔记\\", "")[:50]
        print(f"{name:52} {b['chars']:>6}→{c['chars']:<6} {b['imgs']:>4}→{c['imgs']:<4}{flag}")
    print("-" * 82)
    print(f"{'合计':52} {tc0:>6}→{tc1:<6} {ti0:>4}→{ti1:<4}")
    print(f"\n正文字数: -{tc0-tc1} ({100*(tc0-tc1)/max(tc0,1):.0f}%)   插图: -{ti0-ti1} ({100*(ti0-ti1)/max(ti0,1):.0f}%)")
    worst = [(rel, base[rel]["chars"] - cur.get(rel, {}).get("chars", 0)) for rel in base if base[rel]["chars"]]
    worst.sort(key=lambda x: x[1])
    print("\n精简幅度最小的 5 个文件 (需重点复查):")
    for rel, d in worst[:5]:
        print(f"  {rel}: -{d} 字")


if __name__ == "__main__":
    main()
