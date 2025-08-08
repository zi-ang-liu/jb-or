---
bibliography:
  - references.bib
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 確率的・連続観測在庫モデル

:::{code-cell} python
:tags: [remove-input, remove-output]
!pip install matplotlib numpy
!pip install scipy
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
:::

これまで紹介した在庫モデルは、需要が決定論的であると仮定していた。ここからは、需要が確率的であると仮定した在庫モデルを紹介する。

## 在庫方策

確率的在庫モデルにおいて、一つ重要な概念は**在庫方策**（inventory policy）である。在庫方策は、在庫の状況に応じて、在庫管理のルールを定めるものである。代表的な在庫方策を以下に示す。

1. $(r, Q)$ 方策：在庫量を連続的に観測し、在庫量が発注点 $r$ 以下になったときに発注量 $Q$ を発注する方式である。**発注点方式**とも呼ばれる。
2. BSP 方策（Base Stock Policy）：在庫量を定期的に観測し、在庫量が基準在庫 $S$ 以下になったときに、在庫量を $S$ まで補充する方式である。**定期発注方式**とも呼ばれる。
3. $(s, S)$ 方策：在庫量を定期的に観測し、在庫量が発注点 $s$ 以下になったときに、在庫量を補充点 $S$ まで補充する方式である。

一部の確率的在庫モデルにに対し、これらの在庫方策は**最適**であることが知られている。その場合、在庫方策が持つパラメータを最適化することで、在庫の期待コストを最小化することができる。

## 問題設定

需要 $D$ がある確率分布に従うと仮定する。リードタイムを $L$ とし、既知の定数とする。発注費用を $K$、単位あたりの保管費用を $h$ とする。在庫量が連続的に観測され、いつでも発注が可能であるとする**連続観測**の場合を考える。

$(r, Q)$ 方策が用いられるとする。在庫量が発注点 $r$ 以下になったときに、発注量 $Q$ を発注する。この場合、発注点 $r$ と発注量 $Q$ を決定変数とし、在庫の**期待コスト**（expected cost）を最小化することを目的とする。

