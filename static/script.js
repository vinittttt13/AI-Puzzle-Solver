/**
 * AI 8-PUZZLE SOLVER - FRONTEND APPLICATION LOGIC
 * Designed for 5th Semester Artificial Intelligence Minor Project.
 * Focuses on interactive puzzle solving, step playback, and algorithm comparison.
 */

// Global Application State
const state = {
    size: 3,
    board: [4, 1, 3, 2, 0, 5, 7, 8, 6],
    initialBoard: [4, 1, 3, 2, 0, 5, 7, 8, 6],
    solutionPath: [],
    solutionActions: [],
    currentStep: 0,
    isPlaying: false,
    playTimer: null,
    playSpeed: 600,
    presets: {
        "easy_6_moves": { name: "Easy (6 moves)", difficulty: "Easy", size: 3, board: [4, 1, 3, 2, 0, 5, 7, 8, 6], optimal_moves: 6, description: "Solvable by all algorithms in < 10ms." },
        "very_easy_2_moves": { name: "Very Easy (2 moves)", difficulty: "Easy", size: 3, board: [1, 2, 3, 4, 5, 6, 0, 7, 8], optimal_moves: 2, description: "Requires only 2 moves. Ideal for rapid algorithm sanity checks." },
        "medium_8_moves": { name: "Medium (8 moves)", difficulty: "Medium", size: 3, board: [2, 5, 3, 1, 7, 6, 4, 8, 0], optimal_moves: 8, description: "Ideal for benchmark comparison." },
        "medium_12_moves": { name: "Medium-Hard (12 moves)", difficulty: "Medium", size: 3, board: [5, 2, 3, 1, 8, 4, 0, 7, 6], optimal_moves: 12, description: "Noticeable branching explosion in BFS vs. A* Search." },
        "medium_18_moves": { name: "Medium-Hard (18 moves)", difficulty: "Medium", size: 3, board: [8, 7, 2, 5, 3, 6, 1, 4, 0], optimal_moves: 18, description: "Noticeable contrast between uninformed BFS and heuristic A* Search." },
        "hard_20_moves": { name: "Hard (20 moves)", difficulty: "Hard", size: 3, board: [7, 2, 4, 5, 0, 6, 8, 3, 1], optimal_moves: 20, description: "Demonstrates why Linear Conflict A* outclasses Misplaced Tiles." },
        "extreme_31_moves": { name: "Worst-Case 8-Puzzle (31 moves)", difficulty: "Expert", size: 3, board: [8, 6, 7, 2, 5, 4, 3, 0, 1], optimal_moves: 31, description: "Diameter of the 8-puzzle state graph." },
        "unsolvable_demo": { name: "Unsolvable Demo (Odd Inversions)", difficulty: "Unsolvable", size: 3, board: [1, 2, 3, 4, 5, 6, 8, 7, 0], optimal_moves: -1, description: "Tiles 7 and 8 swapped. Inversion count = 1 (Odd), impossible to solve!" }
    },
    algorithmsMeta: {
        "astar_manhattan": { name: "A* Search (Manhattan Distance)", type: "Informed (Heuristic)", optimal: true, description: "Uses f(n) = g(n) + h(n) with Manhattan distance. Guarantees the shortest solution path while expanding minimal nodes." },
        "astar_linear_conflict": { name: "A* Search (Linear Conflict)", type: "Informed (Heuristic)", optimal: true, description: "Uses Manhattan distance + linear conflict penalty (+2 per conflict). Highly informed and admissible." },
        "astar_misplaced": { name: "A* Search (Misplaced Tiles)", type: "Informed (Heuristic)", optimal: true, description: "Uses f(n) = g(n) + h(n) with the count of misplaced tiles. Admissible heuristic guaranteeing optimal solution." },
        "astar_euclidean": { name: "A* Search (Euclidean Distance)", type: "Informed (Heuristic)", optimal: true, description: "Uses straight-line Euclidean distance heuristic. Admissible but less informed than Manhattan distance." },
        "idastar_manhattan": { name: "IDA* Search (Manhattan Distance)", type: "Informed (Heuristic)", optimal: true, description: "Iterative Deepening A* with Manhattan distance. Guarantees optimal path with O(d) linear memory." },
        "idastar_linear_conflict": { name: "IDA* Search (Linear Conflict)", type: "Informed (Heuristic)", optimal: true, description: "Iterative Deepening A* with Linear Conflict heuristic. High pruning power with minimal memory." },
        "greedy_manhattan": { name: "Greedy Best-First Search (Manhattan)", type: "Informed (Heuristic)", optimal: false, description: "Evaluates nodes solely by heuristic f(n) = h(n). Fast goal pursuit, but does not guarantee the shortest path." },
        "greedy_linear_conflict": { name: "Greedy Best-First Search (Linear Conflict)", type: "Informed (Heuristic)", optimal: false, description: "Greedy best-first search guided by linear conflict heuristic." },
        "bfs": { name: "Breadth-First Search (BFS)", type: "Uninformed (Blind)", optimal: true, description: "Explores states level-by-level using a FIFO queue. Guarantees the shortest path for unit step costs." },
        "iddfs": { name: "Iterative Deepening DFS (IDDFS)", type: "Uninformed (Blind)", optimal: true, description: "Combines DFS space efficiency with BFS optimality by iteratively increasing the depth limit." },
        "dfs": { name: "Depth-First Search (DFS)", type: "Uninformed (Blind)", optimal: false, description: "Explores deeply along each branch using a LIFO stack (depth-limited to avoid infinite loops)." }
    }
};

