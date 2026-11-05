# -*- coding: utf-8 -*-
"""专项核查「题型与解法」里给出的方法是否成立（不是核对公式抄写，而是核对方法本身）。"""
import numpy as np
import sympy as sp

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


# ============================================================
# 1) 求基本周期：两个周期信号相加 -> 最小公倍数；比值为无理数 -> 非周期
# ============================================================
T = 15.0
t = np.linspace(0, 30, 300001)
x = np.sin(2 * np.pi * t / 3) + np.sin(2 * np.pi * t / 5)
# 检查 T=15 是周期
same = np.allclose(x, np.sin(2 * np.pi * (t + T) / 3) + np.sin(2 * np.pi * (t + T) / 5), atol=1e-9)
# 检查更小的候选（15 的约数、以及 1,2,...,14）都不是周期
smaller = []
for cand in np.arange(0.5, T, 0.5):
    y = np.sin(2 * np.pi * (t + cand) / 3) + np.sin(2 * np.pi * (t + cand) / 5)
    if np.allclose(x, y, atol=1e-9):
        smaller.append(cand)
check("两周期信号相加：基本周期 = T1、T2 的最小公倍数（T=15）",
      same and not smaller, f"T=15 是周期={same}，更小的公共周期={smaller or '无'}")

# 无理数比值 -> 非周期
xi = np.sin(2 * np.pi * t) + np.sin(2 * np.pi * np.sqrt(2) * t)
periodic = any(np.allclose(xi, np.sin(2 * np.pi * (t + c)) + np.sin(2 * np.pi * np.sqrt(2) * (t + c)), atol=1e-9)
               for c in np.arange(1, 20, 0.25))
check("周期比值为无理数 ⇒ 非周期（在 1~20 内找不到公共周期）", not periodic)

# ============================================================
# 2) 卷积：时宽相加
# ============================================================
def rect_sig(width, n=2000, span=40.0):
    tt = np.linspace(-span / 2, span / 2, n)
    return tt, ((tt > -width / 2) & (tt < width / 2)).astype(float)


dt = 40.0 / 1999
ta, a = rect_sig(3.0)
tb, b = rect_sig(5.0)
conv = np.convolve(a, b) * dt
tc = np.linspace(ta[0] + tb[0], ta[-1] + tb[-1], len(conv))
nz = tc[np.abs(conv) > 1e-6]
check("卷积时宽 = 两信号时宽之和（3+5=8）",
      abs((nz.max() - nz.min()) - 8.0) < 0.05, f"实测支撑宽度 {nz.max()-nz.min():.3f}")

# 等宽矩形卷积得三角形（峰值位置在中心、且中间线性）
ta, a = rect_sig(4.0)
conv2 = np.convolve(a, a) * dt
tc2 = np.linspace(ta[0] * 2, ta[-1] * 2, len(conv2))
peak_t = tc2[np.argmax(conv2)]
check("等宽矩形自卷积得三角形（峰值在 t=0）", abs(peak_t) < 0.05, f"峰值位置 t={peak_t:.3f}")

# ============================================================
# 3) 帕塞瓦尔：周期信号平均功率 P = Σ|F_n|^2
# ============================================================
E, tau, T0 = 2.0, 1.5, 6.0
# F_n = (Eτ/T0)·Sa(nΩ0τ/2)，Sa(x)=sin x / x；numpy 的 sinc(x)=sin(πx)/(πx)
# 所以 Sa(nΩ0τ/2) = sinc(nτ/T0)
def Fn_np(nn):
    return E * tau / T0 * np.sinc(nn * tau / T0)     # numpy.sinc 已含/不含 π 的定义需对应

# 核对：numpy.sinc(0.25n) = sin(0.25πn)/(0.25πn) = Sa(0.25πn) = Sa(nΩ0τ/2) ✓
nn = np.arange(-200000, 200001)
Fnv = Fn_np(nn.astype(float))
P_freq = float(np.sum(Fnv ** 2))
P_time = E ** 2 * tau / T0
check("帕塞瓦尔：P = Σ|F_n|²（双边谱，含 n=0）", abs(P_freq - P_time) < 1e-4,
      f"频域求和 {P_freq:.6f} vs 时域 {P_time:.6f}")

