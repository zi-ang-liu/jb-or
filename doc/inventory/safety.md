---
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

## $(r, Q)$ 方策

需要 $D$ がある確率分布に従うと仮定する。リードタイムを $L$ とし、既知の定数とする。在庫量が連続的に観測され、いつでも発注が可能であるとする**連続観測**の場合を考える。

適切な在庫管理を行うために、以下の2つを決定する必要がある。

- いつ発注を行うか（発注のタイミング）
- 発注量をどれくらいにするか（発注量）

確率的・連続観測の在庫モデルでは、一般的に $(r, Q)$ 方策を採用する。ここで、$r$ は**発注点**（reorder point）と呼ばれ、在庫量が $r$ 以下になったときに発注を行う。$Q$ は**発注量**である。この方式は、**発注点法**とも呼ばれる。

次の図は $(r, Q)$ 方策を用いた在庫量の変化を示している。需要が確率的である。

:::{code-cell} python
:tags: [remove-input]

:::

$r$ と $Q$ を決定変数とし、在庫の**期待コスト**（expected cost）を最小化することを目的とする。

## 問題設定

単位期間あたりの需要を $D$ とし、$D$ は正規分布 $N(\mu, \sigma^2)$ に従うと仮定する。ここで、$\mu$ は平均需要、$\sigma$ は需要の標準偏差である。

リードタイムを $L$ とし、既知の定数とする。発注費用を $K$、単位あたりの保管費用を $h$ とする。

:::{note}
この問題の定式化および厳密解法は、ここでは説明しない。[Snyder & Shen (2019)](https://doi.org/10.1002/9781119584445) の「Fundamentals of Supply Chain Theory」などの文献を参照されたい。
以下は $(r, Q)$ の近似解法を紹介する。
:::

### 発注点 $r$ 

発注点 $r$ を決めるためには、**サービスレベル**（service level）を考える。ここでは、サービスレベルを、リードタイム期間中に需要を満たす確率と定義する。サービスレベルを $\alpha$ とし、$0 < \alpha < 1$ とする。

リードタイム期間中の需要を確率変数 $D_L$ とし、$D_L \leq r$ の確率が $\alpha$ になるように発注点 $r$ を決定する。すなわち、

$$
P(D_L \leq r) = \alpha
$$

により、発注点 $r$ を求める。

リードタイム期間中に発生する需要は $D_L \sim N(\mu_L, \sigma_L^2)$ とし、正規分布の再生性により、

$$
\mu_L = \mu L, \quad \sigma_L^2 = \sigma^2 L
$$

になる。すなわち、リードタイム期間中の平均需要は $\mu_L = \mu L$、標準偏差は $\sigma_L = \sigma \sqrt{L}$ である。

$D_L$ は確率変数であるため、発注点 $r$ は平均需要と安全在庫 $s$ の和として表される。

$$
r = \mu_L + s
$$

従って、

$$
P(D_L \leq r) = P(D_L \leq \mu_L + s) = \alpha
$$
となる。この式を変形すると、

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
:label: example:safety_stock
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

### 発注量 $Q$