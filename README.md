# Word Ladder Solver — A* Search Algorithm

A Python tool that finds the shortest transformation chain between two English words, changing exactly one letter at each step so every intermediate word is valid.

**Example:** `cold → cord → card → ward → warm`

## How It Works

The solver models the problem as a graph where each word is a node and edges connect words that differ by exactly one letter. It then searches for the shortest path using:

- **A\* Search** — Uses `f(n) = g(n) + h(n)` where `g(n)` is the number of steps taken and `h(n)` is the Hamming distance (number of differing characters) to the goal. This heuristic is admissible, guaranteeing an optimal solution while exploring fewer nodes than uninformed search.
- **BFS** — Breadth-first search explores all nodes at the current depth before moving deeper. Guarantees the shortest path but explores more nodes than A*.
- **Dijkstra's Algorithm** — Uses a priority queue with uniform edge cost. Equivalent to BFS for unweighted graphs, included for comparison.

## Installation

```bash
pip install -r requirements.txt
```

**Dependencies:** matplotlib, networkx, seaborn (Python 3.10+)

## Usage

### Solve a word ladder

```bash
python main.py --start cold --goal warm
```

Output:
```
Algorithm:      A*
Path:           cold → cord → card → ward → warm
Path length:    4 steps
Nodes explored: 12
Time:           0.0030s
```

### Compare all three algorithms

```bash
python main.py --start cold --goal warm --algorithm all
```

### Generate visualizations

```bash
python main.py --start cold --goal warm --visualize
```

Generates four high-resolution PNG images in `output/`:

| File | Description |
|------|-------------|
| `search_graph.png` | Explored subgraph with optimal path highlighted |
| `comparison_chart.png` | Bar chart comparing nodes explored across algorithms |
| `astar_steps.png` | Step-by-step A* expansion panels |
| `heuristic_accuracy.png` | Scatter plot of heuristic estimate vs actual cost |

### Run preset comparison

```bash
python main.py --compare
```

Runs all three algorithms on five word pairs and generates the comparison bar chart.

## Algorithm Comparison

A* consistently explores fewer nodes than BFS and Dijkstra by using the Hamming distance heuristic to guide the search toward the goal. BFS and Dijkstra explore roughly the same number of nodes (as expected for unweighted graphs), expanding outward uniformly in all directions.

## Project Structure

```
├── main.py              # CLI entry point
├── solver/
│   ├── graph.py         # Dictionary loading & adjacency graph
│   ├── astar.py         # A* search implementation
│   ├── bfs.py           # BFS implementation
│   ├── dijkstra.py      # Dijkstra implementation
│   └── heuristics.py    # Hamming distance heuristic
├── visualizer/
│   ├── search_graph.py  # Search graph visualization
│   ├── comparison.py    # Algorithm comparison bar chart
│   ├── step_viewer.py   # Step-by-step A* expansion
│   └── heuristic_plot.py# Heuristic accuracy scatter plot
├── data/
│   └── dictionary.txt   # Word list (~3,200 words, 3-5 letters)
└── output/              # Generated images
```

## Tech Stack

Python | networkx | matplotlib | seaborn
