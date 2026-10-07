#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OMML (Office Math Markup Language) -> LaTeX 转换器。

用于从 pptx 中提取课件里的公式对象 (python-pptx 与朴素文本提取都拿不到)。
覆盖课件常见结构: 分数、上下标、根式、求和/积分、括号、矩阵、 accents、函数名。
"""
from lxml import etree

M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"

GREEK = {
    "α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta", "ε": r"\varepsilon",
    "ζ": r"\zeta", "η": r"\eta", "θ": r"\theta", "ι": r"\iota", "κ": r"\kappa",
    "λ": r"\lambda", "μ": r"\mu", "ν": r"\nu", "ξ": r"\xi", "π": r"\pi", "ρ": r"\rho",
    "σ": r"\sigma", "τ": r"\tau", "υ": r"\upsilon", "φ": r"\varphi", "χ": r"\chi",
    "ψ": r"\psi", "ω": r"\omega", "Γ": r"\Gamma", "Δ": r"\Delta", "Θ": r"\Theta",
    "Λ": r"\Lambda", "Ξ": r"\Xi", "Π": r"\Pi", "Σ": r"\Sigma", "Φ": r"\Phi",
    "Ψ": r"\Psi", "Ω": r"\Omega",
}
OPS = {"∞": r"\infty", "∑": r"\sum", "∫": r"\int", "∏": r"\prod", "≤": r"\le", "≥": r"\ge",
       "≠": r"\ne", "→": r"\to", "±": r"\pm", "×": r"\times", "·": r"\cdot", "∂": r"\partial",
       "∈": r"\in", "∀": r"\forall", "∃": r"\exists", "≈": r"\approx", "⇒": r"\Rightarrow"}
FUNCS = {"sin", "cos", "tan", "cot", "sec", "csc", "log", "ln", "exp", "lim", "max", "min",
         "Sa", "sinc", "sgn", "d", "e", "j"}


def _txt(el):
    return "".join(t.text or "" for t in el.iter(M + "t"))


GREEK_UP = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
GREEK_LO = "αβγδεζηθικλμνξοπρστυφχψω"

MATH_GREEK = {}
for _i, _c in enumerate(GREEK_UP):
    for _base in (0x1D6A8, 0x1D6E2, 0x1D71C, 0x1D756, 0x1D790):   # 粗/斜/粗斜/无衬线粗/无衬线粗斜
        MATH_GREEK[_base + _i] = _c
for _i, _c in enumerate(GREEK_LO):
    for _base in (0x1D6C2, 0x1D6FC, 0x1D736, 0x1D770, 0x1D7AA):
        MATH_GREEK[_base + _i] = _c
MATH_GREEK.update({
    0x1D6DB: "∂", 0x1D6DC: "ε", 0x1D6DD: "ϑ", 0x1D6DE: "ϰ", 0x1D6DF: "ϕ",
    0x1D6E0: "ϱ", 0x1D6E1: "ϖ", 0x1D7CA: "Ϝ", 0x1D7CB: "ϝ",
    0x2212: "-", 0x00a0: " ", 0x2206: r"\Delta ", 0x2044: "/",
})


def _plain(ch):
    """数学字母数字符号 (U+1D400–U+1D7FF) 还原为普通字符。"""
    o = ord(ch)
    if o in MATH_GREEK:
        return MATH_GREEK[o]
    if 0x1D6A8 <= o <= 0x1D7CB:
        return "?"      # 未覆盖的数学希腊字母, 显式标记以免静默丢失
    if 0x1D400 <= o <= 0x1D419:
        return chr(o - 0x1D400 + ord("A"))
    if 0x1D41A <= o <= 0x1D433:
        return chr(o - 0x1D41A + ord("a"))
    if 0x1D434 <= o <= 0x1D44D:
        return chr(o - 0x1D434 + ord("A"))
    if 0x1D44E <= o <= 0x1D467:
        return chr(o - 0x1D44E + ord("a"))
    if 0x1D468 <= o <= 0x1D481:
        return chr(o - 0x1D468 + ord("A"))
    if 0x1D482 <= o <= 0x1D49B:
        return chr(o - 0x1D482 + ord("a"))
    if 0x1D7CE <= o <= 0x1D7D7:
        return chr(o - 0x1D7CE + ord("0"))
    if 0x1D7E2 <= o <= 0x1D7EB:
        return chr(o - 0x1D7E2 + ord("0"))
    return ch


def _esc(s):
    out = []
    for ch in s:
        ch = _plain(ch)
        if ch in GREEK:
            out.append(GREEK[ch] + " ")
        elif ch in OPS:
            out.append(OPS[ch] + " ")
        else:
            out.append(ch)
    return "".join(out)


def _children(el):
    return [c for c in el if isinstance(c.tag, str)]


def conv(el):
    """把一个元素转成 LaTeX 片段。"""
    if not isinstance(el.tag, str):
        return ""
    loc = etree.QName(el).localname
    kids = _children(el)

    if loc in ("oMath", "oMathPara", "e", "num", "den", "sub", "sup", "fName", "lim", "deg", "rad", "oMathParaPr", "oMathPara"):
        return "".join(conv(k) for k in kids)
    if loc == "r":
        # 数学 run: 可能是 m:t, 也可能是普通文本 run (a:t)
        s = _txt(el)
        if not s:
            s = "".join(t.text or "" for t in el.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"))
        return _esc(s)
    if loc == "f":
        num = el.find(M + "num")
        den = el.find(M + "den")
        return r"\frac{%s}{%s}" % (conv(num) if num is not None else "",
                                   conv(den) if den is not None else "")
    if loc == "sSup":
        return "{%s}^{%s}" % (conv(el.find(M + "e")), conv(el.find(M + "sup")))
    if loc == "sSub":
        return "{%s}_{%s}" % (conv(el.find(M + "e")), conv(el.find(M + "sub")))
    if loc == "sSubSup":
        return "{%s}_{%s}^{%s}" % (conv(el.find(M + "e")), conv(el.find(M + "sub")),
                                   conv(el.find(M + "sup")))
    if loc == "rad":
        deg = el.find(M + "deg")
        d = conv(deg)
        e = conv(el.find(M + "e"))
        return (r"\sqrt[%s]{%s}" % (d, e)) if d.strip() else (r"\sqrt{%s}" % e)
    if loc == "nary":
        chr_el = el.find(M + "naryPr/" + M + "chr")
        op = chr_el.get(M + "val") if chr_el is not None and chr_el.get(M + "val") else "∫"
        latex_op = OPS.get(op, op)
        sub = el.find(M + "sub")
        sup = el.find(M + "sup")
        e = conv(el.find(M + "e"))
        s = (r"_{%s}" % conv(sub)) if sub is not None else ""
        p = (r"^{%s}" % conv(sup)) if sup is not None else ""
        return "%s%s%s %s" % (latex_op, s, p, e)
    if loc == "d":
        pr = el.find(M + "dPr")
        beg = end = None
        if pr is not None:
            b = pr.find(M + "begChr")
            e2 = pr.find(M + "endChr")
            if b is not None:
                beg = b.get(M + "val")
            if e2 is not None:
                end = e2.get(M + "val")
        # 单边定界符: 缺失的一侧补成配对符号, 避免 \left\{ ... \right) 这类不匹配
        if beg is None and end is None:
            beg, end = "(", ")"
        elif beg is None:
            beg = {"}": "{", ")": "(", "]": "[", "⟩": "⟨", "|": "|"}.get(end, ".")
        elif end is None:
            end = {"{": "}", "(": ")", "[": "]", "⟨": "⟩", "|": "|"}.get(beg, ".")
        inner = "".join(conv(k) for k in kids if etree.QName(k).localname == "e")
        LB = {"(": "(", "[": "[", "{": r"\{", "⟨": r"\langle", "|": "|", "‖": r"\|", "": "."}
        RB = {")": ")", "]": "]", "}": r"\}", "⟩": r"\rangle", "|": "|", "‖": r"\|", "": "."}
        lb = LB.get(beg, beg)
        rb = RB.get(end, end)
        return r"\left%s %s \right%s" % (lb, inner, rb)
    if loc == "m":
        rows = []
        for mr in el.findall(M + "mr"):
            rows.append(" & ".join(conv(e) for e in mr.findall(M + "e")))
        return r"\begin{matrix}%s\end{matrix}" % (r" \\ ".join(rows))
    if loc == "func":
        return r"%s\left(%s\right)" % (conv(el.find(M + "fName")), conv(el.find(M + "e")))
    if loc in ("acc", "bar", "groupChr", "box", "borderBox"):
        e = conv(el.find(M + "e"))
        pr = el.find(M + "accPr")
        ch = "hat"
        if pr is not None:
            c = pr.find(M + "chr")
            if c is not None:
                v = c.get(M + "val") or ""
                ch = {"̄": "bar", "‾": "bar", "̂": "hat", "→": "vec", "~": "tilde", "̇": "dot", "̈": "ddot"}.get(v, "hat")
        if ch == "bar":
            return r"\overline{%s}" % e
        if ch == "vec":
            return r"\vec{%s}" % e
        if ch == "tilde":
            return r"\tilde{%s}" % e
        if ch == "dot":
            return r"\dot{%s}" % e
        if ch == "ddot":
            return r"\ddot{%s}" % e
        return r"\hat{%s}" % e
    if loc == "limLow":
        return r"%s_{%s}" % (conv(el.find(M + "e")), conv(el.find(M + "lim")))
    if loc == "limUpp":
        return r"%s^{%s}" % (conv(el.find(M + "e")), conv(el.find(M + "lim")))
    if loc in ("eqArr",):
        return r" \\ ".join(conv(e) for e in el.findall(M + "e"))
    if loc == "t":
        return _esc(el.text or "")
    # 其它容器: 递归
    return "".join(conv(k) for k in kids)


def formulas(root):
    """提取文档中所有 oMath 的 LaTeX 列表。"""
    out = []
    for m in root.iter(M + "oMath"):
        s = conv(m).strip()
        s = " ".join(s.split())
        if s:
            out.append(s)
    return out
