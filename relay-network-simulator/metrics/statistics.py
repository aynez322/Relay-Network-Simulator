from __future__ import annotations
from typing import Iterable
import numpy as np
import pandas as pd
def safe_mean(values: Iterable[float]) -> float:
    arr = np.array(list(values), dtype=float)
    return float(arr.mean()) if arr.size else 0.0
def summarize_by(df: pd.DataFrame, group_cols: list[str], metric_cols: list[str]) -> pd.DataFrame:
    if df.empty:
        return df
    grouped = df.groupby(group_cols, as_index=False)[metric_cols].mean()
    return grouped.sort_values(group_cols).reset_index(drop=True)
