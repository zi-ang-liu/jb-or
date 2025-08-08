# 確率

離散型確率変数 $X$ が特定の値 $x$ をとる確率を

$$
P(X = x) = p_X(x)
$$

と表すとき、$p_X(x)$ を $X$ の**確率質量関数** (PMF) という。

連続型確率変数 $X$ がある区間 $[a, b]$ にある値をとる確率を

$$
P(a \leq X \leq b) = \int_a^b f_X(x) dx
$$

と表す。$f_X(x)$ を $X$ の**確率密度関数** (PDF) という。

確率変数 $X$ の**累計分布関数**（CDF）は

$$
F_X(x) = P(X \leq x) = \begin{cases}
\sum_{k \leq x} p_X(k) & \text{if } X \text{ is discrete} \\
\int_{-\infty}^x f_X(t) dt & \text{if } X \text{ is continuous}
\end{cases}
$$

と表す。確率密度関数 $f_X(x)$ は累計分布関数 $F_X(x)$ の微分である。

$$
f_X(x) = \frac{d}{dx} F_X(x)
$$

## 正規分布

連続型確率変数 $X$ は**正規分布**（normal distribution）に従うとき、$X \sim N(\mu, \sigma^2)$ と表す。ここで $\mu$ は平均、$\sigma^2$ は分散である。$X$ の確率密度関数は

$$
f_X(x) = \frac{1}{\sqrt{2\pi} \sigma} e^{-\frac{(x - \mu)^2}{2\sigma^2}}
$$

と表す。平均は $E[X] = \mu$、分散は $\text{Var}(X) = \sigma^2$ である。

$X$ が $N(\mu, \sigma^2)$ に従うとき、$Y = aX + b$ は、$N(a\mu + b, a^2\sigma^2)$ に従う。特に、$Z = \frac{X - \mu}{\sigma}$ は標準正規分布（standard normal distribution）に従う。すなわち、$Z \sim N(0, 1)$ である。

連続型確率変数 $Y$ が標準正規分布に従うとき、$Y$ の累計分布関数は

$$
\Phi(y) = P(Y \leq y) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^y e^{-\frac{t^2}{2}} dt
$$

と表す。**標準正規分布表**から、$y$ の値に対する $\Phi(y)$ を調べることができる。

Python では、以下のように $\Phi(y)$ を計算できる。

```python
from scipy.stats import norm
def phi(y):
    return norm.cdf(y)

phi(0)  # 0.5
```

また、$\Phi(y)=0.95$ のときの $y$ の値を求めるには、以下のようにする。

```python
from scipy.stats import norm
def phi_inverse(p):
    return norm.ppf(p)

phi_inverse(0.95)  # 約1.64485
```

与えられた $X \sim N(\mu, \sigma^2)$ の累計分布関数 $F_X(x)$ の値を求めるには、以下のように変換する。

$$
\begin{align*}
P(X \leq x) 
&= P \left( \frac{X - \mu}{\sigma} \leq \frac{x - \mu}{\sigma} \right) \\\\
&= P\left( Y \leq \frac{x - \mu}{\sigma} \right) \\\\
&= \Phi \left( \frac{x - \mu}{\sigma} \right)
\end{align*}
$$

正規分布は**再生性**（reproductive property）を持つ。すなわち、$X_1, X_2, \ldots, X_n$ が独立に $N(\mu_i, \sigma_i^2)$ に従うとき、$Y = \sum_{i=1}^n a_i X_i$ は $N\left(\sum_{i=1}^n a_i \mu_i, \sum_{i=1}^n a_i^2 \sigma_i^2\right)$ に従う。

