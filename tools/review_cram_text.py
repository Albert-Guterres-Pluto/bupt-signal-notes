# -*- coding: utf-8 -*-
r"""抱佛脚速记：文本层一致性核查（术语 / 符号 / 编号 / 交叉引用 / 表格结构）。"""
import glob, os, re, sys, collections

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "笔记", "00-抱佛脚版")
FILES = sorted(glob.glob(os.path.join(SRC, "*.md")))

issues = []


def add(fn, line, kind, msg):
    issues.append((fn, line, kind, msg))


print("=" * 78)
print("A. 术语一致性：对偶性 / 对称性")
print("=" * 78)
for f in FILES:
    for i, ln in enumerate(open(f, encoding="utf-8").read().splitlines(), 1):
        if "对称性" in ln:
            # 「对偶性」重命名只针对傅里叶变换的**性质名**；
            # 「波形对称性 / 半波对称 / 奇偶对称」讲的是波形形状，属另一个概念，不算旧名残留
            OK_CTX = ("旧称对称性", "旧版", "波形对称性", "半波对称", "奇偶对称", "对称性省事")
            if not any(k in ln for k in OK_CTX):
                add(os.path.basename(f), i, "术语", "用了旧名「对称性」但未注明是旧称")
        if "对偶性" in ln:
            pass
n_dui = sum(open(f, encoding="utf-8").read().count("对偶性") for f in FILES)
print(f"  「对偶性」出现 {n_dui} 次")
bad = [x for x in issues if x[2] == "术语"]
print(f"  问题：{len(bad)}")
for b in bad:
    print(f"    {b[0]}:{b[1]} {b[3]}")
    print(f"       ...{''}")

print()
print("=" * 78)
print("B. 符号：σ / τ 的用法（τ 只该用于时间常数、脉宽、积分变量）")
print("=" * 78)
TAU_OK = ("时间常数", "脉宽", "积分变量", "延时", "延迟", "t\\tau", "\\tau}", "\\tau ", "d\\tau",
          "\\tau\\downarrow", "\\tau\\to0", "\\tau>0", "\\tau/2", "\\tau_i", "τ", "\\tau_0",
          "G_\\tau", "nT", "f(\\tau)", "x(\\tau)", "h(t-\\tau)", "e^{-t/\\tau}", "|t|/\\tau",
          "\\tau\\text{", "\\tau_{", "\\tau)", "\\tau\\cdot", "S_\\tau", "时间常数 \\tau")
n_sigma = sum(open(f, encoding="utf-8").read().count("sigma") for f in FILES)
print(f"  σ(sigma) 出现 {n_sigma} 次；τ(tau) 出现 "
      f"{sum(open(f, encoding='utf-8').read().count(chr(92)+'tau') for f in FILES)} 次")

print()
print("=" * 78)
print("C. 章节编号连续性")
print("=" * 78)
CN_NUM = "一二三四五六七八九十"
for f in FILES:
    lines = open(f, encoding="utf-8").read().splitlines()
    part = None
    seq = []
    for i, ln in enumerate(lines, 1):
        if ln.startswith("# "):
            part = ln[2:].strip()
            seq = []
        m = re.match(r"^## ([一二三四五六七八九十]+)、", ln)
        if m:
            seq.append((m.group(1), i, ln[3:].strip()[:30]))
        m2 = re.match(r"^## (\d+)\. ", ln)
        if m2:
            seq.append((m2.group(1), i, ln[3:].strip()[:30]))
    if not seq:
        continue
    # 中文序号
    if all(s[0] in CN_NUM for s in seq):
        idx = [CN_NUM.index(s[0]) for s in seq]
        ok = idx == list(range(len(idx)))
        print(f"  {os.path.basename(f)}（{len(seq)} 节）: {'✅ 连续' if ok else '❌ 不连续 ' + str([s[0] for s in seq])}")
        if not ok:
            add(os.path.basename(f), 0, "编号", f"中文序号不连续 {[s[0] for s in seq]}")
    else:
        idx = [int(s[0]) for s in seq]
        ok = idx == list(range(idx[0], idx[0] + len(idx)))
        print(f"  {os.path.basename(f)}（{len(seq)} 节）: {'✅ 连续' if ok else '❌ 不连续 ' + str(idx)}")

