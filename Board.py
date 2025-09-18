from Tile import Tile # Imports Tile class from Tile.py
import random # Imports random module to generate random numbers
from collections import deque # Imports deque function from collections module

class Board: # Creates Board class for the game board
    def __init__(self, w=10, h=10, m_count=10): # Initializes class variables/functions
        self.width = w # Width of board
        self.height = h # Height of board
        self.mine_count = m_count # Number of mines on board
        self.flags_placed = 0 # Number of flags placed by the player
        self.make_grid = [[Tile() for _ in range(w)] for _ in range(h)] # Creates game board grid
        self.are_mines_placed = False # Tracks if mines have been placed on the board
        self.fail_state = False # Indicates if player has lost the game
        self.win_state = False # Indicates if player has won the game
        self.mine_explosion = None # Holds location of mine that has exploded
        self.board_reveal = deque() # Queue for revealing tiles during recursive reveal

    def board_reset(self, m_count=None): # Function that resets game board
        if m_count is not None: 
            self.mine_count = m_count # Resets number of mines
        self.are_mines_placed = False # Resets mines placed flag
        self.fail_state = False # Resets fail state flag
        self.win_state = False # Resets win state flag
        self.flags_placed = 0 # Resets number of flags placed
        self.mine_explosion = None # Resets mine explosion location
        self.board_reveal.clear() # Clears the reveal queue
        
        # Loop resets each Tile on board
        for row in range(self.height):
            for col in range(self.width):
                self.make_grid[row][col].reset_tile()

    def _find_adjacent_tiles(self, row, col):
        """Finds all valid adjacent tiles to the given coordinates"""
        adjacent = []
        # Check all 8 surrounding positions
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0: # Skip the current tile itself
                    continue
                new_row, new_col = row + dr, col + dc
                # Make sure target is within board boundaries
                if 0 <= new_row < self.height and 0 <= new_col < self.width:
                    adjacent.append((new_row, new_col))
        return adjacent

    def set_mines(self, start): # Start should be a safe tile (first click)
        safe_row, safe_col = start # Set starting point to tile that the player clicked first
        safety_zone = {(safe_row, safe_col)} # Set zone where mines should NOT be placed
        
        # Add adjacent tiles to safety zone (guarantee safe area around first click)
        for adj_row, adj_col in self._find_adjacent_tiles(safe_row, safe_col):
            safety_zone.add((adj_row, adj_col))
        
        # Create list of coordinates that are not in safety zone
        possible_locations = []
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) not in safety_zone:
                    possible_locations.append((row, col))
        
        # Make sure total mines placed does not exceed available spaces
        mine_count_total = min(self.mine_count, len(possible_locations))
        # Randomly choose spaces for the mines to be placed
        mine_locations = random.sample(possible_locations, mine_count_total)
        
        # Place mines at randomly generated locations
        for row, col in mine_locations:
            self.make_grid[row][col].is_mine = True
        
        # Calculate adjacent mine counts for all non-mine tiles
        for row in range(self.height):
            for col in range(self.width):
                if not self.make_grid[row][col].is_mine:
                    count = 0
                    for adj_row, adj_col in self._find_adjacent_tiles(row, col):
                        if self.make_grid[adj_row][adj_col].is_mine:
                            count += 1
                    self.make_grid[row][col].adj_mines = count

    def show_tile(self, row, col):
        """Reveals a tile and handles game logic for mine detection and recursive reveal"""
        if self.fail_state or self.win_state: # Check if game is already over
            return None
            
        tile = self.make_grid[row][col] # Get tile at specified coordinates
        
        if not self.are_mines_placed: # Place mines if they haven't been placed yet
            self.set_mines((row, col))
            self.are_mines_placed = True
            
        if tile.flagged or tile.is_revealed: # Do nothing if tile is flagged or already revealed
            return None
            
        if tile.is_mine: # Player clicked on a mine - game over
            self.mine_explosion = (row, col) # Store location of mine that was clicked
            self.fail_state = True # Set fail state to True
            # Reveal all mines on the board
            for r in range(self.height):
                for c in range(self.width):
                    if self.make_grid[r][c].is_mine:
                        self.make_grid[r][c].is_revealed = True
            return 'game over'
        
        tile.is_revealed = True # Reveal the tile (it's safe)
        
        # If tile has no adjacent mines, recursively reveal adjacent tiles
        if tile.adj_mines == 0:
            self._reveal_adjacent_tiles(row, col)

        if self.win_check(): # Check if this action wins the game
            return 'Win!'
        return None

    def _reveal_adjacent_tiles(self, start_row, start_col):
        """Recursively reveals adjacent tiles for empty cells using BFS algorithm"""
        queue = deque([(start_row, start_col)])
        visited = set([(start_row, start_col)])
        
        while queue:
            current_row, current_col = queue.popleft()
            current_tile = self.make_grid[current_row][current_col]
            
            # Only process empty cells (adj_mines == 0)
            if current_tile.adj_mines == 0:
                # Reveal all adjacent cells
                for adj_row, adj_col in self._find_adjacent_tiles(current_row, current_col):
                    if (adj_row, adj_col) not in visited:
                        visited.add((adj_row, adj_col))
                        adj_tile = self.make_grid[adj_row][adj_col]
                        
                        # Only reveal if not flagged, not a mine, and not already revealed
                        if not adj_tile.flagged and not adj_tile.is_mine and not adj_tile.is_revealed:
                            adj_tile.is_revealed = True
                            
                            # If this adjacent tile is also empty, add to queue for further processing
                            if adj_tile.adj_mines == 0:
                                queue.append((adj_row, adj_col))

    def flag_on_off(self, row, col):
        """Toggles flag on/off for a tile"""
        if self.fail_state or self.win_state: # Function doesn't run if game is over
            return
            
        tile = self.make_grid[row][col] # Get the target tile
        
        if tile.is_revealed: # Cannot flag revealed tiles
            return
            
        if tile.flagged: # Remove flag
            tile.flagged = False
            self.flags_placed -= 1 # Decrement number of flags placed
        else: # Add flag
            if self.flags_placed < self.mine_count: # Only flag if haven't reached mine count
                tile.flagged = True
                self.flags_placed += 1 # Increment number of flags placed
                
    def win_check(self):
        """Checks if the player has won the game by revealing all non-mine tiles"""
        if self.fail_state: # Player already lost, cannot win
            return False
            
        # Check if any non-mine tiles are still hidden
        for row in range(self.height):
            for col in range(self.width):
                tile = self.make_grid[row][col]
                if not tile.is_mine and not tile.is_revealed:
                    return False # Game not won yet
                    
        self.win_state = True # All non-mine tiles revealed - player wins!
        return True