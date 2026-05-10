# Relay Network Simulator

A modular Python project that simulates message dissemination in relay-node networks and compares **Flooding** vs **Gossip** protocols under packet loss.

## Purpose and Problem Statement

Reliable message propagation in relay-based networks is hard when links are unreliable and bandwidth is limited.  
This project evaluates a core trade-off:

- **Flooding**: maximize reachability by aggressively forwarding packets
- **Gossip**: reduce redundant traffic with probabilistic forwarding

The simulator helps quantify how these strategies behave under different network structures, sizes, densities, and packet-loss conditions.

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

## Simulation Model (How It Works Internally)

- The network is represented as a graph where nodes are relays and edges are communication links.
- A source injects messages into the graph and events are processed in discrete time steps.
- Each transmission is subject to configurable packet loss and delivery delay.
- Messages carry a TTL/hop budget to prevent infinite propagation.
- Nodes track already-seen message IDs to suppress duplicates.
- The simulator records per-run metrics, then aggregates repeated runs for stable comparisons.

### Protocol Behavior

#### Flooding

- On first reception, a node forwards the message to (almost) all eligible neighbors.
- Strength: high delivery probability in connected topologies.
- Cost: high transmission overhead from duplicate forwarding attempts.

#### Gossip

- On first reception, a node forwards with probability *p* (or to a subset of neighbors).
- Strength: lower traffic and better scalability.
- Cost: delivery ratio can drop, especially in sparse or lossy networks.

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

## Experiment Workflow

1. Configure experiment parameters (topology, node count, loss rate, protocol).
2. Run one or all experiments from CLI.
3. Collect run-level metrics (delivery ratio, transmissions, overhead, latency where available).
4. Aggregate and export outputs:
   - `results/csv`: tabular metrics
   - `results/plots`: generated visual comparisons
   - `results/logs`: summaries and run details

## Outputs and Interpretation

- **Delivery Ratio**: fraction of nodes that receive the message. Higher is better for reliability.
- **Overhead**: extra transmissions beyond minimally necessary delivery. Lower is better for efficiency.
- **Transmissions**: total forwarding workload; key scalability indicator.
- **Topology sensitivity**: sparse graphs expose reachability limits; dense graphs amplify redundancy.
- **Loss sensitivity**: increasing packet loss stresses robustness and reveals protocol resilience.

Typical pattern: Flooding tends to maximize delivery but at high overhead, while Gossip trades some reliability for lower network load.

## Plots

Representative generated plots (from `results/plots`):

### Experiment 1: Baseline Protocol Comparison

![Experiment 1 Topology](results/plots/experiment1_topology.png)
![Experiment 1 Delivery Ratio](results/plots/experiment1_delivery_ratio.png)
![Experiment 1 Overhead](results/plots/experiment1_overhead.png)

### Experiment 2: Packet Loss Impact

![Experiment 2 Packet Loss vs Delivery](results/plots/experiment2_packet_loss_delivery.png)

### Experiment 3: Scaling with Network Size

![Experiment 3 Transmissions](results/plots/experiment3_transmissions.png)

### Experiment 4: Sparse vs Dense Topologies

![Experiment 4 Delivery Ratio](results/plots/experiment4_delivery_ratio.png)

CSV outputs are saved in `results/csv`, plots in `results/plots`, and summaries in `results/logs`.

