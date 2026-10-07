#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""把 笔记/ 下所有单章 md 合成一份整体笔记: 信号分析与处理-完整笔记.md。

规则:
- 每个课件作为一篇, 每章升一级标题 (# -> ##), 便于整体形成层级。
- 每章前插入 HTML 锚点 (<a id="ch-XX"></a>), 使目录链接在 VSCode / GitHub 都可跳转。
- 章内原有的 "> 来源：" 元信息块保留 (紧跟在标题后), 其余正文照抄。
- 插图路径由 ../../assets/... 改写为 assets/... (合成文件位于工作区根目录)。
- 源笔记里的相对 md 链接 (如 00-索引.md) 统一指向对应的单章文件。
"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NOTES = os.path.join(ROOT, "笔记" if os.path.isdir(os.path.join(ROOT, "笔记")) else "notes")
NOTES_NAME = os.path.basename(NOTES)   # 工作区里是"笔记", 仓库里是"notes"
OUT = os.path.join(ROOT, "signal-notes.md" if not os.path.isdir(os.path.join(ROOT, "笔记")) else "信号分析与处理-完整笔记.md")

DECKS = [
    ("01-信号分析与处理概述", "第一篇　第一章 绪论", "《信号分析与处理》01_20260915.pptx，96 页"),
    ("02-1-连续时间信号分析", "第二篇　2.1 连续时间信号的时域分析", "《信号分析与处理》2.1节-20260920.pptx，121 页"),
    ("02-2-连续时间信号的频域分析", "第三篇　2.2 连续时间信号的频域分析", "《信号分析与处理》2.2节-20260920.pptx，144 页"),
]
FENCE = re.compile(r'^\s*(```|~~~)')
H_RE = re.compile(r'^(#{1,6})(\s+)(.*)$')


def demote(text):
    """章节内标题整体降一级; 跳过代码块内部。"""
    out, in_fence, fence_mark = [], False, None
    for line in text.splitlines():
        m = FENCE.match(line)
        if m:
            mark = m.group(1)
            if not in_fence:
                in_fence, fence_mark = True, mark
            elif mark == fence_mark:
                in_fence, fence_mark = False, None
            out.append(line)
            continue
        if not in_fence:
            h = H_RE.match(line)
            if h:
                line = "#" + line
        out.append(line)
    return "\n".join(out)


def split_title(text):
    """拆出首个 H1 标题与其余正文。"""
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.startswith("# "):
            return l[2:].strip(), "\n".join(lines[i + 1:]).strip("\n")
    return "(无标题)", text


def main():
    toc, body = [], []

    # 先收集各篇的章文件清单, 才能算出总章数
    entries = []      # (deck, 篇名, 来源, [文件])
    for deck, deck_title, src in DECKS:
        ddir = os.path.join(NOTES, deck)
        files = sorted(f for f in glob.glob(os.path.join(ddir, "*.md"))
                       if os.path.basename(f) != "00-索引.md")
        entries.append((deck, deck_title, src, files))
    total_ch = sum(len(e[3]) for e in entries)

    body.append("# 《信号分析与处理》完整笔记")
    body.append("")
    body.append("北京邮电大学《信号分析与处理》课程课件（3 份、361 张幻灯片）整理而成的合并笔记。")
    body.append("")
    body.append(f"> **阅读建议**：本文件是全部笔记的合并版（3 篇 {total_ch} 章，浓缩版）。")
    body.append("> 用编辑器的大纲（VSCode：`Ctrl+Shift+O`）或下面的目录跳转；")
    body.append("> 只想看某一节时，打开 `笔记/` 下对应的单章文件更轻快。")
    body.append(">")
    body.append("> **来源标注**：每章开头 `> 来源：` 给出对应课件与页码范围；")
    body.append("> 插图均为课件原页渲染图，点击可放大；课件里被设为隐藏、未导出的页面已在正文中注明。")
    body.append(">")
    body.append("> **公式说明**：2.1 节的公式可由课件原始 XML 提取（OMML），01 与 2.2 节的公式是 MathType 对象、")
    body.append("> 无法提取文字，因此这些页的公式以**课件截图为准**，正文 LaTeX 仅供检索与排版参考。")
    body.append("")
    body.append("---")
    body.append("")

    # ---- 目录 ----
    toc.append(f"## 目录（共 3 篇 {total_ch} 章）")
    toc.append("")
    idx = 0
    for deck, deck_title, src, files in entries:
        toc.append(f"**{deck_title}**　<span style=\"color:gray\">（{src}）</span>")
        toc.append("")
        for f in files:
            idx += 1
            title, _ = split_title(open(f, encoding="utf-8").read())
            anchor = f"ch-{idx:02d}"
            toc.append(f"{idx}. [{title}](#{anchor})")
        toc.append("")
    body.extend(toc)
    body.append("---")
    body.append("")

    # ---- 正文 ----
    idx = 0
    for deck, deck_title, src, files in entries:
        body.append(f"<a id=\"deck-{deck}\"></a>")
        body.append("")
        body.append(f"# {deck_title}")
        body.append("")
        body.append(f"> 对应课件：{src}")
        body.append("")
        for f in files:
            idx += 1
            text = open(f, encoding="utf-8").read()
            title, rest = split_title(text)
            # 图片路径: 合成文件在根目录, 用 assets/ 或 images/
            rest = rest.replace("](../../assets/", "](assets/").replace("](../../images/", "](images/")
            # 源笔记里的同级 md 链接 -> 指向真实文件
            rest = re.sub(r'\]\(\s*<?\.?/?([0-9A-Za-z\-]+\.md)>?\s*\)',
                          lambda m: f']({NOTES_NAME}/{deck}/{m.group(1)})', rest)
            body.append("---")
            body.append("")
            body.append(f"<a id=\"ch-{idx:02d}\"></a>")
            body.append("")
            rel_single = f"{NOTES_NAME}/{deck}/{os.path.basename(f)}"
            body.append(f"## {idx}. {title}")
            body.append("")
            body.append(f"> 单章文件：[{os.path.basename(f)}]({rel_single})")
            body.append("")
            body.append(demote(rest).strip())
            body.append("")
        body.append("")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(body).rstrip() + "\n")

    size = os.path.getsize(OUT)
    txt = open(OUT, encoding="utf-8").read()
    n_img = txt.count("](assets/") + txt.count("](images/")
    print(f"已生成: {os.path.relpath(OUT, ROOT)}")
    print(f"  篇章 {total_ch} 章 | 插图引用 {n_img} 张 | 字符 {len(txt)} | 体积 {size/1048576:.1f} MB")


if __name__ == "__main__":
    main()
