import pygame
import os
from . import setup as st

from abc import ABC, abstractmethod

# --- ABSTRACT SCREEN CLASS (BASE FOR ALL SCREENS) ---

class Screen(ABC): #
    """
    An abstract base class for all game screens.
    Ensures that every screen has a consistent structure and behavior.
    """ #
    def __init__(self, screen, player_data=None): #
        self.screen = screen #
        self.player_data = player_data #
        self.next_screen = None #
        self._background = None #

        # Load common sounds #
        
        
        #self.select_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "computer-processing-sound-effects-short-click-select-02-122133.ogg")) 
        #self.ok_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "computer-processing-sound-effects-short-click-select-01-122134.ogg"))
        #self.select_sound.set_volume(0.2)
        #self.ok_sound.set_volume(0.2)
        #self.reset_sound.set_volume(0.2)
        
        self.select_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "short-click-select_02.ogg")) #
        self.ok_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "short-click-select_01.ogg")) #
        self.reset_sound = pygame.mixer.Sound(os.path.join(st.sound_folder, "reset.ogg")) #

    def set_background(self, image_path): #
        """Sets and scales the background image.""" #
        background = pygame.image.load(image_path).convert() #
        self._background = pygame.transform.scale(background, self.screen.get_size()) #

    def set_music(self, music_path, volume=0.2): #
        """Loads and plays background music in a loop.""" #
        pygame.mixer.music.load(music_path) #
        pygame.mixer.music.set_volume(volume) #
        pygame.mixer.music.play(-1) #

    def draw_text_with_outline(self, surface, text, font, pos, text_color, outline_color, outline_width=2): #
        """Renders text with a simple outline.""" #
        x, y = pos #
        # Render outline #
        for dx in range(-outline_width, outline_width + 1): #
            for dy in range(-outline_width, outline_width + 1): #
                if dx != 0 or dy != 0: #
                    outline_surf = font.render(text, True, outline_color) #
                    surface.blit(outline_surf, (x - outline_surf.get_width() // 2 + dx, y - outline_surf.get_height() // 2 + dy)) #
        # Render main text #
        text_surf = font.render(text, True, text_color) #
        surface.blit(text_surf, (x - text_surf.get_width() // 2, y - text_surf.get_height() // 2)) #


    @abstractmethod
    def handle_event(self, event): #
        """Abstract method to handle screen-specific events.""" #
        pass #

    @abstractmethod
    def draw(self): #
        """Abstract method to draw the screen's elements.""" #
        pass #

    def loop(self): #
        """
        The main loop for a screen. It handles events, updates, and drawing.
        Returns the key for the next screen to be displayed.
        """ #
        is_running = True #
        while is_running: #
            st.clock.tick(st.FPS) #

            for event in pygame.event.get(): #
                if event.type == pygame.QUIT: #
                    self.next_screen = "QUIT" #
                # Pass the event to the specific handler of the child screen #
                self.handle_event(event) #

            self.draw() #
            pygame.display.flip() #
            
            if self.next_screen: #
                is_running = False #
        
        return self.next_screen #

# --- SCREEN IMPLEMENTATIONS ---

"""
class BetAmountScreen(Screen):
    def __init__(self, screen, prompt_text="Digite o valor da aposta:"):
        super().__init__(screen)
        self.prompt_text = prompt_text
        self.input_value = ''
        self.amount = 0
        self.font = pygame.font.Font(st.text_font, 32)
        self.done = False
        self.__box_width = 400
        self.__box_height = 150

        self.__box_rect = pygame.Rect((st.SCREEN_WIDTH - self.__box_width) // 2,(st.SCREEN_HEIGHT - self.__box_height) // 2,self.__box_width, self.__box_height )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                self.next_screen = "BLACKJACK"
            elif event.key == pygame.K_BACKSPACE:
                self.input_value = self.input_value[:-1]
            elif event.unicode.isdigit():
                self.input_value += event.unicode

    def getAmount(self):
        return self.amount

    def draw(self):
        #self.screen.fill(st.BLACK)  # Limpa a tela com fundo preto
        pygame.draw.rect(self.screen, st.BLACK, self.__box_rect)  # fundo da caixa
        pygame.draw.rect(self.screen, st.WHITE, self.__box_rect, 2)  # borda branca

        # Renderiza o texto do prompt
        prompt_surface = self.font.render(self.prompt_text, True, st.WHITE)
        prompt_rect = prompt_surface.get_rect(center=(st.SCREEN_WIDTH / 2, st.SCREEN_HEIGHT / 2 - 40))
        self.screen.blit(prompt_surface, prompt_rect)

        # Renderiza o valor digitado
        input_surface = self.font.render(self.input_value, True, st.GREEN)
        input_rect = input_surface.get_rect(center=(st.SCREEN_WIDTH / 2, st.SCREEN_HEIGHT / 2 + 10))
        self.screen.blit(input_surface, input_rect)

    def loop(self):
        while not self.done:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            pygame.display.flip()
        return int(self.input_value) if self.input_value else 0
"""


class PlayerNameScreen(Screen): #
    def __init__(self, screen, prompt_text="Enter Your Name and Press Enter"): #
        super().__init__(screen) #
        self.set_background(os.path.join(st.img_folder, "title.png")) #
        self.font = pygame.font.Font(st.text_font, 32) #
        self.input_font = pygame.font.Font(st.text_font, 28) #
        self.player_name = "" #
        self.prompt_text = prompt_text #

    def handle_event(self, event): #
        if event.type == pygame.KEYDOWN: #
            if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]: #
                self.ok_sound.play() #
                self.next_screen = "GET_PLAYER" #
            elif event.key == pygame.K_BACKSPACE: #
                self.player_name = self.player_name[:-1] #
            else:
                if event.unicode.isprintable() and len(self.player_name) < 15: # Limit name length #
                    self.player_name += event.unicode #
    
    def draw(self): #
        self.screen.blit(self._background, (0, 0)) #
        self.draw_text_with_outline(self.screen, self.prompt_text, self.font, (st.SCREEN_WIDTH / 2, st.SCREEN_HEIGHT / 2 - 50), st.WHITE, st.BLACK) #
        
        input_rect = pygame.Rect(st.SCREEN_WIDTH / 2 - 150, st.SCREEN_HEIGHT / 2, 300, 50) #
        pygame.draw.rect(self.screen, st.WHITE, input_rect, 2) #
        input_surface = self.input_font.render(self.player_name, True, st.WHITE) #
        self.screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10)) #

class MenuScreen(Screen): #
    def __init__(self, screen, player_data): #
        super().__init__(screen, player_data) #
        self.set_background(os.path.join(st.img_folder, "title.png")) #
        self.set_music(os.path.join(st.sound_folder, "1197551_Butterflies.ogg")) #
        self.title_font = pygame.font.Font(os.path.join(st.font_folder, st.title_font), st.title_size) #
        
        self.buttons = [ #
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 200), "Start", "GAME_SELECT"), #
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 150), "Erase Data", "ERASE_DATA"), #
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 100), "Config", "CONFIG"), #
            Button((st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT - 50), "Quit", "QUIT") #
        ]
        self.selected_index = 0 #
        self.all_sprites = pygame.sprite.Group(self.buttons) #

    def handle_event(self, event): #
        if event.type == pygame.KEYDOWN: #
            if event.key in (pygame.K_UP, pygame.K_w): #
                self.select_sound.play() #
                self.selected_index = (self.selected_index - 1) % len(self.buttons) #
            elif event.key in (pygame.K_DOWN, pygame.K_s): #
                self.select_sound.play() #
                self.selected_index = (self.selected_index + 1) % len(self.buttons) #
            elif event.key in (pygame.K_z, pygame.K_RETURN): #
                selected_button = self.buttons[self.selected_index] #
                if selected_button.action == "ERASE_DATA": #
                    self.reset_sound.play() #
                else:
                    self.ok_sound.play() #
                self.next_screen = selected_button.action #

    def draw(self): #
        self.screen.blit(self._background, (0, 0)) #
        self.draw_text_with_outline(self.screen, "CARD GAME", self.title_font, (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/4), st.BLACK, st.WHITE) #
        
        welcome_text = f"Welcome, {self.player_data['name']}! Points: {self.player_data['blackjack_points']}" #
        self.draw_text_with_outline(self.screen, welcome_text, pygame.font.Font(st.button_font, 22), (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2), st.WHITE, st.BLACK) #

        for i, button in enumerate(self.buttons): #
            button.set_selected(i == self.selected_index) #
        self.all_sprites.update() #
        self.all_sprites.draw(self.screen) #