// ================= DOM ELEMENTS =================
const boardEl = document.getElementById("puzzle-board");
const presetSelect = document.getElementById("preset-select");
const algorithmSelect = document.getElementById("algorithm-select");
const timelineSlider = document.getElementById("timeline-slider");
const stepCounterLabel = document.getElementById("step-counter-label");
const actionPills = document.getElementById("action-pills");
const solvabilityBadge = document.getElementById("solvability-badge");
const solvabilityText = document.getElementById("solvability-text");
const inversionExplanationText = document.getElementById("inversion-explanation-text");
const previewHVal = document.getElementById("preview-h-val");

const btnPlay = document.getElementById("btn-play");
const playIcon = document.getElementById("play-icon");
const btnFirst = document.getElementById("btn-first");
const btnPrev = document.getElementById("btn-prev");
const btnNext = document.getElementById("btn-next");
const btnLast = document.getElementById("btn-last");
const btnSolve = document.getElementById("btn-solve");
const btnReset = document.getElementById("btn-reset");
const btnShuffle = document.getElementById("btn-shuffle");
const btnLoadPreset = document.getElementById("btn-load-preset");
const playbackSpeedSelect = document.getElementById("playback-speed");
const shuffleStepsInput = document.getElementById("shuffle-steps");
const shuffleStepsVal = document.getElementById("shuffle-steps-val");

// ================= INVERSION PARITY MATHEMATICS =================
function getSolvabilityLocally(board, size = 3) {
    let inv = 0;
    const tiles = board.filter(x => x !== 0);
    for (let i = 0; i < tiles.length; i++) {
        for (let j = i + 1; j < tiles.length; j++) {
            if (tiles[i] > tiles[j]) inv++;
        }
    }
    const solvable = (inv % 2 === 0);
    return {
        is_solvable: solvable,
        inversion_count: inv,
        reason: solvable
            ? `Inversion count is ${inv} (even). For a 3x3 puzzle, solvability requires an EVEN number of inversions.`
            : `Inversion count is ${inv} (odd). A 3x3 puzzle is mathematically impossible to solve with an odd number of inversions.`
    };
}

// ================= INITIALIZATION =================
function initApp() {
    renderBoard();
    setupEventListeners();
    checkBoardSolvability();
    fetchPresets();
    fetchAlgorithmsMeta();
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initApp);
} else {
    initApp();
}