:::{note}
この問題の定式化および厳密解法は、ここでは説明しない。[Snyder & Shen (2019)](https://doi.org/10.1002/9781119584445) の「Fundamentals of Supply Chain Theory」などの文献を参照されたい。
以下は $(r, Q)$ の近似解法を紹介する。
:::

## 近似解法

以下では、単位期間あたりの需要を $D$ とし、$D$ は正規分布 $N(\mu, \sigma^2)$ に従うと仮定する。ここで、$\mu$ は平均需要、$\sigma$ は需要の標準偏差である。

### 発注量 $Q$

$D$ の平均 $\mu$ をEOQモデルの需要率とみなすと、発注量 $Q$ は次のように求めることができる[@Camm2022-zv]。

$$
Q = \sqrt{\frac{2K \mu}{h}}
$$

また、欠品費用も考慮する場合、バックオーダーを考慮した EOQ モデルを用いて、発注量 $Q$ は次のように求めることができる[@Hillier2025-cb]。

$$
Q = \sqrt{\frac{2K \mu}{h}} \sqrt{\frac{p+h}{p}}
$$
$p$ は単位あたりの欠品費用である。

得られた発注量 $Q$ は、最適解ではなく、近似解であることに注意されたい。

### 発注点 $r$ 



リードタイム期間中に発生する需要は $D_L \sim N(\mu_L, \sigma_L^2)$ とし、正規分布の再生性により、

$$
\mu_L = \mu L, \quad \sigma_L^2 = \sigma^2 L
$$

になる。すなわち、リードタイム期間中の平均需要は $\mu_L = \mu L$、標準偏差は $\sigma_L = \sigma \sqrt{L}$ である。

発注点 $r$ を決めるためには、**サービスレベル**（service level）を考える。ここでは、サービスレベルを、リードタイム期間中に需要を満たす確率と定義する。サービスレベルを $\alpha$ とし、$0 < \alpha < 1$ とする。

与えられたサービスレベル $\alpha$ に対して、$D_L$ が発注点 $r$ 以下になる確率（欠品が発生しない確率、つまり、サービスレベル）が $\alpha$ になるように発注点 $r$ を決定する。

$$
P(D_L \leq r) = \alpha
$$

もし、発注点 $r = \mu_L$ とすると、$P(D_L \leq \mu_L) = 0.5$ となる。すなわち、50% の確率で欠品が発生することになる。

:::{note}

$$
P(D_L \leq \mu_L) = P\left(\frac{D_L - \mu_L}{\sigma_L} \leq 0\right) = \Phi(0) = 0.5
$$
:::

したがって、サービスレベル $\alpha > 0.5$ の場合、発注点 $r$ は平均需要 $\mu_L$ より大きくなる必要がある。それを**安全在庫**（safety stock）と呼び、$s$ と表す。

:::{prf:example}
:label: example:safety_stock

単位期間あたりの需要 $D$ が連続一様分布 $U(200, 300)$ に従うと仮定する。平均需要は $\mu = 250$ である。一回の発注量を $Q = 500$ とする。次の図は、在庫量の時間的変化を示す。灰色の領域は、需要の範囲を示す。赤い領域は、在庫量が0以下になったときの欠品を示す。黒い線は平均需要に基づく在庫量の変化を示す。

:::{code-cell} python
:tags: [remove-input]
import numpy as np
import matplotlib.pyplot as plt

# Parameters
d_mean = 250  # Mean demand rate
d_max = 300   # Max demand rate
d_min = 200   # Min demand rate
Q = 500       # Order quantity
T = Q / d_mean  # Average cycle length

# Simulate over multiple cycles to show repeated pattern
n_cycles = 1
t = np.linspace(0, n_cycles * T, 1000)

# Inventory levels: linear depletion over time
inventory_mean = Q - d_mean * (t % T)
inventory_mean[0] = 0
inventory_max = Q - d_max * (t % T)
inventory_min = Q - d_min * (t % T)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(t, inventory_mean, label="Mean Demand", color="black", linewidth=2)
plt.fill_between(t, inventory_min, inventory_max, color="gray", alpha=0.5, label="Demand Range")

# Highlight when inventory drops below 0 (shortage)
plt.fill_between(t, inventory_max, 0, where=(inventory_max < 0), color="red", alpha=0.3, label="Shortage")

# Aesthetics
plt.axhline(0, color="gray", linewidth=1)
plt.xlabel("Time", fontsize=14)
plt.ylabel("Inventory Level", fontsize=14)
plt.title("Inventory Level Over Time with Uniform Demand Distribution", fontsize=16)
plt.legend(fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

:::

よって、発注点 $r$ は次のように表される。

$$
r = \mu_L + s
$$

従って、$P(D_L \leq r) = \alpha$ は次のように表される。

$$
P(D_L \leq \mu_L + s) = \alpha
$$

この式を変形すると、

$$
\begin{align*}
P(D_L - \mu_L \leq s) &= \alpha \\
P\left(\frac{D_L - \mu_L}{\sigma_L} \leq \frac{s}{\sigma_L}\right) &= \alpha \\
\Phi\left(\frac{s}{\sigma_L}\right) &= \alpha \\
\frac{s}{\sigma_L} &= \Phi^{-1}(\alpha) \\
s &= \sigma_L \Phi^{-1}(\alpha) \\
s &= \sigma \sqrt{L} \Phi^{-1}(\alpha)
\end{align*}
$$

ここで、$\Phi(\cdot)$ は標準正規分布の累計分布関数であり、$\Phi^{-1}(\alpha)$ はその逆関数である。したがって、発注点 $r$ は次のように表される。

$$
r = \mu_L + s = \mu L + \sigma \sqrt{L} \Phi^{-1}(\alpha)
$$

$\Phi^{-1}(\alpha)$ は標準正規分布表、Excel、Python などを用いて求めることができる。

:::{prf:example}
:label: example:safety_stock_calculation
リードタイム $L = 4$、平均需要 $\mu = 100$、需要の標準偏差 $\sigma = 20$、サービスレベル $\alpha = 0.95$ のとき、発注点 $r$ と安全在庫 $s$ を求める。

リードタイム期間中の平均需要と標準偏差は次のように計算される。

$$
\begin{align*}
\mu_L &= \mu L = 100 \cdot 4 = 400 \\
\sigma_L &= \sigma \sqrt{L} = 20 \sqrt{4} = 40 \\
\end{align*}
$$

標準正規分布表から $\Phi^{-1}(0.95) \approx 1.64485$ を得る。これを用いて安全在庫 $s$ と発注点 $r$ を求める。

$$
\begin{align*}
s &= \sigma_L \Phi^{-1}(0.95) \approx 40 \cdot 1.64485 \approx 65.79 \\
r &= \mu_L + s \approx 400 + 65.79 \approx 465.79
\end{align*}
$$

したがって、発注点 $r$ は約465.79、必要な安全在庫 $s$ は約65.79となる。

Python では、以下のように計算できる。

:::{code-cell} python
from scipy.stats import norm

L = 4
mu = 100
sigma = 20
alpha = 0.95

mu_L = mu * L
sigma_L = sigma * (L ** 0.5)

s = sigma_L * norm.ppf(alpha)
r = mu_L + s

print(f"reorder point: {r:.2f},  safety stock: {s:.2f}")
:::

