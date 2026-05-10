# Relay Network Simulator - Presentation Outline

## Slide 1: Title

- Relay Network Simulator
- Flooding vs Gossip under packet loss

## Slide 2: Problem

- Efficient dissemination in unreliable networks
- Trade-off between robustness and overhead

## Slide 3: System Design

- Graph-based topology model
- Discrete-event propagation engine
- Modular protocol strategy pattern

## Slide 4: Protocol Logic

- Flooding: high coverage, high overhead
- Gossip: lower overhead, probabilistic coverage

## Slide 5: Experiment Setup

- Topologies: random, mesh, grid, small-world
- Loss rates: 0, 10, 20, 50%
- Sizes: 50, 100, 500 nodes

## Slide 6: Metrics

- Delivery ratio
- Total transmissions
- Redundancy
- Delay and hop count
- Packet-loss impact

## Slide 7: Results Visualization

- Delivery ratio and overhead comparison
- Packet-loss sensitivity plots
- Scale and density comparison charts

## Slide 8: Conclusions

- Flooding improves reachability but costs bandwidth
- Gossip reduces overhead and can remain resilient with tuned fan-out
- Topology and loss strongly affect protocol efficiency