// ================= EVENT LISTENERS =================
function setupEventListeners() {
    // Presets
    if (btnLoadPreset) btnLoadPreset.addEventListener("click", loadSelectedPreset);
    if (presetSelect) presetSelect.addEventListener("change", loadSelectedPreset);

    // Shuffle
    if (shuffleStepsInput && shuffleStepsVal) {
        shuffleStepsInput.addEventListener("input", (e) => {
            shuffleStepsVal.textContent = `${e.target.value} moves`;
        });
    }
    if (btnShuffle) btnShuffle.addEventListener("click", handleShuffle);

    // Algorithm selection
    if (algorithmSelect) algorithmSelect.addEventListener("change", updateAlgorithmInfo);

    // Solver Actions
    if (btnSolve) btnSolve.addEventListener("click", solveCurrentPuzzle);
    if (btnReset) btnReset.addEventListener("click", resetToInitial);

    // Playback Navigation
    if (btnPlay) btnPlay.addEventListener("click", togglePlayPause);
    if (btnFirst) btnFirst.addEventListener("click", () => { pauseSolution(); setPlaybackStep(0); });
    if (btnPrev) btnPrev.addEventListener("click", () => { pauseSolution(); setPlaybackStep(state.currentStep - 1); });
    if (btnNext) btnNext.addEventListener("click", () => { pauseSolution(); setPlaybackStep(state.currentStep + 1); });
    if (btnLast) btnLast.addEventListener("click", () => { pauseSolution(); setPlaybackStep(state.solutionPath.length - 1); });

    // Timeline Slider
    if (timelineSlider) {
        timelineSlider.addEventListener("input", (e) => {
            pauseSolution();
            setPlaybackStep(parseInt(e.target.value, 10));
        });
    }

    // Playback Speed
    if (playbackSpeedSelect) {
        playbackSpeedSelect.addEventListener("change", (e) => {
            state.playSpeed = parseInt(e.target.value, 10);
            if (state.isPlaying) {
                pauseSolution();
                playSolution();
            }
        });
    }

    // Keyboard controls for manual puzzle play
    document.addEventListener("keydown", (e) => {
        if (["ArrowUp", "KeyW"].includes(e.code)) {
            e.preventDefault();
            slideTileInDirection(1, 0); // tile below moves up into blank
        } else if (["ArrowDown", "KeyS"].includes(e.code)) {
            e.preventDefault();
            slideTileInDirection(-1, 0); // tile above moves down into blank
        } else if (["ArrowLeft", "KeyA"].includes(e.code)) {
            e.preventDefault();
            slideTileInDirection(0, 1); // tile to the right moves left into blank
        } else if (["ArrowRight", "KeyD"].includes(e.code)) {
            e.preventDefault();
            slideTileInDirection(0, -1); // tile to the left moves right into blank
        } else if (e.code === "Space" && state.solutionPath.length > 0) {
            e.preventDefault();
            togglePlayPause();
        }
    });
}

// ================= API CALLS & DATA FETCHING =================
async function fetchPresets() {
    try {
        const res = await fetch("/api/presets");
        if (!res.ok) return;
        const data = await res.json();
        state.presets = Object.assign({}, state.presets, data);

        if (presetSelect) {
            presetSelect.innerHTML = "";
            for (const [key, p] of Object.entries(state.presets)) {
                if (p.size === 3) {
                    const opt = document.createElement("option");
                    opt.value = key;
                    opt.textContent = `[${p.difficulty}] ${p.name}`;
                    if (key === "easy_6_moves") opt.selected = true;
                    presetSelect.appendChild(opt);
                }
            }
            presetSelect.value = "easy_6_moves";
        }
    } catch (e) {
        console.warn("Using offline presets fallback:", e);
    }
}

async function fetchAlgorithmsMeta() {
    try {
        const res = await fetch("/api/algorithms_meta");
        if (!res.ok) return;
        const data = await res.json();
        if (data.metadata) {
            state.algorithmsMeta = Object.assign({}, state.algorithmsMeta, data.metadata);
        }
        updateAlgorithmInfo();
    } catch (e) {
        console.warn("Using offline algorithm metadata:", e);
        updateAlgorithmInfo();
    }
}

