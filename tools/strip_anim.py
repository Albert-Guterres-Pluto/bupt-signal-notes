#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""生成"去动画版" pptx：删除所有幻灯片的 <p:timing>（动画）与 <p:transition>（切换）。

用途：LibreOffice 导出 PDF 时会把动画的各个"构建步"全部拍平，造成同一公式/图形
在一页里叠印多份（某些课件里很明显）。删掉 timing 后导出即为"最终态"，画面干净。

用法:
  python _tools\strip_anim.py <输入.pptx> [输出.pptx]
默认输出到 _tools/pdf/<原名>-noanim.pptx
"""
import os, re, sys, zipfile, shutil
from lxml import etree

sys.stdout.reconfigure(encoding="utf-8")
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS = {"p": P}


def strip(src, dst):
    zin = zipfile.ZipFile(src)
    zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    n_slides = n_stripped = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if re.match(r"ppt/slides/slide\d+\.xml$", item.filename):
            n_slides += 1
            try:
                root = etree.fromstring(data)
            except etree.XMLSyntaxError:
                # 畸形属性容错（历史上 01 课件有此问题）
                txt = data.decode("utf-8", "replace")
                txt = re.sub(r'\s([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*"([^"]*)"',
                             lambda m: '' if len(m.group(2)) > 100000 else m.group(0), txt)
                root = etree.fromstring(txt.encode("utf-8"))
            removed = False
            for tag in ("timing", "transition"):
                for el in root.findall(f"{{{P}}}{tag}"):
                    el.getparent().remove(el)
                    removed = True
            if removed:
                n_stripped += 1
                data = etree.tostring(root, xml_declaration=True,
                                      encoding="UTF-8", standalone=True)
        zout.writestr(item, data)
    zout.close()
    zin.close()
    print(f"  幻灯片 {n_slides} 页，去掉动画/切换节点 {n_stripped} 页")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    src = sys.argv[1]
    base = os.path.splitext(os.path.basename(src))[0]
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "pdf", f"{base}-noanim.pptx")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    print(f"输入: {src}")
    strip(src, dst)
    print(f"输出: {dst}  ({os.path.getsize(dst)/1048576:.1f} MB)")
