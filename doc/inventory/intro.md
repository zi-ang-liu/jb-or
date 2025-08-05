---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

:::{code-cell} python
:tags: [remove-input, remove-output]
!pip install matplotlib numpy
import matplotlib.pyplot as plt
import numpy as np
:::

# 在庫管理とは

## 在庫モデルの分類

需要（demand）
: 需要が**決定論的** (Deterministic) か**確率的** (Stochastic) か。

観測（review）
: 在庫量を**連続観測** (Continuous Review) するか、**周期観測** (Periodic Review) するか。連続観測の場合、在庫量が連続的に観測でき、いつでも発注が可能である。周期観測の場合、一定の期間（例えば1週間）ごとに在庫量を観測する。

リードタイム（lead time）
: 発注から納品までの期間。調達期間とも呼ばれる。リードタイムが**決定論的**か**確率的** か。また、リードタイムが0かどうか。

バックオーダー（backorder）
: バックオーダーが許容されるかどうか。

計画期間（planning horizon）
: 単一期間 (Single Period) か、複数期間 (Multi Period) か、無限 (Infinite) か。

## 在庫の費用

在庫管理の目的は、在庫に関わる費用を最小化する（あるいは、利益を最大化する）ことである。ここでは、在庫に関わる費用を紹介する。

保管費用（holding cost）
: 在庫を保管するためにかかる倉庫費用、保険費用、税金、機会費用など。通常、単位時間あたりの1単位あたりの保管費用を $h$ とする。

:::{code-cell} python
:tags: [remove-input]

# Parameters
d = 250  # Demand rate
Q = 500  # Order quantity
T = Q / d  # Cycle length
t = np.linspace(0, 2.999 * T, 1000) 

# Inventory level over time
inventory = np.maximum(0, Q - (d * t) % Q)

# Plotting the inventory level
plt.figure(figsize=(12, 6))
plt.fill_between(t, inventory, color="lightgray", alpha=0.5, label="Inventory Level")
plt.plot(t, inventory, label="Inventory Level", color="black", linewidth=2)
plt.xlabel("Time", fontsize=14)
plt.ylabel("Inventory Level", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.axhline(0, color="gray", linewidth=1)
plt.ylim(bottom=0, top=Q + 200)
plt.xlim(0, 3.5 * T)
plt.tight_layout()
plt.show()
:::

発注費用（ordering cost）
: 発注量に関わらず、1回の発注にかかる費用。調達費用、固定費用（fixed cost）などとも呼ばれる。通常、1回の発注にかかる費用を $K$ とする。

購入費用（purchase cost）
: 商品を購入するためにかかる費用。通常、単位あたりの購入費用を $c$ とする。

欠品費用（stockout cost）
: 需要が在庫を上回った場合に発生する費用。通常、単位あたりの欠品費用を $p$ とする。

## Note

- [在庫最適化と安全在庫配置システム MESSA (MEta Safety Stock Allocation system)](https://scmopt.github.io/manual/03inventory.html)
- [Snyder (2023)](https://doi.org/10.1287/educ.2023.0256)はStockpylという在庫最適化とシミュレーションのためのPythonライブラリを開発した。

https://orsj.org/wp-content/or-archives50/pdf/bul/Vol.30_11_673.pdf
