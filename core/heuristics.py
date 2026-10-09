"""
Heuristic functions for N-Puzzle state evaluation.
All heuristics implemented here are admissible (never overestimate true cost)
and consistent (satisfy triangle inequality h(n) <= c(n, a, n') + h(n')).
"""
import math
from typing import Tuple, Dict, Callable
from core.puzzle import PuzzleState, GOAL_8, GOAL_15

# Precompute goal coordinate maps for fast O(1) coordinate lookup
def _build_goal_coords(goal: Tuple[int, ...], size: int) -> Dict[int, Tuple[int, int]]:
    return {tile: divmod(idx, size) for idx, tile in enumerate(goal) if tile != 0}

GOAL_COORDS_8 = _build_goal_coords(GOAL_8, 3)
GOAL_COORDS_15 = _build_goal_coords(GOAL_15, 4)

def get_goal_coords(size: int) -> Dict[int, Tuple[int, int]]:
    return GOAL_COORDS_8 if size == 3 else GOAL_COORDS_15


def misplaced_tiles(state: PuzzleState) -> int:
    """
    h_1(n): Number of misplaced tiles compared to the goal state.
    Blank tile (0) is excluded.
    Admissible and consistent.
    """
    goal = state.goal_state
    misplaced = 0
    for i, tile in enumerate(state.board):
        if tile != 0 and tile != goal[i]:
            misplaced += 1
    return misplaced


def manhattan_distance(state: PuzzleState) -> int:
    """
    h_2(n): Sum of the absolute horizontal and vertical distances
    of each tile from its target position.
    Blank tile (0) is excluded.
    Admissible and consistent.
    """
    coords = get_goal_coords(state.size)
    size = state.size
    dist = 0
    for idx, tile in enumerate(state.board):
        if tile != 0:
            current_r, current_c = divmod(idx, size)
            goal_r, goal_c = coords[tile]
            dist += abs(current_r - goal_r) + abs(current_c - goal_c)
    return dist


def euclidean_distance(state: PuzzleState) -> float:
    """
    h_3(n): Straight-line Euclidean distance for each tile to its target.
    Blank tile (0) is excluded.
    Admissible since Euclidean <= Manhattan <= True Cost.
    """
    coords = get_goal_coords(state.size)
    size = state.size
    dist = 0.0
    for idx, tile in enumerate(state.board):
        if tile != 0:
            current_r, current_c = divmod(idx, size)
            goal_r, goal_c = coords[tile]
            dist += math.sqrt((current_r - goal_r) ** 2 + (current_c - goal_c) ** 2)
    return dist


def linear_conflict(state: PuzzleState) -> int:
    """
    h_4(n): Manhattan Distance + 2 * (linear conflicts in rows + linear conflicts in cols).
    A linear conflict occurs when two tiles tj and tk are in the same line (row or column),
    both have their goals in that same line, tj is ahead of tk, but tj's goal is behind tk's goal.
    One tile must move out of the line and back, adding at least 2 moves.
    Strictly dominates Manhattan Distance while remaining fully admissible!
    """
    coords = get_goal_coords(state.size)
    size = state.size
    base_manhattan = 0
    conflicts = 0

    # Row analysis
    for r in range(size):
        row_tiles = []
        for c in range(size):
            tile = state.board[r * size + c]
            if tile != 0:
                gr, gc = coords[tile]
                base_manhattan += abs(r - gr) + abs(c - gc)
                if gr == r:
                    # Tile belongs in this row
                    row_tiles.append((tile, c, gc))

        # Check for linear conflicts in this row
        n_row = len(row_tiles)
        for i in range(n_row):
            for j in range(i + 1, n_row):
                # i is to the left of j in the row (c_i < c_j)
                # conflict if goal of i is to the right of goal of j (gc_i > gc_j)
                if row_tiles[i][2] > row_tiles[j][2]:
                    conflicts += 1

    # Column analysis
    for c in range(size):
        col_tiles = []
        for r in range(size):
            tile = state.board[r * size + c]
            if tile != 0:
                gr, gc = coords[tile]
                if gc == c:
                    # Tile belongs in this column
                    col_tiles.append((tile, r, gr))

        # Check for linear conflicts in this column
        n_col = len(col_tiles)
        for i in range(n_col):
            for j in range(i + 1, n_col):
                # i is above j (r_i < r_j)
                # conflict if goal of i is below goal of j (gr_i > gr_j)
                if col_tiles[i][2] > col_tiles[j][2]:
                    conflicts += 1

    return base_manhattan + (2 * conflicts)


HEURISTIC_MAP: Dict[str, Callable[[PuzzleState], float]] = {
    "manhattan": manhattan_distance,
    "linear_conflict": linear_conflict,
    "misplaced": misplaced_tiles,
    "euclidean": euclidean_distance
}

HEURISTIC_DESCRIPTIONS: Dict[str, dict] = {
    "manhattan": {
        "name": "Manhattan Distance",
        "formula": "Sum of |x_curr - x_goal| + |y_curr - y_goal|",
        "admissible": True,
        "consistent": True,
        "dominance": "Standard benchmark, strictly dominates Misplaced Tiles."
    },
    "linear_conflict": {
        "name": "Linear Conflict + Manhattan",
        "formula": "Manhattan + 2 * (Number of Row/Col Conflicts)",
        "admissible": True,
        "consistent": True,
        "dominance": "Strongest heuristic, strictly dominates standard Manhattan Distance."
    },
    "misplaced": {
        "name": "Misplaced Tiles",
        "formula": "Count of tiles where tile != goal_tile",
        "admissible": True,
        "consistent": True,
        "dominance": "Simple, admissible, but expands significantly more nodes than Manhattan."
    },
    "euclidean": {
        "name": "Euclidean Distance",
        "formula": "Sum of sqrt((x_curr - x_goal)^2 + (y_curr - y_goal)^2)",
        "admissible": True,
        "consistent": True,
        "dominance": "Admissible, but lower than Manhattan so explores more nodes."
    }
}
