import pygetwindow as gw
import logging
import time

logger = logging.getLogger(__name__)

class WindowManager:
    def __init__(self):
        self.target_window = None

    def list_windows(self):
        """Returns a list of all visible windows with titles."""
        windows = gw.getAllTitles()
        return [w for w in windows if w.strip()]

    def select_window(self):
        """Prompts the user to select a window from a list."""
        windows = self.list_windows()
        if not windows:
            logger.error("No windows found!")
            return None

        print("\nAvailable Windows:")
        for i, title in enumerate(windows):
            print(f"{i + 1}. {title}")

        while True:
            try:
                choice = input("\nEnter the number of the browser window running UnMaze: ")
                idx = int(choice) - 1
                if 0 <= idx < len(windows):
                    self.target_window = gw.getWindowsWithTitle(windows[idx])[0]
                    logger.info(f"Selected window: {self.target_window.title}")
                    return self.target_window
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                logger.error(f"Error selecting window: {e}")
                return None

    def maximize_window(self):
        """Maximizes the currently selected window and brings it to the foreground."""
        if not self.target_window:
            logger.warning("No window selected to maximize.")
            return False

        try:
            if not self.target_window.isMaximized:
                self.target_window.maximize()

            # Bring to front
            self.target_window.activate()
            time.sleep(1) # Wait for window to come to front and maximize
            logger.info("Window maximized and brought to foreground.")
            return True
        except Exception as e:
            logger.error(f"Failed to maximize window: {e}")
            return False

    def get_window_rect(self):
        """Returns the bounding box (left, top, width, height) of the window."""
        if not self.target_window:
            return None
        return (
            self.target_window.left,
            self.target_window.top,
            self.target_window.width,
            self.target_window.height
        )
