#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""把抱佛脚速记（5 篇 markdown）编译成 PDF（xelatex）。

流程： 拼接 md → pandoc 转 latex 正文 → 后处理（章节/表格/环境适配）→
      套模板 → xelatex 编两次（稳定页码/目录）→ 清理中间文件

用法: python _tools\build_cram_pdf.py
输出: 信号分析与处理-抱佛脚速记.pdf（工作区根目录）
"""
import os, re, sys, glob, shutil, subprocess

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_PDF = os.path.join(ROOT, "信号分析与处理-抱佛脚速记.pdf")
BUILD = os.path.join(HERE, "pdfbuild")
TEXLIVE = r"C:\texlive\2026\bin\windows"

CRAM_ORDER = [
    "01-概念公式速记.md",
    "02-1-典型信号与基本运算速记.md",
    "02-2-频域分析速记.md",
    "02-3-复频域分析速记.md",
    "03-04-系统与滤波器速记.md",
]

# PDF 里每篇的统一标题（源 md 的 H1 写法不统一，有的带"抱佛脚版·"有的不带）
PART_TITLES = {
    "01-概念公式速记.md": ("第一篇", "概念与分类（绪论）"),
    "02-1-典型信号与基本运算速记.md": ("第二篇", "典型信号与基本运算（2.1）"),
    "02-2-频域分析速记.md": ("第三篇", "傅里叶分析（2.2）"),
    "02-3-复频域分析速记.md": ("第四篇", "复频域分析（2.3）"),
    "03-04-系统与滤波器速记.md": ("第五篇", "连续系统与滤波器（第 3、4 章）"),
}

PREAMBLE = r"""\documentclass[UTF8,a4paper,zihao=5]{ctexart}
\usepackage[top=1.9cm,bottom=1.9cm,left=1.6cm,right=1.6cm,headsep=0.4cm,footskip=0.9cm]{geometry}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{mathrsfs}
\usepackage{booktabs,longtable,array,tabularx,multirow,makecell}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage[colorlinks,linkcolor=blue!50!black,urlcolor=blue!50!black,
            pdftitle={信号分析与处理 抱佛脚速记},
            pdfauthor={BUPT 信号分析与处理课程笔记},
            pdfsubject={考前速记：概念·公式·性质·成立条件},
            pdfkeywords={信号分析与处理, 傅里叶变换, 拉普拉斯变换, 滤波器, 北邮}]{hyperref}

\setmainfont{Times New Roman}
\setsansfont{Arial}
\setmonofont{Consolas}[Scale=0.90]
\setCJKmainfont{Microsoft YaHei}[BoldFont=Microsoft YaHei Bold]
\setCJKsansfont{Microsoft YaHei}
\setCJKmonofont{SimSun}

\definecolor{accent}{HTML}{1F5FA9}
\definecolor{rulegray}{HTML}{B8C4D0}

% 顶层（每篇）用 section*，不加编号；小节标题自带"一、二、"与"2.1"等序号，
% 因此不再叠加自动编号（否则会渲染成 "1 一、核心名词" 这种重复）
\ctexset{
  section/format       = \LARGE\bfseries\color{accent}\raggedright,
  section/beforeskip   = 0.6ex plus .2ex,
  section/afterskip    = 0.9ex,
  subsection/number    = {},
  subsection/format    = \normalsize\bfseries\color{accent!88!black}\raggedright,
  subsection/beforeskip= 0.9ex plus .2ex,
  subsection/afterskip = 0.4ex,
  subsubsection/number = {},
  subsubsection/format = \normalsize\bfseries\color{black!78}\raggedright,
  subsubsection/beforeskip = 0.6ex,
  subsubsection/afterskip  = 0.3ex,
}

\renewcommand{\arraystretch}{1.18}
\setlength{\tabcolsep}{3.5pt}
\AtBeginEnvironment{longtable}{\footnotesize}
\AtBeginEnvironment{tabularx}{\footnotesize}
\setlist[itemize]{leftmargin=1.3em,itemsep=0.8pt,topsep=2pt,parsep=0pt}
\setlist[enumerate]{leftmargin=1.5em,itemsep=0.8pt,topsep=2pt,parsep=0pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.30ex}
\setlength{\emergencystretch}{2em}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\fancyhead[L]{\footnotesize\color{black!55}《信号分析与处理》抱佛脚速记}
\fancyhead[R]{\footnotesize\color{black!55}\leftmark}
\fancyfoot[C]{\footnotesize\color{black!60}\thepage}

