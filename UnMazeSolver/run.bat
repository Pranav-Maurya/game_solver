@echo off
echo ==================================================
echo UnMaze Auto-Solver Setup
echo ==================================================

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH. Please install Python 3 and try again.
    pause
    exit /b 1
)

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Dependencies installed successfully.
echo Starting UnMaze Solver...
python main.py %*
pause
