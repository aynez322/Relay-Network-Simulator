# Relay Network Simulator

A modular Python project that simulates message dissemination in relay-node networks and compares **Flooding** vs **Gossip** protocols under packet loss.

## Features

- Graph topologies: random, mesh, grid, small-world
- Discrete-event simulation engine with configurable delay and TTL
- Flooding and Gossip dissemination protocols
- Packet-loss model per transmission
- Metrics collection and statistical aggregation
- Automated experiments (protocol, loss, scale, density)
- Plots, CSV exports, and optional propagation animation
- Reproducible runs via random seeds

## Project Structure

```text
relay-network-simulator/
├── main.py
├── config/
├── network/
├── protocols/
├── simulation/
├── metrics/
├── visualization/
├── experiments/
├── results/
├── docs/
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

From inside `relay-network-simulator`:

```bash
python main.py --experiment all --seed 42
```

Run a specific experiment:

```bash
python main.py --experiment experiment2 --seed 42
```

CLI options:

- `--experiment`: `experiment1`, `experiment2`, `experiment3`, `experiment4`, `all`
- `--seed`: random seed for reproducibility
- `--no-anim`: skip animation generation

## Experiments

1. Flooding vs Gossip (no packet loss)
2. Packet loss sweep (0%, 10%, 20%, 50%)
3. Network size scaling (50, 100, 500 nodes)
4. Sparse vs dense topologies

CSV outputs are saved in `results/csv`, plots in `results/plots`, and summaries in `results/logs`.

