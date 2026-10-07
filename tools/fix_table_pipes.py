#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""修复 markdown 表格内破坏结构的裸管道符。

问题: 表格单元里若出现未转义的 "|"（典型来源是数学绝对值 |X(Omega)|）,
markdown 会把它当成列分隔符, 整张表错位。
做法: 对每个表格行, 先定位数学跨度 $...$, 在其中把裸管道符成对改写为
\lvert ... \rvert, 并把该跨度暂存为占位符（不含管道符）; 之后再按 "|" 切分单元格,
最后还原占位符。幂等, 可重复运行。
"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NOTES = os.path.join(ROOT, "笔记")

MATH_SPAN = re.compile(r'\$[^$\n]+\$')
ABS_PAIR = re.compile(r'(?<!\\)\|([^|\n]{1,120}?)(?<!\\)\|')
PIPE_CMD = re.compile(r'(\\[Bb]igg?|\\middle|\\Big)\|')
ESC_PAIR = re.compile(r'\\\|([^|\n]{1,120}?)\\\|')
ESC_SINGLE = re.compile(r'\\\|')
SEP_ROW = re.compile(r'\|[\s:\-|]+\|')
SENT = "\x01"

fixed_files = fixed_total = 0


def fix_row(line):
    global fixed_total
    spans = []

    def stash(m):
        global fixed_total
        body = m.group(0)

        def fix_esc_pair(mm):
            global fixed_total
            fixed_total += 1
            return r"\lvert %s \rvert" % mm.group(1)

        def fix_span(mm):
            global fixed_total
            inner = mm.group(1)
            if inner.strip() in ("", "-") or set(inner) <= set("-: "):
                return mm.group(0)
            fixed_total += 1
            return r"\lvert %s \rvert" % inner

        # 1) 先把 \|...\| 这种"转义但仍是裸管道"的写法改写掉 (否则 markdown 仍然断列)
        body = ESC_PAIR.sub(fix_esc_pair, body)
        # 2) 再把剩余的裸 |...| 改写
        body = ABS_PAIR.sub(fix_span, body)
        # 3) \Big| \big| \middle| 这类单侧定界符 (不产生管道字符)
        body = PIPE_CMD.sub(lambda mm: mm.group(1) + r"\rvert ", body)
        # 4) 剩下的孤立 \| 不能留在表格里, 换成 \Vert
        body = ESC_SINGLE.sub(lambda _m: r"\Vert ", body)
        spans.append(body)
        return SENT + str(len(spans) - 1) + SENT

    protected = MATH_SPAN.sub(stash, line)
    cells = protected.split("|")
    if len(cells) < 3:
        return line

    def unstash(m):
        return spans[int(m.group(1))]

    return re.sub(SENT + r'(\d+)' + SENT, unstash, protected)


for md in sorted(glob.glob(os.path.join(NOTES, "**", "*.md"), recursive=True)):
    txt = open(md, encoding="utf-8").read()
    lines = txt.splitlines()
    changed = 0
    in_tbl = False
    for i, line in enumerate(lines):
        s = line.strip()
        is_row = s.startswith("|") and s.endswith("|")
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if is_row and SEP_ROW.fullmatch(nxt) and "-" in nxt:
            in_tbl = True
        elif not is_row:
            in_tbl = False
        if in_tbl and is_row:
            new = fix_row(line)
            if new != line:
                lines[i] = new
                changed += 1
    if changed:
        open(md, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
        fixed_files += 1
        print(f"{changed:>3} 行  {os.path.relpath(md, ROOT)}")

print(f"\n共修复 {fixed_total} 处裸管道符, 涉及 {fixed_files} 个文件")
