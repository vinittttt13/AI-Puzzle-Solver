/**
 * AI N-PUZZLE SOLVER - FRONTEND APPLICATION LOGIC
 * Supports interactive playback, manual tile movements, live benchmarking,
 * solvability analysis, and Chart.js visualizations.
 */

// Global Application State
const state = {
    size: 3,
    board: [1, 2, 3, 4, 5, 6, 0, 7, 8],
    initialBoard: [1, 2, 3, 4, 5, 6, 0, 7, 8],
    solutionPath: [],
    solutionActions: [],
    currentStep: 0,
    isPlaying: false,
    playTimer: null,
    playSpeed: 600,
    soundEnabled: true,
    audioCtx: null,
    presets: {},
    algorithmsMeta: {},
    benchmarkResults: null,
    charts: {
        nodes: null,
        time: null,
        memory: null,
        cost: null
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
const soundToggleBtn = document.getElementById("sound-toggle-btn");

// ================= INITIALIZATION =================
document.addEventListener("DOMContentLoaded", async () => {
    initTabs();
    initAudio();
    await fetchPresets();
    await fetchAlgorithmsMeta();
    setupEventListeners();
    renderBoard();
    checkBoardSolvability();
    buildCustomGrid();
});

// ================= TABS NAVIGATION =================
function initTabs() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            
            btn.classList.add("active");
            const targetId = btn.getAttribute("data-tab");
            document.getElementById(targetId).classList.add("active");
        });
    });
}

function openTheoryModal() {
    const theoryTabBtn = document.querySelector('[data-tab="theory-tab"]');
    if (theoryTabBtn) theoryTabBtn.click();
}

// ================= WEB AUDIO API FEEDBACK =================
function initAudio() {
    soundToggleBtn.addEventListener("click", () => {
        state.soundEnabled = !state.soundEnabled;
        document.getElementById("sound-icon").textContent = state.soundEnabled ? "🔊" : "🔇";
    });
}

function playClickSound(freq = 440) {
    if (!state.soundEnabled) return;
    try {
        if (!state.audioCtx) {
            state.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (state.audioCtx.state === "suspended") {
            state.audioCtx.resume();
        }
        const osc = state.audioCtx.createOscillator();
        const gain = state.audioCtx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, state.audioCtx.currentTime);
        gain.gain.setValueAtTime(0.08, state.audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, state.audioCtx.currentTime + 0.08);
        osc.connect(gain);
        gain.connect(state.audioCtx.destination);
        osc.start();
        osc.stop(state.audioCtx.currentTime + 0.08);
    } catch (e) {
        // Fallback silently if audio context is blocked
    }
}

// ================= API CALLS & DATA FETCHING =================
async function fetchPresets() {
    try {
        const res = await fetch("/api/presets");
        state.presets = await res.json();
        presetSelect.innerHTML = "";
        for (const [key, p] of Object.entries(state.presets)) {
            const opt = document.createElement("option");
            opt.value = key;
            opt.textContent = `[${p.difficulty}] ${p.name}`;
            presetSelect.appendChild(opt);
        }
        // Load default easy preset
        if (state.presets["very_easy_2_moves"]) {
            state.board = [...state.presets["very_easy_2_moves"].board];
            state.initialBoard = [...state.board];
        }
    } catch (e) {
        console.error("Failed to load presets:", e);
    }
}

async function fetchAlgorithmsMeta() {
    try {
        const res = await fetch("/api/algorithms_meta");
        const data = await res.json();
        state.algorithmsMeta = data.metadata;
        updateAlgorithmInfo();
    } catch (e) {
        console.error("Failed to load algorithms metadata:", e);
    }
}

function updateAlgorithmInfo() {
    const selectedKey = algorithmSelect.value;
    const meta = state.algorithmsMeta[selectedKey];
    if (!meta) return;

    document.getElementById("alg-category-tag").textContent = meta.type;
    const optTag = document.getElementById("alg-optimal-tag");
    if (meta.optimal) {
        optTag.textContent = "Guaranteed Optimal";
        optTag.className = "info-tag opt-tag";
    } else {
        optTag.textContent = "Sub-optimal / Heuristic";
        optTag.className = "info-tag";
        optTag.style.background = "rgba(245, 158, 11, 0.15)";
        optTag.style.color = "var(--accent-amber)";
    }
    document.getElementById("alg-description-text").textContent = meta.description;
}

