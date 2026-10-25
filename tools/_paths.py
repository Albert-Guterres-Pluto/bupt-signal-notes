#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""统一路径探测：让脚本同时适配「工作区」与「git 仓库」两种布局。

工作区:  信号/笔记/*.md           信号/assets/slidesNN/*.jpg     输出在 信号/ 根
仓库:    仓库/notes/*.md          仓库/images/slidesNN/*.jpg     输出在 仓库/ 根
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# 笔记目录
if os.path.isdir(os.path.join(ROOT, "笔记")):
    NOTES_DIR = os.path.join(ROOT, "笔记")
    NOTES_NAME = "笔记"
    IS_REPO = False
elif os.path.isdir(os.path.join(ROOT, "notes")):
    NOTES_DIR = os.path.join(ROOT, "notes")
    NOTES_NAME = "notes"
    IS_REPO = True
else:
    NOTES_DIR = os.path.join(ROOT, "笔记")
    NOTES_NAME = "笔记"
    IS_REPO = False

# 图片目录
if os.path.isdir(os.path.join(ROOT, "assets")):
    IMAGES_DIR = os.path.join(ROOT, "assets")
    IMAGES_NAME = "assets"
elif os.path.isdir(os.path.join(ROOT, "images")):
    IMAGES_DIR = os.path.join(ROOT, "images")
    IMAGES_NAME = "images"
else:
    IMAGES_DIR = os.path.join(ROOT, "assets")
    IMAGES_NAME = "assets"

# 抱佛脚版目录（工作区在 笔记/00-抱佛脚版，仓库在 cram/）
_cram_in_notes = os.path.join(NOTES_DIR, "00-抱佛脚版")
if os.path.isdir(_cram_in_notes):
    CRAM_DIR = _cram_in_notes
elif os.path.isdir(os.path.join(ROOT, "cram")):
    CRAM_DIR = os.path.join(ROOT, "cram")
else:
    CRAM_DIR = _cram_in_notes

# 输出文件名
COMBINED_OUT = os.path.join(ROOT, "signal-notes.md" if IS_REPO else "信号分析与处理-完整笔记.md")
CRAM_OUT = os.path.join(ROOT, "cram-sheet.md" if IS_REPO else "信号分析与处理-抱佛脚速记.md")
