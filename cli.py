"""
Interactive Command-Line Interface (CLI) for AI 8-Puzzle Solver.
Designed for 5th Semester Artificial Intelligence Minor Project.
"""
import sys
import time
from core.puzzle import PuzzleState, generate_puzzle_by_shuffling
from algorithms import get_algorithm, ALGORITHM_METADATA
from presets import PRESETS

def print_board(state: PuzzleState, header: str = ""):
    if header:
        print(f"\n--- {header} ---")
    size = state.size
    line = "+----" * size + "+"
    print(line)
    for r in range(size):
        row_str = "| "
        for c in range(size):
            val = state.board[r * size + c]
            if val == 0:
                row_str += " .  | "
            else:
                row_str += f"{val:2d}  | "
        print(row_str)
        print(line)

def run_cli_solver():
    print("=" * 60)
    print("      AI 8-PUZZLE SOLVER - 5th SEMESTER AI PROJECT")
    print("=" * 60)

    while True:
        print("\nMain Menu:")
        print("1. Choose a Curated Preset")
        print("2. Generate Random Solvable Puzzle (Shuffle)")
        print("3. Input Custom 8-Puzzle Board")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()
        if choice == "4":
            print("Exiting AI Puzzle Solver. Goodbye!")
            break

        state = None

        if choice == "1":
            print("\nAvailable Presets:")
            preset_items = [
                ("very_easy_2_moves", "Very Easy (2 moves)"),
                ("easy_6_moves", "Easy (6 moves)"),
                ("medium_8_moves", "Medium (8 moves)"),
                ("medium_12_moves", "Medium-Hard (12 moves)"),
                ("hard_20_moves", "Hard (20 moves)"),
                ("unsolvable_demo", "Unsolvable Parity Test")
            ]
            for i, (key, label) in enumerate(preset_items, 1):
                p = PRESETS.get(key, {})
                print(f"  {i}. {label} - {p.get('description', '')}")
            preset_idx = input("Select preset (1-6): ").strip()
            try:
                preset_key = preset_items[int(preset_idx) - 1][0]
                p = PRESETS[preset_key]
                state = PuzzleState(tuple(p["board"]), p["size"])
            except Exception:
                print("Invalid choice, defaulting to Easy preset.")
                state = PuzzleState(tuple(PRESETS["easy_6_moves"]["board"]), 3)

        elif choice == "2":
            moves = input("Number of random shuffle steps (e.g. 5 to 25) [Default: 12]: ").strip()
            moves = int(moves) if moves.isdigit() else 12
            state = generate_puzzle_by_shuffling(steps=moves, size=3)
            print(f"Generated 8-puzzle by {moves} random valid moves from goal state.")

        elif choice == "3":
            print("\nEnter 9 space-separated numbers (0-8, where 0 represents blank):")
            print("Example: 1 2 3 4 0 5 7 8 6")
            inp = input("Board: ").strip()
            try:
                nums = [int(x) for x in inp.split()]
                if len(nums) != 9 or set(nums) != set(range(9)):
                    print("Error: Board must contain exactly numbers 0 to 8 without duplicates.")
                    continue
                state = PuzzleState(tuple(nums), 3)
            except Exception as e:
                print(f"Invalid input: {e}")
                continue

        if not state:
            continue

        print_board(state, "Initial Board State")
        details = state.solvability_details()
        print(f"Solvability Check: {'SOLVABLE' if details['is_solvable'] else 'UNSOLVABLE'}")
        print(f"Reason: {details['reason']}")

        if not details["is_solvable"]:
            print("\n[NOTE] Puzzle cannot be solved due to odd inversion parity.")
            continue

        print("\nSelect Search Algorithm:")
        alg_options = [
            ("astar_manhattan", "A* Search (Manhattan Distance) [Optimal]"),
            ("astar_linear_conflict", "A* Search (Linear Conflict) [Highest Pruning]"),
            ("astar_misplaced", "A* Search (Misplaced Tiles) [Optimal]"),
            ("idastar_manhattan", "IDA* Search (Manhattan Distance) [Optimal, O(d) Memory]"),
            ("bfs", "Breadth-First Search (BFS) [Optimal]"),
            ("iddfs", "Iterative Deepening DFS (IDDFS) [Optimal]"),
            ("dfs", "Depth-First Search (DFS) [Depth-Limited 25]"),
            ("greedy_manhattan", "Greedy Best-First Search [Heuristic Fast]")
        ]

        for i, (k, label) in enumerate(alg_options, 1):
            print(f"  {i}. {label}")

        alg_choice = input(f"Select algorithm (1-{len(alg_options)}) [Default 1]: ").strip()
        try:
            chosen_key = alg_options[int(alg_choice) - 1][0]
        except Exception:
            chosen_key = "astar_manhattan"

        print(f"\nSolving using {chosen_key}...")
        solver = get_algorithm(chosen_key)
        start_t = time.perf_counter()
        result = solver.solve(state, timeout_sec=8.0)
        elapsed = time.perf_counter() - start_t

        if not result.success:
            print(f"\n[ERROR] Solve failed: {result.error_message}")
            continue

        print("\n" + "=" * 50)
        print("          SOLUTION METRICS")
        print("=" * 50)
        print(f"Algorithm:           {result.algorithm_name}")
        print(f"Optimal Solution:    {'YES' if result.is_optimal else 'NO'}")
        print(f"Total Moves (Cost):  {result.cost}")
        print(f"Nodes Expanded:      {result.nodes_expanded}")
        print(f"Execution Time:      {result.execution_time_ms:.2f} ms")
        print(f"Action Sequence:     {' -> '.join(result.actions)}")
        print("=" * 50)

        step_by_step = input("\nStep through the solution path? (y/n) [Default y]: ").strip().lower()
        if step_by_step != 'n':
            for step_num, step_state in enumerate(result.path):
                act = result.actions[step_num - 1] if step_num > 0 else "START"
                print_board(step_state, f"Step {step_num}/{result.cost} [Action: {act}]")
                if step_num < len(result.path) - 1:
                    input("Press Enter for next step...")
            print("\n🎉 Puzzle Solved Successfully!")

if __name__ == "__main__":
    run_cli_solver()
