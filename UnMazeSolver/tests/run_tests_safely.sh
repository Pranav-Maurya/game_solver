#!/bin/bash
export PYTHONPATH=/app/UnMazeSolver
python3 -m pytest -v /app/UnMazeSolver/tests/test_vision.py
python3 -m pytest -v /app/UnMazeSolver/tests/test_solver.py
python3 -m pytest -v /app/UnMazeSolver/tests/test_control.py
python3 -m pytest -v /app/UnMazeSolver/tests/test_capture.py
python3 -m pytest -v /app/UnMazeSolver/tests/test_main.py
