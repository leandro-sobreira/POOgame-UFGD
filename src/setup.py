import os
import pygame

"""
File containing the global variables for the game.
"""

# Define paths for necessary folders
source_folder = os.path.dirname(__file__) #
img_folder = os.path.join(source_folder, "img") #
sound_folder = os.path.join(source_folder, "sounds") #
font_folder = os.path.join(source_folder, "fonts") #

# CORRECTED: Removed pygame.init() and pygame.mixer.init()
# Initialization should happen once in the main entry point.

FPS = 30 #
SCALE = 1 #
SCREEN_HEIGHT = 480 * SCALE #
SCREEN_WIDTH = 854 * SCALE #

# Define colors 
RED = (255, 0, 0) #
GREEN = (20, 255, 140) #
BLUE = (100, 100, 255) #
GREY = (210, 210 ,210) #
WHITE = (255, 255, 255) #
BLACK = (0, 0, 0) #
MAGENTA = (194,9,84) #

# Font and UI sizes
button_size = 30 * SCALE #
title_size = 50 * SCALE #

# Font path
button_font = os.path.join(font_folder, "Segoe Script Bold.ttf") #

# Global clock
clock = pygame.time.Clock() #