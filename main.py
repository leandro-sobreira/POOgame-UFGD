"""
This is the main module, it will be executed to display the game.
"""
import sys
from src.main_game import Game

# Initializes the game
if __name__ == "__main__":
    try:
        Game()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Optionally, log the error to a file
    finally:
        sys.exit()