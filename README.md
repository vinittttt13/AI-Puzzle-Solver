# 🧩 AI 8-Puzzle Solver

> **Artificial Intelligence Minor Project &bull; 5th Semester &bull; Project-Based Learning (PBL)**  
> An interactive visual state-space search platform demonstrating informed heuristic and uninformed search algorithms on the classic 8-puzzle problem.

---

## 🌟 Project Overview

The **8-Puzzle** ($3 \times 3$ grid with 8 numbered tiles and 1 empty space) is the classic problem in Artificial Intelligence used to study:
- **State-space formulation & representation**
- **Uninformed search algorithms (BFS, DFS)**
- **Informed / Heuristic search algorithms (A*, Greedy Best-First)**
- **Admissible heuristic functions (Manhattan Distance, Misplaced Tiles)**
- **Solvability verification via Inversion Parity**

This project provides:
1. **Interactive Web Dashboard**: Beautiful visual board with step-by-step solution playback, timeline scrubbing, speed control, and manual tile sliding.
2. **Interactive Terminal CLI**: Command-line solver with step-by-step ASCII visualizations.
3. **Core AI Algorithms**: Limited strictly to standard undergraduate AI syllabus algorithms.

---

## 🚀 Key Features

- **Standard 8-Puzzle ($3 \times 3$)**: Focused directly on the classic syllabus problem.
- **5 Core Search Algorithms**:
  - **A\* Search (Manhattan Distance)**: Guaranteed optimal solution using $f(n) = g(n) + h(n)$ with $h_2(n)$.
  - **A\* Search (Misplaced Tiles)**: Guaranteed optimal solution using $h_1(n)$.
  - **Breadth-First Search (BFS)**: Uninformed search guaranteeing the shortest path.
  - **Depth-First Search (DFS)**: Uninformed search with depth-limiting to prevent cycles.
  - **Greedy Best-First Search**: Heuristic search using $f(n) = h(n)$ for fast exploration.
- **Mathematical Solvability Analysis**: Instant verification using the **Inversion Parity Theorem** before invoking any search algorithm.
- **Step-by-Step Solution Playback**:
  - Play / Pause animation
  - Scrubbing slider across solution steps
  - Action pills highlighting moves (`UP`, `DOWN`, `LEFT`, `RIGHT`)
- **Manual Game Mode**: Slide tiles directly by clicking or using Arrow Keys / WASD.
- **Performance Metrics**: Direct measurement of Solution Moves, Nodes Expanded, Execution Time (ms), and Peak Memory.

---

## 🏗️ Project Architecture

```
AI 5th sem/
├── core/
│   ├── puzzle.py            # Board representation, state transitions, solvability math
│   └── heuristics.py        # Manhattan Distance & Misplaced Tiles heuristics
├── algorithms/
│   ├── base.py              # SearchAlgorithm abstract base class & SearchResult model
│   ├── astar.py             # A* Graph Search with Priority Queue (heapq)
│   ├── bfs.py               # Breadth-First Search (FIFO queue)
│   ├── dfs.py               # Depth-Limited Depth-First Search
│   ├── greedy.py            # Greedy Best-First Search
│   └── __init__.py          # Algorithm Registry & metadata
├── static/
│   ├── index.html           # Clean, single-view puzzle solver UI
│   ├── style.css            # Glassmorphic CSS design system
│   └── script.js            # Board rendering, playback engine, API integration
├── tests/
│   ├── test_solver.py       # Core logic, heuristics & algorithm unit tests
│   └── test_api.py          # FastAPI endpoint tests
├── server.py                # FastAPI backend server
├── cli.py                   # Interactive Terminal CLI
├── run.py                   # Universal launcher script (Web / CLI / Tests)
├── run.bat                  # One-click Windows batch launcher
└── requirements.txt         # Project dependencies (FastAPI, Uvicorn)
```

---

## 📐 Mathematical Theory: Solvability & Inversion Parity

Not all randomly permuted 8-puzzle configurations can reach the goal state. Exactly **50% of all configurations are unreachable**.

An **inversion** is any pair of tiles $(A, B)$ such that $A > B$ and $A$ appears before $B$ in row-major order (ignoring the blank tile $0$).

- For an odd grid width ($3 \times 3$ 8-puzzle):
  - Every valid blank move changes the inversion count by an even number ($\Delta \in \{-2, 0, +2\}$).
  - Therefore, the **parity of inversions is an invariant**.
  - **Theorem**: An 8-puzzle state is solvable if and only if its number of inversions is **even**.

---

## 🧠 Heuristic Functions

1. **Misplaced Tiles ($h_1$)**:
   $$\text{Counts tiles } i \neq 0 \text{ such that current position } \neq \text{ goal position}$$
   - *Admissible*: Each misplaced tile requires at least 1 move.
   - *Consistent*: Satisfies the triangle inequality.

2. **Manhattan Distance ($h_2$)**:
   $$h_2(n) = \sum_{\text{tile } i = 1}^{8} \left( |r_i - r_{\text{goal}}| + |c_i - c_{\text{goal}}| \right)$$
   - *Admissible*: Each move changes Manhattan distance by at most 1.
   - *Dominance*: $h_2(n) \ge h_1(n)$ for all states $n$, meaning A* with Manhattan distance will always expand fewer or equal nodes than A* with Misplaced Tiles.

---

## 📊 Algorithms & Complexity Comparison

| Algorithm | Category | Heuristic | Optimality | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A\* Search** | Informed | Manhattan ($h_2$) | **Yes** | $O(b^d)$ | $O(b^d)$ |
| **A\* Search** | Informed | Misplaced ($h_1$) | **Yes** | $O(b^d)$ | $O(b^d)$ |
| **BFS** | Uninformed | None | **Yes** | $O(b^d)$ | $O(b^d)$ |
| **DFS** | Uninformed | None | No | $O(b^m)$ | $O(b \cdot m)$ |
| **Greedy Best-First** | Informed | Manhattan ($h_2$) | No | $O(b^m)$ | $O(b^m)$ |

---

## 💻 How to Run

### 1. Web Application (Recommended)
```bash
python run.py web
```
Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### 2. Terminal CLI
```bash
python run.py cli
```

### 3. Run Automated Tests
```bash
python run.py test
```