% 提示块（源自 markdown 引用）
\newenvironment{tipblock}%
  {\par\vspace{0.15em}\begingroup\leftskip=0.6em\rightskip=0.6em
   \color{black!62}\small\setlength{\parskip}{0.15em}}%
  {\par\endgroup\vspace{0.15em}}

\newcommand{\pgbreak}{\clearpage}

% 篇与篇之间的分隔条（不强制分页，避免出现大片空白页）
\newcommand{\partsep}{%
  \par\vspace{1.5em}%
  \noindent{\color{accent}\rule{\linewidth}{1.5pt}}%
  \par\vspace{0.22em}%
}

% ⚠ 与 ✓ 等符号：中文字体缺字形，统一用 LaTeX 记号
% ⚠ 用红色三角代替（原文 19 处都是"注意/易错"提示）
\newcommand{\warnsym}{\textcolor{red!75!black}{\small$\blacktriangleright$}\,}
"""

TITLE = r"""\begin{document}
\thispagestyle{empty}
\begin{center}
\vspace*{1.2cm}
{\Huge\bfseries\color{accent} 《信号分析与处理》}\\[0.5em]
{\LARGE\bfseries 抱佛脚速记}\\[1.2em]
{\large 北京邮电大学 \quad 80 学时 / 5 学分}\\[0.4em]
{\normalsize 覆盖六份课件，共 702 张幻灯片}\\[2.0em]
\end{center}

