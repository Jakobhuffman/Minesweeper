import random
from collections import deque
from Tile import Tile

class Board:
    """
    Manages the Minesweeper grid, including mine placement and tile states.
    It sets up the game state based on player actions.
    """
    def __init__(self, width=10, height=10, mine_count=10):
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.flags_placed = 0
        # Renamed `make_grid` to `grid` for consistency and clarity
        self.grid = [[Tile() for _ in range(width)] for _ in range(height)]
        self.are_mines_placed = False
        self.fail_state = False
        self.win_state = False
        self.mine_explosion = None
        # `board_reveal` and `is_reveal_done` were removed as the new logic
        # handles cascading reveals in a single pass.

    def reset_board(self, m_count=None):
        if m_count is not None:
            self.mine_count = m_count
        self.are_mines_placed = False
        self.fail_state = False
        self.win_state = False
        self.flags_placed = 0
        self.mine_explosion = None
        for row in self.grid:
            for tile in row:
                tile.reset()

    def _find_neighbors(self, row, col):
        for r_offset in (-1, 0, 1):
            for c_offset in (-1, 0, 1):
                if r_offset == 0 and c_offset == 0:
                    continue
                n_row, n_col = row + r_offset, col + c_offset
                if 0 <= n_row < self.height and 0 <= n_col < self.width:
                    yield n_row, n_col

    def _set_mines(self, start_pos): #should be safe
        start_row, start_col = start_pos
        safety_zone = {(start_row, start_col)}
        for n_row, n_col in self._find_neighbors(start_row, start_col):
            safety_zone.add((n_row, n_col))

        all_coords = [(r, c) for r in range(self.height) for c in range(self.width)]
        available_coords = [coord for coord in all_coords if coord not in safety_zone]
        
        mine_locations = random.sample(available_coords, min(self.mine_count, len(available_coords)))
        
        for r, c in mine_locations:
            self.grid[r][c].is_mine = True
        
        for r, c in mine_locations:
            for n_r, n_c in self._find_neighbors(r, c):
                self.grid[n_r][n_c].adj_mines += 1
        
        self.are_mines_placed = True

    def _cascade_uncover(self, row, col):
        q = deque([(row, col)])
        
        while q:
            r, c = q.popleft()
            
            tile = self.grid[r][c]
            if tile.is_revealed or tile.flagged:
                continue
            
            tile.is_revealed = True
            
            if tile.adj_mines == 0:
                for n_r, n_c in self._find_neighbors(r, c):
                    q.append((n_r, n_c))

    def show_tile(self, row, col):
        if self.fail_state or self.win_state:
            return None

        if not self.are_mines_placed:
            self._set_mines((row, col))
        
        tile = self.grid[row][col]

        if tile.is_revealed:
            return 'already_revealed'
        if tile.flagged:
            return 'flagged'

        if tile.is_mine:
            self.mine_explosion = (row, col)
            self.fail_state = True
            for r in range(self.height):
                for c in range(self.width):
                    if self.grid[r][c].is_mine:
                        self.grid[r][c].is_revealed = True
            return 'loss'
        
        # Unify the reveal logic by always using the cascade function.
        # It correctly handles both single-tile reveals and cascades.
        self._cascade_uncover(row, col)

        if self.check_win():
            self.win_state = True
            return 'win'
        return 'playing'

    def flag_on_off(self, row, col):
        if self.fail_state or self.win_state:
            return
        
        tile = self.grid[row][col]
        if tile.is_revealed:
            return 'already_revealed'
            
        if tile.flagged:
            tile.flagged = False
            self.flags_placed -= 1
        else:
            if self.flags_placed < self.mine_count:
                tile.flagged = True
                self.flags_placed += 1
            else:
                # All available flags have been used.
                return 'no_more_flags'

    def check_win(self):
        for r in range(self.height):
            for c in range(self.width):
                tile = self.grid[r][c]
                if not tile.is_mine and not tile.is_revealed:
                    return False
        return True
