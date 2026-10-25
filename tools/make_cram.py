#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""把抱佛脚版各篇合并成一份总的速记卡，并校验"无例题/无图片/无练习"。

用法:
  python _tools\make_cram.py          # 合并 + 校验
输出: 信号分析与处理-抱佛脚速记.md（工作区根目录）
"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from _paths import CRAM_DIR, CRAM_OUT
SRC = CRAM_DIR
OUT = CRAM_OUT

ORDER = [
    ("01-概念公式速记.md", "第一篇　概念与分类（绪论）", "《信号分析与处理》01_20260915.pptx，96 页"),
    ("02-1-典型信号与基本运算速记.md", "第二篇　典型信号与基本运算（2.1）", "《信号分析与处理》2.1节-20260920.pptx，121 页"),
    ("02-2-频域分析速记.md", "第三篇　傅里叶分析（2.2）", "《信号分析与处理》2.2节-20261007.pptx，152 页"),
    ("02-3-复频域分析速记.md", "第四篇　复频域分析（2.3）", "《信号分析与处理》2.3节20261008.pptx，87 页"),
    ("03-04-系统与滤波器速记.md", "第五篇　连续系统分析与滤波器（第3、4章）",
     "《信号分析与处理》第3章-20261020.pptx（145 页）+ 第4章-20261020.pptx（101 页）"),
]

# 抱佛脚版禁止出现的东西
BAD_PATTERNS = [
    (re.compile(r'!\[[^\]]*\]\('), "图片引用"),
    (re.compile(r'^\s*#{2,4}\s*例\s*\d', re.M), "例题小节"),
    (re.compile(r'^\s*\*\*解\*\*', re.M), "解答段落"),
    (re.compile(r'^\s*#{2,4}\s*(自测|练习|习题)', re.M), "自测/练习题"),
    (re.compile(r'(我们来看|下面来看|举一个例子|例如：)', re.M), "举例引导语"),
]


def strip_title(text):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.startswith("# "):
            return l[2:].strip(), "\n".join(lines[i + 1:]).strip("\n")
    return "(无标题)", text


def main():
    if not os.path.isdir(SRC):
        print("❌ 还没有 笔记/00-抱佛脚版/ 目录")
        sys.exit(2)
    problems = []
    body = []
    toc = []
    total_chars = 0

    body.append("# 《信号分析与处理》抱佛脚速记")
    body.append("")
    body.append("考前突击用：**只有概念、公式、性质和条件**，没有例题、没有练习、没有图片。")
    body.append("按「考前 1 小时」的用法组织——三篇按顺序扫一遍，重点看标了 ⚠️ 的条件和易错点。")
    body.append("")
    body.append("> **完整版**（含例题、推导、课件截图）：[信号分析与处理-完整笔记.md](信号分析与处理-完整笔记.md)")
    body.append("> **分篇笔记**：见 [README.md](README.md)")
    body.append("")

    sections = []
    for fname, title, src in ORDER:
        p = os.path.join(SRC, fname)
        if not os.path.exists(p):
            problems.append(f"缺少文件: {fname}")
            continue
        text = open(p, encoding="utf-8").read()
        # 校验
        for pat, what in BAD_PATTERNS:
            for m in pat.finditer(text):
                line = text[:m.start()].count("\n") + 1
                problems.append(f"{fname}:{line} 出现{what}: {m.group(0)[:40]!r}")
        _, rest = strip_title(text)
        rest = rest.replace("](../../assets/", "](assets/")
        sections.append((title, src, rest, fname))
        total_chars += len(re.sub(r'\s', '', rest))

    body.append(f"## 目录")
    body.append("")
    idx = 0
    for title, src, _, _fn in sections:
        idx += 1
        body.append(f"{idx}. [{title}](#cram-{idx:02d})　<span style=\"color:gray\">（{src}）</span>")
    body.append("")
    body.append("---")
    body.append("")

    idx = 0
    for title, src, rest, _fn in sections:
        idx += 1
        body.append(f'<a id="cram-{idx:02d}"></a>')
        body.append("")
        body.append(f"# {title}")
        body.append("")
        body.append(f"> 对应课件：{src}")
        body.append("")
        body.append(rest)
        body.append("")
        body.append("---")
        body.append("")

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(body).rstrip() + "\n")

    txt = open(OUT, encoding="utf-8").read()
    print(f"已生成: {os.path.relpath(OUT, ROOT)}")
    print(f"  篇数 {len(sections)} | 正文 {total_chars} 字 | 总字符 {len(txt)} | 行数 {txt.count(chr(10)) + 1}")
    # 各篇规模与表格行数
    print()
    print(f"  {'篇':44} {'字数':>6} {'表行':>5} {'公式':>5}")
    for title, src, rest, fname in sections:
        chars = len(re.sub(r'\s', '', rest))
        tbl = len(re.findall(r'^\|', rest, re.M))
        fml = len(re.findall(r'\$[^$\n]+\$', rest))
        print(f"  {title[:42]:44} {chars:>6} {tbl:>5} {fml:>5}")
    print()
    if problems:
        print(f"❌ 发现 {len(problems)} 个问题:")
        for p in problems[:40]:
            print("  -", p)
        sys.exit(1)
    print("✅ 校验通过：无图片、无例题、无练习、无自测")


if __name__ == "__main__":
    main()
