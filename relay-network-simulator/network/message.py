from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class Message:
    message_id: str
    source_id: int
    timestamp: float
    ttl: int
    hop_count: int = 0
    def forward_copy(self) -> "Message":
        return Message(
            message_id=self.message_id,
            source_id=self.source_id,
            timestamp=self.timestamp,
            ttl=self.ttl - 1,
            hop_count=self.hop_count + 1,
        )
