"""
Iterative Deepening A* (IDA*) Search Algorithm.
Invented by Richard Korf (1985) for puzzle state-space search.
Uses f(n) = g(n) + h(n) cutoff thresholds.
Guarantees optimal solutions with O(d) linear memory footprint.
"""
import time
from typing import Callable, Optional, Tuple, List
from core.puzzle import PuzzleState
from core.heuristics import manhattan_distance, HEURISTIC_MAP
from algorithms.base import SearchAlgorithm, SearchResult

class IDAStarSearch(SearchAlgorithm):
    def __init__(self, heuristic_name: str = "manhattan", heuristic_fn: Optional[Callable[[PuzzleState], float]] = None):
        name = f"IDA* ({heuristic_name.replace('_', ' ').title()})"
        super().__init__(name=name, is_optimal=True)
        self.heuristic_name = heuristic_name
        self.heuristic_fn = heuristic_fn or HEURISTIC_MAP.get(heuristic_name, manhattan_distance)

    def solve(self, initial_state: PuzzleState, timeout_sec: float = 10.0) -> SearchResult:
        start_time = time.perf_counter()

        if initial_state.is_goal():
            return SearchResult(
                algorithm_name=self.name,
                heuristic_name=self.heuristic_name,
                success=True,
                path=[initial_state],
                actions=[],
                cost=0,
                nodes_expanded=0,
                max_frontier_size=1,
                execution_time_ms=(time.perf_counter() - start_time) * 1000,
                is_optimal=True
            )

        threshold = self.heuristic_fn(initial_state)
        path = [initial_state]
        actions = []

        total_nodes_expanded = 0
        max_depth_seen = 1

        while True:
            if time.perf_counter() - start_time > timeout_sec:
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=self.heuristic_name,
                    success=False,
                    nodes_expanded=total_nodes_expanded,
                    max_frontier_size=max_depth_seen,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=True,
                    error_message=f"Timeout ({timeout_sec}s) exceeded at f-threshold {threshold}."
                )

            status, next_threshold, nodes_in_iter = self._search(
                path, actions, 0, threshold, start_time, timeout_sec
            )
            total_nodes_expanded += nodes_in_iter
            max_depth_seen = max(max_depth_seen, len(path))

            if status == "FOUND":
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=self.heuristic_name,
                    success=True,
                    path=list(path),
                    actions=list(actions),
                    cost=len(actions),
                    nodes_expanded=total_nodes_expanded,
                    max_frontier_size=max_depth_seen,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=True
                )

            if status == "TIMEOUT":
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=self.heuristic_name,
                    success=False,
                    nodes_expanded=total_nodes_expanded,
                    max_frontier_size=max_depth_seen,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=True,
                    error_message=f"Timeout ({timeout_sec}s) reached."
                )

            if next_threshold == float('inf'):
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=self.heuristic_name,
                    success=False,
                    nodes_expanded=total_nodes_expanded,
                    max_frontier_size=max_depth_seen,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=True,
                    error_message="Search space exhausted without finding solution."
                )

            threshold = next_threshold

    def _search(
        self,
        path: List[PuzzleState],
        actions: List[str],
        g: int,
        threshold: float,
        start_time: float,
        timeout_sec: float
    ) -> Tuple[str, float, int]:
        nodes_expanded = 0
        current = path[-1]
        f = g + self.heuristic_fn(current)

        if f > threshold:
            return "NOT_FOUND", f, 0

        if current.is_goal():
            return "FOUND", f, 0

        if time.perf_counter() - start_time > timeout_sec:
            return "TIMEOUT", f, 0

        nodes_expanded += 1
        min_cutoff = float('inf')

        for neighbor, action in current.get_neighbors():
            if neighbor not in path:
                path.append(neighbor)
                actions.append(action)

                status, res, child_expanded = self._search(
                    path, actions, g + 1, threshold, start_time, timeout_sec
                )
                nodes_expanded += child_expanded

                if status == "FOUND":
                    return "FOUND", res, nodes_expanded
                if status == "TIMEOUT":
                    return "TIMEOUT", res, nodes_expanded

                min_cutoff = min(min_cutoff, res)
                path.pop()
                actions.pop()

        return "NOT_FOUND", min_cutoff, nodes_expanded
