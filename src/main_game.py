# Importe as bibliotecas necessárias
import json
import math
import os
import pygame
import random
import sys
import setup as st
import interface as it
import database_manager as db # <--- ADD THIS LINE

from games import blackjack, game_intro, uno

#Inicialização do Pygame
pygame.init()

# Crie o nome do jogo (exibido no superior da janela)
pygame.display.set_caption("Cassino Online UFGD")
pygame.display.set_icon(pygame.image.load(os.path.join(st.img_folder, "icon.png")))# Define o ícone da janela com uma imagem (com transparência)

# Relógio para controlar o tempo das ações no jogo
clock = pygame.time.Clock()

#Pré-configura o mixer de áudio
pygame.mixer.pre_init(44100, -16, 1, 512)# 44100 Hz de frequência, 16 bits (signed), mono, buffer de 512 bytes
pygame.mixer.init()# Inicializa o mixer de áudio com os parâmetros acima

#DISPLAY – define a resolução da janela, titulo e icone
screen_size = (st.SCREEN_WIDTH, st.SCREEN_HEIGHT)  # Largura x Altura da janela
screen = pygame.display.set_mode(screen_size)  # Cria a janela com esse tamanho

def Game():
    game_over = False

    intro_screen = it.IntroScreen(screen, "CARD GAME", os.path.join(st.font_folder, "Ghost Shadow.ttf"), 64, 1)

    # The intro loop now returns the selected game (e.g., 3 for Blackjack)
    intro_screen.loop()
    selected_game = intro_screen.selected_game

    print("Game selected:", selected_game)

    # --- Player and Game Session Logic ---
    curret_player_data = None

    # Proceed only if a game was chosen (not quit)
    if selected_game and selected_game > 0:
        # Step 1: Get player name. For now, we use a fixed name.
        # Later, we can create a Pygame screen to ask for the player's name.
        player_name = "Lepanto"
        curret_player_data = db.get_player(player_name)
        
        print(f"Welcome, {curret_player_data['name']}!")
        print(f"Your blackjack points: {curret_player_data['blackjack_points']}")
        print(f"Your UNO wins: {curret_player_data['uno_wins']}")

    # -- Game Launch Logic --
    if selected_game == 3: # Blackjack
        """ This is where the integration between logic and UI happens.
        The BlackjackScreen needs to be modified to run the game logic instead of its own loop.

        PSEUDO-CODE FOR MY DUMBASS TEAMMATES, or for future integrations:
        blackjack_instance = blackjack.BlackjackGame(current_player_data)
        blackjack_instance.play_graphical(screen) # A new method in our game class
        current_player_data = blackjack_instance.get_player_data() # Get updated data

        And for now we just call our existing screen
        """
        it.BlackjackScreem(screen).loop()

        """ The uno game is currently not connected to the menu, but here's how Marcos ou Abner could do it:
        elif selected_game == 4: # Assuming 4 is for Uno
        uno_game = uno.UnoGame(['Lepanto', 'Bot1', 'Bot2', 'Bot3'])
        winner_name = uno_game.play()
        if winner_name == current_player_data['name']:
            current_player_data['uno_wins'] += 1
        """

    # --- Save Data After Game ---
    if curret_player_data:
        # This is where the score should be updated after a game ends.
        # Example: current_player_data['blackjack_points'] = final_score_from_game
        db.update_player(curret_player_data)
    
    # The rest of the shitty cleaning code:
    pygame.mouse.set_visible(True)
    pygame.mixer.music.fadeout(1000)
    pygame.time.delay(1000)

    pygame.quit()