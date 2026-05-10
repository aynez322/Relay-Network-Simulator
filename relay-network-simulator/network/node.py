from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Iterable, Set
from network.message import Message
@dataclass
class NodeStats:
    sent: int = 0
    received_unique: int = 0
    duplicates: int = 0
    dropped_incoming: int = 0
@dataclass
class Node:
    node_id: int
    neighbors: Set[int] = field(default_factory=set)
    received_messages: Dict[str, Message] = field(default_factory=dict)
    first_receive_time: Dict[str, float] = field(default_factory=dict)
    stats: NodeStats = field(default_factory=NodeStats)
    def set_neighbors(self, neighbors: Iterable[int]) -> None:
        self.neighbors = set(neighbors)
    def has_message(self, message_id: str) -> bool:
        return message_id in self.received_messages
    def receive(self, message: Message, now: float) -> bool:
        if self.has_message(message.message_id):
            self.stats.duplicates += 1
            return False
        self.received_messages[message.message_id] = message
        self.first_receive_time[message.message_id] = now
        self.stats.received_unique += 1
        return True
