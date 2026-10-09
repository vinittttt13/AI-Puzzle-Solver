"""
FastAPI Backend Application Entry Point for AI Puzzle Solver Web Dashboard.
Delegates to server module for unified routes, middleware, and models.
"""
from server import server_app as app, server_app
import uvicorn

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("[*] AI N-PUZZLE SOLVER WEB SERVER RUNNING")
    print("[*] Dashboard URL: http://127.0.0.1:8000")
    print("=" * 65 + "\n")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

