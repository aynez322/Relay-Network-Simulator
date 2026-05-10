from __future__ import annotations
from random import Random
from typing import Iterable, List, Optional
class GossipProtocol:
    name = "gossip"
    def __init__(
        self,
        k: int | None = 2,
        probability: float | None = None,
        adaptive: bool = False,
        min_k: int = 1,
        max_k: int = 4,
    ) -> None:
        if k is None and probability is None:
            raise ValueError("Either k or probability must be provided for Gossip.")
        self.k = k
        self.probability = probability
        self.adaptive = adaptive
        self.min_k = min_k
        self.max_k = max_k
    def choose_targets(
        self,
        neighbors: Iterable[int],
        rng: Random,
        previous_sender: Optional[int] = None,
        ttl: Optional[int] = None,
    ) -> List[int]:
        candidates = [n for n in neighbors if n != previous_sender]
        if not candidates:
            return []
        if self.k is not None:
            sample_size = self.k
            if self.adaptive and ttl is not None:
                sample_size = min(self.max_k, max(self.min_k, ttl // 2))
            sample_size = min(sample_size, len(candidates))
            return rng.sample(candidates, sample_size)
        assert self.probability is not None
        return [n for n in candidates if rng.random() <= self.probability]
