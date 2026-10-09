"""
Benchmarking engine for comparing AI search algorithms on N-Puzzle instances.
"""
from typing import List, Dict, Any, Optional
from core.puzzle import PuzzleState
from algorithms import get_algorithm, ALGORITHM_METADATA

# Default algorithms to compare in a standard benchmark run
DEFAULT_BENCHMARK_ALGS = [
    "astar_linear_conflict",
    "astar_manhattan",
    "astar_misplaced",
    "greedy_manhattan",
    "bfs",
    "idastar_manhattan"
]

def run_benchmark(
    initial_state: PuzzleState,
    algorithm_keys: Optional[List[str]] = None,
    timeout_sec: float = 6.0
) -> Dict[str, Any]:
    """
    Executes multiple algorithms on the exact same puzzle instance and gathers comparative statistics.
    """
    if algorithm_keys is None:
        algorithm_keys = DEFAULT_BENCHMARK_ALGS

    results = []
    for key in algorithm_keys:
        try:
            solver = get_algorithm(key)
            # DFS can explode on moderate depths, cap timeout
            effective_timeout = min(timeout_sec, 4.0) if key == "dfs" else timeout_sec
            res = solver.solve(initial_state, timeout_sec=effective_timeout)
            meta = ALGORITHM_METADATA.get(key, {})
            
            res_dict = res.to_dict()
            res_dict["key"] = key
            res_dict["category"] = meta.get("type", "Unknown")
            res_dict["time_complexity"] = meta.get("time_complexity", "-")
            res_dict["space_complexity"] = meta.get("space_complexity", "-")
            results.append(res_dict)
        except Exception as e:
            results.append({
                "key": key,
                "algorithm_name": key,
                "heuristic_name": None,
                "success": False,
                "cost": 0,
                "nodes_expanded": 0,
                "max_frontier_size": 0,
                "execution_time_ms": 0.0,
                "is_optimal": False,
                "error_message": str(e)
            })

    return {
        "initial_board": list(initial_state.board),
        "size": initial_state.size,
        "is_solvable": initial_state.is_solvable(),
        "benchmark_results": results
    }
