# Import necessary libraries
import pygame
import os
import sys

# CORREÇÃO: Use importações relativas para módulos no mesmo pacote (src)
from . import setup as st
from . import interface as it
from . import database_manager as db
from .games import blackjack

def Game():
    """
    Main function that manages the game flow and transitions between screens.
    """
    # Pygame Initialization
    pygame.init()
    pygame.mixer.init()

    # Screen and window settings
    screen_size = (st.SCREEN_WIDTH, st.SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("CardGame HUB")
    icon_path = os.path.join(st.img_folder, "icon.png")
    pygame.display.set_icon(pygame.image.load(icon_path))

    # Game control variables
    current_player_data = None
    running = True

    # Screen Manager
    # The first screen is now for entering the player's name.
    current_screen = it.PlayerNameScreen(screen)

    while running:
        # Each screen's loop method now returns the key for the next screen to be displayed,
        # or None/QUIT to exit the game.
        next_screen_key = current_screen.loop()

        if next_screen_key == "QUIT":
            running = False
        
        elif next_screen_key == "GET_PLAYER":
            player_name = current_screen.player_name
            if not player_name:  # If the name is empty, use a default
                player_name = "Player 1"
            current_player_data = db.get_player(player_name)
            current_screen = it.MenuScreen(screen, current_player_data)

        elif next_screen_key == "MENU":
            current_screen = it.MenuScreen(screen, current_player_data)

        elif next_screen_key == "GAME_SELECT":
            current_screen = it.GameSelectScreen(screen, current_player_data)
        
        elif next_screen_key == "ERASE_DATA":
            db.erase_data()
            # Shows a confirmation screen before returning to the menu
            current_screen = it.NotificationScreen(screen, "Player data erased!", "MENU", current_player_data)

        elif next_screen_key == "BLACKJACK":
            # 1. Instantiate the game (Model)
            blackjack_instance = blackjack.BlackjackGame(current_player_data)
            # 2. Instantiate the game screen (View) and pass the model to it
            current_screen = it.BlackjackScreen(screen, blackjack_instance)
        
        elif next_screen_key == "UPDATE_PLAYER_DATA":
            # The game screen (e.g., BlackjackScreen) returns the updated data
            updated_data = current_screen.get_player_data()
            if updated_data:
                db.update_player(updated_data)
            # Reload data to reflect changes immediately
            current_player_data = db.get_player(updated_data["name"]) 
            current_screen = it.MenuScreen(screen, current_player_data)
            
        else: # Fallback for unknown screen keys or unimplemented features
            message = f"Feature '{next_screen_key}' not implemented yet!"
            current_screen = it.NotificationScreen(screen, message, "MENU", current_player_data)

    # Quit Pygame
    pygame.quit()
    sys.exit()