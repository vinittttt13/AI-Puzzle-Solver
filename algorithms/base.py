"""
Base classes and result structures for Search Algorithms.
"""
from dataclasses import dataclass, field
from typing import List, Optional
import time
from abc import ABC, abstractmethod
from core.puzzle import PuzzleState

@dataclass
class SearchResult:
    algorithm_name: str
    heuristic_name: Optional[str]
    success: bool
    path: List[PuzzleState] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    cost: int = 0
    nodes_expanded: int = 0
    max_frontier_size: int = 0
    execution_time_ms: float = 0.0
    is_optimal: bool = False
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "algorithm_name": self.algorithm_name,
            "heuristic_name": self.heuristic_name,
            "success": self.success,
            "path": [list(state.board) for state in self.path],
            "actions": self.actions,
            "cost": self.cost,
            "nodes_expanded": self.nodes_expanded,
            "max_frontier_size": self.max_frontier_size,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "is_optimal": self.is_optimal,
            "error_message": self.error_message
        }


class SearchAlgorithm(ABC):
    """
    Abstract interface for graph/tree search algorithms.
    """
    def __init__(self, name: str, is_optimal: bool = True):
        self.name = name
        self.is_optimal = is_optimal

    @abstractmethod
    def solve(self, initial_state: PuzzleState, timeout_sec: float = 10.0) -> SearchResult:
        pass

    @staticmethod
    def reconstruct_path(came_from: dict, action_taken: dict, current: PuzzleState) -> tuple[List[PuzzleState], List[str]]:
        path = [current]
        actions = []
        while current in came_from and came_from[current] is not None:
            actions.append(action_taken[current])
            current = came_from[current]
            path.append(current)
        path.reverse()
        actions.reverse()
        return path, actions
