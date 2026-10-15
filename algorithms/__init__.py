from .base import SearchAlgorithm, SearchResult
from .astar import AStarSearch
from .bfs import BreadthFirstSearch
from .dfs import DepthFirstSearch
from .iddfs import IterativeDeepeningDFS
from .greedy import GreedyBestFirstSearch
from .idastar import IDAStarSearch

# Core Algorithms Registry - Focused on 5th Semester AI Syllabus
ALGORITHM_REGISTRY = {
    "astar_manhattan": lambda: AStarSearch(heuristic_name="manhattan"),
    "astar_misplaced": lambda: AStarSearch(heuristic_name="misplaced"),
    "bfs": lambda: BreadthFirstSearch(),
    "dfs": lambda: DepthFirstSearch(max_depth=25),
    "greedy_manhattan": lambda: GreedyBestFirstSearch(heuristic_name="manhattan"),
    # Compatibility mappings
    "astar_linear_conflict": lambda: AStarSearch(heuristic_name="linear_conflict"),
    "astar_euclidean": lambda: AStarSearch(heuristic_name="euclidean"),
    "greedy_linear_conflict": lambda: GreedyBestFirstSearch(heuristic_name="linear_conflict"),
    "greedy_misplaced": lambda: GreedyBestFirstSearch(heuristic_name="misplaced"),
    "iddfs": lambda: IterativeDeepeningDFS(max_limit=32),
    "idastar_manhattan": lambda: IDAStarSearch(heuristic_name="manhattan"),
    "idastar_linear_conflict": lambda: IDAStarSearch(heuristic_name="linear_conflict")
}

# Metadata for the standard AI algorithms
ALGORITHM_METADATA = {
    "astar_manhattan": {
        "name": "A* Search (Manhattan Distance)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b^d)",
        "description": "Uses f(n) = g(n) + h(n) with Manhattan distance. Guarantees the optimal (shortest) solution path while expanding minimal nodes."
    },
    "astar_linear_conflict": {
        "name": "A* Search (Linear Conflict)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b^d)",
        "description": "Uses Manhattan distance + linear conflict penalty (+2 per conflict). Highly informed and admissible."
    },
    "astar_euclidean": {
        "name": "A* Search (Euclidean Distance)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b^d)",
        "description": "Uses straight-line Euclidean distance heuristic. Admissible but less informed than Manhattan distance."
    },
    "astar_misplaced": {
        "name": "A* Search (Misplaced Tiles)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b^d)",
        "description": "Uses f(n) = g(n) + h(n) with the count of misplaced tiles. Admissible heuristic guaranteeing optimal solution."
    },
    "bfs": {
        "name": "Breadth-First Search (BFS)",
        "type": "Uninformed (Blind)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b^d)",
        "description": "Explores states level-by-level using a FIFO queue. Guarantees the shortest path for unit step costs."
    },
    "dfs": {
        "name": "Depth-First Search (DFS)",
        "type": "Uninformed (Blind)",
        "optimal": False,
        "time_complexity": "O(b^m)",
        "space_complexity": "O(b*m)",
        "description": "Explores deeply along each branch before backtracking using a LIFO stack (depth-limited to avoid infinite loops)."
    },
    "iddfs": {
        "name": "Iterative Deepening DFS (IDDFS)",
        "type": "Uninformed (Blind)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(b*d)",
        "description": "Combines DFS space efficiency with BFS optimality by iteratively increasing the depth limit."
    },
    "greedy_manhattan": {
        "name": "Greedy Best-First Search (Manhattan)",
        "type": "Informed (Heuristic)",
        "optimal": False,
        "time_complexity": "O(b^m)",
        "space_complexity": "O(b^m)",
        "description": "Evaluates nodes solely by heuristic f(n) = h(n). Fast goal pursuit, but does not guarantee the shortest path."
    },
    "greedy_linear_conflict": {
        "name": "Greedy Best-First Search (Linear Conflict)",
        "type": "Informed (Heuristic)",
        "optimal": False,
        "time_complexity": "O(b^m)",
        "space_complexity": "O(b^m)",
        "description": "Greedy best-first search guided by linear conflict heuristic."
    },
    "greedy_misplaced": {
        "name": "Greedy Best-First Search (Misplaced)",
        "type": "Informed (Heuristic)",
        "optimal": False,
        "time_complexity": "O(b^m)",
        "space_complexity": "O(b^m)",
        "description": "Greedy best-first search guided by misplaced tiles heuristic."
    },
    "idastar_manhattan": {
        "name": "IDA* Search (Manhattan)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(d)",
        "description": "Iterative Deepening A* with Manhattan distance. Guarantees optimal path with linear memory."
    },
    "idastar_linear_conflict": {
        "name": "IDA* Search (Linear Conflict)",
        "type": "Informed (Heuristic)",
        "optimal": True,
        "time_complexity": "O(b^d)",
        "space_complexity": "O(d)",
        "description": "Iterative Deepening A* with Linear Conflict heuristic. High pruning power with minimal memory."
    }
}

def get_algorithm(key: str) -> SearchAlgorithm:
    if key not in ALGORITHM_REGISTRY:
        raise ValueError(f"Unknown algorithm '{key}'. Available: {list(ALGORITHM_REGISTRY.keys())}")
    return ALGORITHM_REGISTRY[key]()
