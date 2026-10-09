"""
A* Search Algorithm Implementation.
Evaluation function: f(n) = g(n) + h(n)
Guarantees optimality when heuristic h(n) is admissible and consistent.
"""
import time
import heapq
from typing import Callable, Optional
from core.puzzle import PuzzleState
from core.heuristics import manhattan_distance, HEURISTIC_MAP
from algorithms.base import SearchAlgorithm, SearchResult

class AStarSearch(SearchAlgorithm):
    def __init__(self, heuristic_name: str = "manhattan", heuristic_fn: Optional[Callable[[PuzzleState], float]] = None):
        name = f"A* ({heuristic_name.replace('_', ' ').title()})"
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

        # Priority Queue elements: (f_score, counter, state)
        counter = 0
        h_start = self.heuristic_fn(initial_state)
        frontier = [(h_start, counter, initial_state)]
        heapq.heapify(frontier)

        g_score = {initial_state: 0}
        came_from = {initial_state: None}
        action_taken = {}
        closed_set = set()

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
                    is_optimal=True,
                    error_message=f"Timeout reached ({timeout_sec}s). State space too large for allotted time."
                )

            current_f, _, current = heapq.heappop(frontier)

            if current in closed_set:
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
                    is_optimal=True
                )

            closed_set.add(current)
            nodes_expanded += 1
            curr_g = g_score[current]

            for neighbor, action in current.get_neighbors():
                if neighbor in closed_set:
                    continue

                tentative_g = curr_g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    action_taken[neighbor] = action
                    g_score[neighbor] = tentative_g
                    h_val = self.heuristic_fn(neighbor)
                    f_val = tentative_g + h_val
                    counter += 1
                    heapq.heappush(frontier, (f_val, counter, neighbor))

            if len(frontier) > max_frontier_size:
                max_frontier_size = len(frontier)

        return SearchResult(
            algorithm_name=self.name,
            heuristic_name=self.heuristic_name,
            success=False,
            nodes_expanded=nodes_expanded,
            max_frontier_size=max_frontier_size,
            execution_time_ms=(time.perf_counter() - start_time) * 1000,
            is_optimal=True,
            error_message="Frontier exhausted without reaching goal state."
        )
