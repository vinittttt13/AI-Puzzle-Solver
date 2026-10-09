"""
Core puzzle representation and logic for N-Puzzle (8-Puzzle and 15-Puzzle).
"""
from typing import Tuple, List, Optional
import random

# Standard goal states
GOAL_8 = (1, 2, 3, 4, 5, 6, 7, 8, 0)
GOAL_15 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)

# Movement offsets: (d_row, d_col, Action Name)
DIRECTIONS = [
    (-1, 0, "UP"),
    (1, 0, "DOWN"),
    (0, -1, "LEFT"),
    (0, 1, "RIGHT")
]

class PuzzleState:
    """
    Immutable representation of an N-Puzzle board state.
    board: tuple of integers, where 0 represents the blank space.
    size: dimension of the grid (e.g., 3 for 8-puzzle, 4 for 15-puzzle).
    """
    __slots__ = ('board', 'size', 'blank_idx', '_hash')

    def __init__(self, board: Tuple[int, ...], size: int = 3):
        if len(board) != size * size:
            raise ValueError(f"Board length {len(board)} does not match size {size}x{size}")
        self.board = board
        self.size = size
        self.blank_idx = board.index(0)
        self._hash = hash(board)

    @classmethod
    def from_list(cls, board_list: List[int], size: int = 3) -> "PuzzleState":
        return cls(tuple(board_list), size)

    @property
    def goal_state(self) -> Tuple[int, ...]:
        return GOAL_8 if self.size == 3 else GOAL_15

    def is_goal(self) -> bool:
        return self.board == self.goal_state

    def get_neighbors(self) -> List[Tuple["PuzzleState", str]]:
        """
        Returns valid neighboring states along with the move taken by the blank.
        """
        neighbors = []
        r, c = divmod(self.blank_idx, self.size)
        board_list = list(self.board)

        for dr, dc, action in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                target_idx = nr * self.size + nc
                # Swap blank with neighbor
                board_list[self.blank_idx], board_list[target_idx] = board_list[target_idx], board_list[self.blank_idx]
                neighbor_state = PuzzleState(tuple(board_list), self.size)
                neighbors.append((neighbor_state, action))
                # Swap back for next iteration
                board_list[self.blank_idx], board_list[target_idx] = board_list[target_idx], board_list[self.blank_idx]

        return neighbors

    def count_inversions(self) -> int:
        """
        Calculates the number of inversions in the board (ignoring the 0 blank).
        An inversion occurs when a tile i > j appears before tile j.
        """
        arr = [x for x in self.board if x != 0]
        inversions = 0
        n = len(arr)
        for i in range(n):
            for j in range(i + 1, n):
                if arr[i] > arr[j]:
                    inversions += 1
        return inversions

    def is_solvable(self) -> bool:
        """
        Determines if the puzzle configuration is solvable to standard goal state.
        For odd grid size (3x3): Solvable iff inversion count is even.
        For even grid size (4x4): Solvable iff:
          - blank on even row from bottom (1-indexed) and inversion count is odd, OR
          - blank on odd row from bottom (1-indexed) and inversion count is even.
        Equivalently: (inversions + blank_row_from_bottom) % 2 == 1
        """
        inversions = self.count_inversions()
        if self.size % 2 == 1:
            # 3x3 8-puzzle
            return inversions % 2 == 0
        else:
            # 4x4 15-puzzle
            blank_row = self.blank_idx // self.size
            blank_row_from_bottom = self.size - blank_row
            return (inversions + blank_row_from_bottom) % 2 == 1

    def solvability_details(self) -> dict:
        """
        Detailed breakdown for educational explanations.
        """
        inversions = self.count_inversions()
        solvable = self.is_solvable()
        blank_row = self.blank_idx // self.size
        blank_row_from_bottom = self.size - blank_row

        if self.size % 2 == 1:
            reason = (
                f"Inversion count is {inversions} ({'even' if inversions % 2 == 0 else 'odd'}). "
                f"For a {self.size}x{self.size} puzzle, solvability requires an EVEN number of inversions."
            )
        else:
            parity = (inversions + blank_row_from_bottom) % 2
            reason = (
                f"Inversion count is {inversions}, blank row from bottom is {blank_row_from_bottom} (1-indexed). "
                f"(inversions + blank_row_from_bottom) = {inversions + blank_row_from_bottom} (parity: {parity}). "
                f"For a {self.size}x{self.size} puzzle, solvable requires odd parity sum."
            )

        return {
            "is_solvable": solvable,
            "inversion_count": inversions,
            "blank_row_from_bottom": blank_row_from_bottom if self.size % 2 == 0 else None,
            "reason": reason
        }

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, PuzzleState):
            return False
        return self.board == other.board

    def __lt__(self, other):
        return self.board < other.board

    def __repr__(self):
        rows = [self.board[i * self.size : (i + 1) * self.size] for i in range(self.size)]
        return "\n".join(" ".join(f"{x:2d}" if x != 0 else " _" for x in row) for row in rows)


def generate_random_puzzle(size: int = 3, solvable: bool = True) -> PuzzleState:
    """
    Generates a random puzzle permutation with specified solvability.
    """
    tiles = list(range(size * size))
    while True:
        random.shuffle(tiles)
        state = PuzzleState(tuple(tiles), size)
        if state.is_solvable() == solvable and not state.is_goal():
            return state


def generate_puzzle_by_shuffling(steps: int = 15, size: int = 3) -> PuzzleState:
    """
    Generates a guaranteed solvable puzzle by applying random valid moves from the goal.
    """
    goal = GOAL_8 if size == 3 else GOAL_15
    current = PuzzleState(goal, size)
    prev = None

    for _ in range(steps):
        neighbors = current.get_neighbors()
        # Avoid undoing immediate previous move if possible
        valid_next = [n for n, _ in neighbors if n != prev]
        if not valid_next:
            valid_next = [n for n, _ in neighbors]
        prev = current
        current = random.choice(valid_next)

    return current