\begin{center}
\begin{minipage}{0.90\linewidth}
\small\color{black!72}
\textbf{用法}\quad 这是一份考前突击用的浓缩笔记：只有概念、公式、性质与成立条件，
\textbf{不含例题、练习与插图}。建议只看表格与标 \warnsym{} 的条件；
遇到看不懂的地方，回完整笔记查上下文。\\[0.6em]
\textbf{来源}\quad 每篇开头标注对应课件与页数；完整版与分篇笔记见
\href{https://github.com/Albert-Guterres-Pluto/bupt-signal-notes}{GitHub: bupt-signal-notes}。\\[0.6em]
\textbf{符号}\quad 角频率 $\Omega$、复频率 $s=\sigma+\mathrm{j}\Omega$、抽样函数
$\mathrm{Sa}(x)=\frac{\sin x}{x}$；傅里叶变换对记作 $x(t)\leftrightarrow X(\Omega)$。
\end{minipage}
\end{center}

\vspace{1.4em}
\hrule height 0.6pt
\vspace{1.0em}

\begin{center}
\begin{minipage}{0.86\linewidth}
\small
\textbf{五篇内容}\\[0.4em]
\begin{tabular}{@{}p{0.06\linewidth}p{0.36\linewidth}p{0.52\linewidth}@{}}
\toprule
一 & 概念与分类（绪论） & 信号/消息/信息、信号四组分类、系统五组分类、必背公式 \\
二 & 典型信号与基本运算（2.1） & 典型信号表、奇异信号与 $\delta(t)$ 三性质、几何变换、卷积 \\
三 & 傅里叶分析（2.2） & 级数三形式、变换对表、性质总表（12 条）、周期信号变换 \\
四 & 复频域分析（2.3） & 拉氏变换与 ROC、性质总表、变换对、逆变换、与傅氏关系 \\
五 & 系统与滤波器（第3、4章） & 系统四大特性、零极点判据、梅森公式、巴特沃斯、频率变换 \\
\bottomrule
\end{tabular}
\end{minipage}
\end{center}

\vspace{1.6em}
\setcounter{tocdepth}{1}%   目录只列 5 篇，不列小节
{\renewcommand{\contentsname}{\normalsize\bfseries 目\quad 录}%
\tableofcontents}

\clearpage
"""

POSTAMBLE = "\n\\end{document}\n"


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def concat_md():
    parts = []
    for fn in CRAM_ORDER:
        p = os.path.join(ROOT, "笔记", "00-抱佛脚版", fn)
        if not os.path.exists(p):
            print(f"  ⚠ 缺少 {fn}")
            continue
        txt = open(p, encoding="utf-8").read().strip()
        # 统一 H1：第一篇由文件序号统一生成；其余 H1（如 03-04 里的"第3章""第4章"）
        # 一律降为 H2，保证目录里恰好 5 条、层级干净
        lines = txt.splitlines()
        seen_h1 = False
        for k, ln in enumerate(lines):
            if ln.startswith("# ") and not ln.startswith("## "):
                if not seen_h1:
                    num, name = PART_TITLES.get(fn, ("", ""))
                    lines[k] = f"# {num}　{name}" if num else ln
                    seen_h1 = True
                else:
                    lines[k] = "## " + ln[2:].strip()
        parts.append("\n".join(lines))
    md = "\n\n".join(parts) + "\n"
    out = os.path.join(BUILD, "cram_all.md")
    open(out, "w", encoding="utf-8", newline="\n").write(md)
    return out


def fix_widths(tex):
    """把 pandoc 的 longtable 列宽改成等分 \\linewidth 的 tabularx，避免超宽溢出。"""
    def repl(m):
        body, ncol = m.group(1), int(m.group(2))
        spec = "".join(r">{\raggedright\arraybackslash}X" for _ in range(ncol))
        tbl = body.replace(r"\begin{longtable}[]{@{}" + "@{}" * 0 + "", "", 0)
        return body
    return tex


def table_fix(tex):
    """把 longtable 环境整体替换为 tabularx（等分列宽 + 自动换行）。"""
    out = []
    i = 0
    n_fixed = 0
    while True:
        j = tex.find(r"\begin{longtable}", i)
        if j < 0:
            out.append(tex[i:])
            break
        k = tex.find(r"\end{longtable}", j)
        if k < 0:
            out.append(tex[i:])
            break
        k_end = k + len(r"\end{longtable}")
        block = tex[j:k_end]
        # 先把 longtable 的骨架命令整体抹掉，只留真正的单元格内容行。
        # pandoc 的表结构形如:
        #   \begin{longtable}[]{@{}lll@{}}
        #   \toprule\noalign{}
        #   表头1 & 表头2 \\
        #   \midrule\noalign{}
        #   数据... \\
        #   \bottomrule\noalign{}
        #   \end{longtable}
        s = block
        # \begin{longtable}[]{@{}...@{}} 到 \toprule 之间全是列格式定义，一次性截掉
        s = re.sub(r'\\begin\{longtable\}.*?\\toprule', r'\\toprule', s, count=1, flags=re.S)
        if s.lstrip().startswith(r"\begin{longtable}"):
            # 没有 \toprule 的退化情况
            s = re.sub(r'\\begin\{longtable\}.*?\n', '', s, count=1, flags=re.S)
        s = s.replace(r"\end{longtable}", "")
        s = re.sub(r'\\noalign\{\}', '', s)
        s = re.sub(r'\\toprule|\\midrule|\\bottomrule', '', s)
        s = re.sub(r'\\endhead|\\endfirsthead|\\endlastfoot', '', s)
        # 剥掉 pandoc 为单元格加的 minipage 包裹
        s = s.replace(r"\begin{minipage}[b]{\linewidth}\raggedright", "")
        s = s.replace(r"\end{minipage}", "")
        s = s.replace(r"\begin{minipage}[t]{\linewidth}\raggedright", "")
        # 按 LaTeX 表格真正的行分隔符 \\ 切分（不能按换行切，pandoc 把一行表头
        # 拆成多行写）。但 \begin{cases}...\end{cases} 等数学环境内部的 \\ 是
        # 环境自己的换行符，必须先保护起来，否则会把一条公式切成几行。
        MATH_ENVS = ("cases", "matrix", "pmatrix", "bmatrix", "vmatrix", "Vmatrix",
                     "aligned", "align", "gathered", "split", "array", "subarray")
        _store = []
        pat_env = r'\\begin\{(' + "|".join(MATH_ENVS) + r')\}.*?\\end\{\1\}'

        def _hide(m):
            _store.append(m.group(0))
            return "\x01P%dX\x01" % (len(_store) - 1)

        s = re.sub(pat_env, _hide, s, flags=re.S)
        flat = re.sub(r'\s+', ' ', s).strip()
        rows_hidden = []          # 占位符状态（cases 等已被替换）
        for piece in re.split(r'\\\\', flat):
            t0 = piece.strip()
            if not t0:
                continue
            # 丢掉只含列格式定义的行
            if '&' not in t0 and re.fullmatch(r'[>@{}lcrXhpw*.\- ]+', t0):
                continue
            rows_hidden.append(t0)

        # 还原被保护的数学环境，并去掉占位符两侧可能多出的空格
        def _unhide(t0):
            def _r(m):
                return _store[int(m.group(1))]
            return re.sub(r'\s*\x01P(\d+)X\x01\s*', _r, t0)

        rows = [_unhide(r) for r in rows_hidden]

        # 列数必须基于"占位符状态"统计：cases/matrix 里的 & 是数学对齐符，
        # 不是表格列分隔符（否则会把 4 列表误判成 8 列，宽度全算错）
        ncol = 1
        for r in rows_hidden:
            c = len(re.findall(r'(?<!\\)&', r)) + 1
            ncol = max(ncol, c)
        cleaned = [r for r in rows if r.strip()]
        if not cleaned:
            out.append(tex[i:j])
            out.append(block)
            i = k_end
            continue

        # ---- 按内容估算每列相对宽度 ----
        # 文本：中文按 2、其余按 1；行内公式不能断行，按字符数 ×1.4 估渲染宽度，
        # 否则公式列会被压得过窄而溢出（tabularx 的 X 列只在空格处断行）。
        def vis_len(cell):
            maths = re.findall(r'\\\((.*?)\\\)', cell, re.S) + re.findall(r'\$(.+?)\$', cell, re.S)
            text = re.sub(r'\\\(.*?\\\)', ' ', cell, flags=re.S)
            text = re.sub(r'\$.+?\$', ' ', text, flags=re.S)
            text = re.sub(r'\\[A-Za-z]+\*?', '', text)     # 去 LaTeX 命令名
            text = re.sub(r'[{}\\^_~]', '', text)
            n = 0
            for ch in text:
                n += 2 if ord(ch) > 0x2E80 else 1
            for mth in maths:
                mm = re.sub(r'\\[A-Za-z]+\*?', '', mth)     # 去命令名，保留内容
                mm = re.sub(r'[{}\\^_~]', '', mm)
                n += max(1, len(mm)) * 1.4
            return n

        col_w = [0] * ncol
        for r in rows_hidden:          # 用占位符状态统计，避免 cases 的 & 干扰
            cells = re.split(r'(?<!\\)&', r)
            for ci, c in enumerate(cells[:ncol]):
                if c.strip().startswith(r"\#") or c.strip() in ("#",):
                    continue
                # 占位符按其原始数学环境的宽度折算（cases 公式很宽）
                def _expand(m):
                    orig = _store[int(m.group(1))]
                    orig = re.sub(r'\\[A-Za-z]+\*?', '', orig)
                    orig = re.sub(r'[{}\\^_~&]', '', orig)
                    return "x" * max(1, int(len(orig) * 1.2))
                c2 = re.sub(r'\x01P(\d+)X\x01', _expand, c)
                col_w[ci] = max(col_w[ci], vis_len(c2))
        total_w = sum(col_w) or ncol
        # 映射到 \hsize 相对值：每列 hsize 系数之和为 ncol（tabularx 约定）
        MINR, MAXR = 0.62, 2.8
        ratios = []
        for w in col_w:
            r0 = ncol * (w / total_w) if total_w else 1.0
            ratios.append(max(MINR, min(MAXR, r0)))
        s = sum(ratios)
        ratios = [r * ncol / s for r in ratios]
        spec = "".join(
            r">{\raggedright\arraybackslash\hsize=%.3f\hsize}X" % rt for rt in ratios
        )

        # 第一行当表头，后面补 \midrule
        # 注意：按 \\ 切分时行尾的 \\ 被吃掉了，这里每行重新补回
        head = cleaned[0].rstrip()
        if head.endswith(r"\\"):
            head = head[:-2].rstrip()
        head = head + r" \\"
        rest = [r.rstrip() + r" \\" for r in cleaned[1:] if r.strip()]
        body_rows = head + "\n" + r"\midrule" + "\n" + "\n".join(rest)
        # 内容特别重的表（含长公式）自动降一档字号 + 收紧列间距，避免右侧溢出
        max_cell = 0
        for r in cleaned:
            for c in re.split(r'(?<!\\)&', r):
                max_cell = max(max_cell, vis_len(c))
        if max_cell > 150:
            fsize, tsep = r"\scriptsize", "2.2pt"
        elif max_cell > 100:
            fsize, tsep = r"\footnotesize", "2.8pt"
        else:
            fsize, tsep = r"\small", "3.2pt"
        new = ("\\begin{center}\n"
               "\\begingroup%s\\setlength{\\tabcolsep}{%s}\n"
               "\\begin{tabularx}{\\linewidth}{@{}%s@{}}\n"
               "\\toprule\n%s\\bottomrule\n"
               "\\end{tabularx}\n\\endgroup\n\\end{center}\n"
               % (fsize, tsep, spec, body_rows + "\n"))
        out.append(tex[i:j])
        out.append(new)
        n_fixed += 1
        i = k_end
    return "".join(out), n_fixed


def postprocess(body):
    # 标题层级：H1(篇) -> section*；H2 -> subsection；H3 -> subsubsection
    # 篇之间用"醒目分隔条 + 适当留白"而不是强制分页：抱佛脚速记要紧凑，
    # 强制分页会留下 4~5 页只有两三行的空白页。用 \partsep 在版心内分隔。
    body = re.sub(r'\\section\{(.+?)\}\\label\{[^}]*\}\n?',
                  lambda m: ("\\partsep\\section*{%s}\\addcontentsline{toc}{section}{%s}"
                             "\\markboth{%s}{}\n" % (m.group(1), m.group(1), m.group(1))), body)
    body = re.sub(r'\\subsection\{(.+?)\}\\label\{[^}]*\}',
                  lambda m: "\\subsection{%s}" % m.group(1), body)
    body = re.sub(r'\\subsubsection\{(.+?)\}\\label\{[^}]*\}',
                  lambda m: "\\subsubsection{%s}" % m.group(1), body)
    body = body.replace(r"\tightlist", "")
    # 首次出现的 pgbreak 去掉（紧跟标题页，已有 clearpage）
    body = body.lstrip()
    if body.startswith(r"\partsep"):
        body = body[len(r"\partsep"):].lstrip()
    # 引用块 -> tipblock
    body = body.replace(r"\begin{quote}", r"\begin{tipblock}")
    body = body.replace(r"\end{quote}", r"\end{tipblock}")
    # 去掉 pandoc 的 \hypertarget 冗长标签（保留可读性）
    body = re.sub(r'\\hypertarget\{[^}]*\}\{%\n?', '', body)
    body = re.sub(r'\\label\{[^}]*\}', '', body)
    body = fix_symbols(body)
    body, n = table_fix(body)
    print(f"  表格转换：{n} 个 longtable -> tabularx")
    return body


# ---- 特殊符号：字体缺字形的 Unicode 符号统一换成 LaTeX 记号 ----
# 注意：这里写的是"真实字符"，不是转义序列（转义序列在 r-string 里不会生效）
SYM_MAP = [
    ("\ufe0f", ""),                        # 变体选择符（⚠️ 的第二个码点）
    ("\u26a0", r"\warnsym{}"),             # ⚠
    ("\u21d2", r"\(\Rightarrow\)"),        # ⇒
    ("\u21d4", r"\(\Leftrightarrow\)"),    # ⇔
    ("\u2194", r"\(\leftrightarrow\)"),    # ↔
    ("\u27f7", r"\(\longleftrightarrow\)"),  # ⟷
    ("\u2713", r"\(\checkmark\)"),         # ✓
    ("\u2460", r"\textbf{(1)}"),           # ①
    ("\u2461", r"\textbf{(2)}"),           # ②
    ("\u2462", r"\textbf{(3)}"),           # ③
    ("\u2463", r"\textbf{(4)}"),           # ④
    ("\u2605", r"$\bigstar$"),             # ★（雅黑无此字形，用数学符号）
]


def fix_symbols(tex):
    for a, b in SYM_MAP:
        tex = tex.replace(a, b)
    return tex


def main():
    os.makedirs(BUILD, exist_ok=True)
    env_path = TEXLIVE + os.pathsep + os.environ.get("PATH", "")
    os.environ["PATH"] = env_path

    print("[1/5] 拼接 markdown")
    md = concat_md()
    print(f"  {md}  ({os.path.getsize(md)} 字节)")

    print("[2/5] pandoc 转 LaTeX 正文")
    body_tex = os.path.join(BUILD, "body.tex")
    code, log = run(["pandoc", md, "-o", body_tex, "-t", "latex",
                     "--wrap=preserve", "--columns=400", "--syntax-highlighting=none"])
    if code != 0:
        print("  ❌ pandoc 失败：", log[-1500:])
        sys.exit(1)
    print(f"  ok ({os.path.getsize(body_tex)} 字节)")

    print("[3/5] 后处理（章节/表格/环境）")
    body = open(body_tex, encoding="utf-8").read()
    body = postprocess(body)
    full = PREAMBLE + "\n" + TITLE + "\n" + body + POSTAMBLE
    tex_path = os.path.join(BUILD, "cram.tex")
    open(tex_path, "w", encoding="utf-8", newline="\n").write(full)
    print(f"  {tex_path}  ({len(full)} 字符)")

    print("[4/5] xelatex 编译（两遍）")
    for i in (1, 2):
        code, log = run(["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                         "cram.tex"], cwd=BUILD)
        print(f"  第 {i} 遍 exit={code}")
        if code != 0:
            print(log[-4000:])
            sys.exit(1)
    pdf = os.path.join(BUILD, "cram.pdf")
    if not os.path.exists(pdf):
        print("  ❌ 未生成 PDF")
        sys.exit(1)

    print("[5/5] 输出")
    shutil.copy2(pdf, OUT_PDF)
    print(f"  ✅ {OUT_PDF}  ({os.path.getsize(OUT_PDF)/1048576:.2f} MB)")


if __name__ == "__main__":
    main()
