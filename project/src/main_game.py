import pygame
import os
import sys

from .games import blackjack_game as blackjack
from .games import uno_game as uno

from . import setup as st
from . import interface as it
# Import the new class instead of the old module alias
from .database_manager import ScoreRepository

class Game():
    """
    Main Game class, serves as the Controller to initialize and manage game flow.
    """
    def __init__(self):
        """
        Game constructor. Initializes Pygame and the persistence repository.
        """
        # Pygame Initialization
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("CardGame HUB")

        # Instantiate the repository here
        self.score_repository = ScoreRepository()

        self.__player_name = "Player"
        self.__running = True
        self.__screen_size = (st.SCREEN_WIDTH, st.SCREEN_HEIGHT)
        self.__screen = None
        self.__icon_path = None

    @property
    def player_name(self):
        return self.__player_name

    @property
    def running(self):
        return self.__running
    
    @property
    def screen_size(self):
        return self.__screen_size
    
    @property
    def screen(self):
        return self.__screen

    @property
    def icon_path(self):
        return self.__icon_path
    
    @player_name.setter
    def player_name(self, player_name):
        self.__player_name = player_name

    @running.setter
    def running(self, running):
        self.__running = running
    
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
        """
        Main method responsible for running the game loop and handling screen transitions.
        """
        current_screen = it.PlayerNameScreen(self.__screen)

        if current_screen is None:
            raise Exception("No screen has been configured for rendering!")
        
        while self.__running:
            next_screen_key = current_screen.loop()

            if next_screen_key == "QUIT":
                self.__running = False
            
            elif next_screen_key == "GET_PLAYER":
                player_name = current_screen.player_name
                if not player_name:
                    player_name = "Player 1"
                self.__player_name = player_name 
                current_screen = it.MenuScreen(self.__screen, self.__player_name)

            elif next_screen_key == "MENU":
                current_screen = it.MenuScreen(self.__screen, self.__player_name)

            elif next_screen_key == "GAME_SELECT":
                current_screen = it.GameSelectScreen(self.__screen, self.__player_name)

            elif next_screen_key == "SCORES":
                # The Controller now fetches the data and passes it to the View (ScoresScreen)
                all_scores = self.score_repository.get_all_scores()
                current_screen = it.ScoresScreen(self.__screen, all_scores) 
            
            elif next_screen_key == "ERASE_DATA":
                # The erase logic is now called through the repository object
                self.score_repository.clear_all()
                current_screen = it.NotificationScreen(self.__screen, "Player data erased!", "MENU", self.__player_name)

            elif next_screen_key == "BLACKJACK":
                blackjack_instance = blackjack.BlackjackGame(self.__player_name)
                current_screen = it.BlackjackScreen(self.__screen, blackjack_instance)

            elif next_screen_key == "UNO":
                uno_instance = uno.UnoGame(self.__player_name) 
                current_screen = it.UnoScreen(self.__screen, uno_instance)
            
            # MODIFIED LOG_WIN logic
            elif isinstance(next_screen_key, tuple) and next_screen_key[0] == "LOG_WIN":
                _, final_score, game_name = next_screen_key
                
                # The controller uses the repository's method to add the score
                self.score_repository.add_score(self.__player_name, final_score, game_name)
                
                message = "Win registered!"
                current_screen = it.NotificationScreen(self.__screen, message, "MENU")

            else: # Fallback for unknown screen keys or unimplemented features
                message = f"Feature '{next_screen_key}' not implemented yet!"
                current_screen = it.NotificationScreen(self.__screen, message, "MENU")

        # Quit Pygame
        pygame.quit()
        sys.exit()