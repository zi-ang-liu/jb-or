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
!pip install pydot graphviz
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

プロジェクトは、次の要素で構成される。

- 作業（Activity）：プロジェクトを構成する仕事。活動、アクティビティとも呼ばれる。
- 先行関係（Precedence Relationship）：それぞれの作業の先行作業を定義する関係。
- 作業時間：各作業に必要な時間。通常、確率変数として与えられる。

## プロジェクト・ネットワーク

プロジェクトを表現するネットワークを**プロジェクト・ネットワーク**（Project Network）と呼ぶ。プロジェクト・ネットワークには、**AOA**（Activity on Arrow）や **AON**（Activity on Node）という 2 種類の表現方法がある。

AOA では、作業を辺で表現し、先行関係をノードで表現する。AON では、作業を頂点（node）で表現し、先行関係を辺（edge）で表現する。日本の教科書では AOA が一般的であるが、AON のほうが理解と作成が容易であるため、海外の教科書では AON が一般的で、実務でも AON がよく使われる[@Camm2022-zv; @Hillier2025-cb; @Eiselt2022-qy]。これ以降の説明では、AON を用いる。

:::{prf:example}
:label: example:pert_1

学生の田中さんと佐藤さんが協力し、ある授業のレポートを作成することになった。このレポートを作成するためには、下の表に示すように、いくつかの作業を行う必要がある。

| 作業 | 作業内容     | 先行作業 | 時間（日） |
| ---- | ------------ | -------- | ---------- |
| A    | 課題の理解   | -        | 2          |
| B    | データ収集   | A        | 3          |
| C    | データ分析   | B        | 4          |
| D    | 文献調査     | A        | 2          |
| E    | レポート作成 | C, D     | 5          |

このプロジェクトを表現するプロジェクト・ネットワークは次の図のようになる。

:::{code-cell} python
:tags: [remove-input]

class ProjectNetwork:
    def __init__(self, tasks):
        self.tasks = tasks
        self.G = nx.DiGraph()
        self._create_graph()

    def _create_graph(self):
        # Add tasks
        for task_id, task in self.tasks.items():
            self.G.add_node(
                task_id, label=f"{task_id}\n({task['duration']})"
            )

        # Add Start and Finish nodes
        self.G.add_node("Start", label="Start")
        self.G.add_node("Finish", label="Finish")

        # Add edges for precedence
        for task_id, task in self.tasks.items():
            if not task["predecessors"]:  # no predecessors → connect from Start
                self.G.add_edge("Start", task_id)
            else:
                for pred in task["predecessors"]:
                    self.G.add_edge(pred, task_id)

        # Add Finish connections (tasks with no successors → to Finish)
        for task_id in self.tasks:
            if self.G.out_degree(task_id) == 0:  # no outgoing edges
                self.G.add_edge(task_id, "Finish")

    def draw(self):
        # Graphviz layout (top-to-bottom)
        pos = graphviz_layout(self.G, prog="dot")

        # Draw the graph
        plt.figure(figsize=(10, 10))
        nx.draw(
            self.G,
            pos,
            with_labels=False,
            node_size=2000,
            node_color="lightyellow",
            edgecolors="black",
            arrows=True,
            arrowsize=20,
        )
        nx.draw_networkx_labels(
            self.G, pos, labels=nx.get_node_attributes(self.G, "label"), font_size=10
        )

        plt.title("Project Network Diagram")
        plt.axis("off")
        plt.show()

tasks = {
    "A": {"name": "課題の理解", "predecessors": [], "duration": 2},
    "B": {"name": "データ収集", "predecessors": ["A"], "duration": 3},
    "C": {"name": "データ分析", "predecessors": ["B"], "duration": 4},
    "D": {"name": "文献調査", "predecessors": ["A"], "duration": 2},
    "E": {"name": "レポート作成", "predecessors": ["C", "D"], "duration": 5},
}

project_network = ProjectNetwork(tasks)
project_network.draw()
:::

グラフ理論において、**有向非巡回グラフ**（Directed Acyclic Graph, DAG）とは、閉路を含まない有向グラフのことを指す。
プロジェクト・ネットワークは辺の向きがあるため、有向グラフであり、作業の先行関係は循環しないため、閉路を含まない。したがって、プロジェクト・ネットワークは DAG である。

作業リストに示す作業に加えて、プロジェクト・ネットワークには、**始点**（Start Node）と**終点**（Finish Node）が含まれる。始点は、先行作業を持たない作業から接続される。終点は、後続作業を持たない作業から接続される。上の例では、先行作業を持たない作業は A であり、後続作業を持たない作業は E であるため、始点から A に接続され、E から終点に接続されている。

:::{prf:example}
:label: example:pert_2

以下の作業リストに基づいて、プロジェクト・ネットワークを作成せよ。

| 作業 | 先行作業 | 時間（日） |
| ---- | -------- | ---------- |
| A    | -        | 2          |
| B    | -        | 4          |
| C    | A, B     | 4          |
| D    | C        | 6          |
| E    | C        | 5          |
| F    | E        | 5          |
| G    | D        | 6          |
| H    | E, G     | 9          |
| I    | C        | 8          |
| J    | F, I     | 7          |
| K    | J        | 4          |
| L    | J        | 6          |
| M    | H        | 2          |
| N    | K, L     | 6          |

先行作業がない作業は A と B であり、後続作業がない作業は M と N であるため、始点から A と B に接続され、M と N から終点に接続される。

:::{code-cell} python
:tags: [remove-input]

tasks = {
    "A": {"name": "", "predecessors": [], "duration": 2},
    "B": {"name": "", "predecessors": [], "duration": 4},
    "C": {"name": "", "predecessors": ["A", "B"], "duration": 4},
    "D": {"name": "", "predecessors": ["C"], "duration": 6},
    "E": {"name": "", "predecessors": ["C"], "duration": 5},
    "F": {"name": "", "predecessors": ["E"], "duration": 5},
    "G": {"name": "", "predecessors": ["D"], "duration": 6},
    "H": {"name": "", "predecessors": ["E", "G"], "duration": 9},
    "I": {"name": "", "predecessors": ["C"], "duration": 8},
    "J": {"name": "", "predecessors": ["F", "I"], "duration": 7},
    "K": {"name": "", "predecessors": ["J"], "duration": 4},
    "L": {"name": "", "predecessors": ["J"], "duration": 6},
    "M": {"name": "", "predecessors": ["H"], "duration": 2},
    "N": {"name": "", "predecessors": ["K", "L"], "duration": 6},
}

project_network = ProjectNetwork(tasks)
project_network.draw()
:::

## クリティカルパス

プロジェクト・ネットワークにおいて、始点から終点までの経路を**パス**（path）と呼ぶ。