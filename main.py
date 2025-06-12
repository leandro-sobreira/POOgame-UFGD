"""Esse é o módulo principal, ele será executado para exibir o jogo.
"""

# Importe as bibliotecas necessárias
import sys
sys.path.insert(0, "./src")

from main_game import Game #arquivo principal do fluxo do jogo


# Start the game
Game()

"""from games.uno import UnoGame
game = UnoGame('Lepanto')
print(game.play())"""
