"""
Integration test for FastAPI endpoints using Starlette TestClient.
"""
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from server import server_app

client = TestClient(server_app)

def test_presets_endpoint():
    res = client.get("/api/presets")
    assert res.status_code == 200
    data = res.json()
    assert "easy_6_moves" in data
    print("[PASS] /api/presets")

def test_solvability_endpoint():
    # Solvable 8-puzzle
    res = client.post("/api/check_solvability", json={"board": [1, 2, 3, 4, 5, 6, 0, 7, 8], "size": 3})
    assert res.status_code == 200
    assert res.json()["is_solvable"] is True

    # Unsolvable 8-puzzle (odd inversions)
    res = client.post("/api/check_solvability", json={"board": [1, 2, 3, 4, 5, 6, 8, 7, 0], "size": 3})
    assert res.status_code == 200
    assert res.json()["is_solvable"] is False
    print("[PASS] /api/check_solvability")

def test_solve_endpoint():
    res = client.post("/api/solve", json={
        "board": [1, 2, 3, 4, 5, 6, 0, 7, 8],
        "size": 3,
        "algorithm": "astar_linear_conflict",
        "timeout_sec": 5.0
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["cost"] == 2
    print("[PASS] /api/solve")

def test_benchmark_endpoint():
    res = client.post("/api/benchmark", json={
        "board": [1, 2, 3, 4, 5, 6, 0, 7, 8],
        "size": 3,
        "algorithms": ["astar_linear_conflict", "astar_manhattan", "bfs"],
        "timeout_sec": 5.0
    })
    assert res.status_code == 200
    data = res.json()
    assert len(data["benchmark_results"]) == 3
    print("[PASS] /api/benchmark")

def test_algorithms_meta_endpoint():
    res = client.get("/api/algorithms_meta")
    assert res.status_code == 200
    data = res.json()
    assert "astar_linear_conflict" in data["metadata"]
    assert "idastar_linear_conflict" in data["metadata"]
    print("[PASS] /api/algorithms_meta")

def test_heuristics_meta_endpoint():
    res = client.get("/api/heuristics_meta")
    assert res.status_code == 200
    data = res.json()
    assert "linear_conflict" in data
    print("[PASS] /api/heuristics_meta")

def test_generate_shuffle_endpoint():
    res = client.post("/api/generate_shuffle", json={"size": 3, "steps": 10})
    assert res.status_code == 200
    data = res.json()
    assert len(data["board"]) == 9
    assert data["solvability"]["is_solvable"] is True
def test_static_index():
    res = client.get("/")
    assert res.status_code == 200
    assert "AI N-Puzzle Solver" in res.text
    print("[PASS] Static frontend /")

if __name__ == "__main__":
    test_presets_endpoint()
    test_solvability_endpoint()
    test_solve_endpoint()
    test_benchmark_endpoint()
    test_algorithms_meta_endpoint()
    test_heuristics_meta_endpoint()
    test_generate_shuffle_endpoint()
    test_static_index()
    print("\nALL API & BACKEND INTEGRATION TESTS PASSED SUCCESSFULLY!")