class GameSelectScreen(Screen): #
    def __init__(self, screen, player_data): #
        super().__init__(screen, player_data) #
        self.set_background(os.path.join(st.img_folder, "games/blackjack/mesa.png")) #
        self.title_font = pygame.font.Font(st.button_font, st.title_size) #

        self.buttons = [ #
            Button((st.SCREEN_WIDTH/2, 200), "Blackjack", "BLACKJACK"), #
            Button((st.SCREEN_WIDTH/2, 250), "UNO", "UNO"), #
            Button((st.SCREEN_WIDTH/2, 350), "Back to Menu", "MENU") #
        ]
        self.selected_index = 0 #
        self.all_sprites = pygame.sprite.Group(self.buttons) #

    def handle_event(self, event): #
        if event.type == pygame.KEYDOWN: #
            if event.key in (pygame.K_UP, pygame.K_w): #
                self.select_sound.play() #
                self.selected_index = (self.selected_index - 1) % len(self.buttons) #
            elif event.key in (pygame.K_DOWN, pygame.K_s): #
                self.select_sound.play() #
                self.selected_index = (self.selected_index + 1) % len(self.buttons) #
            elif event.key in (pygame.K_z, pygame.K_RETURN): #
                self.ok_sound.play() #
                self.next_screen = self.buttons[self.selected_index].action #
    
    def draw(self): #
        self.screen.blit(self._background, (0, 0)) #
        self.draw_text_with_outline(self.screen, "Select a Game", self.title_font, (st.SCREEN_WIDTH/2, 80), st.WHITE, st.BLACK) #
        for i, button in enumerate(self.buttons): #
            button.set_selected(i == self.selected_index) #
        self.all_sprites.update() #
        self.all_sprites.draw(self.screen) #

