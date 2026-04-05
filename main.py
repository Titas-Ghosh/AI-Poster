#!/usr/bin/env python3
"""Word Ladder Solver — CLI entry point.

Usage:
    python main.py --start cold --goal warm
    python main.py --start cold --goal warm --visualize
    python main.py --compare
"""

import argparse
import sys

from solver.astar import astar
from solver.bfs import bfs
from solver.dijkstra import dijkstra
from solver.graph import WordGraph


def print_result(result):
    """Pretty-print a search result to the console."""
    print(f"\n{'-' * 50}")
    print(f"  Algorithm:      {result.algorithm}")
    if result.path:
        print(f"  Path:           {' -> '.join(result.path)}")
        print(f"  Path length:    {result.path_length} steps")
    else:
        print("  Path:           No path found!")
    print(f"  Nodes explored: {result.nodes_explored}")
    print(f"  Time:           {result.execution_time:.4f}s")
    print(f"{'-' * 50}")


def cmd_solve(args, graph):
    """Solve a single word ladder and optionally generate visualizations."""
    start, goal = args.start.lower(), args.goal.lower()

    # Validation
    if len(start) != len(goal):
        print(f"Error: Words must be the same length. "
              f"'{start}' has {len(start)} letters, '{goal}' has {len(goal)}.")
        sys.exit(1)
    if not graph.has_word(start):
        print(f"Error: '{start}' is not in the dictionary.")
        sys.exit(1)
    if not graph.has_word(goal):
        print(f"Error: '{goal}' is not in the dictionary.")
        sys.exit(1)

    # Run selected algorithm(s)
    algorithms = {"astar": ("A*", astar), "bfs": ("BFS", bfs), "dijkstra": ("Dijkstra", dijkstra)}

    if args.algorithm == "all":
        for name, fn in algorithms.values():
            result = fn(graph, start, goal)
            print_result(result)
    else:
        name, fn = algorithms[args.algorithm]
        result = fn(graph, start, goal)
        print_result(result)

    # Visualizations (always run A* for these, since they need expansion history)
    if args.visualize:
        astar_result = astar(graph, start, goal) if args.algorithm != "astar" else result

        from visualizer.search_graph import plot_search_graph
        from visualizer.step_viewer import plot_step_viewer
        from visualizer.heuristic_plot import plot_heuristic_accuracy
        from visualizer.comparison import plot_comparison

        print("\nGenerating visualizations...")
        plot_search_graph(astar_result, graph)
        plot_step_viewer(astar_result, graph)
        plot_heuristic_accuracy(goal, graph)
        plot_comparison(graph)
        print("\nAll visualizations saved to output/")


def cmd_compare(args, graph):
    """Run algorithm comparison across preset word pairs."""
    from visualizer.comparison import plot_comparison, DEFAULT_WORD_PAIRS

    print("Running algorithm comparison...")
    print(f"Word pairs: {', '.join(f'{s}->{g}' for s, g in DEFAULT_WORD_PAIRS)}\n")

    results = plot_comparison(graph)

    # Print table
    current_pair = None
    for r in results:
        if r["pair"] != current_pair:
            current_pair = r["pair"]
            print(f"\n  {current_pair}:")
        print(f"    {r['algorithm']:>8s}  |  explored: {r['nodes_explored']:>4d}  |  "
              f"path length: {r['path_length']}  |  {r['path']}")


def main():
    parser = argparse.ArgumentParser(
        description="Word Ladder Solver using A*, BFS, and Dijkstra",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python main.py --start cold --goal warm\n"
               "  python main.py --start cold --goal warm --visualize\n"
               "  python main.py --start cold --goal warm --algorithm all\n"
               "  python main.py --compare\n",
    )
    parser.add_argument("-s", "--start", type=str, help="Start word")
    parser.add_argument("-g", "--goal", type=str, help="Goal word")
    parser.add_argument("-a", "--algorithm", type=str, default="astar",
                        choices=["astar", "bfs", "dijkstra", "all"],
                        help="Algorithm to use (default: astar)")
    parser.add_argument("-v", "--visualize", action="store_true",
                        help="Generate all visualizations")
    parser.add_argument("-c", "--compare", action="store_true",
                        help="Run algorithm comparison on preset word pairs")
    parser.add_argument("-d", "--dictionary", type=str,
                        default="data/dictionary.txt",
                        help="Path to dictionary file")

    args = parser.parse_args()

    # Load dictionary and build graph
    print(f"Loading dictionary from {args.dictionary}...")
    graph = WordGraph(args.dictionary)
    print(f"Loaded {len(graph.words)} words "
          f"({', '.join(f'{k}-letter: {len(v)}' for k, v in sorted(graph.words_by_length.items()))})")

    if args.compare:
        cmd_compare(args, graph)
    elif args.start and args.goal:
        cmd_solve(args, graph)
    else:
        parser.print_help()
        print("\nError: Provide --start and --goal, or use --compare.")
        sys.exit(1)


if __name__ == "__main__":
    main()