function updateAlgorithmInfo() {
    if (!algorithmSelect) return;
    const selectedKey = algorithmSelect.value;
    const meta = state.algorithmsMeta[selectedKey];
    if (!meta) return;

    const catTag = document.getElementById("alg-category-tag");
    if (catTag) catTag.textContent = meta.type;

    const optTag = document.getElementById("alg-optimal-tag");
    if (optTag) {
        if (meta.optimal) {
            optTag.textContent = "Guaranteed Optimal";
            optTag.className = "info-tag opt-tag";
            optTag.style.background = "";
            optTag.style.color = "";
        } else {
            optTag.textContent = "Sub-optimal / Heuristic";
            optTag.className = "info-tag";
            optTag.style.background = "rgba(245, 158, 11, 0.15)";
            optTag.style.color = "var(--accent-amber)";
        }
    }

    const descEl = document.getElementById("alg-description-text");
    if (descEl) descEl.textContent = meta.description;
}

// ================= PUZZLE BOARD RENDERING & INTERACTION =================
function renderBoard() {
    if (!boardEl) return;
    boardEl.innerHTML = "";
    boardEl.className = "puzzle-board size-3";
    const emptyIdx = state.board.indexOf(0);
    const emptyR = Math.floor(emptyIdx / 3);
    const emptyC = emptyIdx % 3;

    state.board.forEach((tileVal, idx) => {
        const tile = document.createElement("div");
        const r = Math.floor(idx / 3);
        const c = idx % 3;

        if (tileVal === 0) {
            tile.className = "puzzle-tile empty-slot";
        } else {
            tile.className = "puzzle-tile";
            tile.textContent = tileVal;

            // Highlight if tile is in its target goal position (1-8)
            const targetR = Math.floor((tileVal - 1) / 3);
            const targetC = (tileVal - 1) % 3;
            if (r === targetR && c === targetC) {
                tile.classList.add("in-goal");
            }

            // Check if adjacent to blank space (clickable to slide manually)
            const isAdjacent = (Math.abs(r - emptyR) + Math.abs(c - emptyC)) === 1;
            if (isAdjacent) {
                tile.classList.add("clickable");
                tile.title = "Click to slide tile";
                tile.addEventListener("click", () => handleTileClick(idx, emptyIdx));
            }
        }
        boardEl.appendChild(tile);
    });

    updateHeuristicPreview();
    updateVictoryStatus();
}

function isCurrentStateGoal() {
    for (let i = 0; i < 8; i++) {
        if (state.board[i] !== i + 1) return false;
    }
    return state.board[8] === 0;
}

function updateVictoryStatus() {
    const banner = document.getElementById("victory-banner");
    if (!banner) return;
    if (isCurrentStateGoal()) {
        banner.classList.remove("hidden");
    } else {
        banner.classList.add("hidden");
    }
}

function handleTileClick(tileIdx, emptyIdx) {
    if (state.isPlaying) pauseSolution();

    // Swap tile and blank
    [state.board[tileIdx], state.board[emptyIdx]] = [state.board[emptyIdx], state.board[tileIdx]];
    renderBoard();
    checkBoardSolvability();

    // Clear previous computed solution since user altered board
    clearSolutionState();
}

function slideTileInDirection(dr, dc) {
    if (state.isPlaying) pauseSolution();
    const emptyIdx = state.board.indexOf(0);
    const emptyR = Math.floor(emptyIdx / 3);
    const emptyC = emptyIdx % 3;
    const targetR = emptyR + dr;
    const targetC = emptyC + dc;

    if (targetR >= 0 && targetR < 3 && targetC >= 0 && targetC < 3) {
        const targetIdx = targetR * 3 + targetC;
        handleTileClick(targetIdx, emptyIdx);
    }
}

function updateHeuristicPreview() {
    let manhattan = 0;
    state.board.forEach((tile, idx) => {
        if (tile !== 0) {
            const currR = Math.floor(idx / 3);
            const currC = idx % 3;
            const goalR = Math.floor((tile - 1) / 3);
            const goalC = (tile - 1) % 3;
            manhattan += Math.abs(currR - goalR) + Math.abs(currC - goalC);
        }
    });
    if (previewHVal) previewHVal.textContent = manhattan;
}

