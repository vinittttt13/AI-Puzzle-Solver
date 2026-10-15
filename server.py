"""
FastAPI Backend Application for AI Puzzle Solver Web Dashboard.
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import uvicorn

from core.puzzle import PuzzleState, generate_puzzle_by_shuffling, generate_random_puzzle
from core.heuristics import HEURISTIC_DESCRIPTIONS
from algorithms import get_algorithm, ALGORITHM_METADATA, ALGORITHM_REGISTRY
from benchmark import run_benchmark, DEFAULT_BENCHMARK_ALGS
from presets import PRESETS

server_app = FastAPI(
    title="AI N-Puzzle Solver",
    description="Interactive AI Search Algorithm Demonstrator for College Minor Project",
    version="1.0.0"
)

# Request Models
class SolveRequest(BaseModel):
    board: List[int] = Field(..., description="Flat board representation")
    size: int = Field(3, ge=3, le=4)
    algorithm: str = Field("astar_manhattan")
    timeout_sec: float = Field(8.0, ge=0.5, le=30.0)

class BenchmarkRequest(BaseModel):
    board: List[int]
    size: int = Field(3, ge=3, le=4)
    algorithms: Optional[List[str]] = None
    timeout_sec: float = Field(6.0, ge=0.5, le=20.0)

class SolvabilityRequest(BaseModel):
    board: List[int]
    size: int = Field(3, ge=3, le=4)

class ShuffleRequest(BaseModel):
    size: int = Field(3, ge=3, le=4)
    steps: int = Field(15, ge=1, le=100)


@server_app.get("/api/presets")
def get_presets():
    return PRESETS


@server_app.get("/api/algorithms_meta")
def get_algorithms_meta():
    return {
        "metadata": ALGORITHM_METADATA,
        "available_keys": list(ALGORITHM_REGISTRY.keys())
    }


@server_app.get("/api/heuristics_meta")
def get_heuristics_meta():
    return HEURISTIC_DESCRIPTIONS


@server_app.post("/api/check_solvability")
def check_solvability(req: SolvabilityRequest):
    try:
        state = PuzzleState(tuple(req.board), req.size)
        return state.solvability_details()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@server_app.post("/api/generate_shuffle")
def generate_shuffle(req: ShuffleRequest):
    try:
        shuffled_state = generate_puzzle_by_shuffling(steps=req.steps, size=req.size)
        return {
            "board": list(shuffled_state.board),
            "size": req.size,
            "solvability": shuffled_state.solvability_details()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@server_app.post("/api/solve")
def solve_puzzle(req: SolveRequest):
    try:
        state = PuzzleState(tuple(req.board), req.size)
        if not state.is_solvable():
            details = state.solvability_details()
            return {
                "success": False,
                "algorithm_name": req.algorithm,
                "heuristic_name": None,
                "error_message": f"Puzzle is mathematically unsolvable. {details['reason']}",
                "solvability": details,
                "path": [],
                "actions": [],
                "cost": 0,
                "nodes_expanded": 0,
                "max_frontier_size": 0,
                "execution_time_ms": 0.0,
                "is_optimal": False
            }

        solver = get_algorithm(req.algorithm)
        result = solver.solve(state, timeout_sec=req.timeout_sec)
        res_dict = result.to_dict()
        res_dict["solvability"] = state.solvability_details()
        return res_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Solver error: {str(e)}")


@server_app.post("/api/benchmark")
def benchmark_puzzle(req: BenchmarkRequest):
    try:
        state = PuzzleState(tuple(req.board), req.size)
        bench = run_benchmark(
            initial_state=state,
            algorithm_keys=req.algorithms,
            timeout_sec=req.timeout_sec
        )
        return bench
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark error: {str(e)}")


@server_app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/static") or request.url.path == "/":
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


# Mount static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

server_app.mount("/static", StaticFiles(directory=static_dir), name="static")

@server_app.get("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(
            index_file,
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    return {"message": "AI Puzzle Solver Backend is Running."}

# Aliases for compatibility with various uvicorn invocation conventions
app = server_app


if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("[*] AI N-PUZZLE SOLVER WEB SERVER RUNNING")
    print("[*] Dashboard URL: http://127.0.0.1:8000")
    print("=" * 65 + "\n")
    uvicorn.run("server:server_app", host="127.0.0.1", port=8000, reload=True)

