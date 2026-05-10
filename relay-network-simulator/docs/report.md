# Relay Network Simulator Report

## Objective

This project evaluates message dissemination in relay-node networks by comparing **Flooding** and **Gossip** protocols across topology, scale, and packet-loss scenarios.

## Architecture

- **network/**: core entities (`Node`, `Message`) and topology generator
- **protocols/**: forwarding strategies (Flooding, Gossip)
- **simulation/**: discrete-event scheduler, packet-loss model, simulator engine
- **metrics/**: run-level metric collection and statistical summaries
- **visualization/**: topology plotting, experiment charts, propagation animation
- **experiments/**: repeatable scenario runners with CSV/plot export

## Protocols

### Flooding

Each node forwards a newly received message to all neighbors (optionally probabilistic forwarding). Duplicate receptions are ignored. TTL limits propagation depth.

### Gossip

Each node forwards to a subset of neighbors:

- fixed `K` random neighbors, or
- neighbors selected by probability `P`

An adaptive mode can increase/decrease fan-out based on remaining TTL.

## Simulation Model

- Discrete events processed by timestamp
- Per-link transmission delay sampled from configurable range
- Independent packet loss per transmission
- Optional node failures
- Optional congestion-based delay inflation

## Metrics

1. Delivery Ratio
2. Total Transmissions
3. Redundant Messages
4. Average Hop Count
5. Average Delay
6. Network Overhead
7. Packet Loss Impact

## Reproducibility

All experiments support deterministic replay by seed control.

## How to Run

```bash
python main.py --experiment all --seed 42
```

