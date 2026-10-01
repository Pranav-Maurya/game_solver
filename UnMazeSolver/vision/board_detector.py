import cv2
import numpy as np

class BoardDetector:
    def __init__(self):
        pass

    def detect_board(self, image):
        """
        Detects the outer boundary of the game board.
        Returns the (x, y, w, h) bounding box of the board.
        """
        if image is None:
            return None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # The game board usually has a faint bounding box or is a massive
        # concentrated area of black arrows.
        # We can find the bounding box of all arrows combined.
        binary = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )

        # Find all contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        # Get the bounding box of ALL contours combined to find the global board area
        x_min, y_min = np.inf, np.inf
        x_max, y_max = 0, 0

        valid_contours_found = False

        for contour in contours:
            if cv2.contourArea(contour) > 50:
                valid_contours_found = True
                x, y, w, h = cv2.boundingRect(contour)
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x + w)
                y_max = max(y_max, y + h)

        if not valid_contours_found:
            return None

        # Add a small margin
        margin = 10
        x_min = max(0, x_min - margin)
        y_min = max(0, y_min - margin)
        x_max = min(image.shape[1], x_max + margin)
        y_max = min(image.shape[0], y_max + margin)

        return (x_min, y_min, x_max - x_min, y_max - y_min)
