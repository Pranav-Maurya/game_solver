import cv2
import numpy as np
import time
from capture.screen_capture import ScreenCapture

class ActionVerifier:
    def __init__(self, capture: ScreenCapture):
        self.capture = capture

    def wait_for_animation(self, region, timeout=2.0, max_frames=20):
        """
        Wait for the game board to stabilize visually after a click.
        Returns True if stabilized, False if it timed out.
        """
        prev_img = self.capture.capture_region(region)
        if prev_img is None:
            time.sleep(0.5)
            return True

        start_time = time.time()

        for _ in range(max_frames):
            if time.time() - start_time > timeout:
                return False # Timeout

            time.sleep(0.05)
            curr_img = self.capture.capture_region(region)

            if curr_img is None:
                continue

            # Calculate mean squared error (MSE) between frames
            err = np.sum((prev_img.astype("float") - curr_img.astype("float")) ** 2)
            err /= float(prev_img.shape[0] * prev_img.shape[1])

            # If visual difference is very small, animation is likely over
            if err < 50:
                return True

            prev_img = curr_img

        return False