// ================= PUZZLE BOARD RENDERING & INTERACTION =================
function renderBoard() {
    boardEl.innerHTML = "";
    boardEl.className = `puzzle-board size-${state.size}`;
    const emptyIdx = state.board.indexOf(0);
    const emptyR = Math.floor(emptyIdx / state.size);
    const emptyC = emptyIdx % state.size;

    state.board.forEach((tileVal, idx) => {
        const tile = document.createElement("div");
        const r = Math.floor(idx / state.size);
        const c = idx % state.size;

        if (tileVal === 0) {
            tile.className = "puzzle-tile empty-slot";
        } else {
            tile.className = "puzzle-tile";
            tile.textContent = tileVal;

            // Small indicator of target goal index
            const goalTarget = tileVal;
            const targetR = Math.floor((goalTarget - 1) / state.size);
            const targetC = (goalTarget - 1) % state.size;
            if (r === targetR && c === targetC) {
                tile.classList.add("in-goal");
            }

            // Check if adjacent to blank space (clickable to slide manually!)
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
    const total = state.size * state.size;
    for (let i = 0; i < total - 1; i++) {
        if (state.board[i] !== i + 1) return false;
    }
    return state.board[total - 1] === 0;
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

function playVictoryFanfare() {
    if (!state.soundEnabled) return;
    [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
        setTimeout(() => playClickSound(freq), i * 85);
    });
}

function handleTileClick(tileIdx, emptyIdx) {
    if (state.isPlaying) pauseSolution();

    // Swap tile and blank
    [state.board[tileIdx], state.board[emptyIdx]] = [state.board[emptyIdx], state.board[tileIdx]];
    playClickSound(520);
    renderBoard();
    checkBoardSolvability();

    if (isCurrentStateGoal()) {
        playVictoryFanfare();
    }

    // Reset current solution path since user intervened
    clearSolutionState();
}

function slideTileInDirection(dr, dc) {
    if (state.isPlaying) pauseSolution();
    const emptyIdx = state.board.indexOf(0);
    const emptyR = Math.floor(emptyIdx / state.size);
    const emptyC = emptyIdx % state.size;
    const targetR = emptyR + dr;
    const targetC = emptyC + dc;

    if (targetR >= 0 && targetR < state.size && targetC >= 0 && targetC < state.size) {
        const targetIdx = targetR * state.size + targetC;
        handleTileClick(targetIdx, emptyIdx);
    }
}

function updateHeuristicPreview() {
    let manhattan = 0;
    state.board.forEach((tile, idx) => {
        if (tile !== 0) {
            const currR = Math.floor(idx / state.size);
            const currC = idx % state.size;
            const goalR = Math.floor((tile - 1) / state.size);
            const goalC = (tile - 1) % state.size;
            manhattan += Math.abs(currR - goalR) + Math.abs(currC - goalC);
        }
    });
    previewHVal.textContent = manhattan;
}

// ================= SOLVABILITY CHECK =================
async function checkBoardSolvability() {
    try {
        const res = await fetch("/api/check_solvability", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board: state.board, size: state.size })
        });
        const details = await res.json();
        
        if (details.is_solvable) {
            solvabilityBadge.className = "badge badge-success";
            solvabilityText.textContent = "Solvable";
            btnSolve.disabled = false;
        } else {
            solvabilityBadge.className = "badge badge-danger";
            solvabilityText.textContent = "Unsolvable";
            btnSolve.disabled = true;
        }

        inversionExplanationText.textContent = details.reason;
    } catch (e) {
        console.error("Solvability check error:", e);
    }
}

