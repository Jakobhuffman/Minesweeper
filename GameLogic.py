import os # Imports the os module for operating system dependent functionality
import sys # Imports the sys module for system-specific parameters and functions
from Board import Board # Imports the Board class from the Board.py file

class GameLogic: # Defines the GameLogic class to manage the game flow
    def __init__(self, width, height, mine_count): # Initializes the GameLogic object
        self.board = Board(width, height, mine_count) # Creates a new Board object with specified dimensions and mine count
        self.game_state = "playing" # Sets the initial state of the game to "playing"

    def handle_input(self, command): # Defines a method to process user input
        if self.game_state != "playing": # Checks if the game is already over
            print(f"Game is already over. State: {self.game_state.upper()}")
            return # Exits the method if the game is not in the "playing" state

        parts = command.lower().split() # Converts the command to lowercase and splits it into parts
        if not parts: # Checks if the command is empty
            return # Exits the method if there are no parts to the command

        action = parts[0] # Gets the action part of the command (e.g., 'uncover', 'flag')
        if len(parts) < 2: # Checks if the command has at least two parts (action and coordinate)
            print("Invalid command. Please use 'uncover A1' or 'flag B2'.")
            return # Exits the method if the command is incomplete

        try: # Starts a try block to handle potential errors in coordinate parsing
            col_char = parts[1][0] # Gets the column character from the coordinate (e.g., 'A')
            row_num = int(parts[1][1:]) # Converts the row part of the coordinate to an integer
            
            col = ord(col_char) - ord('a') # Converts the column character to a zero-based index (e.g., 'a' -> 0)
            row = row_num - 1 # Converts the 1-based row number to a zero-based index

            if not (0 <= row < self.board.height and 0 <= col < self.board.width): # Checks if the coordinates are within the board's boundaries
                print("Coordinates out of bounds.")
                return # Exits the method if coordinates are out of bounds

            if action == 'uncover' or action == 'u': # Checks if the action is 'uncover' or 'u'
                result = self.board.show_tile(row, col) # Calls the show_tile method on the board
                if result == 'game over': # Checks if the result of showing the tile is 'game over'
                    self.game_state = "loss" # Sets the game state to "loss"
                elif result == 'Win!': # Checks if the result is a win
                    self.game_state = "win" # Sets the game state to "win"
            elif action == 'flag' or action == 'f': # Checks if the action is 'flag' or 'f'
                self.board.flag_on_off(row, col) # Toggles the flag on the specified tile
            else: # If the action is not recognized
                print("Invalid action. Use 'uncover' or 'flag'.")

        except (ValueError, IndexError): # Catches errors if coordinate parsing fails
            print("Invalid coordinate format. Please use 'uncover A1' or 'flag B2'.")

    def display_board(self): # Defines a method to display the current state of the board
        os.system('cls' if os.name == 'nt' else 'clear') # Clears the console screen

        # Print column headers
        print("   " + " ".join([chr(ord('A') + i) for i in range(self.board.width)]))
        
        # Print the grid
        for row in range(self.board.height): # Iterates over each row of the board
            # Print row numbers with proper formatting
            sys.stdout.write(f"{row + 1:2} ") # Writes the row number to the console
            for col in range(self.board.width): # Iterates over each column in the current row
                tile = self.board.make_grid[row][col] # Gets the tile object at the current row and column
                
                # Check for flagged tiles first
                if tile.flagged: # Checks if the tile is flagged
                    sys.stdout.write("F ") # Writes 'F' for a flagged tile
                elif tile.is_revealed: # Checks if the tile has been revealed
                    if tile.is_mine: # Checks if the revealed tile is a mine
                        # Show the exploded mine differently
                        if self.game_state == "loss" and (row, col) == self.board.mine_explosion: # Checks if this is the mine that was clicked to end the game
                            sys.stdout.write("💣 ") # Writes an explosion emoji for the clicked mine
                        else: # For other mines revealed at the end of the game
                            sys.stdout.write("💥 ") # Writes a different explosion emoji
                    elif tile.adj_mines > 0: # Checks if the tile has adjacent mines
                        sys.stdout.write(f"{tile.adj_mines} ") # Writes the number of adjacent mines
                    else: # If the tile has no adjacent mines
                        sys.stdout.write(". ") # Writes a '.' for an empty revealed tile
                else: # If the tile is not flagged and not revealed
                    sys.stdout.write("# ") # Writes '#' for a hidden tile
            print() # Moves to the next line after printing a row
            
        print("\n--- Status ---")
        print(f"Mines: {self.board.mine_count}")
        print(f"Flags Placed: {self.board.flags_placed}")
        print(f"Remaining Mines: {self.board.mine_count - self.board.flags_placed}")
        print(f"Status: {self.game_state.upper()}")

    def run_game(self): # Defines the main game loop
        self.display_board() # Displays the initial board
        while self.game_state == "playing": # Loop continues as long as the game is in the "playing" state
            try: # Starts a try block to handle user exit commands (Ctrl+C)
                command = input("Enter command (e.g., 'uncover A1', 'flag B2'): ")
                self.handle_input(command) # Processes the user's command
                self.display_board() # Refreshes the board display after the command
            except (KeyboardInterrupt, EOFError): # Catches Ctrl+C or end-of-file
                print("\nExiting game.")
                self.game_state = "exit" # Sets the game state to "exit" to stop the loop
        
        if self.game_state == "loss": # Checks if the game ended in a loss
            print("Game Over! You uncovered a mine.")
        elif self.game_state == "win": # Checks if the game ended in a win
            print("Congratulations! You won the game!")