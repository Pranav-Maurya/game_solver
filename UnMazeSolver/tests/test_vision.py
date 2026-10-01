import pytest
import cv2
import numpy as np
from vision.preprocessing import preprocess_board_image
from vision.piece_detector import PieceDetector, Piece
from vision.arrow_detector import ArrowDetector

def create_synthetic_arrow(direction):
    """Creates a simple synthetic image of an arrow for testing."""
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    # Draw a line
    cv2.line(img, (20, 50), (70, 50), (0, 0, 0), 5)

    # Draw arrowhead pointing right
    if direction == "RIGHT":
        pts = np.array([[70, 40], [70, 60], [85, 50]], np.int32)
        cv2.fillPoly(img, [pts], (0, 0, 0))
    elif direction == "LEFT":
        cv2.line(img, (30, 50), (80, 50), (0, 0, 0), 5)
        pts = np.array([[30, 40], [30, 60], [15, 50]], np.int32)
        cv2.fillPoly(img, [pts], (0, 0, 0))
    elif direction == "UP":
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        cv2.line(img, (50, 80), (50, 30), (0, 0, 0), 5)
        pts = np.array([[40, 30], [60, 30], [50, 15]], np.int32)
        cv2.fillPoly(img, [pts], (0, 0, 0))
    elif direction == "DOWN":
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        cv2.line(img, (50, 20), (50, 70), (0, 0, 0), 5)
        pts = np.array([[40, 70], [60, 70], [50, 85]], np.int32)
        cv2.fillPoly(img, [pts], (0, 0, 0))

    return img

def test_preprocessing():
    img = create_synthetic_arrow("RIGHT")
    binary = preprocess_board_image(img)
    assert binary is not None
    assert binary.shape == (100, 100)
    # The black arrow should become white (255)
    assert binary[50, 50] == 255
    assert binary[10, 10] == 0

def test_arrow_detector_synthetic():
    for direction in ["RIGHT", "LEFT", "UP", "DOWN"]:
        img = create_synthetic_arrow(direction)
        binary = preprocess_board_image(img)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Should find 1 contour
        assert len(contours) == 1

        detected_dir = ArrowDetector.detect(contours[0])
        assert detected_dir == direction, f"Failed to detect {direction}"


from vision.board_detector import BoardDetector

def test_board_detector():
    # Create an image with some fake arrows spread out
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    cv2.rectangle(img, (50, 50), (100, 100), (0, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (400, 400), (450, 450), (0, 0, 0), cv2.FILLED)

    detector = BoardDetector()
    bbox = detector.detect_board(img)

    assert bbox is not None
    x, y, w, h = bbox
    # The bounds should encapsulate both rectangles, plus margin
    assert x <= 50
    assert y <= 50
    assert x + w >= 450
    assert y + h >= 450