// ================= SOLVE & PLAYBACK =================
async function solveCurrentPuzzle() {
    const algKey = algorithmSelect.value;
    btnSolve.disabled = true;
    btnSolve.innerHTML = '<span class="btn-icon">⏳</span> Computing Path...';
    document.getElementById("metrics-status").textContent = "Searching...";

    try {
        const res = await fetch("/api/solve", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                board: state.board,
                size: state.size,
                algorithm: algKey,
                timeout_sec: 10.0
            })
        });

        const data = await res.json();

        if (!data.success) {
            alert(`Search Failed: ${data.error_message || "Unknown error"}`);
            document.getElementById("metrics-status").textContent = "Failed";
            return;
        }

        // Update performance metrics
        document.getElementById("metric-cost").textContent = data.cost;
        document.getElementById("metric-nodes").textContent = data.nodes_expanded.toLocaleString();
        document.getElementById("metric-frontier").textContent = data.max_frontier_size.toLocaleString();
        document.getElementById("metric-time").textContent = data.execution_time_ms.toFixed(2);
        document.getElementById("metrics-status").textContent = "Solved!";

        // Save solution path
        state.solutionPath = data.path;
        state.solutionActions = data.actions;
        state.currentStep = 0;

        renderActionPills();
        enablePlaybackControls();
        setPlaybackStep(0);

    } catch (e) {
        console.error("Solver error:", e);
        alert("Failed to communicate with solver backend.");
    } finally {
        btnSolve.disabled = false;
        btnSolve.innerHTML = '<span class="btn-icon">⚡</span> Solve Puzzle';
    }
}

function clearSolutionState() {
    state.solutionPath = [];
    state.solutionActions = [];
    state.currentStep = 0;
    timelineSlider.value = 0;
    timelineSlider.max = 0;
    timelineSlider.disabled = true;
    stepCounterLabel.textContent = "Step: 0 / 0";
    actionPills.innerHTML = '<span class="placeholder-text">Press "Solve Puzzle" to compute optimal solution path</span>';
    disablePlaybackControls();
}

function enablePlaybackControls() {
    const totalSteps = state.solutionPath.length - 1;
    timelineSlider.max = totalSteps;
    timelineSlider.disabled = totalSteps <= 0;
    btnFirst.disabled = false;
    btnPrev.disabled = false;
    btnPlay.disabled = false;
    btnNext.disabled = false;
    btnLast.disabled = false;
}

function disablePlaybackControls() {
    btnFirst.disabled = true;
    btnPrev.disabled = true;
    btnPlay.disabled = true;
    btnNext.disabled = true;
    btnLast.disabled = true;
}

function renderActionPills() {
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
    
    timelineSlider.value = clamped;
    stepCounterLabel.textContent = `Step: ${clamped} / ${state.solutionPath.length - 1}`;
    
    // Highlight corresponding action pill
    document.querySelectorAll(".action-pill").forEach(p => p.classList.remove("current"));
    const activePill = document.getElementById(`pill-step-${clamped}`);
    if (activePill) {
        activePill.classList.add("current");
        activePill.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
    }

    renderBoard();
    playClickSound(380 + clamped * 12);

    // If reached end, pause & play victory fanfare
    if (clamped === state.solutionPath.length - 1 && state.isPlaying) {
        pauseSolution();
        playVictoryFanfare();
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
    playIcon.textContent = "⏸";
    btnPlay.classList.add("btn-glow");

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
    playIcon.textContent = "▶";
    btnPlay.classList.remove("btn-glow");
    if (state.playTimer) {
        clearInterval(state.playTimer);
        state.playTimer = null;
    }
}

// ================= SHUFFLE & PRESETS =================
async function handleShuffle() {
    if (state.isPlaying) pauseSolution();
    const steps = parseInt(document.getElementById("shuffle-steps").value) || 15;
    try {
        const res = await fetch("/api/generate_shuffle", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ size: state.size, steps: steps })
        });
        const data = await res.json();
        state.board = [...data.board];
        state.initialBoard = [...data.board];
        renderBoard();
        checkBoardSolvability();
        clearSolutionState();
        playClickSound(600);
    } catch (e) {
        console.error("Shuffle failed:", e);
    }
}

function loadSelectedPreset() {
    if (state.isPlaying) pauseSolution();
    const key = presetSelect.value;
    const preset = state.presets[key];
    if (!preset) return;

    state.size = preset.size;
    state.board = [...preset.board];
    state.initialBoard = [...preset.board];
    
    // Update grid tag
    document.getElementById("grid-size-tag").textContent = `${state.size}x${state.size} (${state.size === 3 ? '8' : '15'}-Puzzle)`;
    
    // Toggle active dimension button
    document.querySelectorAll(".btn-toggle").forEach(btn => {
        btn.classList.toggle("active", parseInt(btn.dataset.size) === state.size);
    });

    renderBoard();
    checkBoardSolvability();
    clearSolutionState();
    buildCustomGrid();
    playClickSound(650);
}

