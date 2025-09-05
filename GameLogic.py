import os
import sys
from Board import Board
from collections import deque

class GameLogic:
   
    #Manages the overall game flow, state transitions, and user actions
    #for a terminal-based Minesweeper game.
    def __init__(self, width, height, mine_count):
        #Initializes the game logic with board dimensions and mine count.
        #Args: width (int): The width of the board, height (int): The height of the board, mine_count (int): The number of mines on the board.
        self.board = Board(width, height, mine_count)
        self.game_state = "playing"  # Can be "playing", "win", or "loss"
        self.uncovered_tiles_count = 0

    def handle_input(self, command):
        #Processes a command-line input from the user.
        #Args: command (str): The user's input string (e.g., 'uncover A1', 'flag B2').
        
        if self.game_state != "playing":
            print(f"Game is already over. State: {self.game_state.upper()}")
            return

        parts = command.lower().split()
        if not parts:
            return

        action = parts[0]
        if len(parts) < 2:
            print("Invalid command. Please use 'uncover A1' or 'flag B2'.")
            return

        # Parse row and column from a string like "A1"
        try:
            col_char = parts[1][0]
            row_num = int(parts[1][1:])
            
            col = ord(col_char) - ord('a')
            row = row_num - 1

            if not (0 <= row < self.board.height and 0 <= col < self.board.width):
                print("Coordinates out of bounds.")
                return

            if action == 'uncover' or action == 'u':
                result = self.board.show_tile(row, col)
                if result == 'game over':
                    self.game_state = "loss"
                elif result == 'Win!':
                    self.game_state = "win"
            elif action == 'flag' or action == 'f':
                self.board.flag_on_off(row, col)
            else:
                print("Invalid action. Use 'uncover' or 'flag'.")

        except (ValueError, IndexError):
            print("Invalid coordinate format. Please use 'uncover A1' or 'flag B2'.")

    def display_board(self):
        #Renders the current state of the game board to the terminal.
        #Clear the terminal for a cleaner display
        os.system('cls' if os.name == 'nt' else 'clear')

        # Print column headers (A-J)
        print("  " + " ".join([chr(ord('A') + i) for i in range(self.board.width)]))
        
        # Print the grid
        for r in range(self.board.height):
            # Print row numbers
            sys.stdout.write(f"{r + 1:<2}")
            for c in range(self.board.width):
                tile = self.board.make_grid[r][c]
                
                if tile.is_revealed:
                    if tile.is_mine:
                        if self.game_state == "loss" and (r, c) == self.board.mine_explosion:
                            sys.stdout.write("💣")
                        elif self.game_state == "loss":
                            sys.stdout.write("💥")
                        else:
                            sys.stdout.write("🔥") # Should not be shown in normal play
                    elif tile.adj_mines > 0:
                        sys.stdout.write(f" {tile.adj_mines}")
                    else:
                        sys.stdout.write(" .")
                elif tile.flagged:
                    sys.stdout.write(" F")
                else:
                    sys.stdout.write(" #")
            print()
            
        print("\n--- Status ---")
        print(f"Mines: {self.board.mine_count}")
        print(f"Flags Placed: {self.board.flags_placed}")
        print(f"Remaining Mines: {self.board.mine_count - self.board.flags_placed}")
        print(f"Status: {self.game_state.upper()}")

    def run_game(self):
        #The main game loop for the terminal application.
        self.display_board()
        while self.game_state == "playing":
            try:
                command = input("Enter command (e.g., 'uncover A1', 'flag B2'): ")
                self.handle_input(command)
                self.display_board()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting game.")
                self.game_state = "exit"
        
        # Final board display after game ends
        if self.game_state == "loss":
            print("Game Over! You uncovered a mine.")
            self.display_board()
        elif self.game_state == "win":
            print("Congratulations! You won the game!")
            self.display_board()