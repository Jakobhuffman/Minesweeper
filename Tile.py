class Tile:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.flagged = False
        self.adj_mines = 0
        self.full_reveal = False

    def reset_tile(self):
        self.is_mine = False
        self.is_revealed = False
        self.flagged = False
        self.adj_mines = 0
        self.full_reveal = False