function resetToInitial() {
    if (state.isPlaying) pauseSolution();
    state.board = [...state.initialBoard];
    renderBoard();
    checkBoardSolvability();
    clearSolutionState();
}

// ================= BENCHMARK ARENA =================
async function runAlgorithmBenchmark() {
    const selectedBoxes = document.querySelectorAll("#bench-checkboxes input[type='checkbox']:checked");
    const algKeys = Array.from(selectedBoxes).map(cb => cb.value);

    if (algKeys.length === 0) {
        alert("Please select at least one algorithm to benchmark.");
        return;
    }

    const btnRun = document.getElementById("btn-run-benchmark");
    btnRun.disabled = true;
    btnRun.innerHTML = '⏳ Benchmarking in Progress...';

    const tbody = document.getElementById("benchmark-table-body");
    tbody.innerHTML = `<tr><td colspan="8" class="empty-table-msg">Executing ${algKeys.length} algorithms on current board...</td></tr>`;

    try {
        const res = await fetch("/api/benchmark", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                board: state.board,
                size: state.size,
                algorithms: algKeys,
                timeout_sec: 8.0
            })
        });

        const data = await res.json();
        state.benchmarkResults = data.benchmark_results;

        renderBenchmarkTable(data.benchmark_results);
        updateBenchmarkPodium(data.benchmark_results);
        renderBenchmarkCharts(data.benchmark_results);

        document.getElementById("btn-export-benchmark").disabled = false;

    } catch (e) {
        console.error("Benchmark failed:", e);
        alert("Benchmark execution failed.");
    } finally {
        btnRun.disabled = false;
        btnRun.innerHTML = '🚀 Run All Algorithms';
    }
}

function renderBenchmarkTable(results) {
    const tbody = document.getElementById("benchmark-table-body");
    tbody.innerHTML = "";

    results.forEach(r => {
        const row = document.createElement("tr");
        if (r.success) {
            row.innerHTML = `
                <td><b>${r.algorithm_name}</b></td>
                <td><span class="info-tag">${r.category || 'Search'}</span></td>
                <td>${r.cost} moves</td>
                <td>${r.nodes_expanded.toLocaleString()}</td>
                <td>${r.max_frontier_size.toLocaleString()}</td>
                <td>${r.execution_time_ms.toFixed(2)} ms</td>
                <td>${r.is_optimal ? '<span style="color:var(--accent-emerald)">✓ Optimal</span>' : '<span style="color:var(--accent-amber)">Sub-optimal</span>'}</td>
                <td><span class="badge badge-success">Success</span></td>
            `;
        } else {
            row.innerHTML = `
                <td><b>${r.algorithm_name}</b></td>
                <td><span class="info-tag">${r.category || 'Search'}</span></td>
                <td colspan="5" style="color:var(--accent-rose);">${r.error_message || 'Timeout / Exceeded limits'}</td>
                <td><span class="badge badge-danger">Failed</span></td>
            `;
        }
        tbody.appendChild(row);
    });
}

function updateBenchmarkPodium(results) {
    const successful = results.filter(r => r.success);
    const podiumEl = document.getElementById("benchmark-podium");

    if (successful.length === 0) {
        podiumEl.classList.add("hidden");
        return;
    }

    podiumEl.classList.remove("hidden");

    // Champion: Fewest nodes expanded
    const minNodes = [...successful].sort((a, b) => a.nodes_expanded - b.nodes_expanded)[0];
    document.getElementById("podium-nodes-name").textContent = minNodes.algorithm_name;
    document.getElementById("podium-nodes-val").textContent = `${minNodes.nodes_expanded.toLocaleString()} nodes`;

    // Speed: Fastest execution
    const fastest = [...successful].sort((a, b) => a.execution_time_ms - b.execution_time_ms)[0];
    document.getElementById("podium-speed-name").textContent = fastest.algorithm_name;
    document.getElementById("podium-speed-val").textContent = `${fastest.execution_time_ms.toFixed(2)} ms`;

    // Memory: Lowest peak frontier
    const lowestMem = [...successful].sort((a, b) => a.max_frontier_size - b.max_frontier_size)[0];
    document.getElementById("podium-mem-name").textContent = lowestMem.algorithm_name;
    document.getElementById("podium-mem-val").textContent = `${lowestMem.max_frontier_size.toLocaleString()} frontier`;
}

