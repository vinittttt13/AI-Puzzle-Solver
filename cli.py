"""
Interactive Command-Line Interface (CLI) for AI Puzzle Solver.
Ideal for viva demonstrations, headless testing, and benchmarking.
"""
import sys
import time
from core.puzzle import PuzzleState, generate_random_puzzle, generate_puzzle_by_shuffling
from core.heuristics import HEURISTIC_DESCRIPTIONS
from algorithms import get_algorithm, ALGORITHM_REGISTRY, ALGORITHM_METADATA
from benchmark import run_benchmark
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
    print("=" * 65)
    print("      AI N-PUZZLE SOLVER - ARTIFICIAL INTELLIGENCE MINOR PROJECT")
    print("=" * 65)

    while True:
        print("\nMain Menu:")
        print("1. Choose a Curated Preset")
        print("2. Generate Random Solvable Puzzle")
        print("3. Input Custom Board")
        print("4. Compare All Algorithms (Benchmark)")
        print("5. Theory & Heuristics Information")
        print("6. Exit")

        choice = input("\nEnter choice (1-6): ").strip()
        if choice == "6":
            print("Exiting AI Puzzle Solver. Good luck with your project presentation!")
            break

        state = None

        if choice == "1":
            print("\nAvailable Presets:")
            for i, (key, p) in enumerate(PRESETS.items(), 1):
                print(f"  {i}. [{p['difficulty']}] {p['name']} - {p['description']}")
            preset_idx = input("Select preset (number): ").strip()
            try:
                preset_key = list(PRESETS.keys())[int(preset_idx) - 1]
                p = PRESETS[preset_key]
                state = PuzzleState(tuple(p["board"]), p["size"])
            except Exception:
                print("Invalid choice, defaulting to Easy preset.")
                state = PuzzleState(tuple(PRESETS["easy_6_moves"]["board"]), 3)

        elif choice == "2":
            size_choice = input("Select puzzle size (3 for 8-puzzle, 4 for 15-puzzle) [Default: 3]: ").strip()
            size = 4 if size_choice == "4" else 3
            moves = input("Number of random shuffle steps (e.g. 10 to 30) [Default: 15]: ").strip()
            moves = int(moves) if moves.isdigit() else 15
            state = generate_puzzle_by_shuffling(steps=moves, size=size)
            print(f"Generated {size}x{size} puzzle by {moves} random valid moves from goal state.")

        elif choice == "3":
            print("\nEnter space-separated numbers (0-8 for 8-puzzle, 0 represents blank):")
            print("Example: 1 2 3 4 0 5 7 8 6")
            inp = input("Board: ").strip()
            try:
                nums = [int(x) for x in inp.split()]
                size = 3 if len(nums) == 9 else 4 if len(nums) == 16 else None
                if not size:
                    print("Error: Board must have exactly 9 (3x3) or 16 (4x4) numbers.")
                    continue
                state = PuzzleState(tuple(nums), size)
            except Exception as e:
                print(f"Invalid input: {e}")
                continue

        elif choice == "4":
            print("\nSelect board for benchmark:")
            print("1. Easy Preset (6 moves)")
            print("2. Medium Preset (12 moves)")
            print("3. Medium-Hard Preset (18 moves)")
            b_choice = input("Choice (1-3) [Default 1]: ").strip()
            key = "easy_6_moves" if b_choice == "1" else "medium_12_moves" if b_choice == "2" else "medium_18_moves"
            p = PRESETS[key]
            state = PuzzleState(tuple(p["board"]), p["size"])
            print_board(state, f"Benchmarking on {p['name']}")
            print("\nRunning benchmark across informed and uninformed algorithms...")
            bench = run_benchmark(state, timeout_sec=6.0)

            print("\n" + "=" * 90)
            print(f"{'Algorithm':<32} | {'Cost':<5} | {'Expanded':<9} | {'Peak Mem':<9} | {'Time (ms)':<10} | {'Optimal'}")
            print("-" * 90)
            for res in bench["benchmark_results"]:
                opt_str = "YES" if res["is_optimal"] else "NO"
                if res["success"]:
                    print(f"{res['algorithm_name']:<32} | {res['cost']:<5} | {res['nodes_expanded']:<9} | {res['max_frontier_size']:<9} | {res['execution_time_ms']:<10.2f} | {opt_str}")
                else:
                    print(f"{res['algorithm_name']:<32} | FAILED / TIMEOUT ({res.get('error_message', 'Exceeded limit')})")
            print("=" * 90)
            continue

        elif choice == "5":
            print("\n" + "=" * 60)
            print("          HEURISTIC & ALGORITHM THEORY FOR VIVA")
            print("=" * 60)
            for k, h in HEURISTIC_DESCRIPTIONS.items():
                print(f"\nHeuristic: {h['name']}")
                print(f"  Formula:    {h['formula']}")
                print(f"  Properties: Admissible={h['admissible']}, Consistent={h['consistent']}")
                print(f"  Notes:      {h['dominance']}")
            print("\n" + "=" * 60)
            print("ALGORITHMS COMPLEXITY SUMMARY:")
            print("-" * 60)
            for k, a in ALGORITHM_METADATA.items():
                print(f"• {a['name']}: Time {a['time_complexity']} | Space {a['space_complexity']} | Optimal: {a['optimal']}")
            continue

        if not state:
            continue

        print_board(state, "Initial Puzzle State")
        details = state.solvability_details()
        print(f"Solvability Check: {'SOLVABLE' if details['is_solvable'] else 'UNSOLVABLE'}")
        print(f"Analysis: {details['reason']}")

        if not details["is_solvable"]:
            print("[WARNING] Notice: Because of odd inversion parity, this board cannot be solved to standard goal state.")
            continue

        print("\nSelect Search Algorithm:")
        alg_keys = [
            ("astar_linear_conflict", "A* Search (Linear Conflict + Manhattan) [Fastest & Optimal]"),
            ("astar_manhattan", "A* Search (Manhattan Distance) [Classic Optimal]"),
            ("astar_misplaced", "A* Search (Misplaced Tiles) [Admissible]"),
            ("astar_euclidean", "A* Search (Euclidean Distance) [Admissible]"),
            ("greedy_manhattan", "Greedy Best-First Search (Manhattan) [Greedy/Sub-optimal]"),
            ("bfs", "Breadth-First Search (BFS) [Uninformed Optimal]"),
            ("idastar_linear_conflict", "IDA* Search (Linear Conflict) [O(d) Linear Space Optimal]"),
            ("idastar_manhattan", "IDA* Search (Manhattan Distance) [O(d) Linear Space Optimal]"),
            ("iddfs", "Iterative Deepening DFS (IDDFS) [Uninformed Optimal]"),
            ("dfs", "Depth-First Search (DFS) [Depth-Limited 25]")
        ]

        for i, (k, label) in enumerate(alg_keys, 1):
            print(f"  {i}. {label}")

        alg_choice = input(f"Select algorithm (1-{len(alg_keys)}) [Default 1]: ").strip()
        try:
            chosen_key = alg_keys[int(alg_choice) - 1][0]
        except Exception:
            chosen_key = "astar_linear_conflict"

        print(f"\nSolving using {chosen_key}...")
        solver = get_algorithm(chosen_key)
        start_t = time.perf_counter()
        result = solver.solve(state, timeout_sec=10.0)
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
        print(f"Max Frontier Size:   {result.max_frontier_size}")
        print(f"Execution Time:      {result.execution_time_ms:.2f} ms")
        print(f"Action Sequence:     {' -> '.join(result.actions[:15])}{' ...' if len(result.actions) > 15 else ''}")
        print("=" * 50)

        step_by_step = input("\nWould you like to step through the solution visually? (y/n) [Default n]: ").strip().lower()
        if step_by_step == 'y':
            for step_num, step_state in enumerate(result.path):
                act = result.actions[step_num - 1] if step_num > 0 else "START"
                print_board(step_state, f"Step {step_num}/{result.cost} [Move: {act}]")
                if step_num < len(result.path) - 1:
                    input("Press Enter for next move...")
            print("\n[SUCCESS] Puzzle Solved!")

if __name__ == "__main__":
    run_cli_solver()
