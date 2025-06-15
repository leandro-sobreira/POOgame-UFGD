"""
This is the main module, it will be executed to display the game.
"""
import sys
import pygame
from src.main_game import Game

# Initializes the game
if __name__ == "__main__":

    game_exe = Game()

    game_exe.icon_path = "icon.png"
    game_exe.screen = pygame.display.set_mode((game_exe.screen_size))

    game_exe.mainLoop()
    