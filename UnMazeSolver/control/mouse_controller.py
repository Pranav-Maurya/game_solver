import pyautogui
import time
import logging

logger = logging.getLogger(__name__)

class MouseController:
    def __init__(self, click_delay: float = 0.5):
        # Enable failsafe (moving mouse to corner stops the script)
        pyautogui.FAILSAFE = True
        self.click_delay = click_delay

    def click_piece(self, x: int, y: int, offset_x: int = 0, offset_y: int = 0):
        """
        Moves the mouse and clicks a specific coordinate.
        The offsets are used if the coordinate is relative to a game region bounding box.
        """
        target_x = x + offset_x
        target_y = y + offset_y

        try:
            logger.debug(f"Moving mouse to ({target_x}, {target_y})")
            pyautogui.moveTo(target_x, target_y, duration=0.0) # Instant movement

            # Brief pause to let browser register hover state
            time.sleep(0.05)

            # Some browser games require explicit down/up or double click
            # We use a double click to ensure it registers
            pyautogui.doubleClick()
            logger.info(f"Double-clicked piece at ({target_x}, {target_y})")

            time.sleep(self.click_delay)
            return True

        except pyautogui.FailSafeException:
            logger.warning("Failsafe triggered! Mouse moved to the corner of the screen.")
            raise
        except Exception as e:
            logger.error(f"Failed to click: {e}")
            return False

    def hover_piece(self, x: int, y: int, offset_x: int = 0, offset_y: int = 0):
        """Hover for dry-run/calibration."""
        target_x = x + offset_x
        target_y = y + offset_y
        pyautogui.moveTo(target_x, target_y, duration=0.2)
