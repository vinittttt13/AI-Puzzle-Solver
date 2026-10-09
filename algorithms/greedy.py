"""
Greedy Best-First Search Algorithm.
Evaluation function: f(n) = h(n).
Fast heuristic search that prioritizes nodes that appear closest to the goal.
Not guaranteed to find the optimal path.
"""
import time
import heapq
from typing import Callable, Optional
from core.puzzle import PuzzleState
from core.heuristics import manhattan_distance, HEURISTIC_MAP
from algorithms.base import SearchAlgorithm, SearchResult

class GreedyBestFirstSearch(SearchAlgorithm):
    def __init__(self, heuristic_name: str = "manhattan", heuristic_fn: Optional[Callable[[PuzzleState], float]] = None):
        name = f"Greedy Best-First ({heuristic_name.replace('_', ' ').title()})"
        super().__init__(name=name, is_optimal=False)
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
                is_optimal=False
            )

        counter = 0
        h_start = self.heuristic_fn(initial_state)
        frontier = [(h_start, counter, initial_state)]
        heapq.heapify(frontier)

        came_from = {initial_state: None}
        action_taken = {}
        visited = set()

        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            if time.perf_counter() - start_time > timeout_sec:
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=self.heuristic_name,
                    success=False,
                    nodes_expanded=nodes_expanded,
                    max_frontier_size=max_frontier_size,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=False,
                    error_message=f"Timeout ({timeout_sec}s) reached in Greedy Best-First Search."
                )

            _, _, current = heapq.heappop(frontier)

            if current in visited:
                continue

            if current.is_goal():
                path, actions = self.reconstruct_path(came_from, action_taken, current)
                return SearchResult(
                    algorithm_name=self.name,
                    heuristic_name=self.heuristic_name,
                    success=True,
                    path=path,
                    actions=actions,
                    cost=len(actions),
                    nodes_expanded=nodes_expanded,
                    max_frontier_size=max_frontier_size,
                    execution_time_ms=(time.perf_counter() - start_time) * 1000,
                    is_optimal=False
                )

            visited.add(current)
            nodes_expanded += 1

            for neighbor, action in current.get_neighbors():
                if neighbor not in visited and neighbor not in came_from:
                    came_from[neighbor] = current
                    action_taken[neighbor] = action
                    h_val = self.heuristic_fn(neighbor)
                    counter += 1
                    heapq.heappush(frontier, (h_val, counter, neighbor))

            if len(frontier) > max_frontier_size:
                max_frontier_size = len(frontier)

        return SearchResult(
            algorithm_name=self.name,
            heuristic_name=self.heuristic_name,
            success=False,
            nodes_expanded=nodes_expanded,
            max_frontier_size=max_frontier_size,
            execution_time_ms=(time.perf_counter() - start_time) * 1000,
            is_optimal=False,
            error_message="Frontier exhausted without reaching goal state."
        )