class BlackjackScreen(Screen): #
    """The View for the Blackjack game. It only draws what the Model tells it to.""" #
    def __init__(self, screen, game_instance): #
        super().__init__(screen) #
        self.game = game_instance  # This is the Model #
        self.set_background(os.path.join(st.img_folder, "games/blackjack/mesa.png")) #
        self.font = pygame.font.Font(st.text_font, 24) #
        self.card_sprites = pygame.sprite.Group() #
        self.load_card_images() #
        self.prompt_text = "Digite o valor da aposta:"
        self.input_value = ''
        self.amount = 0
        self.font = pygame.font.Font(st.text_font, 32)
        self.done = False
        self.__box_width = 400
        self.__box_height = 150

        self.__box_rect = pygame.Rect((st.SCREEN_WIDTH - self.__box_width) // 2,(st.SCREEN_HEIGHT - self.__box_height) // 2,self.__box_width, self.__box_height )

    def load_card_images(self): #
        """Pre-loads all card images into a dictionary for quick access.""" #
        self.card_images = {} #
        cards_path = os.path.join(st.img_folder, "games/blackjack/cards") #
        for filename in os.listdir(cards_path): #
            if filename.endswith(".png"): #
                key = filename.replace(".png", "") # e.g., "king_of_spade" #
                image = pygame.image.load(os.path.join(cards_path, filename)).convert_alpha() #
                self.card_images[key] = pygame.transform.scale(image, (70 * st.SCALE, 98 * st.SCALE)) #

    def handle_event(self, event): #

        if self.game.state == "BET":
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER] and self.input_value != '':
                    self.amount = int(self.input_value)
                    self.game.bet_amount = self.amount
                    self.game.state = "PLAYER_TURN"
                elif event.key == pygame.K_BACKSPACE:
                    self.input_value = self.input_value[:-1]
                elif event.unicode.isdigit():
                    self.input_value += event.unicode
                    
            self.game.setBetAmount()

        elif self.game.state == "PLAYER_TURN": #
            if event.type == pygame.KEYDOWN: #
                if event.key in (pygame.K_z, pygame.K_h): # 'Z' or 'H' to Hit #
                    self.ok_sound.play() #
                    self.game.player_hit() #
                elif event.key in (pygame.K_x, pygame.K_s): # 'X' or 'S' to Stand #
                    self.ok_sound.play() #
                    self.game.player_stand() #

                '''
                    self.game._dealer_play()
                    while self.game._dealer_play



                '''

            """elif self.game.state == "DEALER_TURN":
                self.game._dealer_buy_loop()"""
        
        elif self.game.state == "ROUND_OVER": #
            if event.type == pygame.KEYDOWN: #
                if event.key in (pygame.K_z, pygame.K_RETURN): #
                    # Decide whether to start a new round or exit #
                    if self.game.player.getPoints() >= 10: #
                        self.game.setBetAmount() # Play again #
                    else:
                        self.next_screen = "UPDATE_PLAYER_DATA" # Not enough points, exit to menu #
    
    def sync_sprites_with_model(self): #
        """Updates the card sprites on screen to match the game model.""" #
        self.card_sprites.empty() #
        # Sync dealer's hand #
        for i, card in enumerate(self.game.table.cards): #
            pos = ((st.SCREEN_WIDTH/2 - (len(self.game.table.cards)*20)/2 + i * 20)*st.SCALE, 120) #
            image_key = card.sprite()
            self.card_sprites.add(CardSprite(pos, self.card_images[image_key])) #
        # Sync player's hand #
        for i, card in enumerate(self.game.player.cards): #
            pos = ((st.SCREEN_WIDTH/2 - (len(self.game.player.cards)*20)/2 + i * 20)*st.SCALE, (st.SCREEN_HEIGHT*6/8 +i*15)*st.SCALE) #
            image_key = card.sprite() #
            self.card_sprites.add(CardSprite(pos, self.card_images[image_key])) #

    def draw(self): #
        self.screen.blit(self._background, (0, 0)) #
        self.sync_sprites_with_model() #
        self.card_sprites.draw(self.screen) #
        
        # Draw scores #
        dealer_score_text = f"Dealer's Hand: {self.game.table.sumValues()}" #
        player_score_text = f"{self.game.player.name}'s Hand: {self.game.player.sumValues()}" #
        self.draw_text_with_outline(self.screen, dealer_score_text, self.font, (st.SCREEN_WIDTH/2, 40), st.WHITE, st.BLACK) #
        self.draw_text_with_outline(self.screen, player_score_text, self.font, (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT*4/5+100), st.WHITE, st.BLACK) #

        # Draw prompts or results #
        if self.game.state == "BET":
            pygame.draw.rect(self.screen, st.BLACK, self.__box_rect)  # fundo da caixa
            pygame.draw.rect(self.screen, st.WHITE, self.__box_rect, 2)  # borda branca

            # Renderiza o texto do prompt
            prompt_surface = self.font.render(self.prompt_text, True, st.WHITE)
            prompt_rect = prompt_surface.get_rect(center=(st.SCREEN_WIDTH / 2, st.SCREEN_HEIGHT / 2 - 40))
            self.screen.blit(prompt_surface, prompt_rect)

            # Renderiza o valor digitado
            input_surface = self.font.render(self.input_value, True, st.GREEN)
            input_rect = input_surface.get_rect(center=(st.SCREEN_WIDTH / 2, st.SCREEN_HEIGHT / 2 + 10))
            self.screen.blit(input_surface, input_rect)
    
        elif self.game.state == "PLAYER_TURN": #
            prompt = f'{self.game.player.points}$' #
            self.draw_text_with_outline(self.screen, prompt, self.font, (st.SCREEN_WIDTH*1/8, st.SCREEN_HEIGHT*1/12), st.GREEN, st.BLACK) #

            prompt = "Z Hit" #
            self.draw_text_with_outline(self.screen, prompt, self.font, (st.SCREEN_WIDTH*7/8, st.SCREEN_HEIGHT*11/12), st.GREEN, st.BLACK) #
            prompt = "X Stand" #
            self.draw_text_with_outline(self.screen, prompt, self.font, (st.SCREEN_WIDTH*7/8, st.SCREEN_HEIGHT*11/12-25), st.GREEN, st.BLACK) #

        elif self.game.state == "ROUND_OVER": #
            result_text = f"Result: {self.game.result}" #
            prompt = "Press [Z] to play again." if self.game.player.getPoints() >= 10 else "Not enough points. Press [Z] to exit." #
            self.draw_text_with_outline(self.screen, result_text, pygame.font.Font(st.text_font, 32), (st.SCREEN_WIDTH/2, 240), st.MAGENTA, st.BLACK) #
            self.draw_text_with_outline(self.screen, prompt, self.font, (st.SCREEN_WIDTH/2, 280), st.WHITE, st.BLACK) #
            
            

    def get_player_data(self): #
        """Returns the updated player data when the game is over.""" #
        return self.game.get_player_data() #
    
