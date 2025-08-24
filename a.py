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
        plt.figure(figsize=(10, 6))
        nx.draw(
            self.G,
            pos,
            with_labels=False,
            node_size=2500,
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

# | 作業 | 先行作業 | 時間（日） |
# | ---- | -------- | ---------- |
# | A    | -        | 2          |
# | B    | -        | 4          |
# | C    | A, B     | 4          |
# | D    | C        | 6          |
# | E    | C        | 5          |
# | F    | E        | 5          |
# | G    | D        | 6          |
# | H    | E, G     | 9          |
# | I    | C        | 8          |
# | J    | F, I     | 7          |
# | K    | J        | 4          |
# | L    | J        | 6          |
# | M    | H        | 2          |
# | N    | K, L     | 6          |

tasks = {
    "A": {"name": " ", "predecessors": [], "duration": 2},
    "B": {"name": " ", "predecessors": [], "duration": 4},
    "C": {"name": "", "predecessors": ["A", "B"]