from __future__ import annotations
from random import Random
class PacketLossModel:
    def __init__(self, loss_rate: float, seed: int) -> None:
        if not 0.0 <= loss_rate <= 1.0:
            raise ValueError("loss_rate must be in [0, 1].")
        self.loss_rate = loss_rate
        self.rng = Random(seed)
    def is_lost(self) -> bool:
        return self.rng.random() < self.loss_rate
