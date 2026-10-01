@echo off
setlocal
echo ==================================================
echo UnMaze Auto-Solver Setup (Virtual Environment)
echo ==================================================

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH. Please install Python 3 and try again.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo Creating a virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo Activating virtual environment and installing dependencies...
call .venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Dependencies installed successfully.
echo Starting UnMaze Solver...
python main.py %*

echo.
echo Solver exited.
pause
