from Tile import Tile
import random
from collections import deque

class Board:
    def __init__(self, w = 10, h = 10, m_count = 10):
        self.width = w
        self.height = h
        self.mine_count = m_count
        self.flags_placed = 0
        self.make_grid = [[Tile() for K in range(w)] for U in range(h)]
        self.are_mines_placed = False
        self.is_reveal_done = False
        self.fail_state = False
        self.win_state = False
        self.mine_explosion = None
        self.board_reveal = deque()

    
        

    def board_reset(self, m_count = None):
        if m_count is not None:
            self.mine_count = m_count
        self.are_mines_placed = False
        self.is_reveal_done = False
        self.fail_state = False
        self.win_state = False
        self.flags_placed = 0
        self.mine_explosion = None
        self.board_reveal.clear()
        for K in range(self.height):
            for U in range(self.width):
                self.make_grid[K][U].reset()

    def _find_adj_mines(self, K, U):
        for k in (-1, 0, 1):
            for u in (-1, 0, 1):
                if u == 0 and k == 0:
                    continue
                a = K + k
                n = U + u
                if 0 <= a < self.width and 0 <= n < self.height:
                    yield a, n

    def set_mines(self, start): #start should be safe
        c1, c2 = start
        safety_zone = {(c1, c2)}
        for p1, p2 in self._find_adj_mines(c1, c2):
            safety_zone.add((p1, p2))
        global_coordinates = [(K, U) for U in range(self.height) for K in range(self.width) if (K, U) not in safety_zone]
        mine_count_total = min(self.mine_count, len(global_coordinates))
        mine_locations = random.sample(global_coordinates, mine_count_total)
        for (a, n) in mine_locations:
            self.make_grid[a][n].is_mine = True
        for (a, n) in mine_locations:
            for j, k in self._find_adj_mines(a, n):
                self.make_grid[j][k].adj_mines += 1
    def show_tile(self, K, U):
        if self.fail_state or self.win_state:
            return None
        space = self.make_grid[K][U]
        if not self.are_mines_placed:
            self.set_mines((K, U))
            self.are_mines_placed = True
        if space.flagged or space.is_revealed or space.full_reveal:
            return None
        if space.is_mine:
            self.mine_explosion = (K, U)
            self.fail_state = True
            space.is_revealed = True
            for r in self.make_grid:
                for c in r:
                    if c.is_mine:
                        c.is_revealed = True

            return 'game over'
        
        space.is_revealed = True
        if space.adj_mines == 0:
            for j, k in self._find_adj_mines(K, U):
                adj = self.make_grid[k][j]
                if (not adj.is_revealed) and (not adj.flagged) and (not adj.full_reveal):
                    if not adj.is_mine:
                        adj.full_reveal = True
                        self.board_reveal.append((j, k))
                        self.is_reveal_done = True

        if self.win_check():
            return 'Win!'
        return None

    def anime_show(self):
        if not self.board_reveal:
            return
        K, U = self.board_reveal.popleft()
        space = self.make_grid[U][K]
        space.is_revealed = True
        space.full_reveal = False
        if space.adj_mines == 0:
            for k, u in self._find_adj_mines(K, U):
                adj = self.make_grid[u][k]
                if (not adj.is_revealed) and (not adj.flagged) and (not adj.full_reveal):
                    if not adj.is_mine:
                        adj.full_reveal = True
                        self.board_reveal.append((k, u))
        if not self.board_reveal:
            self.is_reveal_done = False
            self.win_check()

    def flag_on_off(self, K, U):
        if self.fail_state or self.win_state:
            return
        space = self.make_grid[U][K]
        if space.is_revealed:
            return
        if space.flagged:
            space.flagged = False
            self.flags_placed -= 1
        else:
            if self.flags_placed < self.mine_count:
                space.flagged = True
                self.flags_placed += 1
    def win_check(self):
        if self.fail_state:
            return False
        for r in self.make_grid:
            for c in r:
                if not c.is_mine and not c.is_revealed:
                    return False
        self.win_state = True
        return True
