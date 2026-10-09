"""
Depth-First Search (DFS) Algorithm Implementation with Depth Limit.
Explores deepest nodes first using a LIFO stack.
Not optimal and may find very long paths.
Demonstrates why uninformed DFS struggles in cyclic state spaces.
"""
import time
from core.puzzle import PuzzleState
from algorithms.base import SearchAlgorithm, SearchResult

class DepthFirstSearch(SearchAlgorithm):
    def __init__(self, max_depth: int = 25):
        super().__init__(name="Depth-First Search (DFS)", is_optimal=False)
        self.max_depth = max_depth

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
                is_optimal=False
            )

        # Stack holds: (current_state, path_so_far, actions_so_far, depth)
        stack = [(initial_state, [initial_state], [], 0)]
        # Track path ancestor states to prevent loops on the current branch
        visited_depths = {initial_state: 0}

        nodes_expanded = 0
        max_frontier_size = 1

        while stack:
            if time.perf_counter() - start_time > timeout_sec:
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=None,
                    success=False,
                    nodes_expanded=nodes_expanded,
                    max_frontier_size=max_frontier_size,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=False,
                    error_message=f"Timeout ({timeout_sec}s) reached during DFS traversal."
                )

            current, path, actions, depth = stack.pop()

            if current.is_goal():
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=None,
                    success=True,
                    path=path,
                    actions=actions,
                    cost=len(actions),
                    nodes_expanded=nodes_expanded,
                    max_frontier_size=max_frontier_size,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=False
                )

            if depth >= self.max_depth:
                continue

            nodes_expanded += 1

            for neighbor, action in current.get_neighbors():
                # Avoid cycles along the current branch
                if neighbor in path:
                    continue
                # Also prune if visited at shallower depth
                if neighbor in visited_depths and visited_depths[neighbor] <= depth + 1:
                    continue

                visited_depths[neighbor] = depth + 1
                stack.append((neighbor, path + [neighbor], actions + [action], depth + 1))

            if len(stack) > max_frontier_size:
                max_frontier_size = len(stack)

        return SearchResult(
            algorithm_name=self.name,
            heuristic_name=None,
            success=False,
            nodes_expanded=nodes_expanded,
            max_frontier_size=max_frontier_size,
            execution_time_ms=(time.perf_counter() - start_time) * 1000,
            is_optimal=False,
            error_message=f"No solution found within depth limit of {self.max_depth} moves."
        )
