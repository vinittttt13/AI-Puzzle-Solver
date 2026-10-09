"""
Iterative Deepening Depth-First Search (IDDFS).
Combines the space efficiency of DFS with the completeness and optimality of BFS.
Time Complexity: O(b^d), Space Complexity: O(bd).
"""
import time
from typing import Optional, List, Tuple
from core.puzzle import PuzzleState
from algorithms.base import SearchAlgorithm, SearchResult

class IterativeDeepeningDFS(SearchAlgorithm):
    def __init__(self, max_limit: int = 35):
        super().__init__(name="Iterative Deepening DFS (IDDFS)", is_optimal=True)
        self.max_limit = max_limit

    def solve(self, initial_state: PuzzleState, timeout_sec: float = 10.0) -> SearchResult:
        start_time = time.perf_counter()

        if initial_state.is_goal():
            return SearchResult(
                algorithm_name=self.name,
                heuristic_name=None,
                success=True,
                path=[initial_state],
                actions=[],
                cost=0,
                nodes_expanded=0,
                max_frontier_size=1,
                execution_time_ms=(time.perf_counter() - start_time) * 1000,
                is_optimal=True
            )

        total_nodes_expanded = 0
        overall_max_frontier = 1

        for depth_limit in range(self.max_limit + 1):
            if time.perf_counter() - start_time > timeout_sec:
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=None,
                    success=False,
                    nodes_expanded=total_nodes_expanded,
                    max_frontier_size=overall_max_frontier,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=True,
                    error_message=f"Timeout ({timeout_sec}s) exceeded at depth level {depth_limit}."
                )

            # Perform depth-limited search using iterative stack
            found, path, actions, expanded, peak_frontier = self._depth_limited_search(
                initial_state, depth_limit, start_time, timeout_sec
            )
            total_nodes_expanded += expanded
            overall_max_frontier = max(overall_max_frontier, peak_frontier)

            if found:
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=None,
                    success=True,
                    path=path,
                    actions=actions,
                    cost=len(actions),
                    nodes_expanded=total_nodes_expanded,
                    max_frontier_size=overall_max_frontier,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=True
                )

        return SearchResult(
            algorithm_name=self.name,
            heuristic_name=None,
            success=False,
            nodes_expanded=total_nodes_expanded,
            max_frontier_size=overall_max_frontier,
            execution_time_ms=(time.perf_counter() - start_time) * 1000,
            is_optimal=True,
            error_message=f"No solution found within maximum iterative depth limit {self.max_limit}."
        )

    def _depth_limited_search(
        self, start: PuzzleState, limit: int, start_time: float, timeout_sec: float
    ) -> Tuple[bool, List[PuzzleState], List[str], int, int]:
        stack = [(start, [start], [], 0)]
        expanded = 0
        peak_frontier = 1

        while stack:
            if time.perf_counter() - start_time > timeout_sec:
                return False, [], [], expanded, peak_frontier

            current, path, actions, depth = stack.pop()

            if current.is_goal():
                return True, path, actions, expanded, peak_frontier

            if depth < limit:
                expanded += 1
                for neighbor, action in current.get_neighbors():
                    # Cycle check on current branch
                    if neighbor not in path:
                        stack.append((neighbor, path + [neighbor], actions + [action], depth + 1))

            if len(stack) > peak_frontier:
                peak_frontier = len(stack)

        return False, [], [], expanded, peak_frontier