class UnoScreen(Screen):
    def __init__(self, screen, game_instance):
        super().__init__(screen)
        self.__game = game_instance
        self.set_background(os.path.join(st.img_folder, "games/uno/mesa.png"))
        self.__selected_card = 0
        self.__selected_color = 0
        self.__card_sprites = pygame.sprite.Group() 
        self.load_card_images()

    def load_card_images(self): #
        """Pre-loads all card images into a dictionary for quick access.""" #
        self.card_images = {} #
        cards_path = os.path.join(st.img_folder, "games/uno/cards") #
        for filename in os.listdir(cards_path): #
            if filename.endswith(".png"): #
                key = filename.replace(".png", "") # e.g., "blue_2" #
                image = pygame.image.load(os.path.join(cards_path, filename)).convert_alpha() #
                self.card_images[key] = pygame.transform.scale(image, (st.UNO_CARD_WIDTH, st.UNO_CARD_HEIGHT))

    def sync_sprites_with_model(self):
        self.__card_sprites.empty()
    # Sync Bot1 hand #
        for i, card in enumerate(self.__game.getPlayers()[1].getCards()): #
            pos = (st.SCREEN_WIDTH*9/10 , (st.SCREEN_HEIGHT/2 - (len(self.__game.getPlayers()[3].getCards())*25)/2 + i * 25)*st.SCALE) #
            image_key = card.getSprite()
            self.__card_sprites.add(CardSprite(pos, pygame.transform.rotate(self.card_images[image_key],90))) #
    # Sync Bot2 hand #
        for i, card in enumerate(self.__game.getPlayers()[2].getCards()): #
            pos = ((st.SCREEN_WIDTH/2 - (len(self.__game.getPlayers()[2].getCards())*25)/2 + i * 25)*st.SCALE, st.SCREEN_HEIGHT*1/8) #
            image_key = card.getSprite()
            self.__card_sprites.add(CardSprite(pos, pygame.transform.rotate(self.card_images[image_key],180))) #
    # Sync Bot3 hand #
        for i, card in enumerate(self.__game.getPlayers()[3].getCards()): #
            pos = (st.SCREEN_WIDTH*1/10 , (st.SCREEN_HEIGHT/2 - (len(self.__game.getPlayers()[3].getCards())*25)/2 + i * 25)*st.SCALE) #
            image_key = card.getSprite()
            self.__card_sprites.add(CardSprite(pos, pygame.transform.rotate(self.card_images[image_key],-90))) #
    # Sync Player hand #
        for i, card in enumerate(self.__game.getPlayers()[0].getCards()): #
            posx=(st.SCREEN_WIDTH/2 - (len(self.__game.getPlayers()[0].getCards())*25)/2 + i * 25)*st.SCALE
            posy=st.SCREEN_HEIGHT*7/8
            if self.__selected_card == -1:
                pos = (posx, posy)
            elif i == self.__selected_card:
                pos = (posx-25, posy-30)
            elif i < self.__selected_card:
                pos = (posx-25, posy)
            else:
                pos = (posx+25, posy) #
            image_key = card.getSprite()
            self.__card_sprites.add(CardSprite(pos, self.card_images[image_key])) #

    # Sync Discard Deck #
        
        pos = (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2)
        image_key = self.__game.getDiscDeck().topCard().getSprite()   
        self.__card_sprites.add(CardSprite(pos, self.card_images[image_key]))

    # Sync Buy Deck #
        image_key = self.__game.getBuyDeck().topCard().getSprite()
        for i in range(int(self.__game.getBuyDeck().size()/10)):
            pos = (st.SCREEN_WIDTH*7/10+i, st.SCREEN_HEIGHT*2/5)
            if i == int(self.__game.getBuyDeck().size()/10)-1 and self.__selected_card == -1:
                pos = (st.SCREEN_WIDTH*7/10+i, st.SCREEN_HEIGHT*2/5+30)
            self.__card_sprites.add(CardSprite(pos, self.card_images[image_key])) #
            
    def draw(self):
        self.screen.blit(self._background, (0, 0))
        self.sync_sprites_with_model()
        self.__card_sprites.draw(self.screen)  
        #place de rotacion image        
        if self.__game.getPlayers().getRotation() == 1:
            rotation_image = pygame.image.load(os.path.join(st.img_folder, "games/uno/rotation.png")).convert_alpha()
            rect = rotation_image.get_rect(center=(st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2))
            self.screen.blit(rotation_image, rect)
        else:
            rotation_image = pygame.image.load(os.path.join(st.img_folder, "games/uno/rotation.png")).convert_alpha()
            rotation_image = pygame.transform.flip(rotation_image, True, False)
            rect = rotation_image.get_rect(center=(st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2))
            self.screen.blit(rotation_image, rect)

        
            

        if self.__game.getState() != "PLAYER_TURN":
            self.__selected_card = -2


        if self.__game.getState() == "PLAYER_SELEC_COLOR":
            colors = ['red','yellow','green','blue']
            color_buttons = [
                Button((st.SCREEN_WIDTH/2 - 150, st.SCREEN_HEIGHT/2+100), "Red", "red", 30),
                Button((st.SCREEN_WIDTH/2 - 50, st.SCREEN_HEIGHT/2+100), "Yellow", "yellow", 30),
                Button((st.SCREEN_WIDTH/2 + 50, st.SCREEN_HEIGHT/2+100), "Green", "green", 30),
                Button((st.SCREEN_WIDTH/2 + 150, st.SCREEN_HEIGHT/2+100), "Blue", "blue", 30)
            ]
            for i, button in enumerate(color_buttons):
                button.set_selected(i == self.__selected_color)
            color_sprite_group = pygame.sprite.Group(color_buttons)
            self.__game.getDiscDeck().topCard().setColor(colors[self.__selected_color])
            color_sprite_group.update()
            color_sprite_group.draw(self.screen)
            self.draw_text_with_outline(self.screen, "Select a color", pygame.font.Font(st.button_font, 30), (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2-100), st.WHITE, st.BLACK)

                  

    def handle_event(self, event):
        # Possible states: START, PLAYER_TURN, PLAYER_SELEC_COLOR, BOT_TURN, ,ROUND_OVER
        if self.__game.getState() == "START":
            self.__game.start_round()

        elif self.__game.getState() == "PLAYER_TURN":
            #print("PLAYER TURN")
            player_cards = self.__game.getPlayers().getHumanPlayer().getCards()

            if event.type == pygame.KEYDOWN: #
                if event.key in (pygame.K_LEFT, pygame.K_a): #
                    self.select_sound.play() #
                    self.__selected_card = ((self.__selected_card - 1) % (self.__game.getPlayers().getHumanPlayer().size()+1)) #
                elif event.key in (pygame.K_RIGHT, pygame.K_d): #
                    self.select_sound.play() #
                    self.__selected_card = ((self.__selected_card + 1) % (self.__game.getPlayers().getHumanPlayer().size()+1)) #
                elif event.key in (pygame.K_z, pygame.K_RETURN): #
                    if self.__selected_card >= 0:
                        self.__game.player_play_card(self.__selected_card)    
                    elif self.__selected_card == -1:
                        self.__game.human_draw_card()
                    self.__selected_card = 0

                if self.__selected_card == self.__game.getPlayers().getHumanPlayer().size():
                    self.__selected_card = -1
        
        elif self.__game.getState() == "PLAYER_SELEC_COLOR":
            print("PLAYER SELEC COLOR")
            colors = ['red','yellow','green','blue']

            if event.type == pygame.KEYDOWN: #
                if event.key in (pygame.K_RIGHT, pygame.K_d): #
                    self.select_sound.play() #
                    self.__selected_color = (self.__selected_color + 1) % len(colors) #
                elif event.key in (pygame.K_LEFT, pygame.K_a): #
                    self.select_sound.play() #
                    self.__selected_color = (self.__selected_color - 1) % len(colors) #
                elif event.key in (pygame.K_z, pygame.K_RETURN): #
                    self.__game.human_select_color(colors[self.__selected_color])

        elif self.__game.getState() == "BOT_TURN":
            #print("BOT TURN")
            pass
        
        elif self.__game.getState() == "ROUND_OVER":
            print("ROUND OVER")

                    


