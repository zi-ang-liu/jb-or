import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout 

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
    G.add_node(task_id, label=f"{task_id}: {task['name']}\n({task['duration']}日)")

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
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=False, node_size=2500, node_color="lightyellow", edgecolors="black", arrows=True, arrowsize=20)
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, "label"), font_size=10)

plt.title("Project Network Diagram (PERT/CPM style)")
plt.axis("off")
plt.show()
