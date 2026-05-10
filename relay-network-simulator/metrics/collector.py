from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
import pandas as pd
@dataclass
class MetricsCollector:
    records: List[Dict[str, float]] = field(default_factory=list)
    def add_record(self, record: Dict[str, float]) -> None:
        self.records.append(record)
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.records)
