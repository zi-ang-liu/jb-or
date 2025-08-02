# Wagner-Whitin モデル

| 記号          | 意味                                            |
| ------------- | ----------------------------------------------- |
| $\mathcal{T}$ | 期間の集合、$\mathcal{T} = \{1, 2, \ldots, T\}$ |
| $K$           | 1回あたりの発注費用                             |
| $h$           | 単位あたりの保管費用                            |
| $d_t$         | 第 $t$ 期の需要量                               |
| $q_t$         | 第 $t$ 期の発注量                               |
| $x_t$         | 第 $t$ 期の在庫量                               |
| $y_t$         | 第 $t$ 期に発注する場合は 1、しない場合は 0     |
| $M$           | 非負の大きな数                                  |

Wagner-Whitin モデルは次のように定式化される。

$$
\begin{align*}
\text{minimize} \quad & \sum_{t=1}^{T} (K y_t + h x_t) \\
\text{subject to} \quad & x_t = x_{t-1} + q_t - d_t \quad & \forall t \in \mathcal{T} \\
& q_t \geq 0 \quad & \forall t \in \mathcal{T} \\
& q_t \leq M y_t \quad & \forall t \in \mathcal{T} \\
& x_t \geq 0 \quad & \forall t \in \mathcal{T} \\
& y_t \in \{0, 1\} \quad & \forall t \in \mathcal{T}
\end{align*}  
$$

