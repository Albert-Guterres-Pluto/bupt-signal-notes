# 《信号分析与处理》抱佛脚速记

考前突击用：**只有概念、公式、性质和条件**，没有例题、没有练习、没有图片。
按「考前 1 小时」的用法组织——三篇按顺序扫一遍，重点看标了 ⚠️ 的条件和易错点。

> **完整版**（含例题、推导、课件截图）：[信号分析与处理-完整笔记.md](信号分析与处理-完整笔记.md)
> **分篇笔记**：见 [README.md](README.md)

## 目录

1. [第一篇　概念与分类（绪论）](#cram-01)　<span style="color:gray">（《信号分析与处理》01_20260915.pptx，96 页）</span>
2. [第二篇　典型信号与基本运算（2.1）](#cram-02)　<span style="color:gray">（《信号分析与处理》2.1节-20260920.pptx，121 页）</span>
3. [第三篇　傅里叶分析（2.2）](#cram-03)　<span style="color:gray">（《信号分析与处理》2.2节-20260920.pptx，144 页）</span>

---

<a id="cram-01"></a>

# 第一篇　概念与分类（绪论）

> 对应课件：《信号分析与处理》01_20260915.pptx，96 页

> 来源：《信号分析与处理》01_20260915.pptx（96 页）的浓缩版；完整版见 笔记/01-信号分析与处理概述/

## 一、核心名词

| 名词 | 一句话定义 | 关键词 |
|---|---|---|
| 信号 | 消息的表现形式，是随一些参数变化的某种物理量或物理现象 | 内容的形式 |
| 消息 | 信号的具体内容，可以是语言、文字、图像或数据 | 形式里的内容 |
| 信息 | 消息中赋予人们的新知识、新概念，即消息中有意义的内容 | 内容里的意义 |
| 信号分析 | 研究信号基本性能（表示、频谱、运算），研究时域波形与频域频谱，提取特征、揭示规律 | 认知信号 |
| 信号传输 | 发送端消息→信号→接收端信号→消息，即通信 | 传递消息 |
| 信号处理 | 对信号加工或变换（变换、滤波、增强、压缩、识别），剔除冗余与干扰、保留有用信息 | 优化信号 |

- 信号与消息（信息）是**内容与形式**的关系：信号是表现形式，消息（信息）是具体内容。
- 分析与处理前后衔接：先看清特征，处理才有依据。
- 数学描述：信号 = 具有一个或多个变量的函数。语音 $f(t)$（一维连续）、图像 $f(x,y)$（二维连续）、指数序列 $f[n]$（一维离散，$n$ 为整数）。
- 表示法三种：公式法、图形法、表格法。

## 二、信号的四组分类

| 维度 | 两类 | 判别依据 |
|---|---|---|
| 确定性 | 确定 / 随机 | 指定时刻 $t$ 能否确定函数值 $x(t)$ |
| 自变量 | 连续 $x(t)$ / 离散 $x[n]$ | 自变量取值是否连续（幅值是否离散另分模拟/数字） |
| 周期性 | 周期 / 非周期 | 是否存在 $T>0$ 使 $x(t+T)=x(t)$；离散为 $N$ 为正整数使 $x[n+N]=x[n]$ |
| 能量功率 | 能量 / 功率 | $E<\infty$（则 $P=0$）为能量信号；$P<\infty$（则 $E=\infty$）为功率信号 |

### 2.1 确定与随机

| 项目 | 确定信号 | 随机信号（不确定信号） |
|---|---|---|
| 定义 | 指定时刻 $t$ 可确定函数值 $x(t)$（若干不连续点除外） | 不是时间的确定函数，具有未可知的不确定性 |
| 描述 | 确定的时间函数或确定的数列 | 统计特性：均值、方差、概率分布 |

平稳高斯：统计特性（均值、方差）不随时间变化，幅值严格服从正态分布（对称钟形，极端值概率低）。
非平稳非高斯：统计特性随时间演变，幅值分布呈尖峰、重尾或不对称，极端值更易出现。

### 2.2 连续与离散（含模拟/数字）

| 类型 | 时间（自变量） | 幅值 | 记号 |
|---|---|---|---|
| 连续时间信号 | 连续 | —— | $x(t)$ |
| 模拟信号 | 连续 | 连续 | —— |
| 离散时间信号 | 离散 | 仍连续 | $x[n]$，$n$ 为整数 |
| 数字信号 | 离散 | 离散 | —— |

链路：模拟信号 →**抽样**（时间离散）→ 离散时间信号 →**量化**（幅值离散）→ 数字信号。

### 2.3 周期与非周期

| 项目 | 连续时间 | 离散时间 |
|---|---|---|
| 定义 | 存在正数 $T$ 使 $x(t)=x(t+T)$ | 存在正整数 $N$ 使 $x[n]=x[n+N]$ |
| 基本周期 | 满足条件的最小正 $T$ | 满足条件的最小正 $N$ |
| 条件 | $T$ 为任意正实数 | $N$ 必须是正整数 |

非周期信号：不满足上述周期定义。

### 2.4 能量与功率

| 项目 | 能量信号 | 功率信号 |
|---|---|---|
| 总能量 $E$ | 有限（$E<\infty$） | 无穷（$E=\infty$） |
| 平均功率 $P$ | 零（$P=0$） | 有限（$P<\infty$） |
| 数学表示 | $E=\int_{-\infty}^{\infty}\lvert f(t)\rvert^{2}\,dt$ | $P=\lim_{T\to\infty}\frac{1}{2T}\int_{-T}^{T}\lvert f(t)\rvert^{2}\,dt$ |
| 特征 | 能量集中在有限时间范围 | 持续时间无限、能量不断累积，单位时间功率恒定 |

判定：先算 $E$；$E<\infty$ 则 $P=0$（能量信号），否则 $P<\infty$ 为功率信号（$E=\infty$）。两类互斥。

## 三、系统的五组分类

系统：对输入信号加工、变换并产生输出的装置；描述分**输入输出描述**与**状态变量描述**。

| # | 分类 | 两类 | 判别方法 |
|---|---|---|---|
| 1 | 线性 | 线性 / 非线性 | 是否**同时**满足齐次特性与叠加特性；线性只改变频率成分幅度，非线性产生谐波与互调 |
| 2 | 时不变 | 非时变 / 时变 | **零状态条件**下，输入延迟 $\tau$、输出是否同步延迟 $\tau$；判断时不涉及初始状态 |
| 3 | 因果 | 因果 / 非因果 | 某时刻输出是否只由当前和过去时刻的输入决定，是否依赖未来输入 |
| 4 | 稳定 | 稳定 / 非稳定 | 是否满足 BIBO：有界输入 → 有界输出，不发散 |
| 5 | 连续/离散 | 连续时间系统 / 离散时间系统 | 输入输出均为连续时间信号即连续时间系统；均为离散时间信号即离散时间系统 |

**本课程聚焦：线性、时不变、因果、稳定的连续时间系统与离散时间系统。**

## 四、必背公式

| 公式 | 表达式 | 适用条件 |
|---|---|---|
| 连续周期条件 | $x(t)=x(t+T)$ | $T$ 为正数；最小正 $T$ 为基本周期 |
| 离散周期条件 | $x[n]=x[n+N]$ | $N$ 为正整数；最小正 $N$ 为基本周期 |
| 信号能量 | $E=\int_{-\infty}^{\infty}\lvert f(t)\rvert^{2}\,dt$ | 信号视为电压/电流，$1\,\Omega$ 电阻上的总能量；非负实数 |
| 平均功率 | $P=\lim_{T\to\infty}\frac{1}{2T}\int_{-T}^{T}\lvert f(t)\rvert^{2}\,dt$ | $1\,\Omega$ 电阻上的平均功率；非负实数 |
| 齐次特性 | $x(t)\to y(t)\Longrightarrow a\,x(t)\to a\,y(t)$ | $a$ 为任意常数；线性的必要条件之一 |
| 叠加特性 | $x_1(t)\to y_1(t)$、$x_2(t)\to y_2(t)\Longrightarrow x_1(t)+x_2(t)\to y_1(t)+y_2(t)$ | 与齐次特性同时满足才是线性系统 |
| 连续系统模型 | **微分方程**，描述输入 $x(t)$ 与输出 $y(t)$ 的关系 | 连续时间系统；依元件特性约束与网络拓扑约束（KCL、KVL）列写；课件未给其通式 |
| 离散系统差分方程 | $\sum_{k=0}^{N}a_k\,y[n-k]=\sum_{m=0}^{M}b_m\,x[n-m]$ | $N$ 阶常系数线性差分方程；阶数 = 变量最高与最低序号之差 |

微分方程可用差分方程逼近：前者解为精确解，后者为近似解，分析方法类似。

## 五、数字类考点

| 考点 | 数字 / 结论 |
|---|---|
| 学时 / 学分 | 80 学时，5 学分 |
| 教学周 / 每周课时 | 第 3–18 周，每周 5 课时 |
| 成绩构成 | 作业 20% + 实验报告 10% + 课堂表现 10% + 期中 20% + 期末 40% |
| 过程性考核 | 作业 + 实验 + 课堂表现合计 40%，期末只占 40% |
| 考试形式 | 期中、期末统一闭卷 |
| 课程目标指标点 | 1.4、2.3、4.1、4.2 |
| 课程主线 | 信号 → 系统 → 处理系统，每步都有模拟/数字两条路线 |
| 本课程聚焦 | 线性、时不变、因果、稳定的连续时间系统与离散时间系统 |

## 六、易错点

- 抽样 ≠ 量化：抽样只离散**时间**（幅值仍连续），量化才离散**幅值**（得数字信号）。
- 连续/离散看**自变量**，模拟/数字看**时间与幅值是否都连续**：数字信号一定离散，离散时间信号不一定数字。
- 基本周期：连续取最小正 $T$（任意正实数），离散取最小正整数 $N$。
- 能量信号与功率信号**互斥**：$E<\infty$ 则 $P=0$，$P<\infty$ 则 $E=\infty$，不存在两者都有限。
- 平稳 ≠ 高斯：平稳说统计特性不随时间变，高斯说幅值的概率分布形状，两者独立。
- 线性 ≠ 时不变：线性看齐次性与叠加性，时不变看特性是否随时间改变，两者独立。
- 判断时不变性**不涉及初始状态**，必须在零状态下比较"输入延迟 $\tau$，输出是否延迟 $\tau$"。
- 因果看的是**未来输入**，不是未来的输出；非因果系统不能实时实现，但可用于理论分析与离线后处理。
- 稳定性是 **BIBO**（有界输入 → 有界输出），不要与因果性混淆。
- 分析与处理前后衔接而非并列：先看清特征，处理才有依据。
- **DFT** 与 **FFT** 不是一回事：FFT 是 DFT 的快速算法。

---

<a id="cram-02"></a>

# 第二篇　典型信号与基本运算（2.1）

> 对应课件：《信号分析与处理》2.1节-20260920.pptx，121 页

> 来源：《信号分析与处理》2.1节-20260920.pptx（121 页）的浓缩版；完整版见 笔记/02-1-连续时间信号分析/

**10 分钟路线**：2.1.1 典型信号 → 2.1.2 运算（几何变换、微积分、相加相乘、卷积）→ 2.1.3 分解与矢量空间。

**分类**：按光滑性分**普通信号**（连续光滑）/ **奇异信号**（本身或各阶导数有跳变点）；按能量功率分**能量信号**（$0<E<\infty$、$P=0$）/ **功率信号**（$E=\infty$、$0<P<\infty$），二者互斥。

---

## 一、典型连续时间信号一览表

| 信号 | 定义式 | 一句话特征 |
|---|---|---|
| 直流 | $x(t)=A,\ -\infty<t<\infty$ | 不随时间变化；$\sigma=0$ 的实指数 |
| 正弦 | $x(t)=A\sin(\Omega t+\varphi)$ | $A$ 振幅、$\Omega$ 角频率、$\varphi$ 初相；$T_0=\frac{2\pi}{\Omega}=\frac{1}{f_0}$，$\Omega=2\pi f_0$ |
| 实指数 | $x(t)=Ae^{\sigma t}$ | $\sigma>0$ 增长、$\sigma<0$ 衰减、$\sigma=0$ 直流；微分积分后仍为指数形式 |
| 单边指数 | $f(t)=e^{-t/\tau}u(t)$ | $\tau>0$ 时间常数（量纲为时间），定衰减快慢；求卷积常用 |
| 双边指数 | $f(t)=e^{-\lvert t\rvert/\tau}$ | 左右对称衰减 |
| 虚指数 | $x(t)=Ae^{j\Omega t}=A[\cos\Omega t+j\sin\Omega t]$ | 周期信号，基本周期 $T_0=\frac{2\pi}{\lvert\Omega\rvert}$ |
| 复指数 | $x(t)=Ae^{st},\ s=\sigma+j\Omega$ | $=Ae^{\sigma t}\cos\Omega t+jAe^{\sigma t}\sin\Omega t$；$e^{\sigma t}$ 定包络、$\Omega$ 定振荡快慢 |
| $\mathrm{Sa}$ | $\mathrm{Sa}(t)=\frac{\sin t}{t}$ | 偶函数；$\mathrm{Sa}(0)=1$；零点 $t=\pm n\pi$；面积 $\int_{-\infty}^{\infty}\mathrm{Sa}(t)dt=\pi$（半轴各 $\pi/2$）；两端趋于 0 |
| $\mathrm{sinc}$ | $\mathrm{sinc}(t)=\frac{\sin\pi t}{\pi t}$ | $\mathrm{Sa}(t)=\mathrm{sinc}(t/\pi)$；零点 $t=\pm n\ (n\ne0)$ |

**$e^{st}$ 三种情形**：$\Omega=0$ 实指数（$\sigma$ 定增减）；$\sigma=0,\Omega\ne0$ 虚指数（等幅振荡）；$\sigma\ne0,\Omega\ne0$ 复指数（$\sigma$ 定包络、$\Omega$ 定振荡；$\sigma<0$ 衰减振荡、$\sigma>0$ 增幅振荡）。$\Omega\ne0$ 时等间隔过零点。

**欧拉公式**：$\cos\Omega t=\frac{1}{2}(e^{j\Omega t}+e^{-j\Omega t})$，$\sin\Omega t=\frac{1}{2j}(e^{j\Omega t}-e^{-j\Omega t})$。

---

## 二、奇异信号表

奇异信号：函数本身或其各阶导数存在不连续点（跳变点），用于模拟瞬时通断、短时冲击、定时采样。

| 名称 | 定义 | 关键性质 |
|---|---|---|
| 单位斜变 $r(t)$ | $r(t)=\begin{cases}0,&t<0\\ t,&t\ge0\end{cases}$ | $\frac{dr}{dt}=u(t)$，$r(t)=\int_{-\infty}^{t}u(\tau)d\tau$ |
| 单位阶跃 $u(t)$ | $u(t)=\begin{cases}1,&t>0\\ 0,&t<0\end{cases}$，跳变点函数值未定义 | $\frac{du}{dt}=\delta(t)$，$u(t)=\int_{-\infty}^{t}\delta(\tau)d\tau$（延迟同理换 $t-t_0$） |
| 单位冲激 $\delta(t)$ | ① $\delta(t)=0\,(t\ne0)$，$\int_{-\infty}^{+\infty}\delta(t)dt=1$；② $\delta(t)=\lim\limits_{\tau\to0}\frac{1}{\tau}[u(t+\frac{\tau}{2})-u(t-\frac{\tau}{2})]$ | 宽 0、面积（强度）1、高度无界；强度 $=\int_{-\infty}^{+\infty}k\delta(t)dt=k$ |
| 周期冲激序列 | $\delta_T(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT_0)$ | 理想采样器的数学模型 |

**$u(t)$ 的 4 个用途**

| 用途 | 写法 |
|---|---|
| 表示开关 | $t=t_0$ 接通 ↔ 接入 $u(t-t_0)$ |
| 表示矩形脉冲/门函数 | $x(t)=u(t-T)-u(t-2T)$；门函数 $G_\tau(t)=u(t+\frac{\tau}{2})-u(t-\frac{\tau}{2})$ |
| 表示符号函数 | $\operatorname{sgn}(t)$：$t>0$ 为 1、$t<0$ 为 $-1$、$t=0$ 为 0，由阶跃组合表示 |
| 表示时间范围（单边性） | 乘 $u(t-t_0)$ 即从 $t_0$ 起截取；$x(t)u(t-t_0)$ 只改接入时刻，$x(t-t_0)u(t-t_0)$ 接入与相位同时延迟 |

**$\delta(t)$ 三条性质与使用条件**

| 性质 | 公式 | 条件 / 说明 |
|---|---|---|
| 筛选特性 | $\int_{-\infty}^{+\infty}x(t)\delta(t-t_0)dt=x(t_0)$；$x(t)\delta(t)=x(0)\delta(t)$ | 积分区间**不含** $t=t_0$ 时结果必为零 |
| 展缩特性 | $\delta(at)=\frac{1}{\lvert a\rvert}\delta(t)$；$\delta(at\pm b)=\frac{1}{\lvert a\rvert}\delta(t\pm\frac{b}{a})$（$a\ne0$） | 复合自变量必须**先展缩、再筛选** |
| 偶函数（推论） | $\delta(-t)=\delta(t)$（取 $a=-1$） | — |

**微积分链（必背）**：$r(t)\xrightarrow{\ d/dt\ }u(t)\xrightarrow{\ d/dt\ }\delta(t)\xrightarrow{\ d/dt\ }\delta'(t)$；反向即积分——$u=\frac{dr}{dt}$，$\delta=\frac{du}{dt}=\frac{d^2r}{dt^2}$，$r=\int u\,dt$，$u=\int\delta\,dt$。

---

## 三、基本运算速记

| 变换 | 表达式 | 图形规则 | 记忆要点 |
|---|---|---|---|
| 平移（时移） | $x(t)\to x(t\mp t_0)$ | $x(t-t_0)$ 右移（延迟）；$x(t+t_0)$ 左移（提前） | 括号内 $-$ 右移、$+$ 左移 |
| 反褶（翻转） | $x(t)\to x(-t)$ | 以纵轴为中心 180° 翻转 | 只要有 $-t$ 就一定有翻转 |
| 尺度变换 | $x(t)\to x(at),\ a>0$ | $a>1$ 压缩；$0<a<1$ 扩展 | 只改持续时间与变化快慢，**普通信号幅值不变** |
| 综合变换 | $f(at\pm b)=f[a(t\pm\frac{b}{a})]$ | **先展缩、后平移** | 平移量是 $\frac{b}{a}$，不是 $b$ |
| 含反褶 | $f(-at\pm b)=f[-a(t\mp\frac{b}{a})]$ | **先展缩 → 再反褶 → 后平移** | 一切变换都是相对 $t$ 而言 |

**端点函数值不变法**（一句话）：变换前后函数值不变，令新旧括号内自变量相等，解出关键点（起点、峰值、零点、终点）的新横坐标后重新描点连线；形状不变，关键点顺序由递增变递减即发生过反褶。

**尺度变换与幅度**：时间轴压缩/拉伸后，为保持总面积（能量）不变，高度变 $\frac{1}{\lvert a\rvert}$ 倍——**冲激强度随之改变**（$\delta(3t-3)=\frac{1}{3}\delta(t-1)$），**普通信号幅值不变**。

| 微积分运算 | 定义 | 效果 |
|---|---|---|
| 微分 | $y(t)=\frac{dx(t)}{dt}$ | 突出变化部分；间断点导数用冲激表示，**强度 = 跳跃值** |
| 积分 | $y(t)=\int_{-\infty}^{t}x(\tau)d\tau=x^{(-1)}(t)$ | 变上限积分；使变化部分平滑（求面积） |

**相加与相乘**：$x=x_1+\cdots+x_n$、$x=x_1x_2$，必须在**对应时刻**逐点运算（时间轴对齐）；乘积非零区间 = 两信号非零区间之**交集**。

---

## 四、卷积速记

$$r(t)=e(t)*h(t)=\int_{-\infty}^{\infty}e(\tau)h(t-\tau)d\tau\qquad(\text{课件也写 } e(t)\otimes h(t))$$

$\tau$ 是积分变量、$t$ 是参变量；$h(t)$ 表示 LTI 系统特性时，卷积即为输入 $e(t)$ 经过该系统的输出响应 $r(t)$。

**四组性质**

| 组 | 公式 | 备注 |
|---|---|---|
| 代数性质 | 交换 $x_1*x_2=x_2*x_1$；分配 $x_1*[x_2+x_3]=x_1*x_2+x_1*x_3$；结合 $[x*h_1]*h_2=x*[h_1*h_2]$ | 交换 = 级联次序可换；分配 = **并联**；结合 = **串联**（等效 $h_1*h_2$） |
| 时移性质 | $x_1(t-t_1)*x_2(t)=x(t-t_1)$；$x_1(t-t_1)*x_2(t-t_2)=x(t-t_1-t_2)$ | 延时器可整体移到卷积之外 |
| 与 $\delta/\delta'/u$ 卷积 | $x*\delta(t)=x(t)$；$x*\delta(t-t_0)=x(t-t_0)$；$x*\delta'(t)=x'(t)$；$x*\delta^{(k)}(t-t_0)=x^{(k)}(t-t_0)$；$x*u(t)=\int_{-\infty}^{t}x(\lambda)d\lambda$ | $\delta(t)$ 理想导线；$\delta'(t)$ 微分器；$u(t)$ 积分器 |
| 微积分性质 | 设 $g(t)=x(t)*h(t)$：$g'=x'*h=x*h'$；$g^{(n)}=x*h^{(n)}=x^{(n)}*h$；$g^{(n-m)}=x^{(n)}*h^{(-m)}$ | 微分算子可搬到任一因子；简单因子求导、复杂因子积分 |

**使用条件**：被微分的信号必须**有起始点**，即 $\int_{-\infty}^{t}\frac{df(\tau)}{d\tau}d\tau=f(t)$（"微分—积分"可逆，微积分次数才能抵消）。

**解析式法步骤提纲**：① 代定义式，写出 $e(\tau)h(t-\tau)$；② 由各阶跃/门函数的非零条件列关于 $\tau$ 的不等式组，与 $t$ 联立定出积分限；③ 对参变量 $t$ 分段积分；④ 汇总成分段表达式。积分限是关键。

**图解法步骤提纲**：① 变量替换 $f_1(t)\to f_1(\tau)$、$f_2(t)\to f_2(\tau)$；② 反褶 $f_2(\tau)\to f_2(-\tau)$；③ 时移 $f_2(-\tau)\to f_2(t-\tau)$；④ 相乘积分 $\int f_1(\tau)f_2(t-\tau)d\tau$。物理含义是重叠面积随 $t$ 变化；两矩形卷积得三角形/梯形，分段点即两波形端点相遇的时刻。

**结果区间**：非零区间 $[t_1,t_2]$、$[t_3,t_4]$ ⇒ 卷积非零区间 $t_1+t_3\le t\le t_2+t_4$；**卷积时宽 = 两信号时宽之和**（可验算分段区间）。

---

## 五、信号的分解

| 分解 | 分解式 | 分量表达式 | 关键性质 |
|---|---|---|---|
| 直流/交流 | $x(t)=x_{DC}(t)+x_{AC}(t)$ | $x_{DC}(t)=\frac{1}{T}\int_{t_0}^{t_0+T}x(t)dt$ | 直流分量即平均值；$\frac{1}{T}\int_{t_0}^{t_0+T}x_{AC}(t)dt=0$ |
| 偶/奇 | $x(t)=x_e(t)+x_o(t)$ | $x_e(t)=\frac{x(t)+x(-t)}{2}$；$x_o(t)=\frac{x(t)-x(-t)}{2}$ | $x_e$ 偶、$x_o$ 奇；分解**唯一**，原信号为偶时 $x_o=0$ |
| 实部/虚部 | $x(t)=x_R(t)+jx_I(t)$ | $x_R(t)=\frac{x(t)+x^*(t)}{2}$；$x_I(t)=\frac{x(t)-x^*(t)}{2j}$ | $x^*(t)=x_R(t)-jx_I(t)$；极坐标 $x=A(t)e^{j\theta(t)}$，$A=\sqrt{x_R^2+x_I^2}$，$\theta=\arg[x(t)]$ |

**功率关系**：$P=\frac{1}{T}\int_{t_0}^{t_0+T}x^2(t)dt=x_{DC}^2+\frac{1}{T}\int_{t_0}^{t_0+T}x_{AC}^2(t)dt$，即 $P=P_{DC}+P_{AC}$——交叉项积分为零，直流分量与零均值交流分量正交。

**正交函数分量**：$\langle x_m,x_n\rangle=\int_{t_1}^{t_2}x_m(t)x_n^*(t)dt$；$\langle x_m,x_n\rangle=0\ (m\ne n)$ 即**正交**。$x(t)=\sum_{n=1}^{N}c_nx_n(t)$ 时 $c_n=\frac{\langle x,x_n\rangle}{\langle x_n,x_n\rangle}$（沿第 $n$ 个正交函数的投影）；$\langle x_n,x_n\rangle=1$ 称**单位正交函数**。正交性由"函数对 + 区间"共同决定。

**信号矢量空间**：信号可视为矢量（连续无限维、离散有限维）；矢量空间 = 对加法与数乘封闭的信号集合。内积 $\langle x,y\rangle=\int x(t)y^*(t)dt$（离散 $\sum x[n]y^*[n]$）衡量相似性；范数 $\lVert x\rVert=\sqrt{\langle x,x\rangle}$ 衡量能量/长度；相关系数 $\rho=\frac{\lvert\langle x_1,x_2\rangle\rvert}{\lVert x_1\rVert\lVert x_2\rVert}$，$\rho=0$ 正交、$\rho$ 接近 1 方向接近。正交基 = 一组正交信号的完备基（如傅里叶级数中的复指数信号）。

**最佳逼近**：$\hat{x}_N(t)=\sum_{n=1}^{N}c_nx_n(t)$，误差 $e(t)=x(t)-\hat{x}_N(t)$；当 $\langle e,x_n\rangle=0\ (n=1,2,\cdots,N)$ 时为**最小均方误差**逼近——几何上即向子空间作垂线，垂足为最佳近似。

---

## 六、易错点（一行一条）

- 卷积是**积分**不是相乘：$x_1(t)x_2(t)\ne x_1(t)*x_2(t)$。
- 冲激只有**强度（面积）**有意义，"高度"无意义。
- 展缩别漏 $\frac{1}{\lvert a\rvert}$：$\delta(3t-3)=\frac{1}{3}\delta(t-1)$。
- $\int x(t)\delta(at+b)dt$ 必须先化 $\frac{1}{\lvert a\rvert}\delta(t+\frac{b}{a})$，再取 $x(-\frac{b}{a})$。
- 筛选区间**不含** $t=t_0$ 时结果必为零——常设陷阱。
- 尺度变换只改横轴：普通信号幅值不变，冲激强度变 $\frac{1}{\lvert a\rvert}$（面积守恒）——最易混。
- 平移量是 $\frac{b}{a}$ 不是 $b$：$f(2t-6)=f[2(t-3)]$ 即压缩 2 倍 + 右移 3。
- 微分丢直流："先微分再积分"只有被微分信号**有起始点**时才可逆。
- 阶跃在跳变点函数值未定义，该点不影响积分值。
- $T_0=\frac{2\pi}{\Omega}$ 分母是**角频率**；用频率则 $T_0=\frac{1}{f_0}$，且 $\Omega=2\pi f_0$。
- 虚指数基本周期用 $\lvert\Omega\rvert$（周期必须为正）。
- $\mathrm{Sa}(t)$ 零点在 $\pm n\pi$，$\mathrm{sinc}(t)$ 零点在 $\pm n$。
- 别把 $x_2(t-\tau)$ 写成 $x_2(t)$：$t$ 参变量、$\tau$ 积分变量。
- 偶、奇分量都要除以 2，$x_o$ 用 $x(t)-x(-t)$（别反号）；虚部分母是 $2j$ 不是 $2$。
- 直流分量是**平均值**不是最小值（周期取一个周期、非周期取定义区间）。
- 说"两个函数正交"必须指明**区间**（正交性依赖区间）。
- 卷积时宽 = 两信号时宽之和（有限时宽信号），可快速验算。

---

<a id="cram-03"></a>

# 第三篇　傅里叶分析（2.2）

> 对应课件：《信号分析与处理》2.2节-20260920.pptx，144 页

> 来源：《信号分析与处理》2.2节-20260920.pptx（144 页）的浓缩版；完整版见 笔记/02-2-连续时间信号的频域分析/

## 1. 三种傅里叶级数形式

周期信号 $x(t)$，周期 $T_0$，$\Omega_0=\frac{2\pi}{T_0}$，且满足**狄利克雷条件**。

| 形式 | 级数式 | 系数 |
|---|---|---|
| 三角形式 | $x(t)=a_0+\sum\limits_{n=1}^{\infty}\left[a_n\cos(n\Omega_0 t)+b_n\sin(n\Omega_0 t)\right]$ | $a_0=\frac{1}{T_0}\int_{t_0}^{t_0+T_0}x(t)\mathrm{d}t$；$a_n=\frac{2}{T_0}\int x(t)\cos(n\Omega_0 t)\mathrm{d}t$；$b_n=\frac{2}{T_0}\int x(t)\sin(n\Omega_0 t)\mathrm{d}t$ |
| 谐波形式（同频率合并） | $x(t)=c_0+\sum\limits_{n=1}^{\infty}c_n\cos(n\Omega_0 t+\varphi_n)$ | $c_0=a_0$；$c_n=\sqrt{a_n^2+b_n^2}\ (c_n\ge 0)$；$\varphi_n=\arctan\!\left(-\frac{b_n}{a_n}\right)$ |
| 指数形式 | $x(t)=\sum\limits_{n=-\infty}^{\infty}F_n\mathrm{e}^{\mathrm{j}n\Omega_0 t}$ | $F_n=\frac{1}{T_0}\int_{t_0}^{t_0+T_0}x(t)\mathrm{e}^{-\mathrm{j}n\Omega_0 t}\mathrm{d}t$ |

**系数关系**（$x(t)$ 为**实函数**）：$F_n=\frac{1}{2}(a_n-\mathrm{j}b_n)$，$F_{-n}=\frac{1}{2}(a_n+\mathrm{j}b_n)$，$|F_n|=|F_{-n}|=\frac{1}{2}c_n$，$\varphi_n=-\varphi_{-n}$。

**狄利克雷条件**（充分条件）：一周期内 ① **绝对可积**；② **间断点有限个**；③ **极值有限个**。

**吉布斯现象**：有限项逼近时，间断点两侧有约 **9%** 的振铃过冲；增加项数只让振荡变窄、位置向间断点收拢，高度不消失；间断点处收敛到跳变极限的**平均值**。

## 2. 周期信号的频谱

- **三条特征**：离散性（谐波性，谱线只在 $n\Omega_0$ 处）、收敛性（$n\uparrow$ 则 $|F(n\Omega_0)|\downarrow$）、唯一性。特例：周期冲激信号 $F_n=\frac{1}{T_0}$ 为常数，**无收敛性、频带无限宽**。
- **单边谱 / 双边谱**：单边谱只画 $\Omega\ge 0$、谱线高 $c_n$；双边谱含负频率、谱线高 $|F_n|=\frac{1}{2}c_n$（同一信号）。
- **周期矩形脉冲序列**（脉宽 $\tau$、周期 $T_0$、高 $E$、偶对称，抽样函数 $\mathrm{Sa}(x)=\frac{\sin x}{x}$）：$F_n=\frac{E\tau}{T_0}\mathrm{Sa}\!\left(\frac{n\Omega_0\tau}{2}\right)$，包络 $\frac{E\tau}{T_0}\mathrm{Sa}\!\left(\frac{\Omega\tau}{2}\right)$；直流 $F_0=E\frac{\tau}{T_0}$；谱线间隔 $\Omega_0=\frac{2\pi}{T_0}$；包络第一零点 $B=\frac{2\pi}{\tau}$。

| 变化 | 频谱响应 |
|---|---|
| $E\uparrow$ | $F_n$ 与 $E$ **成正比** |
| $\tau\downarrow$（$T_0$ 不变） | 谱线位置与间隔**不变**；包络零点 $B=2\pi/\tau$ **变大**、包络展宽 → **时域压缩、频域扩展** |
| $T_0\uparrow$ | 谱线间隔 $\Omega_0$ **变小**、谱线变密；包络不动。$T_0\to\infty$ 时 $\Omega_0\to0$，离散谱线连成**连续谱** |

- **带宽**：信号主要占用的频率范围。零点带宽 $\Omega_B=\frac{2\pi}{\tau}$；$3\ \mathrm{dB}$ 半功率带宽（幅值降到最大值 $0.707$ 倍）；能量有效带宽。**时频制约**：时域越窄、主瓣越宽。

## 3. 傅里叶变换：定义、物理意义、存在条件

$$X(\Omega)=\int_{-\infty}^{\infty}x(t)\mathrm{e}^{-\mathrm{j}\Omega t}\mathrm{d}t=F[x(t)],\qquad x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(\Omega)\mathrm{e}^{\mathrm{j}\Omega t}\mathrm{d}\Omega=F^{-1}[X(\Omega)]$$

记 $x(t)\leftrightarrow X(\Omega)$；$X(\Omega)=|X(\Omega)|\mathrm{e}^{\mathrm{j}\varphi(\Omega)}$，$|X(\Omega)|$、$\varphi(\Omega)$ 分别为幅度谱与相位谱。

- **频谱密度**：$X(\Omega)=\lim\limits_{T_0\to\infty}T_0F(n\Omega_0)$，即**单位频带上的频谱值**。周期信号是离散谱、幅度有限；非周期信号是连续谱、幅度无限小但相对大小有别。
- **物理意义**：$x(t)=\frac{1}{\pi}\int_{0}^{\infty}|X(\Omega)|\cos[\Omega t+\varphi(\Omega)]\,\mathrm{d}\Omega$——**无穷多个振幅为无穷小的连续余弦分量之和**。
- **存在条件**（狄利克雷，**充分条件**）：**绝对可积** $\int_{-\infty}^{\infty}|x(t)|\mathrm{d}t<\infty$；有限区间内极值有限个；不连续点有限个且均为有限值。能量有限信号存在变换；引入 $\delta(\Omega)$ 后 $\delta(t)$、$u(t)$ 等也可变换。

## 4. 典型非周期信号傅里叶变换对表（课件 6 对 + 1 条推论）

| 信号 | 时域 $x(t)$ | 频域 $X(\Omega)$ | 备注（条件 / 记忆点） |
|---|---|---|---|
| 矩形脉冲（门函数） | $E\left[u\!\left(t+\dfrac{\tau}{2}\right)-u\!\left(t-\dfrac{\tau}{2}\right)\right]$ | $E\tau\,\mathrm{Sa}\!\left(\dfrac{\Omega\tau}{2}\right)$ | 宽 $\tau$、高 $E$、实偶 → 频谱为实、相位 $0$ 或 $\pi$；第一零点 $\pm\frac{2\pi}{\tau}$ |
| 单边指数 | $\mathrm{e}^{-\alpha t}u(t)\quad(\alpha>0)$ | $\dfrac{1}{\alpha+\mathrm{j}\Omega}$ | $\lvert X\rvert=\frac{1}{\sqrt{\alpha^2+\Omega^2}}$；$\Omega=0$ 最大 $\frac{1}{\alpha}$，$\Omega=\alpha$ 为 $0.707$ 倍（$-3\ \mathrm{dB}$）；$\varphi=-\arctan\frac{\Omega}{\alpha}$ |
| 双边指数（**推论，课件未单列**） | $\mathrm{e}^{-\alpha\lvert t\rvert}\quad(\alpha>0)$ | $\dfrac{2\alpha}{\alpha^2+\Omega^2}$ | 实偶 → 频谱实偶；**课件未单列此对**，由 slide 63 符号函数页分段积分的两半相加：$\frac{1}{\alpha+\mathrm{j}\Omega}+\frac{1}{\alpha-\mathrm{j}\Omega}$ |
| 直流 | $A$ | $2\pi A\,\delta(\Omega)$ | **不绝对可积**，用宽 $2\tau$、高 1 的矩形脉冲取 $\tau\to\infty$ 极限；与 $\delta(t)\leftrightarrow1$ 对偶 |
| 单位冲激 | $\delta(t)$ | $1$ | 由抽样性质 $\int\delta(t)\mathrm{e}^{-\mathrm{j}\Omega t}\mathrm{d}t=1$；**时域无限窄、频域无限宽** |
| 符号函数 | $\mathrm{sgn}(t)=\begin{cases}+1,&t>0\\ 0,&t=0\\ -1,&t<0\end{cases}$ | $\dfrac{2}{\mathrm{j}\Omega}$ | **不绝对可积**；考点：构造 $\mathrm{sgn}(t)\mathrm{e}^{-\alpha\lvert t\rvert}$ 逼近、再取 $\alpha\to0$；$\lvert X\rvert=\frac{2}{\lvert\Omega\rvert}$，相位 $\Omega>0$ 为 $-\pi/2$、$\Omega<0$ 为 $+\pi/2$ |
| 单位阶跃 | $u(t)=\begin{cases}1,&t>0\\ 0,&t<0\end{cases}$ | $\pi\delta(\Omega)+\dfrac{1}{\mathrm{j}\Omega}$ | **不绝对可积**，用 $u(t)=\frac{1}{2}+\frac{1}{2}\mathrm{sgn}(t)$ 及线性性质；$\pi\delta(\Omega)$ 是直流分量 $\frac{1}{2}$ 的贡献，**不能丢** |

## 5. 傅里叶变换性质总表（12 条）

| # | 性质名 | 时域 | 频域 | 成立条件 / 记忆要点 |
|---|---|---|---|---|
| 1 | 线性 | $\sum\limits_{i=1}^{n}a_ix_i(t)$ | $\sum\limits_{i=1}^{n}a_iX_i(\Omega)$ | $a_i$ 为常数、$n$ 为正整数；有限项叠加无问题，无穷级数需一致收敛 |
| 2 | 对称性 | $X(t)$ | $2\pi x(-\Omega)$ | 条件 $x(t)\leftrightarrow X(\Omega)$；**$2\pi$ 与反褶 $(-\Omega)$ 都不能漏** |
| 3 | 奇偶虚实性（含共轭对称性） | 实信号；偶函数（奇分量为零）／奇函数（偶分量为零） | 偶 → 实偶函数、相位 $0$ 或 $\pi$；奇 → 虚奇函数、相位 $\pm\pi/2$；共轭对称 $X(-\Omega)=X^{*}(\Omega)$ | 条件：$x(t)$ 为**实函数**；口诀"时域偶→频域实、时域奇→频域虚"；幅频偶、相频奇 |
| 4 | 尺度变换 | $x(at)$ | $\frac{1}{\lvert a\rvert}X\!\left(\frac{\Omega}{a}\right)$ | **$a$ 为非零实常数**；除 $\lvert a\rvert$ 而不是 $a$；$a=-1$ 时 $x(-t)\leftrightarrow X(-\Omega)$。含时移：$x[a(t-t_0)]\leftrightarrow\frac{1}{\lvert a\rvert}X\!\left(\frac{\Omega}{a}\right)\mathrm{e}^{-\mathrm{j}\Omega t_0}$ |
| 5 | 时移 | $x(t-t_0)$ | $X(\Omega)\mathrm{e}^{-\mathrm{j}\Omega t_0}$ | **幅度谱不变**，只给相位加线性项 $-\Omega t_0$ |
| 6 | 频移 | $x(t)\mathrm{e}^{\mathrm{j}\Omega_0 t}$ | $X(\Omega-\Omega_0)$ | $\Omega_0$ 为常数，**注意 $\pm$ 号**；调制 $x(t)\cos\Omega_0t\leftrightarrow\frac{1}{2}[X(\Omega-\Omega_0)+X(\Omega+\Omega_0)]$，峰值减半 |
| 7 | 时域微分 | $x^{(n)}(t)$ | $(\mathrm{j}\Omega)^nX(\Omega)$ | 幅度乘 $\lvert\Omega\rvert$、相位加 $\pi/2$，高频增强（高通）；**零点位置不变** |
| 8 | 频域微分 | $t^nx(t)$ | $(\mathrm{j})^n\frac{\mathrm{d}^nX(\Omega)}{\mathrm{d}\Omega^n}$ | 等价写法 $\mathscr{F}[(-\mathrm{j}t)^nx(t)]=\frac{\mathrm{d}^nX(\Omega)}{\mathrm{d}\Omega^n}$；符号别反 |
| 9 | 时域积分 | $\int_{-\infty}^{t}x(\tau)\mathrm{d}\tau$ | $X(\Omega)\left[\frac{1}{\mathrm{j}\Omega}+\pi\delta(\Omega)\right]$；**若 $X(0)=0$** 则为 $\frac{X(\Omega)}{\mathrm{j}\Omega}$ | 条件：$X(0)=\int x(t)\mathrm{d}t=0$（面积为零、无直流分量）才能省 $\pi\delta(\Omega)$；幅度按 $1/\lvert\Omega\rvert$ 衰减、相位减 $\pi/2$（低通）；等价于与 $u(t)$ 卷积 |
| 10 | 频域积分（了解） | $-\frac{x(t)}{\mathrm{j}t}+\pi f(0)\delta(t)$ | $\int_{-\infty}^{\Omega}X(v)\mathrm{d}v$ | 与频域微分对偶 |
| 11 | 时域卷积定理 | $x_1(t)*x_2(t)$ | $X_1(\Omega)\cdot X_2(\Omega)$ | 时域卷积 ↔ 频域**乘积**，**无系数**；卷积的时宽 = 两信号时宽之和 |
| 12 | 频域卷积定理 | $x_1(t)\cdot x_2(t)$ | $\frac{1}{2\pi}X_1(\Omega)*X_2(\Omega)$ | 时域乘积 ↔ 频域卷积，**系数 $\frac{1}{2\pi}$ 只在这一侧**；加窗截断 → 频谱泄漏 |

## 6. 频谱中心点校验

$$X(0)=\int_{-\infty}^{\infty}x(t)\,\mathrm{d}t,\qquad x(0)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(\Omega)\,\mathrm{d}\Omega$$

## 7. 一般周期信号的傅里叶变换

$$\mathrm{F}[x(t)]=2\pi\sum_{n=-\infty}^{\infty}F_n\delta(\Omega-n\Omega_0),\qquad \Omega_0=\frac{2\pi}{T}$$

- 冲激位置 $\Omega=n\Omega_0$（谐波频率处）、强度 $2\pi F_n$；$X(\Omega)$ 是**频谱密度**，只在 $n\Omega_0$ 处有值、幅度 $\infty$（无"有限高度的谱线"）。
- **周期信号 = 单脉冲 * 冲激序列**：$x(t)=x_0(t)*\sum\delta(t-nT)$，由时域卷积定理 $X(\Omega)=X_0(\Omega)\cdot\Omega_0\sum\delta(\Omega-n\Omega_0)$；**包络由 $X_0(\Omega)$ 决定，间隔由 $\Omega_0$ 决定**。
- **系数与单脉冲频谱**：$F_n=\frac{1}{T}F_0(\mathrm{j}n\Omega_0)=\frac{1}{T}F_0(\mathrm{j}\Omega)\big|_{\Omega=n\Omega_0}$；等价形式 $\mathrm{F}[f_T(t)]=\Omega_0\sum F_0(\mathrm{j}n\Omega_0)\delta(\Omega-n\Omega_0)$。
- **四步法**：① **找**第一个周期的单体 $f_0(t)$；② **求**其变换 $F_0(\mathrm{j}\Omega)$；③ **换**$F_n=\frac{1}{T}F_0(\mathrm{j}n\Omega_0)$；④ **写**$\mathrm{F}[f_T(t)]=2\pi\sum F_n\delta(\Omega-n\Omega_0)$。

## 8. 三个典型周期信号的傅里叶变换

$$\cos\Omega_0t\ \leftrightarrow\ \pi\left[\delta(\Omega+\Omega_0)+\delta(\Omega-\Omega_0)\right]$$

$$\sin\Omega_0t\ \leftrightarrow\ -\mathrm{j}\pi\delta(\Omega-\Omega_0)+\mathrm{j}\pi\delta(\Omega+\Omega_0)$$

$$\delta_T(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT_0)\ \leftrightarrow\ \Omega_0\sum_{n=-\infty}^{\infty}\delta(\Omega-n\Omega_0)$$

- $\sin$ 与 $\cos$：**幅度谱相同**（$\pm\Omega_0$ 处强度 $\pi$ 的冲激），**相位谱差 $\pi/2$**。
- $\delta_T(t)$ 的频谱仍是冲激序列，强度与间隔都是 $\Omega_0$（时/频域自相似）。
- 两种谱别混：级数谱高 $F_n=\frac{1}{T_0}$，变换谱冲激强度 $\Omega_0=\frac{2\pi}{T_0}$；都满足离散性、**不满足收敛性**、频带无限宽。

## 9. 易错点（一行一条）

- 时移只改**相位谱**、不改幅度谱；问"时移后幅度谱如何变化"，答案永远是"不变"。
- 尺度变换除 $\lvert a\rvert$ 而不是 $a$；$a<0$ 时上下限互换的负号与 $\frac{1}{a}$ 的负号相消。
- 对称性差一个 $2\pi$，而且要反褶（$x(-\Omega)$），两个都不能漏。
- 周期信号的频谱是**冲激串**（频谱密度），不是连续谱；"高度"是冲激强度 $2\pi F_n$。
- 系数：$a_n,b_n$ 前是 $\frac{2}{T_0}$；$a_0$、$F_n$ 前是 $\frac{1}{T_0}$；$\mathrm{F}[f_T(t)]$ 前是 $2\pi$；$F_n=\frac{1}{T}F_0$ 的因子是 $\frac{1}{T}$。
- 时域积分的 $\pi\delta(\Omega)$ 只在 $X(0)=0$ 时可省；面积不为零时丢掉就是错。
- 卷积定理两侧不对称：时域卷积对频域乘积**无系数**，时域乘积对频域卷积乘 $\frac{1}{2\pi}$。
- $\mathrm{Sa}(x)=\frac{\sin x}{x}$ 第一零点在 $x=\pi$，故矩形脉冲频谱第一零点在 $\pm\frac{2\pi}{\tau}$（不是 $\pm\frac{\pi}{\tau}$）。
- $u(t)$ 的频谱**必须带** $\pi\delta(\Omega)$；$\mathrm{sgn}(t)$ 是 $\frac{2}{\mathrm{j}\Omega}$ 而非 $\frac{2}{\Omega}$，相位奇对称。
- 频移符号：$\mathrm{e}^{\mathrm{j}\Omega_0t}\to X(\Omega-\Omega_0)$，$\mathrm{e}^{-\mathrm{j}\Omega_0t}\to X(\Omega+\Omega_0)$。

---
