import argparse
import logging
import sys
import time
import keyboard

import config
from capture.window_manager import WindowManager
from capture.screen_capture import ScreenCapture
from vision.preprocessing import preprocess_board_image
from vision.board_detector import BoardDetector
from vision.piece_detector import PieceDetector
from solver.board_state import BoardState
from solver.greedy_solver import GreedySolver
from control.mouse_controller import MouseController
from control.action_verifier import ActionVerifier

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("UnMazeSolver")

# Fix for Windows display scaling (DPI)
# Without this, pyautogui clicks the wrong coordinates if Windows display scaling > 100%
if sys.platform == 'win32':
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass

def main():
    parser = argparse.ArgumentParser(description="UnMaze Autonomous Bot")
    parser.add_argument("--dry-run", action="store_true", help="Detect and solve, but do not click")
    parser.add_argument("--debug", action="store_true", help="Show debug visualization")
    parser.add_argument("--delay", type=float, default=config.CLICK_DELAY, help="Delay between clicks")
    parser.add_argument("--once", action="store_true", help="Solve only one board and exit")
    parser.add_argument("--calibrate", action="store_true", help="Interactive mode to set specific game region")
    args = parser.parse_args()

    config.DRY_RUN = args.dry_run
    config.DEBUG_MODE = args.debug
    config.CLICK_DELAY = args.delay
    if args.once:
        config.CONTINUOUS_MODE = False

    logger.info("Initializing UnMaze Solver Bot...")

    # 1. Setup Capture
    wm = WindowManager()

    if args.calibrate:
        logger.info("CALIBRATION MODE: Ensure the browser is open before continuing.")

    logger.info("Please select the game window from the terminal prompt.")
    window = wm.select_window()
    if not window:
        logger.error("No window selected. Exiting.")
        sys.exit(1)

    logger.info("Maximizing game window...")
    wm.maximize_window()

    time.sleep(2) # Give window time to render

    capture = ScreenCapture()

    # 2. Modules
    board_detector = BoardDetector()
    piece_detector = PieceDetector()
    solver = GreedySolver()
    mouse = MouseController(click_delay=config.CLICK_DELAY)
    verifier = ActionVerifier(capture)

    window_rect = wm.get_window_rect()
    if not window_rect:
        logger.warning("Could not get window rect, falling back to full screen capture.")
        region = None
    else:
        left, top, w, h = window_rect
        region = (left, top, w, h)

    logger.info("Starting automation loop. Press 'ESC' or 'CTRL+C' in terminal to stop.")

    try:
        while True:
            if keyboard.is_pressed('esc'):
                logger.info("Emergency Stop (ESC) pressed! Terminating...")
                break

            # 3. Capture
            if region:
                img = capture.capture_region(region)
            else:
                img = capture.capture_full_screen()

            if img is None:
                logger.warning("Failed to capture screen. Retrying...")
                time.sleep(0.5)
                continue

            # 4. Find Game Board
            board_bbox = board_detector.detect_board(img)
            if not board_bbox:
                logger.debug("No board detected. Waiting...")
                time.sleep(0.1)
                continue

            bx, by, bw, bh = board_bbox
            board_img = img[by:by+bh, bx:bx+bw]

            # 5. Vision Pipeline
            binary_board = preprocess_board_image(board_img)
            pieces = piece_detector.detect_pieces(binary_board)

            if not pieces:
                logger.info("No pieces found! Level might be solved or loading.")
                if not config.CONTINUOUS_MODE:
                    logger.info("Running in --once mode. Exiting as board is clear.")
                    break
                time.sleep(0.5)
                continue

            # 6. Solver
            board_state = BoardState(bw, bh, pieces)
            next_piece_id = solver.get_next_move(board_state)

            if next_piece_id is None:
                logger.warning("Solver stuck! No unblocked pieces found.")
                time.sleep(0.5)
                continue

            target_piece = board_state.pieces[next_piece_id]
            logger.info(f"Selected Piece ID: {target_piece.id} | Direction: {target_piece.direction}")

            # 7. Action
            global_x = target_piece.center[0] + bx + (region[0] if region else 0)
            global_y = target_piece.center[1] + by + (region[1] if region else 0)

            if config.DRY_RUN:
                logger.info("DRY-RUN: Hovering piece instead of clicking.")
                mouse.hover_piece(target_piece.center[0], target_piece.center[1],
                                  offset_x=bx + (region[0] if region else 0),
                                  offset_y=by + (region[1] if region else 0))
                time.sleep(1)
            else:
                mouse.click_piece(global_x, global_y)

                # 8. Verify action
                logger.debug("Waiting for board to stabilize...")
                changed = verifier.wait_for_animation((global_x - 50, global_y - 50, 100, 100), timeout=config.ANIMATION_TIMEOUT)

                # If the board did not change, the click likely didn't register.
                # In order to prevent an infinite loop of clicking the exact same piece endlessly
                # without success, we briefly move the mouse away to reset any hover state
                if not changed:
                    logger.debug("Click did not seem to change the board, resetting hover state.")
                    mouse.hover_piece(0, 0) # Move to corner briefly
                    time.sleep(0.1)

    except KeyboardInterrupt:
        logger.info("Terminated by user (Ctrl+C).")
    finally:
        capture.close()
        logger.info("Automation stopped.")

if __name__ == "__main__":
    main()