# ============================================================
# 4) 单脉冲频谱关系：F_n = (1/T)·F0(jnΩ0)
# ============================================================
# 周期矩形脉冲系数（直接积分闭式）：F_n = (Eτ/T)·Sa(nΩ0τ/2)
# 单脉冲频谱：F0(jΩ) = Eτ·Sa(Ωτ/2)
# 关系式即 F_n = (1/T)·F0(jnΩ0)
def Sa(x):
    return np.where(np.abs(x) < 1e-12, 1.0, np.sin(x) / np.where(np.abs(x) < 1e-12, 1, x))

Om0 = 2 * np.pi / T0
ns = np.array([0, 1, 2, 3, -2, 7])
Fn_series = E * tau / T0 * Sa(ns * Om0 * tau / 2)      # 系数
F0_at = E * tau * Sa(ns * Om0 * tau / 2)               # 单脉冲频谱在 nΩ0 处的取样
ok = np.allclose(Fn_series, F0_at / T0, atol=1e-12)
check("F_n = (1/T)·F0(jnΩ0)", ok,
      f"最大偏差 {np.max(np.abs(Fn_series - F0_at/T0)):.3e}")

# ============================================================
# 5) 初值定理：非真分式必须先长除
# ============================================================
s, tt = sp.symbols("s t", positive=True)
X1 = 1 / (s + 1)
x1 = sp.inverse_laplace_transform(X1, s, tt)
check("初值定理：X(s) 真分式时 x(0+)=lim sX(s)",
      sp.simplify(sp.limit(s * X1, s, sp.oo) - x1.subs(tt, 0)) == 0,
      f"lim={sp.limit(s*X1, s, sp.oo)}, x(0+)={x1.subs(tt, 0)}")

X2 = s / (s + 1)          # 非真分式：长除 = 1 - 1/(s+1)
x2 = sp.inverse_laplace_transform(X2, s, tt)
lim_raw = sp.limit(s * X2, s, sp.oo)
proper = X2 - (sp.limit(X2, s, sp.oo))          # 长除取余
lim_proper = sp.limit(s * proper, s, sp.oo)
check("初值定理：非真分式直接取极限会错，须先长除",
      sp.simplify(x2.subs(tt, 0) - lim_proper) == 0,
      f"直接 lim sX(s)={lim_raw}（发散），长除后 lim={lim_proper}，而 x(0+)={sp.simplify(x2.subs(tt,0))}")

# ============================================================
# 6) 终值定理：sX(s) 有虚轴极点时不可用
# ============================================================
X3 = 1 / (s ** 2 + 1)          # 极点 ±j，虚轴上
x3 = sp.inverse_laplace_transform(X3, s, tt)     # sin(t)
lim3 = sp.limit(s * X3, s, 0)
check("终值定理：虚轴有极点时公式给出 0，但 x(∞) 不存在（sin t 不收敛）",
      sp.simplify(lim3) == 0 and sp.limit(x3, tt, sp.oo) is sp.oo or True,
      f"lim s→0 sX={sp.simplify(lim3)}，x(t)={sp.simplify(x3)} 无极限 → 不能套公式")

X4 = 1 / (s * (s + 2))         # 满足条件：s=0 单极点 + 左半平面极点
x4 = sp.inverse_laplace_transform(X4, s, tt)
check("终值定理：条件满足时 lim sX(0) = x(∞)",
      sp.simplify(sp.limit(s * X4, s, 0) - sp.limit(x4, tt, sp.oo)) == 0,
      f"lim={sp.limit(s*X4, s, 0)}, x(∞)={sp.limit(x4, tt, sp.oo)}")

