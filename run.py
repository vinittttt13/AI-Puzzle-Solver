"""
AI N-Puzzle Solver - Universal Project Launcher.
Convenient script to launch the Web Application, CLI, or Test Suite.

Usage:
  python run.py          (Opens interactive launcher)
  python run.py web      (Starts the Web Dashboard server)
  python run.py cli      (Starts the Interactive Terminal CLI)
  python run.py test     (Runs the full automated test suite)
"""
import sys
import os
import webbrowser

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def run_web():
    import uvicorn
    import threading
    import time
    from server import server_app
    print("\n" + "=" * 65)
    print("[*] LAUNCHING AI N-PUZZLE SOLVER WEB DASHBOARD")
    print("[*] URL: http://127.0.0.1:8000")
    print("=" * 65 + "\n")
    
    def _open_browser():
        time.sleep(1.2)
        try:
            webbrowser.open("http://127.0.0.1:8000")
        except Exception:
            pass
            
    threading.Thread(target=_open_browser, daemon=True).start()
    uvicorn.run("server:server_app", host="127.0.0.1", port=8000, reload=True)

def run_cli():
    from cli import run_cli_solver
    run_cli_solver()

def run_tests():
    import unittest
    print("\n" + "=" * 60)
    print("[*] RUNNING AI N-PUZZLE SOLVER TEST SUITE")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n[SUCCESS] All unit and algorithm tests passed successfully!")
    else:
        print("\n[FAILURE] Some tests failed.")
        sys.exit(1)


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower().strip()
        if arg in ("web", "server", "gui"):
            run_web()
            return
        elif arg in ("cli", "terminal"):
            run_cli()
            return
        elif arg in ("test", "tests"):
            run_tests()
            return

    print("=" * 60)
    print("   AI N-PUZZLE SOLVER (5th SEMESTER AI PROJECT)")
    print("=" * 60)
    print("Select mode to run:")
    print("1. Web Application Dashboard (Recommended - Browser GUI)")
    print("2. Interactive Terminal CLI")
    print("3. Run Full Automated Test Suite")
    print("4. Exit")

    choice = input("\nEnter choice (1-4) [Default 1]: ").strip()
    if choice == "2":
        run_cli()
    elif choice == "3":
        run_tests()
    elif choice == "4":
        print("Goodbye!")
    else:
        run_web()

if __name__ == "__main__":
    main()
