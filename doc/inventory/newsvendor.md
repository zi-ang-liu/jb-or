# 新聞売り子問題

新聞売り子問題（Newsvendor Problem）は、古典的な確率的在庫モデルの一つである。

[Arrow et al. (1951)](https://doi.org/10.2307/1906813)
[Chen et al. (2016)](https://doi.org/10.1111/deci.12215) は新聞売り子問題の最新研究をレビューしている。最近では、データ駆動新聞売り子問題（Data-Driven Newsvendor Problem）に関する研究が行われている。

新聞売り子が毎日新聞を仕入れ、販売する問題を考える。新聞 1 部の仕入れ価格を $c$、販売価格を $r$、残存価額を $v$、欠品費用を $p$、保管費用を $h$ とする。

- $r > c$. 販売価格は仕入れ価格より高い。
- $r > v$. 販売価格は残存価値より高い。

新聞の需要 $D$ は正規分布 $N(\mu, \sigma^2)$ に従い、$\mu$ と $\sigma$ は既知である。新聞売り子はどれだけの新聞を仕入れればよいか。

## 定式化

ある日、新聞売り子が $S$ 部の新聞を仕入れ、需要 $D$ が $d$ であったとする。このとき、新聞売り子の利益は以下のように表される。

$$
\pi(S, d) = r \min\{d, S\} - cS + v \max\{0, S - d\} \\
- h \max\{0, S - d\} - p \max\{0, d - S\}
$$

第一項は販売利益、第二項は仕入れコスト、第三項は残存価値、第四項は保管コスト、第五項は欠品コストである。

以下は、$\max\{0, x\} = x^+$ を用いて書き換えた形である。整理すると、利益は以下のように表される。

$$
\pi(S, d) = r \min\{d, S\} - cS + (v - h) (S - d)^+ - p (d - S)^+
$$

第一項を以下のように書き換えることができる。

$$
r \min\{d, S\} = r d - r (d - S)^+
$$

:::{note}
- $d < S$ の場合、$r \min\{d, S\} = r d$ となる。
- $d >= S$ の場合、$r \min\{d, S\} = r d - r(d - S) = r S$ となる。
:::

したがって、利益は以下のように書き換えられる。

$$
\pi(S, d) = r d - cS + (v- h) (S - d)^+ - (p + r) (d - S)^+
$$

利益の最大化は、コストの最小化に帰着される。したがって、コスト関数 $g(S, d) = -\pi(S, d)$ は以下のように表される。

$$
g(S, d) = cS - rd + (h - v) (S - d)^+ + (p + r) (d - S)^+
$$

$D$ が確率変数であるため、コストの期待値 $g(S)$ は以下のように表される。

$$
\begin{align*}
g(S) &= \mathbb{E}[g(S, D)] \\
&= \int_{0}^{\infty} g(S, d) f_D(d) dd \\
&= cS - r\mathbb{E}[D] + (h - v) \mathbb{E}[(S - D)^+] + (p + r) \mathbb{E}[(D - S)^+] \\
&= c S - r \mu + (h - v)  \int_{0}^{\infty}(S - d)^+ f_D(d) dd + (p + r) \int_{0}^{\infty} (d - S)^+ f_D(d) dd \\
&= c S - r \mu + (h - v) \int_{0}^{S} (S - d) f_D(d) dd + (p + r) \int_{S}^{\infty} (d - S) f_D(d) dd
\end{align*}
$$

## 最適化

$g(S)$ の1階微分は以下のように求める。

$$
\begin{align*}
\frac{dg(S)}{dS} &= c + (h - v) F_D(S) - (p + r) (1 - F_D(S)) \\
\end{align*}
$$

よって、$dg(S)/dS = 0$ から、

$$
\begin{align*}
c + (h - v) F_D(S) - (p + r) (1 - F_D(S)) &= 0 \\
F_D(S) &= \frac{p + r - c}{h + p + r - v}
\end{align*}
$$

になる。2 階微分は

$$
\begin{align*}
\frac{d^2g(S)}{dS^2} &= (h - v) f_D(S) + (p + r) f_D(S) \\
&= (h - v + p + r) f_D(S) 
\end{align*}
$$

である。したがって、コスト関数 $g(S)$ は凸関数であり、1 階微分が 0 になる点は最小値を与える。

コスト関数 $g(S)$ を最小化するための最適発注量 $S^*$ は以下のように表される。

$$
S^* = F_D^{-1}\left(\frac{p + r - c}{h + p + r - v}\right)
$$

ここで、$F_D^{-1}$ は需要 $D$ の累積分布関数の逆関数である。

## 臨界率

新聞売り子問題において、より一般的に、在庫超過費用（overage cost）と 在庫不足費用（underage cost）を考慮する。

$$
C_o = h + c - v, \quad C_u = p + r - c
$$

在庫超過費用 $C_o$ は、在庫が余ったときのコストである。1 部の在庫超過に対し、保管コストと仕入れコストが発生するが、残存価額が得られないため、$C_o = h + c - v$ となる。

在庫不足費用 $C_u$ は、在庫が不足したときのコストである。1 部の在庫不足に対し、欠品コスト $p$ と失われた販売機会の利益 $r - c$ が発生するため、$C_u = p + r - c$ となる。

従って、

$$
\begin{align*}
S^* &= F_D^{-1}\left(\frac{p + r - c}{h + p + r - v}\right)\\
&= F_D^{-1}\left(\frac{C_u}{C_o + C_u}\right)
\end{align*}
$$

が得られる。

:::{prf:theorem} Newsvendor Problem
:label: theorem:newsvendor

新聞売り子問題における最適発注量 $S^*$ は、

$$
S^* = F_D^{-1}\left(\frac{C_u}{C_o + C_u}\right)
$$

で与えられる。
:::

$C_u/(C_o + C_u)$ は**臨界率**（critical ratio）と呼ばれる。臨界率は、在庫不足費用と在庫超過費用の比率を表す。

ここで、$F_D(S) = P(D \leq S)$ は欠品が発生しない確率を表す。この確率のことは**サービスレベル**（service level）と呼ぶ。したがって、最適発注量 $S^*$ を用いることは、サービスレベルを $C_u/(C_o + C_u)$ に等しくすることを意味する。$1 - C_u/(C_o + C_u) = C_o/(C_o + C_u)$ の確率で欠品が発生することが最適である。

:::{prf:observation}
:label: observation:newsvendor_ratio
- 在庫不足費用 $C_u$ の増加に伴い、サービスレベルと最適発注量 $S^*$ は増加する。
- 在庫超過費用 $C_o$ の増加に伴い、サービスレベルと最適発注量 $S^*$ は減少する。
:::

:::{prf:example}
:label: example:news_1

需要 $D$ が正規分布 $N(100, 25)$ に従う新聞売り子問題を考える。在庫超過費用が $C_o = 10$、在庫不足費用が $C_u = 40$ のとき、最適発注量 $S^*$ を求める。

$$
S^* = F_D^{-1}\left(\frac{C_u}{C_o + C_u}\right) = F_D^{-1}\left(\frac{40}{10 + 40}\right) = F_D^{-1}\left(0.8\right)
$$

ここで、$F_D^{-1}$ は需要 $D$ の累積分布関数の逆関数である。Python では、SciPy ライブラリの `ppf()` 関数を用いて、逆関数を求めることができる。

```python
from scipy.stats import norm

# 正規分布のパラメータ
mu = 100
sigma = 5

# 在庫超過費用と在庫不足費用
C_o = 10
C_u = 40

# 臨界率
critical_ratio = C_u / (C_o + C_u)

# 最適発注量
S_star = norm.ppf(critical_ratio, loc=mu, scale=sigma)
```
:::