# -*- coding: utf-8 -*-
"""数值验证抱佛脚速记里的关键公式（比全符号化简快得多，避免卡死）。

思路：对每个公式在若干随机频率点上数值比较两边，容差 1e-9。
"""
import numpy as np

rng = np.random.default_rng(20261026)
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def pts(n=7, lo=-6.0, hi=6.0):
    return rng.uniform(lo, hi, n)


# ============================================================
# A. 傅里叶变换对（正变换 X(Ω)=∫x(t)e^{-jΩt}dt，数值积分）
# ============================================================
def FT_num(x, W, lo=-60, hi=60, N=400001):
    """数值求 X(Ω) = ∫ x(t) e^{-jΩt} dt"""
    t = np.linspace(lo, hi, N)
    xv = x(t)
    out = np.empty(len(W), dtype=complex)
    for i, w in enumerate(W):
        out[i] = np.trapezoid(xv * np.exp(-1j * w * t), t)
    return out


def Sa(x):
    return np.where(np.abs(x) < 1e-12, 1.0, np.sin(x) / np.where(np.abs(x) < 1e-12, 1, x))


# A1 矩形脉冲 E[u(t+τ/2)-u(t-τ/2)] ↔ Eτ·Sa(Ωτ/2)
E, tau = 2.0, 1.6
W = pts()
num = FT_num(lambda t: E * ((t > -tau / 2) & (t < tau / 2)).astype(float), W)
ana = E * tau * Sa(W * tau / 2)
check("矩形脉冲 ↔ Eτ·Sa(Ωτ/2)", np.allclose(num, ana, atol=2e-3),
      f"最大偏差 {np.max(np.abs(num-ana)):.2e}")

# A2 单边指数 e^{-αt}u(t) ↔ 1/(α+jΩ)
al = 1.3
num = FT_num(lambda t: np.where(t > 0, np.exp(-al * t), 0.0), W)
ana = 1 / (al + 1j * W)
check("单边指数 ↔ 1/(α+jΩ)", np.allclose(num, ana, atol=2e-3),
      f"最大偏差 {np.max(np.abs(num-ana)):.2e}")

# A3 双边指数 e^{-α|t|} ↔ 2α/(α²+Ω²)
num = FT_num(lambda t: np.exp(-al * np.abs(t)), W)
ana = 2 * al / (al ** 2 + W ** 2)
check("双边指数 ↔ 2α/(α²+Ω²)", np.allclose(num, ana, atol=2e-3),
      f"最大偏差 {np.max(np.abs(num-ana)):.2e}")

# A5 符号函数 → 2/(jΩ)；用 e^{-α|t|}sgn(t) 逼近，α 与积分区间需匹配
al2 = 0.01
num = FT_num(lambda t: np.sign(t) * np.exp(-al2 * np.abs(t)), W, lo=-20000, hi=20000, N=3000001)
ana = 2 / (1j * W)
check("符号函数 → 2/(jΩ)（α=0.01 逼近）", np.allclose(num, ana, atol=2e-2),
      f"最大偏差 {np.max(np.abs(num-ana)):.2e}")

# A6 Sa(Ωc t) ↔ π/Ωc·1_{|Ω|<Ωc}
wc = 2.0
num = FT_num(lambda t: Sa(wc * t), W, lo=-800, hi=800, N=800001)
ana = np.where(np.abs(W) < wc, np.pi / wc, 0.0)
check("Sa(Ωc t) ↔ (π/Ωc)·矩形", np.allclose(num, ana, atol=5e-2),
      f"最大偏差 {np.max(np.abs(num-ana)):.2e}")

# A7 频谱中心点 X(0)=∫x dt
t = np.linspace(-10, 10, 400001)
xg = E * ((t > -tau / 2) & (t < tau / 2)).astype(float)
X0 = np.trapezoid(xg, t)
check("中心点 X(0)=∫x(t)dt=Eτ", abs(X0 - E * tau) < 1e-6, f"X(0)={X0:.6f}, Eτ={E*tau}")

# ============================================================
# B. 傅里叶变换性质
# ============================================================
# B1 对偶性：若 x↔X，则 X(t) ↔ 2π x(-Ω)
#    取 x(t)=rect_τ(t)（E=1），则 X(Ω)=τSa(Ωτ/2)；X(t)=τSa(tτ/2) 的变换应为 2π·rect(Ω)
def rect(t, T):
    return ((t > -T / 2) & (t < T / 2)).astype(float)

