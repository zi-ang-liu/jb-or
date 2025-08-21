---
title: PERT/CPM
bibliography:
  - references.bib
kernelspec:
  name: python3
  display_name: 'Python 3'
---

:::{code-cell} python
:tags: [remove-input, remove-output]
!pip install matplotlib numpy networkx
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout 
:::

- Camm et al. (2022) Chapter 9
- Taha (2016) Chapter 6
- Hillier and Lieberman (2020) Chapter 22
- Eiselt and Sandblom (2019) Chapter 8
  
**PERT**（Program Evaluation and Review Technique）
**CPM**（Critical Path Method）

ある作業の開始前に完了しなければならない作業を**先行作業**（Immediate Predecessor）と呼ぶ。

プロジェクト
- 作業（Activity）：プロジェクトを構成する仕事。活動、アクティビティとも呼ばれる。
- 先行関係（Precedence Relationship）：それぞれの作業の先行作業を定義する関係。
- 作業時間：各作業に必要な時間。通常、確率変数として与えられる。

プロジェクトを表現するネットワークを**プロジェクト・ネットワーク**（Project Network）と呼ぶ。プロジェクト・ネットワークには、**AOA**（Activity on Arrow）や **AON**（Activity on Node）という 2 種類の表現方法がある。

AOA では、作業を辺で表現し、先行関係をノードで表現する。AON では、作業を頂点（node）で表現し、先行関係は辺（edge）で表現する。日本の教科書では AOA が一般的であるが、AON のほうが理解と作成が容易であるため、海外の教科書では AON が一般的で、実務でも AON がよく使われる[@Camm2022-zv; @Hillier2025-cb; @Eiselt2022-qy]。これ以降の説明では、AON を用いる。

:::{prf:example}
:label: example:pert_1

学生の田中さんと佐藤さんが協力し、ある授業のレポートを作成することになった。このレポートを作成するためには、下の表に示すように、いくつかの作業を行う必要がある。

|作業|作業内容|先行作業|時間（日）|
|----|--------|--------|--------|
|A   |課題の理解|なし     |2       |
|B   |データ収集|A       |3       |
|C   |データ分析|B       |4       |
|D   |文献調査|A       |2       |
|E   |レポート作成|C, D   |5       |



:::{code-cell} python
:tags: [remove-input]

# Define the tasks
tasks = {
    "A": {"name": "課題の理解", "predecessors": [], "duration": 2},
    "B": {"name": "データ収集", "predecessors": ["A"], "duration": 3},
    "C": {"name": "データ分析", "predecessors": ["B"], "duration": 4},
    "D": {"name": "文献調査", "predecessors": ["A"], "duration": 2},
    "E": {"name": "レポート作成", "predecessors": ["C", "D"], "duration": 5},
}

# Create a directed graph
G = nx.DiGraph()

# Add tasks
for task_id, task in tasks.items():
    G.add_node(task_id, label=f"{task_id}")

# Add Start and Finish nodes
G.add_node("Start", label="Start")
G.add_node("Finish", label="Finish")

# Add edges for precedence
for task_id, task in tasks.items():
    if not task["predecessors"]:  # no predecessors → connect from Start
        G.add_edge("Start", task_id)
    else:
        for pred in task["predecessors"]:
            G.add_edge(pred, task_id)

# Add Finish connections (tasks with no successors → to Finish)
for task_id in tasks:
    if G.out_degree(task_id) == 0:  # no outgoing edges
        G.add_edge(task_id, "Finish")

# Graphviz layout (top-to-bottom)
pos = graphviz_layout(G, prog="dot")

# Draw the graph
plt.figure(figsize=(3, 5))
nx.draw(G, pos, with_labels=False, node_size=1000, node_color="lightyellow", edgecolors="black", arrows=True, arrowsize=20)
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, "label"), font_size=10)

plt.title("Project Network Diagram")
plt.axis("off")
plt.show()

:::



