import os
import sys
from Board import Board
from collections import deque

class GameLogic:
    """
    Manages the overall game flow, state transitions, and user actions
    for a terminal-based Minesweeper game.
    """
    def __init__(self, width, height, mine_count):
        self.board = Board(width, height, mine_count)
        self.game_state = "playing"

    def handle_input(self, command):
        if self.game_state != "playing":
            print(f"Game is already over. State: {self.game_state.upper()}")
            return

        parts = command.lower().split()

        if len(parts) == 1 and parts[0] in ['quit', 'exit']:
            self.game_state = "exit"
            return

        if len(parts) != 2:
            print("Invalid command. Please use 'uncover A1' or 'flag B2'.")
            return

        action, coords = parts[0], parts[1]
        
        try:
            col = ord(coords[0]) - ord('a')
            row = int(coords[1:]) - 1

            if not (0 <= row < self.board.height and 0 <= col < self.board.width):
                print("Coordinates out of bounds.")
                return

            if action in ['uncover', 'u']:
                result = self.board.show_tile(row, col)
                if result == 'loss':
                    self.game_state = "loss"
                elif result == 'win':
                    self.game_state = "win"
                elif result == 'already_revealed':
                    print("That tile is already revealed.")
                elif result == 'flagged':
                    print("Cannot uncover a flagged tile. Unflag it first.")
            elif action in ['flag', 'f']:
                result = self.board.flag_on_off(row, col)
                if result == 'already_revealed':
                    print("Cannot flag a revealed tile.")
                elif result == 'no_more_flags':
                    print(f"No more flags to place. You can only use {self.board.mine_count}.")
            else:
                print("Invalid action. Use 'uncover' or 'flag'.")
        except (ValueError, IndexError):
            print("Invalid coordinate format. Please use 'uncover A1' or 'flag B2'.")

    def display_board(self):
        #Renders the current state of the game board to the terminal.
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("  " + " ".join([chr(ord('A') + i) for i in range(self.board.width)]))
        for r in range(self.board.height):
            sys.stdout.write(f"{r + 1:<2}")
            for c in range(self.board.width):
                tile = self.board.grid[r][c]
                
                if tile.is_revealed:
                    if tile.is_mine:
                        sys.stdout.write(" 💣")
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
        while self.game_state == "playing":
            self.display_board()
            try:
                command = input("Enter command (e.g., 'uncover A1', 'flag B2'): ")
                self.handle_input(command)
            except (KeyboardInterrupt, EOFError):
                self.game_state = "exit"
        
        # Display the final board after the game ends
        if self.game_state == "loss":
            self.display_board()
            print("Game Over! You uncovered a mine.")
        elif self.game_state == "win":
            self.display_board()
            print("Congratulations! You won the game!")
        elif self.game_state == "exit":
            print("\nExiting game.")