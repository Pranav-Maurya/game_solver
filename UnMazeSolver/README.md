# UnMaze Autonomous Bot

An autonomous desktop bot that solves the YouTube Playables game "UnMaze" using live screen capture, computer vision, and mouse automation.

## Mechanics & Architecture

* **Live Screen Capture (`mss`)**: The bot rapidly screenshots the active browser window instead of requiring manual image uploads.
* **Computer Vision (`OpenCV`)**: The visual pipeline converts the board to a binary mask, reconstructing individual pieces as complete geometric entities using connected components, and determines their movement direction using convex hulls.
* **Solver Algorithm (`numpy`)**: The solver avoids blind guessing by performing accurate pixel sweep collisions of the geometric masks to determine which piece can slide off the board freely.
* **Automation (`pyautogui`)**: Safely takes control of the mouse, clicks the unblocked piece, and utilizes an action-verifier to wait for visual stabilization (animations finishing) before recalculating the next move.

## Setup & Installation

### Windows Easy Install (Recommended)

1. Ensure you have **Python 3.x** installed and added to your system PATH.
2. Download or clone this repository.
3. Double-click the `run.bat` file.
   * This batch script will automatically create a virtual environment (optional/if configured), install all dependencies from `requirements.txt`, and start the bot.

### Manual Setup (Linux/Mac/Windows)

```bash
# Clone the repository
git clone https://github.com/Pranav-Maurya/game_solver.git
cd game_solver

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

## How to Use

1. Open your browser (e.g., Google Chrome or Brave).
2. Start the "UnMaze" game and ensure the puzzle board is fully visible on the screen. (Note: If the board is larger than the screen, you *must* use your mouse wheel to zoom out until the borders are visible).
3. Run the bot (`run.bat` or `python main.py`).
4. The terminal will list your open windows. Type the number corresponding to your browser window and press Enter.
5. The bot will automatically maximize the browser, scan the board, and begin solving it in real-time!

### Command Line Arguments

* `--dry-run`: Runs the vision pipeline and calculates the solution, but will only *hover* the mouse over the pieces. It will **not** click. (Great for testing safely).
* `--once`: Solves exactly one board and then exits, instead of waiting continuously for new levels.
* `--calibrate`: Interactive mode to help lock onto specific game coordinates.
* `--debug`: Shows detailed OpenCV visualization windows during solving.
* `--delay <seconds>`: Override the default 0.5s wait between clicks.

## Emergency Stop / Failsafe

If the bot makes a mistake or you need to regain control of your computer:
1. **PyAutoGUI Failsafe**: Slam your physical mouse into any of the 4 extreme corners of your monitor. This immediately crashes the bot and returns control.
2. **Keyboard Interrupt**: Press `ESC` on your keyboard, or press `Ctrl+C` in the terminal window running the script.

## Known Limitations
* The solver currently requires the *entire* board to be visible on the screen at once. If a level is massively oversized, it will fail to detect blocked pieces that extend off-screen.
