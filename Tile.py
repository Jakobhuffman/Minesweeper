class Tile:
    """Represents a single tile on the Minesweeper board."""
    def __init__(self):
        """Initializes a tile to its default, hidden state."""
        self.is_mine = False   #Shows if the tile is a mine
        self.is_revealed = False  #Shows if the status of the tile is revealed to the player or not
        self.flagged = False  #Shows if the tile has been flagged by the player
        self.adj_mines = 0  #Shows number of adjacent mines to the tile
        

    def reset(self):
        """Resets the tile to its initial state for a new game."""
        self.is_mine = False  #Resets mine/not mine status
        self.is_revealed = False #Hides tile
        self.flagged = False #unflags tile
        self.adj_mines = 0 #Sets adjacent mine count to 0