from __future__ import annotations
from pathlib import Path
from random import Random
from typing import Dict
import pandas as pd
from config.settings import ExperimentConfig, SimulationConfig
from metrics.collector import MetricsCollector
from network.topology import TopologyBuilder
from protocols.flooding import FloodingProtocol
from protocols.gossip import GossipProtocol
from simulation.simulator import RelayNetworkSimulator
from visualization.animator import create_propagation_animation
from visualization.charts import ChartBuilder
from visualization.graph_drawer import draw_topology
def _run_single(
    protocol_name: str,
    topology: str,
    node_count: int,
    loss_rate: float,
    seed: int,
    topology_kwargs: Dict[str, float] | None = None,
) -> Dict[str, float]:
    topology_kwargs = topology_kwargs or {}
    graph = TopologyBuilder.create(topology, node_count=node_count, seed=seed, **topology_kwargs)
    protocol = FloodingProtocol() if protocol_name == "flooding" else GossipProtocol(k=2)
    sim_cfg = SimulationConfig(loss_rate=loss_rate, seed=seed)
    sim = RelayNetworkSimulator(graph=graph, protocol=protocol, config=sim_cfg)
    result = sim.run(source_id=0)
    record = {
        "protocol": protocol_name,
        "topology": topology,
        "node_count": float(graph.number_of_nodes()),
        "loss_rate": float(loss_rate),
    }
    record.update(result.metrics)
    return record
def _save_df(df: pd.DataFrame, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
def run_experiment1(cfg: ExperimentConfig) -> pd.DataFrame:
    collector = MetricsCollector()
    rng = Random(cfg.seed)
    topologies = ["random", "small_world"]
    for protocol_name in ("flooding", "gossip"):
        for topology in topologies:
            for _ in range(cfg.repeats):
                run_seed = rng.randint(0, 10_000_000)
                collector.add_record(
                    _run_single(
                        protocol_name=protocol_name,
                        topology=topology,
                        node_count=cfg.default_node_count,
                        loss_rate=0.0,
                        seed=run_seed,
                    )
                )
    df = collector.to_dataframe()
    _save_df(df, cfg.results_csv_dir / "experiment1_protocol_comparison.csv")
    ChartBuilder.protocol_comparison(
        df, "delivery_ratio", cfg.results_plots_dir / "experiment1_delivery_ratio.png", "Experiment 1: Delivery Ratio"
    )
    ChartBuilder.protocol_comparison(
        df,
        "network_overhead",
        cfg.results_plots_dir / "experiment1_overhead.png",
        "Experiment 1: Network Overhead",
    )
    sample_graph = TopologyBuilder.create("small_world", cfg.default_node_count, cfg.seed, k=6, rewire_probability=0.2)
    draw_topology(sample_graph, cfg.results_plots_dir / "experiment1_topology.png", "Small-World Topology")
    if cfg.save_animation:
        sample_sim = RelayNetworkSimulator(sample_graph, GossipProtocol(k=2), SimulationConfig(seed=cfg.seed))
        sample_result = sample_sim.run(source_id=0)
        create_propagation_animation(
            sample_result.graph,
            sample_result.event_log,
            cfg.results_plots_dir / "experiment1_dissemination.gif",
        )
    return df
def run_experiment2(cfg: ExperimentConfig) -> pd.DataFrame:
    collector = MetricsCollector()
    rng = Random(cfg.seed + 100)
    loss_values = [0.0, 0.1, 0.2, 0.5]
    for protocol_name in ("flooding", "gossip"):
        for loss in loss_values:
            for _ in range(cfg.repeats):
                run_seed = rng.randint(0, 10_000_000)
                collector.add_record(
                    _run_single(
                        protocol_name=protocol_name,
                        topology="small_world",
                        node_count=cfg.default_node_count,
                        loss_rate=loss,
                        seed=run_seed,
                    )
                )
    df = collector.to_dataframe()
    _save_df(df, cfg.results_csv_dir / "experiment2_packet_loss.csv")
    ChartBuilder.packet_loss_curve(
        df,
        "delivery_ratio",
        cfg.results_plots_dir / "experiment2_packet_loss_delivery.png",
        "Experiment 2: Delivery Ratio",
    )
    ChartBuilder.packet_loss_curve(
        df,
        "network_overhead",
        cfg.results_plots_dir / "experiment2_packet_loss_overhead.png",
        "Experiment 2: Network Overhead",
    )
    return df
def run_experiment3(cfg: ExperimentConfig) -> pd.DataFrame:
    collector = MetricsCollector()
    rng = Random(cfg.seed + 200)
    sizes = [50, 100, 500]
    for protocol_name in ("flooding", "gossip"):
        for size in sizes:
            for _ in range(max(2, cfg.repeats // 2)):
                run_seed = rng.randint(0, 10_000_000)
                collector.add_record(
                    _run_single(
                        protocol_name=protocol_name,
                        topology="random",
                        node_count=size,
                        loss_rate=0.1,
                        seed=run_seed,
                        topology_kwargs={"edge_probability": 0.05},
                    )
                )
    df = collector.to_dataframe()
    _save_df(df, cfg.results_csv_dir / "experiment3_scale.csv")
    ChartBuilder.grouped_bars(
        df,
        "node_count",
        "delivery_ratio",
        cfg.results_plots_dir / "experiment3_delivery_ratio.png",
        "Experiment 3: Delivery Ratio",
    )
    ChartBuilder.grouped_bars(
        df,
        "node_count",
        "total_transmissions",
        cfg.results_plots_dir / "experiment3_transmissions.png",
        "Experiment 3: Total Transmissions",
    )
    return df
def run_experiment4(cfg: ExperimentConfig) -> pd.DataFrame:
    collector = MetricsCollector()
    rng = Random(cfg.seed + 300)
    density_map = {"sparse": 0.03, "dense": 0.15}
    for protocol_name in ("flooding", "gossip"):
        for density_label, edge_probability in density_map.items():
            for _ in range(cfg.repeats):
                run_seed = rng.randint(0, 10_000_000)
                record = _run_single(
                    protocol_name=protocol_name,
                    topology="random",
                    node_count=cfg.default_node_count,
                    loss_rate=0.1,
                    seed=run_seed,
                    topology_kwargs={"edge_probability": edge_probability},
                )
                record["density_label"] = density_label
                collector.add_record(record)
    df = collector.to_dataframe()
    _save_df(df, cfg.results_csv_dir / "experiment4_density.csv")
    ChartBuilder.grouped_bars(
        df,
        "density_label",
        "delivery_ratio",
        cfg.results_plots_dir / "experiment4_delivery_ratio.png",
        "Experiment 4: Delivery Ratio",
    )
    ChartBuilder.grouped_bars(
        df,
        "density_label",
        "network_overhead",
        cfg.results_plots_dir / "experiment4_overhead.png",
        "Experiment 4: Network Overhead",
    )
    return df