function renderBenchmarkCharts(results) {
    const successful = results.filter(r => r.success);
    const labels = successful.map(r => r.algorithm_name.replace("Search", "").trim());

    const nodesData = successful.map(r => r.nodes_expanded);
    const timeData = successful.map(r => r.execution_time_ms);
    const memoryData = successful.map(r => r.max_frontier_size);
    const costData = successful.map(r => r.cost);

    const colors = [
        '#6366f1', '#38bdf8', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#14b8a6'
    ];

    // Helper chart builder
    const buildChart = (ctxId, chartKey, label, data, isLog = false) => {
        if (state.charts[chartKey]) {
            state.charts[chartKey].destroy();
        }
        const ctx = document.getElementById(ctxId).getContext('2d');
        state.charts[chartKey] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    backgroundColor: colors.slice(0, labels.length),
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        type: isLog ? 'logarithmic' : 'linear',
                        grid: { color: 'rgba(255, 255, 255, 0.06)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8', font: { size: 10 } }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    };

    buildChart('chart-nodes', 'nodes', 'Nodes Expanded (Log Scale)', nodesData, true);
    buildChart('chart-time', 'time', 'Time (ms)', timeData, false);
    buildChart('chart-memory', 'memory', 'Max Frontier Size', memoryData, false);
    buildChart('chart-cost', 'cost', 'Move Count', costData, false);
}

function exportBenchmarkCSV() {
    if (!state.benchmarkResults) return;
    let csv = "Algorithm,Category,Optimal,Path Cost,Nodes Expanded,Max Frontier Size,Execution Time (ms),Status\n";
    state.benchmarkResults.forEach(r => {
        csv += `"${r.algorithm_name}","${r.category || ''}","${r.is_optimal}","${r.cost}","${r.nodes_expanded}","${r.max_frontier_size}","${r.execution_time_ms}","${r.success ? 'Success' : 'Failed'}"\n`;
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `AI_Puzzle_Benchmark_Report_${Date.now()}.csv`;
    link.click();
}

// ================= CUSTOM BOARD EDITOR =================
function buildCustomGrid() {
    const gridEl = document.getElementById("custom-grid-inputs");
    gridEl.innerHTML = "";
    gridEl.className = `custom-grid size-${state.size}`;

    state.board.forEach((val, idx) => {
        const input = document.createElement("input");
        input.type = "number";
        input.min = "0";
        input.max = String(state.size * state.size - 1);
        input.value = val;
        input.className = "custom-cell-input";
        input.id = `custom-cell-${idx}`;
        input.addEventListener("input", syncCustomGridToText);
        gridEl.appendChild(input);
    });

    syncCustomGridToText();
}

function syncCustomGridToText() {
    const inputs = document.querySelectorAll(".custom-cell-input");
    const vals = Array.from(inputs).map(inp => inp.value.trim());
    document.getElementById("custom-text-input").value = vals.join(" ");
}

function quickFill(arr) {
    document.getElementById("custom-text-input").value = arr.join(" ");
    validateAndApplyCustom(false);
}

async function validateAndApplyCustom(apply = false) {
    const text = document.getElementById("custom-text-input").value.trim();
    const tokens = text.replace(/,/g, " ").split(/\s+/).filter(Boolean);
    const nums = tokens.map(x => parseInt(x));
    const diagEl = document.getElementById("custom-status-text");

    const expectedCount = state.size * state.size;
    if (nums.length !== expectedCount) {
        diagEl.innerHTML = `<span style="color:var(--accent-rose)">❌ Invalid length: Expected ${expectedCount} tiles, got ${nums.length}.</span>`;
        return false;
    }

    const uniqueSet = new Set(nums);
    const validRange = nums.every(n => n >= 0 && n < expectedCount);
    if (uniqueSet.size !== expectedCount || !validRange) {
        diagEl.innerHTML = `<span style="color:var(--accent-rose)">❌ Permutation error: Must contain unique integers 0 through ${expectedCount - 1}.</span>`;
        return false;
    }

    // Call Solvability API
    try {
        const res = await fetch("/api/check_solvability", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board: nums, size: state.size })
        });
        const details = await res.json();

        if (details.is_solvable) {
            diagEl.innerHTML = `<span style="color:var(--accent-emerald)">✓ Valid & Solvable: ${details.reason}</span>`;
            if (apply) {
                state.board = [...nums];
                state.initialBoard = [...nums];
                renderBoard();
                checkBoardSolvability();
                clearSolutionState();
                // Switch back to solver tab
                document.querySelector('[data-tab="solver-tab"]').click();
            }
            return true;
        } else {
            diagEl.innerHTML = `<span style="color:var(--accent-amber)">⚠️ Valid Permutation, BUT Unsolvable: ${details.reason}</span>`;
            return false;
        }
    } catch (e) {
        diagEl.textContent = `Error verifying board: ${e.message}`;
        return false;
    }
}

