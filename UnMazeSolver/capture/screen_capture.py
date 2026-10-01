import mss
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()

    def capture_full_screen(self):
        """Captures the primary monitor full screen."""
        try:
            # Monitor 1 is the primary monitor in MSS
            monitor = self.sct.monitors[1]
            sct_img = self.sct.grab(monitor)
            # Convert to numpy array and drop alpha channel (BGRA -> BGR)
            img = np.array(sct_img)[:, :, :3]
            return img
        except Exception as e:
            logger.error(f"Error capturing full screen: {e}")
            return None

    def capture_region(self, region):
        """
        Captures a specific region of the screen.
        region: tuple of (left, top, width, height)
        """
        try:
            left, top, width, height = region
            monitor = {"top": top, "left": left, "width": width, "height": height}
            sct_img = self.sct.grab(monitor)
            # Convert to numpy array and drop alpha channel (BGRA -> BGR)
            img = np.array(sct_img)[:, :, :3]
            return img
        except Exception as e:
            logger.error(f"Error capturing region: {e}")
            return None

    def close(self):
        self.sct.close()
