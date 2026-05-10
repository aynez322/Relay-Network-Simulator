from __future__ import annotations
from dataclasses import dataclass
from random import Random
from typing import Any, Dict, List, Optional, Protocol
import uuid
import networkx as nx
from config.settings import SimulationConfig
from network.message import Message
from network.node import Node
from simulation.packet_loss import PacketLossModel
from simulation.scheduler import EventScheduler
class ProtocolStrategy(Protocol):
    name: str
    def choose_targets(self, neighbors: List[int], *args: Any, **kwargs: Any) -> List[int]:
        ...
@dataclass
class SimulationResult:
    metrics: Dict[str, float]
    event_log: List[tuple[float, int, int]]
    graph: nx.Graph
class RelayNetworkSimulator:
    def __init__(
        self,
        graph: nx.Graph,
        protocol: ProtocolStrategy,
        config: SimulationConfig,
    ) -> None:
        self.graph = graph
        self.protocol = protocol
        self.config = config
        self.rng = Random(config.seed)
        self.loss_model = PacketLossModel(config.loss_rate, config.seed + 17)
        self.nodes = self._build_nodes(graph)
        self.failed_nodes: set[int] = set()
        self.scheduler = EventScheduler()
        self.event_log: List[tuple[float, int, int]] = []
        self.reset_counters()
    def _build_nodes(self, graph: nx.Graph) -> Dict[int, Node]:
        nodes: Dict[int, Node] = {}
        for node_id in graph.nodes:
            node = Node(node_id=node_id)
            node.set_neighbors(graph.neighbors(node_id))
            nodes[node_id] = node
        return nodes
    def reset_counters(self) -> None:
        self.total_transmissions = 0
        self.successful_transmissions = 0
        self.redundant_messages = 0
        self.dropped_packets = 0
        self.first_hops: List[int] = []
        self.first_delays: List[float] = []
        self.received_nodes: set[int] = set()
        self.event_log = []
        self.scheduler = EventScheduler()
    def _sample_delay(self) -> float:
        base = self.rng.uniform(self.config.min_delay, self.config.max_delay)
        queue_pressure = self.scheduler.queue_length / max(self.graph.number_of_nodes(), 1)
        return base * (1.0 + self.config.congestion_factor * queue_pressure)
    def _schedule_transmission(self, sender: int, receiver: int, message: Message, now: float) -> None:
        if sender in self.failed_nodes or receiver in self.failed_nodes:
            self.dropped_packets += 1
            return
        self.total_transmissions += 1
        self.nodes[sender].stats.sent += 1
        arrival = now + self._sample_delay()
        self.scheduler.schedule(arrival, self._deliver_message, sender, receiver, message, arrival)
        self.event_log.append((arrival, sender, receiver))
    def _choose_targets(self, node_id: int, previous_sender: Optional[int]) -> List[int]:
        neighbors = list(self.nodes[node_id].neighbors)
        if self.protocol.name == "flooding":
            return self.protocol.choose_targets(neighbors, rng=self.rng, previous_sender=previous_sender)
        return self.protocol.choose_targets(neighbors, self.rng, previous_sender=previous_sender)
    def _deliver_message(self, sender: int, receiver: int, message: Message, now: float) -> None:
        if receiver in self.failed_nodes:
            self.dropped_packets += 1
            return
        if self.loss_model.is_lost():
            self.dropped_packets += 1
            self.nodes[receiver].stats.dropped_incoming += 1
            return
        receiver_node = self.nodes[receiver]
        is_new = receiver_node.receive(message, now)
        if not is_new:
            self.redundant_messages += 1
            return
        self.successful_transmissions += 1
        self.received_nodes.add(receiver)
        self.first_hops.append(message.hop_count)
        self.first_delays.append(now - message.timestamp)
        if message.ttl <= 1:
            return
        forwarded = message.forward_copy()
        if self.protocol.name == "gossip":
            targets = self.protocol.choose_targets(
                list(self.nodes[receiver].neighbors),
                self.rng,
                previous_sender=sender,
                ttl=forwarded.ttl,
            )
        else:
            targets = self._choose_targets(receiver, previous_sender=sender)
        for target in targets:
            self._schedule_transmission(receiver, target, forwarded, now)
    def run(self, source_id: int = 0, message_id: Optional[str] = None, ttl: Optional[int] = None) -> SimulationResult:
        self.reset_counters()
        self.failed_nodes = set()
        for node_id in self.graph.nodes:
            if node_id != source_id and self.rng.random() < self.config.node_failure_rate:
                self.failed_nodes.add(node_id)
        message_id = message_id or str(uuid.uuid4())
        msg = Message(
            message_id=message_id,
            source_id=source_id,
            timestamp=0.0,
            ttl=ttl if ttl is not None else self.config.ttl,
            hop_count=0,
        )
        source_node = self.nodes[source_id]
        source_node.receive(msg, now=0.0)
        self.received_nodes.add(source_id)
        self.first_hops.append(0)
        self.first_delays.append(0.0)
        initial_targets = self._choose_targets(source_id, previous_sender=None)
        for target in initial_targets:
            self._schedule_transmission(source_id, target, msg.forward_copy(), now=0.0)
        self.scheduler.run()
        metrics = self._collect_metrics()
        return SimulationResult(metrics=metrics, event_log=self.event_log, graph=self.graph)
    def _collect_metrics(self) -> Dict[str, float]:
        total_nodes = self.graph.number_of_nodes()
        unique_receivers = len(self.received_nodes)
        delivery_ratio = unique_receivers / total_nodes if total_nodes else 0.0
        avg_hop = sum(self.first_hops) / len(self.first_hops) if self.first_hops else 0.0
        avg_delay = sum(self.first_delays) / len(self.first_delays) if self.first_delays else 0.0
        overhead = self.total_transmissions / max(unique_receivers - 1, 1)
        loss_impact = self.dropped_packets / self.total_transmissions if self.total_transmissions else 0.0
        return {
            "delivery_ratio": delivery_ratio,
            "total_transmissions": float(self.total_transmissions),
            "redundant_messages": float(self.redundant_messages),
            "avg_hop": avg_hop,
            "avg_delay": avg_delay,
            "network_overhead": overhead,
            "loss_impact": loss_impact,
            "unique_receivers": float(unique_receivers),
            "dropped_packets": float(self.dropped_packets),
            "successful_transmissions": float(self.successful_transmissions),
        }