// ================= EVENT LISTENERS =================
function setupEventListeners() {
    algorithmSelect.addEventListener("change", updateAlgorithmInfo);
    btnSolve.addEventListener("click", solveCurrentPuzzle);
    btnReset.addEventListener("click", resetToInitial);
    btnShuffle.addEventListener("click", handleShuffle);
    btnLoadPreset.addEventListener("click", loadSelectedPreset);
    btnPlay.addEventListener("click", togglePlayPause);

    btnFirst.addEventListener("click", () => {
        pauseSolution();
        setPlaybackStep(0);
    });
    btnPrev.addEventListener("click", () => {
        pauseSolution();
        setPlaybackStep(state.currentStep - 1);
    });
    btnNext.addEventListener("click", () => {
        pauseSolution();
        setPlaybackStep(state.currentStep + 1);
    });
    btnLast.addEventListener("click", () => {
        pauseSolution();
        setPlaybackStep(state.solutionPath.length - 1);
    });

    timelineSlider.addEventListener("input", (e) => {
        pauseSolution();
        setPlaybackStep(parseInt(e.target.value));
    });

    playbackSpeedSelect.addEventListener("change", (e) => {
        state.playSpeed = parseInt(e.target.value);
        if (state.isPlaying) {
            pauseSolution();
            playSolution();
        }
    });

    document.getElementById("shuffle-steps").addEventListener("input", (e) => {
        document.getElementById("shuffle-steps-val").textContent = `${e.target.value} moves`;
    });

    // Dimension toggle buttons
    document.querySelectorAll(".btn-toggle").forEach(btn => {
        btn.addEventListener("click", () => {
            const newSize = parseInt(btn.dataset.size);
            if (newSize === state.size) return;

            document.querySelectorAll(".btn-toggle").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            state.size = newSize;

            document.getElementById("grid-size-tag").textContent = `${newSize}x${newSize} (${newSize === 3 ? '8' : '15'}-Puzzle)`;
            
            // Reinitialize default board for selected size
            if (newSize === 4) {
                state.board = [...state.presets["15_puzzle_easy"].board];
            } else {
                state.board = [...state.presets["very_easy_2_moves"].board];
            }
            state.initialBoard = [...state.board];

            renderBoard();
            checkBoardSolvability();
            clearSolutionState();
            buildCustomGrid();
        });
    });

    // Benchmark Arena
    document.getElementById("btn-run-benchmark").addEventListener("click", runAlgorithmBenchmark);
    document.getElementById("btn-export-benchmark").addEventListener("click", exportBenchmarkCSV);

    // Custom Editor
    document.getElementById("btn-validate-custom").addEventListener("click", () => validateAndApplyCustom(false));
    document.getElementById("btn-apply-custom").addEventListener("click", () => validateAndApplyCustom(true));

    // Keyboard Arrow & WASD Controls
    window.addEventListener("keydown", (e) => {
        if (document.activeElement.tagName === "INPUT" || document.activeElement.tagName === "TEXTAREA") return;
        if (state.solutionPath.length > 0) {
            if (e.key === "ArrowLeft") {
                pauseSolution();
                setPlaybackStep(state.currentStep - 1);
            } else if (e.key === "ArrowRight") {
                pauseSolution();
                setPlaybackStep(state.currentStep + 1);
            } else if (e.key === " ") {
                e.preventDefault();
                togglePlayPause();
            }
        } else {
            if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") {
                e.preventDefault();
                slideTileInDirection(1, 0); // tile below blank moves up
            } else if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") {
                e.preventDefault();
                slideTileInDirection(-1, 0); // tile above blank moves down
            } else if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") {
                e.preventDefault();
                slideTileInDirection(0, 1); // tile right of blank moves left
            } else if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") {
                e.preventDefault();
                slideTileInDirection(0, -1); // tile left of blank moves right
            }
        }
    });
}
