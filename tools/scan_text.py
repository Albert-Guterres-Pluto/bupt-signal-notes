#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""扫描笔记中的文本损坏迹象。

判据:
- BOM / U+FFFD 替换字符
- 同一汉字连续出现 ≥3 次 (几乎不可能是正常中文)
- 同一汉字连续出现 2 次, 且该双字词不在常用词白名单内 (排除"一一对应/等等"等正常叠字)
- "课件"被误替换为"件件"等脚本化替换痕迹
- 数学公式常见的 1/|a| 之类裸管道符残留 (破表风险)
"""
import os, re, sys, glob, collections
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NOTES = os.path.join(ROOT, "笔记")

# 常见正当叠字双字词
OK2 = set("""
一一 二二 三三 两两 步步 层层 处处 点点 常常 渐渐 仅仅 慢慢 每每 明明 明明
偏偏 频频 频频 平平 恰恰 悄悄 轻轻 区区 稍稍 深深 时时 数数 死死 统统 偷偷
往往 微微 细细 渐渐 好好 乖乖 高高 多多 少少 迟迟 早早 久久 远远 紧紧 牢牢
依依 连连 屡屡 略略 忙忙 蒙蒙 默默 喃喃 念念 团团 弯弯 汪汪 心心 星星 徐徐
一一 一一 等等 般般 草草 颤颤 场场 层层 朝朝 沉沉 出出 楚楚 匆匆 簇簇 寸寸
代代 旦旦 荡荡 道道 地地 叠叠 点点 叮叮 栋栋 短短 多多 朵朵 泛泛 方方 纷纷
个个 更更 公公 姑姑 乖乖 关关 管管 光光 行行 浩浩 狠狠 哄哄 花花 缓缓 晃晃
家家 渐渐 件件 仅仅 精精 久久 句句 卷卷 看看 棵棵 空空 苦苦 块块 款款 浪浪
牢牢 累累 历历 连连 凉凉 亮亮 寥寥 林林 溜溜 隆隆 碌碌 屡屡 缕缕 略略 落落
满满 漫漫 茫茫 毛毛 蒙蒙 密密 面面 明明 冥冥 默默 某某 幕幕 年年 念念 娘亲
拍拍 偏偏 频频 平平 齐齐 恰恰 芊芊 悄悄 切切 区区 拳拳 人人 日日 融融 软软
洒洒 三三 深深 生生 声声 时时 事事 试试 世世 是是 收收 时时 双双 说说 丝丝
死死 松松 速速 算算 岁岁 太太 谈谈 堂堂 滔滔 天天 条条 听听 通通 统统 头头
突突 团团 弯弯 往往 微微 巍巍 唯唯 娓娓 稳稳 问问 嗡嗡 我我 稀稀 细细 下下
先先 想想 小小 谢谢 心心 星星 行行 醒醒 熊熊 徐徐 许许 续续 喧喧 学学 雪雪
熏熏 循循 压压 呀呀 言言 严严 眼眼 央央 洋洋 摇摇 遥遥 一一 依依 奕奕 翼翼
阴阴 殷殷 隐隐  Ying 硬硬 悠悠 犹犹 有有 圆圆 远远 怨怨 跃跃 云云 芸芸 早早
嶂嶂 招招 真真 整整 正正 枝枝 直直 植植 种种 重重 周周 株株 逐逐 转转 准准
孜孜 字字 总总 走走 足足 尊尊 多多 星星 点点 滴滴 哈哈 呵呵 嘻嘻 嘿嘿 呼呼
""".split())
LEGIT_RE = re.compile(r'^(.)\1$')


def legit(prev_ch, pair, ctx):
    """判断重复双字是否正当。"""
    if pair in OK2:
        return True
    # 跨词边界: '性质性质' 这类其实是被前一个词的末字与后一个词的首字碰巧相同
    if len(ctx) >= 4:
        # 例如 "线性性质": 重复出现在 "性"+"性", 前字构成 "线性"
        if ctx[0] in "性形原级数带态点面体线" and len(ctx) >= 2:
            return True
    return False


ALLOW_CTX = ["线性性质", "性性质", "形形式", "形形状", "原原理", "原原信号", "级级联", "级级数",
             "带带宽", "态态度", "面面积", "体体积", "信信号", "观观察", "题题面", "大大扩展",
             "刚刚过去", "实实在在", "在在可以", "根根离散", "件件", "点点点",
             # 正规术语：这些词的相邻两字天然相同，不是损坏
             "部分分式", "部分分数", "分分式", "分分析", "分分解", "初始条件时", "件时"]

suspects = []
stats = collections.Counter()

for md in sorted(glob.glob(os.path.join(NOTES, "**", "*.md"), recursive=True)):
    rel = os.path.relpath(md, ROOT)
    raw = open(md, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        suspects.append(f"[BOM] {rel}")
    txt = raw.decode("utf-8")
    stats["files"] += 1
    stats["chars"] += len(txt)
    n_fffd = txt.count("\ufffd")
    if n_fffd:
        stats["fffd"] += n_fffd
        suspects.append(f"[替换字符 U+FFFD ×{n_fffd}] {rel}")
    for m in re.finditer(r'([\u4e00-\u9fff])\1{1,}', txt):
        w = m.group(0)
        line = txt[:m.start()].count("\n") + 1
        ctx = txt[max(0, m.start() - 2):m.end() + 2]
        if len(w) >= 3:
            suspects.append(f"[三连重复 {w}] {rel}:{line} … {ctx}")
            continue
        if w in OK2:
            continue
        if any(a in ctx for a in ALLOW_CTX):
            continue
        suspects.append(f"[重复字 {w}] {rel}:{line} … {ctx}")
    # '件' 出现在明显应为 '课' 的语境。注意 "条件时" / "事件时" 等是正常词，
    # 只匹配真正的损坏形态（"件件"、"件堂"、"件程"），不要匹配单字"件+时"。
    for m in re.finditer(r'件(件|堂|程)(?!时)', txt):
        line = txt[:m.start()].count("\n") + 1
        suspects.append(f"[疑似 课->件 替换] {rel}:{line} … {txt[max(0,m.start()-25):m.start()+25]!r}")
    # 反向: 统计正当用法的 '件' 词频, 便于人工核对
    for w in ("文件", "条件", "组件", "事件", "硬件", "件数", "软件", "元件", "部件"):
        stats[w] += txt.count(w)
    for w in ("课件", "课堂", "条件", "硬件", "事件", "文件", "组件"):
        stats[w] += txt.count(w)

print(f"扫描 {stats['files']} 个 md, 共 {stats['chars']} 字符")
print("词频: " + ", ".join(f"{w}={stats[w]}" for w in ("课件", "课堂", "条件", "硬件", "事件", "文件", "组件")))
print(f"U+FFFD 替换字符: {stats['fffd']}")
print()
if suspects:
    print(f"⚠️ 发现 {len(suspects)} 处可疑:")
    for s in suspects:
        print("  -", s)
else:
    print("✅ 未发现文本损坏迹象")
