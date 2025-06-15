# Import necessary libraries
import pygame
import os
import sys

from .games import blackjack, uno

from . import setup as st
from . import interface as it
from . import database_manager as db

class Game():
    """
    Main Class that manages the game flow and transitions between screens.
    """

    def __init__(self):
        # Pygame Initialization
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("CardGame HUB")

        self.__current_player_data = None
        self.__running = True
        self.__screen_size = (st.SCREEN_WIDTH, st.SCREEN_HEIGHT)
        self.__screen = None
        self.__icon_path = None

    @property
    def current_player_data(self):
        return self.__current_player_data
    
    @property
    def running(self):
        return self.__runnning
    
    @property
    def screen_size(self):
        return self.__screen_size
    
    @property
    def screen(self):
        return self.__screen

    @property
    def icon_path(self):
        return self.__icon_path

    @current_player_data.setter
    def current_player_data(self, player_data):
        self.__current_player_data = player_data
    
    @running.setter
    def running(self, running):
        self.__runnning = running
    
    @screen_size.setter
    def screen_size(self, screen_size):
        self.__screen_size = screen_size

    @screen.setter
    def screen(self, screen):
        self.__screen = screen

    @icon_path.setter
    def icon_path(self, icon_path):
        old_path = self.__icon_path
        new_path = icon_path

        try:
            pygame.display.set_icon(pygame.image.load(os.path.join(st.img_folder, new_path)))
        except FileNotFoundError:
            self.__icon_path = old_path
        else:
            pygame.display.set_icon(pygame.image.load(os.path.join(st.img_folder, new_path)))
            self.__icon_path = new_path
    
    def mainLoop(self):
        # Screen Manager
        # The first screen is now for entering the player's name.
        current_screen = it.PlayerNameScreen(self.__screen)

        if current_screen == None:
            raise Exception("Não foi configurado tela para renderização!")
        
        while self.__running:
            # Each screen's loop method now returns the key for the next screen to be displayed,
            # or None/QUIT to exit the game.
            next_screen_key = current_screen.loop()

            if next_screen_key == "QUIT":
                self.__running = False
            
            elif next_screen_key == "GET_PLAYER":
                player_name = current_screen.player_name
                if not player_name:  # If the name is empty, use a default
                    player_name = "Player 1"
                current_player_data = db.get_player(player_name)
                current_screen = it.MenuScreen(self.__screen, current_player_data)

            elif next_screen_key == "MENU":
                current_screen = it.MenuScreen(self.__screen, current_player_data)

            elif next_screen_key == "GAME_SELECT":
                current_screen = it.GameSelectScreen(self.__screen, current_player_data)
            
            elif next_screen_key == "ERASE_DATA":
                db.erase_data()
                # Shows a confirmation screen before returning to the menu
                current_screen = it.NotificationScreen(self.__screen, "Player data erased!", "MENU", current_player_data)

            elif next_screen_key == "BLACKJACK":
            #while True
                

                """current_screen = it.BetAmountScreen(screen:screen)
                amount = it.BetAmountScreen.getAmount()"""
                #bet_screen = it.BetAmountScreen(screen)
                #bet_amount = bet_screen.loop()

                # 1. Instantiate the game (Model)
                blackjack_instance = blackjack.BlackjackGame(current_player_data)
                
                # 2. Instantiate the game screen (View) and pass the model to it
                current_screen = it.BlackjackScreen(self.__screen, blackjack_instance)
                

            elif next_screen_key == "UNO":
                uno_instance = uno.UnoGame(current_player_data)
                current_screen = it.UnoScreen(self.__screen, uno_instance)
            
            elif next_screen_key == "UPDATE_PLAYER_DATA":
                # The game screen (e.g., BlackjackScreen) returns the updated data
                updated_data = current_screen.get_player_data()
                if updated_data:
                    db.update_player(updated_data)
                # Reload data to reflect changes immediately
                current_player_data = db.get_player(updated_data["name"]) 
                current_screen = it.MenuScreen(self.__screen, current_player_data)
                
            else: # Fallback for unknown screen keys or unimplemented features
                message = f"Feature '{next_screen_key}' not implemented yet!"
                current_screen = it.NotificationScreen(self.__screen, message, "MENU", current_player_data)

        # Quit Pygame
        pygame.quit()
        sys.exit()
