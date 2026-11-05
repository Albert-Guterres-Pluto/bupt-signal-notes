# -*- coding: utf-8 -*-
"""把六张「题型与解法」表从 4 列（#/题型/解法入口/关键提醒）压成 3 列（题型/解法入口/关键提醒），
编号内联到题型列，换取每列更宽、正文更大、换行更少。
"""
import glob, re, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

changed = 0
for f in sorted(glob.glob(os.path.join(ROOT, "笔记", "00-抱佛脚版", "*.md"))):
    lines = open(f, encoding="utf-8").read().split("\n")
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        # 命中表头：| # | 题型（识别特征） | 解法入口 | 关键提醒 |
        if re.match(r'^\|\s*#\s*\|\s*题型', ln):
            # 跳过表头行本身，改写为三列
            out.append("| 题型（识别特征） | 解法入口 | 关键提醒 |")
            i += 1
            # 分隔行
            if i < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i]):
                out.append("|---|---|---|")
                i += 1
            # 数据行：| 1 | ... | ... | ... |
            while i < len(lines) and lines[i].startswith("|") and lines[i].count("|") >= 4:
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if len(cells) != 4:
                    out.append(lines[i])
                    i += 1
                    continue
                num, a, b, c = cells
                # 编号内联：**①** 题型（用圆+数字更省宽度）
                circled = "①②③④⑤⑥⑦⑧⑨"
                try:
                    mark = circled[int(num) - 1]
                except (ValueError, IndexError):
                    mark = num
                out.append(f"| **{mark}** {a} | {b} | {c} |")
                i += 1
            changed += 1
            continue
        out.append(ln)
        i += 1
    open(f, "w", encoding="utf-8", newline="\n").write("\n".join(out))

print(f"已把 {changed} 张题型表改为 3 列")
