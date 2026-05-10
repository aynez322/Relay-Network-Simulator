from __future__ import annotations
import math
from typing import Any
import networkx as nx
class TopologyBuilder:
    @staticmethod
    def create(topology_type: str, node_count: int, seed: int, **kwargs: Any) -> nx.Graph:
        topology_type = topology_type.lower()
        if topology_type == "random":
            p = float(kwargs.get("edge_probability", 0.08))
            graph = nx.gnp_random_graph(node_count, p, seed=seed)
        elif topology_type == "mesh":
            graph = nx.complete_graph(node_count)
        elif topology_type == "grid":
            side = math.ceil(math.sqrt(node_count))
            raw_graph = nx.grid_2d_graph(side, side)
            graph = nx.convert_node_labels_to_integers(raw_graph, ordering="default")
            if graph.number_of_nodes() > node_count:
                extra_nodes = list(range(node_count, graph.number_of_nodes()))
                graph.remove_nodes_from(extra_nodes)
        elif topology_type == "small_world":
            k = int(kwargs.get("k", 6))
            p = float(kwargs.get("rewire_probability", 0.2))
            if k >= node_count:
                k = max(2, node_count - 1)
            if k % 2 == 1:
                k += 1
            graph = nx.watts_strogatz_graph(node_count, k, p, seed=seed)
        else:
            raise ValueError(f"Unsupported topology type: {topology_type}")
        if not nx.is_connected(graph):
            largest = max(nx.connected_components(graph), key=len)
            graph = graph.subgraph(largest).copy()
            graph = nx.convert_node_labels_to_integers(graph, ordering="default")
        return graph
