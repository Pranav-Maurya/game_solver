import cv2
import numpy as np

def preprocess_board_image(image):
    """
    Preprocesses the raw screen capture to isolate the dark arrows
    from the white/light background.
    """
    if image is None:
        return None

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Adaptive thresholding to handle slight lighting/background variations.
    # The arrows are black on a white background, so we want the arrows to be WHITE (255)
    # in the binary mask, and the background to be BLACK (0).
    # We use THRESH_BINARY_INV to flip the colors.
    binary = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    # Morphological operations to clean up noise (like the faint background grid dots)
    kernel = np.ones((3,3), np.uint8)
    clean_binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

    return clean_binary
