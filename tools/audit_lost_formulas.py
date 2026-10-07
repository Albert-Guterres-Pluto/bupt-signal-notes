#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""逐条复核"精简后消失的公式"是否真的丢了内容。

思路: 对每条消失的公式, 抽取其**数学内容 token** (字母、数字、希腊字母、运算符),
在新文件中查找是否有一个公式/文本片段包含全部 token。
- 全部 token 都能在新文件里找到 → 属于"排版合并/变量名规范化", 不算丢失;
- 有 token 缺失 → 标记为可疑, 需人工确认。
用法: python _tools\audit_lost_formulas.py
"""
import os, re, sys, json, glob
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIFF = os.path.join(HERE, "_trim_diff.json")

TOKEN = re.compile(r'\\[A-Za-z]+|[A-Za-z]+|\d+')

# 已知 LaTeX 命令名 (按长度降序匹配, 解决 \to y 被写成 \toy 这类粘连)
COMMANDS = sorted([
    "longrightarrow", "leftrightarrow", "displaystyle", "varnothing", "triangleq",
    "mathscr", "mathrm", "mathbf", "mathbb", "mathcal", "limits", "dfrac", "tfrac",
    "frac", "sqrt", "left", "right", "cdot", "cdots", "ldots", "quad", "qquad",
    "begin", "end", "cases", "text", "sum", "prod", "int", "oint", "infty",
    "delta", "Delta", "omega", "Omega", "alpha", "beta", "gamma", "Gamma", "theta",
    "Theta", "lambda", "Lambda", "sigma", "Sigma", "tau", "phi", "Phi", "varphi",
    "psi", "Psi", "mu", "nu", "xi", "Xi", "eta", "rho", "zeta", "pi", "Pi",
    "varepsilon", "epsilon", "sgn", "sinc", "Sa", "sinc", "sin", "cos", "tan",
    "cot", "sec", "csc", "log", "ln", "exp", "lim", "max", "min", "le", "ge", "ne",
    "pm", "mp", "times", "div", "to", "rightarrow", "Rightarrow", "Leftrightarrow",
    "quad", "lvert", "rvert", "Vert", "vert", "langle", "rangle", "ast", "star",
    "partial", "nabla", "forall", "exists", "in", "notin", "subset", "cup", "cap",
    "align", "aligned", "matrix", "pmatrix", "bmatrix", "overline", "underline",
    "hat", "bar", "vec", "dot", "ddot", "mathcal", "stackrel", "underbrace",
    "overbrace", "Big", "big", "Bigg", "bigg", "middle", "nonumber", "tag",
], key=len, reverse=True)


def normalize(s):
    """把 LaTeX 规范化为 token 流, 命令名按已知表做最长匹配。"""
    parts = []
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch == "\\":
            rest = s[i + 1:]
            hit = None
            for c in COMMANDS:
                if rest.startswith(c):
                    hit = c
                    break
            if hit:
                parts.append("\\" + hit.lower())
                i += 1 + len(hit)
            else:
                m = re.match(r'\\([A-Za-z]+)', s[i:])
                if m:
                    parts.append(m.group(0).lower())
                    i += m.end()
                else:
                    i += 1              # 转义符号 (\, \; \\ 等), 忽略
            continue
        m = re.match(r'[A-Za-z]+|\d+', s[i:])
        if m:
            parts.append(m.group(0).lower())
            i += m.end()
        else:
            i += 1
    return " ".join(parts)


# 纯排版命令与过于通用的单字母, 不参与"是否丢失"的判定
IGNORE = {"\\left", "\\right", "\\frac", "\\dfrac", "\\tfrac", "\\sqrt", "\\displaystyle",
          "\\limits", "\\text", "\\mathrm", "\\mathscr", "\\quad", "\\qquad", "\\cdot",
          "\\cdots", "\\ldots", "\\begin", "\\end", "\\cases", "\\sum", "\\int",
          "\\infty", "\\longrightarrow", "\\leftrightarrow", "\\to", "\\langle",
          "\\rangle", "\\lvert", "\\rvert", "\\le", "\\ge", "\\ne", "\\pm", "\\times"}


def tokens(s):
    out = set()
    for tok in normalize(s).split():
        if tok in IGNORE:
            continue
        if len(tok) <= 1 and not tok.isdigit():
            continue      # 单字母变量太通用, 不作为判定依据
        out.add(tok)
    return out


def main():
    d = json.load(open(DIFF, encoding="utf-8"))
    cache = {}
    for f in glob.glob(os.path.join(ROOT, "笔记", "**", "*.md"), recursive=True):
        rel = os.path.relpath(f, os.path.join(ROOT, "笔记"))
        cache[rel] = normalize(open(f, encoding="utf-8").read())

    ok, suspect = 0, []
    for rel, formula in d["missing_disp"] + d["missing_inl"]:
        txt = cache.get(rel)
        if txt is None:
            suspect.append((rel, formula, "文件缺失"))
            continue
        toks = tokens(formula)
        missing = [t for t in toks if t not in txt]
        if missing:
            suspect.append((rel, formula, "缺 token: " + ", ".join(sorted(missing)[:6])))
        else:
            ok += 1

    print(f"消失公式共 {len(d['missing_disp']) + len(d['missing_inl'])} 条")
    print(f"  内容仍在 (排版合并/变量名规范化): {ok} 条 ✅")
    print(f"  可疑 (有 token 找不到):           {len(suspect)} 条")
    if suspect:
        print("\n--- 可疑清单 (需人工确认) ---")
        for rel, f, why in suspect:
            print(f"  {rel}\n     {f[:100]}\n     → {why}")
    else:
        print("\n✅ 没有真正的公式丢失")
    sys.exit(1 if suspect else 0)


if __name__ == "__main__":
    main()
