@echo off
title AI N-Puzzle Solver
echo ===================================================
echo    AI N-PUZZLE SOLVER - LAUNCHING WEB DASHBOARD
echo ===================================================
echo Opening server at http://127.0.0.1:8000 ...
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python run.py web
    goto end
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py run.py web
    goto end
)

echo [ERROR] Python was not found in your system PATH.
echo Please install Python 3.9+ from https://python.org or add it to PATH.
:end
pause
