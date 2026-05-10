from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
class ChartBuilder:
    @staticmethod
    def protocol_comparison(df: pd.DataFrame, metric: str, output: Path, title: str) -> None:
        output.parent.mkdir(parents=True, exist_ok=True)
        grouped = df.groupby("protocol", as_index=False)[metric].mean()
        plt.figure(figsize=(7, 5))
        plt.bar(grouped["protocol"], grouped[metric], color=["#4C78A8", "#F58518"])
        plt.title(title)
        plt.ylabel(metric.replace("_", " ").title())
        plt.tight_layout()
        plt.savefig(output, dpi=220)
        plt.close()
    @staticmethod
    def packet_loss_curve(df: pd.DataFrame, metric: str, output: Path, title: str) -> None:
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.figure(figsize=(8, 5))
        grouped = df.groupby(["protocol", "loss_rate"], as_index=False)[metric].mean()
        for protocol in grouped["protocol"].unique():
            part = grouped[grouped["protocol"] == protocol]
            plt.plot(part["loss_rate"], part[metric], marker="o", label=protocol)
        plt.xlabel("Packet Loss Rate")
        plt.ylabel(metric.replace("_", " ").title())
        plt.title(title)
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(output, dpi=220)
        plt.close()
    @staticmethod
    def grouped_bars(
        df: pd.DataFrame,
        x_col: str,
        metric: str,
        output: Path,
        title: str,
    ) -> None:
        output.parent.mkdir(parents=True, exist_ok=True)
        pivot = df.groupby([x_col, "protocol"], as_index=False)[metric].mean()
        chart = pivot.pivot(index=x_col, columns="protocol", values=metric)
        chart.plot(kind="bar", figsize=(9, 5))
        plt.title(title)
        plt.ylabel(metric.replace("_", " ").title())
        plt.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig(output, dpi=220)
        plt.close()
