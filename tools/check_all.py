#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""一键跑完全部校验。仓库内提交前 / CI 都跑这个。

用法: python tools/check_all.py
退出码 0 = 全绿, 1 = 有问题。
"""
import os, re, sys, glob, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.stdout.reconfigure(encoding="utf-8")

PY = sys.executable
STEPS = [
    ("插图链接归一化（幂等）", "fix_img_paths.py"),
    ("表格裸管道符修复（幂等）", "fix_table_pipes.py"),
    ("覆盖率 / 链接 / 结构校验", "verify.py"),
    ("插图说明页码映射校验", "verify_captions.py"),
    ("文本损坏扫描", "scan_text.py"),
]


def run(script):
    p = os.path.join(HERE, script)
    if not os.path.exists(p):
        return None, f"脚本不存在: {script}"
    r = subprocess.run([PY, p], cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    tail = "\n".join([l for l in (r.stdout or "").strip().splitlines() if l.strip()][-6:])
    return r.returncode, tail + (("\n" + r.stderr.strip()) if r.stderr.strip() else "")


def main():
    print("=" * 74)
    print("《信号分析与处理》笔记仓库 —— 全量校验")
    print("=" * 74)
    failed = []
    for title, script in STEPS:
        code, out = run(script)
        ok = code == 0
        print(f"\n[{ 'PASS' if ok else 'FAIL' }] {title}  ({script})")
        for line in out.splitlines():
            print("      " + line)
        if not ok:
            failed.append((script, out))

    # 额外: 抱佛脚版不得出现例题 / 图片
    cram_dir = os.path.join(ROOT, "cram")
    if os.path.isdir(cram_dir):
        bad = []
        for f in glob.glob(os.path.join(cram_dir, "*.md")):
            t = open(f, encoding="utf-8").read()
            for pat, what in [(r'!\[', "图片引用"),
                              (r'^#{2,4}\s*例\s*\d', "例题小节"),
                              (r'^\*\*解\*\*', "解答段"),
                              (r'自测|练习|习题', "自测/练习")]:
                if re.search(pat, t, re.M):
                    bad.append(f"{os.path.basename(f)}: 含{what}")
        ok = not bad
        print(f"\n[{ 'PASS' if ok else 'FAIL' }] 抱佛脚版纯净度（无例题/无练习/无图片）")
        for b in bad:
            print("      " + b)
        if not ok:
            failed.append(("cram 纯净度", "\n".join(bad)))

    print("\n" + "=" * 74)
    if failed:
        print(f"❌ {len(failed)} 项未通过")
        sys.exit(1)
    print("✅ 全部校验通过")
    sys.exit(0)


if __name__ == "__main__":
    main()
