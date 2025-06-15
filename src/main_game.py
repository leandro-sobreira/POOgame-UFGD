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
    Classe Game feita para ser a classe principal a ser utilizada para a inicialização do jogo como um todo

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
        Construtor da classe Game responsável por inicializar os atributos de um objeto Game        
        """
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
        """
        Getter de current_player_data

        Returns:
            dict{key: str, key: str}: dicionário atual sendo utilizado para representar os dados de um jogador, sendo
                                      o nome e a pontuação atual as informações armazenadas no dict
        """
        return self.__current_player_data
    
    @property
    def running(self):
        """
        Getter de running

        Returns:
            bool: valor booleano atual sendo utilizado como running para definir estados do jogo
        """
        return self.__runnning
    
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

    @current_player_data.setter
    def current_player_data(self, player_data):
        """
        Setter de current_player_data

        Argumentos:
            player_data (dict{key: str, key: str}): dicionário a ser utilizado para representar os dados de um jogador, sendo
                                      o nome e a pontuação atual as informações armazenadas no dict
        """
        self.__current_player_data = player_data
    
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
        Método principal responsável por inicializar o jogo e também encerrá-lo conforme fluxo decidido
        pela equipe
        """
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
                self.__current_player_data = db.get_player(player_name)
                current_screen = it.MenuScreen(self.__screen, self.__current_player_data)

            elif next_screen_key == "MENU":
                current_screen = it.MenuScreen(self.__screen, self.__current_player_data)

            elif next_screen_key == "GAME_SELECT":
                current_screen = it.GameSelectScreen(self.__screen, self.__current_player_data)
            
            elif next_screen_key == "ERASE_DATA":
                db.erase_data()
                # Shows a confirmation screen before returning to the menu
                current_screen = it.NotificationScreen(self.__screen, "Player data erased!", "MENU", self.__current_player_data)

            elif next_screen_key == "BLACKJACK":
            #while True
                

                """current_screen = it.BetAmountScreen(screen:screen)
                amount = it.BetAmountScreen.getAmount()"""
                #bet_screen = it.BetAmountScreen(screen)
                #bet_amount = bet_screen.loop()

                # 1. Instantiate the game (Model)
                blackjack_instance = blackjack.BlackjackGame(self.__current_player_data)
                
                # 2. Instantiate the game screen (View) and pass the model to it
                current_screen = it.BlackjackScreen(self.__screen, blackjack_instance)
                

            elif next_screen_key == "UNO":
                uno_instance = uno.UnoGame(self.__current_player_data)
                current_screen = it.UnoScreen(self.__screen, uno_instance)
            
            elif next_screen_key == "UPDATE_PLAYER_DATA":
                # The game screen (e.g., BlackjackScreen) returns the updated data
                updated_data = current_screen.get_player_data()
                if updated_data:
                    db.update_player(updated_data)
                # Reload data to reflect changes immediately
                current_player_data = db.get_player(updated_data["name"]) 
                current_screen = it.MenuScreen(self.__screen, self.__current_player_data)
                
            else: # Fallback for unknown screen keys or unimplemented features
                message = f"Feature '{next_screen_key}' not implemented yet!"
                current_screen = it.NotificationScreen(self.__screen, message, "MENU", self.__current_player_data)

        # Quit Pygame
        pygame.quit()
        sys.exit()
