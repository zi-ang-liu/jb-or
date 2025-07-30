---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 経済的発注量

| 英語                    | 日本語       |
| ----------------------- | ------------ |
| Economic Order Quantity | 経済的発注量 |
| Deterministic           | 決定論的     |
| Constant                | 一定         |


記号を以下のように定義する。

| 記号  | 説明                   |
| :---: | :--------------------- |
|  $d$  | 単位時間あたりの需要量 |
|  $Q$  | 発注量                 |
|  $K$  | 発注費用               |
|  $h$  | 保管費用               |
|  $c$  | 購入単価               |
|  $T$  | サイクルの長さ         |

**経済的発注量**（EOQ: Economic Order Quantity）モデルは、最も基本的な在庫管理モデルの一つである。このモデルは、[Harris, (1913)](https://doi.org/10.1287/opre.38.6.947)によって提案された。


:::{code-cell} python
:tags: [remove-input, remove-output]
:tags: [remove-input]
!pip install matplotlib numpy
import matplotlib.pyplot as plt
import numpy as np
:::

## EOQモデル

EOQモデルは、単位時間あたりの需要量は決定論的で、一定であると仮定する。つまり、需要量は事前に分かっており、時間とともに変化しない。単位時間あたりの需要量は需要率（demand rate）と呼ばれ、記号 $d$ で表される。また、納期は0とし、発注から納品までの時間はないと仮定する。さらに、一回の発注量を $Q$ とし、一定であるとする。

在庫に関わるコストは、発注費用 $K$ 、保管費用 $h$ と、購入単価 $c$ がある。ここで、発注費用 $K$ は、発注を行うたびにかかる費用であり、固定費用(fixed cost)と呼ばれる。

EOQモデルの最適解は次の二つの性質を持つ[(Snyder & Shen, 2019)](https://doi.org/10.1002/9781119584445)：

1. Zero-inventory ordering (ZIO). 在庫量が0のときに発注を行う。納期は0であるため、在庫量が0でないときに発注すると、保管コストが発生する。
2. Constant order sizes. 発注量は一定である。需要率 $d$ が一定であり、在庫量が0のときに発注を行うため、最適発注量も一定である。

以上の性質から、在庫量の時間的変化は下図のようになる。



:::{code-cell} python
:tags: [remove-input]

# Parameters
d = 250  # Demand rate
Q = 500  # Order quantity
T = Q / d  # Cycle length
t = np.linspace(0, 3 * T, 1000)  # Time from 0 to 3 cycles

# Inventory level over time
inventory = np.maximum(0, Q - (d * t) % Q)
inventory[0] = 0

# Plotting the inventory level
plt.figure(figsize=(12, 6))
plt.plot(t, inventory, label="Inventory Level", color="black", linewidth=2)
plt.xlabel("Time", fontsize=14)
plt.ylabel("Inventory Level", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.axhline(0, color="gray", linewidth=1)
plt.ylim(bottom=0)
plt.tight_layout()
plt.show()
:::

発注の間隔を**サイクル**(cycle)と呼び、サイクルの長さは 

$$
T = \frac{Q}{d}
$$

で与えられる。

:::{prf:example}
:label: example:eoq_cycle

A社は、毎月250個の需要がある商品を取り扱っている。一回の発注量は500個とし、サイクルの長さは

$$
T = \frac{500}{250} = 2 \text{ヶ月}
$$

となる。
:::

## コスト

総コストは、発注コスト、保管コスト、購入コストの和である。ここでは、**1サイクルの総コストを考える**。

発注は1回だけ行うため、発注コストは $K$ である。



## 最適発注量



:::{prf:theorem} Economic Order Quantity
:label: theorem:eoq

EOQモデルにおいて、最適発注量 $Q^*$ は

$$
Q^* = \sqrt{\frac{2Kd}{h}}
$$

で与えられる。

:::

:::{prf:example}
:label: example:eoq

A example.

:::