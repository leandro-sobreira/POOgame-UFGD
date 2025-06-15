# Import necessary libraries
import pygame
import os
import sys

from .games import blackjack_game as blackjack
from .games import uno_game as uno

from . import setup as st
from . import interface as it
from . import database_manager as db

class Game():
    """
    The Game class is intended to be the main class used to initialize the game as a whole.

    Atributos
    ---------
    Privados:
        current_player_data : dict{key: str, key: int}
        running : bool
        screen_size : tuple(int, int)
        screen : pygame.Surface
        icon_path : str

    Métodos
    -------
    current_player_data():
        Getter de current_player_data
    running():
        Getter de running
    screen_size():
        Getter de screen_size
    screen():
        Getter de screen
    icon_path():
        Getter de icon_path
    current_player_data():
        Setter de current_player_data
    running():
        Setter de running
    screen_size():
        Setter de screen_size
    screen():
        Setter de screen
    icon_path():
        Setter de icon_path
    mainLoop():
        Realiza a execução do looping principal do jogo e também a finalização da execução
    """
    def __init__(self):
        """
        Constructor of the Game class, responsible for initializing the attributes of a Game object.     
        """
        # Pygame Initialization
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("CardGame HUB")

        self.__player_name = "Player"
        self.__running = True
        self.__screen_size = (st.SCREEN_WIDTH, st.SCREEN_HEIGHT)
        self.__screen = None
        self.__icon_path = None

    @property
    def running(self):
        """
        Getter de running

        Returns:
            bool: valor booleano atual sendo utilizado como running para definir estados do jogo
        """
        return self.__running
    
    @property
    def screen_size(self):
        """
        Getter de screen_size

        Returns:
            tuple(int, int): tupla de inteiros atual sendo utilizada para definir o tamanho da tela utilizada
        """
        return self.__screen_size
    
    @property
    def screen(self):
        """
        Getter de screen

        Returns:
            pygame.Surface: objeto pygame.Surface atual sendo utilizado como tela a ser renderizada
        """
        return self.__screen

    @property
    def icon_path(self):
        """
        Getter de icon_path

        Returns:
            str: string atual sendo utilizada como path do arquivo de icon a ser renderizado
        """
        return self.__icon_path
    
    @running.setter
    def running(self, running):
        """
        Setter de running

        Argumentos:
            running (bool): valor booleano a ser utilizado como running para definir estados do jogo
        """
        self.__runnning = running
    
    @screen_size.setter
    def screen_size(self, screen_size):
        """
        Setter de screen_size

        Argumentos:
            screen_size (tuple(int, int)): tupla de inteiros a ser utilizada para definir o tamanho da tela utilizada
        """
        self.__screen_size = screen_size

    @screen.setter
    def screen(self, screen):
        """
        Setter de screen

        Argumentos:
            screen (pygame.Surface): objeto pygame.Surface a ser utilizado como tela a ser renderizada
        """
        self.__screen = screen

    @icon_path.setter
    def icon_path(self, icon_path):
        """
        Setter de icon_path

        Argumentos:
            icon_path (str): string a ser utilizada como path do arquivo de icon a ser renderizado
        """

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
        Main method responsible for initializing the game and also ending it according to the flow.
        """
        # Screen Manager
        # The first screen is now for entering the player's name.
        current_screen = it.PlayerNameScreen(self.__screen)

        if current_screen == None:
            raise Exception("No screen has been configured for rendering!")
        
        while self.__running:
            # Each screen's loop method now returns the key for the next screen to be displayed,
            # or None/QUIT to exit the game.
            next_screen_key = current_screen.loop()

            if next_screen_key == "QUIT":
                self.__running = False
            
            elif next_screen_key == "GET_PLAYER":
                player_name = current_screen.player_name
                if not player_name:
                    player_name = "Player 1"
                # Just stores the name, without calling the database
                self.__player_name = player_name 
                current_screen = it.MenuScreen(self.__screen, self.__player_name)

            elif next_screen_key == "MENU":
                current_screen = it.MenuScreen(self.__screen, self.__player_name)

            elif next_screen_key == "GAME_SELECT":
                current_screen = it.GameSelectScreen(self.__screen, self.__player_name)

            elif next_screen_key == "SCORES":
                # The scores screen now loads data directly from the DB
                current_screen = it.ScoresScreen(self.__screen) 
            
            elif next_screen_key == "ERASE_DATA":
                db.erase_data()
                current_screen = it.NotificationScreen(self.__screen, "Player data erased!", "MENU", self.__player_name)

            elif next_screen_key == "BLACKJACK":
                # Instantiates the game passing only the name
                blackjack_instance = blackjack.BlackjackGame(self.__player_name)
                current_screen = it.BlackjackScreen(self.__screen, blackjack_instance)

            elif next_screen_key == "UNO":
                # Assuming UnoGame is adjusted to take player_name
                uno_instance = uno.UnoGame(self.__player_name) 
                current_screen = it.UnoScreen(self.__screen, uno_instance)
            
            # NEW STATE TO LOG WINS
            elif isinstance(next_screen_key, tuple) and next_screen_key[0] == "LOG_WIN":
                # The screen will return a tuple: ("LOG_WIN", score, game_name)
                _, final_score, game_name = next_screen_key
                db.log_win(self.__player_name, final_score, game_name)
                
                message = "Win registered!"
                current_screen = it.NotificationScreen(self.__screen, message, "MENU") # No player data needed here

            else: # Fallback for unknown screen keys or unimplemented features
                message = f"Feature '{next_screen_key}' not implemented yet!"
                current_screen = it.NotificationScreen(self.__screen, message, "MENU")

        # Quit Pygame
        pygame.quit()
        sys.exit()