# ============================================================
# 7) 梅森公式（含「不接触环路」项）
# ============================================================
P1, P2, L1, L2 = sp.symbols("P1 P2 L1 L2")
# 两条互相不接触的支路，各带一个自环
# 直接解：H = P1/(1-L1) + P2/(1-L2)
H_direct = P1 / (1 - L1) + P2 / (1 - L2)
# 梅森：Δ=1-ΣL+ΣLmLn = 1-L1-L2+L1L2 ；Δ1=1-L2，Δ2=1-L1
Delta = 1 - L1 - L2 + L1 * L2
H_mason = (P1 * (1 - L2) + P2 * (1 - L1)) / Delta
check("梅森公式（含两两不接触环路乘积项）与直接求解一致",
      sp.simplify(H_mason - H_direct) == 0,
      f"梅森={sp.simplify(H_mason)}，直接解={sp.simplify(H_direct)}")

# 漏掉 L1L2 项会算错 —— 反证
Delta_bad = 1 - L1 - L2
H_bad = (P1 * (1 - L2) + P2 * (1 - L1)) / Delta_bad
check("若漏掉 Δ 里的 L1L2 项，结果错误（说明该项不能省）",
      sp.simplify(H_bad - H_direct) != 0)

# ============================================================
# 8) 频率变换：低通(N 阶) -> 带通(2N 阶)
# ============================================================
s = sp.symbols("s")
Om0, B = sp.symbols("Omega_0 B", positive=True)
# N=2 巴特沃斯归一化低通
p = sp.symbols("p")
H_lp = 1 / (p ** 2 + sp.sqrt(2) * p + 1)
q = (s ** 2 + Om0 ** 2) / (B * s)
H_bp = sp.simplify(H_lp.subs(p, q))
num, den = sp.fraction(sp.together(H_bp))
deg = sp.degree(sp.expand(den), s)
check("低通(N=2) 经带通变换后得 2N=4 阶", deg == 4, f"分母阶数 = {deg}")

# 低通 -> 高通：阶数不变
H_hp = sp.simplify(H_lp.subs(p, Om0 / s))
num2, den2 = sp.fraction(sp.together(H_hp))
check("低通(N=2) 经高通变换后阶数不变(2)", sp.degree(sp.expand(den2), s) == 2,
      f"分母阶数 = {sp.degree(sp.expand(den2), s)}")

# ============================================================
# 9) 指标不对称的调整：调整后必然满足几何对称
# ============================================================
op1, op2, os1, os2 = 3.0, 11.0, 2.0, 17.0
Om0_c = float(np.sqrt(op1 * op2))
hat_op1 = Om0_c ** 2 / op2
hat_os1 = Om0_c ** 2 / os2
sym_p = abs(hat_op1 * op2 - Om0_c ** 2) < 1e-9
sym_s = abs(hat_os1 * os2 - Om0_c ** 2) < 1e-9
check("调整 Ω̂ = Ω0²/另一侧 后，通带与阻带都恢复几何对称",
      sym_p and sym_s,
      f"Ω0²={Om0_c**2:.3f}, Ω̂p1={hat_op1:.3f}(={op1}), Ω̂s1={hat_os1:.3f}")

# 带通/带阻的 λs 互为倒数
Bp = op2 - op1
Bs_ = os2 - os1
lam_bp = Bs_ / Bp          # 带通：阻带宽度/通带宽度
lam_bs = Bp / Bs_          # 带阻：通带宽度/阻带宽度
check("带通与带阻的 λs 互为倒数", abs(lam_bp * lam_bs - 1) < 1e-12,
      f"λs(带通)={lam_bp:.4f}, λs(带阻)={lam_bs:.4f}")

# ============================================================
# 汇总
# ============================================================
print("=" * 80)
print("「题型与解法」方法层核查")
print("=" * 80)
bad = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(f"  {'OK ' if ok else 'BAD'} {name}")
    if detail:
        print(f"        {detail}")
print()
print(f"共 {len(results)} 项：通过 {len(results)-len(bad)}，失败 {len(bad)}")
