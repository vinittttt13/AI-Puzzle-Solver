# 🧩 AI N-Puzzle Solver (8-Puzzle & 15-Puzzle)

> **Artificial Intelligence Minor Project &bull; 5th Semester &bull; Project-Based Learning (PBL)**  
> An interactive, high-performance state-space search platform demonstrating informed heuristic and uninformed search algorithms, mathematical solvability analysis, and empirical benchmarking.

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [System Architecture](#-system-architecture)
4. [Mathematical Theory & Solvability](#-mathematical-theory--solvability)
5. [Heuristic Functions & Dominance](#-heuristic-functions--dominance)
6. [Algorithms & Complexity Matrix](#-algorithms--complexity-matrix)
7. [Installation & Setup](#-installation--setup)
8. [How to Run](#-how-to-run)
9. [Viva & Oral Examination Guide](#-viva--oral-examination-guide)

---

## 🌟 Project Overview

The **N-Puzzle** (such as the 8-puzzle on a $3 \times 3$ grid and 15-puzzle on a $4 \times 4$ grid) is a classic problem in Artificial Intelligence for studying state-space representation, graph traversal, and heuristic evaluation. 

This project provides:
- A modern **Glassmorphic Web Dashboard** (FastAPI backend + Vanilla CSS frontend).
- An **Interactive Terminal CLI** tailored for viva demonstrations.
- **Empirical Benchmarking Arena** measuring execution time (ms), nodes expanded, peak memory frontier, and path optimality.
- Visual **Playback Controls** (step-by-step scrub, play/pause, speed selector).
- **Manual Game Mode** with keyboard (Arrow keys / WASD) and tile click interaction.

---

## 🚀 Key Features

- **8-Puzzle ($3 \times 3$) and 15-Puzzle ($4 \times 4$) Support**: Real-time dimension switching.
- **Solvability Diagnostics**: Instant mathematical verification using the **Inversion Parity Theorem** before running search.
- **6 Search Algorithms with 10 Heuristic Configurations**:
  - Informed: $A^*$, $\text{IDA}^*$ (Iterative Deepening $A^*$), Greedy Best-First.
  - Uninformed: Breadth-First Search (BFS), Depth-First Search (DFS), Iterative Deepening DFS (IDDFS).
- **Admissible Heuristics**: Manhattan Distance, Linear Conflict + Manhattan, Misplaced Tiles, Euclidean Distance.
- **Interactive Step Timeline**: Scrub through moves, see active move pills, and inspect states.
- **Benchmark Arena & Charts**: Side-by-side performance comparison with logarithmic Chart.js bar charts and CSV report export.
- **Custom Board Permutation Editor**: Live validation and error detection for custom puzzle states.
- **Viva Preparation Module**: Built-in tab with theoretical proofs, Big-O tables, and oral exam FAQs.

---

## 🏗️ System Architecture

```
AI 5th sem/
├── core/
│   ├── puzzle.py            # Board representation, state transitions, solvability math
│   └── heuristics.py        # Admissible & consistent heuristic implementations
├── algorithms/
│   ├── base.py              # SearchAlgorithm abstract base class & SearchResult model
│   ├── astar.py             # A* Graph Search with Priority Queue (heapq)
│   ├── idastar.py           # Iterative Deepening A* (O(d) linear memory)
│   ├── greedy.py            # Greedy Best-First Search
│   ├── bfs.py               # Breadth-First Search (FIFO queue)
│   ├── dfs.py               # Depth-Limited Depth-First Search
│   ├── iddfs.py             # Iterative Deepening DFS (BFS optimality + DFS space)
│   └── __init__.py          # Algorithm Registry and complexity metadata
├── static/
│   ├── index.html           # Modern responsive dashboard UI
│   ├── style.css            # Custom Vanilla CSS design system (Glassmorphism)
│   └── script.js            # Interactive board rendering, Chart.js, audio feedback
├── tests/
│   ├── test_solver.py       # Core logic, heuristics & algorithm unit tests
│   └── test_api.py          # FastAPI REST endpoint integration tests
├── app.py                   # FastAPI application entry point
├── server.py                # Web server backend with route definitions
├── benchmark.py             # Multi-algorithm batch benchmarking engine
├── presets.py               # Verified puzzle configurations (2 to 31 moves)
├── cli.py                   # Interactive Command-Line Interface
├── run.py                   # Universal launcher script (Web / CLI / Tests)
├── run.bat                  # One-click Windows batch launcher
└── requirements.txt         # Project dependencies
```

---

## 📐 Mathematical Theory & Solvability

### Problem Formulation
- **State Space**: Permutations of $\{0, 1, \dots, N^2 - 1\}$, where $0$ denotes the empty slot.
  - $3 \times 3$ (8-puzzle): $9! / 2 = 181,440$ reachable states.
  - $4 \times 4$ (15-puzzle): $16! / 2 \approx 1.046 \times 10^{13}$ reachable states.
- **Actions**: $\text{Move Blank} \in \{\text{UP}, \text{DOWN}, \text{LEFT}, \text{RIGHT}\}$ within grid boundaries.
- **Path Cost**: Uniform unit cost $c(n, a, n') = 1$ per move. Total cost equals path length.

### Inversion Parity Theorem
Not all puzzle states can reach the goal. Exactly 50% of all random permutations are unreachable.

An **inversion** occurs when a tile $A$ precedes tile $B$ in linear row-major order, but $A > B$ (ignoring the blank tile $0$).

1. **Odd Grid Width ($3 \times 3$ 8-Puzzle)**:
   - Horizontal moves preserve tile order (0 inversions changed).
   - Vertical moves shift a tile across 2 positions, altering inversions by $\Delta \in \{-2, 0, +2\}$.
   - Inversion parity is invariant. The standard goal state has 0 inversions (even).
   - **Condition**: A $3 \times 3$ state is **solvable iff its inversion count is EVEN**.

2. **Even Grid Width ($4 \times 4$ 15-Puzzle)**:
   - Vertical moves shift a tile across 3 positions, altering inversions by an odd number ($\pm 1$ or $\pm 3$).
   - **Condition**: Solvable iff `(inversions + blank_row_from_bottom) % 2 == 1` (where bottom row is index 1).

---

## 🎯 Heuristic Functions & Dominance

All heuristics implemented in this project are **admissible** ($h(n) \le h^*(n)$) and **consistent** ($h(n) \le c(n, a, n') + h(n')$):

| Heuristic | Formula | Dominance | Description |
|---|---|---|---|
| **Misplaced Tiles ($h_1$)** | $\sum [tile_i \ne goal_i]$ | Baseline | Counts number of tiles out of position. Simplest admissible heuristic. |
| **Euclidean Distance ($h_2$)** | $\sum \sqrt{\Delta r^2 + \Delta c^2}$ | Intermediate | Straight-line geometric distance. Admissible but expands more nodes than Manhattan. |
| **Manhattan Distance ($h_3$)** | $\sum (\|\Delta r\| + \|\Delta c\|)$ | Dominates $h_1, h_2$ | Grid taxicab distance for each tile to its target slot. Classic optimal heuristic. |
| **Linear Conflict ($h_4$)** | $h_3 + 2 \times \text{conflicts}$ | **Strictly Dominates $h_3$** | When 2 tiles are in their target line but inverted, one must move aside and back ($\ge 2$ extra moves). **Expands the fewest nodes**. |

---

## 📊 Algorithms & Complexity Matrix

| Algorithm | Type | Time Complexity | Space Complexity | Complete? | Optimal? |
|---|---|---|---|---|---|
| **A\* Search** | Informed | $O(b^d)$ | $O(b^d)$ | Yes | **Yes** (with admissible $h$) |
| **IDA\* Search** | Informed | $O(b^d)$ | $O(d)$ | Yes | **Yes** (Linear Space) |
| **Greedy Best-First** | Informed | $O(b^m)$ | $O(b^m)$ | No (cycles) | No (sub-optimal) |
| **Breadth-First (BFS)** | Uninformed | $O(b^d)$ | $O(b^d)$ | Yes | **Yes** (unit cost) |
| **IDDFS** | Uninformed | $O(b^d)$ | $O(bd)$ | Yes | **Yes** (Linear Space) |
| **Depth-First (DFS)** | Uninformed | $O(b^m)$ | $O(bm)$ | No (infinite/cyclic) | No |

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Modern Web Browser (Chrome, Edge, Firefox, Safari)

### 1. Clone or Download Repository
```bash
git clone <repository_url>
cd "AI 5th sem"
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### Option 1: Universal Launcher (Easiest)
```bash
python run.py
```
Or double-click `run.bat` on Windows.

### Option 2: Web Application Directly
```bash
python server.py
# or: uvicorn app:app --port 8000 --reload
```
Then open your browser at: **`http://127.0.0.1:8000`**

### Option 3: Interactive Terminal CLI
```bash
python cli.py
```

### Option 4: Automated Test Suite
```bash
python run.py test
# or: python -m unittest discover tests
```

---

## 🎓 Viva & Oral Examination Guide

### Q1: Why is $A^*$ search guaranteed to return the optimal path?
> **Answer:** $A^*$ expands nodes in order of $f(n) = g(n) + h(n)$. When $h(n)$ is admissible ($h(n) \le h^*(n)$), the goal node is only dequeued when its cost is less than or equal to any other potential path in the frontier, guaranteeing that the first goal popped is optimal.

### Q2: What is the difference between Admissibility and Consistency?
> **Answer:**
> - **Admissibility**: $h(n) \le h^*(n)$ for all $n$ (never overestimates).
> - **Consistency (Monotonicity)**: $h(n) \le c(n, a, n') + h(n')$ (satisfies triangle inequality).
> - Consistency is a stronger condition and implies admissibility. It guarantees that $f(n)$ values along any path are monotonically non-decreasing, so nodes never need to be re-opened once closed.

### Q3: Why does Linear Conflict strictly dominate Manhattan Distance?
> **Answer:** Two tiles $t_1$ and $t_2$ are in linear conflict if both belong in the same row/col, $t_1$ is positioned before $t_2$, but their goal positions require $t_2$ before $t_1$. Because tiles cannot jump over each other, one tile must step out of the line to let the other pass and step back in, requiring at least 2 additional moves. Since $h_{LC} = h_{Manhattan} + 2 \times \text{conflicts} \le h^*$, it is admissible and strictly greater than $h_{Manhattan}$.

### Q4: Why does IDA* outclass BFS for deep puzzle instances?
> **Answer:** BFS stores all explored nodes in memory ($O(b^d)$). At depth 20, BFS requires storing millions of states, exhausting RAM. IDA* uses depth-first iterations with threshold cutoffs, requiring only $O(d)$ memory (proportional to depth) while retaining completeness and optimality.

### Q5: Can any arbitrary 8-puzzle be solved?
> **Answer:** No. Tile moves preserve the parity of the permutation's inversion count. Exactly half ($181,440$) of all configurations have an odd inversion count and can never reach the standard goal state (which has 0 inversions, an even number).

---

## 👥 Contributors & Academic Acknowledgments
- **Course**: Artificial Intelligence (5th Semester)
- **Component**: Project-Based Learning (PBL) Minor Project
- Built with Python, FastAPI, Chart.js, and Vanilla CSS.
