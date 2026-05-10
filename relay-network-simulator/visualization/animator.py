from __future__ import annotations
from pathlib import Path
from typing import List, Tuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import networkx as nx
def create_propagation_animation(
    graph: nx.Graph,
    event_log: List[Tuple[float, int, int]],
    output_path: Path,
) -> None:
    if not event_log:
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sorted_events = sorted(event_log, key=lambda x: x[0])
    pos = nx.spring_layout(graph, seed=42)
    fig, ax = plt.subplots(figsize=(9, 7))
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="lightgray", alpha=0.5)
    nodes = nx.draw_networkx_nodes(graph, pos, ax=ax, node_size=120, node_color="lightblue")
    ax.set_title("Message Dissemination Animation")
    ax.set_axis_off()
    active_nodes: set[int] = set()
    def update(frame: int) -> None:
        _, sender, receiver = sorted_events[frame]
        active_nodes.add(sender)
        active_nodes.add(receiver)
        colors = ["tomato" if n in active_nodes else "lightblue" for n in graph.nodes()]
        nodes.set_color(colors)
        ax.set_title(f"Message Dissemination Step {frame + 1}/{len(sorted_events)}")
    anim = FuncAnimation(fig, update, frames=len(sorted_events), interval=250, repeat=False)
    anim.save(output_path, writer=PillowWriter(fps=4))
    plt.close(fig)
