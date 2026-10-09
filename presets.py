"""
Curated puzzle presets of varying difficulty levels for demonstration and testing.
All optimal move costs are mathematically verified.
"""

PRESETS = {
    "very_easy_2_moves": {
        "name": "Very Easy (2 moves)",
        "difficulty": "Easy",
        "size": 3,
        "board": [1, 2, 3, 4, 5, 6, 0, 7, 8],
        "optimal_moves": 2,
        "description": "Requires only 2 moves. Ideal for rapid algorithm sanity checks."
    },
    "easy_6_moves": {
        "name": "Easy (6 moves)",
        "difficulty": "Easy",
        "size": 3,
        "board": [4, 1, 3, 2, 0, 5, 7, 8, 6],
        "optimal_moves": 6,
        "description": "Solvable by all algorithms (including BFS and DFS) in < 10ms."
    },
    "medium_8_moves": {
        "name": "Medium (8 moves)",
        "difficulty": "Medium",
        "size": 3,
        "board": [2, 5, 3, 1, 7, 6, 4, 8, 0],
        "optimal_moves": 8,
        "description": "Ideal for side-by-side benchmark comparison."
    },
    "medium_12_moves": {
        "name": "Medium-Hard (12 moves)",
        "difficulty": "Medium",
        "size": 3,
        "board": [5, 2, 3, 1, 8, 4, 0, 7, 6],
        "optimal_moves": 12,
        "description": "Noticeable branching explosion in BFS vs. A* Search."
    },
    "medium_18_moves": {
        "name": "Medium-Hard (18 moves)",
        "difficulty": "Medium",
        "size": 3,
        "board": [8, 7, 2, 5, 3, 6, 1, 4, 0],
        "optimal_moves": 18,
        "description": "Noticeable contrast between uninformed BFS and heuristic A* Search."
    },
    "hard_20_moves": {
        "name": "Hard (20 moves)",
        "difficulty": "Hard",
        "size": 3,
        "board": [7, 2, 4, 5, 0, 6, 8, 3, 1],
        "optimal_moves": 20,
        "description": "Demonstrates why Linear Conflict A* outclasses Misplaced Tiles."
    },
    "extreme_31_moves": {
        "name": "Worst-Case 8-Puzzle (31 moves)",
        "difficulty": "Expert",
        "size": 3,
        "board": [8, 6, 7, 2, 5, 4, 3, 0, 1],
        "optimal_moves": 31,
        "description": "Diameter of the 8-puzzle state graph (maximum possible optimal moves = 31)."
    },
    "unsolvable_demo": {
        "name": "Unsolvable Demo (Odd Inversions)",
        "difficulty": "Unsolvable",
        "size": 3,
        "board": [1, 2, 3, 4, 5, 6, 8, 7, 0],
        "optimal_moves": -1,
        "description": "Tiles 7 and 8 are swapped. Inversion count = 1 (Odd), provably impossible to solve!"
    },
    "15_puzzle_easy": {
        "name": "15-Puzzle (4x4 - 2 moves)",
        "difficulty": "Easy",
        "size": 4,
        "board": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0, 14, 15],
        "optimal_moves": 2,
        "description": "4x4 puzzle demonstration state (2 moves)."
    },
    "15_puzzle_4_moves": {
        "name": "15-Puzzle (4x4 - 4 moves)",
        "difficulty": "Medium",
        "size": 4,
        "board": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 11, 13, 0, 14, 12],
        "optimal_moves": 4,
        "description": "4x4 puzzle demonstration state (4 moves)."
    },
    "15_puzzle_6_moves": {
        "name": "15-Puzzle (4x4 - 6 moves)",
        "difficulty": "Medium",
        "size": 4,
        "board": [1, 2, 3, 4, 9, 5, 6, 8, 0, 10, 7, 12, 13, 14, 11, 15],
        "optimal_moves": 6,
        "description": "4x4 puzzle demonstration state (6 moves)."
    }
}

