class Tile:
    def __init__(self):
        self.is_mine = False  # Indicates whether this tile contains a mine
        self.is_revealed = False  # Indicates whether the tile has been uncovered by the player
        self.flagged = False  # Indicates whether the player has placed a flag on this tile
        self.adj_mines = 0  # Count of mines in adjacent tiles (0-8)
        self.full_reveal = False  # Used for recursive reveal of empty tiles during gameplay

    def reset_tile(self):
        """Resets the tile to its initial state for a new game"""
        self.is_mine = False  # Remove any mine from this tile
        self.is_revealed = False  # Hide the tile (cover it up)
        self.flagged = False  # Remove any flag placed by the player
        self.adj_mines = 0  # Reset adjacent mine count to zero
        self.full_reveal = False  # Reset the recursive reveal flag