print()
print("=" * 78)
print("D. 不应出现的内容（例题/练习/自测）")
print("=" * 78)
BANNED = [("图片", re.compile(r'!\[')),
          ("例题小节", re.compile(r'^\s*#{2,4}\s*例\s*\d', re.M)),
          ("解答段落", re.compile(r'^\s*\*\*解\*\*', re.M)),
          ("自测/练习", re.compile(r'^\s*#{2,4}\s*(自测|练习|习题)', re.M)),
          ("举例引导", re.compile(r'(我们来看|下面来看|举一个例子|例如：)', re.M)),
          ("管理信息", re.compile(r'(学时|学分|成绩构成|指标点|闭卷|教学周|考核)'))]
for f in FILES:
    txt = open(f, encoding="utf-8").read()
    for label, pat in BANNED:
        m = pat.search(txt)
        if m:
            ln = txt[:m.start()].count("\n") + 1
            add(os.path.basename(f), ln, "违禁", f"出现{label}: {m.group(0)[:30]!r}")
bad = [x for x in issues if x[2] == "违禁"]
print(f"  问题：{len(bad)}")
for b in bad:
    print(f"    {b[0]}:{b[1]} {b[3]}")

print()
print("=" * 78)
print("E. 表格结构（列数一致 / 不含裸管道符）")
print("=" * 78)
for f in FILES:
    lines = open(f, encoding="utf-8").read().splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("|") and i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i + 1]):
            hdr_n = lines[i].count("|") - 1
            j = i + 2
            row = 0
            while j < len(lines) and lines[j].startswith("|"):
                n = lines[j].count("|") - 1
                if n != hdr_n:
                    add(os.path.basename(f), j + 1, "表格", f"列数 {n} != 表头 {hdr_n}")
                row += 1
                j += 1
            i = j
        else:
            i += 1
bad = [x for x in issues if x[2] == "表格"]
print(f"  问题：{len(bad)}")
for b in bad[:10]:
    print(f"    {b[0]}:{b[1]} {b[3]}")

print()
print("=" * 78)
print("F. 交叉引用（见 §N / 第 N 节）是否指向存在的节")
print("=" * 78)
for f in FILES:
    txt = open(f, encoding="utf-8").read()
    secs = set(re.findall(r'^## (\d+)\.', txt, re.M))
    for m in re.finditer(r'见\s*§\s*(\d+)', txt):
        if m.group(1) not in secs:
            ln = txt[:m.start()].count("\n") + 1
            add(os.path.basename(f), ln, "引用", f"见 §{m.group(1)} 但本文件无该节")
bad = [x for x in issues if x[2] == "引用"]
print(f"  问题：{len(bad)}")
for b in bad:
    print(f"    {b[0]}:{b[1]} {b[3]}")

print()
print("=" * 78)
print("G. 重复内容（同一行出现两次以上）")
print("=" * 78)
alllines = collections.Counter()
for f in FILES:
    for ln in open(f, encoding="utf-8").read().splitlines():
        s = ln.strip()
        if len(s) > 25:
            alllines[s] += 1
dups = [(s, c) for s, c in alllines.items() if c > 1]
print(f"  完全重复的长行：{len(dups)}")
for s, c in dups[:6]:
    print(f"    ×{c}  {s[:70]}")

print()
print("=" * 78)
print("汇  总")
print("=" * 78)
by_kind = collections.Counter(x[2] for x in issues)
print(f"  共发现 {len(issues)} 处问题：{dict(by_kind) or '无'}")
