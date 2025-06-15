import os
import pygame

"""
File containing the global variables for the game.
"""

# Define paths for necessary folders
source_folder = os.path.dirname(__file__) #
assets_folder = os.path.join(source_folder, '../assets') #
img_folder = os.path.join(assets_folder, "img") #
sound_folder = os.path.join(assets_folder, "sounds") #
font_folder = os.path.join(assets_folder, "fonts") #

# CORRECTED: Removed pygame.init() and pygame.mixer.init()
# Initialization should happen once in the main entry point.

FPS = 30 #
SCALE = 1 #
SCREEN_HEIGHT = 720 * SCALE #
SCREEN_WIDTH = 1280 * SCALE #

STANDARD_CARD_WIDTH = 140 * SCALE #
STANDARD_CARD_HEIGHT = 190 * SCALE #

UNO_CARD_WIDTH = 85 * SCALE #
UNO_CARD_HEIGHT = 140 * SCALE #

# Define colors 
RED = (255, 0, 0) #
GREEN = (20, 255, 140) #
YELLOW = (255, 255, 0) #
BLUE = (100, 100, 255) #
GREY = (210, 210 ,210) #
WHITE = (255, 255, 255) #
BLACK = (0, 0, 0) #
MAGENTA = (194,9,84) #

# Font and UI sizes
button_size = 30 * SCALE #
title_size = 50 * SCALE #

# Font path
title_font = os.path.join(font_folder, "Ghost Shadow.ttf") #
text_font = os.path.join(font_folder, "Typori.ttf") #
button_font = os.path.join(font_folder, "Segoe Script Bold.ttf") #

# Global clock
clock = pygame.time.Clock() #