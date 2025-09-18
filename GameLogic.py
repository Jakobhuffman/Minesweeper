import os
import sys
from Board import Board

class GameLogic:
    def __init__(self, width, height, mine_count):
        self.board = Board(width, height, mine_count)
        self.game_state = "playing"

    def handle_input(self, command):
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
        os.system('cls' if os.name == 'nt' else 'clear')

        # Print column headers
        print("   " + " ".join([chr(ord('A') + i) for i in range(self.board.width)]))
        
        # Print the grid
        for row in range(self.board.height):
            # Print row numbers with proper formatting
            sys.stdout.write(f"{row + 1:2} ")
            for col in range(self.board.width):
                tile = self.board.make_grid[row][col]
                
                # Check for flagged tiles first
                if tile.flagged:
                    sys.stdout.write("F ")
                elif tile.is_revealed:
                    if tile.is_mine:
                        # Show the exploded mine differently
                        if self.game_state == "loss" and (row, col) == self.board.mine_explosion:
                            sys.stdout.write("💣 ")
                        else:
                            sys.stdout.write("💥 ")
                    elif tile.adj_mines > 0:
                        sys.stdout.write(f"{tile.adj_mines} ")
                    else:
                        sys.stdout.write(". ")
                else:
                    sys.stdout.write("# ")
            print()
            
        print("\n--- Status ---")
        print(f"Mines: {self.board.mine_count}")
        print(f"Flags Placed: {self.board.flags_placed}")
        print(f"Remaining Mines: {self.board.mine_count - self.board.flags_placed}")
        print(f"Status: {self.game_state.upper()}")

    def run_game(self):
        self.display_board()
        while self.game_state == "playing":
            try:
                command = input("Enter command (e.g., 'uncover A1', 'flag B2'): ")
                self.handle_input(command)
                self.display_board()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting game.")
                self.game_state = "exit"
        
        if self.game_state == "loss":
            print("Game Over! You uncovered a mine.")
        elif self.game_state == "win":
            print("Congratulations! You won the game!")