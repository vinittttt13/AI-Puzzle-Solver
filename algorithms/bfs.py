"""
Breadth-First Search (BFS) Algorithm Implementation.
Explores nodes layer by layer using a FIFO queue.
Guaranteed to find the shortest path (optimal) for uniform edge costs.
"""
import time
from collections import deque
from core.puzzle import PuzzleState
from algorithms.base import SearchAlgorithm, SearchResult

class BreadthFirstSearch(SearchAlgorithm):
    def __init__(self):
        super().__init__(name="Breadth-First Search (BFS)", is_optimal=True)

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

        queue = deque([initial_state])
        came_from = {initial_state: None}
        action_taken = {}
        visited = {initial_state}

        nodes_expanded = 0
        max_frontier_size = 1

        while queue:
            if time.perf_counter() - start_time > timeout_sec:
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=None,
                    success=False,
                    nodes_expanded=nodes_expanded,
                    max_frontier_size=max_frontier_size,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=True,
                    error_message=f"Timeout ({timeout_sec}s) exceeded. BFS memory/time limit reached."
                )

            current = queue.popleft()
            nodes_expanded += 1

            for neighbor, action in current.get_neighbors():
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    action_taken[neighbor] = action

                    if neighbor.is_goal():
                        path, actions = self.reconstruct_path(came_from, action_taken, neighbor)
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
                            is_optimal=True
                        )

                    queue.append(neighbor)

            if len(queue) > max_frontier_size:
                max_frontier_size = len(queue)

        return SearchResult(
            algorithm_name=self.name,
            heuristic_name=None,
            success=False,
            nodes_expanded=nodes_expanded,
            max_frontier_size=max_frontier_size,
            execution_time_ms=(time.perf_counter() - start_time) * 1000,
            is_optimal=True,
            error_message="Frontier exhausted without reaching goal state."
        )