class NotificationScreen(Screen): #
    """A simple screen to display a message for a short time before transitioning.""" #
    def __init__(self, screen, message, next_screen, player_data=None): #
        super().__init__(screen, player_data) #
        self.message = message #
        self.next_screen_key = next_screen #
        self.font = pygame.font.Font(st.button_font, st.title_size) #
        self.set_background(os.path.join(st.img_folder, "title.png")) #
        self.entry_time = pygame.time.get_ticks() #

    def handle_event(self, event): #
        # Transition on key press or after a delay #
        if event.type == pygame.KEYDOWN or pygame.time.get_ticks() - self.entry_time > 2000: #
            self.next_screen = self.next_screen_key #
            
    def draw(self): #
        self.screen.blit(self._background, (0,0)) #
        self.draw_text_with_outline(self.screen, self.message, self.font, (st.SCREEN_WIDTH/2, st.SCREEN_HEIGHT/2), st.WHITE, st.BLACK) #

# --- SPRITE CLASSES ---

class Button(pygame.sprite.Sprite): #
    def __init__(self, xy_pos, message, action, font_size=st.button_size): #
        super().__init__() #
        self.__message = message #
        self.action = action #
        self.__font = pygame.font.Font(st.button_font, font_size) #
        self.__is_selected = False #
        self.__colors = [st.WHITE, st.GREEN] #
        self.image = self.__font.render(self.__message, True, self.__colors[0]) #
        self.rect = self.image.get_rect(center=xy_pos) #
    
    def set_selected(self, is_selected): #
        self.__is_selected = is_selected #

    def update(self): #
        color = self.__colors[1] if self.__is_selected else self.__colors[0] #
        self.image = self.__font.render(self.__message, True, color) #

class CardSprite(pygame.sprite.Sprite): #
    def __init__(self, pos, image): #
        super().__init__() #
        self.image = image #
        self.rect = self.image.get_rect(center=pos) #