// ================= SOLVABILITY CHECK =================
async function checkBoardSolvability() {
    // 1. Immediately apply instant local parity calculation
    const local = getSolvabilityLocally(state.board, 3);
    if (solvabilityBadge) {
        solvabilityBadge.className = local.is_solvable ? "badge badge-success" : "badge badge-danger";
    }
    if (solvabilityText) {
        solvabilityText.textContent = local.is_solvable ? "Solvable" : "Unsolvable";
    }
    if (btnSolve) {
        btnSolve.disabled = !local.is_solvable;
    }
    if (inversionExplanationText) {
        inversionExplanationText.textContent = local.reason;
    }

    // 2. Also verify against backend API
    try {
        const res = await fetch("/api/check_solvability", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board: state.board, size: 3 })
        });
        if (!res.ok) return;
        const details = await res.json();

        if (details && typeof details.is_solvable === "boolean") {
            if (solvabilityBadge) {
                solvabilityBadge.className = details.is_solvable ? "badge badge-success" : "badge badge-danger";
            }
            if (solvabilityText) {
                solvabilityText.textContent = details.is_solvable ? "Solvable" : "Unsolvable";
            }
            if (btnSolve) {
                btnSolve.disabled = !details.is_solvable;
            }
            if (inversionExplanationText && details.reason) {
                inversionExplanationText.textContent = details.reason;
            }
        }
    } catch (e) {
        // Fallback already active via synchronous step 1
    }
}

// ================= SOLVE & PLAYBACK =================
async function solveCurrentPuzzle() {
    if (!algorithmSelect || !btnSolve) return;
    const algKey = algorithmSelect.value;
    btnSolve.disabled = true;
    btnSolve.innerHTML = '<span class="btn-icon">⏳</span> Solving...';
    const statusEl = document.getElementById("metrics-status");
    if (statusEl) statusEl.textContent = "Searching...";

    try {
        const res = await fetch("/api/solve", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                board: state.board,
                size: 3,
                algorithm: algKey,
                timeout_sec: 10.0
            })
        });

        const data = await res.json();

        if (!data.success) {
            alert(`Search Failed: ${data.error_message || "Could not find solution"}`);
            if (statusEl) statusEl.textContent = "Failed";
            return;
        }

        // Update performance metrics
        const costEl = document.getElementById("metric-cost");
        if (costEl) costEl.textContent = `${data.cost} moves`;

        const nodesEl = document.getElementById("metric-nodes");
        if (nodesEl) nodesEl.textContent = (data.nodes_expanded || 0).toLocaleString();

        const frontEl = document.getElementById("metric-frontier");
        if (frontEl) frontEl.textContent = (data.max_frontier_size || 0).toLocaleString();

        const timeEl = document.getElementById("metric-time");
        if (timeEl) timeEl.textContent = `${(data.execution_time_ms || 0).toFixed(2)} ms`;

        if (statusEl) statusEl.textContent = `Solved in ${data.cost} moves!`;

        // Save solution path
        state.solutionPath = data.path || [];
        state.solutionActions = data.actions || [];
        state.currentStep = 0;

        renderActionPills();
        enablePlaybackControls();
        setPlaybackStep(0);

    } catch (e) {
        console.error("Solver error:", e);
        alert("Failed to communicate with solver backend.");
    } finally {
        if (btnSolve) {
            btnSolve.disabled = false;
            btnSolve.innerHTML = '<span class="btn-icon">⚡</span> Solve Puzzle';
        }
    }
}

function clearSolutionState() {
    state.solutionPath = [];
    state.solutionActions = [];
    state.currentStep = 0;
    if (timelineSlider) {
        timelineSlider.value = 0;
        timelineSlider.max = 0;
        timelineSlider.disabled = true;
    }
    if (stepCounterLabel) stepCounterLabel.textContent = "Step: 0 / 0";
    if (actionPills) {
        actionPills.innerHTML = '<span class="placeholder-text">Press "Solve Puzzle" to compute optimal solution path</span>';
    }
    disablePlaybackControls();
}

function enablePlaybackControls() {
    const totalSteps = state.solutionPath.length - 1;
    if (timelineSlider) {
        timelineSlider.max = Math.max(0, totalSteps);
        timelineSlider.disabled = totalSteps <= 0;
    }
    if (btnFirst) btnFirst.disabled = false;
    if (btnPrev) btnPrev.disabled = false;
    if (btnPlay) btnPlay.disabled = false;
    if (btnNext) btnNext.disabled = false;
    if (btnLast) btnLast.disabled = false;
}

