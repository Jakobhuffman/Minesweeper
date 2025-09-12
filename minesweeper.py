
from GameLogic import GameLogic

def get_mine_count():
    # Get the number of mines from the user
    print("Welcome to Minesweeper!")
    print("Board: 10x10 grid (A-J columns, 1-10 rows)")
    
    while True:
        try:
            mine_count = int(input("\nEnter number of mines (10-20): "))
            if 10 <= mine_count <= 20:
                return mine_count
            else:
                print("Please enter a number between 10 and 20.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    # Main function to run the Minesweeper game.
    mine_count = get_mine_count()
    
    print(f"\nStarting game with {mine_count} mines.")
    print("Commands: 'uncover A1' to uncover, 'flag B2' to flag")
    
    # Create and run the game 
    game = GameLogic(10, 10, mine_count)
    game.run_game()

if __name__ == "__main__":
    main()
