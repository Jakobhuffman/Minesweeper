class Tile:
    def __init__(self):
        self.is_mine = False #Shows if the tile is a mine
        self.is_revealed = False #Shows if the status of the tile is revealed to the player or not
        self.flagged = False #Shows if the tile has been flagged by the player
        self.adj_mines = 0 #Shows number of adjacent mines to the tile
        self.full_reveal = False #Shows if the tile has been revealed in the full board reveal

    def reset_tile(self):
        self.is_mine = False #Resets mine/not mine status
        self.is_revealed = False #Hides tile
        self.flagged = False #unflags tile
        self.adj_mines = 0 #Sets adjacent mine count to 0
        self.full_reveal = False #Resets full board reveal
