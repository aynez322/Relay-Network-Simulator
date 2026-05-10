from __future__ import annotations
from random import Random
from typing import Iterable, List, Optional
class FloodingProtocol:
    name = "flooding"
    def __init__(self, forward_probability: float = 1.0) -> None:
        if not 0.0 <= forward_probability <= 1.0:
            raise ValueError("forward_probability must be in [0, 1].")
        self.forward_probability = forward_probability
    def choose_targets(
        self,
        neighbors: Iterable[int],
        rng: Optional[Random] = None,
        previous_sender: Optional[int] = None,
    ) -> List[int]:
        candidates = [n for n in neighbors if n != previous_sender]
        if self.forward_probability >= 1.0:
            return candidates
        if rng is None:
            raise ValueError("rng is required when using probabilistic flooding.")
        return [n for n in candidates if rng.random() <= self.forward_probability]
