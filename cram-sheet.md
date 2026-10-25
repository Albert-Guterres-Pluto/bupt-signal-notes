# 《信号分析与处理》抱佛脚速记

考前突击用：**只有概念、公式、性质和条件**，没有例题、没有练习、没有图片。
按「考前 1 小时」的用法组织——三篇按顺序扫一遍，重点看标了 ⚠️ 的条件和易错点。

> **完整版**（含例题、推导、课件截图）：[信号分析与处理-完整笔记.md](信号分析与处理-完整笔记.md)
> **分篇笔记**：见 [README.md](README.md)

## 目录

1. [第一篇　概念与分类（绪论）](#cram-01)　<span style="color:gray">（《信号分析与处理》01_20260915.pptx，96 页）</span>
2. [第二篇　典型信号与基本运算（2.1）](#cram-02)　<span style="color:gray">（《信号分析与处理》2.1节-20260920.pptx，121 页）</span>
3. [第三篇　傅里叶分析（2.2）](#cram-03)　<span style="color:gray">（《信号分析与处理》2.2节-20261007.pptx，152 页）</span>
4. [第四篇　复频域分析（2.3）](#cram-04)　<span style="color:gray">（《信号分析与处理》2.3节20261008.pptx，87 页）</span>
5. [第五篇　连续系统分析与滤波器（第3、4章）](#cram-05)　<span style="color:gray">（《信号分析与处理》第3章-20261020.pptx（145 页）+ 第4章-20261020.pptx（101 页））</span>

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

> 对应课件：《信号分析与处理》2.2节-20261007.pptx，152 页

> 来源：《信号分析与处理》2.2节-20261007.pptx（152 页）的浓缩版；完整版见 笔记/02-3-连续时间信号的频域分析/

**15 分钟路线**：傅里叶级数（三种形式）→ 周期信号频谱（三条特征 + 矩形脉冲谱）→ 傅里叶变换（定义、频谱密度、存在条件）→ 典型变换对表 → 性质总表（12 条）→ 一般周期信号的变换与四步法 → 易错点。

**一句话主线**：任何信号都能拆成复指数（或正弦）分量之和——周期信号用**级数**（离散谱线、高度有限），非周期信号用**变换**（连续谱、幅度无穷小，靠**频谱密度**区分相对大小）；周期信号也能做变换，其谱密度是一串**冲激**。

> **术语**：本版把旧版的「对称性」改称 **「对偶性」**，公式不变。下文一律用新名，括号内附旧称便于对照旧讲义。

---

## 一、傅里叶级数：三种形式与系数关系

周期信号 $x(t)$，周期 $T_0$（2.2.4 节课件改用 $T$），基波角频率 $\Omega_0=\dfrac{2\pi}{T_0}$，且满足**狄利克雷条件**。基信号 $\{\mathrm{e}^{\mathrm{j}n\Omega_0 t}\}$、$\{\cos n\Omega_0 t,\ \sin n\Omega_0 t\}$ 在一个周期内构成**完备正交集**，系数由正交投影逐项求出。

| 形式 | 级数式 | 系数 |
|---|---|---|
| 三角函数形式 | $x(t)=a_0+\sum\limits_{n=1}^{\infty}\left[a_n\cos(n\Omega_0 t)+b_n\sin(n\Omega_0 t)\right]$ | $a_0=\dfrac{1}{T_0}\displaystyle\int_{T_0}x(t)\mathrm{d}t$；$a_n=\dfrac{2}{T_0}\displaystyle\int_{T_0}x(t)\cos(n\Omega_0 t)\mathrm{d}t$；$b_n=\dfrac{2}{T_0}\displaystyle\int_{T_0}x(t)\sin(n\Omega_0 t)\mathrm{d}t$ |
| 谐波（余弦）形式 | $x(t)=c_0+\sum\limits_{n=1}^{\infty}c_n\cos(n\Omega_0 t+\varphi_n)$ | $c_0=a_0$；$c_n=\sqrt{a_n^2+b_n^2}\ (c_n\ge 0)$；$\varphi_n=\arctan\!\left(-\dfrac{b_n}{a_n}\right)$ |
| 指数形式 | $x(t)=\sum\limits_{n=-\infty}^{\infty}F_n\mathrm{e}^{\mathrm{j}n\Omega_0 t}$ | $F_n=\dfrac{1}{T_0}\displaystyle\int_{T_0}x(t)\mathrm{e}^{-\mathrm{j}n\Omega_0 t}\mathrm{d}t$ |

**物理含义**：$n=0$（$c_0=a_0=F_0$）为**直流**（一周期平均值）；$n=1$ 为**基波**；$n$ 为 **$n$ 次谐波**。同频合并时必须统一成**余弦**才能读出幅度与初相（遇 $-\cos\alpha$ 先把负号转成相位 $\pm\pi$）。

**三种形式的系数关系**（$x(t)$ 为**实函数**时）：

$$F_n=\frac{1}{2}(a_n-\mathrm{j}b_n),\qquad F_{-n}=\frac{1}{2}(a_n+\mathrm{j}b_n),\qquad |F_n|=|F_{-n}|=\frac{1}{2}c_n,\qquad \varphi_n=-\varphi_{-n}$$

指数形式的谱系数 $F_n$ 反映各次谐波幅度、相位随频率的分布，$x(t)$ 与 $F_n$ **一一对应**；$F_n$ 为实函数时一张图即可表频谱，为虚函数时须分幅度谱、相位谱两张图。**引入负频率的理由**：实信号展开成虚指数必须成**共轭对**，虚部相互抵消才能保证结果为实函数。虚指数是傅里叶分析的理想基：**对时间微分、积分后仍是同频虚指数**（只差因子 $\mathrm{j}\Omega$），故微分方程在频域化为代数方程。

**狄利克雷条件**（级数存在的**充分条件**）：一周期内 ① **绝对可积** $\displaystyle\int_{T_0}|x(t)|\mathrm{d}t<\infty$；② **间断点有限个**；③ **极值有限个**。

**吉布斯现象**：有限项逼近时，间断点两侧始终存在**振铃状过冲**，峰值约为跳变值的 **9%**；增加项数只使振荡变窄、位置向间断点收拢，**高度不消失**；间断点处级数收敛到跳变前后极限值的**平均值**。工程启示：削弱高次谐波会使方波、脉冲的边沿变圆滑。

---

## 二、周期信号的频谱

### 1. 三条特征（周期信号频谱的"身份证"）

| 特征 | 含义 |
|---|---|
| **离散性**（谐波性） | 谱线只出现在 $\Omega=n\Omega_0$ 处，间隔为基频 $\Omega_0$ |
| **收敛性** | $n\uparrow$ 时 $\lvert F_n\rvert\downarrow$（各次谐波幅度随次数衰减） |
| **唯一性** | $x(t)$ 的谱线唯一，时域与频域一一对应 |

⚠️ 三条特征是**对一般周期信号**而言，不能无条件套用：周期冲激序列 $\delta_T(t)$ 的 $F_n=\dfrac{1}{T_0}$ 为常数，**有离散性、有谐波性，但无收敛性，频带无限宽**。

**单边谱与双边谱**：同一条谱的两种画法。单边谱只画 $\Omega\ge0$、谱线高度 $c_n$；双边谱画到负频率、谱线高度 $|F_n|=\dfrac{1}{2}c_n$（幅度谱形状相同、差一个 2 倍系数），相位谱**奇对称** $\varphi_{-n}=-\varphi_n$。负频率不是"负的频率"，而是共轭对的另一半。

### 2. 周期矩形脉冲序列（样板信号）

脉宽 $\tau$、周期 $T_0$、脉冲高度 $E$、关于原点偶对称（占空比 $\tau/T_0$，$\mathrm{Sa}(x)=\dfrac{\sin x}{x}$）：

$$F_n=\frac{E\tau}{T_0}\,\mathrm{Sa}\!\left(\frac{n\Omega_0\tau}{2}\right),\qquad F_0=E\frac{\tau}{T_0},\qquad \text{包络}=\frac{E\tau}{T_0}\,\mathrm{Sa}\!\left(\frac{\Omega\tau}{2}\right)$$

- 谱线间隔 $\Omega_0=\dfrac{2\pi}{T_0}$；包络**第一零点** $B=\dfrac{2\pi}{\tau}$（零点用**连续变量** $\Omega$ 求，因为零点一般不与谱线位置 $n\Omega_0$ 重合）。
- $x(t)$ 为偶函数 $\Rightarrow b_n=0$、$F_n$ 为实函数，故**一张图**（$F_n$ 本身）即可表频谱；若分成幅度谱与相位谱两图，则相位只在 $0$ 与 $\pi$ 之间跳变。

| 参数变化 | 频谱响应 |
|---|---|
| $E\uparrow$ | $F_n$ 与 $E$ **成正比**（整体按比例放大） |
| $\tau\downarrow$（$T_0$ 不变） | 谱线位置与间隔**不变**；包络零点 $B=2\pi/\tau$ **变大**、包络展宽 → **时域压缩、频域扩展** |
| $T_0\uparrow$ | 谱线间隔 $\Omega_0$ **变小**、谱线变密；包络不动。$T_0\to\infty$ 时 $\Omega_0\to0$，离散谱线连成**连续谱** |

### 3. 频带宽度（带宽）

**带宽**＝信号主要占用的频率范围，是频域分析的核心指标，由**幅度频谱**决定。

| 定义 | 含义 |
|---|---|
| 零点带宽 | 幅度谱**第一个过零点**，矩形信号 $\Omega_B=\dfrac{2\pi}{\tau}$ |
| $3\ \mathrm{dB}$ 半功率带宽 | 幅值降至最大值 $0.707$ 倍的频率范围 |
| 能量有效带宽 | 含信号总能量一定占比的频率区间 |

**时频制约**：时域波形越窄，频谱主瓣越宽；时域越宽，主瓣越窄（等效脉冲宽度与等效带宽成反比）。工程含义：通信速率提高 → 码元持续时间缩短 → 占用频带更宽，这是高速传输与有限带宽矛盾的根源。

---

## 三、傅里叶变换：定义、频谱密度、物理意义、存在条件

### 1. 变换对与频谱密度

$$X(\Omega)=\int_{-\infty}^{\infty}x(t)\mathrm{e}^{-\mathrm{j}\Omega t}\,\mathrm{d}t=F[x(t)],\qquad x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(\Omega)\mathrm{e}^{\mathrm{j}\Omega t}\,\mathrm{d}\Omega=F^{-1}[X(\Omega)]$$

记 $x(t)\leftrightarrow X(\Omega)$：$x(t)$ 为**原函数**，$X(\Omega)$ 为**傅里叶变换函数**（一般复值）。写成 $X(\Omega)=|X(\Omega)|\mathrm{e}^{\mathrm{j}\varphi(\Omega)}$，则 $|X(\Omega)|\sim\Omega$ 为**幅度频谱**、$\varphi(\Omega)\sim\Omega$ 为**相位频谱**。$\Omega$ 体系下系数 $\dfrac{1}{2\pi}$ **只在反变换一侧**；用频率 $f$ 体系时正反变换对称、无 $2\pi$，两套不要混用。

**频谱密度**：由 $F(n\Omega_0)=\dfrac{1}{T_0}\displaystyle\int_{-T_0/2}^{T_0/2}x(t)\mathrm{e}^{-\mathrm{j}n\Omega_0 t}\mathrm{d}t$ 出发，$T_0\to\infty$ 时 $F(n\Omega_0)\to0$，但比值

$$X(\Omega)=\lim_{T_0\to\infty}T_0F(n\Omega_0)=\lim_{T_0\to\infty}\frac{F(n\Omega_0)}{f}$$

趋于有界函数，即**单位频带上的频谱值**，简称频谱（也记 $F(\Omega)$、$F(\mathrm{j}\Omega)$）。对照：周期信号为**离散谱**、谱线幅度有限；非周期信号为**连续谱**、各分量幅度无穷小，但**相对大小仍有区别**——这正是必须引入频谱密度的原因。

### 2. 物理意义

把 $X(\Omega)$ 写成模与相位代入反变换，利用 $\sin[\cdot]$ 对 $\Omega$ 为奇函数（积分为零）与 $|X|$ 偶、$\varphi$ 奇：

$$x(t)=\frac{1}{\pi}\int_{0}^{\infty}|X(\Omega)|\cos\left[\Omega t+\varphi(\Omega)\right]\mathrm{d}\Omega$$

即实信号是**无穷多个振幅为无穷小**（$\dfrac{1}{\pi}|X(\Omega)|\mathrm{d}\Omega$）的**带初始相位的余弦波**连续叠加；从复数角度也可看作无穷多个无穷小幅度的**连续指数信号**在 $-\infty<\Omega<\infty$ 上叠加。

### 3. 存在条件（狄利克雷，充分条件）

① **绝对可积** $\displaystyle\int_{-\infty}^{\infty}|x(t)|\mathrm{d}t<\infty$；② 任意有限区间内**极值有限个**；③ 任意有限区间内**间断点有限个**且每个间断点都是**有限值**。

⚠️ 这是**充分条件而非必要条件**：$\delta(t)$、$u(t)$、$\mathrm{sgn}(t)$ 都不满足绝对可积，但引入 $\delta(\Omega)$ 后仍有傅里叶变换。**能量有限信号**的变换一定存在。

### 4. 频谱中心点（最快的自检式）

$$X(0)=\int_{-\infty}^{\infty}x(t)\,\mathrm{d}t,\qquad x(0)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(\Omega)\,\mathrm{d}\Omega$$

即"信号面积＝零频谱值"、"频谱面积＝$2\pi x(0)$"。算完频谱先代 $\Omega=0$ 验一遍归一化系数。

---

## 四、典型非周期信号的傅里叶变换对表

| 信号 | 时域 $x(t)$ | 频域 $X(\Omega)$ | 条件 / 记忆点 |
|---|---|---|---|
| 矩形脉冲（门函数） | $E\left[u\!\left(t+\dfrac{\tau}{2}\right)-u\!\left(t-\dfrac{\tau}{2}\right)\right]$ | $E\tau\,\mathrm{Sa}\!\left(\dfrac{\Omega\tau}{2}\right)$ | 宽 $\tau$、高 $E$、实偶 → 频谱实、相位 $0$ 或 $\pi$；主瓣 $\left(-\dfrac{2\pi}{\tau},\dfrac{2\pi}{\tau}\right)$，第一零点 $\pm\dfrac{2\pi}{\tau}$，$X(0)=E\tau$ |
| 单边指数 | $E\mathrm{e}^{-\alpha t}u(t)\quad(\alpha>0)$ | $\dfrac{E}{\alpha+\mathrm{j}\Omega}$ | $\lvert X\rvert=\dfrac{E}{\sqrt{\alpha^2+\Omega^2}}$；$\Omega=0$ 取峰值 $\dfrac{E}{\alpha}$；$\Omega=\alpha$ 处为峰值 $0.707$ 倍（$-3\ \mathrm{dB}$）；$\varphi=-\arctan\dfrac{\Omega}{\alpha}$ |
| 双边指数（**推论，课件未单列**） | $\mathrm{e}^{-\alpha\lvert t\rvert}\quad(\alpha>0)$ | $\dfrac{2\alpha}{\alpha^2+\Omega^2}$ | 实偶 → 频谱实偶；由 $t<0$ 的 $\mathrm{e}^{\alpha t}$ 与 $t>0$ 的 $\mathrm{e}^{-\alpha t}$ 两半相加：$\dfrac{1}{\alpha-\mathrm{j}\Omega}+\dfrac{1}{\alpha+\mathrm{j}\Omega}$ |
| 直流 | $A$ | $2\pi A\,\delta(\Omega)$ | **不绝对可积**；把直流看成宽 $2\tau$、高 1 的矩形脉冲取 $\tau\to\infty$ 的极限；与 $\delta(t)\leftrightarrow1$ 构成时频对偶 |
| 单位冲激 | $\delta(t)$ | $1$ | 由抽样性质 $\displaystyle\int\delta(t)\mathrm{e}^{-\mathrm{j}\Omega t}\mathrm{d}t=1$；**时域无限窄、频域无限宽** |
| 符号函数 | $\mathrm{sgn}(t)=\begin{cases}+1,&t>0\\ 0,&t=0\\ -1,&t<0\end{cases}$ | $\dfrac{2}{\mathrm{j}\Omega}$ | **不绝对可积**；构造 $\mathrm{sgn}(t)\mathrm{e}^{-\alpha\lvert t\rvert}$ 分段积分后取 $\alpha\to0$；$\lvert X\rvert=\dfrac{2}{\lvert\Omega\rvert}$，相位 $\Omega>0$ 为 $-\dfrac{\pi}{2}$、$\Omega<0$ 为 $+\dfrac{\pi}{2}$；$\Omega=0$ 处无定义 |
| 单位阶跃 | $u(t)=\begin{cases}1,&t>0\\ 0,&t<0\end{cases}$ | $\pi\delta(\Omega)+\dfrac{1}{\mathrm{j}\Omega}$ | **不绝对可积**；$u(t)=\dfrac{1}{2}+\dfrac{1}{2}\mathrm{sgn}(t)$，用线性性质由直流与符号函数的变换对相加；$\pi\delta(\Omega)$ 是直流分量 $\dfrac{1}{2}$ 的贡献，**不能丢** |

**两条速记规律**：① **时域越窄、频域越宽**（$\delta(t)\leftrightarrow1$ 是极端情形）；② 不满足绝对可积的信号只有两类办法——**取极限**（直流）或**拆成已知信号之和**（$u(t)$）；$\mathrm{sgn}(t)$ 属于后者，先乘衰减因子使其绝对可积、再取极限。

**由对偶性导出的两对**（课件以性质应用的形式给出，未列入上表）：

$$\mathrm{Sa}(\Omega_c t)\ \leftrightarrow\ \frac{\pi}{\Omega_c}\ \ (|\Omega|<\Omega_c,\ \text{否则}\ 0);\qquad \frac{1}{t}\ \leftrightarrow\ -\mathrm{j}\pi\,\mathrm{sgn}(\Omega)$$

---

## 五、傅里叶变换性质总表（12 条）

约定 $\mathscr{F}[x(t)]=X(\Omega)$；正变换取 $\mathrm{e}^{-\mathrm{j}\Omega t}$。下表"条件"一栏即考试判分点。

| # | 性质 | 时域 | 频域 | 成立条件 / 记忆要点 |
|---|---|---|---|---|
| 1 | 线性 | $\sum\limits_{i=1}^{n}a_ix_i(t)$ | $\sum\limits_{i=1}^{n}a_iX_i(\Omega)$ | $a_i$ 为常数、$n$ 为正整数；**有限项**叠加无附加条件，无穷级数需一致收敛 |
| 2 | **对偶性**（旧称对称性） | $X(t)$ | $2\pi x(-\Omega)$ | 条件 $x(t)\leftrightarrow X(\Omega)$；**$2\pi$ 与反褶 $(-\Omega)$ 都不能漏**；先确认 $x(\cdot)$ 的奇偶性再代入 |
| 3 | 奇偶虚实性（实信号） | 实偶函数（奇分量为零）／实奇函数（偶分量为零） | 偶 → 实偶谱、相位 $0$ 或 $\pi$；奇 → 虚奇谱、相位 $\pm\dfrac{\pi}{2}$；共轭对称 $X(-\Omega)=X^{*}(\Omega)$ | 条件：$x(t)$ 为**实函数**；口诀"时域偶→频域实，时域奇→频域虚"；幅频偶、相频奇 |
| 4 | 尺度变换 | $x(at)$ | $\dfrac{1}{\lvert a\rvert}X\!\left(\dfrac{\Omega}{a}\right)$ | **$a$ 为非零实常数**；除 $\lvert a\rvert$ 不是 $a$；$a=-1$ 得 $x(-t)\leftrightarrow X(-\Omega)$ |
| 5 | 时移 | $x(t-t_0)$ | $X(\Omega)\mathrm{e}^{-\mathrm{j}\Omega t_0}$ | $t_0$ 为实常数；**幅度谱不变**，只把相位加线性项 $-\Omega t_0$ |
| 6 | 频移 | $x(t)\mathrm{e}^{\mathrm{j}\Omega_0 t}$ | $X(\Omega-\Omega_0)$ | $\Omega_0$ 为实常数，**注意 $\pm$ 号**（$\mathrm{e}^{-\mathrm{j}\Omega_0 t}\to X(\Omega+\Omega_0)$）；调制定理：$x(t)\cos\Omega_0t\leftrightarrow\dfrac{1}{2}[X(\Omega-\Omega_0)+X(\Omega+\Omega_0)]$，峰值减半 |
| 7 | 时域微分 | $x^{(n)}(t)$ | $(\mathrm{j}\Omega)^nX(\Omega)$ | 条件：变换存在且可导足够阶（不绝对可积时按广义函数理解）；幅度乘 $\lvert\Omega\rvert^n$、相位加 $n\dfrac{\pi}{2}$，**高通、增强高频**，零点位置不变 |
| 8 | 频域微分 | $t^nx(t)$ | $(\mathrm{j})^n\dfrac{\mathrm{d}^nX(\Omega)}{\mathrm{d}\Omega^n}$，等价写法 $\mathscr{F}[(-\mathrm{j}t)^nx(t)]=\dfrac{\mathrm{d}^nX(\Omega)}{\mathrm{d}\Omega^n}$ | 条件：$X(\Omega)$ 对 $\Omega$ $n$ 阶可导；符号别反（由 $\mathrm{e}^{-\mathrm{j}\Omega t}$ 对 $\Omega$ 求导得 $-\mathrm{j}t$） |
| 9 | 时域积分 | $\displaystyle\int_{-\infty}^{t}x(\tau)\mathrm{d}\tau$ | $X(\Omega)\left[\dfrac{1}{\mathrm{j}\Omega}+\pi\delta(\Omega)\right]$；**若 $X(0)=0$** 则为 $\dfrac{X(\Omega)}{\mathrm{j}\Omega}$ | 判据：$X(0)=\displaystyle\int x(t)\mathrm{d}t=0$（信号面积为零、无直流）才能省 $\pi\delta(\Omega)$；幅度按 $\dfrac{1}{\lvert\Omega\rvert}$ 衰减、相位减 $\dfrac{\pi}{2}$，**低通**；等价于与 $u(t)$ 卷积 |
| 10 | 频域积分（了解） | $-\dfrac{x(t)}{\mathrm{j}t}+\pi x(0)\delta(t)$ | $\displaystyle\int_{-\infty}^{\Omega}X(v)\mathrm{d}v$ | 与频域微分对偶；仅要求会写、会用 |
| 11 | 时域卷积定理 | $x_1(t)*x_2(t)$ | $X_1(\Omega)\cdot X_2(\Omega)$ | 两变换都存在；时域卷积 ↔ 频域**乘积，无系数**；卷积的时宽 = 两信号时宽之和 |
| 12 | 频域卷积定理 | $x_1(t)\cdot x_2(t)$ | $\dfrac{1}{2\pi}X_1(\Omega)*X_2(\Omega)$ | 两变换都存在；**系数 $\dfrac{1}{2\pi}$ 只在这一侧**；加窗截断 → 频谱泄漏 |

**三条组合/补充式**（由表中性质合成，判分同样看条件）：

$$\text{时移＋尺度：}\ \mathscr{F}\left[x(at+b)\right]=\frac{1}{\lvert a\rvert}X\!\left(\frac{\Omega}{a}\right)\mathrm{e}^{\mathrm{j}\Omega\frac{b}{a}};\qquad \text{等价式：}\ x\!\left[a(t-t_0)\right]\leftrightarrow\frac{1}{\lvert a\rvert}X\!\left(\frac{\Omega}{a}\right)\mathrm{e}^{-\mathrm{j}\Omega t_0}$$

$$\text{复信号共轭：}\ \mathscr{F}\left[x^{*}(t)\right]=X^{*}(-\Omega);\qquad \text{实信号特例：}\ X(-\Omega)=X^{*}(\Omega)$$

**三条性质的分工（背这一句）**：改**谱的形状**靠**尺度** $a$；只改**相位**靠**时移** $t_0$；只改**谱的位置**靠**频移** $\Omega_0$。两条卷积定理互为对偶：**时域卷积 ⇔ 频域乘积**（无系数）、**时域乘积 ⇔ 频域卷积**（有 $\dfrac{1}{2\pi}$）——工程上"时域卷一次"与"频域乘一下"是同一件事，**设计滤波器本质上就是设计 $H(\mathrm{j}\Omega)$ 的形状**；而频谱分析必然加窗，选窗是在**分辨率（主瓣宽度）与泄漏（旁瓣电平）**之间折中（矩形窗主瓣窄、旁瓣大；汉宁窗旁瓣小）。

---

## 六、一般周期信号的傅里叶变换

### 1. 变换公式与频谱结构

周期为 $T$ 的信号展开成指数级数后逐项求变换（$F_n$ 与 $t$ 无关），并用 $1\leftrightarrow2\pi\delta(\Omega)$、$\mathrm{e}^{\mathrm{j}n\Omega_0 t}\leftrightarrow2\pi\delta(\Omega-n\Omega_0)$：

$$X(\Omega)=\mathrm{F}\left[x(t)\right]=2\pi\sum_{n=-\infty}^{\infty}F_n\,\delta(\Omega-n\Omega_0),\qquad \Omega_0=\frac{2\pi}{T}$$

- **冲激位置**：$\Omega=n\Omega_0$（谐波频率处）；**冲激强度**：$2\pi F_n$，与 $F_n$ 成正比，由傅里叶系数决定。
- $X(\Omega)$ 是**频谱密度**：周期信号的谱**只在 $\Omega=n\Omega_0$ 处有值**（每处频带宽度为零、冲激幅度为 $\infty$）——不存在"有限高度的谱线"。**离散谱**，只含基频 $\Omega_0$ 的整数倍分量。

### 2. 周期信号 = 单脉冲 * 冲激序列

$$x(t)=x_0(t)*\delta_T(t)=x_0(t)*\sum_{n=-\infty}^{\infty}\delta(t-nT)\quad\Rightarrow\quad X(\Omega)=X_0(\Omega)\cdot\Omega_0\sum_{n=-\infty}^{\infty}\delta(\Omega-n\Omega_0)$$

其中用到冲激的搬移（筛选）性质 $x(t)*\delta(t-t_0)=x(t-t_0)$。**读图要点：整体包络由单脉冲频谱 $X_0(\Omega)$ 决定，谱线间隔由 $\Omega_0$ 决定。**

### 3. $F_n$ 与单脉冲频谱 $F_0(\mathrm{j}\Omega)$ 的关系

比较 $X(\Omega)=2\pi\sum F_n\delta(\Omega-n\Omega_0)$ 与 $X(\Omega)=\Omega_0\sum F_0(\mathrm{j}n\Omega_0)\delta(\Omega-n\Omega_0)$（$2\pi F_n=\Omega_0F_0(\mathrm{j}n\Omega_0)$，$\Omega_0=\dfrac{2\pi}{T}$）：

$$\boxed{\ F_n=\frac{1}{T}F_0(\mathrm{j}n\Omega_0)=\frac{1}{T}F_0(\mathrm{j}\Omega)\Big|_{\Omega=n\Omega_0}\ }\qquad \text{等价：}\ \mathrm{F}[f_T(t)]=\Omega_0\sum_{n=-\infty}^{\infty}F_0(\mathrm{j}n\Omega_0)\delta(\Omega-n\Omega_0)$$

**记法**：周期信号的傅里叶系数 $F_n$ = 单脉冲频谱密度在 $n\Omega_0$ 处的**抽样值 × $\dfrac{1}{T}$**；而 $\mathrm{F}[f_T(t)]$ 外面乘的是 $2\pi$。两个系数（$\dfrac{1}{T}$ 与 $2\pi$）最易写错。

### 4. 四步法（求周期信号的傅里叶变换）

1. **找**：取出周期信号在第一个周期内的**单脉冲** $f_0(t)$（截出一个周期的波形）；
2. **求**：算它的傅里叶变换 $F_0(\mathrm{j}\Omega)$；
3. **换**：$F_n=\dfrac{1}{T}F_0(\mathrm{j}n\Omega_0)=\dfrac{1}{T}F_0(\mathrm{j}\Omega)\big|_{\Omega=n\Omega_0}$；
4. **写**：$\mathrm{F}\left[f_T(t)\right]=2\pi\sum\limits_{n=-\infty}^{\infty}F_n\delta(\Omega-n\Omega_0)$，$\Omega_0=\dfrac{2\pi}{T}$。

> 单脉冲 $x_0(t)$ 的取法影响 $F_0(\mathrm{j}\Omega)$ 的表达式（不同时移带来相位因子），但 $F_n$ 的结果唯一——只要 $x_0(t)$ 恰好是 $f_T(t)$ 在一个周期内的波形即可。

### 5. 三个典型周期信号的变换对

| 信号 | 傅里叶变换 | 说明 |
|---|---|---|
| $\cos\Omega_0t$ | $\pi\left[\delta(\Omega+\Omega_0)+\delta(\Omega-\Omega_0)\right]$ | 由欧拉公式 + 频移性质；$\pm\Omega_0$ 处强度 $\pi$ 的冲激 |
| $\sin\Omega_0t$ | $-\mathrm{j}\pi\delta(\Omega-\Omega_0)+\mathrm{j}\pi\delta(\Omega+\Omega_0)$ | 幅度谱与 $\cos$ **相同**，相位谱**差 $\dfrac{\pi}{2}$**：$\Omega>0$ 为 $-\dfrac{\pi}{2}$、$\Omega<0$ 为 $+\dfrac{\pi}{2}$；$\cos$ 相位为 $0$（或 $\pi$） |
| $\delta_T(t)=\sum\limits_{n=-\infty}^{\infty}\delta(t-nT_0)$ | $\Omega_0\sum\limits_{n=-\infty}^{\infty}\delta(\Omega-n\Omega_0)$ | 频谱仍是冲激序列，强度与间隔都是 $\Omega_0$（时频自相似，是对偶性的典型应用） |

**两种谱不能混**（以 $\delta_T(t)$ 为例）：

| 项目 | 傅里叶级数频谱 | 傅里叶变换频谱 |
|---|---|---|
| 谱线形状 | 冲激序列 | 冲激序列 |
| 高度／强度 | $F_n=\dfrac{1}{T_0}$ | $\Omega_0=\dfrac{2\pi}{T_0}$ |
| 满足的性质 | 离散性、谐波性；**不满足收敛性**、频带无限宽 | 同左 |

时域间隔 $T_0$ 与频域间隔 $\Omega_0=\dfrac{2\pi}{T_0}$ **成反比**。另外，由"单脉冲 * 冲激序列"可见：**脉冲个数增加 → 频谱振荡；成为周期序列 → 频谱离散化**。

---

## 七、易错点（一行一条）

- 系数易混：$a_n,b_n$ 前是 $\dfrac{2}{T_0}$；$a_0$ 与 $F_n$ 前是 $\dfrac{1}{T_0}$；$\mathrm{F}[f_T(t)]$ 前是 $2\pi$；$F_n=\dfrac{1}{T}F_0(\mathrm{j}n\Omega_0)$ 的因子是 $\dfrac{1}{T}$（不是 $2\pi$、也不是 $\dfrac{1}{2\pi}$）。
- 谐波形式必须统一为**余弦**再读相位；遇 $-\cos(\cdot)$ 先把负号转成相位 $\pm\pi$。
- $F_n=\dfrac{1}{2}(a_n-\mathrm{j}b_n)$ 的负号位置易反，与 $F_{-n}=\dfrac{1}{2}(a_n+\mathrm{j}b_n)$ 成对记。
- 双边谱的谱线高度是单边谱的**一半**（$|F_n|=c_n/2$），别照抄单边谱高度；相位谱奇对称。
- 吉布斯过冲约 **9%** 是"截断"造成的，**不是"项数不够多"**；增加项数只让振荡变窄。
- "频谱"与"频谱密度"不同：$F_n$ 是谱线幅度（有限值），$X(\Omega)$ 是单位频带上的值；$T_0\to\infty$ 时谱线幅度趋于零，但不能说"频谱为零"。
- 反变换前的 $\dfrac{1}{2\pi}$ 只在**反变换**一侧（$\Omega$ 体系）；换到 $f$ 体系则对称、无 $2\pi$，两套不能混用。
- 狄利克雷条件是**充分条件**不是必要条件：$\delta(t)$、$u(t)$、$\mathrm{sgn}(t)$ 都不绝对可积，但引入 $\delta(\Omega)$ 后仍有变换。
- **对偶性**（旧称对称性）差一个 $2\pi$，还要**反褶** $x(-\Omega)$，两个都不能漏；默写按新版写"对偶性"。
- 尺度变换除 $\lvert a\rvert$ 而不是 $a$；$a<0$ 时"上下限互换"的负号与 $\dfrac{1}{a}$ 的负号恰好抵消。平移量是 $\dfrac{b}{a}$ 不是 $b$：$x(2t-5)=x\left[2\left(t-\dfrac{5}{2}\right)\right]$。
- 时移只改**相位谱**、不改幅度谱；问"时移后幅度谱如何变化"，答案永远是"不变"。
- 频移符号：$\mathrm{e}^{\mathrm{j}\Omega_0t}\to X(\Omega-\Omega_0)$，$\mathrm{e}^{-\mathrm{j}\Omega_0t}\to X(\Omega+\Omega_0)$；调制定理的 $\dfrac{1}{2}$ 不能丢（峰值减半）。
- 时域积分的 $\pi\delta(\Omega)$ **只在 $X(0)=0$**（面积为零、无直流）时可省；面积不为零时丢掉就是错。
- 卷积定理两侧不对称：时域卷积对频域乘积**无系数**，时域乘积对频域卷积乘 $\dfrac{1}{2\pi}$。
- 时域微分是**高通**（幅度按 $\lvert\Omega\rvert$ 加权、相位 $+\dfrac{\pi}{2}$），时域积分是**低通**（幅度按 $\dfrac{1}{\lvert\Omega\rvert}$、相位 $-\dfrac{\pi}{2}$）；两者互为逆操作。
- $\mathrm{Sa}(x)=\dfrac{\sin x}{x}$ 第一零点在 $x=\pi$，故矩形脉冲频谱第一零点在 $\pm\dfrac{2\pi}{\tau}$（**不是** $\pm\dfrac{\pi}{\tau}$）；包络零点 $B=\dfrac{2\pi}{\tau}$ 与谱线间隔 $\Omega_0$ 是两条独立规律，别混。
- 幅度谱恒非负；实谱变号（如 $\mathrm{Sa}$ 变负）时，负号全部体现为相位谱在 $0$ 与 $\pi$ 之间跳变，不要把负值画进幅度谱。
- $u(t)$ 的频谱**必须带** $\pi\delta(\Omega)$；$\mathrm{sgn}(t)$ 是 $\dfrac{2}{\mathrm{j}\Omega}$（不是 $\dfrac{2}{\Omega}$），相位奇对称、$\Omega=0$ 处频谱无定义。
- 周期信号的谱是**冲激串**（频谱密度），"高度"是冲激强度 $2\pi F_n$，不是有限幅度；$\delta_T(t)$ 是**唯一没有收敛性**的典型周期信号。
- 比较 $\cos$ 与 $\sin$：**幅度谱相同、相位谱相差 $\dfrac{\pi}{2}$**；答"差别在哪"要答相位。

---

<a id="cram-04"></a>

# 第四篇　复频域分析（2.3）

> 对应课件：《信号分析与处理》2.3节20261008.pptx，87 页

> 来源：《信号分析与处理》2.3节20261008.pptx（87 页）的浓缩版；完整版见 笔记/02-2-连续时间信号的复频域分析/

## 0. 符号约定

| 符号 | 含义 |
|---|---|
| $s=\sigma+\mathrm{j}\Omega$ | **复频率**：$\sigma$ 为实部（待定实常数），$\Omega$ 为虚部角频率 |
| $\mathscr{L}\{\cdot\}$、$\mathscr{L}^{-1}\{\cdot\}$ | 双边拉氏正变换、逆变换算子 |
| $\mathscr{L}_+\{\cdot\}$ | 单边拉氏变换（积分下限 $0^{-}$） |
| $x(t)\leftrightarrow X(s)$ | 拉氏变换对的简写 |
| ROC（$R_x,R_1,R_2$） | 收敛域：$X(s)$ 存在的 $s$ 的取值范围 |
| $\gamma$ | 逆变换积分路径的实横坐标，必须取在 ROC 内 |
| $p_i$、$z_j$ | 极点（图上画 ×）、零点（图上画 ○） |

## 1. 定义与收敛域 ROC

**由来**：傅氏变换要求绝对可积，阶跃、增长指数等不满足；乘衰减因子 $\mathrm{e}^{-\sigma t}$ 把信号"压住"后再作傅氏变换，就得到拉氏变换，实频率由此推广为**复频率** $s=\sigma+\mathrm{j}\Omega$。

| 名称 | 定义式 | 说明 |
|---|---|---|
| 双边正变换 | $X(s)=\mathscr{L}\{x(t)\}=\displaystyle\int_{-\infty}^{\infty}x(t)\mathrm{e}^{-st}\,\mathrm{d}t$ | 记 $x(t)\leftrightarrow X(s)$，$s\in$ ROC |
| 双边逆变换 | $x(t)=\mathscr{L}^{-1}\{X(s)\}=\dfrac{1}{2\pi\mathrm{j}}\displaystyle\int_{\gamma-\mathrm{j}\infty}^{\gamma+\mathrm{j}\infty}X(s)\mathrm{e}^{st}\,\mathrm{d}s$ | 积分路径是 ROC 内的一条竖直线 $\mathrm{Re}\{s\}=\gamma$；路径不在 ROC 内则逆变换不收敛 |
| 单边变换 | $X(s)=\mathscr{L}_+\{x(t)\}=\displaystyle\int_{0^{-}}^{\infty}x(t)\mathrm{e}^{-st}\,\mathrm{d}t$ | 下限取 $0^{-}$：把 $t=0$ 处的冲激及其各阶导数包含进来，初始值一律写 $x(0^{-})$ |
| 存在条件 | $\displaystyle\int_{-\infty}^{\infty}\lvert x(t)\mathrm{e}^{-\sigma t}\rvert\,\mathrm{d}t<\infty$ | 即 $x(t)\mathrm{e}^{-\sigma t}$ **绝对可积** |
| ROC 定义 | 使 $x(t)\mathrm{e}^{-\sigma t}$ **绝对可积**（即上式成立）的 $\sigma$ 所对应的全体 $s$ | 可积性只取决于 $\mathrm{Re}\{s\}=\sigma$、与虚部 $\Omega$ 无关；ROC **不含边界** |
| 有理函数 | $X(s)=\dfrac{b_m\prod_{j=1}^{m}(s-z_j)}{\prod_{i=1}^{n}(s-p_i)}$ | 分子根 $z_j$ 为零点，分母根 $p_i$ 为极点；极点位置决定 ROC 边界与时域形态 |

⚠️ 双边变换**必须成对写出 $X(s)$ 与 ROC**——只写 $X(s)$ 定不了 $x(t)$。

## 2. ROC 的基本特性与形状

**基本特性**：

- ROC 内**不含任何极点**；ROC 的边界由极点所在的竖直线决定。
- ROC 是 $s$ 平面中**平行于虚轴**的区域：右半平面、左半平面或竖直带（两端都开）。

| 信号类型 | 非零区间（定义） | ROC 形状 |
|---|---|---|
| 右边信号 | $t<T_1$ 时 $x(t)=0$ | 某条竖直线的**右侧**：$\mathrm{Re}\{s\}>\sigma_0$ |
| 左边信号 | $t>T_2$ 时 $x(t)=0$ | 某条竖直线的**左侧**：$\mathrm{Re}\{s\}<\sigma_0$ |
| 双边信号 | 两侧都有非零部分 | 两条竖直线**之间**的竖直带：$\sigma_1<\mathrm{Re}\{s\}<\sigma_2$ |
| 时限信号 | 只在 $[T_1,T_2]$ 内非零 | 若绝对可积，可扩展为**整个 $s$ 平面** |

**同一像函数、不同 ROC → 不同 $x(t)$**：

| $X(s)$ | ROC | 对应 $x(t)$ |
|---|---|---|
| $\dfrac{1}{s-\alpha}$ | $\mathrm{Re}\{s\}>\alpha$（右边） | $\mathrm{e}^{\alpha t}u(t)$ |
| $\dfrac{1}{s-\alpha}$ | $\mathrm{Re}\{s\}<\alpha$（左边） | $-\mathrm{e}^{\alpha t}u(-t)$ |
| $\dfrac{1}{s-\alpha}-\dfrac{1}{s-\beta}$（$\alpha<\beta$） | $\alpha<\mathrm{Re}\{s\}<\beta$（双边） | $\mathrm{e}^{\alpha t}u(t)+\mathrm{e}^{\beta t}u(-t)$ |

⚠️ 两段 ROC 边界重合（$\alpha\ge\beta$）时条带消失，说明该信号的双边拉氏变换不存在。

## 3. 拉氏变换性质总表（含成立条件）

### 3.1 双边变换的性质

| # | 性质 | 时域 | $s$ 域 | 成立条件 / ROC |
|---|---|---|---|---|
| 1 | 线性 | $a x_1(t)+b x_2(t)$ | $aX_1(s)+bX_2(s)$ | $a,b$ 为任意常数；ROC $\supseteq R_1\cap R_2$（零极点相消时可能扩大） |
| 2 | 共轭 | $x^{*}(t)$ | $X^{*}(s^{*})$ | ROC $=R_x$ |
| 3 | 尺度变换 | $x(at)$ | $\dfrac{1}{\lvert a\rvert}X\!\left(\dfrac{s}{a}\right)$ | $a$ 为**非零实常数**；ROC $=aR_x$（$a<0$ 时随反褶左右翻转） |
| 4 | 时移 | $x(t-t_0)$ | $\mathrm{e}^{-st_0}X(s)$ | $t_0$ 为实常数；ROC $=R_x$（只乘相位因子，不改变收敛性） |
| 5 | 复频域平移（频移） | $\mathrm{e}^{s_0t}x(t)$ | $X(s-s_0)$ | $s_0$ 为复常数；ROC $=R_x+\mathrm{Re}\{s_0\}$（只随实部平移，与虚部无关） |
| 6 | 时域卷积 | $x_1(t)*x_2(t)$ | $X_1(s)X_2(s)$ | ROC $\supseteq R_1\cap R_2$，要求两 ROC 有公共部分 |
| 7 | 时域微分 | $\dfrac{\mathrm{d}x(t)}{\mathrm{d}t}$ | $sX(s)$ | 双边形式**不含初始值项**；ROC $\supseteq R_x$，可能扩大（乘 $s$ 消去原点极点） |
| 8 | 时域积分 | $\displaystyle\int_{-\infty}^{t}x(v)\,\mathrm{d}v$ | $\dfrac{X(s)}{s}$ | ROC $\supseteq R_x\cap\{\mathrm{Re}\{s\}>0\}$；下限为 $-\infty$ |
| 9 | 复频域微分 | $-t\,x(t)$ | $\dfrac{\mathrm{d}X(s)}{\mathrm{d}s}$ | 要求 $X(s)$ 可导；ROC $=R_x$ |

### 3.2 单边变换的常用性质（下限 $0^{-}$）

| 性质 | 时域 | $s$ 域 | 条件 |
|---|---|---|---|
| 时移 | $x(t-t_0)u(t-t_0)$ | $\mathrm{e}^{-st_0}X(s)$ | $t_0>0$，且要求 $t<0$ 时 $x(t)=0$（因果信号）；否则须补 $t<0$ 段的修正项 |
| 一阶微分 | $\dfrac{\mathrm{d}x(t)}{\mathrm{d}t}$ | $sX(s)-x(0^{-})$ | 初始值一律取 $x(0^{-})$ |
| 二阶微分 | $\dfrac{\mathrm{d}^2x(t)}{\mathrm{d}t^2}$ | $s^2X(s)-s\,x(0^{-})-x'(0^{-})$ | 同上 |
| $n$ 阶微分 | $\dfrac{\mathrm{d}^nx(t)}{\mathrm{d}t^n}$ | $s^nX(s)-\displaystyle\sum_{r=0}^{n-1}s^{n-r-1}x^{(r)}(0^{-})$ | 同上 |
| 积分 | $\displaystyle\int_{0^{-}}^{t}x(v)\,\mathrm{d}v$ | $\dfrac{X(s)}{s}$ | 下限 $0^{-}$，无初始值附加项 |

### 3.3 初值定理与终值定理

| 定理 | 结论 | 成立条件 |
|---|---|---|
| 初值定理 | $x(0^{+})=\lim\limits_{s\to\infty}sX(s)$ | $t<0$ 时 $x(t)=0$；且 $t=0$ 处**不含冲激或高阶奇异函数**，即 $sX(s)$ 的极限存在（$X(s)$ 非真分式时先长除、只对真分式部分用）；结果是 $x(0^{+})$ 而非 $x(0^{-})$ |
| 终值定理 | $x(\infty)=\lim\limits_{t\to\infty}x(t)=\lim\limits_{s\to0}sX(s)$ | $t<0$ 时 $x(t)=0$；$sX(s)$ **全部极点位于左半平面**（等价于 $X(s)$ 的极点除 $s=0$ 至多一个单重极点外全在左半平面） |

⚠️ 做题顺序：**先查极点条件，再用初值/终值定理**；条件不满足时代出来的是假值。

## 4. 常用信号拉氏变换对表

表中全是**因果信号**（$t<0$ 时为 $0$），故单边与双边结果相同。

| # | $x(t)$ | $X(s)$ | ROC |
|---|---|---|---|
| 1 | $\delta(t)$ | $1$ | 全 $s$ 平面 |
| 2 | $u(t)$ | $\dfrac{1}{s}$ | $\mathrm{Re}\{s\}>0$ |
| 3 | $\mathrm{e}^{at}u(t)$ | $\dfrac{1}{s-a}$ | $\mathrm{Re}\{s\}>\mathrm{Re}\{a\}$ |
| 4 | $t^n\mathrm{e}^{at}u(t)$ | $\dfrac{n!}{(s-a)^{n+1}}$ | $\mathrm{Re}\{s\}>\mathrm{Re}\{a\}$ |
| 5 | $t^nu(t)$ | $\dfrac{n!}{s^{n+1}}$，如 $tu(t)\leftrightarrow\dfrac{1}{s^2}$ | $\mathrm{Re}\{s\}>0$ |
| 6 | $\cos(\Omega_0t)u(t)$ | $\dfrac{s}{s^2+\Omega_0^2}$ | $\mathrm{Re}\{s\}>0$ |
| 7 | $\sin(\Omega_0t)u(t)$ | $\dfrac{\Omega_0}{s^2+\Omega_0^2}$ | $\mathrm{Re}\{s\}>0$ |
| 8 | $\mathrm{e}^{-at}\cos(\Omega_0t)u(t)$ | $\dfrac{s+a}{(s+a)^2+\Omega_0^2}$ | $\mathrm{Re}\{s\}>-a$ |
| 9 | $\mathrm{e}^{-at}\sin(\Omega_0t)u(t)$ | $\dfrac{\Omega_0}{(s+a)^2+\Omega_0^2}$ | $\mathrm{Re}\{s\}>-a$ |
| 10 | $\sum\limits_{n=0}^{\infty}\delta(t-nT)$ | $\dfrac{1}{1-\mathrm{e}^{-sT}}$ | $\mathrm{Re}\{s\}>0$ |

**记法**：$\mathrm{e}^{at}u(t)\leftrightarrow\dfrac{1}{s-a}$ 是母对（$a=0$ 得 $u(t)$，乘 $t^n$ 用复频域微分反复求导）；三角对分子 $\cos$ 取 $s$、$\sin$ 取 $\Omega_0$，分母同为 $s^2+\Omega_0^2$，衰减情形把 $s$ 换成 $s+a$、ROC 左边界移到 $-a$。

**极点位置定时域形态**：极点越靠左衰减越快；虚轴上为等幅振荡；实部为正则发散；虚部大小即振荡角频率 $\Omega_0$；$r$ 重极点带 $t^{r-1}$ 包络因子。

## 5. 拉氏逆变换

**总流程**：判分子阶数 $m$ 与分母阶数 $n$ → 假分式先长除 → 真分式部分分式展开 → 查表 → **由 ROC 定时域项**。

有理函数 $X(s)=\dfrac{B(s)}{A(s)}=\dfrac{b_ms^m+\cdots+b_0}{s^n+a_{n-1}s^{n-1}+\cdots+a_0}$（系数为实数）：$m\ge n$ 为**假（非真）分式**，$m<n$ 为**真分式**。

### 5.1 非真分式（$m\ge n$）：先长除

$$X(s)=\frac{B(s)}{A(s)}=Q(s)+\frac{R(s)}{A(s)},\qquad
Q(s)=\sum_{k=0}^{m-n}c_ks^k\ \longleftrightarrow\ \sum_{k=0}^{m-n}c_k\delta^{(k)}(t)$$

漏掉长除必漏 $\delta(t)$ 及其各阶导数项。

### 5.2 真分式（$m<n$）：三类极点的部分分式展开

单极点情形先分解为 $X(s)=\sum\limits_{i}\dfrac{K_i}{s-p_i}$，再由 $p_i$ 的类型与 ROC 查表：

| 极点类型 | 系数求法 | 对应时域项 | ROC 与取向 |
|---|---|---|---|
| 单实极点 $p_i$ | $K_i=\left.(s-p_i)X(s)\right\rvert_{s=p_i}$ | $K_i\mathrm{e}^{p_it}u(t)$；ROC 在左时取 $-K_i\mathrm{e}^{p_it}u(-t)$ | $\mathrm{Re}\{s\}>\mathrm{Re}\{p_i\}$ 取 $u(t)$；反之取 $u(-t)$ |
| 单复极点 $p_{1,2}=\alpha\pm\mathrm{j}\Omega_0$ | 求一个 $K=C+\mathrm{j}D$，另一项自动取共轭 $K^{*}$ | $2\mathrm{e}^{\alpha t}\left[C\cos\Omega_0t-D\sin\Omega_0t\right]u(t)$ | $\mathrm{Re}\{s\}>\alpha$（或 $<\alpha$ 时整体反号换 $u(-t)$）；合成**别漏乘 2** |
| $r$ 重极点 $p$ | $K_k=\dfrac{1}{(r-k)!}\left.\dfrac{\mathrm{d}^{r-k}}{\mathrm{d}s^{r-k}}\left[(s-p)^rX(s)\right]\right\rvert_{s=p}$，$k=1,\dots,r$ | 每项 $\dfrac{t^{k-1}}{(k-1)!}\mathrm{e}^{pt}u(t)$ | $\mathrm{Re}\{s\}>\mathrm{Re}\{p\}$；$K_r$ 直接代 $s=p$ 不求导 |

### 5.3 同一个 $X(s)$、不同 ROC → 不同 $x(t)$

- ROC 为**最右极点以右**：各项全取 $u(t)$，得右边信号；
- ROC 为**最左极点以左**：各项全取 $u(-t)$，得左边信号（系数符号也相反）；
- ROC 为**两极点之间的条带**：条带以右的极点项取 $u(t)$、以左的取 $u(-t)$，得双边信号。

⚠️ 算完回代：逐项正变换应还原 $X(s)$，且 ROC 一致。

## 6. 拉氏变换与傅里叶变换的关系

判据只有一句：**虚轴 $s=\mathrm{j}\Omega$（即 $\sigma=0$）是否落在 ROC 内**。

| 情形 | 结论 |
|---|---|
| 虚轴在 ROC 内 | $X_F(\Omega)=\left.X(s)\right\rvert_{s=\mathrm{j}\Omega}$：把 $X(s)$ 中的 $s$ 直接换成 $\mathrm{j}\Omega$ |
| 虚轴不在 ROC 内、且无虚轴极点 | 傅氏积分不收敛，$X_F(\Omega)$ 不存在；但取 $\sigma\ne0$ 且属于 ROC 时拉氏变换仍存在（拉氏适用范围更广的原因） |
| 虚轴上有**单重**极点 $\mathrm{j}\Omega_k$ | $X_F(\Omega)=X_0(\mathrm{j}\Omega)+\pi\sum\limits_k A_k\delta(\Omega-\Omega_k)+\mathrm{PV}\sum\limits_k\dfrac{A_k}{\mathrm{j}(\Omega-\Omega_k)}$ |
| 虚轴上有 $r$ 重极点 $\mathrm{j}\Omega_0$ | $X_F(\Omega)=X_0(\mathrm{j}\Omega)+\pi\sum\limits_{r}\dfrac{A_r\mathrm{j}^{r-1}}{(r-1)!}\delta^{(r-1)}(\Omega-\Omega_0)$，**$\delta$ 的阶数等于 $r-1$** |

- **稳定判据**：ROC 含虚轴 ⇔ 系统稳定。因果系统的 ROC 是最右极点以右，故又等价于**全部极点位于左半平面**。
- **三步判断**：求出 $X(s)$ 的极点并标在 $s$ 平面 → 确定 ROC → 看虚轴是否落在 ROC 内。

## 7. 易错点（一行一条）

- $s=\sigma+\mathrm{j}\Omega$ 中 $\sigma$ 是**实部**；逆变换路径的横坐标另记 $\gamma$（取在 ROC 内），$\sigma$ 与 $\gamma$ 不要混。
- 双边拉氏变换必须**成对写 $X(s)$ 与 ROC**；只写像函数无法定信号。
- ROC **不含边界、内无极点**；边界由极点所在竖直线决定；双边信号对应两端都开的条带。
- 单边变换下限是 $0^{-}$ 而不是 $0$ 或 $0^{+}$；初始值一律写 $x(0^{-})$。
- ROC 的等号与包含：线性、卷积、时域积分的 ROC 只能写"至少包含"（零极点相消可能扩大）；时移、频移、尺度、复频域微分可写等号。
- 尺度变换系数是 $\dfrac{1}{\lvert a\rvert}$ 而不是 $\dfrac{1}{a}$；且 $a$ 必须为非零实常数。
- 时移只乘 $\mathrm{e}^{-st_0}$，**ROC 与幅度谱都不变**；频移把 ROC 沿实轴平移 $\mathrm{Re}\{s_0\}$，与虚部无关。
- 时域微分：双边是 $sX(s)$（无初始值项），单边是 $sX(s)-x(0^{-})$——**漏初始值项是最常见失分点**。
- 时域积分除以 $s$ 会在原点加极点，ROC 还要挖掉 $\mathrm{Re}\{s\}=0$ 这条边界。
- $\delta(t)\leftrightarrow1$ 的 ROC 是**全 $s$ 平面**，不是 $\mathrm{Re}\{s\}>0$。
- 三角对分子：$\cos$ 取 $s$、$\sin$ 取 $\Omega_0$，不要记反；衰减余弦的 ROC 是 $\mathrm{Re}\{s\}>-a$（不是 $>a$）。
- 逆变换先判 $m$ 与 $n$：$m\ge n$ 不先长除，必漏 $\delta$ 及其导数项。
- 单复极点合成后系数是 $2\mathrm{e}^{\alpha t}[\cdot]$，**别漏乘 2**；共轭两项只需算一个系数。
- 重极点系数里乘的是 $(s-p)^rX(s)$（**全部 $r$ 次幂**），求导阶数是 $r-k$，不是 $r$ 或 $k$。
- ROC 与 $u(t)/u(-t)$ 必须配套：$\dfrac{1}{s-\alpha}$ 在 $\mathrm{Re}\{s\}>\alpha$ 下是 $\mathrm{e}^{\alpha t}u(t)$，在 $\mathrm{Re}\{s\}<\alpha$ 下是 $-\mathrm{e}^{\alpha t}u(-t)$，**符号也相反**。
- 初值定理给的是 $x(0^{+})$（不是 $x(0^{-})$），且 $t=0$ 含冲激时反映不出来；$X(s)$ 含 $s$ 正幂次要先长除。
- 终值定理必须先查 $sX(s)$ 的极点：存在虚轴极点（$s=0$ 一重除外）或右半平面极点时终值不存在，硬套公式必错。
- 与傅氏关系：只有虚轴在 ROC 内才可写 $X_F(\Omega)=X(s)\rvert_{s=\mathrm{j}\Omega}$；虚轴有极点时要补 $\pi A_k\delta$ 与 $\mathrm{PV}$ 项，$r$ 重极点对应 $\delta^{(r-1)}$。

---

<a id="cram-05"></a>

# 第五篇　连续系统分析与滤波器（第3、4章）

> 对应课件：《信号分析与处理》第3章-20261020.pptx（145 页）+ 第4章-20261020.pptx（101 页）

> 来源：《信号分析与处理》第3章-20261020.pptx（145 页）+ 第4章-20261020.pptx（101 页）的浓缩版；完整版见 笔记/03-连续时间系统的分析/ 与 笔记/04-滤波与滤波器/

考前用法：第 3 章抓**两张表**（四大特性判别表、零极点判据全表）+ 梅森公式；第 4 章抓**两条主线**（无失真条件、巴特沃斯四步）+ 一张频率变换表。

# 第3章 连续时间系统的分析

系统即算子 $y(t)=T[x(t)]$。四条路线描述同一个系统：**时域**（微分方程、$h(t)$、卷积）⟷**频域**（$H(j\Omega)$）⟷**复频域**（$H(s)$、零极点图）⟷**结构**（方框图/信号流图）。全部结论以 **LTI** 为前提。

## 1. ★ 系统四大特性判别表

| 特性 | 数学判据 | 要点 |
|---|---|---|
| 线性 | $T[a x_1+b x_2]=aT[x_1]+bT[x_2]=ay_1+by_2$ | = **可加性 + 齐次性**，缺一不可；判时一次性代入 $ax_1+bx_2$，出现交叉项即非线性 |
| 时不变 | $T[x(t-t_0)]=y(t-t_0)$ | 先时移再入系统 = 先入系统再时移；判时看输出里**所有** $t$ 是否同步换成 $t-t_0$ |
| 因果 | $x(t)=0\ (t<t_0)\Rightarrow y(t)=0\ (t<t_0)$ | 输出只用当前与过去输入；输入中出现 $t+t_0\,(t_0>0)$ 即用了未来值 |
| 稳定 | $\lvert x\rvert<\infty\Rightarrow\lvert y\rvert<\infty$（BIBO） | 有界输入 → 有界输出；与"响应最终是否衰减到 0"是两回事 |

⚠️ 四性**各自独立**：$y=tx(t)$ 线性但时变；$y=x^2(t)$ 非线性但时不变；因果与稳定互不蕴含。

## 2. 时域分析

### 2.1 系统模型

$n$ 阶线性常系数微分方程（$a_n\ne0$）：$\sum\limits_{i=0}^{n}a_i\,y^{(i)}(t)=\sum\limits_{j=0}^{m}b_j\,x^{(j)}(t)$。微分方程、方框图、信号流图三者**等价**；基本单元为加法器、数乘器、**积分器** $1/s$（微分器改用积分器实现）。

### 2.2 完全响应分解（依据线性）

$$y(t)=y_{zi}(t)+y_{zs}(t)$$

| 分量 | 由谁决定 | 形式 |
|---|---|---|
| 零输入响应 $y_{zi}$ | 只由**初始状态**决定，与激励无关 | **齐次解** |
| 零状态响应 $y_{zs}$ | 只由**激励**决定，初始状态取零 | 特解（用卷积求） |

### 2.3 零输入响应（齐次解）

① 特征方程 $\sum a_i\alpha^i=0$ 求特征根；② 按根型写齐次解；③ 用 $t=0_-$ 的初始值定系数（输入为零时状态不跳变）。

| 特征根 | 齐次解 |
|---|---|
| 互异实根 $\alpha_i$ / $r$ 重根 $\alpha$ | $\sum_i A_i e^{\alpha_i t}$ / $(A_0+A_1t+\cdots+A_{r-1}t^{r-1})e^{\alpha t}$ |
| 共轭复根 $\sigma\pm\mathrm{j}\Omega$ | $e^{\sigma t}(A\cos\Omega t+B\sin\Omega t)$ |

### 2.4 零状态响应：卷积

$$y_{zs}(t)=x(t)*h(t)=\int_{-\infty}^{\infty}x(\upsilon)h(t-\upsilon)\,\mathrm{d}\upsilon$$

思路三步：① 输入拆成冲激的组合 $x(t)=\int x(\upsilon)\delta(t-\upsilon)\mathrm{d}\upsilon$；② 由**时不变性** $\delta(t-\upsilon)\to h(t-\upsilon)$；③ 由**线性**叠加得卷积。⚠️ 两条前提各用一次。激励时移原样传给响应：$\delta(t-t_0)\to h(t-t_0)$、$u(t-t_0)\to g(t-t_0)$。两矩形脉冲卷积得**分段线性梯形**（等宽时退化为三角形），卷积时宽 = 两信号时宽之和。

### 2.5 冲激响应 $h(t)$ 与阶跃响应 $g(t)$

两者都是**零状态**响应（初始状态零），互为微积分：阶跃响应 $s(t)$（本课记 $g(t)$）满足 $g(t)=\int_{-\infty}^{t}h(\upsilon)\mathrm{d}\upsilon$、$h(t)=\dfrac{\mathrm{d}g}{\mathrm{d}t}$。

⚠️ 方向别反：$h=\mathrm{d}g/\mathrm{d}t$。

| 系统 | $h(t)$ |
|---|---|
| 放大器（数乘 $a$） | $a\delta(t)$ |
| 微分器 | $\delta'(t)$ |
| 积分器 | $u(t)$ |
| 延时器（延 $\upsilon$） | $\delta(t-\upsilon)$ |

**由微分方程求 $h(t)$**：令 $x=\delta$、$y=h$ 代入，按阶次分两种情形，再比较两端 $\delta$ 各阶导数系数定 $A_i$（及 $B_j$）。

- $n>m$：$h(t)=\big(\sum_{i=1}^{n}A_ie^{\alpha_it}\big)u(t)$，**不含冲激项**；
- $n\le m$：$h(t)=\big(\sum_{i=1}^{n}A_ie^{\alpha_it}\big)u(t)+\sum_{j=0}^{m-n}B_j\delta^{(j)}(t)$，**含 $\delta$ 及其各阶导数**。

也可由反变换求：$h(t)=\mathscr{L}^{-1}\{H(s)\}$（见 §4）。

### 2.6 ★ 用 $h(t)$ 判因果与稳定（充要条件）

| 特性 | 充要条件 | 反例 / 注意 |
|---|---|---|
| 因果 | $h(t)=0,\quad t<0$ | $h=\delta(t+1)$ 在 $t<0$ 非零 ⇒ 非因果 |
| 稳定 | $\displaystyle\int_{-\infty}^{\infty}\lvert h(t)\rvert\,\mathrm{d}t<\infty$（绝对可积） | 积分器 $h=u(t)$ 积分发散 ⇒ 不稳定 |

⚠️ 稳定判据里**绝对值不能丢**；因果看 $t<0$ 是否**恒为零**。

### 2.7 时域分析链条

建方程 → 求 $y_{zi}$（特征方程→齐次解→初值定系数）+ $y_{zs}$（$h(t)$ 卷积）→ 相加 → 由 $h(t)$ 判因果/稳定。$t\to\infty$ 趋于 0 的是**暂态分量**，保留的是**稳态分量**。

## 3. 频域分析

$$H(j\Omega)=\int_{-\infty}^{+\infty}h(t)e^{-\mathrm{j}\Omega t}\,\mathrm{d}t=\mathscr{F}[h(t)],\qquad Y_{zs}(j\Omega)=X(j\Omega)\,H(j\Omega),\qquad H(j\Omega)=\frac{Y_{zs}(j\Omega)}{X(j\Omega)}$$

虚指数 $e^{\mathrm{j}\Omega t}$ 通过稳定 LTI 系统仍是同频虚指数、只乘复常数 $H(j\Omega)$，即 **频率响应 = 冲激响应的傅里叶变换**。

**幅频与相频**：$H=\lvert H\rvert e^{\mathrm{j}\chi(\Omega)}$，$\lvert H\rvert$ 是 $\Omega$ 的**偶函数**、$\chi$ 是**奇函数**；输出 $\lvert Y\rvert=\lvert X\rvert\lvert H\rvert$、$\chi_y=\chi_x+\chi$。

**正弦稳态响应**：$\cos(\Omega_0t)\to\lvert H(j\Omega_0)\rvert\cos[\Omega_0t+\chi(\Omega_0)]$，$\sin$ 同理——**幅度乘 $\lvert H\rvert$、相位加 $\chi$**。

**频域分析法三步**：① 求 $H(j\Omega)$；② $Y_{zs}=X\cdot H$；③ 反变换。由微分方程求：$\frac{\mathrm{d}^k}{\mathrm{d}t^k}\to(j\Omega)^k$，得 $H(j\Omega)=\dfrac{\sum b_k(j\Omega)^k}{\sum a_k(j\Omega)^k}$。⚠️ 频域分析只求**零状态**响应。

## 4. 复频域分析（重点）

### 4.1 系统函数 $H(s)$（微分方程 ↔ $H(s)$ ↔ 方框图/流图，三种等价描述）

$$H(s)=\int_{-\infty}^{+\infty}h(t)e^{-st}\,\mathrm{d}t=\mathscr{L}[h(t)],\qquad Y_{zs}(s)=X(s)H(s),\qquad H(s)=\frac{Y_{zs}(s)}{X(s)}=\frac{\sum_{k=0}^{m}b_ks^k}{\sum_{k=0}^{n}a_ks^k}$$

即 **$H(s)$ 与 $h(t)$ 互为拉普拉斯变换对**：$h(t)\leftrightarrow H(s)$；由微分方程（零状态）$\frac{\mathrm{d}^k}{\mathrm{d}t^k}\to s^k$ 直接代入即得。**三步**：① 求 $H(s)$；② $Y_{zs}(s)=X(s)H(s)$；③ 反变换 $y_{zs}=\mathscr{L}^{-1}\{Y_{zs}(s)\}$。

### 4.2 零极点形式与零极点图

$$H(s)=H_0\frac{\prod_{j=1}^{m}(s-z_j)}{\prod_{i=1}^{n}(s-p_i)},\qquad H_0=\frac{b_m}{a_n}$$

**零点** $z_j$：使 $H(s)=0$ 的分子根；**极点** $p_i$：使 $H(s)\to\infty$ 的分母根。零极点图：$s$ 平面上零点画 $\circ$、极点画 $\times$，重根标重数。实系数 ⇒ 零极点必成**共轭对**。

### 4.3 ★ 零极点判据全表

| 结论 | 收敛域 / 极点条件 | 等价说法 |
|---|---|---|
| **因果** | ROC 是 $\mathrm{Re}\{s\}>\tau_0$，即**最右极点右侧**的右半平面 | $h(t)=0\ (t<0)$ |
| **稳定** | ROC **包含虚轴** $j\Omega$ | $\int\lvert h(t)\rvert\mathrm{d}t<\infty$ |
| **因果且稳定** | **全部极点位于左半平面**（$\mathrm{Re}\{s\}<0$） | 最右极点也在虚轴左侧 |

推理链：因果 ⇒ ROC 在最右极点右侧；稳定 ⇒ ROC 含虚轴；两者同时成立 ⇒ 最右极点必在虚轴左侧 ⇒ 极点全在左半平面。**右半平面有极点必不稳定；虚轴上有极点 ⇒ 不是稳定系统（等幅振荡）。**

### 4.4 ★ 零极点位置 → 时域模态

| 极点位置 | $h(t)$ 的模态 |
|---|---|
| 实极点 $\alpha<0$ / $>0$ / $=0$ | $e^{\alpha t}$ 单调衰减 / 单调增长 / 常数 |
| 共轭 $\sigma\pm\mathrm{j}\Omega$，$\sigma<0$ / $=0$ / $>0$ | 衰减振荡 / **等幅振荡** / 增幅振荡 |
| $r$ 重极点 | 乘 $t^{r-1}$ 的同一模态 |

**一句话**：极点**实部符号定稳定性**、**虚部定是否振荡**；**零点只影响幅度与相位，不影响稳定性**。

### 4.5 零极点图与 $H(j\Omega)$

ROC 含虚轴时 $H(j\Omega)=\left.H(s)\right|_{s=\mathrm{j}\Omega}$；$\lvert H\rvert$ 为各零点矢长之积÷各极点矢长之积，$\varphi$ 为零点矢角之和−极点矢角之和。故**离极点越近 $\lvert H\rvert$ 越大、离零点越近越小**。⚠️ 该式**只在 ROC 含虚轴（稳定）时成立**。

## 5. 信号流图与梅森公式

| 术语 | 含义 |
|---|---|
| 节点 / 支路 | 节点表示信号；支路是有向线段并标增益 |
| 前向通路 $P_k$ | 输入→输出且不重复经过节点的通路，增益为各支路增益之积 |
| 环路 $L_k$ | 闭合路径，增益为各支路增益之积 |
| 不接触环路 | **没有公共节点**的环路（仅支路不相交不算） |

$$\boxed{\,H=\frac{\sum_k P_k\Delta_k}{\Delta}\,},\qquad \Delta=1-\sum_kL_k+\sum_{m,n}L_mL_n-\sum_{p,q,r}L_pL_qL_r+\cdots$$

$\Delta$ 称**特征式**：单环路增益之和取负、两两不接触环路增益乘积之和取正、三三取负，符号交替。$\Delta_k$ = 与第 $k$ 条前向通路**不接触**的那部分环路的特征式（无不接触环路时 $\Delta_k=1$）。⚠️ 分子漏掉 $\Delta_k$ 是最常见错误。**转置**：所有支路反向、输入输出互换，传输函数不变。

## 6. 连续系统的模拟结构

基本单元：积分器 $s^{-1}$、加法器、数乘器 $a$。⚠️ 直接Ⅱ型比Ⅰ型省积分器，但 $H(s)$ **不变**；级联用"相乘"、并联用"相加"，别混。

| 结构 | 构造方式 | 特点 |
|---|---|---|
| 直接Ⅰ型 | 按 $H=H_1H_2$ 级联：$H_1$ 实现零点（分子）、$H_2$ 实现极点（分母） | 两条积分链，**积分器最多** |
| 直接Ⅱ型 | 交换 $H_1$、$H_2$ 次序并**共用一条积分链** | **积分器最少**（$N$ 阶用 $N$ 个），工程最常用 |
| 级联型 | 分解为一阶/二阶子系统**相乘**，每节用直接Ⅱ型 | 便于单独调整零极点 |
| 并联型 | 展开为若干一阶/二阶项**相加** | 各支路独立，便于调整各极点 |

## 7. 第3章易错点

- 零输入响应只由初始状态决定（齐次解），求零状态响应必须把初始状态置零；"全响应 = 零输入 + 零状态"只对**线性**系统成立。
- 共轭复根时齐次解写成 $e^{\sigma t}(A\cos+B\sin)$，不要保留复指数。
- 因果 ≠ 稳定；因果系统 ROC 是 $\mathrm{Re}\{s\}>\tau_0$，**不能**据此说"极点都在左半平面"——那是再加稳定才推出的结论。
- 稳定性只看**极点**；虚轴有极点即不稳定，一个极点都不能漏看。

# 第4章 滤波与滤波器

主线：**概念与指标 → 无失真与理想低通 → 巴特沃斯逼近 → 模拟频率变换**。

## 1. 概念与性能指标

**定义**：选择所需频带的信号、抑制其余频带信号的系统。**四个频带**：**通带**（允许通过，边缘即**截止频率**、定义**带宽**）、**阻带**（抑制）、**过渡带**（通带→阻带的过渡范围，理想滤波器没有）、阻带起始。**分类**：按信号（模拟/数字）、按应用（有源/无源）、按通频带（**低通 LPF / 高通 HPF / 带通 BPF / 带阻 BSF**，本章主线）。

**技术指标（LPF 四项）**：通带 $\Omega_p$、$A_p$；阻带 $\Omega_s$、$A_s$；$\Omega_c$ 为 **3 dB 截止频率**。$\varepsilon$ 为通带内波动系数，$A$ 为阻带衰减参数。

| 形式 | 表达式 |
|---|---|
| 绝对指标（通带 / 阻带） | $\dfrac{1}{1+\varepsilon^{2}}\le\lvert H(j\Omega)\rvert^{2}\le1\ (\lvert\Omega\rvert\le\Omega_p)$；$0\le\lvert H_a(j\Omega)\rvert^{2}\le\dfrac{1}{A^{2}}\ (\lvert\Omega\rvert\ge\Omega_s)$ |
| 相对指标 | $A_p=10\lg(1+\varepsilon^{2})\ \mathrm{dB}$（**通带最大衰减**）；$A_s=20\lg A\ \mathrm{dB}$（**阻带最小衰减**） |
| 反算 | $\varepsilon^{2}=10^{0.1A_p}-1$；$A=10^{0.1A_s/2}=10^{A_s/20}$ |

⚠️ dB 系数：**功率/幅度平方比用 $10\lg$**（$A_p$ 由 $\lvert H\rvert^2$ 来）、**幅度比用 $20\lg$**（$A_s$ 由 $\lvert H\rvert$ 来）。$A_p$ 是"**最大**衰减"、$A_s$ 是"**最小**衰减"，不等式方向别写反。

## 2. 无失真传输

**幅度失真**：各频率分量被不同程度加权；**相位失真**：各分量相移不与频率成正比 ⇒ 各分量时移不同。**相延时**（单一正弦分量时移）$\tau_p=-\dfrac{\chi(\Omega)}{\Omega}$；**群延时**（包络/整体时移）$\tau_g=-\dfrac{\mathrm{d}\chi(\Omega)}{\mathrm{d}\Omega}$。

| 项目 | 条件 |
|---|---|
| 时域条件 | $y(t)=K\,e(t-t_0)$，$K$、$t_0$ 为**实常数** |
| 频域条件 | $\lvert H(j\Omega)\rvert=K$（**常数**）**且** $\chi(\Omega)=-\Omega t_0$（**过原点直线**） |
| 群延时 | $\tau_g=t_0$ 恒为常数（此时 $\tau_p=t_0$） |
| 冲激响应 | $h(t)=K\delta(t-t_0)$ |

⚠️ 无失真 ≠ 幅度不变：允许常数增益 $K$ 与整体时移 $t_0$，只不许波形变形；幅频、相频条件**缺一不可**。$t_0<0$ 时 $h(t)$ 落在 $t<0$ ⇒ **非因果**。

## 3. 理想低通滤波器

$$H(j\Omega)=\begin{cases}A\,e^{-\mathrm{j}\Omega t_0},&\lvert\Omega\rvert<\Omega_c\\ 0,&\lvert\Omega\rvert>\Omega_c\end{cases}$$

通带内无失真（幅频常数、相频直线）、通带外一律为零、**无过渡带**。

| 项目 | 结论 |
|---|---|
| 冲激响应 | $h(t)=\dfrac{\Omega_c}{\pi}\mathrm{Sa}\left[\Omega_c(t-t_0)\right]$，**无限长** |
| **因果性** | $h(t)$ 在 $t<t_0$（含 $t<0$）已非零 ⇒ **非因果**；因果且物理可实现 ⇒ **必然得不到真正理想的低通** |
| 阶跃响应 | $r(t)=\dfrac{1}{2}+\dfrac{1}{\pi}\mathrm{Si}\left[\Omega_c(t-t_0)\right]$，$\mathrm{Si}(y)=\int_0^y\dfrac{\sin x}{x}\mathrm{d}x$ |
| **上升时间** | $t_r=\dfrac{2\pi}{\Omega_c}=\dfrac{1}{f_c}$，与截止频率**成反比** |
| 矩形脉冲响应 | 两个阶跃响应之差 $r_1=r[\text{阶跃}]-r[\text{延时 }\tau\text{ 的阶跃}]$，跳变处**过冲 + 振铃** ⇒ **吉布斯现象（约 9% 过冲）** |

$\mathrm{Si}(y)$：$\mathrm{Si}(0)=0$、奇函数、$y=\pm\pi$ 处取极值；阶跃响应在 $t=t_0$ 处等于 $1/2$，上升过程是 $\mathrm{Si}$ 形状而非指数。**吉布斯要点**：增大 $\Omega_c$ 只压缩振铃时间尺度、**不改变过冲相对幅度** ⇒"截止越陡"与"无过冲"不可兼得。⚠️ $\Omega_c=2\pi f_c$，别丢 $2\pi$。

## 4. 巴特沃斯滤波器（重点）

| 项目 | 公式 / 结论 |
|---|---|
| 幅频特性（幅度平方） | $\lvert H(j\Omega)\rvert^{2}=\dfrac{1}{1+(\Omega/\Omega_c)^{2N}}$，$N$ 为阶数、$\Omega_c$ 为 3 dB 截止频率 |
| 阶数公式 | $N\ge\dfrac{\lg\sqrt{\dfrac{10^{0.1A_s}-1}{10^{0.1A_p}-1}}}{\lg(\Omega_s/\Omega_p)}$，**向上取整**（等价于 $\dfrac{\lg[\cdot]}{2\lg(\Omega_s/\Omega_p)}$） |
| 3 dB 频率 | 由通带 $\Omega_c=\dfrac{\Omega_p}{\left(10^{0.1A_p}-1\right)^{1/(2N)}}$；或由阻带 $\Omega_c=\dfrac{\Omega_s}{\left(10^{0.1A_s}-1\right)^{1/(2N)}}$ |
| **实际极点** | $\boxed{p_k=\Omega_c\,e^{\mathrm{j}\pi(2k+N+1)/(2N)}}$，$k=0,\dots,N-1$（归一化极点即取 $\Omega_c=1$；左半平面取 $N$ 个） |
| 归一化系统函数 | $H(p)=\dfrac{1}{\prod_{k=0}^{N-1}(p-p_k)}$，$p=s/\Omega_c$（$N=1,2,3$ 时分别为 $p+1$、$p^2+1.4142p+1$、$(p+1)(p^2+p+1)$） |
| 反归一化 | $H(s)=\left.H(p)\right|_{p=s/\Omega_c}=\dfrac{\Omega_c^{N}}{\prod_{k=0}^{N-1}(s-p_k\Omega_c)}$ |

**三个特点**：① **3 dB 点及其不变性**——$\Omega=\Omega_c$ 时 $\lvert H\rvert^2=1/2$、衰减恒为 3 dB，与 $N$ 无关；② **单调下降**；③ **最大平坦**（$\Omega=0$ 处各阶导数除最高阶为零，故称"最平响应滤波器"）。有限平面内**只有极点、零点全在 $s=\infty$** ⇒ **全极点型**。

**极点分布**：$2N$ 个极点均匀分布在半径 $\Omega_c$（归一化时 1）的圆上，间隔 $\pi/N$；一半在左半平面、一半在右半平面；**虚轴上无极点**；起始角 $\pi/2+\pi/(2N)$；$N$ 奇数时实轴上有极点。

**设计四步**：① 由指标求 $N$；② 求 $\Omega_c$；③ 求极点/查表得归一化 $H(p)$；④ 反归一化得 $H(s)$。

⚠️ $N$ 要**向上取整**（如 4.98 取 5）；$\Omega_c$ 与 $\Omega_p$ **只在 $A_p=3$ dB 时重合**；$2N$ 个极点**只取左半平面 $N$ 个**；反归一化分子补 $\Omega_c^{N}$（保证 $\lvert H(j0)\rvert=1$）；阶数公式分母的因子 2 不能漏。另三种逼近：切比雪夫Ⅰ/Ⅱ型（通带/阻带等波纹，过渡带较陡）、椭圆（**最陡**、阶数**最低**、相位最差）。

## 5. 模拟频率变换

思路：目标指标 → **归一化低通**指标 → 设计 $H_{lp}(p)$ → 频率变换 $p=q(s)$ → $H_d(s)$，即 $H_d(s)=H_{lp}(p)\big|_{p=q(s)}$。

| 变换 | $\Omega_r$ | 归一化阻带 $\lambda_s$ | 映射 $p=q(s)$ |
|---|---|---|---|
| 低通→**低通** | $\Omega_p$ | $\dfrac{1}{a}\dfrac{\Omega_s}{\Omega_p}$ | $p=\dfrac{1}{a}\dfrac{s}{\Omega_p}$ |
| 低通→**高通** | $\Omega_p$ | $\dfrac{1}{a}\dfrac{\Omega_p}{\Omega_s}$ | $p=\dfrac{1}{a}\dfrac{\Omega_p}{s}$ |
| 低通→**带通** | $B=\Omega_{p2}-\Omega_{p1}$ | $\dfrac{1}{a}\dfrac{\Omega_{s2}-\Omega_{s1}}{\Omega_{p2}-\Omega_{p1}}$ | $p=\dfrac{1}{a}\dfrac{s^{2}+\Omega_0^{2}}{Bs}$ |
| 低通→**带阻** | $B=\Omega_{p2}-\Omega_{p1}$ | $\dfrac{1}{a}\dfrac{\Omega_{p2}-\Omega_{p1}}{\Omega_{s2}-\Omega_{s1}}$ | $p=\dfrac{1}{a}\dfrac{Bs}{s^{2}+\Omega_0^{2}}$ |

四种变换统一有 $\lambda_p=1/a$（$a$ 为归一化常数，通常取 1）；带通与带阻的 $\lambda_s$ **互为倒数**（一个分子是阻带宽度、一个分子是通带宽度），写反直接算错阶数。

**几何对称条件**（带通/带阻设计前提）：$\Omega_0^{2}=\Omega_{p1}\Omega_{p2}=\Omega_{s1}\Omega_{s2}$。由归一化低通变换得到的带通/带阻**必然关于 $\Omega_0$ 几何对称**；指标不满足时**必须先调整截止频率**：阻带 $\hat\Omega_{s1}=\Omega_0^{2}/\Omega_{s2}$ 并取 $A_s=\max\{A_{s1},A_{s2}\}$；通带 $\hat\Omega_{p1}=\Omega_0^{2}/\Omega_{p2}$ 并取 $A_p=\min\{A_{p1},A_{p2}\}$。一句话：**偏松的一侧收紧到对称位置，衰减取两侧更严者**。

**设计步骤**：① 定目标指标（带通/带阻非几何对称**先调整**）；② 查表换算归一化低通 $\lambda_p,\lambda_s,A_p,A_s$；③ 用巴特沃斯/切比雪夫/椭圆设计归一化低通；④ 查变换表得非归一化 $H_d(s)$。

⚠️ 顺序不能反（先变换指标→设计低通→最后换 $s$）；$N$ 阶低通经带通/带阻变换得 **$2N$ 阶**。

## 6. 第4章易错点

- $\Omega_p$ 是设计给定的通带边缘，$\Omega_c$ 是衰减 3 dB 点，**只有 $A_p=3$ dB 时二者重合**。
- $\Omega_c=2\pi f_c$，$t_r=2\pi/\Omega_c=1/f_c$，别丢 $2\pi$。
- 无失真要求幅频常数 **且** 相频过原点直线，两者缺一不可；只满足幅频仍有相位失真。
- 理想低通 $h(t)$ 无限长且 $t<0$ 非零 ⇒ 非因果，物理不可实现，只能逼近；吉布斯过冲约 9%，增大 $\Omega_c$ 只让振铃变窄、过冲幅度不变。
- 巴特沃斯是**全极点型**，有限平面内没有零点；求 $H(s)$ 只取左半平面极点，反归一化分子补 $\Omega_c^{N}$。
- 带通/带阻指标不对称时必须**先收紧到几何对称**再设计；$N$ 阶低通变换后得 $2N$ 阶。

---
