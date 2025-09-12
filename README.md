# Minesweeper
Project 1 Minesweeper System Development

How to Run
1. Make sure you have Python 3 installed.
2. Navigate to the project directory in your terminal.
3. Run the command: `python3 minesweeper.py`
4. Follow the on-screen prompts to choose the number of mines and start playing.

Rules
The objective of the game is to clear a grid of hidden squares without detonating any mines. Some of the hidden squares will be mines. If you uncover a square that is a mine, the game is over.
When you uncover a square, if it is not a mine it will show how many mines are adjacent to the square. The first square you uncover is always safe.
You can flag squares you think may be a mine.

How to Play
The game is played on a 10x10 grid. You interact with the game by typing commands into the terminal.

### Commands
*   **Uncover a tile:** `uncover <coordinate>` or `u <coordinate>`
    *   Example: `uncover A1`
*   **Flag a tile:** `flag <coordinate>` or `f <coordinate>`
    *   Example: `flag B2`

Coordinates are composed of a column letter (A-J) and a row number (1-10).
