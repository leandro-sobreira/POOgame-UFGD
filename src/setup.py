import os
"""Arquivo contendo as variáveis globais do jogo
"""

#Importe a biblioteca necessária
import pygame

# Defina os caminhos para as pastas necessárias
source_folder = os.path.dirname(__file__)
img_folder = os.path.join(source_folder, "img")
sound_folder = os.path.join(source_folder, "sounds")
font_folder = os.path.join(source_folder, "fonts")

#TODO: arquivos antigos e pasta cards

# Inicializando o pygame e o mixer de sons
pygame.init()
pygame.mixer.init()

FPS = 30

"""
TODO: Observar possibilidade de tela full 
# Dimensões da tela
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h
"""

SCALE = 1
SCREEN_HEIGHT = 480 * SCALE
SCREEN_WIDTH = 854 * SCALE

# Define cores 
RED = (255, 0, 0)
GREEN = (20, 255, 140)
BLUE = (100, 100, 255)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (194,9,84)


button_size = 25 * SCALE
title_size = 50 * SCALE

button_font = os.path.join(font_folder, "Segoe Script Bold.ttf")

clock = pygame.time.Clock()