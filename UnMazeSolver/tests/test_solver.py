import pytest
import numpy as np
import cv2
from vision.piece_detector import Piece
from solver.board_state import BoardState
from solver.greedy_solver import GreedySolver

def create_mock_piece(id, direction, x, y, w, h):
    mask = np.zeros((200, 200), dtype=np.uint8)
    cv2.rectangle(mask, (x, y), (x+w, y+h), 255, cv2.FILLED)

    return Piece(
        id=id,
        direction=direction,
        center=(x + w//2, y + h//2),
        bbox=(x, y, w, h),
        contour=np.array([]), # Not needed for solver test
        mask=mask
    )

def test_collision_detection():
    # Piece 1 is on the left, pointing right.
    p1 = create_mock_piece(1, "RIGHT", 50, 50, 20, 20)
    # Piece 2 is to the right of p1.
    p2 = create_mock_piece(2, "UP", 100, 40, 20, 40)

    board = BoardState(200, 200, [p1, p2])

    # p1 should be blocked by p2 because it moves RIGHT
    assert board.is_piece_blocked(p1) == True

    # p2 should be FREE because it moves UP and nothing is above it
    assert board.is_piece_blocked(p2) == False

def test_greedy_solver():
    p1 = create_mock_piece(1, "RIGHT", 50, 50, 20, 20)
    p2 = create_mock_piece(2, "UP", 100, 40, 20, 40)

    board = BoardState(200, 200, [p1, p2])
    solver = GreedySolver()

    # Sequence should be: remove p2, then remove p1
    seq = solver.solve_full_sequence(board)
    assert seq == [2, 1]
