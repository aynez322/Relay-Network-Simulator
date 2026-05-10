from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
@dataclass
class SimulationConfig:
    ttl: int = 8
    min_delay: float = 1.0
    max_delay: float = 2.0
    loss_rate: float = 0.0
    node_failure_rate: float = 0.0
    congestion_factor: float = 0.0
    probabilistic_flooding_p: float = 1.0
    seed: int = 42
@dataclass
class ExperimentConfig:
    seed: int = 42
    repeats: int = 5
    default_node_count: int = 100
    save_animation: bool = True
    base_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parents[1])
    @property
    def results_csv_dir(self) -> Path:
        return self.base_dir / "results" / "csv"
    @property
    def results_plots_dir(self) -> Path:
        return self.base_dir / "results" / "plots"
    @property
    def results_logs_dir(self) -> Path:
        return self.base_dir / "results" / "logs"
