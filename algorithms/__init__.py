from .base import SearchAlgorithm, SearchResult
from .astar import AStarSearch
from .bfs import BreadthFirstSearch
from .dfs import DepthFirstSearch
from .iddfs import IterativeDeepeningDFS
from .greedy import GreedyBestFirstSearch
from .idastar import IDAStarSearch

ALGORITHM_REGISTRY = {
    "astar_manhattan": lambda: AStarSearch(heuristic_name="manhattan"),
    "astar_linear_conflict": lambda: AStarSearch(heuristic_name="linear_conflict"),
    "astar_misplaced": lambda: AStarSearch(heuristic_name="misplaced"),
    "astar_euclidean": lambda: AStarSearch(heuristic_name="euclidean"),
    "greedy_manhattan": lambda: GreedyBestFirstSearch(heuristic_name="manhattan"),
    "greedy_linear_conflict": lambda: GreedyBestFirstSearch(heuristic_name="linear_conflict"),
    "greedy_misplaced": lambda: GreedyBestFirstSearch(heuristic_name="misplaced"),
    "bfs": lambda: BreadthFirstSearch(),
    "dfs": lambda: DepthFirstSearch(max_depth=30),
    "iddfs": lambda: IterativeDeepeningDFS(max_limit=32),
    "idastar_manhattan": lambda: IDAStarSearch(heuristic_name="manhattan"),
    "idastar_linear_conflict": lambda: IDAStarSearch(heuristic_name="linear_conflict")
}

ALGORITHM_METADATA = {
    "astar_linear_conflict": {
        "name": "A* (Linear Conflict)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b^d)",
        "description": "A* with Manhattan + Linear Conflict. Expands the fewest nodes while guaranteeing an optimal solution."
    },
    "astar_manhattan": {
        "name": "A* (Manhattan Distance)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b^d)",
        "description": "Standard benchmark A* search. Fast and optimal with admissible Manhattan heuristic."
    },
    "astar_misplaced": {
        "name": "A* (Misplaced Tiles)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b^d)",
        "description": "A* using simple misplaced tile count h1. Optimal, but expands more nodes than Manhattan."
    },
    "astar_euclidean": {
        "name": "A* (Euclidean Distance)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b^d)",
        "description": "A* using Euclidean straight-line distance. Admissible, explores more nodes than Manhattan."
    },
    "greedy_manhattan": {
        "name": "Greedy Best-First (Manhattan)",
        "type": "Informed (Heuristic)",
        "optimal": False,
        "time_complexity": "O(b^m)",
        "space_complexity": "O(b^m)",
        "description": "Expands node closest to goal f(n) = h(n). Extremely fast, but path length may not be optimal."
    },
    "greedy_linear_conflict": {
        "name": "Greedy Best-First (Linear Conflict)",
        "type": "Informed (Heuristic)",
        "optimal": False,
        "time_complexity": "O(b^m)",
        "space_complexity": "O(b^m)",
        "description": "Greedy search driven by Linear Conflict + Manhattan heuristic. Aggressive goal-seeking."
    },
    "greedy_misplaced": {
        "name": "Greedy Best-First (Misplaced Tiles)",
        "type": "Informed (Heuristic)",
        "optimal": False,
        "time_complexity": "O(b^m)",
        "space_complexity": "O(b^m)",
        "description": "Greedy search driven by number of misplaced tiles. Fast but path is usually sub-optimal."
    },
    "bfs": {
        "name": "Breadth-First Search (BFS)",
        "type": "Uninformed (Blind)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b^d)",
        "description": "Level-by-level queue exploration. Guaranteed shortest path, but high memory footprint."
    },
    "iddfs": {
        "name": "Iterative Deepening DFS (IDDFS)",
        "type": "Uninformed (Blind)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(bd)",
        "description": "Combines BFS optimality with DFS linear space complexity O(bd)."
    },
    "idastar_manhattan": {
        "name": "Iterative Deepening A* (Manhattan)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(d)",
        "description": "Korf's IDA* search. Optimal with linear memory footprint O(d) using f-bound contours."
    },
    "idastar_linear_conflict": {
        "name": "Iterative Deepening A* (Linear Conflict)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(d)",
        "description": "IDA* using Linear Conflict heuristic. Minimal node expansions with strict O(d) memory bounds."
    },
    "dfs": {
        "name": "Depth-First Search (DFS)",
        "type": "Uninformed (Blind)",
        "optimal": False,
        "time_complexity": "O(b^m)",
        "space_complexity": "O(bm)",
        "description": "Explores branch depth first. Included to demonstrate why blind DFS performs poorly on cyclic graphs."
    }
}

def get_algorithm(key: str) -> SearchAlgorithm:
    if key not in ALGORITHM_REGISTRY:
        raise ValueError(f"Unknown algorithm '{key}'. Available: {list(ALGORITHM_REGISTRY.keys())}")
    return ALGORITHM_REGISTRY[key]()
