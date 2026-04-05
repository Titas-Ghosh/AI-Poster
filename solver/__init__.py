"""Word Ladder Solver — A*, BFS, and Dijkstra implementations."""

import dataclasses
from typing import Optional


@dataclasses.dataclass
class SearchResult:
    """Unified result object returned by all search algorithms."""

    path: Optional[list[str]]           # Solution path, or None if no path exists
    nodes_explored: int                 # Number of nodes expanded
    path_length: int                    # Number of steps (edges) in the path
    algorithm: str                      # "A*", "BFS", or "Dijkstra"
    execution_time: float               # Seconds elapsed

    # A*-specific: list of step snapshots for visualization (None for BFS/Dijkstra)
    # Each dict: {step, current, g, h, f, open_set, closed_set, neighbors_added}
    expansion_history: Optional[list[dict]] = None
