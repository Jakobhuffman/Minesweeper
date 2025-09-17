from Tile import Tile #imports Tile class from Tile.py
import random #imports random module to generate random numbers
from collections import deque #imports deque function from collections module

class Board: #Creates Board class for the game board
    def __init__(self, w = 10, h = 10, m_count = 10): #initalizes class variables/functions
        self.width = w #Width of board
        self.height = h #Height of board
        self.mine_count = m_count #number of mines on board
        self.flags_placed = 0 #numbers of flags placed by the player
        self.make_grid = [[Tile() for K in range(w)] for U in range(h)] #creates game board
        self.are_mines_placed = False #tracks if mines have been placed on the board
        self.is_reveal_done = False #tracks if full board reveal is done
        self.fail_state = False #has player lost
        self.win_state = False #has player won
        self.mine_explosion = None #hold location of mine that has exploded
        self.board_reveal = deque() #function for revealing full board

    
        

    def board_reset(self, m_count = None):#Function that resets game board
        if m_count is not None: 
            self.mine_count = m_count #resets number of mines
        self.are_mines_placed = False #resets .are_mines_placed flag
        self.is_reveal_done = False #resets .is_reveal_dones flag
        self.fail_state = False #resets .fail_state flag
        self.win_state = False #resets .win_state flag
        self.flags_placed = 0 #resets number of flags placed
        self.mine_explosion = None #resets .mine_explosion
        self.board_reveal.clear() #resets full board reveal function
        #############################Loop resets each Tile on board
        for K in range(self.height):
            for U in range(self.width):
                self.make_grid[K][U].reset()
        #############################

    def _find_adj_mines(self, K, U):
        #Checks adjacent tiles vertically and horizontally
        for k in (-1, 0, 1): 
            for u in (-1, 0, 1):
        #########################################
                if u == 0 and k == 0: #does not check case of current space
                    continue
                a = K + k #Find adjacent X coordinate
                n = U + u #Find adjacent Y coordinate
                if 0 <= a < self.width and 0 <= n < self.height:#Make sure target is within board boundaries
                    yield a, n #Return valid adjacent tile coordinates

    def set_mines(self, start): #start should be safe
        c1, c2 = start #set starting point to tile that the player clicked first
        safety_zone = {(c1, c2)} #set zone where mine should NOT be placed to first tile clicked
        for p1, p2 in self._find_adj_mines(c1, c2): #place adjacent tiles into safety zone
            safety_zone.add((p1, p2))
        global_coordinates = [(K, U) for U in range(self.height) for K in range(self.width) if (K, U) not in safety_zone] #create list of coordinates that are not safe
        mine_count_total = min(self.mine_count, len(global_coordinates)) #make sure total mines placed does not exceed limit
        mine_locations = random.sample(global_coordinates, mine_count_total) #Randomly choose spaces for the mines to be placed
        for (a, n) in mine_locations: #place mines at randomly generated locations
            self.make_grid[a][n].is_mine = True
            #########################################increment adjacent mines counter for adjacent tiles
        for (a, n) in mine_locations: 
            for j, k in self._find_adj_mines(a, n):
                self.make_grid[j][k].adj_mines += 1
            ###########################################
    def show_tile(self, K, U):
        if self.fail_state or self.win_state: #Check if game is over
            return None
        space = self.make_grid[K][U] #Get tile at (K, U)
        if not self.are_mines_placed: #Place mines if they have not been placed
            self.set_mines((K, U))
            self.are_mines_placed = True
        if space.flagged or space.is_revealed or space.full_reveal: #Do nothing if tile is flagged, revealed, or if full reveal is in progress
            return None
        if space.is_mine: #Trigger fail state if tile is mine
            self.mine_explosion = (K, U) #Store location of mine that was clicked
            self.fail_state = True #Set fail_state to True
            space.is_revealed = True #Set revealed flag to true
            for r in self.make_grid: # Reveal all tiles on board
                for c in r:
                    if c.is_mine:
                        c.is_revealed = True

            return 'game over'
        
        space.is_revealed = True #show that tile is safe
        if space.adj_mines == 0: #Case for if tile has no adjacent mines
            for j, k in self._find_adj_mines(K, U): #Iterate through adjacent tiles
                adj = self.make_grid[k][j] #Get adjacent tile
                if (not adj.is_revealed) and (not adj.flagged) and (not adj.full_reveal): #only handle adjacent tiles that have not been reavealed or flagged
                    if not adj.is_mine:
                        adj.full_reveal = True #
                        self.board_reveal.append((j, k)) #Add tile to queue to be revealed
                        self.is_reveal_done = True 

        if self.win_check(): #Check if action wins game
            return 'Win!'
        return None

    def anime_show(self): #reveals the full board
        if not self.board_reveal: #checks that the game is over to reveal board
            return
        K, U = self.board_reveal.popleft() #return next tile that is set to be revealed
        space = self.make_grid[U][K] #Get tile at coordinates (K, U)
        space.is_revealed = True #set tile's is_revealed flag to True
        space.full_reveal = False #set tile's full_reveal flag to False so that it is done when it comes to full board reveal
        if space.adj_mines == 0: #if tile has no adjacent mines reveal neighbors
            for k, u in self._find_adj_mines(K, U): #check valid adjacent tile coordinates
                adj = self.make_grid[u][k] #get adjacent tile
                if (not adj.is_revealed) and (not adj.flagged) and (not adj.full_reveal): #check adjacent tile only if it is not already revealed, not flagged, and if full board reveal has not happened
                    if not adj.is_mine: #if adjacent tile is not mine reveal it
                        adj.full_reveal = True
                        self.board_reveal.append((k, u))
        if not self.board_reveal: #If there are not any more spaces to reveal, finish revealing
            self.is_reveal_done = False
            self.win_check()

    def flag_on_off(self, K, U): #toggles tile flag on/off
        if self.fail_state or self.win_state: #function does not run if game is over
            return
        space = self.make_grid[U][K] #sets space that function will operate on
        if space.is_revealed: #cannot flag revealed space
            return
        if space.flagged: #Turns off flag
            space.flagged = False
            self.flags_placed -= 1 #decrements number of flags placed
        else: #Turns on flag
            if self.flags_placed < self.mine_count: #can only flag tiles if total flags placed is less than the number of mines
                space.flagged = True
                self.flags_placed += 1 #increments number of flags placed
    def win_check(self): #Checks if the player has won the game
        if self.fail_state: #checks if the player has lost the game, if so return False
            return False
        ##############################Checks if any tiles are not revealed, if so the game is not over
        for r in self.make_grid: 
            for c in r:
                if not c.is_mine and not c.is_revealed:
                    return False
        ##############################
        self.win_state = True #Sets win state to true
        return True