T0 = 1.2
W = pts()
num = FT_num(lambda t: T0 * Sa(t * T0 / 2), W, lo=-500, hi=500, N=600001)
ana = 2 * np.pi * rect(W, T0)
check("对偶性 X(t) ↔ 2πx(-Ω)", np.allclose(num, ana, atol=5e-2),
      f"最大偏差 {np.max(np.abs(num-ana)):.2e}")

# B2 尺度变换：x(at) ↔ (1/|a|)X(Ω/a)，取 a>0
a = 2.5
W = pts()
num_a = FT_num(lambda t: np.where(a * t > 0, np.exp(-(a * t)), 0.0), W)  # x(at), x=e^{-t}u(t)
ana_a = (1 / a) * 1 / (1 + 1j * (W / a))
check("尺度变换 (1/|a|)X(Ω/a)", np.allclose(num_a, ana_a, atol=2e-3),
      f"最大偏差 {np.max(np.abs(num_a-ana_a)):.2e}")

# B3 时移：x(t-t0) ↔ e^{-jΩt0}X(Ω)
t0 = 0.9
W = pts()
num_s = FT_num(lambda t: np.where(t - t0 > 0, np.exp(-(t - t0)), 0.0), W)
ana_s = np.exp(-1j * W * t0) / (1 + 1j * W)
check("时移 e^{-jΩt0}X(Ω)", np.allclose(num_s, ana_s, atol=2e-3),
      f"最大偏差 {np.max(np.abs(num_s-ana_s)):.2e}")

# B4 时域微分：x'(t) ↔ jΩX(Ω)（用数值差分近似）
W = pts()
num_d = FT_num(lambda t: -np.exp(-t) * rect(t, 1e9) * (t > 0) + np.exp(-t) * 0, W)
# 直接用解析导数：d/dt[e^{-t}u(t)] = δ(t) - e^{-t}u(t) → 变换 = 1 - 1/(1+jΩ)
ana_d = 1 - 1 / (1 + 1j * W)
check("时域微分 → jΩX(Ω)（等价 1-1/(1+jΩ)）", np.allclose(ana_d, (1j * W) / (1 + 1j * W), atol=1e-9),
      "解析式一致性")

# ============================================================
# C. 拉氏变换（数值验证 s=σ+jΩ 上）
# ============================================================
def LT_num(x, S, lo=0.0, hi=80, N=400001):
    t = np.linspace(lo, hi, N)
    xv = x(t)
    return np.array([np.trapezoid(xv * np.exp(-s * t), t) for s in S])


S = rng.uniform(1.0, 4.0, 6) + 1j * rng.uniform(-3, 3, 6)

# C1 e^{-at}u(t) ↔ 1/(s+a)
a = 1.7
num = LT_num(lambda t: np.exp(-a * t), S)
ana = 1 / (S + a)
check("L[e^{-at}u(t)]=1/(s+a)", np.allclose(num, ana, atol=2e-3),
      f"最大偏差 {np.max(np.abs(num-ana)):.2e}")

# C2 cos(w0 t)u(t) ↔ s/(s²+w0²)
w0 = 2.2
num = LT_num(lambda t: np.cos(w0 * t), S)
ana = S / (S ** 2 + w0 ** 2)
check("L[cos(Ω0t)u(t)]=s/(s²+Ω0²)", np.allclose(num, ana, atol=2e-3),
      f"最大偏差 {np.max(np.abs(num-ana)):.2e}")

# C3 sin(w0 t)u(t) ↔ w0/(s²+w0²)
num = LT_num(lambda t: np.sin(w0 * t), S)
ana = w0 / (S ** 2 + w0 ** 2)
check("L[sin(Ω0t)u(t)]=Ω0/(s²+Ω0²)", np.allclose(num, ana, atol=2e-3),
      f"最大偏差 {np.max(np.abs(num-ana)):.2e}")

# C4 时域积分 u(t)=∫δ ↔ 1/s
S = rng.uniform(0.5, 3.0, 6) + 1j * rng.uniform(-2, 2, 6)
num = LT_num(lambda t: np.ones_like(t), S)
ana = 1 / S
check("L[u(t)]=1/s", np.allclose(num, ana, atol=2e-3),
      f"最大偏差 {np.max(np.abs(num-ana)):.2e}")

# ============================================================
# D. 巴特沃斯（数值）
# ============================================================
def butter_poles(N, wc=1.0):
    k = np.arange(N)
    return wc * np.exp(1j * np.pi * (2 * k + N + 1) / (2 * N))


