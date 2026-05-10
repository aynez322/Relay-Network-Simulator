from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
def draw_topology(graph: nx.Graph, output_path: Path, title: str = "Network Topology") -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9, 7))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw_networkx(
        graph,
        pos=pos,
        node_size=120,
        with_labels=False,
        edge_color="gray",
        node_color="steelblue",
        alpha=0.9,
    )
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