function disablePlaybackControls() {
    if (btnFirst) btnFirst.disabled = true;
    if (btnPrev) btnPrev.disabled = true;
    if (btnPlay) btnPlay.disabled = true;
    if (btnNext) btnNext.disabled = true;
    if (btnLast) btnLast.disabled = true;
}

function renderActionPills() {
    if (!actionPills) return;
    actionPills.innerHTML = "";
    if (state.solutionActions.length === 0) {
        actionPills.innerHTML = '<span class="placeholder-text">Already at goal state (0 moves needed)</span>';
        return;
    }

    state.solutionActions.forEach((action, idx) => {
        const pill = document.createElement("span");
        pill.className = "action-pill";
        pill.id = `pill-step-${idx + 1}`;
        pill.textContent = `#${idx + 1}: ${action}`;
        actionPills.appendChild(pill);
    });
}

function setPlaybackStep(stepIndex) {
    if (!state.solutionPath || state.solutionPath.length === 0) return;
    const clamped = Math.max(0, Math.min(stepIndex, state.solutionPath.length - 1));
    state.currentStep = clamped;
    state.board = [...state.solutionPath[clamped]];

    if (timelineSlider) timelineSlider.value = clamped;
    if (stepCounterLabel) stepCounterLabel.textContent = `Step: ${clamped} / ${state.solutionPath.length - 1}`;

    // Highlight active action pill
    document.querySelectorAll(".action-pill").forEach(p => p.classList.remove("current"));
    const activePill = document.getElementById(`pill-step-${clamped}`);
    if (activePill) {
        activePill.classList.add("current");
        activePill.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
    }

    renderBoard();

    // If reached end, pause
    if (clamped === state.solutionPath.length - 1 && state.isPlaying) {
        pauseSolution();
    }
}

function togglePlayPause() {
    if (state.isPlaying) {
        pauseSolution();
    } else {
        playSolution();
    }
}

function playSolution() {
    if (state.solutionPath.length === 0) return;
    if (state.currentStep >= state.solutionPath.length - 1) {
        state.currentStep = 0;
    }
    state.isPlaying = true;
    if (playIcon) playIcon.textContent = "⏸";
    if (btnPlay) btnPlay.classList.add("btn-glow");

    state.playTimer = setInterval(() => {
        if (state.currentStep < state.solutionPath.length - 1) {
            setPlaybackStep(state.currentStep + 1);
        } else {
            pauseSolution();
        }
    }, state.playSpeed);
}

function pauseSolution() {
    state.isPlaying = false;
    if (playIcon) playIcon.textContent = "▶";
    if (btnPlay) btnPlay.classList.remove("btn-glow");
    if (state.playTimer) {
        clearInterval(state.playTimer);
        state.playTimer = null;
    }
}

// ================= SHUFFLE & PRESETS =================
async function handleShuffle() {
    if (state.isPlaying) pauseSolution();
    const steps = (shuffleStepsInput ? parseInt(shuffleStepsInput.value, 10) : 12) || 12;
    try {
        const res = await fetch("/api/generate_shuffle", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ size: 3, steps: steps })
        });
        const data = await res.json();
        state.board = [...data.board];
        state.initialBoard = [...data.board];
        renderBoard();
        checkBoardSolvability();
        clearSolutionState();
    } catch (e) {
        console.error("Shuffle failed:", e);
    }
}

function loadSelectedPreset() {
    if (state.isPlaying) pauseSolution();
    if (!presetSelect) return;
    const key = presetSelect.value;
    const preset = state.presets[key];
    if (!preset) return;

    state.size = 3;
    state.board = [...preset.board];
    state.initialBoard = [...preset.board];

    renderBoard();
    checkBoardSolvability();
    clearSolutionState();
}

function resetToInitial() {
    if (state.isPlaying) pauseSolution();
    state.board = [...state.initialBoard];
    renderBoard();
    checkBoardSolvability();
    clearSolutionState();
}