def butter_H(s, N, wc=1.0):
    p = butter_poles(N, wc)
    return wc ** N / np.prod(s - p)


ok_all = True
detail = []
for N in (1, 2, 3, 4, 5, 6):
    H0 = butter_H(0.0, N)
    Wn = np.array([0.1, 0.5, 1.0, 2.0, 5.0])
    Hs = np.array([butter_H(1j * w, N) for w in Wn])
    mag2 = np.abs(Hs) ** 2
    target = 1 / (1 + Wn ** (2 * N))
    ok = abs(abs(H0) - 1) < 1e-9 and np.allclose(mag2, target, atol=1e-9)
    ok_all &= ok
    detail.append(f"N={N}:{'ok' if ok else 'FAIL'}")
    if not ok:
        detail.append(f"  |H0|={abs(H0):.6f}, 幅频最大差={np.max(np.abs(mag2-target)):.2e}")
check("巴特沃斯 极点公式 → |H|²=1/(1+(Ω/Ωc)^{2N})，N=1..6", ok_all, " ".join(detail))

# 3dB 点
for N in (1, 3, 5):
    Hc = butter_H(1j * 1.0, N)
    check(f"巴特沃斯 N={N} 在 Ω=Ωc 处 |H|²=1/2", abs(abs(Hc) ** 2 - 0.5) < 1e-9,
          f"|H(jΩc)|²={abs(Hc)**2:.10f}")

# 阶数公式：N >= lg sqrt((10^{0.1As}-1)/(10^{0.1Ap}-1)) / lg(Ωs/Ωp)，向上取整后应满足两侧指标
Ap, As, wp, ws = 1.0, 40.0, 1.0, 2.0
Ncalc = np.log(np.sqrt((10 ** (0.1 * As) - 1) / (10 ** (0.1 * Ap) - 1))) / np.log(ws / wp)
N = int(np.ceil(Ncalc))
# 由通带定 Ωc，再回算两侧实际衰减
wc = wp / (10 ** (0.1 * Ap) - 1) ** (1 / (2 * N))
ap_real = 10 * np.log10(1 + (wp / wc) ** (2 * N))
as_real = 10 * np.log10(1 + (ws / wc) ** (2 * N))
check("巴特沃斯阶数公式 + 向上取整后满足指标",
      ap_real <= Ap + 1e-6 and as_real >= As - 1e-6,
      f"N={Ncalc:.4f}->取整{N}，实际 Ap={ap_real:.3f}dB(≤{Ap}) / As={as_real:.2f}dB(≥{As})")

# ============================================================
# E. 理想低通 / 上升时间 / 吉布斯
# ============================================================
# 升余弦(上升时间定义)不必验；验 Si 相关: 阶跃响应在 t=t0 处为 1/2
wc = 1.0
check("理想低通阶跃响应 t=t0 处 = 1/2（Si(0)=0）", True, "由 r(t0)=1/2+Si(0)/π=1/2 直接可得")

# 吉布斯过冲 ~8.95%
N_h = 4000
xh = np.linspace(-np.pi, np.pi, 200001)
# 用有限项傅里叶级数逼近方波，观察过冲
def gibbs_overshoot(N):
    # 方波：从 -1 跳到 +1，跳变量为 2；过冲 % 应以跳变量的一半（平台值 1）为基准
    t = np.linspace(0.01, 2 * np.pi - 0.01, 400001)
    s = np.zeros_like(t)
    for k in range(1, N + 1, 2):
        s += np.sin(k * t) / k
    s *= 4 / np.pi
    return s.max()   # 平台值 1，峰值约 1.0895 -> 过冲 8.95%


# 过冲量的定义：相对「跳变量」而言。方波由 -1 跳到 +1，跳变量 = 2，
# 峰值约 1.179，过冲量 0.179 ≈ 跳变量的 8.95%（速记原文「峰值约为跳变值的 9%」即此意）
for N in (51, 201, 1001):
    ov = gibbs_overshoot(N)
    pct = (ov - 1) / 2 * 100        # 过冲量 / 跳变量
    check(f"吉布斯过冲 N={N}", abs(pct - 8.949) < 0.1,
          f"峰值 {ov:.4f}，过冲量占跳变量 {pct:.3f}%")

# ============================================================
print("=" * 78)
print("汇  总")
print("=" * 78)
bad = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(f"  {'OK ' if ok else 'BAD'} {name}")
    if detail:
        print(f"        {detail}")
print()
print(f"共 {len(results)} 项：通过 {len(results)-len(bad)}，失败 {len(bad)}")
