"""
Unit tests for AI Puzzle Solver algorithms and core mechanics.
"""
import unittest
from core.puzzle import PuzzleState, GOAL_8, GOAL_15
from core.heuristics import misplaced_tiles, manhattan_distance, linear_conflict
from algorithms import (
    AStarSearch, BreadthFirstSearch, GreedyBestFirstSearch,
    IDAStarSearch, IterativeDeepeningDFS
)
from presets import PRESETS

class TestPuzzleCore(unittest.TestCase):
    def test_goal_recognition(self):
        goal = PuzzleState(GOAL_8, 3)
        self.assertTrue(goal.is_goal())
        self.assertTrue(goal.is_solvable())
        self.assertEqual(goal.count_inversions(), 0)

    def test_solvability_parity(self):
        # Unsolvable demo (odd inversions for 3x3)
        unsolvable = PuzzleState(tuple(PRESETS["unsolvable_demo"]["board"]), 3)
        self.assertFalse(unsolvable.is_solvable())
        self.assertEqual(unsolvable.count_inversions() % 2, 1)

        # Solvable preset
        solvable = PuzzleState(tuple(PRESETS["easy_6_moves"]["board"]), 3)
        self.assertTrue(solvable.is_solvable())

    def test_neighbors_validity(self):
        # Blank in center (index 4) should have 4 neighbors
        center_blank = PuzzleState((1, 2, 3, 4, 0, 5, 6, 7, 8), 3)
        neighbors = center_blank.get_neighbors()
        self.assertEqual(len(neighbors), 4)

        # Blank in top-left corner (index 0) should have 2 neighbors
        corner_blank = PuzzleState((0, 1, 2, 3, 4, 5, 6, 7, 8), 3)
        self.assertEqual(len(corner_blank.get_neighbors()), 2)

    def test_heuristics_properties(self):
        goal = PuzzleState(GOAL_8, 3)
        self.assertEqual(misplaced_tiles(goal), 0)
        self.assertEqual(manhattan_distance(goal), 0)
        self.assertEqual(linear_conflict(goal), 0)

        # Linear conflict state: tiles 2 and 1 in row 0 swapped -> (2, 1, 3, 4, 5, 6, 7, 8, 0)
        swapped = PuzzleState((2, 1, 3, 4, 5, 6, 7, 8, 0), 3)
        man = manhattan_distance(swapped)
        lc = linear_conflict(swapped)
        # Linear conflict should be strictly greater than Manhattan
        self.assertGreater(lc, man)


class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.state_2 = PuzzleState(tuple(PRESETS["very_easy_2_moves"]["board"]), 3)
        self.state_6 = PuzzleState(tuple(PRESETS["easy_6_moves"]["board"]), 3)

    def test_astar_linear_conflict_optimal(self):
        solver = AStarSearch(heuristic_name="linear_conflict")
        res = solver.solve(self.state_6)
        self.assertTrue(res.success)
        self.assertEqual(res.cost, 6)

    def test_astar_manhattan_optimal(self):
        solver = AStarSearch(heuristic_name="manhattan")
        res = solver.solve(self.state_6)
        self.assertTrue(res.success)
        self.assertEqual(res.cost, 6)

    def test_bfs_optimal(self):
        solver = BreadthFirstSearch()
        res = solver.solve(self.state_6)
        self.assertTrue(res.success)
        self.assertEqual(res.cost, 6)

    def test_greedy_finds_solution(self):
        solver = GreedyBestFirstSearch(heuristic_name="manhattan")
        res = solver.solve(self.state_2)
        self.assertTrue(res.success)
        self.assertGreaterEqual(res.cost, 2)

    def test_idastar_optimal(self):
        solver = IDAStarSearch(heuristic_name="manhattan")
        res = solver.solve(self.state_2)
        self.assertTrue(res.success)
        self.assertEqual(res.cost, 2)

    def test_iddfs_optimal(self):
        solver = IterativeDeepeningDFS(max_limit=10)
        res = solver.solve(self.state_2)
        self.assertTrue(res.success)
    def test_astar_euclidean_optimal(self):
        solver = AStarSearch(heuristic_name="euclidean")
        res = solver.solve(self.state_2)
        self.assertTrue(res.success)
        self.assertEqual(res.cost, 2)

    def test_idastar_linear_conflict_optimal(self):
        solver = IDAStarSearch(heuristic_name="linear_conflict")
        res = solver.solve(self.state_2)
        self.assertTrue(res.success)
        self.assertEqual(res.cost, 2)

    def test_dfs_finds_path(self):
        from algorithms.dfs import DepthFirstSearch
        solver = DepthFirstSearch(max_depth=10)
        res = solver.solve(self.state_2)
        self.assertTrue(res.success)
        self.assertGreaterEqual(res.cost, 2)

    def test_15_puzzle_solve(self):
        state_15 = PuzzleState(tuple(PRESETS["15_puzzle_easy"]["board"]), 4)
        solver = AStarSearch(heuristic_name="manhattan")
        res = solver.solve(state_15)
        self.assertTrue(res.success)
        self.assertEqual(res.cost, 2)

    def test_presets_integrity(self):
        for key, p in PRESETS.items():
            state = PuzzleState(tuple(p["board"]), p["size"])
            if p["difficulty"] == "Unsolvable":
                self.assertFalse(state.is_solvable(), f"{key} should be unsolvable")
            else:
                self.assertTrue(state.is_solvable(), f"{key} should be solvable")

if __name__ == "__main__":
    unittest.main()

